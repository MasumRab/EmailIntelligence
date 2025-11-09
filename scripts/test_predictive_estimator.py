#!/usr/bin/env python3
"""
Test script for predictive completion time estimator
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__)))

from predictive_estimator import PredictiveTimeEstimator


def test_predictive_estimator():
    """Test the predictive completion time estimator."""
    print("Testing Predictive Completion Time Estimator...")

    # Create estimator
    estimator = PredictiveTimeEstimator()

    # Add some sample data for training
    sample_data = [
        ("api-doc-1", "api", 15, 12, "api-writer", True),
        ("guide-doc-1", "guide", 20, 25, "guide-writer", True),
        ("arch-doc-1", "arch", 30, 28, "architect", True),
        ("api-doc-2", "api", 10, 8, "api-writer", True),
        ("guide-doc-2", "guide", 25, 30, "guide-writer", True),
        ("api-doc-3", "api", 18, 20, "api-writer", True),
        ("guide-doc-3", "guide", 22, 24, "guide-writer", True),
        ("arch-doc-2", "arch", 35, 32, "architect", True),
    ]

    for task_id, task_type, est_time, actual_time, agent, success in sample_data:
        estimator.add_task_result(
            task_id, task_type, est_time, actual_time, agent, success
        )

    # Make predictions
    predicted_api = estimator.predict_completion_time("api", 15, "api-writer")
    predicted_guide = estimator.predict_completion_time("guide", 20, "guide-writer")
    predicted_arch = estimator.predict_completion_time("arch", 30, "architect")

    print(f"Predicted completion time for API task: {predicted_api:.1f} minutes")
    print(f"Predicted completion time for Guide task: {predicted_guide:.1f} minutes")
    print(f"Predicted completion time for Arch task: {predicted_arch:.1f} minutes")

    # Get accuracy stats
    accuracy = estimator.get_prediction_accuracy()
    print(f"Prediction accuracy: {accuracy['accuracy']:.2%}")
    print(f"Total predictions: {accuracy['total_predictions']}")

    # Get performance trends
    trends = estimator.get_performance_trends()
    print(f"Performance trends calculated for {len(trends)} weeks")

    print("Predictive estimator test completed successfully!")


if __name__ == "__main__":
    test_predictive_estimator()
