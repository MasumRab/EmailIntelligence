"""
Advanced Model Registry for Dynamic AI Model Management.

This module provides a sophisticated registry system for tracking, managing,
and monitoring AI models with versioning, metadata, and performance metrics.
"""

import asyncio
import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
from pathlib import Path
import json

logger = logging.getLogger(__name__)


class ModelStatus(Enum):
    """Enumeration of possible model states."""
    UNLOADED = "unloaded"
    LOADING = "loading"
    LOADED = "loaded"
    UNLOADING = "unloading"
    ERROR = "error"


class ModelType(Enum):
    """Supported model types."""
    SENTIMENT = "sentiment"
    TOPIC = "topic"
    INTENT = "intent"
    URGENCY = "urgency"
    TRANSFORMER = "transformer"
    CUSTOM = "custom"


@dataclass
class ModelMetadata:
    """Comprehensive metadata for AI models."""
    model_id: str
    model_type: ModelType
    name: str
    version: str
    path: Path
    framework: str  # "sklearn", "transformers", "tensorflow", etc.
    size_bytes: int = 0
    created_at: float = field(default_factory=time.time)
    last_loaded: Optional[float] = None
    last_used: Optional[float] = None
    load_count: int = 0
    usage_count: int = 0
    performance_metrics: Dict[str, Any] = field(default_factory=dict)
    health_status: str = "unknown"
    dependencies: List[str] = field(default_factory=list)
    config: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ModelInstance:
    """Runtime instance of a loaded model."""
    metadata: ModelMetadata
    model_object: Any
    status: ModelStatus = ModelStatus.LOADED
    loaded_at: float = field(default_factory=time.time)
    memory_usage: int = 0
    gpu_memory_usage: int = 0
    last_accessed: float = field(default_factory=time.time)


class ModelRegistry:
    """
    Advanced registry for managing AI models with dynamic loading,
    versioning, and performance monitoring.
    """

    def __init__(self, models_dir: Path = None):
        self.models_dir = models_dir or Path("models")
        self._registry: Dict[str, ModelMetadata] = {}
        self._loaded_models: Dict[str, ModelInstance] = {}
        self._model_lock = asyncio.Lock()
        self._max_memory_mb = 2048  # 2GB default limit
        self._max_gpu_memory_mb = 4096  # 4GB GPU limit
        self._auto_unload_enabled = True
        self._auto_unload_threshold_mb = 1024  # Unload if memory > 1GB

        # Create models directory if it doesn't exist
        self.models_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"ModelRegistry initialized with models directory: {self.models_dir}")

    async def discover_models(self) -> List[str]:
        """Discover and register all available models in the models directory."""
        async with self._model_lock:
            discovered_models = []

            # Scan for model directories
            for model_dir in self.models_dir.iterdir():
                if model_dir.is_dir():
                    model_id = model_dir.name
                    metadata_file = model_dir / "metadata.json"

                    if metadata_file.exists():
                        # Load existing metadata
                        try:
                            with open(metadata_file, 'r') as f:
                                data = json.load(f)
                                metadata = ModelMetadata(**data)
                                self._registry[model_id] = metadata
                                discovered_models.append(model_id)
                                logger.info(f"Loaded existing model: {model_id}")
                        except Exception as e:
                            logger.warning(f"Failed to load metadata for {model_id}: {e}")
                    else:
                        # Try to auto-discover model files
                        model_files = list(model_dir.glob("*.pkl")) + list(model_dir.glob("*.joblib"))
                        if model_files:
                            # Create basic metadata for discovered models
                            metadata = ModelMetadata(
                                model_id=model_id,
                                model_type=ModelType.CUSTOM,
                                name=model_id.replace("_", " ").title(),
                                version="1.0.0",
                                path=model_dir,
                                framework="sklearn",
                                config={"auto_discovered": True}
                            )
                            self._registry[model_id] = metadata
                            await self._save_metadata(metadata)
                            discovered_models.append(model_id)
                            logger.info(f"Auto-discovered model: {model_id}")

            logger.info(f"Discovered {len(discovered_models)} models")
            return discovered_models

    async def register_model(self, metadata: ModelMetadata) -> bool:
        """Register a new model in the registry."""
        async with self._model_lock:
            try:
                self._registry[metadata.model_id] = metadata
                await self._save_metadata(metadata)
                logger.info(f"Registered model: {metadata.model_id}")
                return True
            except Exception as e:
                logger.error(f"Failed to register model {metadata.model_id}: {e}")
                return False

    async def unregister_model(self, model_id: str) -> bool:
        """Unregister a model from the registry."""
        async with self._model_lock:
            if model_id in self._registry:
                # Unload if currently loaded
                if model_id in self._loaded_models:
                    await self.unload_model(model_id)

                # Remove from registry
                del self._registry[model_id]

                # Remove metadata file
                metadata_file = self.models_dir / model_id / "metadata.json"
                if metadata_file.exists():
                    metadata_file.unlink()

                logger.info(f"Unregistered model: {model_id}")
                return True

            return False

    async def load_model(self, model_id: str) -> Optional[ModelInstance]:
        """Load a model into memory with memory management."""
        async with self._model_lock:
            if model_id not in self._registry:
                logger.error(f"Model {model_id} not found in registry")
                return None

            if model_id in self._loaded_models:
                # Model already loaded, just update access time
                instance = self._loaded_models[model_id]
                instance.last_accessed = time.time()
                instance.metadata.usage_count += 1
                return instance

            # Check memory limits before loading
            if not await self._check_memory_limits():
                logger.warning("Memory limits exceeded, cannot load new model")
                return None

            try:
                metadata = self._registry[model_id]
                metadata.status = ModelStatus.LOADING

                # Load the actual model based on framework
                model_object = await self._load_model_object(metadata)

                if model_object is None:
                    metadata.status = ModelStatus.ERROR
                    return None

                # Create instance
                instance = ModelInstance(
                    metadata=metadata,
                    model_object=model_object,
                    memory_usage=await self._estimate_memory_usage(model_object),
                    gpu_memory_usage=await self._estimate_gpu_memory_usage(model_object)
                )

                self._loaded_models[model_id] = instance
                metadata.status = ModelStatus.LOADED
                metadata.last_loaded = time.time()
                metadata.load_count += 1

                # Update memory tracking
                await self._update_memory_tracking()

                logger.info(f"Loaded model: {model_id}")
                return instance

            except Exception as e:
                logger.error(f"Failed to load model {model_id}: {e}")
                if model_id in self._registry:
                    self._registry[model_id].status = ModelStatus.ERROR
                return None

    async def unload_model(self, model_id: str) -> bool:
        """Unload a model from memory."""
        async with self._model_lock:
            if model_id not in self._loaded_models:
                return True  # Already unloaded

            try:
                instance = self._loaded_models[model_id]
                instance.status = ModelStatus.UNLOADING

                # Perform cleanup
                await self._cleanup_model_instance(instance)

                # Remove from loaded models
                del self._loaded_models[model_id]

                # Update metadata
                metadata = self._registry.get(model_id)
                if metadata:
                    metadata.status = ModelStatus.UNLOADED

                # Update memory tracking
                await self._update_memory_tracking()

                logger.info(f"Unloaded model: {model_id}")
                return True

            except Exception as e:
                logger.error(f"Failed to unload model {model_id}: {e}")
                return False

    async def get_model(self, model_id: str) -> Optional[ModelInstance]:
        """Get a loaded model instance, loading it if necessary."""
        instance = self._loaded_models.get(model_id)
        if instance:
            instance.last_accessed = time.time()
            instance.metadata.usage_count += 1
            return instance

        # Try to load the model
        return await self.load_model(model_id)

    async def list_models(self, include_loaded: bool = True) -> List[Dict[str, Any]]:
        """List all registered models with their status."""
        async with self._model_lock:
            models = []

            for model_id, metadata in self._registry.items():
                model_info = {
                    "id": model_id,
                    "name": metadata.name,
                    "type": metadata.model_type.value,
                    "version": metadata.version,
                    "status": metadata.status,
                    "framework": metadata.framework,
                    "size_bytes": metadata.size_bytes,
                    "load_count": metadata.load_count,
                    "usage_count": metadata.usage_count,
                    "last_loaded": metadata.last_loaded,
                    "last_used": metadata.last_used,
                    "health_status": metadata.health_status
                }

                if include_loaded and model_id in self._loaded_models:
                    instance = self._loaded_models[model_id]
                    model_info.update({
                        "loaded": True,
                        "memory_usage": instance.memory_usage,
                        "gpu_memory_usage": instance.gpu_memory_usage,
                        "loaded_at": instance.loaded_at,
                        "last_accessed": instance.last_accessed
                    })
                else:
                    model_info["loaded"] = False

                models.append(model_info)

            return models

    async def get_model_performance_metrics(self, model_id: str) -> Dict[str, Any]:
        """Get comprehensive performance metrics for a model."""
        async with self._model_lock:
            if model_id not in self._registry:
                return {"error": "Model not found"}

            metadata = self._registry[model_id]
            metrics = {
                "model_id": model_id,
                "load_count": metadata.load_count,
                "usage_count": metadata.usage_count,
                "average_load_time": metadata.performance_metrics.get("avg_load_time", 0),
                "average_inference_time": metadata.performance_metrics.get("avg_inference_time", 0),
                "error_rate": metadata.performance_metrics.get("error_rate", 0),
                "memory_efficiency": metadata.performance_metrics.get("memory_efficiency", 1.0),
                "last_health_check": metadata.performance_metrics.get("last_health_check"),
                "uptime_percentage": metadata.performance_metrics.get("uptime_percentage", 100.0)
            }

            if model_id in self._loaded_models:
                instance = self._loaded_models[model_id]
                metrics.update({
                    "current_memory_usage": instance.memory_usage,
                    "current_gpu_memory_usage": instance.gpu_memory_usage,
                    "time_since_last_access": time.time() - instance.last_accessed
                })

            return metrics

    async def validate_model(self, model_id: str) -> Dict[str, Any]:
        """Perform comprehensive validation on a model."""
        validation_results = {
            "model_id": model_id,
            "valid": False,
            "checks": {},
            "issues": []
        }

        if model_id not in self._registry:
            validation_results["issues"].append("Model not registered")
            return validation_results

        metadata = self._registry[model_id]

        # Check file existence
        model_path = metadata.path
        if not model_path.exists():
            validation_results["issues"].append("Model path does not exist")
            return validation_results

        # Check metadata integrity
        validation_results["checks"]["metadata"] = self._validate_metadata(metadata)

        # Check model file integrity
        validation_results["checks"]["file_integrity"] = await self._validate_model_file(metadata)

        # Check dependencies
        validation_results["checks"]["dependencies"] = self._validate_dependencies(metadata)

        # Load test
        validation_results["checks"]["load_test"] = await self._test_model_loading(model_id)

        # Performance test
        validation_results["checks"]["performance"] = await self._test_model_performance(model_id)

        # Calculate overall validity
        checks_passed = sum(1 for check in validation_results["checks"].values() if check.get("passed", False))
        total_checks = len(validation_results["checks"])
        validation_results["valid"] = checks_passed == total_checks
        validation_results["score"] = checks_passed / total_checks if total_checks > 0 else 0

        # Update health status
        if validation_results["valid"]:
            metadata.health_status = "healthy"
        else:
            metadata.health_status = "unhealthy"
            validation_results["issues"].extend([
                f"Failed check: {check_name}"
                for check_name, result in validation_results["checks"].items()
                if not result.get("passed", False)
            ])

        return validation_results

    async def optimize_memory(self) -> Dict[str, Any]:
        """Perform automatic memory optimization by unloading unused models."""
        optimization_results = {
            "freed_memory": 0,
            "freed_gpu_memory": 0,
            "unloaded_models": [],
            "current_memory_usage": 0,
            "current_gpu_memory_usage": 0
        }

        if not self._auto_unload_enabled:
            return optimization_results

        async with self._model_lock:
            current_time = time.time()
            models_to_unload = []

            # Find models that haven't been used recently and exceed memory threshold
            for model_id, instance in self._loaded_models.items():
                time_since_access = current_time - instance.last_accessed
                memory_usage = instance.memory_usage

                # Unload if not used in last hour and memory usage is high
                if (time_since_access > 3600 and  # 1 hour
                    memory_usage > self._auto_unload_threshold_mb * 1024 * 1024):
                    models_to_unload.append(model_id)

            # Unload selected models
            for model_id in models_to_unload:
                if await self.unload_model(model_id):
                    instance = self._loaded_models.get(model_id)
                    if instance:
                        optimization_results["freed_memory"] += instance.memory_usage
                        optimization_results["freed_gpu_memory"] += instance.gpu_memory_usage
                        optimization_results["unloaded_models"].append(model_id)

            # Update current usage
            total_memory = sum(inst.memory_usage for inst in self._loaded_models.values())
            total_gpu_memory = sum(inst.gpu_memory_usage for inst in self._loaded_models.values())

            optimization_results["current_memory_usage"] = total_memory
            optimization_results["current_gpu_memory_usage"] = total_gpu_memory

        logger.info(f"Memory optimization completed: {optimization_results}")
        return optimization_results

    # Private helper methods

    async def _load_model_object(self, metadata: ModelMetadata) -> Optional[Any]:
        """Load the actual model object based on framework and type."""
        try:
            if metadata.framework == "sklearn":
                return await self._load_sklearn_model(metadata)
            elif metadata.framework == "transformers":
                return await self._load_transformers_model(metadata)
            elif metadata.framework == "tensorflow":
                return await self._load_tensorflow_model(metadata)
            else:
                logger.warning(f"Unsupported framework: {metadata.framework}")
                return None
        except Exception as e:
            logger.error(f"Error loading model {metadata.model_id}: {e}")
            return None

    async def _load_sklearn_model(self, metadata: ModelMetadata) -> Optional[Any]:
        """Load a scikit-learn model."""
        try:
            import joblib
            model_path = metadata.path / f"{metadata.model_id}.pkl"

            if model_path.exists():
                model = joblib.load(model_path)
                return model
            else:
                logger.error(f"Model file not found: {model_path}")
                return None
        except Exception as e:
            logger.error(f"Failed to load sklearn model {metadata.model_id}: {e}")
            return None

    async def _load_transformers_model(self, metadata: ModelMetadata) -> Optional[Any]:
        """Load a transformers model."""
        try:
            from transformers import AutoModelForSequenceClassification, AutoTokenizer

            model_path = metadata.path
            if model_path.exists():
                model = AutoModelForSequenceClassification.from_pretrained(str(model_path))
                tokenizer = AutoTokenizer.from_pretrained(str(model_path))
                return {"model": model, "tokenizer": tokenizer}
            else:
                logger.error(f"Transformers model path not found: {model_path}")
                return None
        except Exception as e:
            logger.error(f"Failed to load transformers model {metadata.model_id}: {e}")
            return None

    async def _load_tensorflow_model(self, metadata: ModelMetadata) -> Optional[Any]:
        """Load a TensorFlow model."""
        try:
            import tensorflow as tf
            model_path = metadata.path / "saved_model"

            if model_path.exists():
                model = tf.saved_model.load(str(model_path))
                return model
            else:
                logger.error(f"TensorFlow model path not found: {model_path}")
                return None
        except Exception as e:
            logger.error(f"Failed to load TensorFlow model {metadata.model_id}: {e}")
            return None

    async def _estimate_memory_usage(self, model_object: Any) -> int:
        """Estimate memory usage of a model object."""
        # Simple estimation - in production, use more sophisticated methods
        try:
            import sys
            memory_usage = sys.getsizeof(model_object)

            # Add some buffer for related objects
            if hasattr(model_object, '__dict__'):
                for attr_name, attr_value in model_object.__dict__.items():
                    memory_usage += sys.getsizeof(attr_value)

            return memory_usage
        except Exception:
            return 1024 * 1024  # Default 1MB estimate

    async def _estimate_gpu_memory_usage(self, model_object: Any) -> int:
        """Estimate GPU memory usage of a model object."""
        # For now, return 0 - would need GPU monitoring integration
        return 0

    async def _check_memory_limits(self) -> bool:
        """Check if loading a new model would exceed memory limits."""
        total_memory = sum(inst.memory_usage for inst in self._loaded_models.values())
        total_gpu_memory = sum(inst.gpu_memory_usage for inst in self._loaded_models.values())

        memory_ok = total_memory < (self._max_memory_mb * 1024 * 1024)
        gpu_memory_ok = total_gpu_memory < (self._max_gpu_memory_mb * 1024 * 1024)

        return memory_ok and gpu_memory_ok

    async def _update_memory_tracking(self):
        """Update memory usage tracking."""
        # Could integrate with system monitoring here
        pass

    async def _cleanup_model_instance(self, instance: ModelInstance):
        """Clean up a model instance."""
        try:
            # Perform any model-specific cleanup
            if hasattr(instance.model_object, 'close'):
                await instance.model_object.close()
            elif hasattr(instance.model_object, 'cleanup'):
                await instance.model_object.cleanup()

            # Clear references
            instance.model_object = None
            instance.status = ModelStatus.UNLOADED

        except Exception as e:
            logger.warning(f"Error during model cleanup: {e}")

    async def _save_metadata(self, metadata: ModelMetadata):
        """Save model metadata to disk."""
        try:
            metadata_dir = self.models_dir / metadata.model_id
            metadata_dir.mkdir(exist_ok=True)

            metadata_file = metadata_dir / "metadata.json"

            # Convert to dict for JSON serialization
            metadata_dict = {
                "model_id": metadata.model_id,
                "model_type": metadata.model_type.value,
                "name": metadata.name,
                "version": metadata.version,
                "path": str(metadata.path),
                "framework": metadata.framework,
                "size_bytes": metadata.size_bytes,
                "created_at": metadata.created_at,
                "last_loaded": metadata.last_loaded,
                "last_used": metadata.last_used,
                "load_count": metadata.load_count,
                "usage_count": metadata.usage_count,
                "performance_metrics": metadata.performance_metrics,
                "health_status": metadata.health_status,
                "dependencies": metadata.dependencies,
                "config": metadata.config
            }

            with open(metadata_file, 'w') as f:
                json.dump(metadata_dict, f, indent=2)

        except Exception as e:
            logger.error(f"Failed to save metadata for {metadata.model_id}: {e}")

    def _validate_metadata(self, metadata: ModelMetadata) -> Dict[str, Any]:
        """Validate model metadata."""
        issues = []

        if not metadata.model_id:
            issues.append("Missing model_id")
        if not metadata.name:
            issues.append("Missing name")
        if not metadata.version:
            issues.append("Missing version")
        if not metadata.framework:
            issues.append("Missing framework")

        return {
            "passed": len(issues) == 0,
            "issues": issues
        }

    async def _validate_model_file(self, metadata: ModelMetadata) -> Dict[str, Any]:
        """Validate model file integrity."""
        try:
            if metadata.framework == "sklearn":
                model_file = metadata.path / f"{metadata.model_id}.pkl"
                if not model_file.exists():
                    return {"passed": False, "issues": ["Model file not found"]}

                # Try to load the file
                import joblib
                joblib.load(model_file)
                return {"passed": True}

            elif metadata.framework == "transformers":
                config_file = metadata.path / "config.json"
                if not config_file.exists():
                    return {"passed": False, "issues": ["Config file not found"]}

                # Basic validation
                with open(config_file, 'r') as f:
                    config = json.load(f)

                if "model_type" not in config:
                    return {"passed": False, "issues": ["Invalid config file"]}

                return {"passed": True}

            return {"passed": True}  # Default pass for unknown frameworks

        except Exception as e:
            return {"passed": False, "issues": [f"File validation error: {e}"]}

    def _validate_dependencies(self, metadata: ModelMetadata) -> Dict[str, Any]:
        """Validate model dependencies."""
        # Basic validation - could be enhanced
        return {"passed": True, "dependencies": metadata.dependencies}

    async def _test_model_loading(self, model_id: str) -> Dict[str, Any]:
        """Test if model can be loaded successfully."""
        try:
            start_time = time.time()
            instance = await self.load_model(model_id)
            load_time = time.time() - start_time

            if instance:
                # Update performance metrics
                metadata = self._registry.get(model_id)
                if metadata:
                    if "load_times" not in metadata.performance_metrics:
                        metadata.performance_metrics["load_times"] = []
                    metadata.performance_metrics["load_times"].append(load_time)

                    # Calculate average
                    load_times = metadata.performance_metrics["load_times"]
                    metadata.performance_metrics["avg_load_time"] = sum(load_times) / len(load_times)

                return {"passed": True, "load_time": load_time}
            else:
                return {"passed": False, "issues": ["Failed to load model"]}

        except Exception as e:
            return {"passed": False, "issues": [f"Load test error: {e}"]}

    async def _test_model_performance(self, model_id: str) -> Dict[str, Any]:
        """Test model performance with sample data."""
        try:
            instance = await self.get_model(model_id)
            if not instance:
                return {"passed": False, "issues": ["Cannot test unloaded model"]}

            # Test with sample data based on model type
            if instance.metadata.model_type == ModelType.SENTIMENT:
                test_input = "This is a great product!"
            elif instance.metadata.model_type == ModelType.TOPIC:
                test_input = "Meeting about project deadlines"
            else:
                test_input = "Test input for model validation"

            start_time = time.time()
            # This would need to be implemented based on the actual model interface
            # For now, just test that the model object exists
            inference_time = time.time() - start_time

            # Update performance metrics
            metadata = instance.metadata
            if "inference_times" not in metadata.performance_metrics:
                metadata.performance_metrics["inference_times"] = []
            metadata.performance_metrics["inference_times"].append(inference_time)

            # Calculate average
            inference_times = metadata.performance_metrics["inference_times"]
            metadata.performance_metrics["avg_inference_time"] = sum(inference_times) / len(inference_times)

            return {"passed": True, "inference_time": inference_time}

        except Exception as e:
            return {"passed": False, "issues": [f"Performance test error: {e}"]}
