"""
API routes for managing workflows.
"""
import logging
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any

from .dependencies import get_workflow_engine
from .workflow_engine import WorkflowEngine

logger = logging.getLogger(__name__)
router = APIRouter()

class WorkflowCreate(BaseModel):
    name: str = Field(..., description="The unique name for the workflow.")
    description: str = ""
    models: Dict[str, str] = Field(..., description="A dictionary mapping model types to model names.")

@router.post("/api/workflows", response_model=dict)
async def create_workflow(
    workflow_data: WorkflowCreate,
    workflow_engine: WorkflowEngine = Depends(get_workflow_engine),
):
    """Creates and persists a new file-based workflow."""
    try:
        # This will call a new method on the engine to handle file creation
        await workflow_engine.create_and_register_workflow_from_config(workflow_data.model_dump())
        return {"message": f"Workflow '{workflow_data.name}' created successfully."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to create workflow: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred while creating the workflow.")

@router.get("/api/workflows", response_model=list[str])
async def list_workflows(
    workflow_engine: WorkflowEngine = Depends(get_workflow_engine),
):
    """Lists the names of all registered workflows."""
    return workflow_engine.list_workflows()

@router.get("/api/workflows/active", response_model=str)
async def get_active_workflow(
    workflow_engine: WorkflowEngine = Depends(get_workflow_engine),
):
    """Gets the name of the currently active workflow."""
    if not workflow_engine.active_workflow:
        raise HTTPException(status_code=404, detail="No active workflow set.")
    return workflow_engine.active_workflow.name

@router.put("/api/workflows/active/{workflow_name}", response_model=dict)
async def set_active_workflow(
    workflow_name: str,
    workflow_engine: WorkflowEngine = Depends(get_workflow_engine),
):
    """Sets the active workflow."""
    try:
        workflow_engine.set_active_workflow(workflow_name)
        return {"message": f"Active workflow set to '{workflow_name}'."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to set active workflow: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")