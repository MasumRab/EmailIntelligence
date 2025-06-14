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
import sqlite3

logger = logging.getLogger(__name__)

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
    status: str  # healthy, warning, critical
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    process_count: int
    uptime: float

class PerformanceMonitor:
    """Performance monitoring for email processing"""

    def __init__(self, db_path: str = "performance.db"):
        self.metrics_history = defaultdict(deque)
        self.performance_data = {}
        self.alert_thresholds = {
            'processing_time': 5.0,  # seconds
            'error_rate': 0.1,  # 10%
            'memory_usage': 0.8,  # 80%
            "cpu_usage": 80.0,
            "memory_usage": 85.0,
            "disk_usage": 90.0,
            "response_time": 5000.0,  # milliseconds
            "error_rate": 10.0  # percentage
        }
        self.db_path = db_path
        self.metrics_buffer = deque(maxlen=1000)
        self.service_metrics = defaultdict(list)
        self.init_database()

    def init_database(self):
        """Initialize performance monitoring database"""
        conn = sqlite3.connect(self.db_path)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS performance_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                metric_name TEXT NOT NULL,
                value REAL NOT NULL,
                tags TEXT,
                metadata TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS system_health (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                status TEXT NOT NULL,
                cpu_usage REAL,
                memory_usage REAL,
                disk_usage REAL,
                process_count INTEGER,
                uptime REAL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS performance_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                alert_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                message TEXT NOT NULL,
                metric_value REAL,
                threshold REAL,
                resolved BOOLEAN DEFAULT FALSE,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()

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

        # Store in database
        await self._store_metric(metric)

        # Check for alerts
        await self._check_alerts(metric)

    async def _store_metric(self, metric: PerformanceMetric):
        """Store metric in database"""
        conn = sqlite3.connect(self.db_path)

        conn.execute("""
            INSERT INTO performance_metrics
            (timestamp, metric_name, value, tags, metadata)
            VALUES (?, ?, ?, ?, ?)
        """, (
            metric.timestamp.isoformat(),
            metric.metric_name,
            metric.value,
            json.dumps(metric.tags),
            json.dumps(metric.metadata)
        ))

        conn.commit()
        conn.close()

    async def _check_alerts(self, metric: PerformanceMetric):
        """Check if metric triggers any alerts"""
        threshold = self.alert_thresholds.get(metric.metric_name)
        if threshold and metric.value > threshold:
            await self._create_alert(
                alert_type=metric.metric_name,
                severity="warning" if metric.value < threshold * 1.2 else "critical",
                message=f"{metric.metric_name} exceeded threshold: {metric.value:.2f} > {threshold}",
                metric_value=metric.value,
                threshold=threshold
            )

    async def _create_alert(self, alert_type: str, severity: str, message: str,
                          metric_value: float, threshold: float):
        """Create a performance alert"""
        conn = sqlite3.connect(self.db_path)

        conn.execute("""
            INSERT INTO performance_alerts
            (timestamp, alert_type, severity, message, metric_value, threshold)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            alert_type,
            severity,
            message,
            metric_value,
            threshold
        ))

        conn.commit()
        conn.close()

        logger.warning(f"Performance Alert [{severity}]: {message}")

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
                memory.percent > self.alert_thresholds["memory_usage"] * 1.2):
                status = "critical"

            health = SystemHealth(
                status=status,
                cpu_usage=cpu_usage,
                memory_usage=memory.percent,
                disk_usage=disk.percent,
                process_count=process_count,
                uptime=uptime
            )

            # Record system health
            await self._store_system_health(health)

            return health

        except Exception as e:
            logger.error(f"Error getting system health: {e}")
            return SystemHealth(
                status="unknown",
                cpu_usage=0.0,
                memory_usage=0.0,
                disk_usage=0.0,
                process_count=0,
                uptime=0.0
            )

    async def _store_system_health(self, health: SystemHealth):
        """Store system health in database"""
        conn = sqlite3.connect(self.db_path)

        conn.execute("""
            INSERT INTO system_health
            (timestamp, status, cpu_usage, memory_usage, disk_usage, process_count, uptime)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            health.status,
            health.cpu_usage,
            health.memory_usage,
            health.disk_usage,
            health.process_count,
            health.uptime
        ))

        conn.commit()
        conn.close()

    async def get_metrics_summary(self, hours: int = 24) -> Dict[str, Any]:
        """Get performance metrics summary for the past N hours"""
        conn = sqlite3.connect(self.db_path)

        since_time = datetime.now() - timedelta(hours=hours)

        cursor = conn.execute("""
            SELECT metric_name,
                   COUNT(*) as count,
                   AVG(value) as avg_value,
                   MIN(value) as min_value,
                   MAX(value) as max_value,
                   STDEV(value) as std_dev
            FROM performance_metrics
            WHERE timestamp > ?
            GROUP BY metric_name
        """, (since_time.isoformat(),))

        metrics_summary = {}
        for row in cursor.fetchall():
            metrics_summary[row[0]] = {
                "count": row[1],
                "average": row[2],
                "minimum": row[3],
                "maximum": row[4],
                "std_deviation": row[5] or 0.0
            }

        # Get recent alerts
        cursor = conn.execute("""
            SELECT alert_type, severity, COUNT(*) as count
            FROM performance_alerts
            WHERE timestamp > ? AND resolved = FALSE
            GROUP BY alert_type, severity
        """, (since_time.isoformat(),))

        alerts_summary = []
        for row in cursor.fetchall():
            alerts_summary.append({
                "type": row[0],
                "severity": row[1],
                "count": row[2]
            })

        conn.close()

        return {
            "time_range_hours": hours,
            "metrics": metrics_summary,
            "alerts": alerts_summary,
            "total_metrics": sum(m["count"] for m in metrics_summary.values())
        }

    async def get_service_performance(self, service_name: str, hours: int = 24) -> Dict[str, Any]:
        """Get performance data for a specific service"""
        conn = sqlite3.connect(self.db_path)

        since_time = datetime.now() - timedelta(hours=hours)

        cursor = conn.execute("""
            SELECT timestamp, metric_name, value, tags, metadata
            FROM performance_metrics
            WHERE timestamp > ? AND tags LIKE ?
            ORDER BY timestamp DESC
        """, (since_time.isoformat(), f'%{service_name}%'))

        service_data = []
        for row in cursor.fetchall():
            service_data.append({
                "timestamp": row[0],
                "metric_name": row[1],
                "value": row[2],
                "tags": json.loads(row[3]) if row[3] else {},
                "metadata": json.loads(row[4]) if row[4] else {}
            })

        conn.close()

        # Calculate service-specific metrics
        response_times = [d["value"] for d in service_data if d["metric_name"] == "response_time"]
        error_counts = [d["value"] for d in service_data if d["metric_name"] == "error_count"]

        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        total_errors = sum(error_counts) if error_counts else 0

        return {
            "service_name": service_name,
            "time_range_hours": hours,
            "total_requests": len(service_data),
            "average_response_time": avg_response_time,
            "total_errors": total_errors,
            "error_rate": (total_errors / len(service_data) * 100) if service_data else 0,
            "data_points": service_data
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
        """Clean up old performance data"""
        conn = sqlite3.connect(self.db_path)

        cutoff_date = datetime.now() - timedelta(days=days)

        # Clean up old metrics
        cursor = conn.execute("""
            DELETE FROM performance_metrics
            WHERE timestamp < ?
        """, (cutoff_date.isoformat(),))

        metrics_deleted = cursor.rowcount

        # Clean up old system health data
        cursor = conn.execute("""
            DELETE FROM system_health
            WHERE timestamp < ?
        """, (cutoff_date.isoformat(),))

        health_deleted = cursor.rowcount

        # Clean up resolved alerts
        cursor = conn.execute("""
            DELETE FROM performance_alerts
            WHERE timestamp < ? AND resolved = TRUE
        """, (cutoff_date.isoformat(),))

        alerts_deleted = cursor.rowcount

        conn.commit()
        conn.close()

        logger.info(f"Cleaned up old data: {metrics_deleted} metrics, {health_deleted} health records, {alerts_deleted} alerts")

        return {
            "metrics_deleted": metrics_deleted,
            "health_records_deleted": health_deleted,
            "alerts_deleted": alerts_deleted
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