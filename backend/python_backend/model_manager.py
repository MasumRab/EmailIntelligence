"""
Model Manager for the Email Intelligence Platform

This module provides a centralized system for discovering, loading, unloading,
and managing AI models.
"""

import importlib
import json
import logging
import os
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class ModelManager:
    """
    Manages the lifecycle of AI models.
    """

    def __init__(self, model_directory: str = "models/"):
        self.model_directory = model_directory
        self._models: Dict[str, Any] = {}  # Registry for model instances
        self._model_metadata: Dict[str, Dict[str, Any]] = {}  # Registry for model metadata

    def discover_models(self):
        """
        Discovers models by scanning for JSON configuration files in the model directory.
        """
        logger.info(f"Discovering models from: {self.model_directory}")
        self._model_metadata = {}
        if not os.path.exists(self.model_directory):
            logger.warning(
                f"Model directory '{self.model_directory}' not found. No models will be loaded."
            )
            return

        for filename in os.listdir(self.model_directory):
            if filename.endswith(".json"):
                file_path = os.path.join(self.model_directory, filename)
                try:
                    with open(file_path, "r") as f:
                        meta = json.load(f)
                        model_name = meta.get("name")
                        if not model_name:
                            logger.warning(
                                f"Skipping config file '{filename}' as it's missing a 'name' field."
                            )
                            continue

                        meta["status"] = "unloaded"
                        meta["performance"] = {}
                        self._model_metadata[model_name] = meta
                        logger.info(f"Discovered model '{model_name}' from {filename}")

                except json.JSONDecodeError:
                    logger.error(f"Failed to parse JSON from '{filename}'.")
                except Exception as e:
                    logger.error(f"Failed to process model config '{filename}': {e}")

        logger.info(f"Discovered {len(self._model_metadata)} models in total.")

    def get_model(self, model_name: str) -> Any:
        """
        Loads a model if it's not already loaded, and returns it.
        """
        if model_name not in self._model_metadata:
            raise ValueError(f"Model '{model_name}' not found.")

        if self._model_metadata[model_name].get("status") != "loaded":
            self.load_model(model_name)

        return self._models.get(model_name)

    def load_model(self, model_name: str):
        """
        Loads a model into memory using its metadata.
        """
        if model_name not in self._model_metadata:
            raise ValueError(f"Model '{model_name}' not found.")

        meta = self._model_metadata[model_name]
        module_name = meta.get("module")
        class_name = meta.get("class")

        if not module_name or not class_name:
            raise ValueError(
                f"Model '{model_name}' config is missing 'module' or 'class' information."
            )

        logger.info(f"Loading model '{model_name}' from module '{module_name}'...")
        try:
            module = importlib.import_module(module_name)
            model_class = getattr(module, class_name)
            self._models[model_name] = model_class()
            self._model_metadata[model_name]["status"] = "loaded"
            logger.info(f"Model '{model_name}' loaded successfully.")
        except ImportError:
            logger.error(f"Could not import module '{module_name}' for model '{model_name}'.")
            raise
        except AttributeError:
            logger.error(f"Could not find class '{class_name}' in module '{module_name}'.")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred while loading model '{model_name}': {e}")
            raise

    def unload_model(self, model_name: str):
        """
        Unloads a model from memory.
        """
        if model_name not in self._models:
            logger.warning(f"Model '{model_name}' is not loaded.")
            return

        logger.info(f"Unloading model: {model_name}")
        # In a real scenario, this might involve more complex cleanup.
        del self._models[model_name]
        self._model_metadata[model_name]["status"] = "unloaded"
        logger.info(f"Model '{model_name}' unloaded successfully.")

    def list_models(self) -> List[Dict[str, Any]]:
        """
        Returns a list of all discovered models and their metadata.
        """
        return list(self._model_metadata.values())


# Create a global instance
model_manager = ModelManager()

def get_model_manager() -> ModelManager:
    """Get the global model manager instance"""
    return model_manager
