"""
Model Manager for the Email Intelligence Platform

This module provides a centralized system for discovering, loading, unloading,
and managing AI models. It uses a metadata-driven approach, discovering models
from JSON configuration files.
"""

import importlib
import json
import logging
import os
import time
from enum import Enum
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


class ModelStatus(Enum):
    """Enumeration for the status of a model."""
    LOADING = "loading"
    LOADED = "loaded"
    UNLOADED = "unloaded"
    ERROR = "error"


@dataclass
class ModelInfo:
    """Dataclass to hold all information about a model."""
    name: str
    path: str
    size_mb: float
    status: ModelStatus
    module: str
    class_name: str
    load_time: Optional[float] = None
    performance_metrics: Dict[str, Any] = None
    last_used: Optional[float] = None


class ModelManager:
    """
    Manages the lifecycle of AI models through a metadata-driven discovery process.
    """

    def __init__(self, model_directory: str = "models/"):
        self.model_directory = model_directory
        self._models: Dict[str, Any] = {}  # Registry for loaded model instances
        self._model_metadata: Dict[str, ModelInfo] = {}  # Registry for model metadata

    def discover_models(self):
        """
        Discovers models by scanning for JSON configuration files in the model directory.
        """
        logger.info(f"Discovering models from: {self.model_directory}")
        self._model_metadata = {}
        if not os.path.exists(self.model_directory):
            logger.warning(f"Model directory '{self.model_directory}' not found. Creating it.")
            os.makedirs(self.model_directory, exist_ok=True)
            return

        for filename in os.listdir(self.model_directory):
            if filename.endswith(".json"):
                file_path = os.path.join(self.model_directory, filename)
                try:
                    with open(file_path, "r") as f:
                        meta = json.load(f)
                        model_name = meta.get("name")
                        if not all(k in meta for k in ["name", "path", "size_mb", "module", "class"]):
                            logger.warning(f"Skipping config '{filename}': missing required fields.")
                            continue

                        info = ModelInfo(
                            name=model_name,
                            path=meta["path"],
                            size_mb=float(meta["size_mb"]),
                            status=ModelStatus.UNLOADED,
                            module=meta["module"],
                            class_name=meta["class"]
                        )
                        self._model_metadata[model_name] = info
                        logger.info(f"Discovered model '{model_name}' from {filename}")

                except (json.JSONDecodeError, ValueError) as e:
                    logger.error(f"Failed to parse or validate model config '{filename}': {e}")
                except Exception as e:
                    logger.error(f"Failed to process model config '{filename}': {e}")

        logger.info(f"Discovered {len(self._model_metadata)} models in total.")

    def load_model(self, model_name: str) -> bool:
        """
        Loads a model into memory using its discovered metadata.
        """
        if model_name not in self._model_metadata:
            logger.error(f"Model '{model_name}' not found.")
            return False

        info = self._model_metadata[model_name]
        if info.status == ModelStatus.LOADED:
            logger.info(f"Model '{model_name}' is already loaded.")
            return True
        if info.status == ModelStatus.LOADING:
            logger.info(f"Model '{model_name}' is currently loading.")
            return False # Or implement a lock/wait mechanism

        logger.info(f"Loading model '{model_name}' from module '{info.module}'...")
        info.status = ModelStatus.LOADING
        start_time = time.time()

        try:
            module = importlib.import_module(info.module)
            model_class = getattr(module, info.class_name)
            self._models[model_name] = model_class() # Instantiate the model

            info.status = ModelStatus.LOADED
            info.load_time = time.time() - start_time
            info.last_used = time.time()
            logger.info(f"Model '{model_name}' loaded successfully in {info.load_time:.2f}s.")
            return True
        except (ImportError, AttributeError) as e:
            logger.error(f"Failed to import or find class for model '{model_name}': {e}")
            info.status = ModelStatus.ERROR
            return False
        except Exception as e:
            logger.error(f"An unexpected error occurred while loading model '{model_name}': {e}", exc_info=True)
            info.status = ModelStatus.ERROR
            return False

    def unload_model(self, model_name: str) -> bool:
        """
        Unloads a model from memory.
        """
        if model_name not in self._model_metadata:
            logger.error(f"Model '{model_name}' not found.")
            return False

        info = self._model_metadata[model_name]
        if model_name not in self._models:
            logger.warning(f"Model '{model_name}' is not currently loaded.")
            info.status = ModelStatus.UNLOADED
            return True

        logger.info(f"Unloading model: {model_name}")
        try:
            # In a real scenario, this might involve calling a cleanup method on the model instance
            del self._models[model_name]
            info.status = ModelStatus.UNLOADED
            info.load_time = None
            logger.info(f"Model '{model_name}' unloaded successfully.")
            return True
        except Exception as e:
            logger.error(f"An error occurred while unloading model '{model_name}': {e}")
            return False

    def get_model(self, model_name: str) -> Optional[Any]:
        """
        Loads a model if it's not already loaded, and returns the instance.
        """
        if model_name not in self._model_metadata:
            logger.error(f"Model '{model_name}' not found in metadata.")
            return None

        info = self._model_metadata[model_name]
        if info.status != ModelStatus.LOADED:
            if not self.load_model(model_name):
                return None # Loading failed

        info.last_used = time.time()
        return self._models.get(model_name)

    def get_all_models(self) -> List[ModelInfo]:
        """
        Returns a list of all discovered models and their current status.
        """
        return list(self._model_metadata.values())

# Create a global singleton instance of the model manager
model_manager = ModelManager()

def get_model_manager() -> ModelManager:
    """Dependency injector function to get the global model manager instance."""
    return model_manager
