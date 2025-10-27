from fastapi import APIRouter, Depends
from src.core.database import get_db, DatabaseManager
from .models import DashboardStats

router = APIRouter()

@router.get("/api/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats(db: DatabaseManager = Depends(get_db)):
    """
    Provides dashboard statistics.
    """

    total_emails = len(db.emails_data)

    categorized_emails = sum(1 for email in db.emails_data if email.get("category_id") is not None)

    uncategorized_emails = total_emails - categorized_emails

    unread_emails = sum(1 for email in db.emails_data if email.get("is_unread"))

    emails_per_category = {}

    for category in db.categories_data:
        category_id = category.get("id")
        category_name = category.get("name")
        if category_id is not None and category_name is not None:
            count = sum(1 for email in db.emails_data if email.get("category_id") == category_id)
            emails_per_category[category_name] = count

    performance_metrics = {
        "avg_email_processing_time": 0.5,
        "api_response_time": 0.1
    }

    return DashboardStats(
        total_emails=total_emails,
        categorized_emails=categorized_emails,
        uncategorized_emails=uncategorized_emails,
        unread_emails=unread_emails,
        emails_per_category=emails_per_category,
        performance_metrics=performance_metrics
    )
