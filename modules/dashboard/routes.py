import logging
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from src.core.data_source import DataSource
from src.core.factory import get_data_source
from .models import DashboardStats
from collections import defaultdict

logger = logging.getLogger(__name__)
router = APIRouter()

# Use absolute path for performance log file
LOG_FILE = Path(__file__).resolve().parent.parent.parent.parent / "performance_metrics_log.jsonl"

@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(db: DataSource = Depends(get_data_source)):
    """
    Retrieve dashboard statistics.
    """
    try:
        # Email statistics
        # TODO: Consider optimizing by using database aggregation queries instead of fetching all emails
        emails = await db.get_all_emails(limit=10000)  # Assuming a large limit to get all emails
        total_emails = len(emails)
        unread_emails = sum(1 for email in emails if not email.get('is_read'))

        categorized_emails = defaultdict(int)
        for email in emails:
            category = email.get('category', 'Uncategorized')
            categorized_emails[category] += 1

        # Performance metrics
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
        }

        return DashboardStats(
            total_emails=total_emails,
            categorized_emails=dict(categorized_emails),
            unread_emails=unread_emails,
            performance_metrics=avg_performance_metrics,
        )
    except Exception as e:
        logger.error(f"Error fetching dashboard stats: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error fetching dashboard stats.")
