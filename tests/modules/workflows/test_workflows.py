import json
from src.core.workflow_engine import Node, Workflow, WorkflowRunner

# --- Mock Node Operations ---
def add(a, b):
    return a + b

def uppercase(text):
    return text.upper()

def test_workflow_runner():
    """
    Tests the core logic of the WorkflowRunner by executing a simple workflow.
    """
    # 1. Define a simple workflow
    nodes = {
        "node1": Node(node_id="node1", name="Uppercase", operation=uppercase, inputs=["text"], outputs=["uppercased_text"]),
        "node2": Node(node_id="node2", name="Add", operation=add, inputs=["a", "b"], outputs=["sum_result"])
    }

    # In a real scenario, the connections would be used to wire nodes together.
    # For this test, we are just executing a sequence of nodes.
    workflow = Workflow(
        name="Test Workflow",
        nodes=nodes,
        connections={}
    )

    # 2. Provide an initial context
    initial_context = {
        "text": "hello from the test",
        "a": 15,
        "b": 10
    }

    # 3. Execute the workflow and assert the results
    runner = WorkflowRunner(workflow)
    final_context = runner.run(initial_context)

    assert final_context["uppercased_text"] == "HELLO FROM THE TEST"
    assert final_context["sum_result"] == 25