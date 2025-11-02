from pydantic import BaseModel, Field
from typing import Dict, Optional

class WeeklyGrowth(BaseModel):
    """Model representing weekly growth statistics."""
    emails: int
    percentage: float

class ConsolidatedDashboardStats(BaseModel):
    """Comprehensive dashboard statistics model that consolidates both modular and legacy implementations."""

    # Core email statistics
    total_emails: int = Field(..., description="Total number of emails in the system.", example=1234)

    # Category-related statistics
    categorized_emails: Optional[Dict[str, int]] = Field(None, description="Breakdown of emails by category.", example={"Work": 100, "Personal": 200})
    categories: Optional[int] = Field(None, description="Total number of categories.", example=10)

    # Email processing statistics
    unread_emails: Optional[int] = Field(None, description="Number of unread emails.", example=50)
    auto_labeled: Optional[int] = Field(None, description="Number of emails that have been automatically labeled.", example=500)

    # Time and productivity metrics
    time_saved: Optional[str] = Field(None, description="Estimated time saved from auto-labeling (in Xh Ym format).", example="16h 40m")

    # Growth and trend analysis
    weekly_growth: Optional[WeeklyGrowth] = Field(None, description="Weekly growth in email volume.")

    # Performance monitoring
    performance_metrics: Optional[Dict[str, float]] = Field(None, description="Performance metrics for various operations.", example={"get_emails": 0.15, "create_email": 0.3})

    class Config:
        # Allow both field names and aliases during validation
        allow_population_by_field_name = True
        validate_assignment = True

# Keep the original DashboardStats for backward compatibility
class DashboardStats(BaseModel):
    """Legacy modular dashboard stats - kept for backward compatibility."""
    total_emails: int
    categorized_emails: Dict[str, int]
    unread_emails: int
    performance_metrics: Dict[str, float]
    time_saved: str = "0h 0m"  # Time saved from auto-labeling (Xh Ym format)
