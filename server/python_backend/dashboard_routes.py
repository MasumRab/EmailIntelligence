import json
import logging
import aiosqlite

from fastapi import APIRouter, Depends, HTTPException, Request

from .database import DatabaseManager, get_db
from .models import DashboardStats
from .performance_monitor import PerformanceMonitor

logger = logging.getLogger(__name__)
router = APIRouter()
performance_monitor = PerformanceMonitor()


@router.get("/api/dashboard/stats", response_model=DashboardStats)
@performance_monitor.track
async def get_dashboard_stats(request: Request, db: DatabaseManager = Depends(get_db)):
    """Get comprehensive dashboard statistics"""
    try:
        stats_dict = await db.get_dashboard_stats()
        return DashboardStats(**stats_dict)
    except aiosqlite.Error as db_err:
        log_data = {
            "message": "Database operation failed",
            "endpoint": str(request.url),
            "error_type": type(db_err).__name__,
            "error_detail": str(db_err),
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
        logger.error(json.dumps(log_data))
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
        logger.error(json.dumps(log_data))
        raise HTTPException(status_code=500, detail="Failed to fetch performance data")