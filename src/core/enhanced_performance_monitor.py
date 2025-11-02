"""
Enhanced Performance Monitoring for Email Intelligence Platform

Extends the existing performance monitoring with additional metrics collection
for better system visibility and performance optimization.
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


class EnhancedPerformanceMonitor:
    """Monitors and tracks performance metrics across the system with enhanced capabilities"""

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
        """Log a performance entry to the log file with enhanced metrics"""
        try:
            # Add system metrics to every log entry
            system_metrics = self.get_system_metrics()
            log_entry.update(system_metrics)
            
            with self.lock:
                with open(LOG_FILE, "a") as f:
                    f.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            logger.warning(f"Failed to log performance: {e}")

    def get_system_metrics(self) -> Dict[str, Any]:
        """Get current system metrics with enhanced information"""
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)  # Short interval for more accurate reading
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Get process-specific metrics
            current_process = psutil.Process()
            process_memory = current_process.memory_info()
            process_cpu = current_process.cpu_percent()
            
            return {
                "system_cpu_percent": cpu_percent,
                "system_memory_percent": memory.percent,
                "system_memory_available": memory.available,
                "system_disk_usage_percent": (disk.used / disk.total) * 100,
                "process_memory_rss": process_memory.rss,
                "process_memory_vms": process_memory.vms,
                "process_cpu_percent": process_cpu,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        except Exception as e:
            logger.warning(f"Failed to get system metrics: {e}")
            return {}

    def record_processing_event(self, event: ProcessingEvent) -> None:
        """Record a processing event"""
        with self.lock:
            self.processing_events.append(event)

    def get_performance_summary(self, operation: str = None, hours: int = 24) -> Dict[str, Any]:
        """Get a summary of performance metrics for a specific operation or all operations"""
        try:
            metrics = []
            cutoff_time = time.time() - (hours * 3600)
            
            # Read log file and filter relevant entries
            with open(LOG_FILE, "r") as f:
                for line in f:
                    try:
                        entry = json.loads(line)
                        entry_time = datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00")).timestamp()
                        if entry_time >= cutoff_time:
                            if operation is None or entry.get("operation") == operation:
                                metrics.append(entry)
                    except (json.JSONDecodeError, ValueError):
                        continue
            
            if not metrics:
                return {"error": "No metrics found"}
            
            # Calculate statistics
            durations = [m["duration_seconds"] for m in metrics]
            avg_duration = sum(durations) / len(durations)
            min_duration = min(durations)
            max_duration = max(durations)
            
            # System metrics averages
            cpu_metrics = [m.get("system_cpu_percent", 0) for m in metrics if "system_cpu_percent" in m]
            memory_metrics = [m.get("system_memory_percent", 0) for m in metrics if "system_memory_percent" in m]
            
            avg_cpu = sum(cpu_metrics) / len(cpu_metrics) if cpu_metrics else 0
            avg_memory = sum(memory_metrics) / len(memory_metrics) if memory_metrics else 0
            
            return {
                "operation": operation or "all_operations",
                "total_executions": len(metrics),
                "average_duration_seconds": avg_duration,
                "min_duration_seconds": min_duration,
                "max_duration_seconds": max_duration,
                "average_system_cpu_percent": avg_cpu,
                "average_system_memory_percent": avg_memory,
                "time_period_hours": hours
            }
        except Exception as e:
            logger.warning(f"Failed to generate performance summary: {e}")
            return {"error": str(e)}


# Global enhanced performance monitor instance
enhanced_performance_monitor = EnhancedPerformanceMonitor()


def log_enhanced_performance(operation_or_func=None, *, operation: str = ""):
    """
    An enhanced decorator to log the performance of both sync and async functions
    with additional system metrics collection.
    Can be used as @log_enhanced_performance or @log_enhanced_performance(operation="custom_name").
    """
    if callable(operation_or_func) and operation == "":
        # Used as @log_enhanced_performance (without parentheses)
        func = operation_or_func
        op_name = func.__name__
        return _create_enhanced_decorator(func, op_name)
    elif operation_or_func is not None and operation == "":
        # Used as @log_enhanced_performance("custom_name")
        op_name = operation

        def decorator(func):
            return _create_enhanced_decorator(func, op_name)

        return decorator
    else:
        # Used as @log_enhanced_performance(operation="custom_name")
        op_name = operation

        def decorator(func):
            return _create_enhanced_decorator(func, op_name)

        return decorator


def _create_enhanced_decorator(func, op_name):
    """Create the enhanced decorator for a function"""
    if asyncio.iscoroutinefunction(func):

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            try:
                result = await func(*args, **kwargs)
                success = True
                error = None
            except Exception as e:
                result = None
                success = False
                error = str(e)
                raise
            finally:
                end_time = time.perf_counter()
                duration = end_time - start_time

                log_entry = {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "operation": op_name,
                    "duration_seconds": duration,
                    "success": success,
                }
                
                if not success:
                    log_entry["error"] = error

                try:
                    enhanced_performance_monitor.log_performance(log_entry)
                except Exception as e:
                    logger.warning(f"Failed to log enhanced performance: {e}")

            return result

        return async_wrapper
    else:

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                success = True
                error = None
            except Exception as e:
                result = None
                success = False
                error = str(e)
                raise
            finally:
                end_time = time.perf_counter()
                duration = end_time - start_time

                log_entry = {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "operation": op_name,
                    "duration_seconds": duration,
                    "success": success,
                }
                
                if not success:
                    log_entry["error"] = error

                try:
                    enhanced_performance_monitor.log_performance(log_entry)
                except Exception as e:
                    logger.warning(f"Failed to log enhanced performance: {e}")

            return result

        return sync_wrapper


# Backward compatibility - keep the original decorator
def log_performance(operation_or_func=None, *, operation: str = ""):
    """
    Maintains backward compatibility with the original performance logging decorator.
    """
    return log_enhanced_performance(operation_or_func, operation=operation)