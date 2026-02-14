"""
Performance Monitoring for Email Intelligence Platform

Implements performance monitoring with logging for processing times,
model usage, memory consumption, and error rates.

Also includes the optimized version features:
- Efficient performance metrics collection with minimal overhead
- Asynchronous processing
- Configurable sampling rates
"""

import asyncio
import atexit
import json
import logging
import random
import threading
import time
from collections import defaultdict, deque
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

import psutil

logger = logging.getLogger(__name__)

LOG_FILE = "performance_metrics_log.jsonl"


@dataclass
class PerformanceMetric:
    """Represents a single performance metric"""

    name: str
    value: Union[int, float]
    unit: str
    timestamp: float
    tags: Dict[str, str]
    sample_rate: float = 1.0  # 1.0 = 100% sampling, 0.1 = 10% sampling

    @property
    def source(self) -> str:
        """Alias for tags.get("source", name) for backward compatibility"""
        return self.tags.get("source", self.name)


@dataclass
class AggregatedMetric:
    """Aggregated performance statistics."""

    name: str
    count: int
    sum: float
    avg: float
    min: float
    max: float
    p95: float
    p99: float
    timestamp: float
    tags: Dict[str, str]


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


class OptimizedPerformanceMonitor:
    """
    High-performance metrics collection with minimal overhead.

    Features:
    - Configurable sampling rates to reduce collection overhead
    - Asynchronous processing to avoid blocking main threads
    - Sliding window aggregation for real-time statistics
    - Memory-efficient storage with automatic cleanup
    """

    def __init__(
        self,
        log_file: str = "logs/performance_metrics.jsonl",
        aggregation_window: int = 60,  # seconds
        max_metrics_buffer: int = 10000,
        flush_interval: int = 10,
    ):
        self.log_file = Path(log_file)
        self.aggregation_window = aggregation_window
        self.max_metrics_buffer = max_metrics_buffer
        self.flush_interval = flush_interval

        # Create logs directory
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        # Metrics storage
        self._metrics_buffer: deque[PerformanceMetric] = deque(maxlen=max_metrics_buffer)
        self._aggregated_metrics: Dict[str, AggregatedMetric] = {}
        self.processing_events: List[ProcessingEvent] = []

        # Threading and async
        self._buffer_lock = threading.Lock()
        self._stop_event = threading.Event()
        self._processing_thread = threading.Thread(
            target=self._process_metrics_background, daemon=True, name="PerformanceMonitor"
        )

        # Start background processing
        self._processing_thread.start()

        # Register cleanup
        atexit.register(self.shutdown)

        logger.info("OptimizedPerformanceMonitor initialized")

    def log_performance(self, log_entry: Dict[str, Any]) -> None:
        """Log a performance entry (compatibility wrapper)."""
        name = log_entry.get("operation", "unknown_operation")
        value = log_entry.get("duration_seconds", 0) * 1000  # Convert to ms
        self.record_metric(name=name, value=value, unit="ms")

    def record_metric(
        self,
        name: str,
        value: Union[int, float],
        unit: str = "ms",
        tags: Optional[Dict[str, str]] = None,
        sample_rate: float = 1.0,
    ):
        """
        Record a performance metric with optional sampling.

        Args:
            name: Metric name (e.g., "api_response_time")
            value: Metric value
            unit: Unit of measurement
            tags: Additional tags for categorization
            sample_rate: Sampling rate (0.0-1.0)
        """
        # Apply sampling
        if sample_rate < 1.0 and random.random() > sample_rate:
            return

        metric = PerformanceMetric(
            name=name,
            value=value,
            unit=unit,
            timestamp=time.time(),
            tags=tags or {},
            sample_rate=sample_rate,
        )

        # Add to buffer (thread-safe)
        with self._buffer_lock:
            self._metrics_buffer.append(metric)

    def time_function(
        self, name: str, tags: Optional[Dict[str, str]] = None, sample_rate: float = 1.0
    ):
        """
        Decorator/context manager to time function execution.

        Usage:
            @monitor.time_function("my_function")
            def my_function():
                pass

            with monitor.time_function("my_operation"):
                do_something()
        """

        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.perf_counter()
                try:
                    return func(*args, **kwargs)
                finally:
                    duration = (time.perf_counter() - start_time) * 1000  # Convert to milliseconds
                    self.record_metric(
                        name=name, value=duration, unit="ms", tags=tags, sample_rate=sample_rate
                    )

            return wrapper

        # Support both decorator and context manager usage
        if callable(name):
            # Used as @time_function
            func = name
            return decorator(func)
        else:
            # Used as @time_function("name") or with time_function("name"):
            class TimerContext:
                def __init__(self, monitor):
                    self.monitor = monitor
                    self.start_time = 0

                def __enter__(self):
                    self.start_time = time.perf_counter()
                    return self

                def __exit__(self, exc_type, exc_val, exc_tb):
                    duration = (time.perf_counter() - self.start_time) * 1000
                    self.monitor.record_metric(
                        name=name, value=duration, unit="ms", tags=tags, sample_rate=sample_rate
                    )

            return TimerContext(self)

    def get_aggregated_metrics(self, name: Optional[str] = None) -> Dict[str, AggregatedMetric]:
        """
        Get current aggregated metrics.

        Args:
            name: Specific metric name, or None for all metrics
        """
        if name:
            return (
                {name: self._aggregated_metrics.get(name)}
                if name in self._aggregated_metrics
                else {}
            )
        return self._aggregated_metrics.copy()

    def get_recent_metrics(self, name: Optional[str] = None, limit: int = 100) -> List[PerformanceMetric]:
        """Get recent raw metrics, optionally filtered by name."""
        with self._buffer_lock:
            if name:
                return [m for m in self._metrics_buffer if m.name == name][-limit:]
            return list(self._metrics_buffer)[-limit:]

    def get_system_metrics(self) -> Dict[str, Any]:
        """Get current system metrics (compatibility method)"""
        try:
            cpu_percent = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage("/")
            return {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_available": memory.available,
                "disk_percent": disk.percent,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        except Exception as e:
            logger.warning(f"Failed to get system metrics: {e}")
            return {}

    def record_processing_event(self, event: ProcessingEvent) -> None:
        """Record a processing event (compatibility method)"""
        with self._buffer_lock:
            self.processing_events.append(event)

    def record_model_performance(
        self,
        model_name: str,
        execution_time: float,
        success: bool = True,
    ) -> None:
        """Record performance metric for a model execution"""
        self.record_metric(
            name=f"model_{model_name}_execution_time",
            value=execution_time,
            unit="seconds",
            tags={"source": "model_execution", "model": model_name}
        )
        self.record_metric(
            name=f"model_{model_name}_success",
            value=1.0 if success else 0.0,
            unit="boolean",
            tags={"source": "model_success", "model": model_name}
        )

    def record_workflow_execution(
        self,
        workflow_name: str,
        execution_time: float,
        success: bool = True,
    ) -> None:
        """Record performance metric for a workflow execution"""
        self.record_metric(
            name=f"workflow_{workflow_name}_execution_time",
            value=execution_time,
            unit="seconds",
            tags={"source": "workflow_execution", "workflow": workflow_name}
        )

    def record_event(
        self,
        event_type: str,
        model_name: Optional[str] = None,
        workflow_name: Optional[str] = None,
        success: bool = True,
        details: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Record a processing event"""
        event = ProcessingEvent(
            event_type=event_type,
            model_name=model_name,
            workflow_name=workflow_name,
            start_time=time.time(),
            end_time=None,
            success=success,
            details=details or {},
        )
        self.record_processing_event(event)
        return f"event_{int(event.start_time)}"

    def complete_event(self, event_id: str, success: bool = True) -> None:
        """Complete a processing event (stub for now as we don't index by ID)"""
        # In a real implementation, we'd need to find the event by ID.
        # Since ProcessingEvent objects are stored in a list, this would require search.
        pass

    def get_model_performance(self, model_name: str, minutes: int = 5) -> List[PerformanceMetric]:
        """Get performance metrics for a specific model."""
        cutoff_time = time.time() - (minutes * 60)
        with self._buffer_lock:
            return [
                m for m in self._metrics_buffer
                if m.tags.get("model") == model_name and m.timestamp >= cutoff_time
            ]

    def get_avg_model_performance(self, model_name: str, minutes: int = 5) -> Optional[float]:
        """Get average performance for a model."""
        metrics = self.get_model_performance(model_name, minutes)
        times = [m.value for m in metrics if "execution_time" in m.name]
        if not times:
            return None
        return sum(times) / len(times)

    def get_system_stats(self) -> Dict[str, float]:
        """Get current system stats."""
        metrics = self.get_system_metrics()
        return {
            "cpu_usage": metrics.get("cpu_percent", 0.0),
            "memory_usage": metrics.get("memory_percent", 0.0),
            "disk_usage": metrics.get("disk_percent", 0.0),
        }

    def get_error_rate(self, minutes: int = 5) -> float:
        """Get the error rate in the last specified minutes."""
        cutoff_time = time.time() - (minutes * 60)
        with self._buffer_lock:
            recent_events = [e for e in self.processing_events if e.start_time >= cutoff_time]

        if not recent_events:
            return 0.0

        failed = [e for e in recent_events if not e.success]
        return len(failed) / len(recent_events)

    def stop_monitoring(self):
        """Stop monitoring (alias for shutdown)."""
        self.shutdown()

    def _process_metrics_background(self):
        """Background thread to process and aggregate metrics."""
        while not self._stop_event.is_set():
            try:
                # Sleep for flush interval
                time.sleep(self.flush_interval)

                # Process metrics
                self._aggregate_metrics()
                self._flush_to_disk()

            except (IOError, OSError) as e:
                logger.error(f"IO Error in metrics processing: {e}")
            except psutil.Error as e:
                logger.error(f"System metrics error: {e}")
            except Exception as e:  # pylint: disable=broad-exception-caught
                logger.exception("Unexpected error in metrics processing thread")

    def _aggregate_metrics(self):
        """Aggregate metrics in sliding windows."""
        current_time = time.time()
        cutoff_time = current_time - self.aggregation_window

        # Collect metrics within window
        metric_values: Dict[str, List[float]] = defaultdict(list)

        with self._buffer_lock:
            for metric in self._metrics_buffer:
                if metric.timestamp >= cutoff_time:
                    metric_values[metric.name].append(metric.value)

        # Calculate aggregations
        for name, values in metric_values.items():
            if not values:
                continue

            values_sorted = sorted(values)
            count = len(values)

            aggregated = AggregatedMetric(
                name=name,
                count=count,
                sum=sum(values),
                avg=sum(values) / count,
                min=min(values),
                max=max(values),
                p95=values_sorted[int(count * 0.95)] if count > 0 else 0,
                p99=values_sorted[int(count * 0.99)] if count > 0 else 0,
                timestamp=current_time,
                tags={},  # Could be enhanced to include common tags
            )

            self._aggregated_metrics[name] = aggregated

    def _flush_to_disk(self):
        """Flush aggregated metrics to disk."""
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                for metric in self._aggregated_metrics.values():
                    json.dump(asdict(metric), f, ensure_ascii=False)
                    f.write("\n")

            # Clear aggregated metrics after flushing
            self._aggregated_metrics.clear()

        except Exception as e:
            logger.error(f"Error flushing metrics to disk: {e}")

    def get_metric_history(
        self, metric_name: str, duration_seconds: int = 3600
    ) -> List[Dict[str, Any]]:
        """Get history of aggregated metrics for a specific metric."""
        # Note: In a real implementation, this would read from the log file
        # For now, we return empty list or buffered metrics if applicable
        # This is a stub to satisfy potential calls
        return []

    def shutdown(self):
        """Shutdown the performance monitor gracefully."""
        logger.info("Shutting down OptimizedPerformanceMonitor")

        self._stop_event.set()

        # Final flush
        try:
            self._aggregate_metrics()
            self._flush_to_disk()
        except Exception as e:
            logger.error(f"Error in final metrics flush: {e}")

        if self._processing_thread.is_alive():
            self._processing_thread.join(timeout=5.0)


# Global performance monitor instance (using the optimized version)
performance_monitor = OptimizedPerformanceMonitor()
PerformanceMonitor = OptimizedPerformanceMonitor  # Alias for backward compatibility


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
            try:
                return await func(*args, **kwargs)
            finally:
                duration = (time.perf_counter() - start_time) * 1000
                performance_monitor.record_metric(name=op_name, value=duration, unit="ms")

        return async_wrapper
    else:

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            try:
                return func(*args, **kwargs)
            finally:
                duration = (time.perf_counter() - start_time) * 1000
                performance_monitor.record_metric(name=op_name, value=duration, unit="ms")

        return sync_wrapper


# Convenience functions
def record_metric(*args, **kwargs):
    """Convenience function to record metrics."""
    performance_monitor.record_metric(*args, **kwargs)


def time_function(*args, **kwargs):
    """Convenience function to time functions."""
    return performance_monitor.time_function(*args, **kwargs)
