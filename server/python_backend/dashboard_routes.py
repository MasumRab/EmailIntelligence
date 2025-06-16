from fastapi import APIRouter, HTTPException, Depends, Request
import psycopg2
import json
import logging

from .database import DatabaseManager, get_db
from .performance_monitor import PerformanceMonitor
from .models import DashboardStats # Changed from .main.DashboardStatsResponse to .models.DashboardStats

logger = logging.getLogger(__name__)
router = APIRouter()
performance_monitor = PerformanceMonitor() # Initialize performance monitor

@router.get("/api/dashboard/stats", response_model=DashboardStats) # Changed to DashboardStats
@performance_monitor.track
async def get_dashboard_stats(request: Request, db: DatabaseManager = Depends(get_db)):
    """Get comprehensive dashboard statistics"""
    try:
        stats_dict = await db.get_dashboard_stats() # db.get_dashboard_stats returns a dict
        # Ensure that the keys in stats_dict match the fields (or aliases) in models.DashboardStats
        # For example, models.DashboardStats might expect 'total_emails' not 'totalEmails' if aliases are used.
        # The current db.get_dashboard_stats() returns keys like 'totalEmails'.
        # The models.DashboardStats uses Field(alias="total_emails"). Pydantic should handle this by default
        # when `validate_by_name = True` (formerly `allow_population_by_field_name=True`) is set in Config.
        # The models.DashboardStats has `validate_by_name = True` so it should work.
        return DashboardStats(**stats_dict) # Ensure it returns DashboardStats
    except psycopg2.Error as db_err:
        logger.error(
            json.dumps({
                "message": "Database operation failed",
                "endpoint": str(request.url),
                "error_type": type(db_err).__name__,
                "error_detail": str(db_err),
                "pgcode": db_err.pgcode if hasattr(db_err, 'pgcode') else None,
            })
        )
        raise HTTPException(status_code=503, detail="Database service unavailable.")
    except Exception as e:
        logger.error(
            json.dumps({
                "message": "Unhandled error in get_dashboard_stats",
                "endpoint": str(request.url),
                "error_type": type(e).__name__,
                "error_detail": str(e),
            })
        )
        raise HTTPException(status_code=500, detail="Failed to fetch dashboard stats")

@router.get("/api/performance/overview")
async def get_performance_overview(request: Request):
    """Get real-time performance overview"""
    try:
        overview = await performance_monitor.get_real_time_dashboard()
        return overview
    except Exception as e:
        logger.error(
            json.dumps({
                "message": "Unhandled error in get_performance_overview",
                "endpoint": str(request.url),
                "error_type": type(e).__name__,
                "error_detail": str(e),
            })
        )
        raise HTTPException(status_code=500, detail="Failed to fetch performance data")
