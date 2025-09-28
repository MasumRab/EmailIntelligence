"""
Performance monitoring module for the Email Intelligence backend.
"""

import time
import logging
from typing import Dict, Any
from contextlib import contextmanager


logger = logging.getLogger(__name__)


class PerformanceMonitor:
    """Monitor and log performance metrics for the application."""
    
    def __init__(self):
        self.metrics: Dict[str, Any] = {}
        self.start_times: Dict[str, float] = {}
    
    @contextmanager
    def measure(self, operation_name: str):
        """Context manager to measure operation duration."""
        start_time = time.time()
        try:
            yield
        finally:
            duration = time.time() - start_time
            self.record_metric(operation_name, duration)
    
    def record_metric(self, name: str, value: Any):
        """Record a performance metric."""
        self.metrics[name] = value
        logger.debug(f"Performance metric recorded: {name} = {value}")
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get all recorded metrics."""
        return self.metrics.copy()
    
    def clear_metrics(self):
        """Clear all recorded metrics."""
        self.metrics.clear()
        self.start_times.clear()