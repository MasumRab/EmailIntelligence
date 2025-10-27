from pydantic import BaseModel
from typing import List, Dict

class DashboardStats(BaseModel):
    total_emails: int
    categorized_emails: int
    uncategorized_emails: int
    unread_emails: int
    emails_per_category: Dict[str, int]
    performance_metrics: Dict[str, float]
