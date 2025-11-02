"""
Performance Monitoring for Email Intelligence Platform

Implements performance monitoring with logging for processing times,
model usage, memory consumption, and error rates.
"""

import asyncio
import json
import logging
import threading
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from functools import wraps
from typing import Any, Callable, Dict, List, Optional

import psutil

logger = logging.getLogger(__name__)

LOG_FILE = "performance_metrics_log.jsonl"


@dataclass
class PerformanceMetric:
    """Represents a single performance metric"""

    timestamp: float
    value: float
    unit: str
    source: str


@dataclass
class ProcessingEvent:
    """Represents a processing event in the system"""

    event_type: str  # 'model_load', 'model_unload', 'workflow_execute', etc.
    model_name: Optional[str]
    workflow_name: Optional[str]
    start_time: float
    end_time: Optional[float]
    success: bool
    details: Dict[str, Any]


class PerformanceMonitor:
    """Monitors and tracks performance metrics across the system"""

    def __init__(self):
        self.metrics: List[PerformanceMetric] = []
        self.processing_events: List[ProcessingEvent] = []
        self.lock = threading.Lock()
        self._ensure_log_file_exists()

    def _ensure_log_file_exists(self):
        """Ensure the log file exists"""
        try:
            with open(LOG_FILE, "a"):
                pass
        except Exception as e:
            logger.warning(f"Failed to create performance log file: {e}")

    def log_performance(self, log_entry: Dict[str, Any]) -> None:
        """Log a performance entry to the log file"""
        try:
            with self.lock:
                with open(LOG_FILE, "a") as f:
                    f.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            logger.warning(f"Failed to log performance: {e}")

    def get_system_metrics(self) -> Dict[str, Any]:
        """Get current system metrics"""
        try:
            cpu_percent = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            return {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_available": memory.available,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        except Exception as e:
            logger.warning(f"Failed to get system metrics: {e}")
            return {}

    def record_processing_event(self, event: ProcessingEvent) -> None:
        """Record a processing event"""
        with self.lock:
            self.processing_events.append(event)


# Global performance monitor instance
performance_monitor = PerformanceMonitor()


def log_performance(operation_or_func=None, *, operation: str = ""):
    """
    A decorator to log the performance of both sync and async functions.
    Can be used as @log_performance or @log_performance(operation="custom_name").
    """
    if callable(operation_or_func) and operation == "":
        # Used as @log_performance (without parentheses)
        func = operation_or_func
        op_name = func.__name__
        return _create_decorator(func, op_name)
    elif operation_or_func is not None and operation == "":
        # Used as @log_performance("custom_name")
        op_name = operation

        def decorator(func):
            return _create_decorator(func, op_name)

        return decorator
    else:
        # Used as @log_performance(operation="custom_name")
        op_name = operation

        def decorator(func):
            return _create_decorator(func, op_name)

        return decorator


def _create_decorator(func, op_name):
    """Create the actual decorator for a function"""
    if asyncio.iscoroutinefunction(func):

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = await func(*args, **kwargs)
            end_time = time.perf_counter()
            duration = end_time - start_time

            log_entry = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "operation": op_name,
                "duration_seconds": duration,
            }

            try:
                performance_monitor.log_performance(log_entry)
            except Exception as e:
                logger.warning(f"Failed to log performance: {e}")

            return result

        return async_wrapper
    else:

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            duration = end_time - start_time

            log_entry = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "operation": op_name,
                "duration_seconds": duration,
            }

            try:
                performance_monitor.log_performance(log_entry)
            except Exception as e:
                logger.warning(f"Failed to log performance: {e}")

            return result

        return sync_wrapper