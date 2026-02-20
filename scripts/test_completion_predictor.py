#!/usr/bin/env python3
"""
Test script for completion prediction system
"""

import time
import tempfile
from pathlib import Path
from completion_predictor import CompletionPredictor, TaskRecord, PredictionResult


def test_task_recording():
    """Test recording task completions for prediction."""
    print("Testing task completion recording...")
    
    # Create temporary directory for test files
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        prediction_file = tmp_path / ".test_completion_predictions.json"
        
        # Initialize predictor
        predictor = CompletionPredictor(prediction_file=prediction_file)
        
        # Record some task completions
        tasks = [
            TaskRecord(
                task_id=f"task-{i}",
                agent_id=f"agent-{i % 3}",
                task_type="content-validation" if i % 2 == 0 else "link-check",
                start_time=time.time() - 300 + i * 60,
                end_time=time.time() - 300 + i * 60 + (30 + i * 10),
                duration=30 + i * 10,
                success=True,
                features={"file_size": 1000 + i * 500, "complexity": 1 + i % 5}
            )
            for i in range(10)
        ]
        
        # Record all tasks
        for task in tasks:
            predictor.record_task_completion(task)
        
        # Verify tasks were recorded
        assert len(predictor.task_records) == 10, "Should have recorded 10 tasks"
        
        # Check task type stats
        validation_durations = predictor.task_type_stats["content-validation"]["durations"]
        link_durations = predictor.task_type_stats["link-check"]["durations"]
        
        assert len(validation_durations) > 0, "Should have content-validation durations"
        assert len(link_durations) > 0, "Should have link-check durations"
        
        print("✓ Task completion recording test passed")


def test_basic_prediction():
    """Test basic completion time prediction."""
    print("\nTesting basic completion time prediction...")
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        prediction_file = tmp_path / ".test_completion_predictions.json"
        
        # Initialize predictor
        predictor = CompletionPredictor(prediction_file=prediction_file)
        
        # Record some historical data
        historical_tasks = [
            TaskRecord(
                task_id=f"hist-{i}",
                agent_id="test-agent",
                task_type="test-task",
                start_time=time.time() - 3600 + i * 300,
                end_time=time.time() - 3600 + i * 300 + 45,
                duration=45.0,  # 45 seconds each
                success=True
            )
            for i in range(20)
        ]
        
        # Record historical tasks
        for task in historical_tasks:
            predictor.record_task_completion(task)
        
        # Make a prediction
        prediction = predictor.predict_completion_time(
            task_id="new-task-1",
            task_type="test-task",
            agent_id="test-agent"
        )
        
        print(f"Prediction: {prediction.predicted_duration:.1f} seconds")
        print(f"Confidence: {prediction.confidence:.1%}")
        
        # Verify prediction structure
        assert isinstance(prediction, PredictionResult), "Should return PredictionResult"
        assert prediction.task_id == "new-task-1", "Task ID should match"
        assert prediction.predicted_duration > 0, "Predicted duration should be positive"
        assert 0 <= prediction.confidence <= 1, "Confidence should be between 0 and 1"
        
        # With good historical data, confidence should be reasonable
        assert prediction.confidence > 0.5, "Confidence should be reasonable with good data"
        
        print("✓ Basic completion time prediction test passed")


def test_agent_performance_factor():
    """Test agent performance factor calculation."""
    print("\nTesting agent performance factor calculation...")
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        prediction_file = tmp_path / ".test_completion_predictions.json"
        
        # Initialize predictor
        predictor = CompletionPredictor(prediction_file=prediction_file)
        
        # Record tasks with different agents having different performance
        # Fast agent: consistently completes in 20 seconds
        fast_agent_tasks = [
            TaskRecord(
                task_id=f"fast-{i}",
                agent_id="fast-agent",
                task_type="standard-task",
                start_time=time.time() - 3600 + i * 300,
                end_time=time.time() - 3600 + i * 300 + 20,
                duration=20.0,
                success=True
            )
            for i in range(10)
        ]
        
        # Slow agent: consistently completes in 60 seconds
        slow_agent_tasks = [
            TaskRecord(
                task_id=f"slow-{i}",
                agent_id="slow-agent",
                task_type="standard-task",
                start_time=time.time() - 3600 + i * 300,
                end_time=time.time() - 3600 + i * 300 + 60,
                duration=60.0,
                success=True
            )
            for i in range(10)
        ]
        
        # Record all tasks
        for task in fast_agent_tasks + slow_agent_tasks:
            predictor.record_task_completion(task)
        
        # Get performance factors
        fast_factor = predictor._get_agent_performance_factor("fast-agent", "standard-task")
        slow_factor = predictor._get_agent_performance_factor("slow-agent", "standard-task")
        avg_factor = predictor._get_agent_performance_factor("average-agent", "standard-task")
        
        print(f"Fast agent factor: {fast_factor:.2f}")
        print(f"Slow agent factor: {slow_factor:.2f}")
        print(f"Average agent factor: {avg_factor:.2f}")
        
        # Fast agent should have factor < 1.0 (faster than average)
        assert fast_factor < 1.0, "Fast agent should have factor < 1.0"
        
        # Slow agent should have factor > 1.0 (slower than average)
        assert slow_factor > 1.0, "Slow agent should have factor > 1.0"
        
        # Unknown agent should have factor = 1.0 (average)
        assert avg_factor == 1.0, "Unknown agent should have factor = 1.0"
        
        print("✓ Agent performance factor calculation test passed")


def test_feature_adjustment():
    """Test feature-based duration adjustment."""
    print("\nTesting feature-based duration adjustment...")
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        prediction_file = tmp_path / ".test_completion_predictions.json"
        
        # Initialize predictor
        predictor = CompletionPredictor(prediction_file=prediction_file)
        
        # Record tasks with features that affect duration
        # Tasks with larger file sizes take longer
        feature_tasks = [
            TaskRecord(
                task_id=f"feature-{i}",
                agent_id="feature-agent",
                task_type="file-processing",
                start_time=time.time() - 3600 + i * 300,
                end_time=time.time() - 3600 + i * 300 + (20 + i * 5),  # Increasing duration
                duration=20 + i * 5,
                success=True,
                features={"file_size": 1000 + i * 1000}  # Increasing file size
            )
            for i in range(15)
        ]
        
        # Record feature tasks
        for task in feature_tasks:
            predictor.record_task_completion(task)
        
        # Test feature adjustment
        adjustment = predictor._get_feature_adjustment(
            "file-processing",
            {"file_size": 5000}  # Large file size
        )
        
        print(f"Feature adjustment: {adjustment:.2f} seconds")
        
        # Should return a numeric value (could be positive or negative)
        assert isinstance(adjustment, (int, float)), "Adjustment should be numeric"
        
        print("✓ Feature-based duration adjustment test passed")


def test_prediction_confidence():
    """Test prediction confidence calculation."""
    print("\nTesting prediction confidence calculation...")
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        prediction_file = tmp_path / ".test_completion_predictions.json"
        
        # Initialize predictor
        predictor = CompletionPredictor(prediction_file=prediction_file)
        
        # Test confidence with no data
        no_data_confidence = predictor._calculate_prediction_confidence(
            "unknown-task", "unknown-agent", {}
        )
        print(f"No data confidence: {no_data_confidence:.2f}")
        
        # Record some data
        for i in range(30):
            task = TaskRecord(
                task_id=f"conf-{i}",
                agent_id="conf-agent" if i < 20 else "other-agent",
                task_type="conf-task",
                start_time=time.time() - 3600 + i * 120,
                end_time=time.time() - 3600 + i * 120 + 30,
                duration=30.0,
                success=True
            )
            predictor.record_task_completion(task)
        
        # Test confidence with good data
        good_data_confidence = predictor._calculate_prediction_confidence(
            "conf-task", "conf-agent", {}
        )
        print(f"Good data confidence: {good_data_confidence:.2f}")
        
        # Confidence with good data should be higher than with no data
        assert good_data_confidence > no_data_confidence, "Good data should give higher confidence"
        
        # Confidence should be between 0 and 1
        assert 0 <= good_data_confidence <= 1, "Confidence should be between 0 and 1"
        
        print("✓ Prediction confidence calculation test passed")


def test_prediction_with_features():
    """Test prediction with task features."""
    print("\nTesting prediction with task features...")
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        prediction_file = tmp_path / ".test_completion_predictions.json"
        
        # Initialize predictor
        predictor = CompletionPredictor(prediction_file=prediction_file)
        
        # Record tasks with features
        for i in range(25):
            task = TaskRecord(
                task_id=f"feature-task-{i}",
                agent_id="feature-agent",
                task_type="complex-task",
                start_time=time.time() - 3600 + i * 150,
                end_time=time.time() - 3600 + i * 150 + (40 + i * 2),
                duration=40 + i * 2,
                success=True,
                features={
                    "complexity": 1 + (i % 5),
                    "file_count": 10 + i * 2,
                    "requires_api": i % 3 == 0
                }
            )
            predictor.record_task_completion(task)
        
        # Make prediction with features
        prediction = predictor.predict_completion_time(
            task_id="new-complex-task",
            task_type="complex-task",
            agent_id="feature-agent",
            features={
                "complexity": 4,
                "file_count": 50,
                "requires_api": True
            }
        )
        
        print(f"Feature-based prediction: {prediction.predicted_duration:.1f} seconds")
        print(f"Confidence: {prediction.confidence:.1%}")
        print(f"Features used: {prediction.features_used}")
        
        # Verify prediction structure
        assert isinstance(prediction, PredictionResult), "Should return PredictionResult"
        assert prediction.predicted_duration > 0, "Predicted duration should be positive"
        assert len(prediction.features_used) > 0, "Should have used features"
        
        print("✓ Prediction with task features test passed")


def test_prediction_persistence():
    """Test prediction data persistence."""
    print("\nTesting prediction data persistence...")
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        prediction_file = tmp_path / ".test_persistence_predictions.json"
        
        # Initialize predictor and add data
        predictor1 = CompletionPredictor(prediction_file=prediction_file)
        
        # Add test data
        test_task = TaskRecord(
            task_id="persistence-test",
            agent_id="persistence-agent",
            task_type="persistence-task",
            start_time=time.time() - 600,
            end_time=time.time() - 550,
            duration=50.0,
            success=True,
            features={"test_feature": 123}
        )
        
        predictor1.record_task_completion(test_task)
        
        # Create new predictor and load data
        predictor2 = CompletionPredictor(prediction_file=prediction_file)
        predictor2.load_prediction_data()
        
        # Verify data was loaded correctly
        assert len(predictor2.task_records) == 1, "Should have loaded one task record"
        assert len(predictor2.task_type_stats["persistence-task"]["durations"]) == 1, "Should have task type stats"
        assert len(predictor2.agent_stats["persistence-agent"]["durations"]) == 1, "Should have agent stats"
        
        loaded_task = predictor2.task_records[0]
        assert loaded_task.task_id == "persistence-test", "Task ID should match"
        assert loaded_task.duration == 50.0, "Duration should match"
        assert loaded_task.features["test_feature"] == 123, "Features should match"
        
        print("✓ Prediction data persistence test passed")


def main():
    """Run all tests."""
    print("Running Completion Prediction Tests")
    print("=" * 38)
    
    try:
        test_task_recording()
        test_basic_prediction()
        test_agent_performance_factor()
        test_feature_adjustment()
        test_prediction_confidence()
        test_prediction_with_features()
        test_prediction_persistence()
        
        print("\n" + "=" * 38)
        print("All tests passed! ✓")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        raise


if __name__ == "__main__":
    main()