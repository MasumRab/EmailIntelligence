"""
Performance Monitoring wrapper for backward compatibility.
Redirects to src.core.performance_monitor.
"""

from src.core.performance_monitor import (
    PerformanceMetric,
    ProcessingEvent,
    OptimizedPerformanceMonitor,
    performance_monitor,
    log_performance,
    record_metric,
    time_function
)

# Alias for backward compatibility
PerformanceMonitor = OptimizedPerformanceMonitor

__all__ = [
    "PerformanceMetric",
    "ProcessingEvent",
    "PerformanceMonitor",
    "performance_monitor",
    "log_performance",
    "record_metric",
    "time_function"
]
