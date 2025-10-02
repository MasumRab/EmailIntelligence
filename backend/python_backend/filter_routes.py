import json
import logging

import psycopg2
from fastapi import APIRouter, Depends, HTTPException, Request

# Corrected import path for SmartFilterManager
from ..python_nlp.smart_filters import (  # Assuming EmailFilter is needed for response model
    EmailFilter,
    SmartFilterManager,
)

from .database import DatabaseManager, get_db
from .models import FilterRequest  # Models are imported from .models
# from .performance_monitor import PerformanceMonitor # Removed

logger = logging.getLogger(__name__)
router = APIRouter()
filter_manager = SmartFilterManager()  # Initialize filter manager
# performance_monitor = PerformanceMonitor() # Removed


@router.get("/api/filters")
async def get_filters(request: Request):
    """
    Retrieves all active smart filters, sorted by priority.

    Args:
        request: The incoming request object.

    Returns:
        A dictionary containing a list of all active filter objects.

    Raises:
        HTTPException: If an unexpected error occurs.
    """
    try:
        filters = filter_manager.get_active_filters_sorted()
        return {"filters": filters}
    except Exception as e:
        log_data = {
            "message": "Unhandled error in get_filters",
            "endpoint": str(request.url),
            "error_type": type(e).__name__,
            "error_detail": str(e),
        }
        logger.error(json.dumps(log_data))
        raise HTTPException(status_code=500, detail="Failed to fetch filters")


@router.post("/api/filters", response_model=EmailFilter)
async def create_filter(request: Request, filter_request_model: FilterRequest):
    """
    Creates a new custom smart filter.

    Args:
        request: The incoming request object.
        filter_request_model: The data for the new filter to be created.

    Returns:
        The newly created filter object.

    Raises:
        HTTPException: If an unexpected error occurs.
    """
    try:
        description = filter_request_model.description or ""

        new_filter_object = filter_manager.add_custom_filter(
            name=filter_request_model.name,
            description=description,
            criteria=filter_request_model.criteria.model_dump(),
            actions=filter_request_model.actions.model_dump(),
            priority=filter_request_model.priority,
        )
        return new_filter_object
    except Exception as e:
        log_data = {
            "message": "Unhandled error in create_filter",
            "endpoint": str(request.url),
            "error_type": type(e).__name__,
            "error_detail": str(e),
        }
        logger.error(json.dumps(log_data))
        raise HTTPException(status_code=500, detail="Failed to create filter")


@router.post("/api/filters/generate-intelligent")
async def generate_intelligent_filters(request: Request, db: DatabaseManager = Depends(get_db)):
    """
    Analyzes recent emails to intelligently generate new smart filters.

    This endpoint scans a batch of recent emails to identify patterns and
    proposes new filters to automate email organization.

    Args:
        request: The incoming request object.
        db: The database manager dependency.

    Returns:
        A dictionary containing the count of created filters and the filter objects.

    Raises:
        HTTPException: If a database error or other unexpected error occurs.
    """
    try:
        emails = await db.get_recent_emails(limit=1000)
        created_filters = await filter_manager.create_intelligent_filters(emails)
        return {"created_filters": len(created_filters), "filters": created_filters}
    except psycopg2.Error as db_err:
        log_data = {
            "message": "DB operation failed during intelligent filter generation",
            "endpoint": str(request.url),
            "error_type": type(db_err).__name__,
            "error_detail": str(db_err),
            "pgcode": db_err.pgcode if hasattr(db_err, "pgcode") else None,
        }
        logger.error(json.dumps(log_data))
        raise HTTPException(status_code=503, detail="Database service unavailable.")
    except Exception as e:
        log_data = {
            "message": "Unhandled error in generate_intelligent_filters",
            "endpoint": str(request.url),
            "error_type": type(e).__name__,
            "error_detail": str(e),
        }
        logger.error(json.dumps(log_data))
        raise HTTPException(status_code=500, detail="Failed to generate filters")


@router.post("/api/filters/prune")
async def prune_filters(request: Request):
    """
    Prunes ineffective or redundant smart filters.

    This endpoint triggers a process to analyze filter performance and remove
    those that are no longer effective.

    Args:
        request: The incoming request object.

    Returns:
        A dictionary with the results of the pruning operation.

    Raises:
        HTTPException: If an unexpected error occurs.
    """
    try:
        results = await filter_manager.prune_ineffective_filters()
        return results
    except Exception as e:
        log_data = {
            "message": "Unhandled error in prune_filters",
            "endpoint": str(request.url),
            "error_type": type(e).__name__,
            "error_detail": str(e),
        }
        logger.error(json.dumps(log_data))
        raise HTTPException(status_code=500, detail="Failed to prune filters")
