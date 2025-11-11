"""
Workflow API Routes for the modular architecture.

This module defines the API routes for managing both legacy and node-based workflows.
"""

import logging
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException

from src.core.auth import get_current_active_user
from src.core.workflow_engine import get_workflow_manager
from src.core.models import WorkflowCreate

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/workflows", tags=["workflows"])


@router.get("/", response_model=List[dict])
async def list_workflows(
    current_user: str = Depends(get_current_active_user),
):
    """Lists all available workflows (both legacy and node-based).
    Requires authentication."""
    try:
        workflow_manager = get_workflow_manager()

        # Get legacy workflows
        legacy_workflows = workflow_manager.list_workflows()

        # Get node-based workflows
        node_workflows = workflow_manager.list_node_workflows()

        # Combine and deduplicate
        all_workflows = []
        seen = set()
        for wf in legacy_workflows + node_workflows:
            wf_name = wf.get("name") if isinstance(wf, dict) else str(wf)
            if wf_name not in seen:
                seen.add(wf_name)
                all_workflows.append(
                    {
                        "name": wf_name,
                        "type": "legacy" if wf in legacy_workflows else "node_based",
                        "description": wf.get("description", "") if isinstance(wf, dict) else "",
                    }
                )

        return all_workflows
    except Exception as e:
        logger.error(f"Error listing workflows: {e}")
        raise HTTPException(status_code=500, detail="Failed to list workflows")


@router.post("/", response_model=dict)
async def create_workflow(
    workflow_data: WorkflowCreate,
    current_user: str = Depends(get_current_active_user),
):
    """Creates and persists a new workflow (either legacy or node-based).
    Requires authentication."""
    try:
        workflow_manager = get_workflow_manager()

        if workflow_data.workflow_type == "node_based":
            # Handle node-based workflow creation
            result = await workflow_manager.create_node_workflow(workflow_data)
            return {"message": f"Node-based workflow '{workflow_data.name}' created successfully."}
        else:
            # Handle legacy workflow creation
            result = await workflow_manager.create_legacy_workflow(workflow_data)
            return {"message": f"Legacy workflow '{workflow_data.name}' created successfully."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to create workflow: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred while creating the workflow."
        )


@router.get("/active", response_model=dict)
async def get_active_workflow(
    current_user: str = Depends(get_current_active_user),
):
    """Gets information about the currently active workflow.
    Requires authentication."""
    try:
        workflow_manager = get_workflow_manager()
        result = await workflow_manager.get_active_workflow()
        return result
    except Exception as e:
        logger.error(f"Failed to get active workflow: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred."
        )


@router.put("/active/{workflow_name}", response_model=dict)
async def set_active_workflow(
    workflow_name: str,
):
    """Sets the active legacy workflow. Node-based workflows are executed on-demand."""
    try:
        workflow_manager = get_workflow_manager()
        result = await workflow_manager.set_active_workflow(workflow_name)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to set active workflow: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred."
        )


@router.get("/{workflow_name}", response_model=dict)
async def get_workflow(
    workflow_name: str,
):
    """Gets a specific workflow by name (either legacy or node-based)."""
    try:
        workflow_manager = get_workflow_manager()
        workflow = await workflow_manager.get_workflow(workflow_name)
        return workflow
    except Exception as e:
        logger.error(f"Failed to get workflow '{workflow_name}': {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred while retrieving the workflow."
        )


@router.delete("/{workflow_name}", response_model=dict)
async def delete_workflow(
    workflow_name: str,
):
    """Deletes a specific workflow by name (either legacy or node-based)."""
    try:
        workflow_manager = get_workflow_manager()
        result = await workflow_manager.delete_workflow(workflow_name)
        return result
    except Exception as e:
        logger.error(f"Failed to delete workflow '{workflow_name}': {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred while deleting the workflow."
        )