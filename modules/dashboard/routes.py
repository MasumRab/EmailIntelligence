"""
Dashboard API Routes for the modular architecture.

This module defines the API routes for the dashboard endpoints,
including statistics and metrics for the Email Intelligence platform.
"""

import logging
from datetime import datetime
from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException

from src.core.models import DashboardStats, WeeklyGrowth
from src.core.auth import get_current_active_user
from src.core.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/stats", response_model=Dict[str, Any])
async def get_dashboard_stats(
    current_user: str = Depends(get_current_active_user),
    db = Depends(get_db)
):
    """
    Retrieve dashboard statistics including total emails, auto-labeled count,
    category count, time saved, and weekly growth metrics.
    
    Returns:
        Dict[str, Any]: A dictionary containing dashboard statistics
    """
    try:
        # Get total emails count
        total_emails = len(await db.get_all_emails())
        
        # Get auto-labeled emails count (emails with categories)
        all_emails = await db.get_all_emails()
        auto_labeled = sum(1 for email in all_emails if email.get("category_id") is not None)
        
        # Get categories count
        categories = await db.get_all_categories()
        categories_count = len(categories)
        
        # Calculate time saved (example calculation - would need actual implementation)
        # Assuming 2 minutes saved per auto-labeled email
        time_saved_minutes = auto_labeled * 2
        time_saved_hours = time_saved_minutes // 60
        time_saved_remaining_minutes = time_saved_minutes % 60
        time_saved = f"{time_saved_hours}h {time_saved_remaining_minutes}m"
        
        # Calculate weekly growth (example implementation)
        # For now, we'll use a placeholder implementation
        weekly_growth = WeeklyGrowth(
            emails=0,
            percentage=0.0
        )
        
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
        logger.error(f"Failed to fetch dashboard stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch dashboard stats: {str(e)}")