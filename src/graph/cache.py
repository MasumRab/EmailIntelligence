"""
Graph-specific caching and monitoring system for PR Resolution Automation
"""

import time
import json
import hashlib
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from enum import Enum
import structlog
from collections import defaultdict, deque

from ...utils.monitoring import get_monitor

logger = structlog.get_logger()


class CacheType(Enum):
    """Types of graph caches"""

    TRAVERSAL_RESULT = "traversal_result"
    QUERY_RESULT = "query_result"
    ANALYTICS_RESULT = "analytics_result"
    CONFLICT_SCORE = "conflict_score"
    PERFORMANCE_METRIC = "performance_metric"
    PATTERN_RESULT = "pattern_result"


class MetricType(Enum):
    """Types of performance metrics"""

    QUERY_EXECUTION_TIME = "query_execution_time"
    TRAVERSAL_NODES_VISITED = "traversal_nodes_visited"
    TRAVERSAL_EDGES_TRAVERSED = "traversal_edges_traversed"
    CONFLICT_DETECTION_TIME = "conflict_detection_time"
    SCORING_TIME = "scoring_time"
    CACHE_HIT_RATE = "cache_hit_rate"
    MEMORY_USAGE = "memory_usage"
    CACHE_SIZE = "cache_size"


class AlertSeverity(Enum):
    """Alert severity levels"""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class CacheEntry:
    """Represents a cache entry with metadata"""

    def __init__(
        self,
        key: str,
        value: Any,
        cache_type: CacheType,
        ttl: int = 3600,  # Default 1 hour
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.key = key
        self.value = value
        self.cache_type = cache_type
        self.created_at = datetime.utcnow()
        self.accessed_at = datetime.utcnow()
        self.access_count = 0
        self.hit_count = 0
        self.ttl = ttl
        self.metadata = metadata or {}

    def is_expired(self) -> bool:
        """Check if cache entry is expired"""
        age = (datetime.utcnow() - self.created_at).total_seconds()
        return age > self.ttl

    def access(self):
        """Mark cache entry as accessed"""
        self.accessed_at = datetime.utcnow()
        self.access_count += 1
        self.hit_count += 1


class GraphCacheManager:
    """
    Specialized cache manager for graph operations
    """

    def __init__(self, max_size: int = 1000, default_ttl: int = 3600):
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.cache: Dict[str, CacheEntry] = {}
        self.access_order = deque()  # For LRU eviction
        self.stats = {"hits": 0, "misses": 0, "evictions": 0, "expired_removed": 0, "total_requests": 0}
        self.monitor = get_monitor()

    def _generate_cache_key(self, operation: str, parameters: Dict[str, Any], cache_type: CacheType) -> str:
        """Generate a unique cache key"""
        key_data = {"operation": operation, "parameters": parameters, "cache_type": cache_type.value}
        key_string = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_string.encode()).hexdigest()

    async def cache_traversal_result(
        self, operation: str, parameters: Dict[str, Any], result: Any, ttl: Optional[int] = None
    ) -> str:
        """Cache a traversal result"""
        cache_key = self._generate_cache_key(operation, parameters, CacheType.TRAVERSAL_RESULT)
        ttl = ttl or self.default_ttl

        entry = CacheEntry(
            key=cache_key,
            value=result,
            cache_type=CacheType.TRAVERSAL_RESULT,
            ttl=ttl,
            metadata={"operation": operation, "parameters": parameters},
        )

        await self._store_entry(cache_key, entry)

        # Record cache operation
        self.monitor.record_metric("graph_cache_traversal_stored", 1.0)

        return cache_key

    async def get_traversal_result(self, operation: str, parameters: Dict[str, Any]) -> Optional[Any]:
        """Get cached traversal result"""
        cache_key = self._generate_cache_key(operation, parameters, CacheType.TRAVERSAL_RESULT)
        return await self._get_entry(cache_key)

    async def cache_query_result(
        self, query_hash: str, parameters: Dict[str, Any], result: Any, ttl: Optional[int] = None
    ) -> str:
        """Cache a query result"""
        cache_key = f"query:{query_hash}:{hashlib.md5(str(sorted(parameters.items())).encode()).hexdigest()}"
        ttl = ttl or self.default_ttl

        entry = CacheEntry(
            key=cache_key,
            value=result,
            cache_type=CacheType.QUERY_RESULT,
            ttl=ttl,
            metadata={"query_hash": query_hash, "parameters": parameters},
        )

        await self._store_entry(cache_key, entry)

        self.monitor.record_metric("graph_cache_query_stored", 1.0)

        return cache_key

    async def get_query_result(self, cache_key: str) -> Optional[Any]:
        """Get cached query result"""
        return await self._get_entry(cache_key)

    async def cache_analytics_result(
        self, analysis_type: str, parameters: Dict[str, Any], result: Any, ttl: Optional[int] = None
    ) -> str:
        """Cache an analytics result"""
        cache_key = self._generate_cache_key(analysis_type, parameters, CacheType.ANALYTICS_RESULT)
        ttl = ttl or (self.default_ttl * 2)  # Analytics results live longer

        entry = CacheEntry(
            key=cache_key,
            value=result,
            cache_type=CacheType.ANALYTICS_RESULT,
            ttl=ttl,
            metadata={"analysis_type": analysis_type, "parameters": parameters},
        )

        await self._store_entry(cache_key, entry)

        self.monitor.record_metric("graph_cache_analytics_stored", 1.0)

        return cache_key

    async def get_analytics_result(self, analysis_type: str, parameters: Dict[str, Any]) -> Optional[Any]:
        """Get cached analytics result"""
        cache_key = self._generate_cache_key(analysis_type, parameters, CacheType.ANALYTICS_RESULT)
        return await self._get_entry(cache_key)

    async def cache_conflict_score(self, conflict_id: str, score_data: Any, ttl: Optional[int] = None) -> str:
        """Cache a conflict score"""
        cache_key = f"conflict_score:{conflict_id}"
        ttl = ttl or (self.default_ttl * 24)  # Conflict scores live for 24 hours

        entry = CacheEntry(
            key=cache_key,
            value=score_data,
            cache_type=CacheType.CONFLICT_SCORE,
            ttl=ttl,
            metadata={"conflict_id": conflict_id},
        )

        await self._store_entry(cache_key, entry)

        self.monitor.record_metric("graph_cache_conflict_score_stored", 1.0)

        return cache_key

    async def get_conflict_score(self, conflict_id: str) -> Optional[Any]:
        """Get cached conflict score"""
        cache_key = f"conflict_score:{conflict_id}"
        return await self._get_entry(cache_key)

    async def cache_pattern_result(
        self, pattern_type: str, parameters: Dict[str, Any], result: Any, ttl: Optional[int] = None
    ) -> str:
        """Cache a pattern detection result"""
        cache_key = self._generate_cache_key(pattern_type, parameters, CacheType.PATTERN_RESULT)
        ttl = ttl or (self.default_ttl * 4)  # Pattern results live for 4 hours

        entry = CacheEntry(
            key=cache_key,
            value=result,
            cache_type=CacheType.PATTERN_RESULT,
            ttl=ttl,
            metadata={"pattern_type": pattern_type, "parameters": parameters},
        )

        await self._store_entry(cache_key, entry)

        self.monitor.record_metric("graph_cache_pattern_stored", 1.0)

        return cache_key

    async def get_pattern_result(self, pattern_type: str, parameters: Dict[str, Any]) -> Optional[Any]:
        """Get cached pattern result"""
        cache_key = self._generate_cache_key(pattern_type, parameters, CacheType.PATTERN_RESULT)
        return await self._get_entry(cache_key)

    async def _store_entry(self, cache_key: str, entry: CacheEntry):
        """Store a cache entry with eviction if necessary"""
        # Remove from access order if exists
        if cache_key in self.access_order:
            self.access_order.remove(cache_key)

        # Add to access order
        self.access_order.append(cache_key)

        # Store entry
        self.cache[cache_key] = entry

        # Evict if necessary
        if len(self.cache) > self.max_size:
            await self._evict_lru()

    async def _get_entry(self, cache_key: str) -> Optional[Any]:
        """Get a cache entry"""
        self.stats["total_requests"] += 1

        if cache_key not in self.cache:
            self.stats["misses"] += 1
            self.monitor.record_metric("graph_cache_miss", 1.0)
            return None

        entry = self.cache[cache_key]

        # Check if expired
        if entry.is_expired():
            await self._remove_entry(cache_key)
            self.stats["expired_removed"] += 1
            self.stats["misses"] += 1
            self.monitor.record_metric("graph_cache_expired", 1.0)
            return None

        # Update access info
        entry.access()
        self.stats["hits"] += 1
        self.monitor.record_metric("graph_cache_hit", 1.0)

        # Update access order
        if cache_key in self.access_order:
            self.access_order.remove(cache_key)
        self.access_order.append(cache_key)

        return entry.value

    async def _remove_entry(self, cache_key: str):
        """Remove a cache entry"""
        if cache_key in self.cache:
            del self.cache[cache_key]
        if cache_key in self.access_order:
            self.access_order.remove(cache_key)

    async def _evict_lru(self):
        """Evict least recently used entries"""
        evicted_count = 0
        target_size = int(self.max_size * 0.8)  # Evict down to 80% capacity

        while len(self.cache) > target_size and self.access_order:
            lru_key = self.access_order.popleft()
            await self._remove_entry(lru_key)
            evicted_count += 1

        self.stats["evictions"] += evicted_count
        self.monitor.record_metric("graph_cache_evictions", float(evicted_count))

    async def cleanup_expired(self):
        """Clean up expired cache entries"""
        expired_keys = []
        for key, entry in self.cache.items():
            if entry.is_expired():
                expired_keys.append(key)

        for key in expired_keys:
            await self._remove_entry(key)

        self.stats["expired_removed"] += len(expired_keys)
        self.monitor.record_metric("graph_cache_cleanup", float(len(expired_keys)))

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_requests = self.stats["hits"] + self.stats["misses"]
        hit_rate = self.stats["hits"] / total_requests if total_requests > 0 else 0.0

        # Calculate average age of entries
        current_time = datetime.utcnow()
        total_age = 0
        for entry in self.cache.values():
            age = (current_time - entry.created_at).total_seconds()
            total_age += age

        avg_age = total_age / len(self.cache) if self.cache else 0.0

        return {
            **self.stats,
            "hit_rate": hit_rate,
            "cache_size": len(self.cache),
            "max_size": self.max_size,
            "avg_entry_age": avg_age,
            "memory_usage_mb": self._estimate_memory_usage(),
        }

    def _estimate_memory_usage(self) -> float:
        """Estimate memory usage in MB"""
        # This is a simplified estimation
        import sys

        total_size = 0
        for key, entry in self.cache.items():
            total_size += sys.getsizeof(key)
            total_size += sys.getsizeof(entry)
            total_size += sys.getsizeof(entry.value)
        return total_size / (1024 * 1024)  # Convert to MB

    async def clear_cache(self, cache_type: Optional[CacheType] = None):
        """Clear cache entries"""
        if cache_type is None:
            # Clear all
            self.cache.clear()
            self.access_order.clear()
        else:
            # Clear specific type
            keys_to_remove = [key for key, entry in self.cache.items() if entry.cache_type == cache_type]
            for key in keys_to_remove:
                await self._remove_entry(key)

        logger.info("Cache cleared", cache_type=cache_type.value if cache_type else "all")


class GraphPerformanceMonitor:
    """
    Monitor performance metrics for graph operations
    """

    def __init__(self):
        self.metrics: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        self.alerts: List[Dict[str, Any]] = []
        self.monitor = get_monitor()
        self.thresholds = {
            MetricType.QUERY_EXECUTION_TIME: 1.0,  # 1 second
            MetricType.TRAVERSAL_NODES_VISITED: 10000,  # 10k nodes
            MetricType.CONFLICT_DETECTION_TIME: 0.5,  # 500ms
            MetricType.SCORING_TIME: 0.1,  # 100ms
            MetricType.CACHE_HIT_RATE: 0.8,  # 80%
            MetricType.MEMORY_USAGE: 500,  # 500MB
        }

    def record_query_execution_time(self, execution_time: float, query_type: str = "general"):
        """Record query execution time"""
        metric_name = f"graph_query_execution_time_{query_type}"
        self.metrics[metric_name].append({"timestamp": datetime.utcnow(), "value": execution_time})

        self.monitor.record_metric(metric_name, execution_time)

        # Check for alerts
        if execution_time > self.thresholds[MetricType.QUERY_EXECUTION_TIME]:
            self._create_alert(
                severity=AlertSeverity.HIGH,
                metric=metric_name,
                message=f"Slow query execution: {execution_time:.3f}s",
                value=execution_time,
                threshold=self.thresholds[MetricType.QUERY_EXECUTION_TIME],
            )

    def record_traversal_metrics(self, nodes_visited: int, edges_traversed: int, execution_time: float, strategy: str):
        """Record traversal performance metrics"""
        # Record nodes visited
        metric_name = f"graph_traversal_nodes_visited_{strategy}"
        self.metrics[metric_name].append({"timestamp": datetime.utcnow(), "value": nodes_visited})
        self.monitor.record_metric(metric_name, float(nodes_visited))

        # Record edges traversed
        metric_name = f"graph_traversal_edges_traversed_{strategy}"
        self.metrics[metric_name].append({"timestamp": datetime.utcnow(), "value": edges_traversed})
        self.monitor.record_metric(metric_name, float(edges_traversed))

        # Record execution time
        metric_name = f"graph_traversal_execution_time_{strategy}"
        self.metrics[metric_name].append({"timestamp": datetime.utcnow(), "value": execution_time})
        self.monitor.record_metric(metric_name, execution_time)

        # Check for alerts
        if nodes_visited > self.thresholds[MetricType.TRAVERSAL_NODES_VISITED]:
            self._create_alert(
                severity=AlertSeverity.MEDIUM,
                metric="graph_traversal_nodes_visited",
                message=f"High node visitation: {nodes_visited} nodes",
                value=nodes_visited,
                threshold=self.thresholds[MetricType.TRAVERSAL_NODES_VISITED],
            )

    def record_conflict_detection_time(self, detection_time: float, conflict_type: str):
        """Record conflict detection time"""
        metric_name = f"graph_conflict_detection_time_{conflict_type}"
        self.metrics[metric_name].append({"timestamp": datetime.utcnow(), "value": detection_time})

        self.monitor.record_metric(metric_name, detection_time)

        # Check for alerts
        if detection_time > self.thresholds[MetricType.CONFLICT_DETECTION_TIME]:
            self._create_alert(
                severity=AlertSeverity.MEDIUM,
                metric=metric_name,
                message=f"Slow conflict detection: {detection_time:.3f}s",
                value=detection_time,
                threshold=self.thresholds[MetricType.CONFLICT_DETECTION_TIME],
            )

    def record_scoring_time(self, scoring_time: float, conflicts_scored: int):
        """Record conflict scoring time"""
        metric_name = "graph_scoring_time_per_conflict"
        avg_time = scoring_time / conflicts_scored if conflicts_scored > 0 else 0

        self.metrics[metric_name].append({"timestamp": datetime.utcnow(), "value": avg_time})

        self.monitor.record_metric(metric_name, avg_time)

        # Check for alerts
        if avg_time > self.thresholds[MetricType.SCORING_TIME]:
            self._create_alert(
                severity=AlertSeverity.MEDIUM,
                metric=metric_name,
                message=f"Slow conflict scoring: {avg_time:.3f}s per conflict",
                value=avg_time,
                threshold=self.thresholds[MetricType.SCORING_TIME],
            )

    def record_cache_performance(self, hit_rate: float, cache_size: int, memory_usage: float):
        """Record cache performance metrics"""
        # Record hit rate
        metric_name = "graph_cache_hit_rate"
        self.metrics[metric_name].append({"timestamp": datetime.utcnow(), "value": hit_rate})
        self.monitor.record_metric(metric_name, hit_rate)

        # Record cache size
        metric_name = "graph_cache_size"
        self.metrics[metric_name].append({"timestamp": datetime.utcnow(), "value": cache_size})
        self.monitor.record_metric(metric_name, float(cache_size))

        # Record memory usage
        metric_name = "graph_cache_memory_usage"
        self.metrics[metric_name].append({"timestamp": datetime.utcnow(), "value": memory_usage})
        self.monitor.record_metric(metric_name, memory_usage)

        # Check for alerts
        if hit_rate < self.thresholds[MetricType.CACHE_HIT_RATE]:
            self._create_alert(
                severity=AlertSeverity.LOW,
                metric="graph_cache_hit_rate",
                message=f"Low cache hit rate: {hit_rate:.2%}",
                value=hit_rate,
                threshold=self.thresholds[MetricType.CACHE_HIT_RATE],
            )

        if memory_usage > self.thresholds[MetricType.MEMORY_USAGE]:
            self._create_alert(
                severity=AlertSeverity.HIGH,
                metric="graph_cache_memory_usage",
                message=f"High cache memory usage: {memory_usage:.1f}MB",
                value=memory_usage,
                threshold=self.thresholds[MetricType.MEMORY_USAGE],
            )

    def _create_alert(self, severity: AlertSeverity, metric: str, message: str, value: float, threshold: float):
        """Create an alert"""
        alert = {
            "id": f"alert_{int(time.time())}",
            "severity": severity.value,
            "metric": metric,
            "message": message,
            "value": value,
            "threshold": threshold,
            "created_at": datetime.utcnow(),
            "acknowledged": False,
        }

        self.alerts.append(alert)

        # Log the alert
        logger.warning(
            "Performance alert generated",
            severity=severity.value,
            metric=metric,
            message=message,
            value=value,
            threshold=threshold,
        )

        # Record alert metric
        self.monitor.record_metric("graph_alerts_generated", 1.0)

    def get_performance_summary(self, duration_minutes: int = 60) -> Dict[str, Any]:
        """Get performance summary for the last N minutes"""
        cutoff_time = datetime.utcnow() - timedelta(minutes=duration_minutes)

        summary = {"period_minutes": duration_minutes, "generated_at": datetime.utcnow(), "metrics": {}}

        for metric_name, values in self.metrics.items():
            # Filter values within the time window
            recent_values = [v for v in values if v["timestamp"] >= cutoff_time]

            if recent_values:
                metric_values = [v["value"] for v in recent_values]
                summary["metrics"][metric_name] = {
                    "count": len(metric_values),
                    "min": min(metric_values),
                    "max": max(metric_values),
                    "avg": sum(metric_values) / len(metric_values),
                    "latest": metric_values[-1],
                }

        return summary

    def get_active_alerts(self, severity: Optional[AlertSeverity] = None) -> List[Dict[str, Any]]:
        """Get active (unacknowledged) alerts"""
        alerts = [alert for alert in self.alerts if not alert["acknowledged"]]

        if severity:
            alerts = [alert for alert in alerts if alert["severity"] == severity.value]

        return alerts

    def acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge an alert"""
        for alert in self.alerts:
            if alert["id"] == alert_id:
                alert["acknowledged"] = True
                logger.info("Alert acknowledged", alert_id=alert_id)
                return True

        return False

    def clear_acknowledged_alerts(self):
        """Remove acknowledged alerts"""
        before_count = len(self.alerts)
        self.alerts = [alert for alert in self.alerts if not alert["acknowledged"]]
        after_count = len(self.alerts)

        logger.info("Cleared acknowledged alerts", before_count=before_count, after_count=after_count)

    def update_threshold(self, metric_type: MetricType, threshold: float):
        """Update alert threshold for a metric"""
        self.thresholds[metric_type] = threshold
        logger.info("Alert threshold updated", metric=metric_type.value, threshold=threshold)

    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health status"""
        health_status = {"overall": "healthy", "components": {}, "critical_issues": [], "warnings": []}

        # Check cache performance
        cache_hit_rates = [v["value"] for v in self.metrics.get("graph_cache_hit_rate", [])[-10:]]
        if cache_hit_rates:
            avg_hit_rate = sum(cache_hit_rates) / len(cache_hit_rates)
            if avg_hit_rate < 0.5:
                health_status["overall"] = "critical"
                health_status["critical_issues"].append("Very low cache hit rate")
            elif avg_hit_rate < 0.7:
                health_status["overall"] = (
                    "warning" if health_status["overall"] == "healthy" else health_status["overall"]
                )
                health_status["warnings"].append("Low cache hit rate")

        # Check query performance
        query_times = [v["value"] for v in self.metrics.get("graph_query_execution_time_general", [])[-10:]]
        if query_times:
            avg_query_time = sum(query_times) / len(query_times)
            if avg_query_time > 2.0:
                health_status["overall"] = (
                    "critical" if health_status["overall"] == "healthy" else health_status["overall"]
                )
                health_status["critical_issues"].append("Very slow query performance")
            elif avg_query_time > 1.0:
                health_status["overall"] = (
                    "warning" if health_status["overall"] == "healthy" else health_status["overall"]
                )
                health_status["warnings"].append("Slow query performance")

        # Check active alerts
        critical_alerts = self.get_active_alerts(AlertSeverity.CRITICAL)
        high_alerts = self.get_active_alerts(AlertSeverity.HIGH)

        if critical_alerts:
            health_status["overall"] = "critical"
            health_status["critical_issues"].append(f"{len(critical_alerts)} critical alerts active")

        if high_alerts:
            health_status["overall"] = "warning" if health_status["overall"] == "healthy" else health_status["overall"]
            health_status["warnings"].append(f"{len(high_alerts)} high priority alerts active")

        health_status["components"] = {
            "cache": "healthy" if len([a for a in critical_alerts if "cache" in a["metric"]]) == 0 else "critical",
            "query_performance": (
                "healthy" if len([a for a in critical_alerts if "query" in a["metric"]]) == 0 else "critical"
            ),
            "traversal": (
                "healthy" if len([a for a in critical_alerts if "traversal" in a["metric"]]) == 0 else "critical"
            ),
        }

        health_status["timestamp"] = datetime.utcnow()
        return health_status


# Global instances
graph_cache = GraphCacheManager(max_size=2000, default_ttl=3600)
graph_monitor = GraphPerformanceMonitor()


# Convenience functions


async def cache_traversal_operation(
    operation: str, parameters: Dict[str, Any], result: Any, ttl: Optional[int] = None
) -> str:
    """Cache a traversal operation result"""
    return await graph_cache.cache_traversal_result(operation, parameters, result, ttl)


async def get_cached_traversal_result(operation: str, parameters: Dict[str, Any]) -> Optional[Any]:
    """Get cached traversal result"""
    return await graph_cache.get_traversal_result(operation, parameters)


def record_traversal_performance(nodes_visited: int, edges_traversed: int, execution_time: float, strategy: str):
    """Record traversal performance metrics"""
    graph_monitor.record_traversal_metrics(nodes_visited, edges_traversed, execution_time, strategy)


def record_cache_performance(hit_rate: float, cache_size: int, memory_usage: float):
    """Record cache performance metrics"""
    graph_monitor.record_cache_performance(hit_rate, cache_size, memory_usage)


def get_graph_performance_summary(duration_minutes: int = 60) -> Dict[str, Any]:
    """Get graph performance summary"""
    return graph_monitor.get_performance_summary(duration_minutes)


def get_graph_system_health() -> Dict[str, Any]:
    """Get graph system health status"""
    return graph_monitor.get_system_health()
