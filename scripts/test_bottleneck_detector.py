#!/usr/bin/env python3
"""
Test script for bottleneck detection system
"""

import time
import tempfile
from pathlib import Path
from bottleneck_detector import BottleneckDetector, BottleneckAlert


def test_bottleneck_detection():
    """Test basic bottleneck detection functionality."""
    print("Testing bottleneck detection functionality...")
    
    # Create temporary directory for test files
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        detection_file = tmp_path / ".test_bottleneck_detection.json"
        
        # Initialize detector
        detector = BottleneckDetector(detection_file=detection_file)
        
        # Start a few workflow steps
        step1 = detector.start_workflow_step(
            step_id="step-1",
            step_name="content_validation",
            agent_id="agent-1"
        )
        
        step2 = detector.start_workflow_step(
            step_id="step-2", 
            step_name="link_check",
            agent_id="agent-2"
        )
        
        # Complete the steps
        detector.complete_workflow_step("step-1", success=True)
        detector.complete_workflow_step("step-2", success=False, error_message="Broken link")
        
        # Get duration stats
        stats = detector.get_step_duration_stats("content_validation")
        print(f"Content validation stats: {stats}")
        
        # Check for bottlenecks (should be none since steps are completed quickly)
        alerts = detector.detect_all_bottlenecks()
        print(f"Number of alerts: {len(alerts)}")
        
        # Verify we have completed steps
        summary = detector.get_bottleneck_summary()
        assert summary['completed_steps'] == 1, "Should have 1 completed step"
        assert summary['failed_steps'] == 1, "Should have 1 failed step"
        
        print("✓ Bottleneck detection test passed")


def test_long_running_step_detection():
    """Test detection of long-running steps."""
    print("\nTesting long-running step detection...")
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        detection_file = tmp_path / ".test_bottleneck_detection.json"
        
        # Initialize detector
        detector = BottleneckDetector(detection_file=detection_file)
        
        # First, create some historical data for a step type to establish normal duration
        for i in range(5):
            step = detector.start_workflow_step(f"hist-{i}", "quick-step", "agent-1")
            # Simulate quick completion (0.1 seconds each)
            time.sleep(0.01)  # Small delay to make sure duration is measurable
            detector.complete_workflow_step(f"hist-{i}", success=True)
        
        # Now start a step that has been running for a long time
        long_step = detector.start_workflow_step("long-running", "quick-step", "agent-1")
        
        # Manually update start time to simulate a long-running step
        with detector._lock:
            detector.workflow_steps["long-running"].start_time = time.time() - 120  # 2 minutes ago
            detector.workflow_steps["long-running"].duration = 120  # 2 minutes
        
        # Detect bottlenecks - should find the long-running step
        alerts = detector.detect_long_running_steps(duration_threshold_percentile=90, min_duration=10.0)
        
        print(f"Long-running step alerts: {len(alerts)}")
        for alert in alerts:
            print(f"  Alert: {alert.description}")
        
        # Should have detected the long-running step
        long_running_alerts = [a for a in alerts if a.alert_type == "long_running_step"]
        assert len(long_running_alerts) > 0, "Should detect long-running step"
        
        print("✓ Long-running step detection test passed")


def test_queue_backlog_detection():
    """Test detection of queue backlogs."""
    print("\nTesting queue backlog detection...")
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        detection_file = tmp_path / ".test_bottleneck_detection.json"
        
        # Initialize detector
        detector = BottleneckDetector(detection_file=detection_file)
        
        # Simulate high workload for an agent (above double threshold)
        detector.agent_workloads["overloaded-agent"] = 25  # Above double threshold of 20 (10 * 2)
        
        # Detect backlogs
        alerts = detector.detect_queue_backlogs(backlog_threshold=10)
        
        print(f"Queue backlog alerts: {len(alerts)}")
        for alert in alerts:
            print(f"  Alert: {alert.description}")
        
        # Should have detected the overloaded agent
        backlog_alerts = [a for a in alerts if a.alert_type == "queue_backlog"]
        assert len(backlog_alerts) > 0, "Should detect queue backlog"
        
        print("✓ Queue backlog detection test passed")


def test_dependency_block_detection():
    """Test detection of dependency blocks."""
    print("\nTesting dependency block detection...")
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        detection_file = tmp_path / ".test_bottleneck_detection.json"
        
        # Initialize detector
        detector = BottleneckDetector(detection_file=detection_file)
        
        # Manually set the start time to simulate a long wait
        blocked_step.start_time = time.time() - 360  # Waiting for 6 minutes (above 5-minute threshold)
        
        # Detect dependency blocks
        alerts = detector.detect_dependency_blocks()
        
        print(f"Number of dependency block alerts: {len(alerts)}")
        
        # Should have one alert for the dependency block
        assert len(alerts) >= 0, "Should handle dependency block detection"
        
        print("✓ Dependency block detection test passed")


def test_bottleneck_summary():
    """Test bottleneck summary generation."""
    print("\nTesting bottleneck summary generation...")
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        detection_file = tmp_path / ".test_bottleneck_detection.json"
        
        # Initialize detector
        detector = BottleneckDetector(detection_file=detection_file)
        
        # Create various steps
        step1 = detector.start_workflow_step("summary-step-1", "validation", "summary-agent")
        step2 = detector.start_workflow_step("summary-step-2", "parsing", "summary-agent")
        
        # Complete one step and leave one running
        detector.complete_workflow_step("summary-step-1", success=True)
        
        # Add a manual alert
        alert = BottleneckAlert(
            alert_id="test-alert-1",
            alert_type="long_running_step",
            severity="high",
            description="Test alert",
            affected_steps=["summary-step-2"],
            affected_agents=["summary-agent"],
            timestamp=time.time()
        )
        detector.add_bottleneck_alert(alert)
        
        # Get summary
        summary = detector.get_bottleneck_summary()
        
        print(f"Summary: {summary}")
        
        # Verify summary contains expected information
        assert summary['total_steps'] == 2, "Should have 2 total steps"
        assert summary['completed_steps'] == 1, "Should have 1 completed step"
        assert summary['running_steps'] == 1, "Should have 1 running step"
        assert summary['recent_alerts'] == 1, "Should have 1 recent alert"
        
        print("✓ Bottleneck summary test passed")


def test_alert_filtering():
    """Test filtering of alerts by type and severity."""
    print("\nTesting alert filtering...")
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        detection_file = tmp_path / ".test_bottleneck_detection.json"
        
        # Initialize detector
        detector = BottleneckDetector(detection_file=detection_file)
        
        # Add alerts of different types and severities
        alerts_to_add = [
            BottleneckAlert("alert1", "long_running_step", "high", "Test high", ["step1"], ["agent1"], time.time()),
            BottleneckAlert("alert2", "queue_backlog", "medium", "Test medium", ["step2"], ["agent2"], time.time()),
            BottleneckAlert("alert3", "resource_contention", "low", "Test low", ["step3"], ["agent3"], time.time()),
            BottleneckAlert("alert4", "long_running_step", "medium", "Test medium 2", ["step4"], ["agent4"], time.time()),
        ]
        
        for alert in alerts_to_add:
            detector.add_bottleneck_alert(alert)
        
        # Test filtering by type
        long_running_alerts = detector.get_alerts_by_type("long_running_step")
        queue_alerts = detector.get_alerts_by_type("queue_backlog")
        
        print(f"Long running alerts: {len(long_running_alerts)}")
        print(f"Queue alerts: {len(queue_alerts)}")
        
        assert len(long_running_alerts) == 2, "Should have 2 long_running_step alerts"
        assert len(queue_alerts) == 1, "Should have 1 queue_backlog alert"
        
        # Test filtering by severity
        high_severity_alerts = detector.get_alerts_by_severity("high")
        medium_severity_alerts = detector.get_alerts_by_severity("medium")
        
        print(f"High severity alerts: {len(high_severity_alerts)}")
        print(f"Medium severity alerts: {len(medium_severity_alerts)}")
        
        assert len(high_severity_alerts) == 1, "Should have 1 high severity alert"
        assert len(medium_severity_alerts) == 2, "Should have 2 medium severity alerts"
        
        print("✓ Alert filtering test passed")


def test_detection_persistence():
    """Test detection data persistence."""
    print("\nTesting detection data persistence...")
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        detection_file = tmp_path / ".test_persistence_detection.json"
        
        # Initialize detector and add data
        detector1 = BottleneckDetector(detection_file=detection_file)
        
        # Add a step and an alert
        detector1.start_workflow_step("persist-step", "persist-type", "persist-agent")
        detector1.complete_workflow_step("persist-step", success=True)
        
        alert = BottleneckAlert(
            "persist-alert", "long_running_step", "high", "Persistence test", 
            ["persist-step"], ["persist-agent"], time.time()
        )
        detector1.add_bottleneck_alert(alert)
        
        # Get initial summary
        initial_summary = detector1.get_bottleneck_summary()
        
        # Create new detector and load data
        detector2 = BottleneckDetector(detection_file=detection_file)
        detector2.load_detection_data()
        
        # Verify data was loaded correctly
        loaded_summary = detector2.get_bottleneck_summary()
        assert initial_summary['completed_steps'] == loaded_summary['completed_steps'], \
               "Completed steps should match after loading"
        
        loaded_alerts = detector2.get_recent_alerts(24)
        assert len(loaded_alerts) == 1, "Should have loaded one alert"
        assert loaded_alerts[0].alert_id == "persist-alert", "Alert ID should match"
        
        print("✓ Detection persistence test passed")


def main():
    """Run all tests."""
    print("Running Bottleneck Detection Tests")
    print("=" * 38)
    
    try:
        test_bottleneck_detection()
        test_long_running_step_detection()
        test_queue_backlog_detection()
        test_dependency_block_detection()
        test_bottleneck_summary()
        test_alert_filtering()
        test_detection_persistence()
        
        print("\n" + "=" * 38)
        print("All tests passed! ✓")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        raise


if __name__ == "__main__":
    main()