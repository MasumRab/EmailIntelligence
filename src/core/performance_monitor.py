"""
Optimized Performance Monitoring for Email Intelligence Platform

<<<<<<< HEAD
Implements performance monitoring with logging for processing times,
model usage, memory consumption, and error rates.

Also includes the optimized version features:
- Efficient performance metrics collection with minimal overhead
- Asynchronous processing
- Configurable sampling rates
=======
Provides efficient performance metrics collection with minimal overhead,
asynchronous processing, and configurable sampling rates.
>>>>>>> 73a8d172 (Complete security hardening and production readiness implementation)
"""

import asyncio
import json
import logging
import threading
import time
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union
import atexit

logger = logging.getLogger(__name__)


@dataclass
class PerformanceMetric:
    """Represents a performance metric with minimal overhead."""

    name: str
    value: Union[int, float]
    unit: str
    timestamp: float
    tags: Dict[str, str]
    sample_rate: float = 1.0  # 1.0 = 100% sampling, 0.1 = 10% sampling


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
        flush_interval: int = 10
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

        # Threading and async
        self._buffer_lock = threading.Lock()
        self._stop_event = threading.Event()
        self._processing_thread = threading.Thread(
            target=self._process_metrics_background,
            daemon=True,
            name="PerformanceMonitor"
        )

        # Start background processing
        self._processing_thread.start()

        # Register cleanup
        atexit.register(self.shutdown)

        logger.info("OptimizedPerformanceMonitor initialized")

    def record_metric(
        self,
        name: str,
        value: Union[int, float],
        unit: str = "ms",
        tags: Optional[Dict[str, str]] = None,
        sample_rate: float = 1.0
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
        import random

        # Apply sampling
        if sample_rate < 1.0 and random.random() > sample_rate:
            return

        metric = PerformanceMetric(
            name=name,
            value=value,
            unit=unit,
            timestamp=time.time(),
            tags=tags or {},
            sample_rate=sample_rate
        )

        # Add to buffer (thread-safe)
        with self._buffer_lock:
            self._metrics_buffer.append(metric)

    def time_function(self, name: str, tags: Optional[Dict[str, str]] = None, sample_rate: float = 1.0):
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
                        name=name,
                        value=duration,
                        unit="ms",
                        tags=tags,
                        sample_rate=sample_rate
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
                def __enter__(self):
                    self.start_time = time.perf_counter()
                    return self

                def __exit__(self, exc_type, exc_val, exc_tb):
                    duration = (time.perf_counter() - self.start_time) * 1000
                    self.record_metric(
                        name=name,
                        value=duration,
                        unit="ms",
                        tags=tags,
                        sample_rate=sample_rate
                    )

            return TimerContext()

    def get_aggregated_metrics(self, name: Optional[str] = None) -> Dict[str, AggregatedMetric]:
        """
        Get current aggregated metrics.

        Args:
            name: Specific metric name, or None for all metrics
        """
        if name:
            return {name: self._aggregated_metrics.get(name)} if name in self._aggregated_metrics else {}
        return self._aggregated_metrics.copy()

    def get_recent_metrics(self, name: str, limit: int = 100) -> List[PerformanceMetric]:
        """Get recent raw metrics for a specific name."""
        with self._buffer_lock:
            return [m for m in self._metrics_buffer if m.name == name][-limit:]

    def _process_metrics_background(self):
        """Background thread to process and aggregate metrics."""
        while not self._stop_event.is_set():
            try:
                # Sleep for flush interval
                time.sleep(self.flush_interval)

                # Process metrics
                self._aggregate_metrics()
                self._flush_to_disk()

            except Exception as e:
                logger.error(f"Error in metrics processing: {e}")

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
                tags={}  # Could be enhanced to include common tags
            )

            self._aggregated_metrics[name] = aggregated

    def _flush_to_disk(self):
        """Flush aggregated metrics to disk."""
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                for metric in self._aggregated_metrics.values():
                    json.dump(asdict(metric), f, ensure_ascii=False)
                    f.write('\n')

            # Clear aggregated metrics after flushing
            self._aggregated_metrics.clear()

        except Exception as e:
            logger.error(f"Error flushing metrics to disk: {e}")

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


# Global performance monitor instance
performance_monitor = OptimizedPerformanceMonitor()

# Convenience functions
def record_metric(*args, **kwargs):
    """Convenience function to record metrics."""
    performance_monitor.record_metric(*args, **kwargs)

<<<<<<< HEAD
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


import atexit

# Enhanced performance monitoring system with additional features
from collections import defaultdict, deque
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Optional, Union

logger = logging.getLogger(__name__)


@dataclass
class PerformanceMetric:
    """Represents a performance metric with minimal overhead."""

    name: str
    value: Union[int, float]
    unit: str
    timestamp: float
    tags: Dict[str, str]
    sample_rate: float = 1.0  # 1.0 = 100% sampling, 0.1 = 10% sampling


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
        self._metrics_buffer: deque[PerformanceMetric] = deque(
            maxlen=max_metrics_buffer
        )
        self._aggregated_metrics: Dict[str, AggregatedMetric] = {}

        # Threading and async
        self._buffer_lock = threading.Lock()
        self._stop_event = threading.Event()
        self._processing_thread = threading.Thread(
            target=self._process_metrics_background,
            daemon=True,
            name="PerformanceMonitor",
        )

        # Start background processing
        self._processing_thread.start()

        # Register cleanup
        atexit.register(self.shutdown)

        logger.info("OptimizedPerformanceMonitor initialized")

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
        import random

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
                    duration = (
                        time.perf_counter() - start_time
                    ) * 1000  # Convert to milliseconds
                    self.record_metric(
                        name=name,
                        value=duration,
                        unit="ms",
                        tags=tags,
                        sample_rate=sample_rate,
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
                def __enter__(self):
                    self.start_time = time.perf_counter()
                    return self

                def __exit__(self, exc_type, exc_val, exc_tb):
                    duration = (time.perf_counter() - self.start_time) * 1000
                    self.record_metric(
                        name=name,
                        value=duration,
                        unit="ms",
                        tags=tags,
                        sample_rate=sample_rate,
                    )

            return TimerContext()

    def get_aggregated_metrics(
        self, name: Optional[str] = None
    ) -> Dict[str, AggregatedMetric]:
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

    def get_recent_metrics(
        self, name: str, limit: int = 100
    ) -> List[PerformanceMetric]:
        """Get recent raw metrics for a specific name."""
        with self._buffer_lock:
            return [m for m in self._metrics_buffer if m.name == name][-limit:]

    def _process_metrics_background(self):
        """Background thread to process and aggregate metrics."""
        while not self._stop_event.is_set():
            try:
                # Sleep for flush interval
                time.sleep(self.flush_interval)

                # Process metrics
                self._aggregate_metrics()
                self._flush_to_disk()

            except Exception as e:
                logger.error(f"Error in metrics processing: {e}")

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


# Global performance monitor instance
performance_monitor = OptimizedPerformanceMonitor()


# Convenience functions
def record_metric(*args, **kwargs):
    """Convenience function to record metrics."""
    performance_monitor.record_metric(*args, **kwargs)


=======
>>>>>>> 73a8d172 (Complete security hardening and production readiness implementation)
def time_function(*args, **kwargs):
    """Convenience function to time functions."""
    return performance_monitor.time_function(*args, **kwargs)
