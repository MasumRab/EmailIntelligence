"""
API routes for advanced workflow features: node-based workflows, advanced processing,
and enterprise workflow management
"""
from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import asyncio

from .dependencies import get_db
from .ai_engine import AdvancedAIEngine
from .model_manager import model_manager
from .workflow_engine import WorkflowEngine
from ..python_nlp.smart_filters import SmartFilterManager
from src.core.advanced_workflow_engine import (
    get_workflow_manager, 
    Workflow as AdvancedWorkflow,
    Connection,
    WorkflowExecutionResult
)

# Try to import security features
try:
    from src.core.security import get_security_manager, SecurityContext, Permission, SecurityLevel
    security_available = True
except ImportError:
    security_available = False
    SecurityContext = None


# Security dependency
async def get_security_context(request: Request) -> Optional[SecurityContext]:
    """Extract and validate security context from request"""
    if not security_available:
        return None
    
    security_manager = get_security_manager()
    
    # Look for session token in headers or cookies
    session_token = request.headers.get("x-session-token") or request.cookies.get("session_token")
    
    if session_token:
        return security_manager.validate_session(session_token)
    
    return None

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
    workflow_manager = get_workflow_manager()
    
    try:
        workflow = AdvancedWorkflow(
            name=request.name,
            description=request.description
        )
        workflow.nodes = request.nodes
        workflow.connections = [Connection.from_dict(conn) for conn in request.connections]
        
        # Save to workflow manager
        workflow_manager._workflows[workflow.workflow_id] = workflow
        
        # Also save to file
        success = workflow_manager.save_workflow(workflow)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to save workflow")
        
        return AdvancedWorkflowResponse(
            workflow_id=workflow.workflow_id,
            name=workflow.name,
            description=workflow.description,
            nodes=workflow.nodes,
            connections=workflow.connections,
            created_at=workflow.created_at,
            updated_at=workflow.updated_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create workflow: {str(e)}")


@router.get("/advanced/workflows", response_model=List[str])
async def list_advanced_workflows():
    """List all available advanced workflows."""
    workflow_manager = get_workflow_manager()
    return workflow_manager.list_workflows()


@router.get("/advanced/workflows/{workflow_id}", response_model=AdvancedWorkflowResponse)
async def get_advanced_workflow(workflow_id: str):
    """Get a specific advanced workflow by ID."""
    workflow_manager = get_workflow_manager()
    workflow = workflow_manager.get_workflow(workflow_id)
    
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    return AdvancedWorkflowResponse(
        workflow_id=workflow.workflow_id,
        name=workflow.name,
        description=workflow.description,
        nodes=workflow.nodes,
        connections=[conn.to_dict() for conn in workflow.connections],
        created_at=workflow.created_at,
        updated_at=workflow.updated_at
    )


@router.put("/advanced/workflows/{workflow_id}", response_model=AdvancedWorkflowResponse)
async def update_advanced_workflow(workflow_id: str, request: AdvancedWorkflowCreateRequest):
    """Update an existing advanced workflow."""
    workflow_manager = get_workflow_manager()
    existing_workflow = workflow_manager.get_workflow(workflow_id)
    
    if not existing_workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    # Update workflow properties
    existing_workflow.name = request.name
    existing_workflow.description = request.description
    existing_workflow.nodes = request.nodes
    existing_workflow.connections = [Connection.from_dict(conn) for conn in request.connections]
    existing_workflow.updated_at = asyncio.get_event_loop().time()
    
    # Save updated workflow
    success = workflow_manager.save_workflow(existing_workflow)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to save workflow")
    
    return AdvancedWorkflowResponse(
        workflow_id=existing_workflow.workflow_id,
        name=existing_workflow.name,
        description=existing_workflow.description,
        nodes=existing_workflow.nodes,
        connections=[conn.to_dict() for conn in existing_workflow.connections],
        created_at=existing_workflow.created_at,
        updated_at=existing_workflow.updated_at
    )


@router.delete("/advanced/workflows/{workflow_id}")
async def delete_advanced_workflow(workflow_id: str):
    """Delete an advanced workflow."""
    workflow_manager = get_workflow_manager()
    
    success = workflow_manager.delete_workflow(workflow_id)
    if not success:
        raise HTTPException(status_code=404, detail="Workflow not found or could not be deleted")
    
    return {"message": "Workflow deleted successfully"}


@router.post("/advanced/workflows/{workflow_id}/execute", response_model=ExecuteWorkflowResponse)
async def execute_advanced_workflow(
    workflow_id: str, 
    request: ExecuteWorkflowRequest,
    security_context: SecurityContext = Depends(get_security_context)
):
    """Execute an advanced workflow with provided inputs."""
    workflow_manager = get_workflow_manager()
    
    try:
        result = await workflow_manager.execute_workflow(
            workflow_id,
            initial_inputs=request.initial_inputs,
            security_context=security_context
        )
        
        return ExecuteWorkflowResponse(
            workflow_id=result.workflow_id,
            status=result.status,
            execution_time=result.execution_time,
            node_results=result.node_results,
            error=result.error
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to execute workflow: {str(e)}")


# Node Management Routes
@router.get("/advanced/nodes", response_model=List[str])
async def get_available_nodes():
    """Get list of available node types."""
    workflow_manager = get_workflow_manager()
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
        "description": f"Schema for {node_type} node type"
    }


# Workflow Execution Management Routes
@router.get("/advanced/execution/status")
async def get_execution_status():
    """Get status of running workflows."""
    workflow_manager = get_workflow_manager()
    running_workflows = workflow_manager.get_running_workflows()
    
    return {
        "running_workflows": running_workflows,
        "total_running": len(running_workflows)
    }


@router.post("/advanced/execution/cancel/{workflow_id}")
async def cancel_workflow_execution(workflow_id: str):
    """Cancel a running workflow execution."""
    workflow_manager = get_workflow_manager()
    
    success = workflow_manager.cancel_workflow(workflow_id)
    if success:
        return {"message": f"Workflow {workflow_id} cancelled successfully"}
    else:
        raise HTTPException(status_code=404, detail="Workflow not currently running or not found")