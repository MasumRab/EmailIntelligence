from pydantic import BaseModel


class WeeklyGrowth(BaseModel):
    """Model representing weekly growth statistics."""

    emails: int
    percentage: float


class ConsolidatedDashboardStats(BaseModel):
    """Comprehensive dashboard statistics model that consolidates both modular and legacy implementations."""

    # Core email statistics
    total_emails: int

    # Category-related statistics
    categorized_emails: dict[str, int] | None = None  # From modular implementation
    categories: int | None = None  # From legacy implementation

    # Email processing statistics
    unread_emails: int | None = None  # From modular implementation
    auto_labeled: int | None = None  # From legacy implementation

    # Time and productivity metrics
    time_saved: str | None = None  # From legacy implementation

    # Growth and trend analysis
    weekly_growth: WeeklyGrowth | None = None  # From legacy implementation

    # Performance monitoring
    performance_metrics: dict[str, float] | None = None  # From modular implementation

    class Config:
        # Allow both field names and aliases during validation
        allow_population_by_field_name = True
        validate_assignment = True


# Keep the original DashboardStats for backward compatibility
class DashboardStats(BaseModel):
    """Legacy modular dashboard stats - kept for backward compatibility."""

    total_emails: int
    categorized_emails: dict[str, int]
    unread_emails: int
    performance_metrics: dict[str, float]
    time_saved: str = "0h 0m"  # Time saved from auto-labeling (Xh Ym format)
