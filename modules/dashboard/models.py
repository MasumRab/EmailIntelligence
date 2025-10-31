from pydantic import BaseModel, Field
from typing import Dict, Optional

class WeeklyGrowth(BaseModel):
    """Model representing weekly growth statistics."""
    emails: int
    percentage: float

class ConsolidatedDashboardStats(BaseModel):
    """Comprehensive dashboard statistics model that consolidates both modular and legacy implementations."""

    # Core email statistics
    total_emails: int = Field(alias="totalEmails")

    # Category-related statistics
    categorized_emails: Optional[Dict[str, int]] = None  # From modular implementation
    categories: Optional[int] = None  # From legacy implementation

    # Email processing statistics
    unread_emails: Optional[int] = None  # From modular implementation
    auto_labeled: Optional[int] = Field(default=None, alias="autoLabeled")  # From legacy implementation

    # Time and productivity metrics
    time_saved: Optional[str] = Field(default=None, alias="timeSaved")  # From legacy implementation

    # Growth and trend analysis
    weekly_growth: Optional[WeeklyGrowth] = Field(default=None, alias="weeklyGrowth")  # From legacy implementation

    # Performance monitoring
    performance_metrics: Optional[Dict[str, float]] = None  # From modular implementation

    class Config:
        allow_population_by_field_name = True
        validate_assignment = True

# Keep the original DashboardStats for backward compatibility
class DashboardStats(BaseModel):
    """Legacy modular dashboard stats - kept for backward compatibility."""
    total_emails: int
    categorized_emails: Dict[str, int]
    unread_emails: int
    performance_metrics: Dict[str, float]
