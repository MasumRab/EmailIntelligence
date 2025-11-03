"""
Dashboard API Routes.

This module defines the API routes for the dashboard endpoints,
including statistics and metrics for the Email Intelligence platform.
"""

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any

from src.core.models import DashboardStats, WeeklyGrowth
from src.core.data_source import DataSource
from src.core.factory import get_data_source
from src.core.auth import get_current_active_user

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/stats", response_model=Dict[str, Any])
async def get_dashboard_stats(
    db: DataSource = Depends(get_data_source),
    current_user: str = Depends(get_current_active_user)
):
    """
    Retrieve dashboard statistics including total emails, auto-labeled count,
    category count, time saved, and weekly growth metrics.
    
    Returns:
        DashboardStats: A model containing various dashboard statistics
    """
    try:
        # Get total emails count
        total_emails = await db.get_total_emails_count()
        
        # Get auto-labeled emails count
        auto_labeled = await db.get_auto_labeled_count()
        
        # Get categories count
        categories_count = await db.get_categories_count()
        
        # Calculate time saved (example calculation - would need actual implementation)
        # Assuming 2 minutes saved per auto-labeled email
        time_saved_minutes = auto_labeled * 2
        time_saved_hours = time_saved_minutes // 60
        time_saved_remaining_minutes = time_saved_minutes % 60
        time_saved = f"{time_saved_hours}h {time_saved_remaining_minutes}m"
        
        # Calculate weekly growth (example implementation)
        weekly_growth = await db.get_weekly_growth()
        
        stats = DashboardStats(
            total_emails=total_emails,
            auto_labeled=auto_labeled,
            categories=categories_count,
            time_saved=time_saved,
            weekly_growth=weekly_growth
        )
        
        return {
            "success": True,
            "data": stats,
            "message": "Dashboard statistics retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch dashboard stats: {str(e)}")