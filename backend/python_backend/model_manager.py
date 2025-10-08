"""
Model Manager System for Email Intelligence Platform

Implements a sophisticated model management system that can dynamically
load, unload, and switch between multiple AI models based on workflow requirements.
Each model has its own performance metrics, memory requirements, and loading status.
"""
import os
import time
import threading
from typing import Dict, Optional, Any, List
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class ModelStatus(Enum):
    """Status of a model in the system"""
    LOADING = "loading"
    LOADED = "loaded"
    UNLOADED = "unloaded"
    ERROR = "error"


@dataclass
class ModelInfo:
    """Information about a model in the system"""
    name: str
    path: str
    size_mb: float
    status: ModelStatus
    load_time: Optional[float] = None
    performance_metrics: Dict[str, Any] = None
    last_used: Optional[float] = None


class ModelManager:
    """Manages loading, unloading, and tracking of AI models"""
    
    def __init__(self):
        self._models: Dict[str, ModelInfo] = {}
        self._loaded_models: Dict[str, Any] = {}  # Actual model instances
        self._lock = threading.Lock()
        
        # Define available models
        self._available_models = {
            "sentiment": {
                "path": "backend/python_nlp/sentiment_model.pkl",
                "size_mb": 15.2
            },
            "topic": {
                "path": "backend/python_nlp/topic_model.pkl", 
                "size_mb": 22.1
            },
            "intent": {
                "path": "backend/python_nlp/intent_model.pkl",
                "size_mb": 18.7
            },
            "urgency": {
                "path": "backend/python_nlp/urgency_model.pkl",
                "size_mb": 12.5
            }
        }
        
    def register_model(self, name: str, path: str, size_mb: float) -> bool:
        """Register a new model with the manager"""
        with self._lock:
            if name in self._models:
                logger.warning(f"Model {name} already registered")
                return False
                
            self._models[name] = ModelInfo(
                name=name,
                path=path,
                size_mb=size_mb,
                status=ModelStatus.UNLOADED
            )
            return True
            
    def load_model(self, name: str) -> bool:
        """Load a model into memory"""
        with self._lock:
            if name not in self._models:
                logger.error(f"Model {name} not registered")
                return False
                
            model_info = self._models[name]
            if model_info.status == ModelStatus.LOADING:
                logger.info(f"Model {name} is already loading")
                return False  # Or wait if we want to block
                
            if model_info.status == ModelStatus.LOADED:
                logger.info(f"Model {name} is already loaded")
                return True
                
            # Mark as loading
            model_info.status = ModelStatus.LOADING
            start_time = time.time()
            
            try:
                # Simulate model loading (replace with actual model loading code)
                # For this example, we'll just store the path as the "model"
                self._loaded_models[name] = model_info.path
                model_info.status = ModelStatus.LOADED
                model_info.load_time = time.time() - start_time
                model_info.last_used = time.time()
                
                logger.info(f"Model {name} loaded successfully in {model_info.load_time:.2f}s")
                return True
            except Exception as e:
                logger.error(f"Failed to load model {name}: {str(e)}")
                model_info.status = ModelStatus.ERROR
                return False
    
    def unload_model(self, name: str) -> bool:
        """Unload a model from memory"""
        with self._lock:
            if name not in self._models:
                logger.error(f"Model {name} not registered")
                return False
                
            if name not in self._loaded_models:
                logger.info(f"Model {name} is not loaded")
                self._models[name].status = ModelStatus.UNLOADED
                return True
                
            try:
                # Remove from loaded models
                del self._loaded_models[name]
                self._models[name].status = ModelStatus.UNLOADED
                logger.info(f"Model {name} unloaded successfully")
                return True
            except Exception as e:
                logger.error(f"Failed to unload model {name}: {str(e)}")
                return False
                
    def get_model(self, name: str) -> Optional[Any]:
        """Get a loaded model instance"""
        with self._lock:
            if name not in self._loaded_models:
                logger.debug(f"Model {name} not loaded in memory")
                return None
            self._models[name].last_used = time.time()
            return self._loaded_models[name]
            
    def get_model_info(self, name: str) -> Optional[ModelInfo]:
        """Get information about a model"""
        with self._lock:
            return self._models.get(name)
            
    def get_all_models(self) -> List[ModelInfo]:
        """Get information about all registered models"""
        with self._lock:
            return list(self._models.values())
            
    def load_available_models(self):
        """Load all available models defined in _available_models"""
        for name, info in self._available_models.items():
            self.register_model(name, info["path"], info["size_mb"])
            self.load_model(name)


# Global model manager instance
model_manager = ModelManager()


def get_model_manager() -> ModelManager:
    """Get the global model manager instance"""
    return model_manager