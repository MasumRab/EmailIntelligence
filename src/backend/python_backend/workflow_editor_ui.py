"""
DEPRECATED: This module is part of the deprecated `backend` package.
It will be removed in a future release.

Workflow Editor UI for Email Intelligence Platform

Implements a Gradio-based node editor interface for creating and managing
node-based workflows, inspired by ComfyUI's interface design.
"""

import json
from typing import Any, Dict, List, Optional

import gradio as gr

from backend.node_engine.node_base import Connection, Workflow
from backend.node_engine.workflow_manager import get_workflow_manager
from backend.plugins.plugin_manager import plugin_manager

# Try to import security manager if available
try:
    from src.core.security import Permission, SecurityLevel, get_security_manager

    security_manager_available = True
except ImportError:
    security_manager_available = False


def create_workflow_editor_ui():
    """
    Creates a Gradio interface for editing node-based workflows
    """
    workflow_manager = get_workflow_manager()

    with gr.Blocks(title="Email Intelligence - Workflow Editor") as workflow_editor:
        gr.Markdown("## 🔄 Node-Based Workflow Editor")
        gr.Markdown(
            "Create and manage advanced workflows using a node-based interface. "
            "Connect nodes to define your email processing pipeline."
        )

        with gr.Row():
            # Left panel: Node library and controls
            with gr.Column(scale=2):
                gr.Markdown("### 🧩 Node Library")

                # Available node types
                available_nodes = gr.Dropdown(
                    choices=workflow_manager.get_registered_node_types(),
                    label="Available Node Types",
                    value=(
                        workflow_manager.get_registered_node_types()[0]
                        if workflow_manager.get_registered_node_types()
                        else None
                    ),
                )

                add_node_btn = gr.Button("Add Node", variant="primary")

                gr.Markdown("### 📁 Workflow Management")
                workflow_name = gr.Textbox(label="Workflow Name", value="My Workflow")
                workflow_description = gr.Textbox(label="Description", lines=2)

                with gr.Row():
                    save_workflow_btn = gr.Button("💾 Save Workflow", variant="secondary")
                    load_workflow_btn = gr.Button("📂 Load Workflow", variant="secondary")

                workflow_list = gr.Dropdown(
                    choices=workflow_manager.list_workflows(), label="Saved Workflows"
                )

                with gr.Row():
                    create_workflow_btn = gr.Button("➕ Create New", variant="secondary")
                    delete_workflow_btn = gr.Button("🗑️ Delete", variant="secondary")

                gr.Markdown("### 🚀 Execute Workflow")
                execute_btn = gr.Button("▶️ Execute Workflow", variant="primary")
                execution_result = gr.JSON(label="Execution Result")

            # Right panel: Canvas/workflow area
            with gr.Column(scale=5):
                gr.Markdown("### 🖼️ Workflow Canvas")

                # Using HTML/JavaScript to create a basic canvas for node editing
                # In a real implementation, we'd use a JavaScript library like
                # React Flow or Draw2D, but for now we'll create a simple interface
                canvas_html = """
                <div id="workflow-canvas" style="width:100%; height:600px; border: 1px solid #ccc; position: relative; background: #f9f9f9;">
                    <div style="position: absolute; top: 20px; left: 20px; width: 120px; height: 80px; background: #e3f2fd; border: 1px solid #1976d2; border-radius: 8px; padding: 10px; cursor: move;">
                        <div style="font-weight: bold; color: #1976d2;">Email Input</div>
                        <div style="font-size: 0.8em; color: #666;">Node 1</div>
                    </div>
                    <div style="position: absolute; top: 150px; left: 200px; width: 120px; height: 80px; background: #e8f5e9; border: 1px solid #388e3c; border-radius: 8px; padding: 10px; cursor: move;">
                        <div style="font-weight: bold; color: #388e3c;">NLP Processor</div>
                        <div style="font-size: 0.8em; color: #666;">Node 2</div>
                    </div>
                    <div style="position: absolute; top: 280px; left: 380px; width: 120px; height: 80px; background: #fff3e0; border: 1px solid #f57c00; border-radius: 8px; padding: 10px; cursor: move;">
                        <div style="font-weight: bold; color: #f57c00;">Email Output</div>
                        <div style="font-size: 0.8em; color: #666;">Node 3</div>
                    </div>
                    <!-- Simple connection lines (would be done with JavaScript in real implementation) -->
                    <svg style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none;" xmlns="http://www.w3.org/2000/svg">
                        <line x1="140" y1="60" x2="200" y2="190" stroke="#999" stroke-width="2" marker-end="url(#arrowhead)"/>
                        <line x1="320" y1="190" x2="380" y2="320" stroke="#999" stroke-width="2" marker-end="url(#arrowhead)"/>
                        <defs>
                            <marker id="arrowhead" markerWidth="10" markerHeight="7" 
                                refX="9" refY="3.5" orient="auto">
                                <polygon points="0 0, 10 3.5, 0 7" fill="#999" />
                            </marker>
                        </defs>
                    </svg>
                </div>
                <script>
                // In a real implementation, we would use JavaScript to handle
                // node dragging, connections, and workflow serialization
                console.log("Workflow canvas initialized");
                </script>
                """

                canvas = gr.HTML(canvas_html, label="Workflow Visualization")

                # JSON representation of workflow (for debugging/serialization)
                workflow_json = gr.Code(
                    label="Workflow JSON (for debugging)",
                    language="json",
                    interactive=True,
                    value=json.dumps(
                        {
                            "name": "Sample Workflow",
                            "nodes": [
                                {
                                    "id": "node1",
                                    "type": "email_input",
                                    "position": {"x": 0, "y": 0},
                                    "parameters": {},
                                },
                                {
                                    "id": "node2",
                                    "type": "nlp_processor",
                                    "position": {"x": 200, "y": 100},
                                    "parameters": {},
                                },
                                {
                                    "id": "node3",
                                    "type": "email_output",
                                    "position": {"x": 400, "y": 200},
                                    "parameters": {},
                                },
                            ],
                            "connections": [
                                {
                                    "source_node_id": "node1",
                                    "source_output": "email",
                                    "target_node_id": "node2",
                                    "target_input": "email",
                                },
                                {
                                    "source_node_id": "node2",
                                    "source_output": "analysis",
                                    "target_node_id": "node3",
                                    "target_input": "analysis",
                                },
                            ],
                        },
                        indent=2,
                    ),
                )

        # Event handlers
        def add_node_to_workflow(node_type: str):
            # This would be handled by JavaScript in a real implementation
            # For now, we'll just update the JSON representation
            workflow_data = {
                "nodes": [
                    {
                        "id": f"node_{len(workflow_manager.get_registered_node_types())}",
                        "type": node_type,
                        "position": {"x": 100, "y": 100},
                        "parameters": {},
                    }
                ],
                "connections": [],
            }
            return json.dumps(workflow_data, indent=2)

        def save_current_workflow(name: str, description: str, workflow_json_str: str):
            try:
                workflow_data = json.loads(workflow_json_str)
                workflow = Workflow(name=name, description=description)
                workflow.nodes = workflow_data.get("nodes", [])
                workflow.connections = workflow_data.get("connections", [])

                success = workflow_manager.save_workflow(workflow)
                if success:
                    return (
                        f"✅ Workflow '{name}' saved successfully!",
                        workflow_manager.list_workflows(),
                    )
                else:
                    return "❌ Failed to save workflow", workflow_manager.list_workflows()
            except Exception as e:
                return f"❌ Error saving workflow: {str(e)}", workflow_manager.list_workflows()

        def load_selected_workflow(workflow_filename: str):
            try:
                workflow = workflow_manager.load_workflow(workflow_filename)
                if workflow:
                    workflow_json_str = json.dumps(workflow.to_dict(), indent=2)
                    return (
                        workflow.name,
                        workflow.description,
                        workflow_json_str,
                        f"✅ Workflow '{workflow.name}' loaded",
                    )
                else:
                    return "", "", "", "❌ Failed to load workflow"
            except Exception as e:
                return "", "", "", f"❌ Error loading workflow: {str(e)}"

        def execute_current_workflow(workflow_json_str: str):
            try:
                workflow_data = json.loads(workflow_json_str)
                workflow = Workflow.from_dict(workflow_data)

                # Add workflow to manager temporarily for execution
                workflow_manager._workflows[workflow.workflow_id] = workflow

                # Execute with sample inputs
                result = workflow_manager.execute_workflow(
                    workflow.workflow_id,
                    initial_inputs={
                        "email_data": {
                            "subject": "Sample Email",
                            "content": "This is a sample email for workflow testing",
                            "sender": "sender@example.com",
                        }
                    },
                )

                return {
                    "status": result.status,
                    "execution_time": result.execution_time,
                    "node_results": result.node_results,
                    "error": result.error,
                }
            except Exception as e:
                return {"error": str(e)}

        # Connect events
        add_node_btn.click(fn=add_node_to_workflow, inputs=available_nodes, outputs=workflow_json)

        save_workflow_btn.click(
            fn=save_current_workflow,
            inputs=[workflow_name, workflow_description, workflow_json],
            outputs=[gr.Textbox(label="Save Status"), workflow_list],
        )

        load_workflow_btn.click(
            fn=load_selected_workflow,
            inputs=workflow_list,
            outputs=[
                workflow_name,
                workflow_description,
                workflow_json,
                gr.Textbox(label="Load Status"),
            ],
        )

        execute_btn.click(
            fn=execute_current_workflow, inputs=workflow_json, outputs=execution_result
        )

    return workflow_editor


def create_advanced_workflow_ui():
    """
    Creates the main Gradio interface that includes the workflow editor
    and other advanced features
    """
    with gr.Blocks(title="Email Intelligence - Advanced Workflows") as advanced_ui:
        gr.Markdown("# 🚀 Email Intelligence Platform - Advanced Workflows")
        gr.Markdown(
            "Node-based workflow system inspired by ComfyUI, with enterprise-grade "
            "security and scalability features."
        )

        with gr.Tabs():
            with gr.TabItem("Workflow Editor"):
                create_workflow_editor_ui()

            with gr.TabItem("Node Gallery"):
                gr.Markdown("### Available Processing Nodes")
                registered_nodes = get_workflow_manager().get_registered_node_types()
                for node_type in registered_nodes:
                    gr.Markdown(f"- **{node_type}**")

                # Show plugin nodes too
                gr.Markdown("### Plugin Nodes")
                plugin_nodes = plugin_manager.get_all_processing_nodes()
                for node_name in plugin_nodes.keys():
                    gr.Markdown(f"- **{node_name}**")

            with gr.TabItem("Performance"):
                gr.Markdown("### Workflow Performance Metrics")
                # This would connect to the performance monitoring system
                # For now, showing sample data
                gr.Dataframe(
                    headers=["Metric", "Value"],
                    value=[
                        ["Active Workflows", 3],
                        ["Completed Workflows", 42],
                        ["Avg Execution Time", "1.2s"],
                        ["Error Rate", "0.02%"],
                    ],
                )

    return advanced_ui


# Initialize the workflow system when this module is loaded
initialize_workflow_system()

if __name__ == "__main__":
    # For testing the workflow editor UI
    ui = create_advanced_workflow_ui()
    ui.launch()
