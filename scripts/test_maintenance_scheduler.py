#!/usr/bin/env python3
"""
Test script for automated maintenance task scheduling system
"""

import time
import tempfile
from pathlib import Path
from maintenance_scheduler import MaintenanceScheduler, MaintenanceAgent, MaintenanceTask, MaintenanceDashboard


def dummy_task_callback(task: MaintenanceTask) -> dict:
    """Dummy callback for testing task execution."""
    # Simulate some work
    time.sleep(0.1)

    # Return some mock results
    return {
        "findings": ["No issues found", "Documentation is up to date"],
        "suggestions": ["Consider adding more examples"],
        "metadata": {"processed_by": "test_agent"}
    }


def test_scheduler_initialization():
    """Test basic scheduler initialization."""
    print("Testing scheduler initialization...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        scheduler_file = tmp_path / ".test_scheduler.json"

        # Initialize scheduler
        scheduler = MaintenanceScheduler(scheduler_file=scheduler_file)

        # Verify initial state
        stats = scheduler.get_scheduler_statistics()
        assert stats['total_agents'] == 0, "Should have 0 agents initially"
        assert stats['total_tasks'] == 0, "Should have 0 tasks initially"
        assert stats['total_schedules'] == 0, "Should have 0 schedules initially"

        print("✓ Scheduler initialization test passed")


def test_agent_registration():
    """Test registering maintenance agents."""
    print("\nTesting agent registration...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        scheduler_file = tmp_path / ".test_scheduler.json"

        # Initialize scheduler
        scheduler = MaintenanceScheduler(scheduler_file=scheduler_file)

        # Create and register an agent
        agent = MaintenanceAgent(
            agent_id="test-agent-1",
            capabilities=["link_check", "format_check", "content_update"]
        )

        success = scheduler.register_agent(agent)
        assert success, "Should register agent successfully"

        # Verify agent was registered
        stats = scheduler.get_scheduler_statistics()
        assert stats['total_agents'] == 1, "Should have 1 agent"

        # Verify agent status
        agent_status = scheduler.get_agent_status("test-agent-1")
        assert agent_status is not None, "Should retrieve agent status"
        assert agent_status.agent_id == "test-agent-1", "Agent ID should match"
        assert "link_check" in agent_status.capabilities, "Should have link_check capability"

        print("✓ Agent registration test passed")


def test_task_callback_registration():
    """Test registering task callbacks."""
    print("\nTesting task callback registration...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        scheduler_file = tmp_path / ".test_scheduler.json"

        # Initialize scheduler
        scheduler = MaintenanceScheduler(scheduler_file=scheduler_file)

        # Register a callback
        scheduler.register_task_callback("link_check", dummy_task_callback)

        # Verify callback was registered
        assert "link_check" in scheduler.task_execution_callbacks, "Should have registered callback"

        print("✓ Task callback registration test passed")


def test_create_maintenance_task():
    """Test creating maintenance tasks."""
    print("\nTesting maintenance task creation...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        scheduler_file = tmp_path / ".test_scheduler.json"

        # Initialize scheduler
        scheduler = MaintenanceScheduler(scheduler_file=scheduler_file)

        # Create and register an agent
        agent = MaintenanceAgent(
            agent_id="test-agent-1",
            capabilities=["link_check"]
        )
        scheduler.register_agent(agent)

        # Register a callback
        scheduler.register_task_callback("link_check", dummy_task_callback)

        # Create a maintenance task
        task_id = scheduler.create_maintenance_task(
            task_type="link_check",
            document_id="test-doc-1.md",
            description="Check links in test document",
            priority="high"
        )

        assert task_id != "", "Should return a valid task ID"

        # Verify task was created
        stats = scheduler.get_scheduler_statistics()
        assert stats['total_tasks'] == 1, "Should have 1 task"
        assert stats['pending_tasks'] == 1, "Should have 1 pending task"

        # Verify task status
        task_status = scheduler.get_task_status(task_id)
        assert task_status is not None, "Should retrieve task status"
        assert task_status.task_type == "link_check", "Task type should match"
        assert task_status.document_id == "test-doc-1.md", "Document ID should match"
        assert task_status.priority == "high", "Priority should match"
        assert task_status.status == "pending", "Status should be pending"

        print("✓ Maintenance task creation test passed")


def test_create_recurring_schedule():
    """Test creating recurring maintenance schedules."""
    print("\nTesting recurring schedule creation...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        scheduler_file = tmp_path / ".test_scheduler.json"

        # Initialize scheduler
        scheduler = MaintenanceScheduler(scheduler_file=scheduler_file)

        # Create a recurring schedule
        schedule_id = scheduler.create_recurring_schedule(
            name="Daily Link Check",
            description="Check links in all documents daily",
            task_type="link_check",
            schedule_pattern="daily",
            task_params={"document_id": "*"}
        )

        assert schedule_id != "", "Should return a valid schedule ID"

        # Verify schedule was created
        stats = scheduler.get_scheduler_statistics()
        assert stats['total_schedules'] == 1, "Should have 1 schedule"

        # Verify schedule status
        schedule_status = scheduler.get_schedule_status(schedule_id)
        assert schedule_status is not None, "Should retrieve schedule status"
        assert schedule_status.name == "Daily Link Check", "Schedule name should match"
        assert schedule_status.task_type == "link_check", "Task type should match"
        assert schedule_status.schedule_pattern == "daily", "Schedule pattern should match"
        assert schedule_status.enabled, "Schedule should be enabled"

        print("✓ Recurring schedule creation test passed")


def test_task_execution():
    """Test executing maintenance tasks."""
    print("\nTesting task execution...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        scheduler_file = tmp_path / ".test_scheduler.json"

        # Initialize scheduler
        scheduler = MaintenanceScheduler(scheduler_file=scheduler_file)

        # Create and register an agent
        agent = MaintenanceAgent(
            agent_id="test-agent-1",
            capabilities=["link_check"]
        )
        scheduler.register_agent(agent)

        # Register a callback
        scheduler.register_task_callback("link_check", dummy_task_callback)

        # Create a maintenance task
        task_id = scheduler.create_maintenance_task(
            task_type="link_check",
            document_id="test-doc-1.md",
            description="Check links in test document",
            priority="normal"
        )

        # Execute the task
        success = scheduler.execute_next_task()
        assert success, "Should execute task successfully"

        # Verify task was completed
        stats = scheduler.get_scheduler_statistics()
        assert stats['completed_tasks'] == 1, "Should have 1 completed task"
        assert stats['pending_tasks'] == 0, "Should have 0 pending tasks"

        # Verify task status
        task_status = scheduler.get_task_status(task_id)
        assert task_status is not None, "Should retrieve task status"
        assert task_status.status == "completed", "Task should be completed"
        assert task_status.start_time > 0, "Start time should be set"
        assert task_status.end_time > 0, "End time should be set"

        # Verify task results
        results = scheduler.get_task_results(task_id)
        assert len(results) == 1, "Should have 1 result"
        assert results[0].status == "success", "Result should be success"
        assert len(results[0].findings) > 0, "Should have findings"

        print("✓ Task execution test passed")


def test_scheduler_statistics():
    """Test scheduler statistics."""
    print("\nTesting scheduler statistics...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        scheduler_file = tmp_path / ".test_scheduler.json"

        # Initialize scheduler
        scheduler = MaintenanceScheduler(scheduler_file=scheduler_file)

        # Create and register agents
        agent1 = MaintenanceAgent(
            agent_id="agent-1",
            capabilities=["link_check", "format_check"]
        )
        agent2 = MaintenanceAgent(
            agent_id="agent-2",
            capabilities=["content_update"]
        )
        scheduler.register_agent(agent1)
        scheduler.register_agent(agent2)

        # Register callbacks
        scheduler.register_task_callback("link_check", dummy_task_callback)
        scheduler.register_task_callback("content_update", dummy_task_callback)

        # Create some tasks
        scheduler.create_maintenance_task(
            task_type="link_check",
            document_id="doc1.md",
            description="Test link check 1"
        )
        scheduler.create_maintenance_task(
            task_type="content_update",
            document_id="doc2.md",
            description="Test content update",
            priority="high"
        )

        # Execute one task
        scheduler.execute_next_task()

        # Get statistics
        stats = scheduler.get_scheduler_statistics()

        print(f"Statistics: {stats}")

        assert stats['total_agents'] == 2, "Should have 2 agents"
        assert stats['active_agents'] == 2, "Should have 2 active agents"
        assert stats['total_tasks'] == 2, "Should have 2 tasks"
        assert stats['completed_tasks'] == 1, "Should have 1 completed task"
        assert stats['pending_tasks'] == 1, "Should have 1 pending task"

        print("✓ Scheduler statistics test passed")


def test_scheduler_dashboard():
    """Test scheduler dashboard functionality."""
    print("\nTesting scheduler dashboard...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        scheduler_file = tmp_path / ".test_scheduler.json"

        # Initialize scheduler and dashboard
        scheduler = MaintenanceScheduler(scheduler_file=scheduler_file)
        dashboard = MaintenanceDashboard(scheduler)

        # Create and register an agent
        agent = MaintenanceAgent(
            agent_id="dashboard-test-agent",
            capabilities=["link_check", "format_check"]
        )
        scheduler.register_agent(agent)

        # Register a callback
        scheduler.register_task_callback("link_check", dummy_task_callback)

        # Create a maintenance task
        task_id = scheduler.create_maintenance_task(
            task_type="link_check",
            document_id="dashboard-test-doc.md",
            description="Dashboard test task"
        )

        # Test dashboard methods (should not crash)
        dashboard.display_scheduler_status()
        dashboard.display_agents()
        dashboard.display_pending_tasks()

        # Execute the task to generate results
        scheduler.execute_next_task()

        # Display results
        dashboard.display_task_results(task_id)

        print("✓ Scheduler dashboard test passed")


def test_scheduler_persistence():
    """Test scheduler data persistence."""
    print("\nTesting scheduler data persistence...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        scheduler_file = tmp_path / ".test_persistence_scheduler.json"

        # Initialize scheduler and add data
        scheduler1 = MaintenanceScheduler(scheduler_file=scheduler_file)

        # Create and register an agent
        agent = MaintenanceAgent(
            agent_id="persistence-test-agent",
            capabilities=["link_check"]
        )
        scheduler1.register_agent(agent)

        # Register a callback
        scheduler1.register_task_callback("link_check", dummy_task_callback)

        # Create a maintenance task
        task_id = scheduler1.create_maintenance_task(
            task_type="link_check",
            document_id="persistence-test-doc.md",
            description="Persistence test task"
        )

        # Execute the task
        scheduler1.execute_next_task()

        # Verify data exists
        stats1 = scheduler1.get_scheduler_statistics()
        assert stats1['total_tasks'] == 1, "Should have 1 task"
        assert stats1['completed_tasks'] == 1, "Should have 1 completed task"

        # Create new scheduler and load data
        scheduler2 = MaintenanceScheduler(scheduler_file=scheduler_file)

        # Verify data was loaded
        stats2 = scheduler2.get_scheduler_statistics()
        assert stats2['total_agents'] == 1, "Should have loaded 1 agent"
        assert stats2['total_tasks'] == 1, "Should have loaded 1 task"
        assert stats2['completed_tasks'] == 1, "Should have loaded 1 completed task"

        # Verify specific data
        loaded_agent = scheduler2.get_agent_status("persistence-test-agent")
        assert loaded_agent is not None, "Should load agent"
        assert "link_check" in loaded_agent.capabilities, "Should have correct capabilities"

        loaded_task = scheduler2.get_task_status(task_id)
        assert loaded_task is not None, "Should load task"
        assert loaded_task.status == "completed", "Should have correct status"

        print("✓ Scheduler data persistence test passed")


def test_find_available_agents():
    """Test finding available agents for tasks."""
    print("\nTesting finding available agents...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        scheduler_file = tmp_path / ".test_scheduler.json"

        # Initialize scheduler
        scheduler = MaintenanceScheduler(scheduler_file=scheduler_file)

        # Create and register agents with different capabilities
        agent1 = MaintenanceAgent(
            agent_id="agent-1",
            capabilities=["link_check", "format_check"]
        )
        agent2 = MaintenanceAgent(
            agent_id="agent-2",
            capabilities=["content_update"]
        )
        agent3 = MaintenanceAgent(
            agent_id="agent-3",
            capabilities=["link_check"]  # Same capability as agent-1
        )
        scheduler.register_agent(agent1)
        scheduler.register_agent(agent2)
        scheduler.register_agent(agent3)

        # Find agents for link_check task
        available_agents = scheduler._find_available_agents("link_check")
        assert "agent-1" in available_agents, "Should find agent-1 for link_check"
        assert "agent-3" in available_agents, "Should find agent-3 for link_check"
        assert "agent-2" not in available_agents, "Should not find agent-2 for link_check"

        # Find agents for content_update task
        available_agents = scheduler._find_available_agents("content_update")
        assert "agent-2" in available_agents, "Should find agent-2 for content_update"

        print("✓ Finding available agents test passed")


def test_task_prioritization():
    """Test task prioritization."""
    print("\nTesting task prioritization...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        scheduler_file = tmp_path / ".test_scheduler.json"

        # Initialize scheduler
        scheduler = MaintenanceScheduler(scheduler_file=scheduler_file)

        # Create and register an agent
        agent = MaintenanceAgent(
            agent_id="priority-test-agent",
            capabilities=["link_check"]
        )
        scheduler.register_agent(agent)

        # Register a callback
        scheduler.register_task_callback("link_check", dummy_task_callback)

        # Create tasks with different priorities
        critical_task_id = scheduler.create_maintenance_task(
            task_type="link_check",
            document_id="critical-doc.md",
            description="Critical task",
            priority="critical"
        )

        low_task_id = scheduler.create_maintenance_task(
            task_type="link_check",
            document_id="low-doc.md",
            description="Low priority task",
            priority="low"
        )

        high_task_id = scheduler.create_maintenance_task(
            task_type="link_check",
            document_id="high-doc.md",
            description="High priority task",
            priority="high"
        )

        # Verify prioritization by finding highest priority task
        highest_priority_task_id = scheduler._find_highest_priority_task()
        assert highest_priority_task_id == critical_task_id, "Critical task should be highest priority"

        print("✓ Task prioritization test passed")


def main():
    """Run all tests."""
    print("Running Automated Maintenance Task Scheduling Tests")
    print("=" * 55)

    try:
        test_scheduler_initialization()
        test_agent_registration()
        test_task_callback_registration()
        test_create_maintenance_task()
        test_create_recurring_schedule()
        test_task_execution()
        test_scheduler_statistics()
        test_scheduler_dashboard()
        test_scheduler_persistence()
        test_find_available_agents()
        test_task_prioritization()

        print("\n" + "=" * 55)
        print("All tests passed! ✓")

    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        raise


if __name__ == "__main__":
    main()