import json
import logging
import aiosqlite
import sqlite3

from fastapi import APIRouter, Depends, HTTPException, Request

from backend.python_nlp.smart_filters import EmailFilter, SmartFilterManager

from .database import DatabaseManager, get_db
from .models import FilterRequest
from .performance_monitor import PerformanceMonitor, log_performance

logger = logging.getLogger(__name__)
router = APIRouter()
filter_manager = SmartFilterManager()
performance_monitor = PerformanceMonitor()


@router.get("/api/filters")
@log_performance
async def get_filters(request: Request):
    """Get all active email filters"""
    try:
        filters = filter_manager.get_active_filters_sorted()
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


@router.post("/api/filters", response_model=EmailFilter)
@log_performance
async def create_filter(request: Request, filter_request_model: FilterRequest):
    """Create new email filter"""
    try:
        description = filter_request_model.description or ""
        new_filter_object = filter_manager.add_custom_filter(
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


@router.post("/api/filters/generate-intelligent")
@log_performance
async def generate_intelligent_filters(request: Request, db: DatabaseManager = Depends(get_db)):
    """Generate intelligent filters based on email patterns."""
    try:
        emails = await db.get_recent_emails(limit=1000)
        created_filters = filter_manager.create_intelligent_filters(emails)
        return {"created_filters": len(created_filters), "filters": created_filters}
    except aiosqlite.Error as db_err:
        log_data = {
            "message": "DB operation failed during intelligent filter generation",
            "endpoint": str(request.url),
            "error_type": type(db_err).__name__,
            "error_detail": str(db_err),
        }
        logger.error(json.dumps(log_data))
        raise HTTPException(status_code=503, detail="Database service unavailable.")
    except (ValueError, RuntimeError, OSError) as e:
        log_data = {
            "message": "Unhandled error in generate_intelligent_filters",
            "endpoint": str(request.url),
            "error_type": type(e).__name__,
            "error_detail": str(e),
        }
        logger.error(json.dumps(log_data))
        raise HTTPException(status_code=500, detail="Failed to generate filters")


@router.post("/api/filters/prune")
@log_performance
async def prune_filters(request: Request):
    """Prune ineffective filters"""
    try:
        results = filter_manager.prune_ineffective_filters()
        return results
    except (sqlite3.Error, ValueError, TypeError, RuntimeError) as e:
        log_data = {
            "message": "Unhandled error in prune_filters",
            "endpoint": str(request.url),
            "error_type": type(e).__name__,
            "error_detail": str(e),
        }
        logger.error(json.dumps(log_data))
        raise HTTPException(status_code=500, detail="Failed to prune filters")
