#!/usr/bin/env python3
"""
Test script for agent performance monitoring system
"""

import time
import tempfile
from pathlib import Path
from agent_performance_monitor import (
    RealTimePerformanceMonitor,
    AgentPerformanceMetrics,
    AgentPerformanceDashboard
)


def test_performance_monitoring():
    """Test basic performance monitoring functionality."""
    print("Testing performance monitoring functionality...")

    # Create temporary directory for test files
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        metrics_file = tmp_path / ".test_performance_metrics.json"

        # Initialize monitor
        monitor = RealTimePerformanceMonitor(metrics_file=metrics_file)

        # Create test metrics
        agent1_metrics = AgentPerformanceMetrics(
            agent_id="agent-1",
            timestamp=time.time(),
            tasks_completed=5,
            success_rate=95.0,
            average_task_time=2.5,
            cpu_percent=45.0,
            memory_percent=30.0
        )

        agent2_metrics = AgentPerformanceMetrics(
            agent_id="agent-2",
            timestamp=time.time(),
            tasks_completed=3,
            success_rate=87.5,
            average_task_time=4.2,
            cpu_percent=65.0,
            memory_percent=45.0
        )

        # Record metrics
        monitor.record_agent_metrics("agent-1", agent1_metrics)
        monitor.record_agent_metrics("agent-2", agent2_metrics)

        # Get metrics back
        retrieved_metrics1 = monitor.get_agent_metrics("agent-1")
        retrieved_metrics2 = monitor.get_agent_metrics("agent-2")

        # Verify metrics were recorded correctly
        assert len(retrieved_metrics1) == 1, "Should have one metric for agent-1"
        assert len(retrieved_metrics2) == 1, "Should have one metric for agent-2"

        assert retrieved_metrics1[0].agent_id == "agent-1", "Agent ID should match"
        assert retrieved_metrics1[0].tasks_completed == 5, "Tasks completed should match"
        assert retrieved_metrics1[0].success_rate == 95.0, "Success rate should match"

        assert retrieved_metrics2[0].agent_id == "agent-2", "Agent ID should match"
        assert retrieved_metrics2[0].tasks_completed == 3, "Tasks completed should match"
        assert retrieved_metrics2[0].success_rate == 87.5, "Success rate should match"

        print("✓ Performance monitoring test passed")


def test_performance_summary():
    """Test performance summary calculations."""
    print("\nTesting performance summary calculations...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        metrics_file = tmp_path / ".test_performance_metrics.json"

        # Initialize monitor
        monitor = RealTimePerformanceMonitor(metrics_file=metrics_file)

        # Create multiple metrics over time for one agent
        base_time = time.time() - 1800  # 30 minutes ago (well within window)
        for i in range(10):
            metrics = AgentPerformanceMetrics(
                agent_id="test-agent",
                timestamp=base_time + (i * 60),  # Every minute
                tasks_completed=i + 1,
                success_rate=90.0 + (i * 0.5),  # Increasing success rate
                average_task_time=3.0 - (i * 0.1),  # Decreasing task time
                cpu_percent=30.0 + (i * 2),  # Increasing CPU usage
                memory_percent=25.0 + i  # Increasing memory usage
            )
            monitor.record_agent_metrics("test-agent", metrics)

        # Get performance summary with a larger time window to ensure all metrics are captured
        summary = monitor.get_agent_performance_summary("test-agent", window_hours=2)

        print(f"Tasks completed: {summary.get('total_tasks_completed', 0)}")
        print(f"Average success rate: {summary.get('average_success_rate', 0):.1f}%")
        print(f"Average task time: {summary.get('average_task_time', 0):.2f}s")
        print(f"Average CPU: {summary.get('average_cpu_percent', 0):.1f}%")
        print(f"Average memory: {summary.get('average_memory_percent', 0):.1f}%")

        # Verify summary calculations
        assert summary['total_tasks_completed'] == 55, "Should sum all tasks (1+2+3+...+10)"
        assert summary['sample_count'] == 10, "Should have 10 samples"
        assert summary['average_success_rate'] > 90.0, "Average success rate should be > 90%"

        print("✓ Performance summary test passed")


def test_dashboard_functionality():
    """Test dashboard functionality."""
    print("\nTesting dashboard functionality...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        metrics_file = tmp_path / ".test_performance_metrics.json"

        # Initialize monitor and dashboard
        monitor = RealTimePerformanceMonitor(metrics_file=metrics_file)
        dashboard = AgentPerformanceDashboard(monitor)

        # Add some test metrics
        metrics1 = AgentPerformanceMetrics(
            agent_id="dashboard-test-1",
            timestamp=time.time(),
            tasks_completed=10,
            success_rate=92.0,
            average_task_time=2.8,
            cpu_percent=40.0,
            memory_percent=35.0
        )

        metrics2 = AgentPerformanceMetrics(
            agent_id="dashboard-test-2",
            timestamp=time.time(),
            tasks_completed=7,
            success_rate=88.5,
            average_task_time=3.5,
            cpu_percent=55.0,
            memory_percent=42.0
        )

        monitor.record_agent_metrics("dashboard-test-1", metrics1)
        monitor.record_agent_metrics("dashboard-test-2", metrics2)

        # Test dashboard display functions (these should not crash)
        dashboard.display_agent_status("dashboard-test-1")
        dashboard.display_system_status()
        dashboard.display_all_agents()

        print("✓ Dashboard functionality test passed")


def test_metrics_persistence():
    """Test metrics saving and loading."""
    print("\nTesting metrics persistence...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        metrics_file = tmp_path / ".test_persistence_metrics.json"

        # Initialize monitor and add metrics
        monitor1 = RealTimePerformanceMonitor(metrics_file=metrics_file)

        metrics = AgentPerformanceMetrics(
            agent_id="persistence-test",
            timestamp=time.time(),
            tasks_completed=15,
            success_rate=94.0,
            average_task_time=2.2,
            cpu_percent=38.0,
            memory_percent=32.0
        )

        monitor1.record_agent_metrics("persistence-test", metrics)

        # Save metrics
        # (This happens automatically in record_agent_metrics)

        # Create new monitor and load metrics
        monitor2 = RealTimePerformanceMonitor(metrics_file=metrics_file)
        monitor2.load_metrics()

        # Verify metrics were loaded correctly
        loaded_metrics = monitor2.get_agent_metrics("persistence-test")
        assert len(loaded_metrics) == 1, "Should have loaded one metric"
        assert loaded_metrics[0].tasks_completed == 15, "Tasks completed should match"
        assert loaded_metrics[0].success_rate == 94.0, "Success rate should match"

        print("✓ Metrics persistence test passed")


def main():
    """Run all tests."""
    print("Running Agent Performance Monitoring Tests")
    print("=" * 45)

    try:
        test_performance_monitoring()
        test_performance_summary()
        test_dashboard_functionality()
        test_metrics_persistence()

        print("\n" + "=" * 45)
        print("All tests passed! ✓")

    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        raise


if __name__ == "__main__":
    main()