"""
API Routes for Performance Monitoring.

This module provides FastAPI routes for monitoring system performance,
including metrics, system stats, and error rates.
"""

import logging
from typing import Dict, List

from fastapi import APIRouter, HTTPException

from .performance_monitor import performance_monitor

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/performance", tags=["Performance Monitoring"])


@router.get("/metrics")
async def get_performance_metrics(minutes: int = 5, source_filter: str = None):
    """Get recent performance metrics."""
    try:
        metrics = performance_monitor.get_recent_metrics(minutes, source_filter)
        return [
            {
                "timestamp": metric.timestamp,
                "value": metric.value,
                "unit": getattr(metric, 'unit', ''),
                "source": getattr(metric, 'source', '')
            }
            for metric in metrics
        ]
    except Exception as e:
        logger.error(f"Error getting performance metrics: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get performance metrics")


@router.get("/system-stats")
async def get_system_stats():
    """Get current system statistics."""
    try:
        return performance_monitor.get_system_stats()
    except Exception as e:
        logger.error(f"Error getting system stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get system stats")


@router.get("/error-rate")
async def get_error_rate(minutes: int = 5):
    """Get the error rate in the last specified minutes."""
    try:
        return performance_monitor.get_error_rate(minutes)
    except Exception as e:
        logger.error(f"Error getting error rate: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get error rate")