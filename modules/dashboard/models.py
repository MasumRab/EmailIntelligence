from pydantic import BaseModel
from typing import Dict

class DashboardStats(BaseModel):
    total_emails: int
    categorized_emails: Dict[str, int]
    unread_emails: int
    performance_metrics: Dict[str, float]
