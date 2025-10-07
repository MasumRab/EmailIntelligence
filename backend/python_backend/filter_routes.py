import json
import logging

from fastapi import APIRouter, Depends, HTTPException, Request

# Corrected import path for SmartFilterManager
from ..python_nlp.smart_filters import (  # Assuming EmailFilter is needed for response model
    EmailFilter,
    SmartFilterManager,
)
from .database import DatabaseManager, get_db
from .dependencies import get_filter_manager
from .exceptions import AIAnalysisError, DatabaseError
from .models import FilterRequest  # Models are imported from .models
from .performance_monitor import log_performance

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/api/filters")
@log_performance(operation="get_filters")
async def get_filters(
    request: Request, filter_manager: SmartFilterManager = Depends(get_filter_manager)
):
    """Get all active email filters"""
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
        raise AIAnalysisError(detail="Failed to fetch filters")


@router.post("/api/filters", response_model=EmailFilter)
@log_performance(operation="create_filter")
async def create_filter(
    request: Request,
    filter_request_model: FilterRequest,
    filter_manager: SmartFilterManager = Depends(get_filter_manager),
):
    """Create new email filter"""
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
        raise AIAnalysisError(detail="Failed to create filter")


@router.post("/api/filters/generate-intelligent")
@log_performance(operation="generate_intelligent_filters")
async def generate_intelligent_filters(
    request: Request,
    db: DatabaseManager = Depends(get_db),
    filter_manager: SmartFilterManager = Depends(get_filter_manager),
):
    """Generate intelligent filters based on email patterns."""
    try:
        emails = await db.get_recent_emails(limit=1000)

        # Assuming filter_manager.create_intelligent_filters exists and
        # returns a list of filter objects/dicts.
        created_filters = filter_manager.create_intelligent_filters(emails)

        return {"created_filters": len(created_filters), "filters": created_filters}
    except Exception as db_err:
        log_data = {
            "message": "DB operation failed during intelligent filter generation",
            "endpoint": str(request.url),
            "error_type": type(db_err).__name__,
            "error_detail": str(db_err),
            "pgcode": None,
        }
        logger.error(json.dumps(log_data))
        raise DatabaseError(detail="Database service unavailable.")
    except Exception as e:
        log_data = {
            "message": "Unhandled error in generate_intelligent_filters",
            "endpoint": str(request.url),
            "error_type": type(e).__name__,
            "error_detail": str(e),
        }
        logger.error(json.dumps(log_data))
        raise AIAnalysisError(detail="Failed to generate filters")


@router.post("/api/filters/prune")
@log_performance(operation="prune_filters")
async def prune_filters(
    request: Request, filter_manager: SmartFilterManager = Depends(get_filter_manager)
):
    """Prune ineffective filters"""
    try:
        # Assuming filter_manager.prune_ineffective_filters exists
        # This method was not in original smart_filters.py, assuming added.
        results = filter_manager.prune_ineffective_filters()
        return results
    except Exception as e:
        log_data = {
            "message": "Unhandled error in prune_filters",
            "endpoint": str(request.url),
            "error_type": type(e).__name__,
            "error_detail": str(e),
        }
        logger.error(json.dumps(log_data))
        raise AIAnalysisError(detail="Failed to prune filters")