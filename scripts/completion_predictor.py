#!/usr/bin/env python3
"""
Completion Prediction Algorithms
Predict task completion times using historical data.
"""

import time
import json
import threading
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from collections import defaultdict, deque
import statistics
import math


@dataclass
class TaskRecord:
    task_id: str
    agent_id: str
    task_type: str
    start_time: float
    end_time: float
    duration: float
    success: bool
    features: Dict[str, Any] = field(default_factory=dict)  # Task features for prediction
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PredictionResult:
    task_id: str
    predicted_duration: float
    confidence: float  # 0.0 to 1.0
    predicted_end_time: float
    prediction_time: float
    features_used: List[str] = field(default_factory=list)
    similar_tasks: List[str] = field(default_factory=list)
    prediction_method: str = "historical_average"


class CompletionPredictor:
    def __init__(self, prediction_file: Path = None, max_history: int = 10000):
        self.prediction_file = prediction_file or Path(".completion_predictions.json")
        self.max_history = max_history
        self.task_records: deque = deque(maxlen=max_history)
        self.task_type_stats: Dict[str, Dict[str, List]] = defaultdict(lambda: defaultdict(list))
        self.agent_stats: Dict[str, Dict[str, List]] = defaultdict(lambda: defaultdict(list))
        self.feature_stats: Dict[str, Dict[str, List]] = defaultdict(lambda: defaultdict(list))
        self._lock = threading.RLock()
        self.load_prediction_data()

    def record_task_completion(self, record: TaskRecord):
        """Record a task completion for use in future predictions."""
        with self._lock:
            self.task_records.append(record)

            # Update task type statistics
            self.task_type_stats[record.task_type]['durations'].append(record.duration)
            self.task_type_stats[record.task_type]['success_rates'].append(1.0 if record.success else 0.0)

            # Update agent statistics
            self.agent_stats[record.agent_id]['durations'].append(record.duration)
            self.agent_stats[record.agent_id]['success_rates'].append(1.0 if record.success else 0.0)

            # Update feature statistics
            for feature_name, feature_value in record.features.items():
                feature_key = f"{record.task_type}_{feature_name}"
                self.feature_stats[feature_key]['values'].append(feature_value)
                self.feature_stats[feature_key]['durations'].append(record.duration)

            self._save_prediction_data()

    def predict_completion_time(self, task_id: str, task_type: str, agent_id: str,
                              features: Dict[str, Any] = None) -> PredictionResult:
        """Predict completion time for a task."""
        if features is None:
            features = {}

        prediction_time = time.time()

        # Get base prediction from task type history
        base_duration = self._get_task_type_average_duration(task_type)

        # Adjust based on agent performance
        agent_factor = self._get_agent_performance_factor(agent_id, task_type)

        # Adjust based on task features
        feature_adjustment = self._get_feature_adjustment(task_type, features)

        # Calculate final prediction
        predicted_duration = base_duration * agent_factor + feature_adjustment

        # Calculate confidence based on available data
        confidence = self._calculate_prediction_confidence(task_type, agent_id, features)

        # Get similar tasks for reference
        similar_tasks = self._get_similar_tasks(task_type, agent_id, features)

        return PredictionResult(
            task_id=task_id,
            predicted_duration=max(0.1, predicted_duration),  # Minimum 0.1 seconds
            confidence=confidence,
            predicted_end_time=prediction_time + predicted_duration,
            prediction_time=prediction_time,
            features_used=list(features.keys()),
            similar_tasks=similar_tasks[:5],  # Top 5 similar tasks
            prediction_method="weighted_historical"
        )

    def _get_task_type_average_duration(self, task_type: str) -> float:
        """Get average duration for a task type."""
        with self._lock:
            durations = self.task_type_stats[task_type]['durations']
            if not durations:
                return 60.0  # Default 1 minute for unknown task types

            # Use median to reduce impact of outliers
            return statistics.median(durations)

    def _get_agent_performance_factor(self, agent_id: str, task_type: str) -> float:
        """Get agent performance factor relative to task type average."""
        with self._lock:
            # Get agent's average duration for this task type
            agent_durations = [
                record.duration for record in self.task_records
                if record.agent_id == agent_id and record.task_type == task_type
            ]

            if not agent_durations:
                return 1.0  # No data, use average

            agent_avg = statistics.mean(agent_durations)
            task_avg = self._get_task_type_average_duration(task_type)

            if task_avg == 0:
                return 1.0

            # Return ratio of agent time to average time
            # < 1.0 means faster than average, > 1.0 means slower
            return agent_avg / task_avg

    def _get_feature_adjustment(self, task_type: str, features: Dict[str, Any]) -> float:
        """Get duration adjustment based on task features."""
        if not features:
            return 0.0

        adjustments = []

        with self._lock:
            for feature_name, feature_value in features.items():
                feature_key = f"{task_type}_{feature_name}"

                if feature_key not in self.feature_stats:
                    continue

                feature_data = self.feature_stats[feature_key]
                values = feature_data['values']
                durations = feature_data['durations']

                if not values or not durations:
                    continue

                # Find correlation between feature value and duration
                try:
                    # Simple linear correlation
                    correlation = self._calculate_correlation(values, durations)

                    # Estimate impact based on how much this feature value differs from average
                    avg_value = statistics.mean(values)
                    if avg_value != 0:
                        value_ratio = (feature_value - avg_value) / avg_value
                        adjustment = correlation * value_ratio * statistics.mean(durations)
                        adjustments.append(adjustment)
                except Exception:
                    # Skip if correlation calculation fails
                    continue

        return sum(adjustments) if adjustments else 0.0

    def _calculate_correlation(self, x: List[float], y: List[float]) -> float:
        """Calculate Pearson correlation coefficient."""
        if len(x) != len(y) or len(x) < 2:
            return 0.0

        try:
            mean_x = statistics.mean(x)
            mean_y = statistics.mean(y)

            numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x)))
            sum_sq_x = sum((x[i] - mean_x) ** 2 for i in range(len(x)))
            sum_sq_y = sum((y[i] - mean_y) ** 2 for i in range(len(y)))

            if sum_sq_x == 0 or sum_sq_y == 0:
                return 0.0

            correlation = numerator / math.sqrt(sum_sq_x * sum_sq_y)
            return max(-1.0, min(1.0, correlation))  # Clamp to [-1, 1]
        except Exception:
            return 0.0

    def _calculate_prediction_confidence(self, task_type: str, agent_id: str,
                                       features: Dict[str, Any]) -> float:
        """Calculate confidence level for prediction."""
        confidence_factors = []

        with self._lock:
            # Confidence based on task type history
            task_durations = self.task_type_stats[task_type]['durations']
            if task_durations:
                # More samples = higher confidence
                sample_confidence = min(1.0, len(task_durations) / 50.0)  # 50+ samples = full confidence
                confidence_factors.append(sample_confidence)
            else:
                confidence_factors.append(0.2)  # Low confidence for unknown task types

            # Confidence based on agent history
            agent_durations = [
                record.duration for record in self.task_records
                if record.agent_id == agent_id and record.task_type == task_type
            ]
            if agent_durations:
                agent_sample_confidence = min(1.0, len(agent_durations) / 10.0)  # 10+ samples = full confidence
                confidence_factors.append(agent_sample_confidence)
            else:
                confidence_factors.append(0.5)  # Medium confidence if no agent history

            # Confidence based on feature data
            if features:
                feature_confidences = []
                for feature_name in features.keys():
                    feature_key = f"{task_type}_{feature_name}"
                    if feature_key in self.feature_stats:
                        feature_values = self.feature_stats[feature_key]['values']
                        feature_confidences.append(min(1.0, len(feature_values) / 20.0))
                    else:
                        feature_confidences.append(0.3)  # Low confidence for unknown features

                if feature_confidences:
                    confidence_factors.append(statistics.mean(feature_confidences))
                else:
                    confidence_factors.append(0.4)  # Medium-low confidence if no features
            else:
                confidence_factors.append(0.6)  # Higher confidence if no features needed

        # Combine confidence factors (geometric mean)
        if not confidence_factors:
            return 0.5

        product = 1.0
        for factor in confidence_factors:
            product *= max(0.01, factor)  # Avoid zero

        geometric_mean = product ** (1.0 / len(confidence_factors))
        return geometric_mean

    def _get_similar_tasks(self, task_type: str, agent_id: str,
                          features: Dict[str, Any]) -> List[str]:
        """Get IDs of similar tasks for reference."""
        similar_tasks = []

        with self._lock:
            # Find tasks of the same type by the same agent
            for record in self.task_records:
                if (record.task_type == task_type and
                    record.agent_id == agent_id and
                    record.task_id not in similar_tasks):
                    similar_tasks.append(record.task_id)

        return similar_tasks

    def get_prediction_accuracy(self, hours: int = 24) -> Dict[str, Any]:
        """Get accuracy statistics for recent predictions."""
        # This would require storing actual vs predicted times
        # For now, we'll return placeholder data
        return {
            'time_window_hours': hours,
            'total_predictions': 0,
            'accurate_predictions': 0,
            'accuracy_rate': 0.0,
            'average_error_seconds': 0.0,
            'median_error_seconds': 0.0
        }

    def get_prediction_trends(self) -> Dict[str, Any]:
        """Get trends in prediction accuracy over time."""
        # This would analyze how prediction accuracy changes over time
        return {
            'trend_data_available': False,
            'improving': None,
            'confidence_correlation_with_accuracy': 0.0
        }

    def _save_prediction_data(self):
        """Save prediction data to file."""
        try:
            data = {
                'timestamp': time.time(),
                'task_records': [
                    {
                        'task_id': record.task_id,
                        'agent_id': record.agent_id,
                        'task_type': record.task_type,
                        'start_time': record.start_time,
                        'end_time': record.end_time,
                        'duration': record.duration,
                        'success': record.success,
                        'features': record.features,
                        'metadata': record.metadata
                    }
                    for record in self.task_records
                ],
                'task_type_stats': {
                    task_type: dict(stats)
                    for task_type, stats in self.task_type_stats.items()
                },
                'agent_stats': {
                    agent_id: dict(stats)
                    for agent_id, stats in self.agent_stats.items()
                },
                'feature_stats': {
                    feature_key: dict(stats)
                    for feature_key, stats in self.feature_stats.items()
                }
            }

            with open(self.prediction_file, 'w') as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"Error saving prediction data: {e}")

    def load_prediction_data(self):
        """Load prediction data from file."""
        try:
            if not self.prediction_file.exists():
                return

            with open(self.prediction_file, 'r') as f:
                data = json.load(f)

            # Restore task records
            self.task_records.clear()
            for record_data in data.get('task_records', []):
                record = TaskRecord(
                    task_id=record_data['task_id'],
                    agent_id=record_data['agent_id'],
                    task_type=record_data['task_type'],
                    start_time=record_data['start_time'],
                    end_time=record_data['end_time'],
                    duration=record_data['duration'],
                    success=record_data['success'],
                    features=record_data.get('features', {}),
                    metadata=record_data.get('metadata', {})
                )
                self.task_records.append(record)

            # Restore task type stats
            self.task_type_stats.clear()
            for task_type, stats in data.get('task_type_stats', {}).items():
                task_stats = defaultdict(list)
                for stat_name, stat_values in stats.items():
                    task_stats[stat_name] = stat_values
                self.task_type_stats[task_type] = task_stats

            # Restore agent stats
            self.agent_stats.clear()
            for agent_id, stats in data.get('agent_stats', {}).items():
                agent_stats = defaultdict(list)
                for stat_name, stat_values in stats.items():
                    agent_stats[stat_name] = stat_values
                self.agent_stats[agent_id] = agent_stats

            # Restore feature stats
            self.feature_stats.clear()
            for feature_key, stats in data.get('feature_stats', {}).items():
                feature_stats = defaultdict(list)
                for stat_name, stat_values in stats.items():
                    feature_stats[stat_name] = stat_values
                self.feature_stats[feature_key] = feature_stats

        except Exception as e:
            print(f"Error loading prediction data: {e}")


class PredictionDashboard:
    def __init__(self, predictor: CompletionPredictor):
        self.predictor = predictor

    def display_prediction(self, prediction: PredictionResult):
        """Display a prediction result."""
        from datetime import datetime

        predicted_end = datetime.fromtimestamp(prediction.predicted_end_time)
        current_time = datetime.fromtimestamp(prediction.prediction_time)

        print(f"\nTask Completion Prediction - {prediction.task_id}")
        print("=" * 50)
        print(f"Predicted Duration: {prediction.predicted_duration:.1f} seconds "
              f"({prediction.predicted_duration/60:.1f} minutes)")
        print(f"Predicted Completion: {predicted_end.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Confidence: {prediction.confidence:.1%}")
        print(f"Prediction Method: {prediction.prediction_method}")

        if prediction.features_used:
            print(f"Features Used: {', '.join(prediction.features_used)}")

        if prediction.similar_tasks:
            print(f"Similar Tasks: {', '.join(prediction.similar_tasks[:3])}")

    def display_prediction_accuracy(self):
        """Display prediction accuracy statistics."""
        accuracy = self.predictor.get_prediction_accuracy()

        print(f"\nPrediction Accuracy Report")
        print("=" * 28)
        print(f"Time Window: {accuracy['time_window_hours']} hours")
        print(f"Total Predictions: {accuracy['total_predictions']}")
        print(f"Accurate Predictions: {accuracy['accurate_predictions']}")
        print(f"Accuracy Rate: {accuracy['accuracy_rate']:.1%}")
        print(f"Average Error: {accuracy['average_error_seconds']:.1f} seconds")
        print(f"Median Error: {accuracy['median_error_seconds']:.1f} seconds")

    def display_prediction_trends(self):
        """Display prediction trends."""
        trends = self.predictor.get_prediction_trends()

        print(f"\nPrediction Trends")
        print("=" * 18)
        if trends['trend_data_available']:
            print(f"Trend: {'Improving' if trends['improving'] else 'Deteriorating'}")
            print(f"Confidence-Accuracy Correlation: {trends['confidence_correlation_with_accuracy']:.2f}")
        else:
            print("No trend data available")


def main():
    # Example usage
    print("Completion Prediction Algorithms")
    print("=" * 35)

    # Create predictor and dashboard
    predictor = CompletionPredictor()
    dashboard = PredictionDashboard(predictor)

    print("Completion prediction system initialized")
    print("System ready to predict task completion times using historical data")

    # Example of what the workflow would look like:
    print("\nExample workflow:")
    print("  1. Record task completion data for training")
    print("  2. Analyze historical completion time patterns")
    print("  3. Predict completion times for new tasks")
    print("  4. Track prediction accuracy over time")
    print("  5. Improve predictions based on actual results")


if __name__ == "__main__":
    main()