"""
DEPRECATED: This module is part of the deprecated `backend` package.
It will be removed in a future release.

API routes for enhanced features: model management, workflows, and performance monitoring
"""

from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.backend.node_engine.workflow_manager import workflow_manager

from ..plugins.plugin_manager import plugin_manager
from .model_manager import model_manager
from .performance_monitor import performance_monitor

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
        raise HTTPException(
            status_code=400, detail=f"Failed to load model {model_name}"
        )
    return {"message": f"Model {model_name} loaded successfully"}


@router.post("/models/{model_name}/unload")
async def unload_model(model_name: str):
    """Unload a specific model from memory."""
    success = model_manager.unload_model(model_name)
    if not success:
        raise HTTPException(
            status_code=400, detail=f"Failed to unload model {model_name}"
        )
    return {"message": f"Model {model_name} unloaded successfully"}


# Workflow Management Routes
class WorkflowCreateRequest(BaseModel):
    name: str
    description: str = ""


class WorkflowResponse(BaseModel):
    workflow_id: str
    name: str
    description: str
    nodes: Dict[str, Any]
    connections: List[Dict[str, Any]]


@router.get("/workflows", response_model=List[Dict[str, Any]])
async def list_workflows():
    """List all available workflow files."""
    return workflow_manager.list_workflows()


@router.get("/workflows/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow(workflow_id: str):
    """Get a specific workflow by ID."""
    workflow = workflow_manager.load_workflow(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    nodes = {
        node_id: {
            "id": node.node_id,
            "name": node.name,
            "type": node.__class__.__name__,
            "description": node.description,
        }
        for node_id, node in workflow.nodes.items()
    }
    connections = [
        {
            "source_node": conn.source_node_id,
            "source_output": conn.source_port,
            "target_node": conn.target_node_id,
            "target_input": conn.target_port,
        }
        for conn in workflow.connections
    ]

    return WorkflowResponse(
        workflow_id=workflow.workflow_id,
        name=workflow.name,
        description=workflow.description,
        nodes=nodes,
        connections=connections,
    )


@router.post("/workflows")
async def create_workflow(request: WorkflowCreateRequest):
    """Create a new workflow."""
    from src.backend.node_engine.email_nodes import (
        AIAnalysisNode,
        EmailSourceNode,
        PreprocessingNode,
    )
    from src.backend.node_engine.node_base import Workflow

    workflow = Workflow(name=request.name, description=request.description)
    # Add some default nodes for demonstration
    input_node = EmailSourceNode(node_id="input_1", name="Email Input")
    processor_node = PreprocessingNode(node_id="processor_1", name="Preprocessing")
    output_node = AIAnalysisNode(node_id="output_1", name="AI Analysis")

    workflow.add_node(input_node)
    workflow.add_node(processor_node)
    workflow.add_node(output_node)

    # Connect the nodes
    from src.backend.node_engine.node_base import Connection

    workflow.add_connection(Connection("input_1", "emails", "processor_1", "emails"))
    workflow.add_connection(
        Connection("processor_1", "processed_emails", "output_1", "emails")
    )

    file_path = workflow_manager.save_workflow(workflow)

    return {
        "message": "Workflow created successfully",
        "workflow_id": workflow.workflow_id,
        "file_path": file_path,
    }


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
            timestamp=metric.timestamp,
            value=metric.value,
            unit=metric.unit,
            source=metric.source,
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
