"""
Performance monitoring module for the Email Intelligence backend.
"""

import time
import logging
from typing import Dict, Any, Callable
from functools import wraps
import asyncio

logger = logging.getLogger(__name__)

class PerformanceMonitor:
    """Monitor and log performance metrics for the application."""

    def __init__(self):
        self.metrics: Dict[str, Any] = {}

    def track(self, func: Callable) -> Callable:
        """Decorator to track and log the execution time of a function."""
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                if asyncio.iscoroutinefunction(func):
                    return await func(*args, **kwargs)
                else:
                    return func(*args, **kwargs)
            finally:
                duration = time.time() - start_time
                self.record_metric(func.__name__, duration)
        return wrapper

    def record_metric(self, name: str, value: Any):
        """Record a performance metric."""
        self.metrics[name] = value
        logger.info(f"Performance: {name} took {value:.4f}s")

    def get_metrics(self) -> Dict[str, Any]:
        """Get all recorded metrics."""
        return self.metrics.copy()

    def clear_metrics(self):
        """Clear all recorded metrics."""
        self.metrics.clear()

performance_monitor = PerformanceMonitor()