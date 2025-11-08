#!/usr/bin/env python3
"""
Test script for task dependency resolver
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from task_dependency_resolver import TaskDependencyGraph
from task_queue import Task, Priority, TaskStatus

def test_task_dependency_resolver():
    """Test the task dependency resolution system."""
    print("Testing Task Dependency Resolution System...")

    # Create dependency graph
    graph = TaskDependencyGraph()

    # Create some sample tasks
    task1 = Task(
        id="api-outline",
        title="Create API documentation outline",
        description="Create outline for API documentation",
        type="api",
        estimated_time=10,
        priority=Priority.NORMAL
    )

    task2 = Task(
        id="api-endpoints",
        title="Write API endpoint descriptions",
        description="Write detailed descriptions for each API endpoint",
        type="api",
        estimated_time=30,
        priority=Priority.NORMAL,
        dependencies=["api-outline"]
    )

    task3 = Task(
        id="api-examples",
        title="Create API examples",
        description="Create code examples for API usage",
        type="api",
        estimated_time=20,
        priority=Priority.NORMAL,
        dependencies=["api-outline"]
    )

    task4 = Task(
        id="api-review",
        title="Review API documentation",
        description="Review and finalize API documentation",
        type="api",
        estimated_time=15,
        priority=Priority.NORMAL,
        dependencies=["api-endpoints", "api-examples"]
    )

    # Add tasks to graph
    for task in [task1, task2, task3, task4]:
        graph.add_task(task)

    # Display graph
    print(graph.visualize_graph())

    # Check initial state
    ready_tasks = graph.get_ready_tasks()
    print(f"\nInitially ready tasks: {[t.id for t in ready_tasks]}")

    # Mark first task as completed
    graph.mark_task_completed("api-outline")

    # Check ready tasks after completion
    ready_tasks = graph.get_ready_tasks()
    print(f"After completing 'api-outline', ready tasks: {[t.id for t in ready_tasks]}")

    # Mark second task as in progress
    graph.mark_task_in_progress("api-endpoints")
    status = graph.get_task_status("api-endpoints")
    print(f"Status of 'api-endpoints': {status}")

    # Get execution order
    try:
        execution_order = graph.get_execution_order()
        print(f"\nExecution order: {execution_order}")
    except ValueError as e:
        print(f"\nError getting execution order: {e}")

    # Get statistics
    stats = graph.get_statistics()
    print(f"\nStatistics: {stats}")

    # Test dependency relationships
    deps_task4 = graph.get_task_dependencies("api-review")
    print(f"Dependencies of 'api-review': {list(deps_task4)}")

    dependents_task1 = graph.get_task_dependents("api-outline")
    print(f"Tasks depending on 'api-outline': {list(dependents_task1)}")

    print("Task dependency resolver test completed successfully!")

if __name__ == "__main__":
    test_task_dependency_resolver()
