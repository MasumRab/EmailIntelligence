<<<<<<< HEAD
"""
API routes for managing AI models.
"""

import logging
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException

from src.core.auth import get_current_active_user

from .dependencies import get_model_manager
from .model_manager import ModelManager

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/api/models", response_model=List[Dict[str, Any]])
async def list_models(
    current_user: str = Depends(get_current_active_user),
    model_manager: ModelManager = Depends(get_model_manager),
):
    """Lists all discovered models and their current status.

    Requires authentication.
    """
    return model_manager.list_models()


@router.post("/api/models/{model_name}/load", response_model=dict)
async def load_model(
    model_name: str,
    current_user: str = Depends(get_current_active_user),
    model_manager: ModelManager = Depends(get_model_manager),
):
    """Loads a specific model into memory.

    Requires authentication.
    """
    try:
        model_manager.load_model(model_name)
        return {"message": f"Model '{model_name}' loaded successfully."}
    except Exception as e:
        logger.error(f"Error loading model {model_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to load model '{model_name}'")


@router.post("/api/models/{model_name}/unload", response_model=dict)
async def unload_model(
    model_name: str,
    current_user: str = Depends(get_current_active_user),
    model_manager: ModelManager = Depends(get_model_manager),
):
    """Unloads a specific model from memory.

    Requires authentication.
    """
    try:
        model_manager.unload_model(model_name)
        return {"message": f"Model '{model_name}' unloaded successfully."}
    except Exception as e:
        logger.error(f"Error unloading model {model_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to unload model '{model_name}'")
=======
>>>>>>> 837f0b4c3be0be620537c058dd8dba25d8ac010d
