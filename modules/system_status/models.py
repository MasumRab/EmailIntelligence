from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime


class SystemStatus(BaseModel):
    """Model for comprehensive system status information."""

    system_info: Dict[str, Any]
    cpu_usage: float
    memory_usage: float
    memory_total: int
    memory_used: int
    disk_usage: float
    disk_total: int
    disk_used: int
    network_stats: Dict[str, int]
    dashboard_stats: Dict[str, Any]
    gmail_performance: Dict[str, Any]
    timestamp: str
    uptime_seconds: int


class HealthCheck(BaseModel):
    """Model for service health check results."""

    overall_status: str  # "healthy" or "unhealthy"
    service_checks: Dict[str, Dict[str, Any]]
    timestamp: str


class PerformanceMetrics(BaseModel):
    """Model for detailed performance metrics."""

    operation: str
    duration_seconds: float
    timestamp: datetime
    success: bool
    metadata: Optional[Dict[str, Any]] = None
