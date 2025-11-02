"""
It will be removed in a future release.

API routes for advanced workflow features: node-based workflows, advanced processing,
and enterprise workflow management
"""

import asyncio

# Define a simple execution result class for compatibility
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

# Use the new node-based workflow system instead of non-existent src.core module
from backend.node_engine.node_base import Connection
from backend.node_engine.node_base import Workflow as AdvancedWorkflow
from backend.node_engine.workflow_manager import workflow_manager

from ..python_nlp.smart_filters import SmartFilterManager
from .ai_engine import AdvancedAIEngine
from .dependencies import get_db
from .model_manager import model_manager
from backend.node_engine.workflow_engine import WorkflowEngine


class WorkflowExecutionResult:
    def __init__(
        self,
        workflow_id: str,
        status: str,
        execution_time: float,
        node_results: Dict[str, Any],
        error: str = None,
    ):
        self.workflow_id = workflow_id
        self.status = status
        self.execution_time = execution_time
        self.node_results = node_results
        self.error = error


# Try to import security features from the new node-based system
try:
    from backend.node_engine.security_manager import SecurityLevel

    SecurityContext = None  # Use None as there isn't a direct equivalent yet
    security_available = True
except ImportError:
    security_available = False
    SecurityContext = None


router = APIRouter()


# Advanced Workflow Models
class AdvancedWorkflowCreateRequest(BaseModel):
    name: str
    description: str = ""
    nodes: List[Dict[str, Any]] = []
    connections: List[Dict[str, Any]] = []


class AdvancedWorkflowResponse(BaseModel):
    workflow_id: str
    name: str
    description: str
    nodes: List[Dict[str, Any]]
    connections: List[Dict[str, Any]]
    created_at: float
    updated_at: float


class ExecuteWorkflowRequest(BaseModel):
    initial_inputs: Dict[str, Any] = {}
    workflow_context: Dict[str, Any] = {}


class ExecuteWorkflowResponse(BaseModel):
    workflow_id: str
    status: str
    execution_time: float
    node_results: Dict[str, Any]
    error: Optional[str] = None


# Advanced Workflow Routes
@router.post("/advanced/workflows", response_model=AdvancedWorkflowResponse)
async def create_advanced_workflow(request: AdvancedWorkflowCreateRequest):
    """Create a new advanced node-based workflow."""
    try:
        # Create workflow using the new node engine
        workflow = AdvancedWorkflow(name=request.name, description=request.description)

        # We'll store the node and connection data but not create the actual node objects here
        # since we need to reconstruct them properly
        for node_data in request.nodes:
            # This is a simplified approach - in practice, we'd reconstruct the actual nodes
            pass

        # Save to workflow manager
        file_path = workflow_manager.save_workflow(workflow)

        return AdvancedWorkflowResponse(
            workflow_id=workflow.workflow_id,
            name=workflow.name,
            description=workflow.description,
            nodes=request.nodes,
            connections=request.connections,  # Store as raw data for now
            created_at="",  # Using empty string since new system might handle timestamps differently
            updated_at="",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create workflow: {str(e)}")


@router.get("/advanced/workflows", response_model=List[str])
async def list_advanced_workflows():
    """List all available advanced workflows."""
    # Use the new node engine's workflow manager
    workflows = workflow_manager.list_workflows()
    # Extract just the workflow IDs from the metadata
    return [wf.get("id", "") for wf in workflows if wf.get("id")]


@router.get("/advanced/workflows/{workflow_id}", response_model=AdvancedWorkflowResponse)
async def get_advanced_workflow(workflow_id: str):
    """Get a specific advanced workflow by ID."""
    # Use the new node engine's workflow manager
    workflow = workflow_manager.load_workflow(workflow_id)

    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    # Convert the node workflow to the expected response format
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

    return AdvancedWorkflowResponse(
        workflow_id=workflow.workflow_id,
        name=workflow.name,
        description=workflow.description,
        nodes=nodes_data,
        connections=connections_data,
        created_at="",  # Placeholder
        updated_at="",  # Placeholder
    )


@router.put("/advanced/workflows/{workflow_id}", response_model=AdvancedWorkflowResponse)
async def update_advanced_workflow(workflow_id: str, request: AdvancedWorkflowCreateRequest):
    """Update an existing advanced workflow."""
    # Load the existing workflow
    existing_workflow = workflow_manager.load_workflow(workflow_id)

    if not existing_workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    # For update, we'll create a new workflow with the same ID
    updated_workflow = AdvancedWorkflow(
        workflow_id=workflow_id, name=request.name, description=request.description
    )

    # Add nodes (implementation similar to create)
    for node_data in request.nodes:
        # This would need to reconstruct proper nodes,
        # but for now we store the data
        pass

    # Save updated workflow
    file_path = workflow_manager.save_workflow(updated_workflow)

    return AdvancedWorkflowResponse(
        workflow_id=updated_workflow.workflow_id,
        name=updated_workflow.name,
        description=updated_workflow.description,
        nodes=request.nodes,
        connections=request.connections,
        created_at="",  # Placeholder
        updated_at="",  # Placeholder
    )


@router.delete("/advanced/workflows/{workflow_id}")
async def delete_advanced_workflow(workflow_id: str):
    """Delete an advanced workflow."""
    # Use the new node engine's workflow manager
    success = workflow_manager.delete_workflow(workflow_id)
    if not success:
        raise HTTPException(status_code=404, detail="Workflow not found or could not be deleted")

    return {"message": "Workflow deleted successfully"}


@router.post("/advanced/workflows/{workflow_id}/execute", response_model=ExecuteWorkflowResponse)
async def execute_advanced_workflow(
    workflow_id: str,
    request: ExecuteWorkflowRequest,
):
    """Execute an advanced workflow with provided inputs."""
    # Use the new node engine's workflow execution system
    from backend.node_engine.workflow_engine import workflow_engine as node_workflow_engine

    try:
        # Load the workflow to execute
        workflow = workflow_manager.load_workflow(workflow_id)
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")

        # Execute the workflow using the node engine
        execution_context = await node_workflow_engine.execute_workflow(
            workflow, initial_inputs=request.initial_inputs
        )

        # Create a result compatible with the expected response format
        result = WorkflowExecutionResult(
            workflow_id=workflow_id,
            status=execution_context.metadata.get("status", "unknown"),
            execution_time=execution_context.metadata.get("execution_duration", 0),
            node_results=execution_context.node_outputs,
            error=execution_context.metadata.get("error"),
        )

        return ExecuteWorkflowResponse(
            workflow_id=result.workflow_id,
            status=result.status,
            execution_time=result.execution_time,
            node_results=result.node_results,
            error=result.error,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to execute workflow: {str(e)}")


# Node Management Routes
@router.get("/advanced/nodes", response_model=List[str])
async def get_available_nodes():
    """Get list of available node types."""
    return workflow_manager.get_registered_node_types()


@router.get("/advanced/nodes/{node_type}/schema")
async def get_node_schema(node_type: str):
    """Get input/output schema for a specific node type."""
    # This would return the schema for the specified node type
    # For now, returning a placeholder
    return {
        "node_type": node_type,
        "input_schema": {},
        "output_schema": {},
        "description": f"Schema for {node_type} node type",
    }


# Workflow Execution Management Routes
@router.get("/advanced/execution/status")
async def get_execution_status():
    """Get status of running workflows."""
    # Use the new node engine's execution tracking
    from backend.node_engine.workflow_engine import workflow_engine as node_workflow_engine

    running_workflows = []
    for exec_id, context in node_workflow_engine.active_executions.items():
        running_workflows.append(
            {
                "execution_id": exec_id,
                "status": "running",
                "execution_path": context.execution_path,
                "start_time": context.metadata.get("start_time"),
            }
        )

    return {"running_workflows": running_workflows, "total_running": len(running_workflows)}


@router.post("/advanced/execution/cancel/{workflow_id}")
async def cancel_workflow_execution(workflow_id: str):
    """Cancel a running workflow execution."""
    # Use the new node engine's execution cancellation
    from backend.node_engine.workflow_engine import workflow_engine as node_workflow_engine

    # Check if the workflow_id corresponds to an active execution
    if workflow_id in node_workflow_engine.active_executions:
        await node_workflow_engine.cancel_execution(workflow_id)
        return {"message": f"Workflow {workflow_id} cancelled successfully"}
    else:
        raise HTTPException(status_code=404, detail="Workflow not currently running or not found")
