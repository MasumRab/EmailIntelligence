<<<<<<< HEAD
import pytest
=======
"""
Unit tests for the enhanced workflow engine.
Tests all the new functionality implemented for workflow engine enhancement.
"""

import os
import sys

# Add the project root to the path to import correctly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

>>>>>>> scientific
from src.core.workflow_engine import Node, Workflow, WorkflowRunner

def test_node_execution():
    """Test that a simple node executes correctly."""
    def add(a, b):
        return a + b

    node = Node(node_id="add", name="Add", operation=add, inputs=["a", "b"], outputs=["c"])
    context = {"a": 1, "b": 2}
    result = node.execute(context)
    assert result == {"c": 3}

def test_node_execution_multiple_outputs():
    """Test a node that produces multiple outputs."""
    def min_max(a, b):
        return min(a, b), max(a, b)

    node = Node(node_id="min_max", name="Min/Max", operation=min_max, inputs=["a", "b"], outputs=["min", "max"])
    context = {"a": 1, "b": 2}
    result = node.execute(context)
    assert result == {"min": 1, "max": 2}

def test_workflow_creation():
    """Test that a workflow can be created."""
    def add(a, b):
        return a + b

    nodes = {
        "add": Node(node_id="add", name="Add", operation=add, inputs=["a", "b"], outputs=["c"])
    }
    connections = {}
    workflow = Workflow(name="test_workflow", nodes=nodes, connections=connections)
    assert workflow.name == "test_workflow"
    assert workflow.nodes["add"].name == "Add"

def test_workflow_runner():
    """Test a simple workflow with two nodes."""
    def add(a, b):
        return a + b

    def multiply(a, b):
        return a * b

    nodes = {
        "add": Node(node_id="add", name="Add", operation=add, inputs=["a", "b"], outputs=["c"]),
        "multiply": Node(node_id="multiply", name="Multiply", operation=multiply, inputs=["c", "d"], outputs=["e"])
    }
    connections = {
        "multiply.c": "add.c"
    }
    workflow = Workflow(name="test_workflow", nodes=nodes, connections=connections)
    runner = WorkflowRunner(workflow)
    initial_context = {"a": 1, "b": 2, "d": 3}
    result = runner.run(initial_context)
    assert result == {"a": 1, "b": 2, "c": 3, "d": 3, "e": 9}

def test_workflow_runner_node_exception():
    """Test that the workflow runner handles exceptions in nodes."""
    def add(a, b):
        return a + b

    def divide(a, b):
        return a / b

    nodes = {
        "add": Node(node_id="add", name="Add", operation=add, inputs=["a", "b"], outputs=["c"]),
        "divide": Node(node_id="divide", name="Divide", operation=divide, inputs=["c", "d"], outputs=["e"])
    }
    connections = {
        "divide.c": "add.c"
    }
    workflow = Workflow(name="test_workflow", nodes=nodes, connections=connections)
    runner = WorkflowRunner(workflow)
<<<<<<< HEAD
    initial_context = {"a": 1, "b": 2, "d": 0}
    result = runner.run(initial_context)
    assert "error" in result
=======

    # Run with memory optimization enabled
    result = runner.run({"input": 1}, memory_optimized=True)
    assert result["success"] is True
    assert "results" in result


def test_parallel_execution():
    """Test parallel execution of independent nodes"""

    def dummy_operation(x):
        return x + 1

    def combine_operation(x, y):
        return x + y

    # Create nodes that can run in parallel after A: A -> B, A -> C, then B,C -> D
    node_a = Node("A", "Node A", dummy_operation, ["input"], ["output"])
    node_b = Node("B", "Node B", dummy_operation, ["input"], ["output"])
    node_c = Node("C", "Node C", dummy_operation, ["input"], ["output"])
    node_d = Node("D", "Node D", combine_operation, ["input1", "input2"], ["output"])

    connections = [
        {"from": {"node_id": "A", "output": "output"}, "to": {"node_id": "B", "input": "input"}},
        {"from": {"node_id": "A", "output": "output"}, "to": {"node_id": "C", "input": "input"}},
        {"from": {"node_id": "B", "output": "output"}, "to": {"node_id": "D", "input": "input1"}},
        {"from": {"node_id": "C", "output": "output"}, "to": {"node_id": "D", "input": "input2"}},
    ]

    workflow = Workflow(
        "parallel_workflow", {"A": node_a, "B": node_b, "C": node_c, "D": node_d}, connections
    )
    runner = WorkflowRunner(workflow, max_concurrent=3)  # Allow up to 3 nodes to run in parallel

    # Run with parallel execution
    result = runner.run({"input": 1}, parallel_execution=True)
    assert result["success"] is True
    assert len(result["results"]) == 4  # All 4 nodes should have executed


def test_metrics_collection():
    """Test metrics collection functionality"""

    def dummy_operation(x):
        return x + 1

    # Create a simple workflow
    node_a = Node("A", "Node A", dummy_operation, ["input"], ["output"])
    node_b = Node("B", "Node B", dummy_operation, ["input"], ["output"])

    connections = [
        {"from": {"node_id": "A", "output": "output"}, "to": {"node_id": "B", "input": "input"}},
    ]

    workflow = Workflow("metrics_workflow", {"A": node_a, "B": node_b}, connections)
    runner = WorkflowRunner(workflow)

    # Run the workflow
    result = runner.run({"input": 1})

    # Check that metrics were collected
    stats = result["stats"]
    assert "nodes_executed" in stats
    assert "nodes_successful" in stats
    assert "total_execution_time" in stats
    assert "node_execution_times" in stats
    assert "start_time" in stats
    assert "end_time" in stats
    assert stats["nodes_executed"] == 2  # Both nodes should execute


if __name__ == "__main__":
    # Run all tests
    test_topological_sort()
    print("✓ Topological sort test passed")

    test_workflow_validation()
    print("✓ Workflow validation test passed")

    test_conditional_execution()
    print("✓ Conditional execution test passed")

    test_error_handling_and_recovery()
    print("✓ Error handling and recovery test passed")

    test_memory_optimization()
    print("✓ Memory optimization test passed")

    test_parallel_execution()
    print("✓ Parallel execution test passed")

    test_metrics_collection()
    print("✓ Metrics collection test passed")

    print("\nAll tests passed! 🎉")
>>>>>>> scientific
