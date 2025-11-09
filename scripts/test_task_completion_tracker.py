#!/usr/bin/env python3
"""
Test script for task completion tracking system
"""

import time
import tempfile
from pathlib import Path
from task_completion_tracker import TaskCompletionTracker, TaskCompletionRecord


def test_task_completion_tracking():
    """Test basic task completion tracking functionality."""
    print("Testing task completion tracking functionality...")

    # Create temporary directory for test files
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        tracking_file = tmp_path / ".test_task_tracking.json"

        # Initialize tracker
        tracker = TaskCompletionTracker(tracking_file=tracking_file)

        # Create test records
        record1 = TaskCompletionRecord(
            task_id="task-1",
            agent_id="agent-1",
            task_type="content_validation",
            start_time=time.time() - 10,
            end_time=time.time(),
            duration=5.0,
            success=True,
        )

        record2 = TaskCompletionRecord(
            task_id="task-2",
            agent_id="agent-2",
            task_type="link_check",
            start_time=time.time() - 5,
            end_time=time.time(),
            duration=2.5,
            success=False,
            error_message="Broken link detected",
        )

        record3 = TaskCompletionRecord(
            task_id="task-3",
            agent_id="agent-1",
            task_type="content_validation",
            start_time=time.time() - 3,
            end_time=time.time(),
            duration=1.5,
            success=True,
        )

        # Record tasks
        tracker.record_task_completion(record1)
        tracker.record_task_completion(record2)
        tracker.record_task_completion(record3)

        # Test completion rates
        overall_rate = tracker.get_completion_rate()
        agent1_rate = tracker.get_completion_rate(agent_id="agent-1")
        agent2_rate = tracker.get_completion_rate(agent_id="agent-2")
        validation_rate = tracker.get_completion_rate(task_type="content_validation")
        link_check_rate = tracker.get_completion_rate(task_type="link_check")

        print(f"Overall completion rate: {overall_rate:.1f}%")
        print(f"Agent-1 completion rate: {agent1_rate:.1f}%")
        print(f"Agent-2 completion rate: {agent2_rate:.1f}%")
        print(f"Content validation rate: {validation_rate:.1f}%")
        print(f"Link check rate: {link_check_rate:.1f}%")

        # Verify completion rates
        # Overall: 2 successful out of 3 total = 66.67%
        assert abs(overall_rate - 66.67) < 0.01, (
            f"Expected ~66.67%, got {overall_rate}%"
        )

        # Agent-1: 2 successful out of 2 total = 100%
        assert agent1_rate == 100.0, f"Expected 100%, got {agent1_rate}%"

        # Agent-2: 0 successful out of 1 total = 0%
        assert agent2_rate == 0.0, f"Expected 0%, got {agent2_rate}%"

        # Content validation: 2 successful out of 2 total = 100%
        assert validation_rate == 100.0, f"Expected 100%, got {validation_rate}%"

        # Link check: 0 successful out of 1 total = 0%
        assert link_check_rate == 0.0, f"Expected 0%, got {link_check_rate}%"

        print("✓ Task completion tracking test passed")


def test_average_completion_time():
    """Test average completion time calculations."""
    print("\nTesting average completion time calculations...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        tracking_file = tmp_path / ".test_task_tracking.json"

        # Initialize tracker
        tracker = TaskCompletionTracker(tracking_file=tracking_file)

        # Create test records with different durations
        base_time = time.time()
        records = [
            TaskCompletionRecord(
                task_id=f"task-{i}",
                agent_id="test-agent",
                task_type="test_type",
                start_time=base_time - (i * 10),
                end_time=base_time - (i * 10) + 5,
                duration=5.0 + (i * 0.5),  # 5.0, 5.5, 6.0, 6.5, 7.0
                success=True,
            )
            for i in range(5)
        ]

        # Record all tasks
        for record in records:
            tracker.record_task_completion(record)

        # Calculate average completion time
        avg_time = tracker.get_average_completion_time()

        print(f"Average completion time: {avg_time:.2f}s")

        # Expected average: (5.0 + 5.5 + 6.0 + 6.5 + 7.0) / 5 = 6.0
        expected_avg = 6.0
        assert abs(avg_time - expected_avg) < 0.01, (
            f"Expected ~{expected_avg}, got {avg_time}"
        )

        print("✓ Average completion time test passed")


def test_completion_trends():
    """Test completion trend calculations."""
    print("\nTesting completion trend calculations...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        tracking_file = tmp_path / ".test_task_tracking.json"

        # Initialize tracker
        tracker = TaskCompletionTracker(tracking_file=tracking_file)

        # Create test records over time
        base_time = time.time()
        for i in range(10):
            # Create 5 successful and 5 failed tasks
            success = i < 5  # First 5 successful, next 5 failed
            record = TaskCompletionRecord(
                task_id=f"trend-task-{i}",
                agent_id="trend-agent",
                task_type="trend-type",
                start_time=base_time - (i * 3600),  # Every hour back
                end_time=base_time - (i * 3600) + 2.0,
                duration=2.0,
                success=success,
            )
            tracker.record_task_completion(record)

        # Get trends for different time windows
        trends = tracker.get_completion_trends(time_windows=[1, 5, 10])

        print("Completion trends:")
        for window, rate in trends:
            print(f"  {window}h: {rate:.1f}%")

        # Verify we got trends for all requested windows
        assert len(trends) == 3, f"Expected 3 trend values, got {len(trends)}"

        # The 1-hour window should have 0% if the last task was failed
        # The 5-hour window should have some intermediate value
        # The 10-hour window should have 50% (5 successful out of 10)
        overall_rate = tracker.get_completion_rate(time_window_hours=24)
        assert abs(overall_rate - 50.0) < 0.01, (
            f"Expected 50% overall, got {overall_rate}%"
        )

        print("✓ Completion trend test passed")


def test_performance_reports():
    """Test performance report generation."""
    print("\nTesting performance report generation...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        tracking_file = tmp_path / ".test_task_tracking.json"

        # Initialize tracker
        tracker = TaskCompletionTracker(tracking_file=tracking_file)

        # Create test records
        for i in range(5):
            record = TaskCompletionRecord(
                task_id=f"report-task-{i}",
                agent_id="report-agent",
                task_type="report-type",
                start_time=time.time() - (i * 60),
                end_time=time.time() - (i * 60) + (2.0 + i * 0.5),
                duration=2.0 + (i * 0.5),  # 2.0, 2.5, 3.0, 3.5, 4.0
                success=True,
            )
            tracker.record_task_completion(record)

        # Test agent performance report
        agent_report = tracker.get_agent_performance_report("report-agent")
        print(f"Agent completion rate: {agent_report['completion_rate']:.1f}%")
        print(f"Agent avg time: {agent_report['average_completion_time']:.2f}s")

        assert agent_report["completion_rate"] == 100.0, (
            "Agent should have 100% completion rate"
        )
        assert agent_report["total_tasks"] == 5, "Agent should have 5 total tasks"

        # Test task type performance report
        task_report = tracker.get_task_type_performance_report("report-type")
        print(f"Task type completion rate: {task_report['completion_rate']:.1f}%")
        print(f"Task type avg time: {task_report['average_completion_time']:.2f}s")

        assert task_report["completion_rate"] == 100.0, (
            "Task type should have 100% completion rate"
        )
        assert task_report["sample_count"] == 5, "Task type should have 5 samples"

        # Test system performance report
        system_report = tracker.get_system_performance_report()
        print(
            f"System completion rate: {system_report['overall_completion_rate']:.1f}%"
        )

        assert system_report["total_tasks_tracked"] == 5, (
            "System should have 5 tracked tasks"
        )

        print("✓ Performance report test passed")


def test_performance_alerts():
    """Test performance alert generation."""
    print("\nTesting performance alert generation...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        tracking_file = tmp_path / ".test_task_tracking.json"

        # Initialize tracker
        tracker = TaskCompletionTracker(tracking_file=tracking_file)

        # Create records to trigger alerts
        # Create 1 successful and 9 failed tasks for agent "bad-agent"
        for i in range(10):
            success = i == 0  # Only first task succeeds
            record = TaskCompletionRecord(
                task_id=f"alert-task-{i}",
                agent_id="bad-agent",
                task_type="alert-type",
                start_time=time.time() - (i * 60),
                end_time=time.time() - (i * 60) + 2.0,
                duration=2.0,
                success=success,
            )
            tracker.record_task_completion(record)

        # Test performance alerts with 50% threshold
        alerts = tracker.get_performance_alerts(completion_rate_threshold=50.0)

        print(f"Number of alerts: {len(alerts)}")
        for alert in alerts:
            print(f"  Alert: {alert['message']}")

        # Should have alerts for both the agent and task type
        assert len(alerts) >= 1, "Should have at least one alert"

        # Check if there's an agent underperforming alert
        agent_alerts = [a for a in alerts if a["type"] == "agent_underperforming"]
        assert len(agent_alerts) > 0, "Should have agent underperforming alert"

        # The agent should have 10% completion rate (1/10), below 50% threshold
        assert agent_alerts[0]["completion_rate"] == 10.0, (
            "Agent completion rate should be 10%"
        )

        print("✓ Performance alert test passed")


def test_tracking_persistence():
    """Test tracking data persistence."""
    print("\nTesting tracking data persistence...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        tracking_file = tmp_path / ".test_persistence_tracking.json"

        # Initialize tracker and add records
        tracker1 = TaskCompletionTracker(tracking_file=tracking_file)

        record = TaskCompletionRecord(
            task_id="persistence-task",
            agent_id="persistence-agent",
            task_type="persistence-type",
            start_time=time.time() - 10,
            end_time=time.time(),
            duration=5.0,
            success=True,
        )

        tracker1.record_task_completion(record)

        # Get initial completion rate
        initial_rate = tracker1.get_completion_rate(agent_id="persistence-agent")

        # Create new tracker and load data
        tracker2 = TaskCompletionTracker(tracking_file=tracking_file)
        tracker2.load_tracking_data()

        # Verify data was loaded correctly
        loaded_rate = tracker2.get_completion_rate(agent_id="persistence-agent")
        assert abs(initial_rate - loaded_rate) < 0.01, (
            "Completion rate should match after loading"
        )

        loaded_records = len(tracker2.completion_records)
        assert loaded_records == 1, "Should have loaded one record"

        print("✓ Tracking persistence test passed")


def main():
    """Run all tests."""
    print("Running Task Completion Tracking Tests")
    print("=" * 42)

    try:
        test_task_completion_tracking()
        test_average_completion_time()
        test_completion_trends()
        test_performance_reports()
        test_performance_alerts()
        test_tracking_persistence()

        print("\n" + "=" * 42)
        print("All tests passed! ✓")

    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        raise


if __name__ == "__main__":
    main()
