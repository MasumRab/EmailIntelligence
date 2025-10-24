"""
DEPRECATED: This module is part of the deprecated `backend` package.
It will be removed in a future release.

API routes for enhanced features: model management, workflows, and performance monitoring
"""

from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..plugins.plugin_manager import plugin_manager
from .model_manager import model_manager
from .performance_monitor import PerformanceMetric, performance_monitor
from .workflow_manager import Workflow, WorkflowManager, workflow_manager

router = APIRouter()


# Model Management Routes
class ModelInfoResponse(BaseModel):
    name: str
    path: str
    size_mb: float
    status: str
    load_time: float | None
    performance_metrics: Dict[str, Any] | None
    last_used: float | None


@router.get("/models", response_model=List[ModelInfoResponse])
async def get_models():
    """Get information about all available models."""
    models = model_manager.get_all_models()
    return [
        ModelInfoResponse(
            name=model.name,
            path=model.path,
            size_mb=model.size_mb,
            status=model.status.value,
            load_time=model.load_time,
            performance_metrics=model.performance_metrics,
            last_used=model.last_used,
        )
        for model in models
    ]


@router.post("/models/{model_name}/load")
async def load_model(model_name: str):
    """Load a specific model into memory."""
    success = model_manager.load_model(model_name)
    if not success:
        raise HTTPException(status_code=400, detail=f"Failed to load model {model_name}")
    return {"message": f"Model {model_name} loaded successfully"}


@router.post("/models/{model_name}/unload")
async def unload_model(model_name: str):
    """Unload a specific model from memory."""
    success = model_manager.unload_model(model_name)
    if not success:
        raise HTTPException(status_code=400, detail=f"Failed to unload model {model_name}")
    return {"message": f"Model {model_name} unloaded successfully"}


# Workflow Management Routes
class WorkflowCreateRequest(BaseModel):
    name: str
    description: str = ""


class WorkflowResponse(BaseModel):
    name: str
    description: str
    created_at: str
    updated_at: str
    version: str
    nodes: List[Dict[str, Any]]
    connections: List[Dict[str, Any]]
    config: Dict[str, Any]


@router.get("/workflows", response_model=List[str])
async def list_workflows():
    """List all available workflow files."""
    return workflow_manager.list_workflows()


@router.get("/workflows/{workflow_filename}", response_model=WorkflowResponse)
async def get_workflow(workflow_filename: str):
    """Get a specific workflow by filename."""
    workflow = workflow_manager.load_workflow(workflow_filename)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    return WorkflowResponse(
        name=workflow.name,
        description=workflow.description,
        created_at=workflow.created_at,
        updated_at=workflow.updated_at,
        version=workflow.version,
        nodes=workflow.nodes,
        connections=workflow.connections,
        config=workflow.config,
    )


@router.post("/workflows")
async def create_workflow(request: WorkflowCreateRequest):
    """Create a new workflow."""
    workflow = Workflow(request.name, request.description)
    # Add some default nodes for demonstration
    workflow.add_node("email_input", "input_1", 0, 0)
    workflow.add_node("nlp_processor", "processor_1", 200, 0)
    workflow.add_node("email_output", "output_1", 400, 0)

    # Connect the nodes
    workflow.add_connection("input_1", "output", "processor_1", "input")
    workflow.add_connection("processor_1", "output", "output_1", "input")

    success = workflow_manager.save_workflow(workflow)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to save workflow")

    return {"message": "Workflow created successfully", "workflow_name": workflow.name}


# Performance Monitoring Routes
class PerformanceMetricResponse(BaseModel):
    timestamp: float
    value: float
    unit: str
    source: str


@router.get("/performance/metrics", response_model=List[PerformanceMetricResponse])
async def get_performance_metrics(minutes: int = 5, source_filter: str = None):
    """Get recent performance metrics."""
    metrics = performance_monitor.get_recent_metrics(minutes, source_filter)
    return [
        PerformanceMetricResponse(
            timestamp=metric.timestamp, value=metric.value, unit=metric.unit, source=metric.source
        )
        for metric in metrics
    ]


@router.get("/performance/system-stats", response_model=Dict[str, float])
async def get_system_stats():
    """Get current system statistics."""
    return performance_monitor.get_system_stats()


@router.get("/performance/error-rate", response_model=float)
async def get_error_rate(minutes: int = 5):
    """Get the error rate in the last specified minutes."""
    return performance_monitor.get_error_rate(minutes)


# Plugin Management Routes
@router.get("/plugins")
async def get_plugins():
    """Get information about all loaded plugins."""
    all_plugins = plugin_manager.get_all_plugins()
    ui_plugins = plugin_manager.get_all_ui_plugins()
    processing_nodes = plugin_manager.get_all_processing_nodes()

    return {
        "regular_plugins": list(all_plugins.keys()),
        "ui_plugins": list(ui_plugins.keys()),
        "processing_nodes": list(processing_nodes.keys()),
    }
