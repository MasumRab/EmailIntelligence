"""
Performance Monitoring Dashboard for Email Intelligence Platform

Implements real-time performance monitoring with visualizations for processing times,
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
        self._metrics: List[PerformanceMetric] = []
        self._events: List[ProcessingEvent] = []
        self._model_performance: Dict[str, List[PerformanceMetric]] = {}
        self._lock = threading.Lock()

        # Monitor system resources
        self._system_monitoring = True
        self._monitoring_thread = threading.Thread(
            target=self._monitor_system_resources, daemon=True
        )
        self._monitoring_thread.start()

    def _monitor_system_resources(self):
        """Monitor system resources in a background thread"""
        while self._system_monitoring:
            with self._lock:
                timestamp = time.time()
                cpu_percent = psutil.cpu_percent(interval=1)
                self._metrics.append(
                    PerformanceMetric(timestamp=timestamp, value=cpu_percent, unit="%", source="cpu_usage")
                )
                memory = psutil.virtual_memory()
                self._metrics.append(
                    PerformanceMetric(timestamp=timestamp, value=memory.percent, unit="%", source="memory_usage")
                )
                disk = psutil.disk_usage("/")
                self._metrics.append(
                    PerformanceMetric(timestamp=timestamp, value=disk.percent, unit="%", source="disk_usage")
                )
            time.sleep(5)  # Monitor every 5 seconds

    def record_model_performance(
        self, model_name: str, execution_time: float, success: bool = True
    ):
        """Record performance metric for a model execution"""
        with self._lock:
            timestamp = time.time()
            self._metrics.append(
                PerformanceMetric(
                    timestamp=timestamp,
                    value=execution_time,
                    unit="seconds",
                    source=f"model_{model_name}_execution_time",
                )
            )
            if model_name not in self._model_performance:
                self._model_performance[model_name] = []
            self._model_performance[model_name].append(
                PerformanceMetric(
                    timestamp=timestamp, value=execution_time, unit="seconds", source="execution_time"
                )
            )
            self._metrics.append(
                PerformanceMetric(
                    timestamp=timestamp,
                    value=1.0 if success else 0.0,
                    unit="boolean",
                    source=f"model_{model_name}_success",
                )
            )

    def record_workflow_execution(
        self, workflow_name: str, execution_time: float, success: bool = True
    ):
        """Record performance metric for a workflow execution"""
        with self._lock:
            timestamp = time.time()
            self._metrics.append(
                PerformanceMetric(
                    timestamp=timestamp,
                    value=execution_time,
                    unit="seconds",
                    source=f"workflow_{workflow_name}_execution_time",
                )
            )

    def get_recent_metrics(
        self, minutes: int = 5, source_filter: Optional[str] = None
    ) -> List[PerformanceMetric]:
        """Get metrics from the last specified minutes"""
        with self._lock:
            cutoff_time = time.time() - (minutes * 60)
            return sorted(
                [
                    m for m in self._metrics
                    if m.timestamp >= cutoff_time and (not source_filter or source_filter in m.source)
                ],
                key=lambda m: m.timestamp,
            )

    def get_system_stats(self) -> Dict[str, float]:
        """Get current system stats"""
        with self._lock:
            cpu = next((m.value for m in reversed(self._metrics) if m.source == "cpu_usage"), 0.0)
            mem = next((m.value for m in reversed(self._metrics) if m.source == "memory_usage"), 0.0)
            disk = next((m.value for m in reversed(self._metrics) if m.source == "disk_usage"), 0.0)
            return {"cpu_usage": cpu, "memory_usage": mem, "disk_usage": disk}

    def get_error_rate(self, minutes: int = 5) -> float:
        """Get the error rate in the last specified minutes"""
        with self._lock:
            cutoff_time = time.time() - (minutes * 60)
            recent_events = [e for e in self._events if e.start_time >= cutoff_time and e.end_time]
            if not recent_events:
                return 0.0
            failed_count = sum(1 for e in recent_events if not e.success)
            return failed_count / len(recent_events)

    def stop_monitoring(self):
        """Stop the system resource monitoring"""
        self._system_monitoring = False

    def log_performance_metric(self, log_entry: Dict[str, Any]):
        """Log a performance entry to file"""
        try:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            logger.error(f"Failed to write performance log: {e}")


# Global performance monitor instance
performance_monitor = PerformanceMonitor()

def get_performance_monitor() -> PerformanceMonitor:
    """Get the global performance monitor instance"""
    return performance_monitor

def _create_decorator(func, op_name):
    """Helper to create the sync/async decorator"""
    if asyncio.iscoroutinefunction(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            try:
                return await func(*args, **kwargs)
            finally:
                duration = time.perf_counter() - start_time
                log_entry = {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "operation": op_name,
                    "duration_seconds": duration,
                }
                performance_monitor.log_performance_metric(log_entry)
        return async_wrapper
    else:
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            try:
                return func(*args, **kwargs)
            finally:
                duration = time.perf_counter() - start_time
                log_entry = {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "operation": op_name,
                    "duration_seconds": duration,
                }
                performance_monitor.log_performance_metric(log_entry)
        return sync_wrapper

def log_performance(operation_or_func=None, *, operation: str = ""):
    """
    A decorator to log the performance of both sync and async functions.
    Can be used as @log_performance or @log_performance(operation="custom_name").
    """
    if callable(operation_or_func):
        # Used as @log_performance
        return _create_decorator(operation_or_func, operation_or_func.__name__)

    # Used as @log_performance() or @log_performance(operation="...")
    def decorator(func):
        op_name = operation or func.__name__
        return _create_decorator(func, op_name)
    return decorator
