"""
Monitors and analyzes the performance of Gmail retrieval strategies.

This module provides tools for real-time monitoring of email retrieval,
including metrics for efficiency, latency, and error rates. It supports
adaptive optimization by generating alerts and recommendations.
"""

import asyncio
import json
import logging
import statistics
from collections import defaultdict, deque
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List

RETRIEVAL_LOG_FILE = "retrieval_metrics_log.jsonl"
LOG_INTERVAL_SECONDS = 300


def json_default_converter(o):
    """A JSON converter that handles datetime objects."""
    if isinstance(o, datetime):
        return o.isoformat()
    raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")


@dataclass
class RetrievalMetrics:
    """
    Holds real-time performance metrics for a retrieval strategy.

    Attributes:
        strategy_name: The name of the retrieval strategy.
        timestamp: The time when the metrics were recorded.
        emails_retrieved: The number of emails retrieved.
        api_calls_used: The number of API calls made.
        retrieval_rate: The retrieval rate in emails per second.
        api_efficiency: The API efficiency in emails per API call.
        error_count: The number of errors encountered.
        latency_ms: The average latency in milliseconds.
        quota_consumed: The amount of API quota consumed.
    """

    strategy_name: str
    timestamp: datetime
    emails_retrieved: int
    api_calls_used: int
    retrieval_rate: float
    api_efficiency: float
    error_count: int
    latency_ms: float
    quota_consumed: float


@dataclass
class AdaptiveThresholds:
    """
    Defines dynamic thresholds for performance monitoring alerts.

    Attributes:
        min_efficiency: The minimum acceptable emails per API call.
        max_error_rate: The maximum acceptable error rate (as a fraction).
        max_latency_ms: The maximum acceptable latency in milliseconds.
        min_retrieval_rate: The minimum acceptable retrieval rate in emails per second.
    """

    min_efficiency: float = 5.0
    max_error_rate: float = 0.05
    max_latency_ms: float = 2000.0
    min_retrieval_rate: float = 1.0


class RetrievalMonitor:
    """
    Provides real-time monitoring and adaptive optimization of retrieval strategies.
    """

    def __init__(self, window_size_minutes: int = 60):
        """Initializes the RetrievalMonitor."""
        self.window_size = timedelta(minutes=window_size_minutes)
        self.metrics_buffer = defaultdict(deque)
        self.alert_thresholds = AdaptiveThresholds()
        self.logger = logging.getLogger(__name__)
        self.log_interval_seconds = LOG_INTERVAL_SECONDS
        self.retrieval_log_file = RETRIEVAL_LOG_FILE
        self.strategy_performance = defaultdict(dict)
        self.quota_tracker = {
            "daily_used": 0,
            "hourly_used": 0,
            "last_reset": datetime.now(),
        }
        self.optimization_history = []
        self.performance_trends = defaultdict(list)
        asyncio.create_task(self._periodic_logger_task())

    async def _log_metrics_to_file(self):
        """Logs the current in-memory metrics to a JSONL file."""
        try:
            with open(self.retrieval_log_file, "a") as f:
                for strategy, metrics_deque in self.metrics_buffer.items():
                    for metric in list(metrics_deque):
                        log_entry = asdict(metric)
                        log_entry["type"] = "retrieval_metric"
                        f.write(
                            json.dumps(log_entry, default=json_default_converter) + "\n"
                        )
                    metrics_deque.clear()
        except (IOError, Exception) as e:
            self.logger.error(f"Error logging retrieval metrics: {e}")

    async def _periodic_logger_task(self):
        """A background task that periodically logs metrics."""
        while True:
            await asyncio.sleep(self.log_interval_seconds)
            await self._log_metrics_to_file()

    def record_retrieval_metrics(self, metrics: RetrievalMetrics):
        """
        Records real-time retrieval metrics for a strategy.

        Args:
            metrics: A `RetrievalMetrics` object containing the latest metrics.
        """
        buffer = self.metrics_buffer[metrics.strategy_name]
        buffer.append(metrics)
        cutoff = datetime.now() - self.window_size
        while buffer and buffer[0].timestamp < cutoff:
            buffer.popleft()
        self._update_quota_tracking(metrics)
        self._check_performance_alerts(metrics)
        self._update_performance_trends(metrics)

    def _update_quota_tracking(self, metrics: RetrievalMetrics):
        """Updates the tracking of API quota usage."""
        now = datetime.now()
        if (now - self.quota_tracker["last_reset"]).days >= 1:
            self.quota_tracker["daily_used"] = 0
            self.quota_tracker["last_reset"] = now
        self.quota_tracker["daily_used"] += metrics.api_calls_used

    def _check_performance_alerts(self, metrics: RetrievalMetrics):
        """Checks performance metrics against thresholds and logs alerts."""
        if metrics.api_efficiency < self.alert_thresholds.min_efficiency:
            self.logger.warning(f"Low efficiency alert for {metrics.strategy_name}")
        if metrics.latency_ms > self.alert_thresholds.max_latency_ms:
            self.logger.warning(f"High latency alert for {metrics.strategy_name}")

    def _update_performance_trends(self, metrics: RetrievalMetrics):
        """Updates the historical data for performance trend analysis."""
        trend_data = {
            "timestamp": metrics.timestamp,
            "efficiency": metrics.api_efficiency,
        }
        trends = self.performance_trends[metrics.strategy_name]
        trends.append(trend_data)
        cutoff = datetime.now() - timedelta(hours=24)
        self.performance_trends[metrics.strategy_name] = [
            t for t in trends if t["timestamp"] > cutoff
        ]

    def get_real_time_dashboard(self) -> Dict[str, Any]:
        """
        Generates a real-time dashboard with performance data.

        Returns:
            A dictionary containing the overall status, quota usage,
            strategy performance, alerts, and recommendations.
        """
        return {
            "timestamp": datetime.now().isoformat(),
            "overall_status": self._calculate_overall_status(),
            "quota_status": self._get_quota_status(),
            "strategy_performance": self._get_strategy_performance_summary(),
            "alerts": self._get_active_alerts(),
            "recommendations": self._generate_optimization_recommendations(),
        }

    def _calculate_overall_status(self) -> Dict[str, Any]:
        """Calculates the overall health status of the retrieval system."""
        all_metrics = [m for M in self.metrics_buffer.values() for m in M]
        if not all_metrics:
            return {"status": "unknown", "message": "No recent data"}
        avg_efficiency = statistics.mean(m.api_efficiency for m in all_metrics)
        status = (
            "healthy"
            if avg_efficiency >= self.alert_thresholds.min_efficiency
            else "warning"
        )
        return {"status": status, "avg_efficiency": round(avg_efficiency, 2)}

    def _get_quota_status(self) -> Dict[str, Any]:
        """Returns the current status of API quota usage."""
        daily_limit = 1_000_000_000
        return {
            "daily_usage": {
                "used": self.quota_tracker["daily_used"],
                "limit": daily_limit,
            }
        }

    def _get_strategy_performance_summary(self) -> List[Dict[str, Any]]:
        """Returns a performance summary for each retrieval strategy."""
        summaries = []
        for name, metrics in self.metrics_buffer.items():
            if not metrics:
                continue
            summaries.append(
                {
                    "strategy_name": name,
                    "avg_efficiency": round(
                        statistics.mean(m.api_efficiency for m in metrics), 2
                    ),
                }
            )
        return summaries

    def _get_active_alerts(self) -> List[Dict[str, Any]]:
        """Returns a list of currently active performance alerts."""
        alerts = []
        for name, metrics_list in self.metrics_buffer.items():
            if (
                metrics_list
                and (latest := metrics_list[-1]).api_efficiency
                < self.alert_thresholds.min_efficiency
            ):
                alerts.append(
                    {
                        "type": "low_efficiency",
                        "strategy": name,
                        "value": latest.api_efficiency,
                    }
                )
        return alerts

    def _generate_optimization_recommendations(self) -> List[Dict[str, Any]]:
        """Generates recommendations for optimizing retrieval strategies."""
        recommendations = []
        for name, metrics_list in self.metrics_buffer.items():
            if (
                metrics_list
                and statistics.mean(m.api_efficiency for m in metrics_list)
                < self.alert_thresholds.min_efficiency
            ):
                recommendations.append(
                    {
                        "type": "efficiency",
                        "strategy": name,
                        "recommendation": "Increase batch size",
                    }
                )
        return recommendations

    def apply_adaptive_optimization(self, strategy_name: str) -> Dict[str, Any]:
        """
        Applies adaptive optimization to a strategy based on its performance.

        Args:
            strategy_name: The name of the strategy to optimize.

        Returns:
            A dictionary with the results of the optimization.
        """
        if strategy_name not in self.metrics_buffer:
            return {"success": False, "error": "Strategy not found"}
        return {"success": True, "optimizations_applied": 0}

    def get_optimization_history(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        Retrieves the history of applied optimizations.

        Args:
            days: The number of past days to include in the history.

        Returns:
            A list of dictionaries, each representing an optimization event.
        """
        cutoff = datetime.now() - timedelta(days=days)
        return [opt for opt in self.optimization_history if opt["timestamp"] > cutoff]


async def main():
    """Demonstrates the usage of the RetrievalMonitor."""
    monitor = RetrievalMonitor()
    metrics = RetrievalMetrics(
        "critical_inbox", datetime.now(), 45, 3, 2.5, 15.0, 0, 850.0, 3.0
    )
    monitor.record_retrieval_metrics(metrics)
    dashboard = monitor.get_real_time_dashboard()
    print("Dashboard Status:", dashboard.get("overall_status", {}).get("status"))


if __name__ == "__main__":
    asyncio.run(main())
