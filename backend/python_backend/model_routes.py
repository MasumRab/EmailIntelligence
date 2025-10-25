"""
API routes for managing AI models.
"""

import logging
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException

from .dependencies import get_model_manager
from .model_manager import ModelManager

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/api/models", response_model=List[Dict[str, Any]])
async def list_models(
    model_manager: ModelManager = Depends(get_model_manager),
):
    """Lists all discovered models and their current status."""
    return model_manager.list_models()


@router.post("/api/models/{model_name}/load", response_model=dict)
async def load_model(
    model_name: str,
    model_manager: ModelManager = Depends(get_model_manager),
):
    """Loads a specific model into memory."""
    try:
        model_manager.load_model(model_name)
        return {"message": f"Model '{model_name}' loaded successfully."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to load model '{model_name}': {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred while loading model '{model_name}'.",
        )


@router.post("/api/models/{model_name}/unload", response_model=dict)
async def unload_model(
    model_name: str,
    model_manager: ModelManager = Depends(get_model_manager),
):
    """Unloads a specific model from memory."""
    try:
        model_manager.unload_model(model_name)
        return {"message": f"Model '{model_name}' unloaded successfully."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to unload model '{model_name}': {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred while unloading model '{model_name}'.",
        )
