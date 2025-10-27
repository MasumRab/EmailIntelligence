"""
DEPRECATED: This module is part of the deprecated `backend` package.
It will be removed in a future release.

API routes for node-based workflows in the Email Intelligence Platform.

This module provides API endpoints for managing and executing node-based workflows
that were implemented in the new node engine architecture.
"""

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from backend.node_engine.email_nodes import (
    ActionNode,
    AIAnalysisNode,
    EmailSourceNode,
    FilterNode,
    PreprocessingNode,
)

# Import the new node-based workflow components
from backend.node_engine.node_base import Workflow as NodeWorkflow
from backend.node_engine.workflow_engine import workflow_engine as node_workflow_engine
from backend.node_engine.workflow_manager import workflow_manager as node_workflow_manager

from ..python_nlp.smart_filters import SmartFilterManager
from .ai_engine import AdvancedAIEngine
from .dependencies import get_db
from .model_manager import model_manager
from backend.node_engine.workflow_engine import WorkflowEngine  # Node engine

router = APIRouter()


class NodeWorkflowCreateRequest(BaseModel):
    name: str
    description: str = ""
    nodes: List[Dict[str, Any]] = []
    connections: List[Dict[str, str]] = (
        []
    )  # Format: {source_node_id, source_port, target_node_id, target_port}


class NodeWorkflowResponse(BaseModel):
    workflow_id: str
    name: str
    description: str
    nodes: List[Dict[str, Any]]
    connections: List[Dict[str, str]]
    created_at: str
    updated_at: str


class ExecuteWorkflowRequest(BaseModel):
    initial_inputs: Dict[str, Any] = {}
    user_id: Optional[str] = None


class ExecuteWorkflowResponse(BaseModel):
    workflow_id: str
    status: str
    execution_time: float
    execution_path: List[str]
    errors: List[Dict[str, Any]]
    outputs: Dict[str, Any]


@router.post("/api/nodes/workflows", response_model=NodeWorkflowResponse)
async def create_node_workflow(request: NodeWorkflowCreateRequest):
    """Create a new node-based workflow."""
    try:
        # Create a new workflow
        workflow = NodeWorkflow(name=request.name, description=request.description)

        # Create nodes from the request data
        for node_data in request.nodes:
            node_type = node_data.get("type")
            node_id = node_data.get("node_id")
            node_name = node_data.get("name", "")
            node_config = node_data.get("config", {})

            # Create the appropriate node based on type
            if node_type == "EmailSourceNode":
                node = EmailSourceNode(config=node_config, node_id=node_id, name=node_name)
            elif node_type == "PreprocessingNode":
                node = PreprocessingNode(config=node_config, node_id=node_id, name=node_name)
            elif node_type == "AIAnalysisNode":
                node = AIAnalysisNode(config=node_config, node_id=node_id, name=node_name)
            elif node_type == "FilterNode":
                node = FilterNode(config=node_config, node_id=node_id, name=node_name)
            elif node_type == "ActionNode":
                node = ActionNode(config=node_config, node_id=node_id, name=node_name)
            else:
                raise HTTPException(status_code=400, detail=f"Unknown node type: {node_type}")

            # Add the node to the workflow
            workflow.add_node(node)

        # Create connections
        for conn_data in request.connections:
            from backend.node_engine.node_base import Connection

            connection = Connection(
                source_node_id=conn_data["source_node_id"],
                source_port=conn_data["source_port"],
                target_node_id=conn_data["target_node_id"],
                target_port=conn_data["target_port"],
            )
            workflow.add_connection(connection)

        # Save the workflow
        file_path = node_workflow_manager.save_workflow(workflow)

        return NodeWorkflowResponse(
            workflow_id=workflow.workflow_id,
            name=workflow.name,
            description=workflow.description,
            nodes=request.nodes,
            connections=request.connections,
            created_at="",  # Placeholder - would need actual timestamp from workflow
            updated_at="",  # Placeholder - would need actual timestamp from workflow
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create node workflow: {str(e)}")


@router.get("/api/nodes/workflows", response_model=List[str])
async def list_node_workflows():
    """List all available node-based workflows."""
    try:
        workflows = node_workflow_manager.list_workflows()
        return [wf["id"] for wf in workflows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list workflows: {str(e)}")


@router.get("/api/nodes/workflows/{workflow_id}", response_model=NodeWorkflowResponse)
async def get_node_workflow(workflow_id: str):
    """Get a specific node-based workflow by ID."""
    try:
        workflow = node_workflow_manager.load_workflow(workflow_id)
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")

        # Convert workflow to response format
        nodes_data = []
        for node_id, node in workflow.nodes.items():
            nodes_data.append(
                {
                    "node_id": node.node_id,
                    "type": node.__class__.__name__,
                    "name": node.name,
                    "description": node.description,
                    "config": getattr(node, "config", {}),
                }
            )

        connections_data = []
        for conn in workflow.connections:
            connections_data.append(
                {
                    "source_node_id": conn.source_node_id,
                    "source_port": conn.source_port,
                    "target_node_id": conn.target_node_id,
                    "target_port": conn.target_port,
                }
            )

        return NodeWorkflowResponse(
            workflow_id=workflow.workflow_id,
            name=workflow.name,
            description=workflow.description,
            nodes=nodes_data,
            connections=connections_data,
            created_at="",  # Would need to get from metadata
            updated_at="",  # Would need to get from metadata
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get workflow: {str(e)}")


@router.put("/api/nodes/workflows/{workflow_id}", response_model=NodeWorkflowResponse)
async def update_node_workflow(workflow_id: str, request: NodeWorkflowCreateRequest):
    """Update an existing node-based workflow."""
    try:
        # For now, we'll create a new workflow and save it with the same ID
        # In a production system, we might want a more nuanced update approach
        updated_workflow = NodeWorkflow(
            workflow_id=workflow_id, name=request.name, description=request.description
        )

        # Create nodes from the request data
        for node_data in request.nodes:
            node_type = node_data.get("type")
            node_id = node_data.get("node_id")
            node_name = node_data.get("name", "")
            node_config = node_data.get("config", {})

            # Create the appropriate node based on type
            if node_type == "EmailSourceNode":
                node = EmailSourceNode(config=node_config, node_id=node_id, name=node_name)
            elif node_type == "PreprocessingNode":
                node = PreprocessingNode(config=node_config, node_id=node_id, name=node_name)
            elif node_type == "AIAnalysisNode":
                node = AIAnalysisNode(config=node_config, node_id=node_id, name=node_name)
            elif node_type == "FilterNode":
                node = FilterNode(config=node_config, node_id=node_id, name=node_name)
            elif node_type == "ActionNode":
                node = ActionNode(config=node_config, node_id=node_id, name=node_name)
            else:
                raise HTTPException(status_code=400, detail=f"Unknown node type: {node_type}")

            updated_workflow.add_node(node)

        # Create connections
        for conn_data in request.connections:
            from backend.node_engine.node_base import Connection

            connection = Connection(
                source_node_id=conn_data["source_node_id"],
                source_port=conn_data["source_port"],
                target_node_id=conn_data["target_node_id"],
                target_port=conn_data["target_port"],
            )
            updated_workflow.add_connection(connection)

        # Save the updated workflow
        file_path = node_workflow_manager.save_workflow(updated_workflow)

        return NodeWorkflowResponse(
            workflow_id=updated_workflow.workflow_id,
            name=updated_workflow.name,
            description=updated_workflow.description,
            nodes=request.nodes,
            connections=request.connections,
            created_at="",  # Placeholder
            updated_at="",  # Placeholder
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update workflow: {str(e)}")


@router.delete("/api/nodes/workflows/{workflow_id}")
async def delete_node_workflow(workflow_id: str):
    """Delete a node-based workflow."""
    try:
        success = node_workflow_manager.delete_workflow(workflow_id)
        if not success:
            raise HTTPException(status_code=404, detail="Workflow not found")

        return {"message": f"Workflow {workflow_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete workflow: {str(e)}")


@router.post("/api/nodes/workflows/{workflow_id}/execute", response_model=ExecuteWorkflowResponse)
async def execute_node_workflow(workflow_id: str, request: ExecuteWorkflowRequest):
    """Execute a node-based workflow with provided inputs."""
    try:
        # Load the workflow
        workflow = node_workflow_manager.load_workflow(workflow_id)
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")

        # Execute the workflow
        execution_context = await node_workflow_engine.execute_workflow(
            workflow, initial_inputs=request.initial_inputs, user_id=request.user_id
        )

        return ExecuteWorkflowResponse(
            workflow_id=workflow_id,
            status=execution_context.metadata.get("status", "unknown"),
            execution_time=execution_context.metadata.get("execution_duration", 0),
            execution_path=execution_context.execution_path,
            errors=execution_context.errors,
            outputs=execution_context.node_outputs,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to execute workflow: {str(e)}")


# Node Management Routes
@router.get("/api/nodes/types", response_model=List[str])
async def get_available_node_types():
    """Get list of available node types."""
    try:
        return node_workflow_engine.get_registered_node_types()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get node types: {str(e)}")


@router.get("/api/nodes/types/{node_type}/info")
async def get_node_info(node_type: str):
    """Get information about a specific node type."""
    try:
        # Create a temporary instance of the node to get its info
        if node_type == "EmailSourceNode":
            node = EmailSourceNode()
        elif node_type == "PreprocessingNode":
            node = PreprocessingNode()
        elif node_type == "AIAnalysisNode":
            node = AIAnalysisNode()
        elif node_type == "FilterNode":
            node = FilterNode()
        elif node_type == "ActionNode":
            node = ActionNode()
        else:
            raise HTTPException(status_code=404, detail=f"Node type {node_type} not found")

        return node.get_node_info()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get node info: {str(e)}")


# Node Library Routes
@router.get("/api/nodes/library/types", response_model=List[str])
async def get_node_types():
    """Get list of all available node types."""
    try:
        from backend.node_engine.node_library import get_available_node_types

        return get_available_node_types()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get node types: {str(e)}")


@router.get("/api/nodes/library/types/{node_type}", response_model=Dict[str, Any])
async def get_node_type_info(node_type: str):
    """Get detailed information about a specific node type."""
    try:
        from backend.node_engine.node_library import get_node_info

        return get_node_info(node_type)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get node info: {str(e)}")


@router.get("/api/nodes/library/categories", response_model=Dict[str, List[Dict[str, Any]]])
async def get_nodes_by_category():
    """Get all nodes grouped by category."""
    try:
        from backend.node_engine.node_library import get_nodes_by_category

        return get_nodes_by_category()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get nodes by category: {str(e)}")


@router.get("/api/nodes/library/all", response_model=List[Dict[str, Any]])
async def get_all_nodes_info():
    """Get information about all available nodes."""
    try:
        from backend.node_engine.node_library import get_all_node_info

        return get_all_node_info()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get all nodes info: {str(e)}")


# Execution Management Routes
@router.get("/api/nodes/execution/active")
async def get_active_executions():
    """Get status of running node-based workflow executions."""
    try:
        # Return the active executions from the engine
        active_executions = []
        for exec_id, context in node_workflow_engine.active_executions.items():
            active_executions.append(
                {
                    "execution_id": exec_id,
                    "status": "running",
                    "execution_path": context.execution_path,
                    "start_time": context.metadata.get("start_time"),
                }
            )

        return {"active_executions": active_executions, "total_active": len(active_executions)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get active executions: {str(e)}")
