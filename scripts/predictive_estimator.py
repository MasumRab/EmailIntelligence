#!/usr/bin/env python3
"""
Predictive Completion Time Estimation
ML-based prediction of task completion times using historical data.
"""

import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score


class TaskHistory:
    def __init__(self, task_id: str, task_type: str, estimated_time: int,
                 actual_time: int, agent_name: str, success: bool = True):
        self.task_id = task_id
        self.task_type = task_type
        self.estimated_time = estimated_time
        self.actual_time = actual_time
        self.agent_name = agent_name
        self.success = success
        self.timestamp = datetime.now().isoformat()


class PredictiveTimeEstimator:
    def __init__(self, history_file: Path = None):
        self.history_file = history_file or Path("task_history.json")
        self.history: List[TaskHistory] = []
        self.model = LinearRegression()
        self.scaler = StandardScaler()
        self.is_trained = False
        self._load_history()

    def _load_history(self):
        """Load task history from file."""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r') as f:
                    data = json.load(f)
                    for item in data:
                        history = TaskHistory(
                            item['task_id'],
                            item['task_type'],
                            item['estimated_time'],
                            item['actual_time'],
                            item['agent_name'],
                            item['success']
                        )
                        history.timestamp = item['timestamp']
                        self.history.append(history)
            except Exception as e:
                print(f"Error loading history: {e}")

    def _save_history(self):
        """Save task history to file."""
        try:
            data = []
            for item in self.history:
                data.append({
                    'task_id': item.task_id,
                    'task_type': item.task_type,
                    'estimated_time': item.estimated_time,
                    'actual_time': item.actual_time,
                    'agent_name': item.agent_name,
                    'success': item.success,
                    'timestamp': item.timestamp
                })
            with open(self.history_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving history: {e}")

    def add_task_result(self, task_id: str, task_type: str, estimated_time: int,
                       actual_time: int, agent_name: str, success: bool = True):
        """Add a completed task result to history."""
        history = TaskHistory(task_id, task_type, estimated_time, actual_time, agent_name, success)
        self.history.append(history)
        self._save_history()

        # Retrain model if we have enough data
        if len(self.history) >= 10:
            self._train_model()

    def _train_model(self):
        """Train the prediction model."""
        if len(self.history) < 5:
            return

        # Prepare features
        features = []
        targets = []

        task_type_map = {}
        agent_map = {}

        # Create mappings for categorical variables
        unique_types = list(set(h.task_type for h in self.history))
        unique_agents = list(set(h.agent_name for h in self.history))

        for i, task_type in enumerate(unique_types):
            task_type_map[task_type] = i

        for i, agent_name in enumerate(unique_agents):
            agent_map[agent_name] = i

        # Prepare training data
        for h in self.history:
            if h.success:  # Only use successful tasks for training
                # Features: [task_type_encoded, estimated_time, agent_encoded]
                feature = [
                    task_type_map.get(h.task_type, 0),
                    h.estimated_time,
                    agent_map.get(h.agent_name, 0)
                ]
                features.append(feature)
                targets.append(h.actual_time)

        if len(features) < 3:
            return

        # Convert to numpy arrays
        X = np.array(features)
        y = np.array(targets)

        # Scale features
        X_scaled = self.scaler.fit_transform(X)

        # Train model
        self.model.fit(X_scaled, y)
        self.is_trained = True

        # Calculate model performance
        y_pred = self.model.predict(X_scaled)
        mse = mean_squared_error(y, y_pred)
        r2 = r2_score(y, y_pred)

        print(f"Model trained with {len(features)} samples")
        print(f"Mean Squared Error: {mse:.2f}")
        print(f"R² Score: {r2:.2f}")

    def predict_completion_time(self, task_type: str, estimated_time: int, agent_name: str) -> Optional[float]:
        """Predict completion time for a task."""
        if not self.is_trained or len(self.history) < 5:
            # Return simple heuristic if not enough data
            return float(estimated_time * 1.2)  # Add 20% buffer

        # Prepare features for prediction
        task_type_map = {}
        agent_map = {}

        # Create mappings (in real implementation, these would be stored)
        unique_types = list(set(h.task_type for h in self.history))
        unique_agents = list(set(h.agent_name for h in self.history))

        for i, task_type_name in enumerate(unique_types):
            task_type_map[task_type_name] = i

        for i, agent_name_name in enumerate(unique_agents):
            agent_map[agent_name_name] = i

        # Encode features
        task_type_encoded = task_type_map.get(task_type, 0)
        agent_encoded = agent_map.get(agent_name, 0)

        # Prepare feature vector
        feature = np.array([[task_type_encoded, estimated_time, agent_encoded]])
        feature_scaled = self.scaler.transform(feature)

        # Make prediction
        prediction = self.model.predict(feature_scaled)[0]
        return float(max(1.0, prediction))  # Minimum 1 minute

    def get_prediction_accuracy(self) -> Dict:
        """Get prediction accuracy statistics."""
        if not self.history:
            return {"accuracy": 0.0, "total_predictions": 0}

        recent_history = [h for h in self.history if h.success][-50:]  # Last 50 successful tasks
        if not recent_history:
            return {"accuracy": 0.0, "total_predictions": 0}

        accurate_predictions = 0
        total_predictions = len(recent_history)

        for h in recent_history:
            predicted = self.predict_completion_time(h.task_type, h.estimated_time, h.agent_name)
            if predicted:
                # Consider prediction accurate if within 30% of actual time
                if abs(predicted - h.actual_time) <= (h.actual_time * 0.3):
                    accurate_predictions += 1

        accuracy = accurate_predictions / total_predictions if total_predictions > 0 else 0.0

        return {
            "accuracy": accuracy,
            "total_predictions": total_predictions,
            "accurate_predictions": accurate_predictions
        }

    def get_early_warning_tasks(self) -> List[Dict]:
        """Get tasks that are taking longer than predicted."""
        # This would be implemented in a real system with real-time monitoring
        return []

    def get_performance_trends(self) -> Dict:
        """Get performance trends over time."""
        if not self.history:
            return {}

        # Group by week and calculate average completion times
        weekly_data = {}

        for h in self.history:
            if h.success:
                timestamp = datetime.fromisoformat(h.timestamp)
                week_key = timestamp.strftime("%Y-W%U")

                if week_key not in weekly_data:
                    weekly_data[week_key] = {
                        'total_time': 0,
                        'task_count': 0,
                        'avg_estimated': 0,
                        'estimated_total': 0
                    }

                weekly_data[week_key]['total_time'] += h.actual_time
                weekly_data[week_key]['task_count'] += 1
                weekly_data[week_key]['estimated_total'] += h.estimated_time

        # Calculate averages
        for week_key, data in weekly_data.items():
            if data['task_count'] > 0:
                data['avg_actual'] = data['total_time'] / data['task_count']
                data['avg_estimated'] = data['estimated_total'] / data['task_count']
                data['efficiency'] = data['avg_estimated'] / data['avg_actual'] if data['avg_actual'] > 0 else 1.0

        return weekly_data


def main():
    # Example usage
    estimator = PredictiveTimeEstimator()

    # Add some sample data for training
    sample_data = [
        ("api-doc-1", "api", 15, 12, "api-writer", True),
        ("guide-doc-1", "guide", 20, 25, "guide-writer", True),
        ("arch-doc-1", "arch", 30, 28, "architect", True),
        ("api-doc-2", "api", 10, 8, "api-writer", True),
        ("guide-doc-2", "guide", 25, 30, "guide-writer", True),
    ]

    for task_id, task_type, est_time, actual_time, agent, success in sample_data:
        estimator.add_task_result(task_id, task_type, est_time, actual_time, agent, success)

    # Make a prediction
    predicted_time = estimator.predict_completion_time("api", 12, "api-writer")
    print(f"Predicted completion time for API task: {predicted_time:.1f} minutes")

    # Get accuracy stats
    accuracy = estimator.get_prediction_accuracy()
    print(f"Prediction accuracy: {accuracy['accuracy']:.2%}")

    print("Predictive completion time estimator initialized")


if __name__ == "__main__":
    main()