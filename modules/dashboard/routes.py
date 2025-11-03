"""
Dashboard API Routes for the modular architecture.

This module defines the API routes for the dashboard endpoints,
including statistics and metrics for the Email Intelligence platform.
"""

import logging
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from src.core.data.repository import EmailRepository
from src.core.factory import get_email_repository
from src.core.auth import get_current_active_user
from .models import DashboardStats, ConsolidatedDashboardStats, WeeklyGrowth
from collections import defaultdict

logger = logging.getLogger(__name__)

# Use absolute path for performance log file
LOG_FILE = Path(__file__).resolve().parent.parent.parent / "performance_metrics_log.jsonl"

@router.get("/stats", response_model=ConsolidatedDashboardStats)
async def get_dashboard_stats(
    repository: EmailRepository = Depends(get_email_repository),
    current_user: str = Depends(get_current_active_user)
):
    """
    Retrieve consolidated dashboard statistics using efficient server-side aggregations.

    Requires authentication. Returns comprehensive aggregate statistics for the authenticated user,
    consolidating both modular and legacy dashboard features.
    """
    try:
        # Log user access for audit purposes
        logger.info(f"Dashboard stats requested by user: {current_user}")

        # Get efficient server-side aggregations
        aggregates = await repository.get_dashboard_aggregates()
        categorized_emails = await repository.get_category_breakdown(limit=10)

        # Extract values from aggregates
        total_emails = aggregates.get('total_emails', 0)
        unread_emails = aggregates.get('unread_count', 0)
        auto_labeled = aggregates.get('auto_labeled', 0)
        categories_count = aggregates.get('categories_count', 0)
        weekly_growth_data = aggregates.get('weekly_growth')

        # Calculate time_saved (2 minutes per auto-labeled email, matching legacy implementation)
        time_saved_minutes = auto_labeled * 2
        time_saved_hours = time_saved_minutes // 60
        time_saved_remaining_minutes = time_saved_minutes % 60
        time_saved = f"{time_saved_hours}h {time_saved_remaining_minutes}m"

        # Parse weekly growth data
        weekly_growth = None
        if weekly_growth_data:
            weekly_growth = WeeklyGrowth(
                emails=weekly_growth_data.get('emails', 0),
                percentage=weekly_growth_data.get('percentage', 0.0)
            )

        # Performance metrics (keep existing logic for now)
        performance_metrics = defaultdict(lambda: {'total_duration': 0, 'count': 0})
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        log_entry = json.loads(line)
                        op = log_entry.get("operation")
                        duration = log_entry.get("duration_seconds")
                        if op and duration is not None:
                            performance_metrics[op]['total_duration'] += duration
                            performance_metrics[op]['count'] += 1
                    except json.JSONDecodeError:
                        continue
        except FileNotFoundError:
            logger.warning(f"Performance log file not found: {LOG_FILE}")

        avg_performance_metrics = {
            op: data['total_duration'] / data['count']
            for op, data in performance_metrics.items()
            if data['count'] > 0  # Avoid division by zero
        }

        return ConsolidatedDashboardStats(
            total_emails=total_emails,
            categorized_emails=categorized_emails,
            unread_emails=unread_emails,
            auto_labeled=auto_labeled,
            categories=categories_count,
            time_saved=time_saved,
            weekly_growth=weekly_growth,
            performance_metrics=avg_performance_metrics,
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
        logger.error(f"Error fetching dashboard stats for user {current_user}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error fetching dashboard stats.")
