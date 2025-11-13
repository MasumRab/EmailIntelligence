"""
Performance monitoring and metrics collection
"""

import time
import psutil
import structlog
from typing import Dict, Any
from collections import defaultdict, deque

logger = structlog.get_logger()


class PerformanceMonitor:
    """Performance monitoring and metrics collection"""

    def __init__(self):
        self.request_times = defaultdict(deque)
        self.query_times = deque(maxlen=1000)
        self.error_counts = defaultdict(int)
        self.total_requests = 0
        self.start_time = time.time()
        self.max_history = 10000  # Maximum number of requests to keep in history

    def record_request(self, method: str, path: str, status_code: int, duration: float):
        """Record HTTP request metrics"""
        self.total_requests += 1

        # Store request time
        self.request_times[f"{method} {path}"].append(duration)

        # Keep only recent requests
        if len(self.request_times[f"{method} {path}"]) > self.max_history:
            self.request_times[f"{method} {path}"].popleft()

        # Record errors
        if status_code >= 400:
            self.error_counts[f"{status_code}"] += 1

        # Log slow requests (> 1 second)
        if duration > 1.0:
            logger.warning(
                "Slow request detected", method=method, path=path, duration=duration, status_code=status_code
            )

    def record_query_execution(self, duration: float):
        """Record GraphQL query execution time"""
        self.query_times.append(duration)

        # Log slow queries
        if duration > 0.5:  # 500ms
            logger.warning("Slow GraphQL query", duration=duration)

    def analyze_query_complexity(self, query: str) -> int:
        """Simple query complexity analysis"""
        # Count field selections, nested queries, and operations
        complexity_score = 0

        # Count field selections (simplified)
        complexity_score += query.count("{")
        complexity_score += query.count("fragment") * 5  # Fragments add complexity

        # Nested queries increase complexity
        nesting_level = 0
        for char in query:
            if char == "{":
                nesting_level += 1
            elif char == "}":
                nesting_level -= 1

        complexity_score += nesting_level * 2

        # Count operations
        complexity_score += query.count("query") * 3
        complexity_score += query.count("mutation") * 5

        logger.debug("Query complexity analyzed", complexity=complexity_score, query_length=len(query))

        return complexity_score

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        current_time = time.time()
        uptime = current_time - self.start_time

        # Calculate average response times
        avg_response_times = {}
        for endpoint, times in self.request_times.items():
            if times:
                avg_response_times[endpoint] = {
                    "avg": sum(times) / len(times),
                    "min": min(times),
                    "max": max(times),
                    "count": len(times),
                }

        # Query performance
        query_stats = {}
        if self.query_times:
            query_stats = {
                "avg_query_time": sum(self.query_times) / len(self.query_times),
                "min_query_time": min(self.query_times),
                "max_query_time": max(self.query_times),
                "total_queries": len(self.query_times),
            }

        return {
            "uptime_seconds": uptime,
            "total_requests": self.total_requests,
            "requests_per_second": self.total_requests / uptime if uptime > 0 else 0,
            "error_rate": sum(self.error_counts.values()) / self.total_requests if self.total_requests > 0 else 0,
            "error_breakdown": dict(self.error_counts),
            "avg_response_times": avg_response_times,
            "query_performance": query_stats,
            "endpoints": list(self.request_times.keys()),
        }

    def get_system_metrics(self) -> Dict[str, Any]:
        """Get system resource metrics"""
        try:
            return {
                "cpu_percent": psutil.cpu_percent(interval=1),
                "memory_percent": psutil.virtual_memory().percent,
                "memory_used_mb": psutil.virtual_memory().used / 1024 / 1024,
                "memory_available_mb": psutil.virtual_memory().available / 1024 / 1024,
                "disk_usage_percent": psutil.disk_usage("/").percent,
                "disk_free_gb": psutil.disk_usage("/").free / 1024 / 1024 / 1024,
                "load_average": list(psutil.getloadavg()) if hasattr(psutil, "getloadavg") else [0, 0, 0],
            }
        except Exception as e:
            logger.error("Failed to get system metrics", error=str(e))
            return {"error": str(e)}


# Global monitor instance
monitor = PerformanceMonitor()
