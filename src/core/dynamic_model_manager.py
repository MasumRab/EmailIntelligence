"""
Dynamic AI Model Management System.

This module provides a comprehensive system for dynamic loading, unloading,
versioning, and performance optimization of AI models with enterprise-grade
features for memory management, health monitoring, and API endpoints.
"""

import asyncio
import logging
import time
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, AsyncGenerator, Dict, List, Optional

from backend.python_backend.performance_monitor import log_performance

from .model_registry import ModelInstance, ModelMetadata, ModelRegistry, ModelType

logger = logging.getLogger(__name__)


class DynamicModelManager:
    """
    Advanced dynamic model manager with comprehensive AI model lifecycle management.

    Features:
    - Dynamic loading/unloading with memory optimization
    - Model versioning and rollback capabilities
    - Performance monitoring and metrics collection
    - Health checking and validation
    - Memory and GPU resource management
    - API endpoints for model operations
    """

    def __init__(self, models_dir: Path = None):
        self.registry = ModelRegistry(models_dir)
        self._health_check_interval = 300  # 5 minutes
        self._memory_optimization_interval = 600  # 10 minutes
        self._health_monitor_task: Optional[asyncio.Task] = None
        self._memory_optimizer_task: Optional[asyncio.Task] = None
        self._initialized = False

        logger.info("DynamicModelManager initialized")

    async def initialize(self):
        """Initialize the model manager and start background tasks."""
        if self._initialized:
            return

        # Discover existing models
        await self.registry.discover_models()

        # Start background monitoring tasks
        self._health_monitor_task = asyncio.create_task(self._health_monitor_loop())
        self._memory_optimizer_task = asyncio.create_task(self._memory_optimizer_loop())

        self._initialized = True
        logger.info("DynamicModelManager fully initialized with background monitoring")

    async def shutdown(self):
        """Shutdown the model manager and cleanup resources."""
        logger.info("Shutting down DynamicModelManager")

        # Stop background tasks
        if self._health_monitor_task:
            self._health_monitor_task.cancel()
            try:
                await self._health_monitor_task
            except asyncio.CancelledError:
                pass

        if self._memory_optimizer_task:
            self._memory_optimizer_task.cancel()
            try:
                await self._memory_optimizer_task
            except asyncio.CancelledError:
                pass

        # Unload all models
        loaded_models = list(self.registry._loaded_models.keys())
        for model_id in loaded_models:
            await self.registry.unload_model(model_id)

        logger.info("DynamicModelManager shutdown complete")

    @asynccontextmanager
    async def get_model(self, model_id: str) -> AsyncGenerator[ModelInstance, None]:
        """
        Get a model instance with automatic resource management.

        Usage:
            async with manager.get_model("sentiment_model") as model:
                result = await model.analyze("text")
        """
        instance = await self.registry.get_model(model_id)
        if not instance:
            raise ValueError(f"Model {model_id} could not be loaded")

        try:
            yield instance
        finally:
            # Update last accessed time
            instance.last_accessed = time.time()

    async def load_model(self, model_id: str) -> bool:
        """Load a model into memory."""
        instance = await self.registry.load_model(model_id)
        return instance is not None

    async def unload_model(self, model_id: str) -> bool:
        """Unload a model from memory."""
        return await self.registry.unload_model(model_id)

    async def register_model(self, metadata: ModelMetadata) -> bool:
        """Register a new model."""
        return await self.registry.register_model(metadata)

    async def unregister_model(self, model_id: str) -> bool:
        """Unregister a model."""
        return await self.registry.unregister_model(model_id)

    async def list_models(self) -> List[Dict[str, Any]]:
        """List all registered models with status."""
        return await self.registry.list_models()

    async def get_model_info(self, model_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific model."""
        models = await self.list_models()
        return next((model for model in models if model["id"] == model_id), None)

    async def get_model_performance(self, model_id: str) -> Dict[str, Any]:
        """Get performance metrics for a model."""
        return await self.registry.get_model_performance_metrics(model_id)

    async def validate_model(self, model_id: str) -> Dict[str, Any]:
        """Validate a model's integrity and functionality."""
        return await self.registry.validate_model(model_id)

    async def optimize_memory(self) -> Dict[str, Any]:
        """Manually trigger memory optimization."""
        return await self.registry.optimize_memory()

    async def create_model_version(self, model_id: str, version: str, model_object: Any) -> bool:
        """Create a new version of an existing model."""
        try:
            if model_id not in self.registry._registry:
                logger.error(f"Model {model_id} not found in registry")
                return False

            base_metadata = self.registry._registry[model_id]

            # Create new metadata for version
            version_metadata = ModelMetadata(
                model_id=f"{model_id}_v{version}",
                model_type=base_metadata.model_type,
                name=f"{base_metadata.name} v{version}",
                version=version,
                path=base_metadata.path / version,
                framework=base_metadata.framework,
                dependencies=base_metadata.dependencies.copy(),
                config=base_metadata.config.copy(),
            )

            # Save the model object
            await self._save_model_object(version_metadata, model_object)

            # Register the version
            return await self.register_model(version_metadata)

        except Exception as e:
            logger.error(f"Failed to create model version: {e}")
            return False

    async def rollback_model(self, model_id: str, version: str) -> bool:
        """Rollback a model to a specific version."""
        try:
            version_id = f"{model_id}_v{version}"

            if version_id not in self.registry._registry:
                logger.error(f"Version {version} of model {model_id} not found")
                return False

            # Unload current version if loaded
            if model_id in self.registry._loaded_models:
                await self.unload_model(model_id)

            # Load the specified version
            return await self.load_model(version_id)

        except Exception as e:
            logger.error(f"Failed to rollback model {model_id} to version {version}: {e}")
            return False

    async def get_available_models(self) -> List[Dict[str, Any]]:
        """Get list of available models for the AI engine."""
        models = await self.list_models()
        return [
            {
                "id": model["id"],
                "type": model["type"],
                "name": model["name"],
                "loaded": model["loaded"],
                "health_status": model["health_status"],
            }
            for model in models
        ]

    # Model-specific getters for AI engine compatibility
    async def get_sentiment_model(self):
        """Get the best available sentiment analysis model."""
        return await self._get_best_model_for_type(ModelType.SENTIMENT)

    async def get_topic_model(self):
        """Get the best available topic classification model."""
        return await self._get_best_model_for_type(ModelType.TOPIC)

    async def get_intent_model(self):
        """Get the best available intent recognition model."""
        return await self._get_best_model_for_type(ModelType.INTENT)

    async def get_urgency_model(self):
        """Get the best available urgency detection model."""
        return await self._get_best_model_for_type(ModelType.URGENCY)

    async def _get_best_model_for_type(self, model_type: ModelType):
        """Get the best available model for a specific type."""
        models = await self.list_models()
        type_models = [m for m in models if m["type"] == model_type.value and m["loaded"]]

        if not type_models:
            # Try to load one
            unloaded_models = [
                m for m in models if m["type"] == model_type.value and not m["loaded"]
            ]
            if unloaded_models:
                # Sort by usage count (prefer more used models)
                unloaded_models.sort(key=lambda x: x.get("usage_count", 0), reverse=True)
                best_model = unloaded_models[0]
                await self.load_model(best_model["id"])
                return await self.registry.get_model(best_model["id"])

            return None

        # Return the most recently used loaded model
        type_models.sort(key=lambda x: x.get("last_used", 0), reverse=True)
        best_model = type_models[0]
        return await self.registry.get_model(best_model["id"])

    async def _save_model_object(self, metadata: ModelMetadata, model_object: Any):
        """Save a model object to disk."""
        try:
            # Create model directory
            model_dir = metadata.path
            model_dir.mkdir(parents=True, exist_ok=True)

            if metadata.framework == "sklearn":
                import joblib

                model_file = model_dir / f"{metadata.model_id}.pkl"
                joblib.dump(model_object, model_file)
                metadata.size_bytes = model_file.stat().st_size

            elif metadata.framework == "transformers":
                # For transformers, assume model is already saved
                # Could implement saving logic here
                pass

            # Save metadata
            await self.registry._save_metadata(metadata)

        except Exception as e:
            logger.error(f"Failed to save model object {metadata.model_id}: {e}")
            raise

    async def _health_monitor_loop(self):
        """Background task for continuous health monitoring."""
        while True:
            try:
                await asyncio.sleep(self._health_check_interval)

                # Perform health checks on all registered models
                model_ids = list(self.registry._registry.keys())
                for model_id in model_ids:
                    try:
                        validation = await self.validate_model(model_id)
                        if not validation.get("valid", False):
                            logger.warning(
                                f"Model {model_id} failed health check: {validation.get('issues', [])}"
                            )
                    except Exception as e:
                        logger.error(f"Health check failed for model {model_id}: {e}")

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Health monitor error: {e}")
                await asyncio.sleep(60)  # Wait before retrying

    async def _memory_optimizer_loop(self):
        """Background task for automatic memory optimization."""
        while True:
            try:
                await asyncio.sleep(self._memory_optimization_interval)

                # Perform memory optimization
                optimization_result = await self.optimize_memory()
                if optimization_result.get("unloaded_models"):
                    logger.info(f"Memory optimization: {optimization_result}")

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Memory optimizer error: {e}")
                await asyncio.sleep(60)  # Wait before retrying

    # API-friendly methods for external access
    def get_health_status(self) -> Dict[str, Any]:
        """Get overall health status of the model manager."""
        loaded_models = len(self.registry._loaded_models)
        total_models = len(self.registry._registry)

        return {
            "status": "healthy" if self._initialized else "initializing",
            "total_models": total_models,
            "loaded_models": loaded_models,
            "memory_usage": sum(
                inst.memory_usage for inst in self.registry._loaded_models.values()
            ),
            "gpu_memory_usage": sum(
                inst.gpu_memory_usage for inst in self.registry._loaded_models.values()
            ),
            "health_checks_enabled": self._health_monitor_task is not None,
            "memory_optimization_enabled": self._memory_optimizer_task is not None,
        }

    async def reload_model(self, model_id: str) -> bool:
        """Reload a model from disk."""
        try:
            # Unload if currently loaded
            await self.unload_model(model_id)

            # Load fresh from disk
            return await self.load_model(model_id)

        except Exception as e:
            logger.error(f"Failed to reload model {model_id}: {e}")
            return False

    async def update_model_config(self, model_id: str, config_updates: Dict[str, Any]) -> bool:
        """Update configuration for a model."""
        try:
            if model_id not in self.registry._registry:
                return False

            metadata = self.registry._registry[model_id]
            metadata.config.update(config_updates)

            # Save updated metadata
            await self.registry._save_metadata(metadata)

            logger.info(f"Updated configuration for model {model_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to update model config {model_id}: {e}")
            return False

    async def get_system_metrics(self) -> Dict[str, Any]:
        """Get comprehensive system metrics."""
        models = await self.list_models()
        loaded_models = [m for m in models if m["loaded"]]

        return {
            "total_models": len(models),
            "loaded_models": len(loaded_models),
            "unloaded_models": len(models) - len(loaded_models),
            "total_memory_usage": sum(m.get("memory_usage", 0) for m in loaded_models),
            "total_gpu_memory_usage": sum(m.get("gpu_memory_usage", 0) for m in loaded_models),
            "models_by_type": self._count_models_by_type(models),
            "models_by_framework": self._count_models_by_framework(models),
            "average_load_time": self._calculate_average_load_time(models),
            "health_summary": self._get_health_summary(models),
        }

    def _count_models_by_type(self, models: List[Dict[str, Any]]) -> Dict[str, int]:
        """Count models by type."""
        counts = {}
        for model in models:
            model_type = model.get("type", "unknown")
            counts[model_type] = counts.get(model_type, 0) + 1
        return counts

    def _count_models_by_framework(self, models: List[Dict[str, Any]]) -> Dict[str, int]:
        """Count models by framework."""
        counts = {}
        for model in models:
            framework = model.get("framework", "unknown")
            counts[framework] = counts.get(framework, 0) + 1
        return counts

    def _calculate_average_load_time(self, models: List[Dict[str, Any]]) -> float:
        """Calculate average load time across all models."""
        load_times = []
        for model in models:
            metrics = model.get("performance_metrics", {})
            avg_load_time = metrics.get("avg_load_time")
            if avg_load_time:
                load_times.append(avg_load_time)

        return sum(load_times) / len(load_times) if load_times else 0.0

    def _get_health_summary(self, models: List[Dict[str, Any]]) -> Dict[str, int]:
        """Get health summary across all models."""
        summary = {"healthy": 0, "unhealthy": 0, "unknown": 0}
        for model in models:
            health = model.get("health_status", "unknown")
            if health in summary:
                summary[health] += 1
        return summary
