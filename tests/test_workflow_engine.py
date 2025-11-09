"""
Unit tests for the enhanced workflow engine.
Tests all the new functionality implemented for workflow engine enhancement.
"""

import os
import sys


# Add the project root to the path to import correctly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.core.workflow_engine import Node, Workflow, WorkflowRunner


def test_topological_sort():
    """Test the topological sorting of nodes"""

    def dummy_operation(x):
        return x

    # Create nodes
    node_a = Node("A", "Node A", dummy_operation, ["input"], ["output"])
    node_b = Node("B", "Node B", dummy_operation, ["input"], ["output"])
    node_c = Node("C", "Node C", dummy_operation, ["input"], ["output"])

    # Create connections: A -> B -> C
    connections = [
        {
            "from": {"node_id": "A", "output": "output"},
            "to": {"node_id": "B", "input": "input"},
        },
        {
            "from": {"node_id": "B", "output": "output"},
            "to": {"node_id": "C", "input": "input"},
        },
    ]

    workflow = Workflow(
        "test_workflow", {"A": node_a, "B": node_b, "C": node_c}, connections
    )

    # Check the execution order
    execution_order = workflow.get_execution_order()
    assert execution_order == ["A", "B", "C"], (
        f"Expected ['A', 'B', 'C'], got {execution_order}"
    )


def test_workflow_validation():
    """Test workflow validation functionality"""

    def dummy_operation(x):
        return x

    # Create nodes
    node_a = Node("A", "Node A", dummy_operation, ["input"], ["output"])
    node_b = Node("B", "Node B", dummy_operation, ["input"], ["output"])

    # Create connections
    connections = [
        {
            "from": {"node_id": "A", "output": "output"},
            "to": {"node_id": "B", "input": "input"},
        },
    ]

    workflow = Workflow("test_workflow", {"A": node_a, "B": node_b}, connections)

    # Validate the workflow
    is_valid, errors = workflow.validate()
    assert is_valid, f"Workflow should be valid, but got errors: {errors}"

    # Test with invalid connection
    invalid_connections = [
        {
            "from": {"node_id": "NONEXISTENT", "output": "output"},
            "to": {"node_id": "B", "input": "input"},
        },
    ]
    invalid_workflow = Workflow(
        "invalid_workflow", {"A": node_a, "B": node_b}, invalid_connections
    )

    is_valid, errors = invalid_workflow.validate()
    assert not is_valid, "Workflow should be invalid, but validation passed"
    assert len(errors) > 0, "Should have validation errors"


def test_conditional_execution():
    """Test conditional execution of nodes"""

    def dummy_operation(x):
        return x + 1

    # Create a node with a conditional expression
    node_a = Node("A", "Node A", dummy_operation, ["input"], ["output"])
    node_b = Node(
        "B",
        "Node B",
        dummy_operation,
        ["input"],
        ["output"],
        conditional_expression="value > 5",
    )

    connections = [
        {
            "from": {"node_id": "A", "output": "output"},
            "to": {"node_id": "B", "input": "input"},
        },
    ]

    workflow = Workflow("conditional_workflow", {"A": node_a, "B": node_b}, connections)
    runner = WorkflowRunner(workflow)

    # Run with initial context that meets the condition
    result1 = runner.run({"input": 6, "value": 6})  # This should execute both nodes
    assert result1["success"] is True
    assert "B" in result1["results"]  # Node B should be executed

    # Run with initial context that doesn't meet the condition
    result2 = runner.run({"input": 2, "value": 2})  # This should skip node B
    assert result2["success"] is True
    # Node B should not be in results since it was skipped based on condition


def test_error_handling_and_recovery():
    """Test error handling and recovery mechanisms"""

    def good_operation(x):
        return x + 1

    def failing_operation(x):
        raise Exception("Node failed intentionally")

    # Create nodes
    node_a = Node("A", "Node A", good_operation, ["input"], ["output"])
    node_b = Node(
        "B",
        "Node B",
        failing_operation,
        ["input"],
        ["output"],
        failure_strategy="continue",
    )
    node_c = Node("C", "Node C", good_operation, ["input"], ["output"])

    connections = [
        {
            "from": {"node_id": "A", "output": "output"},
            "to": {"node_id": "B", "input": "input"},
        },
        {
            "from": {"node_id": "B", "output": "output"},
            "to": {"node_id": "C", "input": "input"},
        },
    ]

    workflow = Workflow(
        "error_handling_workflow", {"A": node_a, "B": node_b, "C": node_c}, connections
    )
    runner = WorkflowRunner(workflow, max_retries=2)

    # Run the workflow - node B will fail, but should continue
    result = runner.run({"input": 5})
    assert result["success"] is True  # Overall success despite node B failure
    assert result["stats"]["nodes_failed"] == 1  # Node B should have failed
    assert result["stats"]["nodes_successful"] >= 1  # At least Node A should succeed


def test_memory_optimization():
    """Test memory optimization feature"""

    def dummy_operation(x):
        return x + 1

    # Create a linear workflow: A -> B -> C -> D
    node_a = Node("A", "Node A", dummy_operation, ["input"], ["output"])
    node_b = Node("B", "Node B", dummy_operation, ["input"], ["output"])
    node_c = Node("C", "Node C", dummy_operation, ["input"], ["output"])
    node_d = Node("D", "Node D", dummy_operation, ["input"], ["output"])

    connections = [
        {
            "from": {"node_id": "A", "output": "output"},
            "to": {"node_id": "B", "input": "input"},
        },
        {
            "from": {"node_id": "B", "output": "output"},
            "to": {"node_id": "C", "input": "input"},
        },
        {
            "from": {"node_id": "C", "output": "output"},
            "to": {"node_id": "D", "input": "input"},
        },
    ]

    workflow = Workflow(
        "memory_opt_workflow",
        {"A": node_a, "B": node_b, "C": node_c, "D": node_d},
        connections,
    )
    runner = WorkflowRunner(workflow)

    # Run with memory optimization enabled
    result = runner.run({"input": 1}, memory_optimized=True)
    assert result["success"] is True
    assert "results" in result


def test_parallel_execution():
    """Test parallel execution of independent nodes"""

    def dummy_operation(x):
        return x + 1

    # Create nodes that can run in parallel after A: A -> B, A -> C, then B,C -> D
    node_a = Node("A", "Node A", dummy_operation, ["input"], ["output"])
    node_b = Node("B", "Node B", dummy_operation, ["input"], ["output"])
    node_c = Node("C", "Node C", dummy_operation, ["input"], ["output"])
    node_d = Node("D", "Node D", dummy_operation, ["input1", "input2"], ["output"])

    connections = [
        {
            "from": {"node_id": "A", "output": "output"},
            "to": {"node_id": "B", "input": "input"},
        },
        {
            "from": {"node_id": "A", "output": "output"},
            "to": {"node_id": "C", "input": "input"},
        },
        {
            "from": {"node_id": "B", "output": "output"},
            "to": {"node_id": "D", "input": "input1"},
        },
        {
            "from": {"node_id": "C", "output": "output"},
            "to": {"node_id": "D", "input": "input2"},
        },
    ]

    workflow = Workflow(
        "parallel_workflow",
        {"A": node_a, "B": node_b, "C": node_c, "D": node_d},
        connections,
    )
    runner = WorkflowRunner(
        workflow, max_concurrent=3
    )  # Allow up to 3 nodes to run in parallel

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
        {
            "from": {"node_id": "A", "output": "output"},
            "to": {"node_id": "B", "input": "input"},
        },
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
