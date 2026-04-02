"""
Filter API Routes for the modular architecture.

This module defines the API routes for managing email filters.
"""

import json
import logging
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, Request

from src.core.auth import get_current_active_user
from src.core.smart_filter_manager import get_smart_filter_manager
from src.core.models import FilterRequest, FilterResponse
from src.core.performance_monitor import log_performance

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/filters", tags=["filters"])


@router.get("/")
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


@router.post("/generate-intelligent")
@log_performance
async def generate_intelligent_filters(
    request: Request,
    current_user: str = Depends(get_current_active_user)
):
    """Generate intelligent filters based on email patterns.
    Requires authentication."""
    try:
        # We'll need to get some sample emails to analyze
        # For now, return a placeholder response
        filter_manager = get_smart_filter_manager()
        # In a real implementation, we'd fetch sample emails from the database
        # and pass them to the filter manager
        return {"message": "Intelligent filter generation endpoint placeholder"}
    except (ValueError, RuntimeError, OSError) as e:
        log_data = {
            "message": "Unhandled error in generate_intelligent_filters",
            "endpoint": str(request.url),
            "error_type": type(e).__name__,
            "error_detail": str(e),
        }
        logger.error(json.dumps(log_data))
        raise HTTPException(status_code=500, detail="Failed to generate filters")


@router.post("/prune")
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