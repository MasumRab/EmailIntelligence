"""
API routes for managing both legacy and node-based workflows.
"""
import logging
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Union

from .dependencies import get_workflow_engine
from .workflow_engine import WorkflowEngine

# Import node-based workflow components
from backend.node_engine.node_base import Workflow as NodeWorkflow
from backend.node_engine.workflow_engine import workflow_engine as node_workflow_engine
from backend.node_engine.workflow_manager import workflow_manager as node_workflow_manager

logger = logging.getLogger(__name__)
router = APIRouter()


class WorkflowType:
    LEGACY = "legacy"
    NODE_BASED = "node_based"


def get_workflow_type(workflow_name: str) -> str:
    """
    Determine if a workflow is legacy or node-based.
    For now, we'll use a simple heuristic - if it exists in node workflow manager, it's node-based.
    """
    # Try to load from node workflow manager
    node_workflow = node_workflow_manager.load_workflow(workflow_name)
    if node_workflow:
        return WorkflowType.NODE_BASED
    
    # If not found in node system, assume it's legacy (handled by legacy engine)
    return WorkflowType.LEGACY

class WorkflowCreate(BaseModel):
    name: str = Field(..., description="The unique name for the workflow.")
    description: str = ""
    workflow_type: str = Field(default="legacy", description="Type of workflow: 'legacy' or 'node_based'")
    models: Dict[str, str] = Field(default={}, description="A dictionary mapping model types to model names for legacy workflows.")
    nodes: List[Dict[str, Any]] = Field(default=[], description="List of nodes for node-based workflows.")
    connections: List[Dict[str, str]] = Field(default=[], description="List of connections for node-based workflows.")

@router.post("/api/workflows", response_model=dict)
async def create_workflow(
    workflow_data: WorkflowCreate,
    workflow_engine: WorkflowEngine = Depends(get_workflow_engine),
):
    """Creates and persists a new workflow (either legacy or node-based)."""
    try:
        if workflow_data.workflow_type == "node_based":
            # Handle node-based workflow creation
            workflow = NodeWorkflow(
                name=workflow_data.name,
                description=workflow_data.description
            )
            
            # Create nodes from the request data
            for node_data in workflow_data.nodes:
                node_type = node_data.get("type")
                node_id = node_data.get("node_id")
                node_name = node_data.get("name", "")
                node_config = node_data.get("config", {})
                
                # Import and create the appropriate node based on type
                from backend.node_engine.email_nodes import (
                    EmailSourceNode, PreprocessingNode, AIAnalysisNode, 
                    FilterNode, ActionNode
                )
                
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
                    raise ValueError(f"Unknown node type: {node_type}")
                
                workflow.add_node(node)
            
            # Create connections
            for conn_data in workflow_data.connections:
                from backend.node_engine.node_base import Connection
                connection = Connection(
                    source_node_id=conn_data["source_node_id"],
                    source_port=conn_data["source_port"],
                    target_node_id=conn_data["target_node_id"],
                    target_port=conn_data["target_port"]
                )
                workflow.add_connection(connection)
            
            # Save the workflow using the node workflow manager
            node_workflow_manager.save_workflow(workflow)
            return {"message": f"Node-based workflow '{workflow_data.name}' created successfully."}
            
        else:
            # Handle legacy workflow creation (original behavior)
            await workflow_engine.create_and_register_workflow_from_config(workflow_data.model_dump())
            return {"message": f"Legacy workflow '{workflow_data.name}' created successfully."}
            
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to create workflow: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred while creating the workflow.")

@router.get("/api/workflows", response_model=list[str])
async def list_workflows(
    workflow_engine: WorkflowEngine = Depends(get_workflow_engine),
):
    """Lists the names of all registered workflows (both legacy and node-based)."""
    # Get legacy workflows
    legacy_workflows = workflow_engine.list_workflows()
    
    # Get node-based workflows
    node_workflows_data = node_workflow_manager.list_workflows()
    node_workflows = [wf.get("id", "") for wf in node_workflows_data if wf.get("id")]
    
    # Combine both lists
    all_workflows = legacy_workflows + node_workflows
    
    # Remove duplicates while preserving order
    seen = set()
    unique_workflows = []
    for wf in all_workflows:
        if wf not in seen:
            seen.add(wf)
            unique_workflows.append(wf)
    
    return unique_workflows

@router.get("/api/workflows/active", response_model=dict)
async def get_active_workflow(
    workflow_engine: WorkflowEngine = Depends(get_workflow_engine),
):
    """Gets information about the currently active workflow."""
    result = {}
    
    # Check for active legacy workflow
    if workflow_engine.active_workflow:
        result["active_legacy_workflow"] = workflow_engine.active_workflow.name
        result["type"] = "legacy"
    else:
        result["active_legacy_workflow"] = None
    
    # Note: For node-based workflows, there isn't a concept of "active" in the same way
    # as legacy workflows, so we don't track that here
    
    if not result["active_legacy_workflow"]:
        result["message"] = "No active legacy workflow set. Node-based workflows are executed on-demand."
        return result
    
    return result

@router.put("/api/workflows/active/{workflow_name}", response_model=dict)
async def set_active_workflow(
    workflow_name: str,
    workflow_engine: WorkflowEngine = Depends(get_workflow_engine),
):
    """Sets the active legacy workflow. Node-based workflows are executed on-demand."""
    try:
        # Determine workflow type
        wf_type = get_workflow_type(workflow_name)
        
        if wf_type == "node_based":
            # For node-based workflows, just verify it exists and inform the user
            # that node workflows are executed on-demand rather than being "active"
            node_workflow = node_workflow_manager.load_workflow(workflow_name)
            if not node_workflow:
                raise ValueError(f"Node-based workflow '{workflow_name}' not found")
            
            return {
                "message": f"Node-based workflow '{workflow_name}' verified. Node workflows are executed on-demand, not set as active."
            }
        else:
            # Legacy behavior for file-based workflows
            workflow_engine.set_active_workflow(workflow_name)
            return {"message": f"Active legacy workflow set to '{workflow_name}'."}
            
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to set active workflow: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


@router.get("/api/workflows/{workflow_name}", response_model=dict)
async def get_workflow(
    workflow_name: str,
    workflow_engine: WorkflowEngine = Depends(get_workflow_engine),
):
    """Gets a specific workflow by name (either legacy or node-based)."""
    try:
        # Determine workflow type
        wf_type = get_workflow_type(workflow_name)
        
        if wf_type == "node_based":
            # Get node-based workflow
            node_workflow = node_workflow_manager.load_workflow(workflow_name)
            if not node_workflow:
                raise HTTPException(status_code=404, detail=f"Node-based workflow '{workflow_name}' not found")
            
            # Convert to appropriate response format
            nodes_data = []
            for node_id, node in node_workflow.nodes.items():
                nodes_data.append({
                    "node_id": node.node_id,
                    "type": node.__class__.__name__,
                    "name": node.name,
                    "description": node.description,
                    "config": getattr(node, 'config', {})
                })
            
            connections_data = []
            for conn in node_workflow.connections:
                connections_data.append({
                    "source_node_id": conn.source_node_id,
                    "source_port": conn.source_port,
                    "target_node_id": conn.target_node_id,
                    "target_port": conn.target_port
                })
            
            return {
                "workflow_id": node_workflow.workflow_id,
                "name": node_workflow.name,
                "description": node_workflow.description,
                "type": "node_based",
                "nodes": nodes_data,
                "connections": connections_data
            }
        else:
            # For legacy workflows, we return basic info since the interface might be different
            # This might require checking if the workflow exists in the legacy engine
            legacy_workflows = workflow_engine.list_workflows()
            if workflow_name not in legacy_workflows:
                raise HTTPException(status_code=404, detail=f"Legacy workflow '{workflow_name}' not found")
            
            # Check if this is the active workflow
            active_workflow_name = None
            if workflow_engine.active_workflow:
                active_workflow_name = workflow_engine.active_workflow.name
                
            return {
                "name": workflow_name,
                "type": "legacy",
                "is_active": workflow_name == active_workflow_name
            }
            
    except Exception as e:
        logger.error(f"Failed to get workflow '{workflow_name}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred while retrieving the workflow.")


@router.delete("/api/workflows/{workflow_name}", response_model=dict)
async def delete_workflow(
    workflow_name: str,
    workflow_engine: WorkflowEngine = Depends(get_workflow_engine),
):
    """Deletes a specific workflow by name (either legacy or node-based)."""
    try:
        # Determine workflow type
        wf_type = get_workflow_type(workflow_name)
        
        if wf_type == "node_based":
            # Delete node-based workflow
            success = node_workflow_manager.delete_workflow(workflow_name)
            if not success:
                raise HTTPException(status_code=404, detail=f"Node-based workflow '{workflow_name}' not found")
            
            return {"message": f"Node-based workflow '{workflow_name}' deleted successfully."}
        else:
            # For legacy workflows, we may need to implement deletion if not already available
            # For now, we'll note that direct deletion may not be supported in the legacy system
            # This would require an enhancement to the legacy workflow engine
            legacy_workflows = workflow_engine.list_workflows()
            if workflow_name not in legacy_workflows:
                raise HTTPException(status_code=404, detail=f"Legacy workflow '{workflow_name}' not found")
            
            # Note: Legacy system may not support direct deletion of individual workflows
            # Implementation would depend on the legacy workflow engine's capabilities
            return {
                "message": f"Legacy workflow '{workflow_name}' found, but direct deletion not implemented in legacy system.",
                "workflow_type": "legacy"
            }
            
    except Exception as e:
        logger.error(f"Failed to delete workflow '{workflow_name}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred while deleting the workflow.")