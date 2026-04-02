import pytest
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
    initial_context = {"a": 1, "b": 2, "d": 0}
    result = runner.run(initial_context)
    assert "error" in result
