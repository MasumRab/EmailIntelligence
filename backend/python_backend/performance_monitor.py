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

                # CPU usage
                cpu_percent = psutil.cpu_percent(interval=1)
                self._metrics.append(
                    PerformanceMetric(
                        timestamp=timestamp, value=cpu_percent, unit="%", source="cpu_usage"
                    )
                )

                # Memory usage
                memory = psutil.virtual_memory()
                self._metrics.append(
                    PerformanceMetric(
                        timestamp=timestamp, value=memory.percent, unit="%", source="memory_usage"
                    )
                )

                # Disk usage
                disk = psutil.disk_usage("/")
                disk_percent = (disk.used / disk.total) * 100
                self._metrics.append(
                    PerformanceMetric(
                        timestamp=timestamp, value=disk_percent, unit="%", source="disk_usage"
                    )
                )

            time.sleep(5)  # Monitor every 5 seconds

    def record_model_performance(
        self, model_name: str, execution_time: float, success: bool = True
    ) -> None:
        """Record performance metric for a model execution"""
        with self._lock:
            timestamp = time.time()

            # Execution time metric
            self._metrics.append(
                PerformanceMetric(
                    timestamp=timestamp,
                    value=execution_time,
                    unit="seconds",
                    source=f"model_{model_name}_execution_time",
                )
            )

            # Add to model-specific metrics
            if model_name not in self._model_performance:
                self._model_performance[model_name] = []
            self._model_performance[model_name].append(
                PerformanceMetric(
                    timestamp=timestamp,
                    value=execution_time,
                    unit="seconds",
                    source="execution_time",
                )
            )

            # Success/failure rate
            success_value = 1.0 if success else 0.0
            self._metrics.append(
                PerformanceMetric(
                    timestamp=timestamp,
                    value=success_value,
                    unit="boolean",
                    source=f"model_{model_name}_success",
                )
            )

    def record_workflow_execution(
        self, workflow_name: str, execution_time: float, success: bool = True
    ) -> None:
        """Record performance metric for a workflow execution"""
        with self._lock:
            timestamp = time.time()

            # Execution time metric
            self._metrics.append(
                PerformanceMetric(
                    timestamp=timestamp,
                    value=execution_time,
                    unit="seconds",
                    source=f"workflow_{workflow_name}_execution_time",
                )
            )

    def record_event(
        self,
        event_type: str,
        model_name: Optional[str] = None,
        workflow_name: Optional[str] = None,
        success: bool = True,
        details: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Record a processing event in the system"""
        with self._lock:
            event = ProcessingEvent(
                event_type=event_type,
                model_name=model_name,
                workflow_name=workflow_name,
                start_time=time.time(),
                end_time=None,
                success=success,
                details=details or {},
            )
            event_id = f"event_{len(self._events)}_{int(event.start_time)}"
            self._events.append(event)
            return event_id

    def complete_event(self, event_id: str, success: bool = True) -> None:
        """Complete a processing event"""
        with self._lock:
            # Find the event with the given ID
            for event in self._events:
                if f"event_{len(self._events)}_{int(event.start_time)}" == event_id:
                    event.end_time = time.time()
                    event.success = success
                    break

    def get_recent_metrics(
        self, minutes: int = 5, source_filter: Optional[str] = None
    ) -> List[PerformanceMetric]:
        """Get metrics from the last specified minutes"""
        with self._lock:
            cutoff_time = time.time() - (minutes * 60)
            filtered_metrics = [
                metric
                for metric in self._metrics
                if metric.timestamp >= cutoff_time
                and (source_filter is None or source_filter in metric.source)
            ]
            return sorted(filtered_metrics, key=lambda m: m.timestamp)

    def get_model_performance(self, model_name: str, minutes: int = 5) -> List[PerformanceMetric]:
        """Get performance metrics for a specific model"""
        with self._lock:
            if model_name not in self._model_performance:
                return []

            cutoff_time = time.time() - (minutes * 60)
            filtered_metrics = [
                metric
                for metric in self._model_performance[model_name]
                if metric.timestamp >= cutoff_time
            ]
            return sorted(filtered_metrics, key=lambda m: m.timestamp)

    def get_avg_model_performance(self, model_name: str, minutes: int = 5) -> Optional[float]:
        """Get average performance for a model in the last specified minutes"""
        metrics = self.get_model_performance(model_name, minutes)
        if not metrics:
            return None

        execution_times = [m.value for m in metrics if m.source == "execution_time"]
        if not execution_times:
            return None

        return sum(execution_times) / len(execution_times)

    def get_system_stats(self) -> Dict[str, float]:
        """Get current system stats"""
        with self._lock:
            # Get the most recent values for CPU, memory, and disk usage
            cpu_metrics = [m for m in self._metrics if m.source == "cpu_usage"]
            memory_metrics = [m for m in self._metrics if m.source == "memory_usage"]
            disk_metrics = [m for m in self._metrics if m.source == "disk_usage"]

            return {
                "cpu_usage": cpu_metrics[-1].value if cpu_metrics else 0.0,
                "memory_usage": memory_metrics[-1].value if memory_metrics else 0.0,
                "disk_usage": disk_metrics[-1].value if disk_metrics else 0.0,
            }

    def get_error_rate(self, minutes: int = 5) -> float:
        """Get the error rate in the last specified minutes"""
        with self._lock:
            cutoff_time = time.time() - (minutes * 60)
            recent_events = [event for event in self._events if event.start_time >= cutoff_time]

            if not recent_events:
                return 0.0

            failed_events = [event for event in recent_events if not event.success]
            return len(failed_events) / len(recent_events)

    def stop_monitoring(self):
        """Stop the system resource monitoring"""
        self._system_monitoring = False

    def log_performance(self, log_entry: Dict[str, Any]) -> None:
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

def log_performance(_func=None, *, operation: str = ""):
    """
    A decorator to log the performance of both sync and async functions.
    Can be used as @log_performance or @log_performance(operation="custom_name").
    """
    def decorator(func):
        op_name = operation or func.__name__

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

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    if _func is None:
        return decorator
    else:
        return decorator(_func)
