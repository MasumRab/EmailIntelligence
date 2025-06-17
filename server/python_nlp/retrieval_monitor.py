"""
Retrieval Monitoring and Performance Analytics
Real-time monitoring of Gmail retrieval strategies with adaptive optimization
"""

import asyncio
import json
import logging
import statistics
from collections import defaultdict, deque
from dataclasses import asdict, dataclass
# Added imports:
from datetime import datetime  # Ensure datetime is directly available
from datetime import timedelta
from typing import Any, Dict, List

RETRIEVAL_LOG_FILE = "retrieval_metrics_log.jsonl"
LOG_INTERVAL_SECONDS = 300


def json_default_converter(o):
    if isinstance(o, datetime):
        return o.isoformat()
    raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")


@dataclass
class RetrievalMetrics:
    """Real-time retrieval performance metrics"""

    strategy_name: str
    timestamp: datetime
    emails_retrieved: int
    api_calls_used: int
    retrieval_rate: float  # emails per second
    api_efficiency: float  # emails per API call
    error_count: int
    latency_ms: float
    quota_consumed: float


@dataclass
class AdaptiveThresholds:
    """Dynamic thresholds for performance monitoring"""

    min_efficiency: float = 5.0  # min emails per API call
    max_error_rate: float = 0.05  # 5% error rate
    max_latency_ms: float = 2000.0  # 2 seconds
    min_retrieval_rate: float = 1.0  # emails per second


class RetrievalMonitor:
    """Real-time monitoring and adaptive optimization of retrieval strategies"""

    def __init__(self, window_size_minutes: int = 60):
        self.window_size = timedelta(minutes=window_size_minutes)
        self.metrics_buffer = defaultdict(deque)
        self.alert_thresholds = AdaptiveThresholds()
        self.logger = logging.getLogger(__name__)
        self.LOG_INTERVAL_SECONDS = LOG_INTERVAL_SECONDS  # Make it instance variable
        self.RETRIEVAL_LOG_FILE = RETRIEVAL_LOG_FILE

        # Performance tracking
        self.strategy_performance = defaultdict(dict)
        self.quota_tracker = {
            "daily_used": 0,
            "hourly_used": 0,
            "last_reset": datetime.now(),
        }

        # Adaptive optimization state
        self.optimization_history = []
        self.performance_trends = defaultdict(list)

        # Start periodic file logging task
        asyncio.create_task(self._periodic_logger_task())

    async def _log_metrics_to_file(self):
        """Logs current in-memory retrieval metrics to a JSONL file and clears buffers."""
        logged_anything = False
        try:
            with open(self.RETRIEVAL_LOG_FILE, "a") as f:
                metrics_buffer_copy = self.metrics_buffer.copy()  # Shallow copy of dict

                for strategy_name, metrics_deque in metrics_buffer_copy.items():
                    current_deque_copy = list(
                        metrics_deque
                    )  # Copy of the deque for this strategy
                    if not current_deque_copy:
                        continue

                    for metric_obj in current_deque_copy:
                        log_entry = asdict(metric_obj)
                        log_entry["type"] = "retrieval_metric"
                        # strategy_name is already in RetrievalMetrics dataclass, but good to have consistently
                        log_entry["strategy_name_key"] = strategy_name
                        log_entry["timestamp_logged"] = datetime.now().isoformat()
                        f.write(
                            json.dumps(log_entry, default=json_default_converter) + "\n"
                        )

                    # Clear the original deque for this strategy after its contents are written
                    self.metrics_buffer[strategy_name].clear()
                    logged_anything = True

            if logged_anything:
                self.logger.info(
                    f"Successfully logged retrieval metrics to {self.RETRIEVAL_LOG_FILE}"
                )

        except IOError as e:
            self.logger.error(
                f"IOError writing retrieval metrics to {self.RETRIEVAL_LOG_FILE}: {e}"
            )
        except Exception as e:
            self.logger.error(
                f"Unexpected error logging retrieval metrics to file: {e}"
            )

    async def _periodic_logger_task(self):
        """Periodically logs metrics to a file."""
        while True:
            try:
                await asyncio.sleep(self.LOG_INTERVAL_SECONDS)
                self.logger.info("Periodic retrieval logger task triggered.")
                await self._log_metrics_to_file()
            except asyncio.CancelledError:
                self.logger.info("Periodic retrieval logger task cancelled.")
                break
            except Exception as e:
                self.logger.error(f"Error in periodic retrieval logger task: {e}")
                await asyncio.sleep(
                    self.LOG_INTERVAL_SECONDS / 2
                )  # Shorter sleep on error

    def record_retrieval_metrics(self, metrics: RetrievalMetrics):
        """Record real-time retrieval metrics"""
        strategy_buffer = self.metrics_buffer[metrics.strategy_name]
        strategy_buffer.append(metrics)

        # Maintain sliding window
        cutoff_time = datetime.now() - self.window_size
        while strategy_buffer and strategy_buffer[0].timestamp < cutoff_time:
            strategy_buffer.popleft()

        # Update quota tracking
        self._update_quota_tracking(metrics)

        # Check for performance alerts
        self._check_performance_alerts(metrics)

        # Update performance trends
        self._update_performance_trends(metrics)

    def _update_quota_tracking(self, metrics: RetrievalMetrics):
        """Update API quota usage tracking"""
        now = datetime.now()

        # Reset counters if needed
        if (now - self.quota_tracker["last_reset"]).days >= 1:
            self.quota_tracker["daily_used"] = 0
            self.quota_tracker["last_reset"] = now

        if (now - self.quota_tracker["last_reset"]).seconds >= 3600:
            self.quota_tracker["hourly_used"] = 0

        # Update usage
        self.quota_tracker["daily_used"] += metrics.api_calls_used
        self.quota_tracker["hourly_used"] += metrics.api_calls_used

    def _check_performance_alerts(self, metrics: RetrievalMetrics):
        """Check for performance issues and generate alerts"""
        alerts = []

        # Low efficiency alert
        if metrics.api_efficiency < self.alert_thresholds.min_efficiency:
            alerts.append(
                {
                    "type": "low_efficiency",
                    "strategy": metrics.strategy_name,
                    "current_value": metrics.api_efficiency,
                    "threshold": self.alert_thresholds.min_efficiency,
                    "severity": "warning",
                }
            )

        # High latency alert
        if metrics.latency_ms > self.alert_thresholds.max_latency_ms:
            alerts.append(
                {
                    "type": "high_latency",
                    "strategy": metrics.strategy_name,
                    "current_value": metrics.latency_ms,
                    "threshold": self.alert_thresholds.max_latency_ms,
                    "severity": "warning",
                }
            )

        # Error rate check (calculated over recent window)
        recent_metrics = list(self.metrics_buffer[metrics.strategy_name])
        if len(recent_metrics) >= 5:
            error_rate = sum(
                1 for m in recent_metrics[-10:] if m.error_count > 0
            ) / min(10, len(recent_metrics))
            if error_rate > self.alert_thresholds.max_error_rate:
                alerts.append(
                    {
                        "type": "high_error_rate",
                        "strategy": metrics.strategy_name,
                        "current_value": error_rate,
                        "threshold": self.alert_thresholds.max_error_rate,
                        "severity": "critical",
                    }
                )

        # Log alerts
        for alert in alerts:
            self.logger.warning(f"Performance alert: {alert}")

    def _update_performance_trends(self, metrics: RetrievalMetrics):
        """Update performance trend analysis"""
        trend_data = {
            "timestamp": metrics.timestamp,
            "efficiency": metrics.api_efficiency,
            "latency": metrics.latency_ms,
            "retrieval_rate": metrics.retrieval_rate,
            "error_count": metrics.error_count,
        }

        trends = self.performance_trends[metrics.strategy_name]
        trends.append(trend_data)

        # Keep only recent trend data (last 24 hours)
        cutoff = datetime.now() - timedelta(hours=24)
        self.performance_trends[metrics.strategy_name] = [
            t for t in trends if t["timestamp"] > cutoff
        ]

    def get_real_time_dashboard(self) -> Dict[str, Any]:
        """Generate real-time monitoring dashboard data"""
        dashboard = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": self._calculate_overall_status(),
            "quota_status": self._get_quota_status(),
            "strategy_performance": self._get_strategy_performance_summary(),
            "alerts": self._get_active_alerts(),
            "performance_trends": self._get_performance_trends_summary(),
            "recommendations": self._generate_optimization_recommendations(),
        }

        return dashboard

    def _calculate_overall_status(self) -> Dict[str, Any]:
        """Calculate overall system health status"""
        all_metrics = []
        for strategy_metrics in self.metrics_buffer.values():
            all_metrics.extend(list(strategy_metrics))

        if not all_metrics:
            return {"status": "unknown", "message": "No recent data"}

        # Calculate aggregate metrics
        avg_efficiency = statistics.mean(m.api_efficiency for m in all_metrics)
        avg_latency = statistics.mean(m.latency_ms for m in all_metrics)
        total_errors = sum(m.error_count for m in all_metrics)
        error_rate = total_errors / len(all_metrics) if all_metrics else 0

        # Determine status
        if (
            avg_efficiency >= self.alert_thresholds.min_efficiency
            and avg_latency <= self.alert_thresholds.max_latency_ms
            and error_rate <= self.alert_thresholds.max_error_rate
        ):
            status = "healthy"
        elif error_rate > self.alert_thresholds.max_error_rate * 2:
            status = "critical"
        else:
            status = "warning"

        return {
            "status": status,
            "avg_efficiency": round(avg_efficiency, 2),
            "avg_latency_ms": round(avg_latency, 2),
            "error_rate": round(error_rate * 100, 2),
            "total_strategies": len(self.metrics_buffer),
            "active_strategies": len([s for s in self.metrics_buffer.values() if s]),
        }

    def _get_quota_status(self) -> Dict[str, Any]:
        """Get current API quota usage status"""
        daily_limit = 1000000000  # 1 billion per day
        hourly_limit = 250  # 250 per 100 seconds, scaled to hourly

        return {
            "daily_usage": {
                "used": self.quota_tracker["daily_used"],
                "limit": daily_limit,
                "percentage": (self.quota_tracker["daily_used"] / daily_limit) * 100,
                "remaining": daily_limit - self.quota_tracker["daily_used"],
            },
            "hourly_usage": {
                "used": self.quota_tracker["hourly_used"],
                "limit": hourly_limit,
                "percentage": (self.quota_tracker["hourly_used"] / hourly_limit) * 100,
                "remaining": hourly_limit - self.quota_tracker["hourly_used"],
            },
            "projected_daily_usage": self._project_daily_usage(),
        }

    def _project_daily_usage(self) -> float:
        """Project daily usage based on current hourly rate"""
        current_hour = datetime.now().hour
        if current_hour == 0:
            return self.quota_tracker["hourly_used"] * 24

        hourly_average = self.quota_tracker["daily_used"] / current_hour
        return hourly_average * 24

    def _get_strategy_performance_summary(self) -> List[Dict[str, Any]]:
        """Get performance summary for each strategy"""
        summaries = []

        for strategy_name, metrics_list in self.metrics_buffer.items():
            if not metrics_list:
                continue

            recent_metrics = list(metrics_list)

            # Calculate summary statistics
            total_emails = sum(m.emails_retrieved for m in recent_metrics)
            total_api_calls = sum(m.api_calls_used for m in recent_metrics)
            avg_efficiency = statistics.mean(m.api_efficiency for m in recent_metrics)
            avg_latency = statistics.mean(m.latency_ms for m in recent_metrics)
            total_errors = sum(m.error_count for m in recent_metrics)

            # Performance score (0-100)
            efficiency_score = min(100, (avg_efficiency / 10) * 100)
            latency_score = max(0, 100 - (avg_latency / 20))
            error_score = max(0, 100 - (total_errors * 10))
            overall_score = (efficiency_score + latency_score + error_score) / 3

            summaries.append(
                {
                    "strategy_name": strategy_name,
                    "total_emails_retrieved": total_emails,
                    "total_api_calls": total_api_calls,
                    "avg_efficiency": round(avg_efficiency, 2),
                    "avg_latency_ms": round(avg_latency, 2),
                    "total_errors": total_errors,
                    "performance_score": round(overall_score, 1),
                    "last_execution": (
                        recent_metrics[-1].timestamp.isoformat()
                        if recent_metrics
                        else None
                    ),
                    "trend": self._calculate_performance_trend(strategy_name),
                }
            )

        return sorted(summaries, key=lambda x: x["performance_score"], reverse=True)

    def _calculate_performance_trend(self, strategy_name: str) -> str:
        """Calculate performance trend (improving, stable, declining)"""
        trends = self.performance_trends.get(strategy_name, [])
        if len(trends) < 2:
            return "stable"

        # Compare recent performance with earlier performance
        recent_efficiency = statistics.mean([t["efficiency"] for t in trends[-5:]])
        earlier_efficiency = statistics.mean([t["efficiency"] for t in trends[:5]])

        if recent_efficiency > earlier_efficiency * 1.1:
            return "improving"
        elif recent_efficiency < earlier_efficiency * 0.9:
            return "declining"
        else:
            return "stable"

    def _get_active_alerts(self) -> List[Dict[str, Any]]:
        """Get currently active performance alerts"""
        alerts = []

        for strategy_name, metrics_list in self.metrics_buffer.items():
            if not metrics_list:
                continue

            latest_metrics = list(metrics_list)[-1]

            # Check each alert condition
            if latest_metrics.api_efficiency < self.alert_thresholds.min_efficiency:
                alerts.append(
                    {
                        "type": "low_efficiency",
                        "strategy": strategy_name,
                        "message": f"Efficiency below threshold: {latest_metrics.api_efficiency:.1f} < {self.alert_thresholds.min_efficiency}",
                        "severity": "warning",
                        "timestamp": latest_metrics.timestamp.isoformat(),
                    }
                )

            if latest_metrics.latency_ms > self.alert_thresholds.max_latency_ms:
                alerts.append(
                    {
                        "type": "high_latency",
                        "strategy": strategy_name,
                        "message": f"High latency detected: {latest_metrics.latency_ms:.0f}ms > {self.alert_thresholds.max_latency_ms}ms",
                        "severity": "warning",
                        "timestamp": latest_metrics.timestamp.isoformat(),
                    }
                )

        return sorted(alerts, key=lambda x: x["timestamp"], reverse=True)

    def _get_performance_trends_summary(self) -> Dict[str, Any]:
        """Get summary of performance trends across strategies"""
        all_trends = []
        for trends in self.performance_trends.values():
            all_trends.extend(trends)

        if not all_trends:
            return {"status": "no_data"}

        # Group by time periods
        now = datetime.now()
        last_hour = [t for t in all_trends if (now - t["timestamp"]).seconds < 3600]
        last_day = [t for t in all_trends if (now - t["timestamp"]).days < 1]

        return {
            "last_hour": {
                "avg_efficiency": (
                    statistics.mean([t["efficiency"] for t in last_hour])
                    if last_hour
                    else 0
                ),
                "avg_latency": (
                    statistics.mean([t["latency"] for t in last_hour])
                    if last_hour
                    else 0
                ),
                "total_errors": sum([t["error_count"] for t in last_hour]),
            },
            "last_24_hours": {
                "avg_efficiency": (
                    statistics.mean([t["efficiency"] for t in last_day])
                    if last_day
                    else 0
                ),
                "avg_latency": (
                    statistics.mean([t["latency"] for t in last_day]) if last_day else 0
                ),
                "total_errors": sum([t["error_count"] for t in last_day]),
            },
            "trend_direction": self._calculate_overall_trend(),
        }

    def _calculate_overall_trend(self) -> str:
        """Calculate overall system performance trend"""
        all_efficiencies = []
        for trends in self.performance_trends.values():
            all_efficiencies.extend([t["efficiency"] for t in trends])

        if len(all_efficiencies) < 10:
            return "stable"

        # Simple trend analysis using first and last quartiles
        first_quarter = all_efficiencies[: len(all_efficiencies) // 4]
        last_quarter = all_efficiencies[-len(all_efficiencies) // 4 :]

        first_avg = statistics.mean(first_quarter)
        last_avg = statistics.mean(last_quarter)

        if last_avg > first_avg * 1.1:
            return "improving"
        elif last_avg < first_avg * 0.9:
            return "declining"
        else:
            return "stable"

    def _generate_optimization_recommendations(self) -> List[Dict[str, Any]]:
        """Generate adaptive optimization recommendations"""
        recommendations = []

        # Analyze each strategy for optimization opportunities
        for strategy_name, metrics_list in self.metrics_buffer.items():
            if not metrics_list:
                continue

            recent_metrics = list(metrics_list)
            avg_efficiency = statistics.mean(m.api_efficiency for m in recent_metrics)
            avg_latency = statistics.mean(m.latency_ms for m in recent_metrics)
            error_count = sum(m.error_count for m in recent_metrics)

            # Low efficiency recommendations
            if avg_efficiency < self.alert_thresholds.min_efficiency:
                recommendations.append(
                    {
                        "type": "efficiency_optimization",
                        "strategy": strategy_name,
                        "priority": "high",
                        "recommendation": "Increase batch size or optimize query filters",
                        "expected_improvement": "20-40% efficiency gain",
                        "action": "increase_batch_size",
                    }
                )

            # High latency recommendations
            if avg_latency > self.alert_thresholds.max_latency_ms:
                recommendations.append(
                    {
                        "type": "latency_optimization",
                        "strategy": strategy_name,
                        "priority": "medium",
                        "recommendation": "Reduce batch size or add request delays",
                        "expected_improvement": "30-50% latency reduction",
                        "action": "reduce_batch_size",
                    }
                )

            # Error reduction recommendations
            if error_count > 0:
                recommendations.append(
                    {
                        "type": "error_reduction",
                        "strategy": strategy_name,
                        "priority": "high",
                        "recommendation": "Implement exponential backoff or filter adjustment",
                        "expected_improvement": "80-95% error reduction",
                        "action": "add_backoff_strategy",
                    }
                )

        # Quota optimization recommendations
        quota_status = self._get_quota_status()
        if quota_status["daily_usage"]["percentage"] > 80:
            recommendations.append(
                {
                    "type": "quota_optimization",
                    "strategy": "global",
                    "priority": "critical",
                    "recommendation": "Reduce retrieval frequency or implement intelligent scheduling",
                    "expected_improvement": "20-30% quota savings",
                    "action": "reduce_frequency",
                }
            )

        return sorted(
            recommendations,
            key=lambda x: {"critical": 3, "high": 2, "medium": 1, "low": 0}[
                x["priority"]
            ],
            reverse=True,
        )

    def apply_adaptive_optimization(self, strategy_name: str) -> Dict[str, Any]:
        """Apply adaptive optimization based on performance metrics"""
        if strategy_name not in self.metrics_buffer:
            return {"success": False, "error": "Strategy not found"}

        recent_metrics = list(self.metrics_buffer[strategy_name])
        if not recent_metrics:
            return {"success": False, "error": "No metrics available"}

        # Calculate optimization parameters
        avg_efficiency = statistics.mean(m.api_efficiency for m in recent_metrics)
        avg_latency = statistics.mean(m.latency_ms for m in recent_metrics)
        error_rate = sum(m.error_count for m in recent_metrics) / len(recent_metrics)

        optimizations = []

        # Efficiency-based optimizations
        if avg_efficiency < 3:
            optimizations.append(
                {
                    "parameter": "batch_size",
                    "action": "increase",
                    "factor": 1.5,
                    "reason": "Low efficiency detected",
                }
            )
        elif avg_efficiency > 15:
            optimizations.append(
                {
                    "parameter": "batch_size",
                    "action": "increase",
                    "factor": 1.2,
                    "reason": "High efficiency - can handle larger batches",
                }
            )

        # Latency-based optimizations
        if avg_latency > 2000:
            optimizations.append(
                {
                    "parameter": "batch_size",
                    "action": "decrease",
                    "factor": 0.8,
                    "reason": "High latency detected",
                }
            )
            optimizations.append(
                {
                    "parameter": "request_delay",
                    "action": "increase",
                    "factor": 1.3,
                    "reason": "Add delay to reduce server load",
                }
            )

        # Error-based optimizations
        if error_rate > 0.1:
            optimizations.append(
                {
                    "parameter": "retry_strategy",
                    "action": "enable",
                    "factor": 1.0,
                    "reason": "High error rate - implement exponential backoff",
                }
            )

        # Record optimization in history
        optimization_record = {
            "timestamp": datetime.now(),
            "strategy_name": strategy_name,
            "optimizations": optimizations,
            "baseline_metrics": {
                "efficiency": avg_efficiency,
                "latency": avg_latency,
                "error_rate": error_rate,
            },
        }

        self.optimization_history.append(optimization_record)

        return {
            "success": True,
            "optimizations_applied": len(optimizations),
            "optimizations": optimizations,
            "baseline_metrics": optimization_record["baseline_metrics"],
        }

    def get_optimization_history(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get optimization history for analysis"""
        cutoff = datetime.now() - timedelta(days=days)

        recent_optimizations = [
            opt for opt in self.optimization_history if opt["timestamp"] > cutoff
        ]

        return recent_optimizations


async def main():
    """Example usage of retrieval monitor"""
    monitor = RetrievalMonitor()

    # Simulate some metrics
    test_metrics = [
        RetrievalMetrics(
            strategy_name="critical_inbox",
            timestamp=datetime.now(),
            emails_retrieved=45,
            api_calls_used=3,
            retrieval_rate=2.5,
            api_efficiency=15.0,
            error_count=0,
            latency_ms=850.0,
            quota_consumed=3.0,
        ),
        RetrievalMetrics(
            strategy_name="personal_daily",
            timestamp=datetime.now(),
            emails_retrieved=120,
            api_calls_used=12,
            retrieval_rate=1.8,
            api_efficiency=10.0,
            error_count=1,
            latency_ms=1200.0,
            quota_consumed=12.0,
        ),
    ]

    # Record metrics
    for metrics in test_metrics:
        monitor.record_retrieval_metrics(metrics)

    # Get dashboard
    dashboard = monitor.get_real_time_dashboard()
    print("Dashboard Status:", dashboard["overall_status"]["status"])
    print("Active Strategies:", dashboard["overall_status"]["active_strategies"])
    print("Recommendations:", len(dashboard["recommendations"]))

    # Apply optimization
    optimization_result = monitor.apply_adaptive_optimization("critical_inbox")
    print("Optimization Applied:", optimization_result["success"])
    if optimization_result["success"]:
        print("Optimizations:", len(optimization_result["optimizations"]))


if __name__ == "__main__":
    asyncio.run(main())
