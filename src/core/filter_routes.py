"""
API Routes for Email Filter Management.

This module provides FastAPI routes for managing email filters,
including creation, listing, intelligent generation, and pruning.
"""

import json
import logging
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, Request

from .auth import get_current_active_user
from .smart_filter_manager import get_smart_filter_manager
from .models import FilterRequest, FilterResponse
from .performance_monitor import log_performance

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/filters", tags=["Filter Management"])


@router.get("/", response_model=Dict[str, Any])
@log_performance
async def get_filters(
    request: Request,
    current_user: str = Depends(get_current_active_user)
):
    """Get all active email filters
    Requires authentication."""
    try:
        filter_manager = get_smart_filter_manager()
        filters = await filter_manager.get_active_filters_sorted()
        return {"filters": filters}
    except (ValueError, KeyError, TypeError, RuntimeError) as e:
        log_data = {
            "message": "Unhandled error in get_filters",
            "endpoint": str(request.url),
            "error_type": type(e).__name__,
            "error_detail": str(e),
        }
        logger.error(json.dumps(log_data))
        raise HTTPException(status_code=500, detail="Failed to fetch filters")


@router.post("/", response_model=FilterResponse)
@log_performance
async def create_filter(
    request: Request,
    filter_request_model: FilterRequest,
    current_user: str = Depends(get_current_active_user)
):
    """Create new email filter
    Requires authentication."""
    try:
        filter_manager = get_smart_filter_manager()
        description = filter_request_model.description or ""
        new_filter_object = await filter_manager.add_custom_filter(
            name=filter_request_model.name,
            description=description,
            criteria=filter_request_model.criteria.model_dump(by_alias=True),
            actions=filter_request_model.actions.model_dump(by_alias=True),
            priority=filter_request_model.priority,
        )
        return new_filter_object
    except (ValueError, KeyError, TypeError, RuntimeError) as e:
        log_data = {
            "message": "Unhandled error in create_filter",
            "endpoint": str(request.url),
            "error_type": type(e).__name__,
            "error_detail": str(e),
        }
        logger.error(json.dumps(log_data))
        raise HTTPException(status_code=500, detail="Failed to create filter")


@router.post("/generate-intelligent", response_model=Dict[str, Any])
@log_performance
async def generate_intelligent_filters(
    request: Request,
    current_user: str = Depends(get_current_active_user)
):
    """Generate intelligent filters based on email patterns.
    Requires authentication."""
    try:
        filter_manager = get_smart_filter_manager()
        # For now, return a placeholder response
        # In a real implementation, we'd fetch sample emails and generate filters
        return {"message": "Intelligent filter generation endpoint ready"}
    except (ValueError, RuntimeError, OSError) as e:
        log_data = {
            "message": "Unhandled error in generate_intelligent_filters",
            "endpoint": str(request.url),
            "error_type": type(e).__name__,
            "error_detail": str(e),
        }
        logger.error(json.dumps(log_data))
        raise HTTPException(status_code=500, detail="Failed to generate filters")


@router.post("/prune", response_model=Dict[str, Any])
@log_performance
async def prune_filters(
    request: Request,
    current_user: str = Depends(get_current_active_user)
):
    """Prune ineffective filters
    Requires authentication."""
    try:
        filter_manager = get_smart_filter_manager()
        results = await filter_manager.prune_ineffective_filters()
        return results
    except (ValueError, TypeError, RuntimeError) as e:
        log_data = {
            "message": "Unhandled error in prune_filters",
            "endpoint": str(request.url),
            "error_type": type(e).__name__,
            "error_detail": str(e),
        }
        logger.error(json.dumps(log_data))
        raise HTTPException(status_code=500, detail="Failed to prune filters")