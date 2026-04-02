from datetime import datetime
from typing import Any

from pydantic import BaseModel


class SystemStatus(BaseModel):
    """Model for comprehensive system status information."""

    system_info: dict[str, Any]
    cpu_usage: float
    memory_usage: float
    memory_total: int
    memory_used: int
    disk_usage: float
    disk_total: int
    disk_used: int
    network_stats: dict[str, int]
    dashboard_stats: dict[str, Any]
    gmail_performance: dict[str, Any]
    timestamp: str
    uptime_seconds: int


class HealthCheck(BaseModel):
    """Model for service health check results."""

    overall_status: str  # "healthy" or "unhealthy"
    service_checks: dict[str, dict[str, Any]]
    timestamp: str


class PerformanceMetrics(BaseModel):
    """Model for detailed performance metrics."""

    operation: str
    duration_seconds: float
    timestamp: datetime
    success: bool
    metadata: dict[str, Any] | None = None
