"""
It will be removed in a future release.

Workflow Editor UI for Email Intelligence Platform

Implements a Gradio-based node editor interface for creating and managing
node-based workflows, inspired by ComfyUI's interface design.
"""

import json
from typing import Any, Dict, List, Optional

import gradio as gr

from backend.plugins.plugin_manager import plugin_manager
from backend.node_engine.node_base import Connection, Workflow
from backend.node_engine.workflow_manager import get_workflow_manager

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

                gr.Markdown("### 📋 Workflow Templates")
                workflow_templates = gr.Dropdown(
                    choices=[
                        "Email Classification Pipeline",
                        "Sentiment Analysis Workflow",
                        "Spam Detection System",
                        "Customer Support Triage",
                        "Newsletter Analysis",
                        "Custom Workflow"
                    ],
                    label="Quick Templates",
                    value="Custom Workflow"
                )
                load_template_btn = gr.Button("📋 Load Template", variant="secondary")

                gr.Markdown("### 📁 Workflow Management")
                workflow_name = gr.Textbox(label="Workflow Name", value="My Workflow")
                workflow_description = gr.Textbox(label="Description", lines=2)

                with gr.Row():
                    save_workflow_btn = gr.Button("💾 Save Workflow", variant="secondary")
                    load_workflow_btn = gr.Button("📂 Load Workflow", variant="secondary")
                    sync_canvas_btn = gr.Button("🔄 Sync Canvas", variant="secondary")

                workflow_list = gr.Dropdown(
                    choices=workflow_manager.list_workflows(), label="Saved Workflows"
                )

                with gr.Row():
                    create_workflow_btn = gr.Button("➕ Create New", variant="secondary")
                    delete_workflow_btn = gr.Button("🗑️ Delete", variant="secondary")

                gr.Markdown("### 🚀 Execute Workflow")
                with gr.Row():
                    validate_btn = gr.Button("✅ Validate Workflow", variant="secondary")
                    execute_btn = gr.Button("▶️ Execute Workflow", variant="primary")

                validation_result = gr.JSON(label="Validation Result")
                execution_result = gr.JSON(label="Execution Result")

            # Right panel: Canvas/workflow area
            with gr.Column(scale=5):
                gr.Markdown("### 🖼️ Workflow Canvas")

                # Advanced JavaScript-based workflow canvas with drag-and-drop functionality
                canvas_html = f"""
                <div id="workflow-canvas" style="width:100%; height:600px; border: 1px solid #ccc; position: relative; background: #f9f9f9; overflow: hidden;">
                    <canvas id="workflow-bg-canvas" style="position: absolute; top: 0; left: 0; pointer-events: none;"></canvas>
                    <svg id="workflow-connections" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 1;" xmlns="http://www.w3.org/2000/svg">
                        <defs>
                            <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                                <polygon points="0 0, 10 3.5, 0 7" fill="#666" />
                            </marker>
                            <marker id="arrowhead-hover" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                                <polygon points="0 0, 10 3.5, 0 7" fill="#1976d2" />
                            </marker>
                        </defs>
                    </svg>
                    <div id="workflow-nodes" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 2;"></div>
                    <div id="node-context-menu" class="context-menu" style="display: none; position: absolute; background: white; border: 1px solid #ccc; border-radius: 4px; padding: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.15); z-index: 1000;">
                        <div class="context-menu-item" onclick="deleteSelectedNode()">Delete Node</div>
                        <div class="context-menu-item" onclick="duplicateNode()">Duplicate</div>
                    </div>
                </div>
                <div style="margin-top: 10px; font-size: 0.9em; color: #666;">
                    <strong>Controls:</strong> Drag nodes to move • Right-click nodes for options • Click and drag on empty space to pan • Mouse wheel to zoom<br>
                    <strong>Note:</strong> Use "🔄 Sync Canvas" button to load workflow JSON into the visual editor
                </div>
                <style>
                .workflow-node {{
                    position: absolute;
                    border-radius: 8px;
                    padding: 12px;
                    cursor: move;
                    user-select: none;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    transition: box-shadow 0.2s;
                    min-width: 140px;
                    min-height: 80px;
                }}
                .workflow-node:hover {{
                    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                }}
                .workflow-node.selected {{
                    box-shadow: 0 0 0 2px #1976d2, 0 4px 8px rgba(0,0,0,0.2);
                }}
                .workflow-node.dragging {{
                    opacity: 0.8;
                    z-index: 1000;
                }}
                .node-header {{
                    font-weight: bold;
                    margin-bottom: 8px;
                    font-size: 0.9em;
                }}
                .node-ports {{
                    position: absolute;
                    width: 12px;
                    height: 12px;
                    border-radius: 50%;
                    border: 2px solid #666;
                    background: white;
                    cursor: pointer;
                    transition: all 0.2s;
                }}
                .node-ports:hover {{
                    border-color: #1976d2;
                    background: #e3f2fd;
                }}
                .node-ports.input {{
                    left: -6px;
                    top: 50%;
                    transform: translateY(-50%);
                }}
                .node-ports.output {{
                    right: -6px;
                    top: 50%;
                    transform: translateY(-50%);
                }}
                .node-ports.connecting {{
                    border-color: #1976d2;
                    background: #1976d2;
                }}
                .connection-line {{
                    stroke: #666;
                    stroke-width: 2;
                    fill: none;
                    pointer-events: stroke;
                    cursor: pointer;
                }}
                .connection-line:hover {{
                    stroke: #1976d2;
                    stroke-width: 3;
                }}
                .context-menu-item {{
                    padding: 4px 8px;
                    cursor: pointer;
                    border-radius: 3px;
                }}
                .context-menu-item:hover {{
                    background: #f5f5f5;
                }}
                </style>
                <script>
                // Workflow Editor JavaScript Implementation
                class WorkflowEditor {{
                    constructor(canvasId) {{
                        this.canvas = document.getElementById(canvasId);
                        this.nodesContainer = document.getElementById('workflow-nodes');
                        this.connectionsSvg = document.getElementById('workflow-connections');
                        this.bgCanvas = document.getElementById('workflow-bg-canvas');
                        this.contextMenu = document.getElementById('node-context-menu');

                        this.nodes = [];
                        this.connections = [];
                        this.selectedNode = null;
                        this.draggedNode = null;
                        this.connecting = false;
                        this.connectionStart = null;
                        this.tempConnection = null;
                        this.panOffset = {{x: 0, y: 0}};
                        this.zoom = 1;
                        this.isPanning = false;
                        this.panStart = {{x: 0, y: 0}};

                        this.init();
                        this.drawGrid();
                    }}

                    init() {{
                        // Mouse event handlers
                        this.canvas.addEventListener('mousedown', (e) => this.handleMouseDown(e));
                        this.canvas.addEventListener('mousemove', (e) => this.handleMouseMove(e));
                        this.canvas.addEventListener('mouseup', (e) => this.handleMouseUp(e));
                        this.canvas.addEventListener('wheel', (e) => this.handleWheel(e));
                        this.canvas.addEventListener('contextmenu', (e) => e.preventDefault());

                        // Prevent context menu on nodes
                        this.nodesContainer.addEventListener('contextmenu', (e) => {{
                            e.preventDefault();
                            if (e.target.closest('.workflow-node')) {{
                                this.showContextMenu(e);
                            }}
                        }});

                        // Hide context menu when clicking elsewhere
                        document.addEventListener('click', () => {{
                            this.contextMenu.style.display = 'none';
                        }});

                        // Keyboard shortcuts
                        document.addEventListener('keydown', (e) => {{
                            if (e.key === 'Delete' && this.selectedNode) {{
                                this.deleteNode(this.selectedNode);
                            }}
                        }});
                    }}

                    createNode(type, x, y, data = {{}}) {{
                        const nodeId = 'node_' + Date.now();
                        const nodeElement = document.createElement('div');
                        nodeElement.className = 'workflow-node';
                        nodeElement.id = nodeId;
                        nodeElement.style.left = x + 'px';
                        nodeElement.style.top = y + 'px';

                        // Node color based on type
                        const colors = {{
                            'email_input': '#e3f2fd',
                            'nlp_processor': '#e8f5e9',
                            'email_output': '#fff3e0',
                            'filter': '#fce4ec',
                            'ai_model': '#f3e5f5',
                            'database': '#e0f2f1'
                        }};
                        nodeElement.style.background = colors[type] || '#f5f5f5';
                        nodeElement.style.border = `1px solid ${{colors[type] ? colors[type].replace('#', '#').replace(/.$/, '8') : '#ccc'}}`;

                        nodeElement.innerHTML = `
                            <div class="node-header">${{type.replace('_', ' ').toUpperCase()}}</div>
                            <div class="node-content">${{data.label || nodeId}}</div>
                            <div class="node-ports input" data-port="input"></div>
                            <div class="node-ports output" data-port="output"></div>
                        `;

                        // Add event listeners
                        nodeElement.addEventListener('mousedown', (e) => this.startDrag(e, nodeElement));
                        nodeElement.addEventListener('click', () => this.selectNode(nodeElement));

                        // Port event listeners
                        const inputPort = nodeElement.querySelector('.node-ports.input');
                        const outputPort = nodeElement.querySelector('.node-ports.output');

                        inputPort.addEventListener('mousedown', (e) => {{
                            e.stopPropagation();
                            this.startConnection(e, nodeElement, 'input');
                        }});

                        outputPort.addEventListener('mousedown', (e) => {{
                            e.stopPropagation();
                            this.startConnection(e, nodeElement, 'output');
                        }});

                        this.nodesContainer.appendChild(nodeElement);

                        const node = {{
                            id: nodeId,
                            type: type,
                            element: nodeElement,
                            x: x,
                            y: y,
                            inputs: [],
                            outputs: [],
                            data: data
                        }};

                        this.nodes.push(node);
                        return node;
                    }}

                    startDrag(e, nodeElement) {{
                        if (this.connecting) return;

                        this.draggedNode = nodeElement;
                        nodeElement.classList.add('dragging');
                        this.dragStart = {{
                            x: e.clientX - nodeElement.offsetLeft,
                            y: e.clientY - nodeElement.offsetTop
                        }};
                    }}

                    handleMouseDown(e) {{
                        if (e.target === this.canvas || e.target === this.bgCanvas) {{
                            // Start panning
                            this.isPanning = true;
                            this.panStart = {{x: e.clientX - this.panOffset.x, y: e.clientY - this.panOffset.y}};
                            this.canvas.style.cursor = 'grabbing';
                        }}
                    }}

                    handleMouseMove(e) {{
                        if (this.draggedNode) {{
                            const newX = e.clientX - this.dragStart.x;
                            const newY = e.clientY - this.dragStart.y;
                            this.draggedNode.style.left = newX + 'px';
                            this.draggedNode.style.top = newY + 'px';

                            // Update node position in data
                            const node = this.nodes.find(n => n.element === this.draggedNode);
                            if (node) {{
                                node.x = newX;
                                node.y = newY;
                            }}

                            this.updateConnections();
                        }} else if (this.isPanning) {{
                            this.panOffset.x = e.clientX - this.panStart.x;
                            this.panOffset.y = e.clientY - this.panStart.y;
                            this.updateCanvasTransform();
                        }} else if (this.connecting) {{
                            this.updateTempConnection(e);
                        }}
                    }}

                    handleMouseUp(e) {{
                        if (this.draggedNode) {{
                            this.draggedNode.classList.remove('dragging');
                            this.draggedNode = null;
                        }}

                        if (this.isPanning) {{
                            this.isPanning = false;
                            this.canvas.style.cursor = 'default';
                        }}

                        if (this.connecting) {{
                            this.finishConnection(e);
                        }}
                    }}

                    handleWheel(e) {{
                        e.preventDefault();
                        const zoomFactor = e.deltaY > 0 ? 0.9 : 1.1;
                        this.zoom *= zoomFactor;
                        this.zoom = Math.max(0.1, Math.min(3, this.zoom));
                        this.updateCanvasTransform();
                    }}

                    updateCanvasTransform() {{
                        const transform = `translate(${{this.panOffset.x}}px, ${{this.panOffset.y}}px) scale(${{this.zoom}})`;
                        this.nodesContainer.style.transform = transform;
                        this.connectionsSvg.style.transform = transform;
                        this.updateConnections();
                    }}

                    selectNode(nodeElement) {{
                        // Deselect previous
                        if (this.selectedNode) {{
                            this.selectedNode.classList.remove('selected');
                        }}

                        // Select new
                        this.selectedNode = nodeElement;
                        nodeElement.classList.add('selected');
                    }}

                    startConnection(e, nodeElement, portType) {{
                        this.connecting = true;
                        this.connectionStart = {{
                            node: nodeElement,
                            port: portType,
                            x: e.clientX,
                            y: e.clientY
                        }};

                        // Add connecting class to port
                        const port = nodeElement.querySelector(`.node-ports.${{portType}}`);
                        port.classList.add('connecting');
                    }}

                    updateTempConnection(e) {{
                        if (!this.tempConnection) {{
                            this.tempConnection = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                            this.tempConnection.setAttribute('class', 'connection-line');
                            this.tempConnection.setAttribute('stroke-dasharray', '5,5');
                            this.connectionsSvg.appendChild(this.tempConnection);
                        }}

                        const rect = this.canvas.getBoundingClientRect();
                        const startX = (this.connectionStart.x - rect.left - this.panOffset.x) / this.zoom;
                        const startY = (this.connectionStart.y - rect.top - this.panOffset.y) / this.zoom;
                        const endX = (e.clientX - rect.left - this.panOffset.x) / this.zoom;
                        const endY = (e.clientY - rect.top - this.panOffset.y) / this.zoom;

                        this.tempConnection.setAttribute('x1', startX);
                        this.tempConnection.setAttribute('y1', startY);
                        this.tempConnection.setAttribute('x2', endX);
                        this.tempConnection.setAttribute('y2', endY);
                    }}

                    finishConnection(e) {{
                        const targetElement = e.target.closest('.node-ports');
                        if (targetElement && targetElement !== this.connectionStart.node.querySelector(`.node-ports.${{this.connectionStart.port}}`)) {{
                            const targetNode = targetElement.closest('.workflow-node');
                            const targetPort = targetElement.classList.contains('input') ? 'input' : 'output';

                            // Validate connection (can't connect input to input or output to output)
                            if (this.connectionStart.port !== targetPort) {{
                                this.createConnection(this.connectionStart.node, this.connectionStart.port, targetNode, targetPort);
                            }}
                        }}

                        // Clean up
                        if (this.tempConnection) {{
                            this.connectionsSvg.removeChild(this.tempConnection);
                            this.tempConnection = null;
                        }}

                        this.connectionStart.node.querySelector(`.node-ports.${{this.connectionStart.port}}`).classList.remove('connecting');
                        this.connecting = false;
                        this.connectionStart = null;
                    }}

                    createConnection(fromNode, fromPort, toNode, toPort) {{
                        const connection = {{
                            id: 'conn_' + Date.now(),
                            fromNode: fromNode.id,
                            fromPort: fromPort,
                            toNode: toNode.id,
                            toPort: toPort
                        }};

                        this.connections.push(connection);
                        this.updateConnections();
                    }}

                    updateConnections() {{
                        // Clear existing connection lines
                        const existingLines = this.connectionsSvg.querySelectorAll('.connection-line:not(#temp-connection)');
                        existingLines.forEach(line => line.remove());

                        // Draw all connections
                        this.connections.forEach(conn => {{
                            const fromNode = this.nodes.find(n => n.id === conn.fromNode);
                            const toNode = this.nodes.find(n => n.id === conn.toNode);

                            if (fromNode && toNode) {{
                                const fromRect = fromNode.element.getBoundingClientRect();
                                const toRect = toNode.element.getBoundingClientRect();
                                const canvasRect = this.canvas.getBoundingClientRect();

                                const x1 = (fromRect.right - canvasRect.left - this.panOffset.x) / this.zoom;
                                const y1 = (fromRect.top + fromRect.height/2 - canvasRect.top - this.panOffset.y) / this.zoom;
                                const x2 = (toRect.left - canvasRect.left - this.panOffset.x) / this.zoom;
                                const y2 = (toRect.top + toRect.height/2 - canvasRect.top - this.panOffset.y) / this.zoom;

                                const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                                line.setAttribute('class', 'connection-line');
                                line.setAttribute('x1', x1);
                                line.setAttribute('y1', y1);
                                line.setAttribute('x2', x2);
                                line.setAttribute('y2', y2);
                                line.setAttribute('marker-end', 'url(#arrowhead)');

                                this.connectionsSvg.appendChild(line);
                            }}
                        }});
                    }}

                    showContextMenu(e) {{
                        this.contextMenu.style.display = 'block';
                        this.contextMenu.style.left = e.clientX + 'px';
                        this.contextMenu.style.top = e.clientY + 'px';
                        this.selectNode(e.target.closest('.workflow-node'));
                    }}

                    deleteNode(nodeElement) {{
                        // Remove connections
                        this.connections = this.connections.filter(conn =>
                            conn.fromNode !== nodeElement.id && conn.toNode !== nodeElement.id
                        );

                        // Remove node
                        this.nodes = this.nodes.filter(n => n.element !== nodeElement);
                        nodeElement.remove();

                        this.updateConnections();
                        this.selectedNode = null;
                    }}

                    drawGrid() {{
                        const ctx = this.bgCanvas.getContext('2d');
                        const gridSize = 20;

                        ctx.canvas.width = this.canvas.offsetWidth;
                        ctx.canvas.height = this.canvas.offsetHeight;

                        ctx.strokeStyle = '#e0e0e0';
                        ctx.lineWidth = 1;

                        for (let x = 0; x < ctx.canvas.width; x += gridSize) {{
                            ctx.beginPath();
                            ctx.moveTo(x, 0);
                            ctx.lineTo(x, ctx.canvas.height);
                            ctx.stroke();
                        }}

                        for (let y = 0; y < ctx.canvas.height; y += gridSize) {{
                            ctx.beginPath();
                            ctx.moveTo(0, y);
                            ctx.lineTo(ctx.canvas.width, y);
                            ctx.stroke();
                        }}
                    }}

                    // Public methods for external control
                    addNode(type, x = 100, y = 100) {{
                        return this.createNode(type, x, y);
                    }}

                    getWorkflowData() {{
                        return {{
                            nodes: this.nodes.map(n => ({{
                                id: n.id,
                                type: n.type,
                                x: n.x,
                                y: n.y,
                                data: n.data
                            }})),
                            connections: this.connections
                        }};
                    }}

                    loadWorkflowData(data) {{
                        // Clear existing
                        this.nodes.forEach(n => n.element.remove());
                        this.nodes = [];
                        this.connections = [];

                        // Load nodes
                        data.nodes.forEach(nodeData => {{
                            this.createNode(nodeData.type, nodeData.x, nodeData.y, nodeData.data);
                        }});

                        // Load connections
                        this.connections = data.connections || [];
                        this.updateConnections();
                    }}
                }}

                // Initialize the workflow editor
                const workflowEditor = new WorkflowEditor('workflow-canvas');

                // Add some sample nodes for demonstration
                workflowEditor.addNode('email_input', 50, 50);
                workflowEditor.addNode('nlp_processor', 250, 150);
                workflowEditor.addNode('email_output', 450, 250);

                // Function to load workflow data from JSON (called by Gradio)
                window.loadWorkflowFromJSON = function(jsonString) {{
                    try {{
                        const data = JSON.parse(jsonString);
                        workflowEditor.loadWorkflowData(data);
                    }} catch (e) {{
                        console.error('Failed to load workflow from JSON:', e);
                    }}
                }};

                // Make workflowEditor available globally for Gradio integration
                window.workflowEditor = workflowEditor;
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
        def add_node_via_js(node_type: str, current_json: str):
            """Add a node to the workflow via JavaScript and return updated JSON"""
            try:
                # Parse current workflow data
                if current_json.strip():
                    workflow_data = json.loads(current_json)
                else:
                    workflow_data = {"nodes": [], "connections": []}

                # Add new node
                node_id = f"node_{len(workflow_data['nodes']) + 1}"
                new_node = {
                    "id": node_id,
                    "type": node_type,
                    "x": 100 + len(workflow_data['nodes']) * 50,
                    "y": 100 + len(workflow_data['nodes']) * 50,
                    "data": {"label": f"{node_type} {len(workflow_data['nodes']) + 1}"}
                }
                workflow_data["nodes"].append(new_node)

                return json.dumps(workflow_data, indent=2)
            except Exception as e:
                return current_json

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

        def load_workflow_template(template_name: str):
            """Load a pre-configured workflow template"""
            templates = {
                "Email Classification Pipeline": {
                    "nodes": [
                        {"id": "input_1", "type": "email_input", "x": 50, "y": 100, "data": {"label": "Email Input"}},
                        {"id": "nlp_1", "type": "nlp_processor", "x": 250, "y": 100, "data": {"label": "Text Analysis"}},
                        {"id": "filter_1", "type": "filter", "x": 450, "y": 50, "data": {"label": "Priority Filter"}},
                        {"id": "filter_2", "type": "filter", "x": 450, "y": 150, "data": {"label": "Category Filter"}},
                        {"id": "output_1", "type": "email_output", "x": 650, "y": 100, "data": {"label": "Classified Output"}}
                    ],
                    "connections": [
                        {"fromNode": "input_1", "fromPort": "output", "toNode": "nlp_1", "toPort": "input"},
                        {"fromNode": "nlp_1", "fromPort": "output", "toNode": "filter_1", "toPort": "input"},
                        {"fromNode": "nlp_1", "fromPort": "output", "toNode": "filter_2", "toPort": "input"},
                        {"fromNode": "filter_1", "fromPort": "output", "toNode": "output_1", "toPort": "input"},
                        {"fromNode": "filter_2", "fromPort": "output", "toNode": "output_1", "toPort": "input"}
                    ]
                },
                "Sentiment Analysis Workflow": {
                    "nodes": [
                        {"id": "input_1", "type": "email_input", "x": 50, "y": 100, "data": {"label": "Email Input"}},
                        {"id": "ai_1", "type": "ai_model", "x": 250, "y": 100, "data": {"label": "Sentiment Model"}},
                        {"id": "output_1", "type": "email_output", "x": 450, "y": 100, "data": {"label": "Sentiment Results"}}
                    ],
                    "connections": [
                        {"fromNode": "input_1", "fromPort": "output", "toNode": "ai_1", "toPort": "input"},
                        {"fromNode": "ai_1", "fromPort": "output", "toNode": "output_1", "toPort": "input"}
                    ]
                },
                "Spam Detection System": {
                    "nodes": [
                        {"id": "input_1", "type": "email_input", "x": 50, "y": 100, "data": {"label": "Email Input"}},
                        {"id": "filter_1", "type": "filter", "x": 250, "y": 50, "data": {"label": "Spam Filter"}},
                        {"id": "ai_1", "type": "ai_model", "x": 250, "y": 150, "data": {"label": "ML Classifier"}},
                        {"id": "output_1", "type": "email_output", "x": 450, "y": 100, "data": {"label": "Filtered Output"}}
                    ],
                    "connections": [
                        {"fromNode": "input_1", "fromPort": "output", "toNode": "filter_1", "toPort": "input"},
                        {"fromNode": "input_1", "fromPort": "output", "toNode": "ai_1", "toPort": "input"},
                        {"fromNode": "filter_1", "fromPort": "output", "toNode": "output_1", "toPort": "input"},
                        {"fromNode": "ai_1", "fromPort": "output", "toNode": "output_1", "toPort": "input"}
                    ]
                },
                "Customer Support Triage": {
                    "nodes": [
                        {"id": "input_1", "type": "email_input", "x": 50, "y": 100, "data": {"label": "Support Email"}},
                        {"id": "nlp_1", "type": "nlp_processor", "x": 250, "y": 50, "data": {"label": "Intent Analysis"}},
                        {"id": "nlp_2", "type": "nlp_processor", "x": 250, "y": 150, "data": {"label": "Urgency Detection"}},
                        {"id": "filter_1", "type": "filter", "x": 450, "y": 100, "data": {"label": "Priority Router"}},
                        {"id": "output_1", "type": "email_output", "x": 650, "y": 50, "data": {"label": "High Priority"}},
                        {"id": "output_2", "type": "email_output", "x": 650, "y": 150, "data": {"label": "Normal Priority"}}
                    ],
                    "connections": [
                        {"fromNode": "input_1", "fromPort": "output", "toNode": "nlp_1", "toPort": "input"},
                        {"fromNode": "input_1", "fromPort": "output", "toNode": "nlp_2", "toPort": "input"},
                        {"fromNode": "nlp_1", "fromPort": "output", "toNode": "filter_1", "toPort": "input"},
                        {"fromNode": "nlp_2", "fromPort": "output", "toNode": "filter_1", "toPort": "input"},
                        {"fromNode": "filter_1", "fromPort": "high_priority", "toNode": "output_1", "toPort": "input"},
                        {"fromNode": "filter_1", "fromPort": "normal_priority", "toNode": "output_2", "toPort": "input"}
                    ]
                },
                "Newsletter Analysis": {
                    "nodes": [
                        {"id": "input_1", "type": "email_input", "x": 50, "y": 100, "data": {"label": "Newsletter Email"}},
                        {"id": "nlp_1", "type": "nlp_processor", "x": 250, "y": 100, "data": {"label": "Content Analysis"}},
                        {"id": "ai_1", "type": "ai_model", "x": 450, "y": 100, "data": {"label": "Topic Modeling"}},
                        {"id": "output_1", "type": "email_output", "x": 650, "y": 100, "data": {"label": "Analysis Report"}}
                    ],
                    "connections": [
                        {"fromNode": "input_1", "fromPort": "output", "toNode": "nlp_1", "toPort": "input"},
                        {"fromNode": "nlp_1", "fromPort": "output", "toNode": "ai_1", "toPort": "input"},
                        {"fromNode": "ai_1", "fromPort": "output", "toNode": "output_1", "toPort": "input"}
                    ]
                }
            }

            if template_name in templates:
                return json.dumps(templates[template_name], indent=2)
            else:
                # Return empty workflow for custom
                return json.dumps({"nodes": [], "connections": []}, indent=2)

        def sync_canvas_with_json(workflow_json_str: str):
            """Sync the JavaScript canvas with the current JSON data"""
            # This will be handled by JavaScript when the JSON changes
            return workflow_json_str

        def validate_workflow(workflow_json_str: str):
            """Validate workflow before execution"""
            try:
                workflow_data = json.loads(workflow_json_str)
                errors = []
                warnings = []

                nodes = workflow_data.get("nodes", [])
                connections = workflow_data.get("connections", [])

                if not nodes:
                    errors.append("Workflow must contain at least one node")
                    return {"valid": False, "errors": errors, "warnings": warnings}

                # Check for valid node types
                valid_types = workflow_manager.get_registered_node_types()
                for node in nodes:
                    if node.get("type") not in valid_types:
                        errors.append(f"Invalid node type: {node.get('type')} for node {node.get('id')}")

                # Check for disconnected nodes
                connected_node_ids = set()
                for conn in connections:
                    connected_node_ids.add(conn.get("fromNode"))
                    connected_node_ids.add(conn.get("toNode"))

                for node in nodes:
                    if node.get("id") not in connected_node_ids:
                        warnings.append(f"Node {node.get('id')} ({node.get('type')}) is not connected to the workflow")

                # Check for circular dependencies
                if has_circular_dependency(connections):
                    errors.append("Workflow contains circular dependencies")

                # Check for nodes with missing required inputs
                for node in nodes:
                    node_type = node.get("type")
                    # Get required inputs for this node type
                    required_inputs = get_node_required_inputs(node_type)
                    connected_inputs = [c for c in connections if c.get("toNode") == node.get("id")]

                    for required_input in required_inputs:
                        if not any(c.get("toPort") == required_input for c in connected_inputs):
                            errors.append(f"Node {node.get('id')} ({node_type}) is missing required input: {required_input}")

                return {
                    "valid": len(errors) == 0,
                    "errors": errors,
                    "warnings": warnings
                }

            except Exception as e:
                return {"valid": False, "errors": [f"Validation failed: {str(e)}"], "warnings": []}

        def has_circular_dependency(connections):
            """Check for circular dependencies in connections"""
            # Build adjacency list
            graph = {}
            for conn in connections:
                from_node = conn.get("fromNode")
                to_node = conn.get("toNode")
                if from_node not in graph:
                    graph[from_node] = []
                graph[from_node].append(to_node)

            # Check for cycles using DFS
            visited = set()
            rec_stack = set()

            def has_cycle(node):
                visited.add(node)
                rec_stack.add(node)

                for neighbor in graph.get(node, []):
                    if neighbor not in visited:
                        if has_cycle(neighbor):
                            return True
                    elif neighbor in rec_stack:
                        return True

                rec_stack.remove(node)
                return False

            for node in graph:
                if node not in visited:
                    if has_cycle(node):
                        return True
            return False

        def get_node_required_inputs(node_type):
            """Get required inputs for a node type"""
            # This would ideally come from the node definitions
            # For now, return basic requirements
            requirements = {
                "email_input": [],
                "nlp_processor": ["email"],
                "email_output": ["data"],
                "filter": ["data"],
                "ai_model": ["input"],
                "database": ["query"]
            }
            return requirements.get(node_type, [])

        def execute_current_workflow(workflow_json_str: str):
            # First validate the workflow
            validation = validate_workflow(workflow_json_str)
            if not validation["valid"]:
                return {
                    "status": "validation_failed",
                    "error": "Workflow validation failed: " + "; ".join(validation["errors"]),
                    "validation_errors": validation["errors"],
                    "validation_warnings": validation["warnings"]
                }

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
                    "validation_warnings": validation["warnings"]
                }
            except Exception as e:
                return {"error": str(e)}

        # Connect events
        add_node_btn.click(
            fn=add_node_via_js,
            inputs=[available_nodes, workflow_json],
            outputs=workflow_json
        )

        sync_canvas_btn.click(
            fn=sync_canvas_with_json,
            inputs=workflow_json,
            outputs=workflow_json
        )

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

        validate_btn.click(
            fn=validate_workflow, inputs=workflow_json, outputs=validation_result
        )

        execute_btn.click(
            fn=execute_current_workflow, inputs=workflow_json, outputs=execution_result
        )

        load_template_btn.click(
            fn=load_workflow_template, inputs=workflow_templates, outputs=workflow_json
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
