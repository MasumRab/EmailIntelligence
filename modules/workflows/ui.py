<<<<<<< HEAD
import json
import logging

import gradio as gr

# Import from the new advanced workflow engine in the core
from src.core.advanced_workflow_engine import (
    Workflow,
    WorkflowRunner,
    WorkflowManager,
    get_workflow_manager
)
from src.core.advanced_workflow_engine import (
    EmailInputNode, 
    NLPProcessorNode, 
    EmailOutputNode,
    BaseNode
)

logger = logging.getLogger(__name__)


# --- Example Node Operations ---
# In a real application, these would be discovered from modules.
def add(a, b):
    """A simple function to add two numbers."""
    return a + b


def uppercase(text):
    """A simple function to convert text to uppercase."""
    return text.upper()


# Import actual node classes from the new advanced workflow engine
# Note: Using the new node types from the advanced workflow engine
class EmailSourceNode(EmailInputNode):
    """Compatibility wrapper for old EmailSourceNode"""
    pass

class PreprocessingNode(NLPProcessorNode):
    """Compatibility wrapper for old PreprocessingNode"""
    pass

class AIAnalysisNode(EmailOutputNode):
    """Compatibility wrapper for old AIAnalysisNode"""
    pass

# A registry of available node types for this proof-of-concept.
# This allows the UI to instantiate the correct Node objects.
AVAILABLE_NODE_CLASSES = {
    "email_source": EmailSourceNode,
    "preprocessing": PreprocessingNode,
    "ai_analysis": AIAnalysisNode,
}

# --- Gradio UI ---


async def run_workflow_from_json(workflow_json: str, initial_context_json: str) -> dict:
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
        # Create a Node Engine workflow from the new advanced workflow engine
        workflow_name = workflow_data.get("name", "My Workflow")
        workflow = Workflow(name=workflow_name)

        # Add nodes to the workflow using the new API
        for node_def in workflow_data.get("nodes", []):
            node_type = node_def.get("type")
            if node_type in AVAILABLE_NODE_CLASSES:
                node_class = AVAILABLE_NODE_CLASSES[node_type]
                # Create node using new workflow's add_node method
                node_id = workflow.add_node(
                    node_type=node_type,
                    node_id=node_def["id"],
                    **node_def.get("config", {})
                )
            else:
                return {"error": f"Unknown node type: {node_type}"}

        # Add connections if specified using the new API
        for conn_def in workflow_data.get("connections", []):
            workflow.add_connection(
                source_node_id=conn_def["source_node"],
                source_output=conn_def["source_output"],
                target_node_id=conn_def["target_node"],
                target_input=conn_def["target_input"],
            )

        # Run the workflow using the new Node Engine
        workflow_manager = get_workflow_manager()  # Use the global workflow manager
        execution_result = await workflow_manager.execute_workflow(
            workflow.workflow_id, 
            initial_inputs=initial_context
        )

        # Return the execution results using the new API
        return {
            "status": execution_result.status,
            "execution_time": execution_result.execution_time,
            "outputs": execution_result.node_results,
            "errors": [execution_result.error] if execution_result.error else [],
        }

    except Exception as e:
        logger.error(f"Workflow execution failed: {e}", exc_info=True)
        return {"error": f"Workflow execution failed: {e}"}


def create_workflow_ui():
    """
    Creates the Gradio UI for the Node Engine workflow system as a self-contained tab.
    """
    with gr.Blocks() as workflow_tab:
        gr.Markdown("## Node Engine Workflow System")
        gr.Markdown(
            "Define and run node-based email processing workflows. "
            "Available node types: email_source, preprocessing, ai_analysis."
        )

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Workflow Definition (JSON)")
                # Provide a default example workflow for users
                default_workflow = {
                    "name": "Email Processing Pipeline",
                    "nodes": [
                        {
                            "id": "source",
                            "type": "email_source",
                            "name": "Email Source",
                            "config": {"max_emails": 5},
                        },
                        {"id": "preprocess", "type": "preprocessing", "name": "Text Preprocessor"},
                        {"id": "analyze", "type": "ai_analysis", "name": "AI Analyzer"},
                    ],
                    "connections": [
                        {
                            "source_node": "source",
                            "source_output": "emails",
                            "target_node": "preprocess",
                            "target_input": "emails",
                        },
                        {
                            "source_node": "preprocess",
                            "source_output": "processed_emails",
                            "target_node": "analyze",
                            "target_input": "emails",
                        },
                    ],
                }
                workflow_input = gr.Code(
                    value=json.dumps(default_workflow, indent=2),
                    language="json",
                    label="Workflow JSON",
                )

                gr.Markdown("### Initial Inputs (JSON)")
                default_context = {"max_emails": 3}
                context_input = gr.Code(
                    value=json.dumps(default_context, indent=2),
                    language="json",
                    label="Initial Inputs JSON",
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
=======
>>>>>>> origin/main
