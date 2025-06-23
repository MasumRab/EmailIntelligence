import json
import logging
import sqlite3 # Added for SQLite error handling

# import psycopg2 # Removed
from fastapi import APIRouter, Depends, HTTPException, Request

from .database import DatabaseManager, get_db
from .models import DashboardStats
from .performance_monitor import PerformanceMonitor

logger = logging.getLogger(__name__)
router = APIRouter()
performance_monitor = PerformanceMonitor()  # Initialize performance monitor


@router.get("/api/dashboard/stats", response_model=DashboardStats)  # Changed to DashboardStats
@performance_monitor.track
async def get_dashboard_stats(request: Request, db: DatabaseManager = Depends(get_db)):
    """Get comprehensive dashboard statistics"""
    try:
        stats_dict = (
            await db.get_dashboard_stats()
        )  # db.get_dashboard_stats returns a dict
        try:
            # Ensure that the keys in stats_dict match the fields (or aliases) in models.DashboardStats
            # Ensure that the keys in stats_dict match the fields (or aliases)
            # in models.DashboardStats. Pydantic's `validate_by_name = True` (formerly
            # `allow_population_by_field_name=True`) in model config handles this.
            return DashboardStats(**stats_dict)
        except Exception as e_outer:
            logger.error(f"Outer exception during get_dashboard_stats Pydantic validation: {type(e_outer)} - {repr(e_outer)}")
            if hasattr(e_outer, 'errors'): # For pydantic.ValidationError
                logger.error(f"Pydantic errors: {e_outer.errors()}")
            raise # Re-raise for FastAPI to handle
    except sqlite3.Error as db_err: # Changed to sqlite3.Error
        log_data = {
            "message": "Database operation failed",
            "endpoint": str(request.url),
            "error_type": type(db_err).__name__,
            "error_detail": str(db_err),
            # "pgcode": db_err.pgcode if hasattr(db_err, "pgcode") else None, # Removed pgcode
        }
        logger.error(json.dumps(log_data))
        raise HTTPException(status_code=503, detail="Database service unavailable.")
    except Exception as e:
        log_data = {
            "message": "Unhandled error in get_dashboard_stats",
                    "endpoint": str(request.url),
                    "error_type": type(e).__name__,
                    "error_detail": str(e),
                }
        logger.error(json.dumps(log_data)) # Added logger call
        raise HTTPException(status_code=500, detail="Failed to fetch dashboard stats")


@router.get("/api/performance/overview")
async def get_performance_overview(request: Request):
    """Get real-time performance overview"""
    try:
        overview = await performance_monitor.get_real_time_dashboard()
        return overview
    except Exception as e:
        log_data = {
            "message": "Unhandled error in get_performance_overview",
                    "endpoint": str(request.url),
                    "error_type": type(e).__name__,
                    "error_detail": str(e),
                }
        logger.error(json.dumps(log_data)) # Added logger call
        raise HTTPException(status_code=500, detail="Failed to fetch performance data")
