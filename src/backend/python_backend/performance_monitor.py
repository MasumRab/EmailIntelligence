"""
Performance Monitoring Dashboard for Email Intelligence Platform

Implements real-time performance monitoring with visualizations for processing times,
model usage, memory consumption, and error rates.
"""
from typing import Any, Dict, List, Optional
from src.core.performance_monitor import (
    OptimizedPerformanceMonitor,
    PerformanceMetric,
    ProcessingEvent,
    performance_monitor as core_monitor,
    log_performance as core_log_performance,
)

# Alias for compatibility
PerformanceMonitor = OptimizedPerformanceMonitor
log_performance = core_log_performance
performance_monitor = core_monitor

def get_performance_monitor() -> PerformanceMonitor:
    """Get the global performance monitor instance"""
    return performance_monitor
