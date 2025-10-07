import gradio as gr
import json
import logging
from src.core.workflow_engine import Node, Workflow, WorkflowRunner

logger = logging.getLogger(__name__)

# --- Example Node Operations ---
# In a real application, these would be discovered from modules.
def add(a, b):
    """A simple function to add two numbers."""
    return a + b

def uppercase(text):
    """A simple function to convert text to uppercase."""
    return text.upper()

# A registry of available node types for this proof-of-concept.
# This allows the UI to instantiate the correct Node objects.
AVAILABLE_NODES = {
    "add": Node(node_id="add", name="Add", operation=add, inputs=["a", "b"], outputs=["result"]),
    "uppercase": Node(node_id="uppercase", name="Uppercase", operation=uppercase, inputs=["text"], outputs=["uppercased_text"]),
}

# --- Gradio UI ---

def run_workflow_from_json(workflow_json: str, initial_context_json: str) -> dict:
    """
    Parses a JSON definition of a workflow, runs it, and returns the result.
    This function serves as the backend logic for the Gradio UI.
    """
    try:
        workflow_data = json.loads(workflow_json)
        initial_context = json.loads(initial_context_json)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON input: {e}")
        return {"error": f"Invalid JSON input: {e}"}

    try:
        # Create Node instances from the workflow definition
        nodes = {}
        for node_def in workflow_data.get("nodes", []):
            node_type = node_def.get("type")
            if node_type in AVAILABLE_NODES:
                # Use the node_def 'id' as the key in our dictionary
                nodes[node_def["id"]] = AVAILABLE_NODES[node_type]
            else:
                return {"error": f"Unknown node type: {node_type}"}

        # Create the Workflow instance
        workflow = Workflow(
            name=workflow_data.get("name", "My Workflow"),
            nodes=nodes,
            connections=workflow_data.get("connections", {})
        )

        # Run the workflow
        runner = WorkflowRunner(workflow)
        result = runner.run(initial_context)
        return result

    except Exception as e:
        logger.error(f"Workflow execution failed: {e}", exc_info=True)
        return {"error": f"Workflow execution failed: {e}"}


def create_workflow_ui():
    """
    Creates the Gradio UI for the workflow engine as a self-contained tab.
    """
    with gr.Blocks() as workflow_tab:
        gr.Markdown("## Node-Based Workflow Engine")
        gr.Markdown(
            "Define and run processing workflows using a JSON-based format. "
            "This is a proof-of-concept interface."
        )

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Workflow Definition (JSON)")
                # Provide a default example workflow for users
                default_workflow = {
                    "name": "Simple Text and Math Workflow",
                    "nodes": [
                        {"id": "node1", "type": "uppercase"},
                        {"id": "node2", "type": "add"}
                    ],
                    "connections": {
                        # This part is not yet used by the simple runner,
                        # but is included to show the intended structure.
                    }
                }
                workflow_input = gr.Code(
                    value=json.dumps(default_workflow, indent=2),
                    language="json",
                    label="Workflow JSON",
                )

                gr.Markdown("### Initial Context (JSON)")
                default_context = {
                    "text": "hello world",
                    "a": 10,
                    "b": 5
                }
                context_input = gr.Code(
                    value=json.dumps(default_context, indent=2),
                    language="json",
                    label="Initial Context JSON",
                )

            with gr.Column(scale=1):
                gr.Markdown("### Workflow Output")
                run_button = gr.Button("Run Workflow", variant="primary")
                output_json = gr.JSON(label="Execution Result")

        run_button.click(
            fn=run_workflow_from_json,
            inputs=[workflow_input, context_input],
            outputs=output_json,
        )
    return workflow_tab