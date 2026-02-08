"""
Performance Monitoring Adapter for Email Intelligence Platform

Adapts the backend performance monitoring requirements to use the
core OptimizedPerformanceMonitor.
"""

import logging
import time
from typing import Any, Dict, List, Optional

from src.core.performance_monitor import performance_monitor as core_monitor
from src.core.performance_monitor import PerformanceMetric
from src.core.performance_monitor import log_performance, time_function  # pylint: disable=unused-import

logger = logging.getLogger(__name__)


class PerformanceMonitorAdapter:
    """
    Adapter to make OptimizedPerformanceMonitor compatible with the
    legacy backend PerformanceMonitor interface.
    """

    def __init__(self):
        self.core = core_monitor

    def record_model_performance(
        self,
        model_name: str,
        execution_time: float,
        success: bool = True,
    ) -> None:
        """Record performance metric for a model execution"""
        self.core.record_metric(
            name="model_execution_time",
            value=execution_time * 1000,  # Convert to ms
            unit="ms",
            tags={"model": model_name, "success": str(success)},
        )
        self.core.record_metric(
            name="model_success",
            value=1 if success else 0,
            unit="count",
            tags={"model": model_name},
        )

    def record_workflow_execution(
        self,
        workflow_name: str,
        execution_time: float,
        success: bool = True,
    ) -> None:
        """Record performance metric for a workflow execution"""
        self.core.record_metric(
            name="workflow_execution_time",
            value=execution_time * 1000,  # Convert to ms
            unit="ms",
            tags={"workflow": workflow_name, "success": str(success)},
        )

    def record_event(
        self,
        event_type: str,
        model_name: Optional[str] = None,
        workflow_name: Optional[str] = None,
        success: bool = True,
        details: Optional[Dict[str, Any]] = None,  # pylint: disable=unused-argument
    ) -> str:
        """
        Record a processing event.
        Note: The optimized monitor handles aggregation, so individual event tracking
        is simplified to metrics.
        """
        tags = {"type": event_type, "success": str(success)}
        if model_name:
            tags["model"] = model_name
        if workflow_name:
            tags["workflow"] = workflow_name

        self.core.record_metric(
            name="processing_event",
            value=1,
            unit="count",
            tags=tags
        )
        return "event_tracked"

    def complete_event(self, event_id: str, success: bool = True) -> None:
        """Complete a processing event (No-op in aggregate monitor)"""

    def get_recent_metrics(
        self,
        minutes: int = 5,
        source_filter: Optional[str] = None,
    ) -> List[PerformanceMetric]:
        """Get recent raw metrics (Delegates to core buffer)"""
        start_time = time.time() - (minutes * 60)
        metrics = self.core.get_metric_history(start_time)

        if source_filter:
            # Filter by source (mapped to metric name here)
            return [m for m in metrics if source_filter in m.name]
        return metrics

    def get_model_performance(self, model_name: str, minutes: int = 5) -> List[PerformanceMetric]:
        """Get performance metrics for a specific model"""
        start_time = time.time() - (minutes * 60)
        metrics = self.core.get_metric_history(start_time, name="model_execution_time")
        return [m for m in metrics if m.tags.get("model") == model_name]

    def get_avg_model_performance(self, model_name: str, minutes: int = 5) -> Optional[float]:
        """Get average performance for a model"""
        metrics = self.get_model_performance(model_name, minutes)
        if not metrics:
            return None

        values = [m.value for m in metrics]
        return (sum(values) / len(values)) / 1000.0  # Convert ms back to seconds

    def get_system_stats(self) -> Dict[str, float]:
        """Get current system stats"""
        metrics = self.core.get_system_metrics()
        return {
            "cpu_usage": metrics.get("cpu_percent", 0.0),
            "memory_usage": metrics.get("memory_percent", 0.0),
            "disk_usage": 0.0, # Not tracked in core yet
        }

    def get_error_rate(self, minutes: int = 5) -> float:
        """Get the error rate"""
        start_time = time.time() - (minutes * 60)
        metrics = self.core.get_metric_history(start_time, name="model_success")

        if not metrics:
            return 0.0

        failures = sum(1 for m in metrics if m.value == 0)
        return failures / len(metrics)

    def stop_monitoring(self):
        """Stop the system resource monitoring"""
        self.core.shutdown()

    def log_performance(self, log_entry: Dict[str, Any]) -> None:
        """Log a performance entry to file"""
        self.core.log_performance(log_entry)


# Global instance
performance_monitor = PerformanceMonitorAdapter()

def get_performance_monitor() -> PerformanceMonitorAdapter:
    return performance_monitor
