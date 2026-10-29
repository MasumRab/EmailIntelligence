"""
API Routes for Dynamic Model Management.

This module provides FastAPI routes for managing AI models dynamically,
including loading, unloading, monitoring, and configuration.
"""

import logging
from typing import List, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from .dynamic_model_manager import DynamicModelManager
from .model_registry import ModelType

logger = logging.getLogger(__name__)

# Global model manager instance
_model_manager: Optional[DynamicModelManager] = None


async def get_model_manager() -> DynamicModelManager:
    """Dependency to get the model manager instance."""
    global _model_manager
    if _model_manager is None:
        _model_manager = DynamicModelManager()
        await _model_manager.initialize()
    return _model_manager


# Pydantic models for API
class ModelInfo(BaseModel):
    """Model information response."""

    id: str
    name: str
    type: str
    version: str
    status: str
    framework: str
    loaded: bool
    memory_usage: Optional[int] = None
    gpu_memory_usage: Optional[int] = None
    load_count: int
    usage_count: int
    health_status: str


class ModelPerformance(BaseModel):
    """Model performance metrics."""

    model_id: str
    load_count: int
    usage_count: int
    average_load_time: float
    average_inference_time: float
    error_rate: float
    memory_efficiency: float
    current_memory_usage: Optional[int] = None
    current_gpu_memory_usage: Optional[int] = None


class ModelRegistration(BaseModel):
    """Model registration request."""

    model_id: str = Field(..., description="Unique identifier for the model")
    name: str = Field(..., description="Human-readable name")
    model_type: ModelType = Field(..., description="Type of AI model")
    version: str = Field("1.0.0", description="Model version")
    framework: str = Field(
        ..., description="ML framework (sklearn, transformers, etc.)"
    )
    dependencies: List[str] = Field(
        default_factory=list, description="Required dependencies"
    )


class HealthStatus(BaseModel):
    """System health status."""

    status: str
    total_models: int
    loaded_models: int
    memory_usage: int
    gpu_memory_usage: int
    health_checks_enabled: bool
    memory_optimization_enabled: bool


class SystemMetrics(BaseModel):
    """Comprehensive system metrics."""

    total_models: int
    loaded_models: int
    unloaded_models: int
    total_memory_usage: int
    total_gpu_memory_usage: int
    models_by_type: dict
    models_by_framework: dict
    average_load_time: float
    health_summary: dict


# Create router
router = APIRouter(prefix="/api/models", tags=["Model Management"])


@router.get("/", response_model=List[ModelInfo])
async def list_models(
    include_loaded: bool = Query(True, description="Include loaded model details"),
    manager: DynamicModelManager = Depends(get_model_manager),
):
    """List all registered models with their status."""
    try:
        models = await manager.list_models()
        return [ModelInfo(**model) for model in models]
    except Exception as e:
        logger.error(f"Error listing models: {e}")
        raise HTTPException(status_code=500, detail="Failed to list models")


@router.get("/{model_id}", response_model=ModelInfo)
async def get_model(
    model_id: str, manager: DynamicModelManager = Depends(get_model_manager)
):
    """Get detailed information about a specific model."""
    try:
        model_info = await manager.get_model_info(model_id)
        if not model_info:
            raise HTTPException(status_code=404, detail=f"Model {model_id} not found")
        return ModelInfo(**model_info)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting model {model_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get model information")


@router.post("/{model_id}/load")
async def load_model(
    model_id: str,
    background_tasks: BackgroundTasks,
    manager: DynamicModelManager = Depends(get_model_manager),
):
    """Load a model into memory."""
    try:
        # Load in background to avoid blocking
        background_tasks.add_task(manager.load_model, model_id)
        return {"message": f"Loading model {model_id}", "status": "initiated"}
    except Exception as e:
        logger.error(f"Error initiating load for model {model_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to initiate model loading")


@router.post("/{model_id}/unload")
async def unload_model(
    model_id: str, manager: DynamicModelManager = Depends(get_model_manager)
):
    """Unload a model from memory."""
    try:
        success = await manager.unload_model(model_id)
        if not success:
            raise HTTPException(
                status_code=400, detail=f"Failed to unload model {model_id}"
            )
        return {"message": f"Model {model_id} unloaded successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error unloading model {model_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to unload model")


@router.post("/{model_id}/reload")
async def reload_model(
    model_id: str, manager: DynamicModelManager = Depends(get_model_manager)
):
    """Reload a model from disk."""
    try:
        success = await manager.reload_model(model_id)
        if not success:
            raise HTTPException(
                status_code=400, detail=f"Failed to reload model {model_id}"
            )
        return {"message": f"Model {model_id} reloaded successfully"}
    except Exception as e:
        logger.error(f"Error reloading model {model_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to reload model")


@router.post("/register")
async def register_model(
    registration: ModelRegistration,
    manager: DynamicModelManager = Depends(get_model_manager),
):
    """Register a new model."""
    try:
        from pathlib import Path

        from .model_registry import ModelMetadata

        # Create metadata
        metadata = ModelMetadata(
            model_id=registration.model_id,
            model_type=registration.model_type,
            name=registration.name,
            version=registration.version,
            path=Path("models") / registration.model_id,
            framework=registration.framework,
            dependencies=registration.dependencies,
        )

        success = await manager.register_model(metadata)
        if not success:
            raise HTTPException(status_code=400, detail="Failed to register model")

        return {"message": f"Model {registration.model_id} registered successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error registering model: {e}")
        raise HTTPException(status_code=500, detail="Failed to register model")


@router.delete("/{model_id}")
async def unregister_model(
    model_id: str, manager: DynamicModelManager = Depends(get_model_manager)
):
    """Unregister a model."""
    try:
        success = await manager.unregister_model(model_id)
        if not success:
            raise HTTPException(
                status_code=400, detail=f"Failed to unregister model {model_id}"
            )
        return {"message": f"Model {model_id} unregistered successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error unregistering model {model_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to unregister model")


@router.get("/{model_id}/performance", response_model=ModelPerformance)
async def get_model_performance(
    model_id: str, manager: DynamicModelManager = Depends(get_model_manager)
):
    """Get performance metrics for a model."""
    try:
        metrics = await manager.get_model_performance(model_id)
        if "error" in metrics:
            raise HTTPException(status_code=404, detail=metrics["error"])
        return ModelPerformance(**metrics)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting performance for model {model_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get performance metrics")


@router.post("/{model_id}/validate")
async def validate_model(
    model_id: str, manager: DynamicModelManager = Depends(get_model_manager)
):
    """Validate a model's integrity and functionality."""
    try:
        validation = await manager.validate_model(model_id)
        return validation
    except Exception as e:
        logger.error(f"Error validating model {model_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to validate model")


@router.post("/optimize-memory")
async def optimize_memory(manager: DynamicModelManager = Depends(get_model_manager)):
    """Trigger memory optimization."""
    try:
        result = await manager.optimize_memory()
        return {"message": "Memory optimization completed", "result": result}
    except Exception as e:
        logger.error(f"Error optimizing memory: {e}")
        raise HTTPException(status_code=500, detail="Failed to optimize memory")


@router.get("/health", response_model=HealthStatus)
async def get_health_status(manager: DynamicModelManager = Depends(get_model_manager)):
    """Get overall health status of the model management system."""
    try:
        return HealthStatus(**manager.get_health_status())
    except Exception as e:
        logger.error(f"Error getting health status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get health status")


@router.get("/metrics", response_model=SystemMetrics)
async def get_system_metrics(manager: DynamicModelManager = Depends(get_model_manager)):
    """Get comprehensive system metrics."""
    try:
        metrics = await manager.get_system_metrics()
        return SystemMetrics(**metrics)
    except Exception as e:
        logger.error(f"Error getting system metrics: {e}")
        raise HTTPException(status_code=500, detail="Failed to get system metrics")


@router.post("/{model_id}/config")
async def update_model_config(
    model_id: str,
    config_updates: dict,
    manager: DynamicModelManager = Depends(get_model_manager),
):
    """Update configuration for a model."""
    try:
        success = await manager.update_model_config(model_id, config_updates)
        if not success:
            raise HTTPException(
                status_code=400, detail=f"Failed to update config for model {model_id}"
            )
        return {"message": f"Configuration updated for model {model_id}"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating config for model {model_id}: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to update model configuration"
        )


@router.post("/{model_id}/version/{version}")
async def create_model_version(
    model_id: str,
    version: str,
    manager: DynamicModelManager = Depends(get_model_manager),
):
    """Create a new version of a model."""
    # This would require the actual model object to be passed
    # For now, return not implemented
    raise HTTPException(status_code=501, detail="Model versioning not yet implemented")


@router.post("/{model_id}/rollback/{version}")
async def rollback_model_version(
    model_id: str,
    version: str,
    manager: DynamicModelManager = Depends(get_model_manager),
):
    """Rollback a model to a specific version."""
    try:
        success = await manager.rollback_model(model_id, version)
        if not success:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to rollback model {model_id} to version {version}",
            )
        return {"message": f"Model {model_id} rolled back to version {version}"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error rolling back model {model_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to rollback model")


# Specialized endpoints for AI engine integration
@router.get("/available", response_model=List[dict])
async def get_available_models(
    manager: DynamicModelManager = Depends(get_model_manager),
):
    """Get list of available models for AI engine integration."""
    try:
        models = await manager.get_available_models()
        return models
    except Exception as e:
        logger.error(f"Error getting available models: {e}")
        raise HTTPException(status_code=500, detail="Failed to get available models")


@router.get("/sentiment/model")
async def get_sentiment_model(
    manager: DynamicModelManager = Depends(get_model_manager),
):
    """Get the best available sentiment analysis model."""
    try:
        model = await manager.get_sentiment_model()
        if model:
            return {"model_id": model.metadata.model_id, "status": "available"}
        else:
            return {"model_id": None, "status": "unavailable"}
    except Exception as e:
        logger.error(f"Error getting sentiment model: {e}")
        raise HTTPException(status_code=500, detail="Failed to get sentiment model")


@router.get("/topic/model")
async def get_topic_model(manager: DynamicModelManager = Depends(get_model_manager)):
    """Get the best available topic classification model."""
    try:
        model = await manager.get_topic_model()
        if model:
            return {"model_id": model.metadata.model_id, "status": "available"}
        else:
            return {"model_id": None, "status": "unavailable"}
    except Exception as e:
        logger.error(f"Error getting topic model: {e}")
        raise HTTPException(status_code=500, detail="Failed to get topic model")


@router.get("/intent/model")
async def get_intent_model(manager: DynamicModelManager = Depends(get_model_manager)):
    """Get the best available intent recognition model."""
    try:
        model = await manager.get_intent_model()
        if model:
            return {"model_id": model.metadata.model_id, "status": "available"}
        else:
            return {"model_id": None, "status": "unavailable"}
    except Exception as e:
        logger.error(f"Error getting intent model: {e}")
        raise HTTPException(status_code=500, detail="Failed to get intent model")


@router.get("/urgency/model")
async def get_urgency_model(manager: DynamicModelManager = Depends(get_model_manager)):
    """Get the best available urgency detection model."""
    try:
        model = await manager.get_urgency_model()
        if model:
            return {"model_id": model.metadata.model_id, "status": "available"}
        else:
            return {"model_id": None, "status": "unavailable"}
    except Exception as e:
        logger.error(f"Error getting urgency model: {e}")
        raise HTTPException(status_code=500, detail="Failed to get urgency model")
