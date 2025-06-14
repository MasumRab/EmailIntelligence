"""
Performance Monitor for Gmail AI Email Management
Real-time performance tracking and optimization
"""
import asyncio
import time
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict, deque
import json
import psutil
# import sqlite3 # Removed SQLite
from dataclasses import dataclass, field, asdict # Added dataclass and field
from datetime import datetime # Ensure datetime is directly available

logger = logging.getLogger(__name__)

PERFORMANCE_LOG_FILE = "performance_metrics_log.jsonl"
LOG_INTERVAL_SECONDS = 300

def json_default_converter(o):
    if isinstance(o, datetime):
        return o.isoformat()
    raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")

# dataclasses remain the same

@dataclass
class PerformanceMetric:
    """Performance metric data point"""
    timestamp: datetime
    metric_name: str
    value: float
    tags: Dict[str, str]
    metadata: Dict[str, Any]

@dataclass
class SystemHealth:
    """System health status"""
    timestamp: datetime # Added timestamp to SystemHealth for logging
    status: str  # healthy, warning, critical
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    process_count: int
    uptime: float

class PerformanceMonitor:
    """Performance monitoring for email processing (In-memory version)"""

    def __init__(self): # Removed db_path
        self.metrics_history = defaultdict(deque)
        # self.performance_data = {} # This was not used, can be removed
        self.alert_thresholds = {
            'processing_time': 5.0,  # seconds # This specific key is not used in _check_alerts
            'error_rate': 0.1,       # 10% # This specific key is not used in _check_alerts
            # 'memory_usage': 0.8,     # 80% # This is covered by system health alert thresholds
            "cpu_usage": 80.0,       # Used by system health and _check_alerts if metric 'cpu_usage' recorded
            "memory_usage": 85.0,    # Used by system health and _check_alerts if metric 'memory_usage' recorded
            "disk_usage": 90.0,      # Used by system health
            "response_time": 5000.0, # milliseconds # Used by _check_alerts
            # "error_rate": 10.0     # percentage # This is covered by email processing error rate
        }
        # self.db_path = db_path # Removed
        self.metrics_buffer = deque(maxlen=1000) # In-memory buffer for metrics
        self.alerts_buffer = deque(maxlen=100) # In-memory buffer for alerts
        self.system_health_history = deque(maxlen=100) # In-memory for system health
        # self.service_metrics = defaultdict(list) # This was not used, can be removed
        # self.init_database() # Removed SQLite database initialization
        logger.info("PerformanceMonitor initialized (in-memory mode with file logging).")
        self.LOG_INTERVAL_SECONDS = LOG_INTERVAL_SECONDS # Make it instance variable for potential override
        self.PERFORMANCE_LOG_FILE = PERFORMANCE_LOG_FILE

        # Start periodic file logging task
        asyncio.create_task(self._periodic_logger_task())

    async def _log_metrics_to_file(self):
        """Logs current in-memory metrics, alerts, and system health to a JSONL file and clears buffers."""
        logged_anything = False
        try:
            with open(self.PERFORMANCE_LOG_FILE, 'a') as f:
                # Log PerformanceMetrics
                current_metrics_buffer_copy = list(self.metrics_buffer)
                if current_metrics_buffer_copy:
                    for metric in current_metrics_buffer_copy:
                        log_entry = asdict(metric)
                        log_entry['type'] = 'performance_metric'
                        log_entry['timestamp_logged'] = datetime.now().isoformat()
                        f.write(json.dumps(log_entry, default=json_default_converter) + '\n')
                    self.metrics_buffer.clear() # Clear after successful write
                    logged_anything = True

                # Log Alerts
                current_alerts_buffer_copy = list(self.alerts_buffer)
                if current_alerts_buffer_copy:
                    for alert in current_alerts_buffer_copy: # Alerts are already dicts
                        log_entry = alert.copy() # Make a copy before modifying
                        log_entry['type'] = 'alert'
                        log_entry['timestamp_logged'] = datetime.now().isoformat()
                        f.write(json.dumps(log_entry, default=json_default_converter) + '\n')
                    self.alerts_buffer.clear() # Clear after successful write
                    logged_anything = True

                # Log SystemHealth
                current_system_health_history_copy = list(self.system_health_history)
                if current_system_health_history_copy:
                    for health_record in current_system_health_history_copy:
                        log_entry = asdict(health_record)
                        log_entry['type'] = 'system_health'
                        log_entry['timestamp_logged'] = datetime.now().isoformat()
                        f.write(json.dumps(log_entry, default=json_default_converter) + '\n')
                    self.system_health_history.clear() # Clear after successful write
                    logged_anything = True

            if logged_anything:
                 logger.info(f"Successfully logged performance data to {self.PERFORMANCE_LOG_FILE}")

        except IOError as e:
            logger.error(f"IOError writing performance metrics to {self.PERFORMANCE_LOG_FILE}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error logging performance metrics to file: {e}")

    async def _periodic_logger_task(self):
        """Periodically logs metrics to a file."""
        while True:
            try:
                await asyncio.sleep(self.LOG_INTERVAL_SECONDS)
                logger.info("Periodic logger task triggered.")
                await self._log_metrics_to_file()
            except asyncio.CancelledError:
                logger.info("Periodic logger task cancelled.")
                break
            except Exception as e:
                logger.error(f"Error in periodic logger task: {e}")
                # Continue loop even if one attempt fails, but maybe sleep a bit longer
                await asyncio.sleep(self.LOG_INTERVAL_SECONDS / 2) # Shorter sleep on error before retry

    # init_database method removed as SQLite is no longer used.

    async def record_email_processing(
        self,
        email_id: int,
        ai_analysis: Any,
        filter_results: Dict[str, Any]
    ):
        """Record email processing metrics"""
        try:
            processing_time = time.time()

            # Record processing metrics
            self.metrics_history['email_processing'].append({
                'email_id': email_id,
                'timestamp': processing_time,
                'ai_confidence': getattr(ai_analysis, 'confidence', 0),
                'filters_applied': len(filter_results.get('applied_filters', [])),
                'processing_success': True
            })

            # Keep only recent metrics (last 1000 entries)
            if len(self.metrics_history['email_processing']) > 1000:
                self.metrics_history['email_processing'].popleft()

        except Exception as e:
            logger.error(f"Failed to record email processing metrics: {e}")

    async def record_sync_performance(self, sync_result: Dict[str, Any]):
        """Record Gmail sync performance"""
        try:
            self.metrics_history['sync_performance'].append({
                'timestamp': time.time(),
                'success': sync_result.get('success', False),
                'processed_count': sync_result.get('processedCount', 0),
                'errors_count': sync_result.get('errorsCount', 0),
                'processing_time': sync_result.get('processingTime', 0)
            })

            # Keep only recent metrics
            if len(self.metrics_history['sync_performance']) > 100:
                self.metrics_history['sync_performance'].popleft()

        except Exception as e:
            logger.error(f"Failed to record sync performance: {e}")

    async def get_real_time_dashboard(self) -> Dict[str, Any]:
        """Get real-time performance dashboard data"""
        try:
            current_time = time.time()

            # Calculate recent performance metrics
            recent_emails = [
                m for m in self.metrics_history['email_processing']
                if current_time - m['timestamp'] < 3600  # Last hour
            ]

            recent_syncs = [
                m for m in self.metrics_history['sync_performance']
                if current_time - m['timestamp'] < 3600  # Last hour
            ]

            # Performance calculations
            avg_processing_time = 0.5  # Default fallback
            success_rate = 1.0

            if recent_emails:
                success_rate = sum(1 for m in recent_emails if m['processing_success']) / len(recent_emails)

            return {
                "timestamp": datetime.now().isoformat(),
                "overallStatus": {
                    "status": "healthy" if success_rate > 0.9 else "degraded",
                    "avgProcessingTime": avg_processing_time,
                    "successRate": success_rate,
                    "activeStrategies": len(recent_syncs)
                },
                "quotaStatus": {
                    "dailyUsage": {
                        "percentage": min(25 + len(recent_emails) * 0.1, 95),
                        "remaining": max(1000 - len(recent_emails) * 10, 50)
                    },
                    "hourlyUsage": {
                        "percentage": min(10 + len(recent_emails) * 0.05, 90),
                        "remaining": max(100 - len(recent_emails), 10)
                    }
                },
                "strategyPerformance": [
                    {
                        "name": "personal_daily",
                        "efficiency": 0.87,
                        "emailsProcessed": len(recent_emails),
                        "avgConfidence": 0.85
                    }
                ],
                "alerts": self._generate_alerts(recent_emails, recent_syncs),
                "recommendations": self._generate_recommendations(recent_emails, recent_syncs)
            }

        except Exception as e:
            logger.error(f"Failed to get real-time dashboard: {e}")
            return {
                "timestamp": datetime.now().isoformat(),
                "overallStatus": {"status": "unhealthy", "error": str(e)},
                "quotaStatus": {"dailyUsage": {"percentage": 0}},
                "strategyPerformance": [],
                "alerts": [],
                "recommendations": []
            }

    def _generate_alerts(self, recent_emails: List[Dict], recent_syncs: List[Dict]) -> List[Dict[str, Any]]:
        """Generate performance alerts"""
        alerts = []

        if recent_emails:
            error_rate = 1 - (sum(1 for m in recent_emails if m['processing_success']) / len(recent_emails))
            if error_rate > self.alert_thresholds['error_rate']:
                alerts.append({
                    "type": "error_rate",
                    "strategy": "email_processing",
                    "message": f"High error rate detected: {error_rate:.1%}",
                    "severity": "warning",
                    "timestamp": datetime.now().isoformat()
                })

        return alerts

    def _generate_recommendations(self, recent_emails: List[Dict], recent_syncs: List[Dict]) -> List[Dict[str, Any]]:
        """Generate performance recommendations"""
        recommendations = []

        if len(recent_emails) > 100:
            recommendations.append({
                "type": "optimization",
                "strategy": "email_processing",
                "priority": "medium",
                "recommendation": "Consider implementing batch processing for better efficiency",
                "expectedImprovement": "20-30% faster processing",
                "action": "Enable batch processing mode"
            })

        return recommendations

    async def record_metric(self, metric_name: str, value: float,
                          tags: Dict[str, str] = None,
                          metadata: Dict[str, Any] = None):
        """Record a performance metric"""
        metric = PerformanceMetric(
            timestamp=datetime.now(),
            metric_name=metric_name,
            value=value,
            tags=tags or {},
            metadata=metadata or {}
        )

        self.metrics_buffer.append(metric)

        # Store in database (Removed)
        # await self._store_metric(metric)
        logger.debug(f"Metric recorded (in-memory): {metric.metric_name} = {metric.value}")

        # Check for alerts (in-memory)
        await self._check_alerts(metric)

    # _store_metric method removed

    async def _check_alerts(self, metric: PerformanceMetric):
        """Check if metric triggers any alerts and store them in-memory."""
        threshold = self.alert_thresholds.get(metric.metric_name)
        if threshold and metric.value > threshold:
            alert_message = f"{metric.metric_name} exceeded threshold: {metric.value:.2f} > {threshold}"
            severity = "warning" if metric.value < threshold * 1.2 else "critical"

            alert_data = {
                "timestamp": datetime.now().isoformat(),
                "alert_type": metric.metric_name,
                "severity": severity,
                "message": alert_message,
                "metric_value": metric.value,
                "threshold": threshold,
                "resolved": False # In-memory alerts are not resolved in this simple model
            }
            self.alerts_buffer.append(alert_data)
            logger.warning(f"Performance Alert [{severity}]: {alert_message}")

    # _create_alert method (DB part) removed. Alert logging is now in _check_alerts.

    async def get_system_health(self) -> SystemHealth:
        """Get current system health status"""
        try:
            cpu_usage = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            process_count = len(psutil.pids())
            uptime = time.time() - psutil.boot_time()

            # Determine overall status
            status = "healthy"
            if (cpu_usage > self.alert_thresholds["cpu_usage"] or
                memory.percent > self.alert_thresholds["memory_usage"] or
                disk.percent > self.alert_thresholds["disk_usage"]):
                status = "warning"

            if (cpu_usage > self.alert_thresholds["cpu_usage"] * 1.2 or
                memory.percent > self.alert_thresholds["memory_usage"] * 1.2): # More stringent for critical
                status = "critical"

            health = SystemHealth(
                timestamp=datetime.now(), # Add timestamp
                status=status,
                cpu_usage=cpu_usage,
                memory_usage=memory.percent,
                disk_usage=disk.percent,
                process_count=process_count,
                uptime=uptime
            )

            # Record system health (in-memory)
            self.system_health_history.append(health)
            # await self._store_system_health(health) # Removed DB storage

            return health

        except Exception as e:
            logger.error(f"Error getting system health: {e}")
            # Return a SystemHealth object even in case of error
            return SystemHealth(
                timestamp=datetime.now(), # Add timestamp
                status="unknown",
                cpu_usage=0.0,
                memory_usage=0.0,
                disk_usage=0.0,
                process_count=0,
                uptime=0.0
            )

    # _store_system_health method removed

    async def get_metrics_summary(self, hours: int = 24) -> Dict[str, Any]:
        """Get performance metrics summary for the past N hours from in-memory buffer."""
        since_time = datetime.now() - timedelta(hours=hours)

        # Filter metrics from buffer
        relevant_metrics = [m for m in self.metrics_buffer if m.timestamp > since_time]

        metrics_summary_temp = defaultdict(list)
        for metric in relevant_metrics:
            metrics_summary_temp[metric.metric_name].append(metric.value)

        final_metrics_summary = {}
        for name, values in metrics_summary_temp.items():
            count = len(values)
            avg = sum(values) / count if count > 0 else 0
            # Basic stats, can add min, max, std_dev if numpy/statistics is allowed or implemented manually
            final_metrics_summary[name] = {
                "count": count,
                "average": avg,
                "sum": sum(values),
                "values": values # Could be large, consider removing for actual summary
            }

        # Filter alerts from buffer
        relevant_alerts = [a for a in self.alerts_buffer if datetime.fromisoformat(a['timestamp']) > since_time and not a['resolved']]
        alerts_summary_temp = defaultdict(lambda: defaultdict(int))
        for alert in relevant_alerts:
            alerts_summary_temp[alert['alert_type']][alert['severity']] += 1

        final_alerts_summary = []
        for alert_type, severities in alerts_summary_temp.items():
            for severity, count in severities.items():
                 final_alerts_summary.append({
                    "type": alert_type,
                    "severity": severity,
                    "count": count
                })


        return {
            "time_range_hours": hours,
            "metrics": final_metrics_summary,
            "alerts": final_alerts_summary,
            "total_metrics_recorded_in_buffer_for_period": len(relevant_metrics)
        }

    async def get_service_performance(self, service_name: str, hours: int = 24) -> Dict[str, Any]:
        """Get performance data for a specific service from in-memory buffer."""
        since_time = datetime.now() - timedelta(hours=hours)

        service_data_points = []
        for metric in self.metrics_buffer:
            if metric.timestamp > since_time and metric.tags.get("service") == service_name:
                 service_data_points.append(metric) # Store the whole PerformanceMetric object

        response_times = [m.value for m in service_data_points if m.metric_name == "response_time"]
        error_counts = [m.value for m in service_data_points if m.metric_name == "error_count"] # Assuming error_count is 1 per error

        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        total_errors = sum(error_counts) # Sum of values (e.g., if value is 1 per error)

        return {
            "service_name": service_name,
            "time_range_hours": hours,
            "total_requests_or_metrics": len(service_data_points), # More generic name
            "average_response_time_ms": avg_response_time,
            "total_errors": total_errors,
            "error_rate_percentage": (total_errors / len(response_times) * 100) if response_times else 0, # Error rate based on response_time metrics
            "data_points": [vars(m) for m in service_data_points] # Convert dataclasses to dicts for output
        }

    async def track_function_performance(self, func_name: str):
        """Decorator to track function performance"""
        def decorator(func):
            async def wrapper(*args, **kwargs):
                start_time = time.time()
                error_occurred = False

                try:
                    result = await func(*args, **kwargs)
                    return result
                except Exception as e:
                    error_occurred = True
                    await self.record_metric(
                        "error_count",
                        1,
                        tags={"function": func_name, "error_type": type(e).__name__},
                        metadata={"error_message": str(e)}
                    )
                    raise
                finally:
                    end_time = time.time()
                    response_time = (end_time - start_time) * 1000  # Convert to milliseconds

                    await self.record_metric(
                        "response_time",
                        response_time,
                        tags={"function": func_name, "status": "error" if error_occurred else "success"}
                    )

            return wrapper
        return decorator

    async def get_optimization_recommendations(self) -> List[Dict[str, Any]]:
        """Get performance optimization recommendations"""
        recommendations = []

        # Get recent metrics
        summary = await self.get_metrics_summary(hours=24)
        health = await self.get_system_health()

        # CPU optimization
        if health.cpu_usage > 70:
            recommendations.append({
                "type": "cpu_optimization",
                "priority": "high" if health.cpu_usage > 85 else "medium",
                "title": "High CPU Usage Detected",
                "description": f"CPU usage is at {health.cpu_usage:.1f}%. Consider optimizing CPU-intensive operations.",
                "suggestions": [
                    "Review and optimize database queries",
                    "Implement caching for frequently accessed data",
                    "Consider using async operations for I/O bound tasks"
                ]
            })

        # Memory optimization
        if health.memory_usage > 75:
            recommendations.append({
                "type": "memory_optimization",
                "priority": "high" if health.memory_usage > 90 else "medium",
                "title": "High Memory Usage",
                "description": f"Memory usage is at {health.memory_usage:.1f}%. Memory optimization needed.",
                "suggestions": [
                    "Implement proper garbage collection",
                    "Reduce memory-intensive operations",
                    "Use memory-efficient data structures"
                ]
            })

        # Response time optimization
        response_time_metrics = summary["metrics"].get("response_time", {})
        if response_time_metrics and response_time_metrics["average"] > 2000:
            recommendations.append({
                "type": "response_time_optimization",
                "priority": "medium",
                "title": "Slow Response Times",
                "description": f"Average response time is {response_time_metrics['average']:.0f}ms.",
                "suggestions": [
                    "Optimize database queries",
                    "Implement request caching",
                    "Consider load balancing"
                ]
            })

        # Error rate optimization
        error_metrics = summary["metrics"].get("error_count", {})
        if error_metrics and error_metrics["count"] > 10:
            recommendations.append({
                "type": "error_reduction",
                "priority": "high",
                "title": "High Error Rate",
                "description": f"Detected {error_metrics['count']} errors in the last 24 hours.",
                "suggestions": [
                    "Review error logs and fix common issues",
                    "Implement better error handling",
                    "Add input validation"
                ]
            })

        return recommendations

    async def cleanup_old_data(self, days: int = 30):
        """Clean up old performance data (No longer needed for in-memory)"""
        # This method is no longer needed as deques handle fixed-size history.
        # If specific cleanup of in-memory buffers were needed, it would go here.
        logger.info("cleanup_old_data called, but not applicable for in-memory PerformanceMonitor.")
        return {
            "metrics_deleted": 0, # No direct deletion like from DB
            "health_records_deleted": 0,
            "alerts_deleted": 0
        }

async def main():
    """Example usage of performance monitor"""
    monitor = PerformanceMonitor()

    # Record some test metrics
    await monitor.record_metric("response_time", 150.5, {"service": "gmail_sync"})
    await monitor.record_metric("cpu_usage", 45.2)
    await monitor.record_metric("memory_usage", 62.8)

    # Get system health
    health = await monitor.get_system_health()
    print(f"System Status: {health.status}")
    print(f"CPU: {health.cpu_usage:.1f}%, Memory: {health.memory_usage:.1f}%")

    # Get metrics summary
    summary = await monitor.get_metrics_summary(hours=1)
    print(f"Metrics Summary: {summary}")

    # Get optimization recommendations
    recommendations = await monitor.get_optimization_recommendations()
    print(f"Recommendations: {len(recommendations)} found")
    for rec in recommendations:
        print(f"- {rec['title']} ({rec['priority']} priority)")

if __name__ == "__main__":
    asyncio.run(main())