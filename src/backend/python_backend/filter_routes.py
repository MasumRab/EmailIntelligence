"""
DEPRECATED: This module is part of the deprecated `backend` package.
It will be removed in a future release.
"""

import logging

from fastapi import APIRouter, Depends, HTTPException, Request

from backend.python_nlp.smart_filters import EmailFilter, SmartFilterManager
from src.core.auth import get_current_active_user

from .database import DatabaseManager, get_db
from .models import FilterRequest
from .performance_monitor import PerformanceMonitor, log_performance

logger = logging.getLogger(__name__)
router = APIRouter()
filter_manager = SmartFilterManager()
performance_monitor = PerformanceMonitor()


@router.get("/api/filters")
@log_performance
async def get_filters(
    request: Request, current_user: str = Depends(get_current_active_user)
):
    """Get all active email filters

    Requires authentication.
    """
    try:
        filters = filter_manager.get_active_filters_sorted()
        return {"filters": filters}
    except Exception as e:
        logger.error(f"Error retrieving filters: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve filters")


@router.post("/api/filters", response_model=EmailFilter)
@log_performance
async def create_filter(
    request: Request,
    filter_request_model: FilterRequest,
    current_user: str = Depends(get_current_active_user),
):
    """Create new email filter

    Requires authentication.
    """
    try:
        description = filter_request_model.description or ""
        new_filter_object = filter_manager.add_custom_filter(
            filter_request_model.criteria, filter_request_model.action, description
        )
        return new_filter_object
    except Exception as e:
        logger.error(f"Error creating filter: {e}")
        raise HTTPException(status_code=500, detail="Failed to create filter")


@router.post("/api/filters/generate-intelligent")
@log_performance
async def generate_intelligent_filters(
    request: Request,
    current_user: str = Depends(get_current_active_user),
    db: DatabaseManager = Depends(get_db),
):
    """Generate intelligent filters based on email patterns.

    Requires authentication.
    """
    try:
        emails = await db.get_recent_emails(limit=1000)
        created_filters = filter_manager.create_intelligent_filters(emails)
        return {"filters_created": len(created_filters), "filters": created_filters}
    except Exception as e:
        logger.error(f"Error generating intelligent filters: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to generate intelligent filters"
        )


@router.post("/api/filters/prune")
@log_performance
async def prune_filters(
    request: Request, current_user: str = Depends(get_current_active_user)
):
    """Prune ineffective filters

    Requires authentication.
    """
    try:
        results = filter_manager.prune_ineffective_filters()
        return results
    except Exception as e:
        logger.error(f"Error pruning filters: {e}")
        raise HTTPException(status_code=500, detail="Failed to prune filters")
