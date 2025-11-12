"""
AI-specific monitoring and metrics collection
"""

import time
import structlog
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict, deque
from dataclasses import dataclass, asdict

from .client import get_openai_client
from .analysis import get_conflict_analyzer
from .processing import get_ai_processor
from ..config.settings import settings

logger = structlog.get_logger()


@dataclass
class AIMetrics:
    """AI metrics data structure"""
    timestamp: datetime
    request_count: int
    success_count: int
    error_count: int
    average_response_time: float
    total_tokens_used: int
    cost_estimate: float
    cache_hit_rate: float
    circuit_breaker_state: str
    active_tasks: int
    completed_tasks: int


class AIMonitor:
    """
    AI service monitoring and metrics collection
    """
    
    def __init__(self, max_history: int = 1000):
        self.max_history = max_history
        self.metrics_history: deque = deque(maxlen=max_history)
        self.service_health: Dict[str, Any] = {}
        self.performance_alerts: List[Dict[str, Any]] = []
        self.usage_analytics: Dict[str, Any] = defaultdict(int)
        self.start_time = time.time()
    
    async def collect_metrics(self) -> AIMetrics:
        """Collect current AI service metrics"""
        try:
            # Get OpenAI client metrics
            client = await get_openai_client()
            client_stats = client.get_stats()
            
            # Get analyzer metrics
            analyzer = await get_conflict_analyzer()
            analyzer_health = await analyzer.health_check()
            
            # Get processor metrics
            processor = await get_ai_processor()
            processor_stats = processor.get_stats()
            
            # Calculate derived metrics
            total_requests = client_stats.get("request_count", 0)
            successful_requests = total_requests - client_stats.get("error_count", 0)
            error_rate = client_stats.get("error_count", 0) / max(total_requests, 1)
            cache_hit_rate = self._calculate_cache_hit_rate()
            
            # Estimate cost (rough calculation)
            cost_estimate = self._estimate_cost(total_requests)
            
            # Create metrics object
            metrics = AIMetrics(
                timestamp=datetime.utcnow(),
                request_count=total_requests,
                success_count=successful_requests,
                error_count=client_stats.get("error_count", 0),
                average_response_time=self._calculate_average_response_time(),
                total_tokens_used=self._estimate_token_usage(total_requests),
                cost_estimate=cost_estimate,
                cache_hit_rate=cache_hit_rate,
                circuit_breaker_state=client_stats.get("circuit_breaker_state", "closed"),
                active_tasks=processor_stats.get("active_tasks", 0),
                completed_tasks=processor_stats.get("completed_tasks", 0)
            )
            
            # Add to history
            self.metrics_history.append(metrics)
            
            # Update service health status
            self.service_health = {
                "openai": client_stats,
                "analyzer": analyzer_health,
                "processor": processor_stats,
                "overall": "healthy" if error_rate < 0.1 else "degraded" if error_rate < 0.3 else "unhealthy"
            }
            
            # Check for alerts
            await self._check_performance_alerts(metrics)
            
            # Update usage analytics
            self._update_usage_analytics()
            
            logger.debug("AI metrics collected",
                        requests=total_requests,
                        errors=metrics.error_count,
                        error_rate=error_rate)
            
            return metrics
            
        except Exception as e:
            logger.error("Failed to collect AI metrics", error=str(e))
            return self._create_fallback_metrics()
    
    async def get_health_report(self) -> Dict[str, Any]:
        """Get comprehensive AI service health report"""
        current_metrics = await self.collect_metrics()
        
        # Calculate trends
        trends = self._calculate_trends()
        
        # Get recent alerts
        recent_alerts = self._get_recent_alerts(hours=24)
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "overall_status": self._get_overall_status(),
            "current_metrics": asdict(current_metrics),
            "service_health": self.service_health,
            "trends": trends,
            "recent_alerts": recent_alerts,
            "usage_analytics": dict(self.usage_analytics),
            "recommendations": self._generate_recommendations()
        }
    
    async def get_performance_analysis(self, hours: int = 24) -> Dict[str, Any]:
        """Get detailed performance analysis"""
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        # Filter metrics by time range
        recent_metrics = [
            m for m in self.metrics_history 
            if m.timestamp >= cutoff_time
        ]
        
        if not recent_metrics:
            return {"error": "No metrics available for the specified time range"}
        
        # Calculate statistics
        total_requests = sum(m.request_count for m in recent_metrics)
        total_errors = sum(m.error_count for m in recent_metrics)
        avg_response_time = sum(m.average_response_time for m in recent_metrics) / len(recent_metrics)
        avg_cache_hit_rate = sum(m.cache_hit_rate for m in recent_metrics) / len(recent_metrics)
        
        # Identify patterns
        patterns = self._identify_performance_patterns(recent_metrics)
        
        # Calculate throughput
        throughput = total_requests / hours if hours > 0 else 0
        
        return {
            "time_range_hours": hours,
            "total_requests": total_requests,
            "total_errors": total_errors,
            "error_rate": total_errors / max(total_requests, 1),
            "average_response_time": avg_response_time,
            "average_cache_hit_rate": avg_cache_hit_rate,
            "throughput_per_hour": throughput,
            "patterns": patterns,
            "peak_usage": self._find_peak_usage(recent_metrics),
            "reliability_score": self._calculate_reliability_score(recent_metrics)
        }
    
    async def check_circuit_breaker_status(self) -> Dict[str, Any]:
        """Check circuit breaker status and recommendations"""
        try:
            client = await get_openai_client()
            stats = client.get_stats()
            
            circuit_breaker_state = stats.get("circuit_breaker_state", "closed")
            error_count = stats.get("error_count", 0)
            request_count = stats.get("request_count", 0)
            
            # Calculate error rate
            error_rate = error_count / max(request_count, 1)
            
            # Determine status and recommendations
            status_info = {
                "state": circuit_breaker_state,
                "error_rate": error_rate,
                "request_count": request_count,
                "error_count": error_count,
                "threshold": settings.ai_circuit_breaker_threshold,
                "timeout": settings.ai_circuit_breaker_timeout,
                "status": "normal"
            }
            
            if circuit_breaker_state == "open":
                status_info.update({
                    "status": "tripped",
                    "recommendations": [
                        "Check OpenAI service status",
                        "Review recent errors",
                        "Consider adjusting rate limits",
                        "Implement exponential backoff"
                    ]
                })
            elif error_rate > 0.2:
                status_info.update({
                    "status": "warning",
                    "recommendations": [
                        "Monitor error rates closely",
                        "Consider reducing concurrency",
                        "Review error patterns"
                    ]
                })
            else:
                status_info.update({
                    "status": "healthy",
                    "recommendations": [
                        "Continue monitoring",
                        "Consider optimizing cache usage"
                    ]
                })
            
            return status_info
            
        except Exception as e:
            logger.error("Failed to check circuit breaker status", error=str(e))
            return {
                "state": "unknown",
                "status": "error",
                "error": str(e),
                "recommendations": ["Check AI service configuration"]
            }
    
    def _calculate_cache_hit_rate(self) -> float:
        """Calculate cache hit rate"""
        # This would ideally get real cache statistics
        # For now, return a placeholder
        return 0.65  # 65% cache hit rate
    
    def _estimate_cost(self, request_count: int) -> float:
        """Estimate API cost (rough calculation)"""
        # Average cost per request (very rough estimate)
        avg_cost_per_request = 0.002  # $0.002 per request
        return request_count * avg_cost_per_request
    
    def _estimate_token_usage(self, request_count: int) -> int:
        """Estimate token usage"""
        # Average tokens per request
        avg_tokens_per_request = 1500
        return request_count * avg_tokens_per_request
    
    def _calculate_average_response_time(self) -> float:
        """Calculate average response time from recent metrics"""
        if not self.metrics_history:
            return 0.0
        
        recent_metrics = list(self.metrics_history)[-10:]  # Last 10 metrics
        return sum(m.average_response_time for m in recent_metrics) / len(recent_metrics)
    
    async def _check_performance_alerts(self, metrics: AIMetrics):
        """Check for performance alerts"""
        alerts = []
        
        # High error rate alert
        error_rate = metrics.error_count / max(metrics.request_count, 1)
        if error_rate > 0.1:  # 10% error rate
            alerts.append({
                "type": "high_error_rate",
                "severity": "high" if error_rate > 0.3 else "medium",
                "message": f"High error rate detected: {error_rate:.1%}",
                "timestamp": datetime.utcnow(),
                "value": error_rate
            })
        
        # Slow response time alert
        if metrics.average_response_time > 10.0:  # 10 seconds
            alerts.append({
                "type": "slow_response",
                "severity": "medium",
                "message": f"Slow AI response time: {metrics.average_response_time:.1f}s",
                "timestamp": datetime.utcnow(),
                "value": metrics.average_response_time
            })
        
        # Circuit breaker open alert
        if metrics.circuit_breaker_state == "open":
            alerts.append({
                "type": "circuit_breaker_open",
                "severity": "critical",
                "message": "Circuit breaker is open - AI service unavailable",
                "timestamp": datetime.utcnow(),
                "value": "open"
            })
        
        # Add alerts to history
        for alert in alerts:
            self.performance_alerts.append(alert)
        
        # Log critical alerts
        for alert in alerts:
            if alert["severity"] == "critical":
                logger.error("AI service alert", **alert)
    
    def _calculate_trends(self) -> Dict[str, Any]:
        """Calculate performance trends"""
        if len(self.metrics_history) < 2:
            return {"error": "Insufficient data for trend analysis"}
        
        recent = list(self.metrics_history)[-10:]  # Last 10 metrics
        older = list(self.metrics_history)[-20:-10] if len(self.metrics_history) >= 20 else []
        
        if not older:
            return {"error": "Insufficient historical data"}
        
        # Calculate trend directions
        trends = {}
        
        # Error rate trend
        recent_error_rate = sum(m.error_count for m in recent) / max(sum(m.request_count for m in recent), 1)
        older_error_rate = sum(m.error_count for m in older) / max(sum(m.request_count for m in older), 1)
        trends["error_rate_trend"] = "increasing" if recent_error_rate > older_error_rate else "decreasing"
        trends["error_rate_change"] = recent_error_rate - older_error_rate
        
        # Response time trend
        recent_avg_response = sum(m.average_response_time for m in recent) / len(recent)
        older_avg_response = sum(m.average_response_time for m in older) / len(older)
        trends["response_time_trend"] = "increasing" if recent_avg_response > older_avg_response else "decreasing"
        trends["response_time_change"] = recent_avg_response - older_avg_response
        
        # Cache hit rate trend
        recent_cache_rate = sum(m.cache_hit_rate for m in recent) / len(recent)
        older_cache_rate = sum(m.cache_hit_rate for m in older) / len(older)
        trends["cache_hit_rate_trend"] = "increasing" if recent_cache_rate > older_cache_rate else "decreasing"
        trends["cache_hit_rate_change"] = recent_cache_rate - older_cache_rate
        
        return trends
    
    def _get_recent_alerts(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get recent alerts"""
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        return [
            alert for alert in self.performance_alerts
            if alert["timestamp"] >= cutoff_time
        ]
    
    def _update_usage_analytics(self):
        """Update usage analytics"""
        if not self.metrics_history:
            return
        
        latest = self.metrics_history[-1]
        self.usage_analytics["total_requests"] += latest.request_count
        self.usage_analytics["total_errors"] += latest.error_count
        self.usage_analytics["total_cost"] += latest.cost_estimate
        self.usage_analytics["total_tokens"] += latest.total_tokens_used
    
    def _get_overall_status(self) -> str:
        """Get overall AI service status"""
        if not self.service_health:
            return "unknown"
        
        return self.service_health.get("overall", "unknown")
    
    def _generate_recommendations(self) -> List[str]:
        """Generate optimization recommendations"""
        if not self.metrics_history:
            return ["No data available for recommendations"]
        
        recent = list(self.metrics_history)[-10:]  # Last 10 metrics
        
        recommendations = []
        
        # Cache optimization
        avg_cache_rate = sum(m.cache_hit_rate for m in recent) / len(recent)
        if avg_cache_rate < 0.5:
            recommendations.append("Consider optimizing cache TTL or cache key generation")
        
        # Error rate optimization
        total_requests = sum(m.request_count for m in recent)
        total_errors = sum(m.error_count for m in recent)
        error_rate = total_errors / max(total_requests, 1)
        
        if error_rate > 0.1:
            recommendations.append("High error rate detected - review error handling and rate limiting")
        
        # Response time optimization
        avg_response_time = sum(m.average_response_time for m in recent) / len(recent)
        if avg_response_time > 5.0:
            recommendations.append("Consider reducing request complexity or implementing more aggressive caching")
        
        # Cost optimization
        avg_cost = sum(m.cost_estimate for m in recent) / len(recent)
        if avg_cost > 0.10:  # $0.10 per metric collection
            recommendations.append("High AI usage costs - consider optimizing request frequency")
        
        if not recommendations:
            recommendations.append("AI service performance is within normal parameters")
        
        return recommendations
    
    def _identify_performance_patterns(self, metrics: List[AIMetrics]) -> List[Dict[str, Any]]:
        """Identify performance patterns"""
        patterns = []
        
        # Look for periodic error spikes
        error_rates = [m.error_count / max(m.request_count, 1) for m in metrics]
        if error_rates:
            avg_error_rate = sum(error_rates) / len(error_rates)
            for i, rate in enumerate(error_rates):
                if rate > avg_error_rate * 2:  # Double the average
                    patterns.append({
                        "type": "error_spike",
                        "timestamp": metrics[i].timestamp.isoformat(),
                        "error_rate": rate,
                        "severity": "high" if rate > avg_error_rate * 3 else "medium"
                    })
        
        return patterns
    
    def _find_peak_usage(self, metrics: List[AIMetrics]) -> Dict[str, Any]:
        """Find peak usage period"""
        if not metrics:
            return {}
        
        max_requests = max(m.request_count for m in metrics)
        peak_metric = next(m for m in metrics if m.request_count == max_requests)
        
        return {
            "timestamp": peak_metric.timestamp.isoformat(),
            "request_count": max_requests,
            "error_count": peak_metric.error_count,
            "response_time": peak_metric.average_response_time
        }
    
    def _calculate_reliability_score(self, metrics: List[AIMetrics]) -> float:
        """Calculate reliability score (0.0 - 1.0)"""
        if not metrics:
            return 0.0
        
        total_requests = sum(m.request_count for m in metrics)
        total_errors = sum(m.error_count for m in metrics)
        
        if total_requests == 0:
            return 1.0
        
        success_rate = (total_requests - total_errors) / total_requests
        
        # Adjust for circuit breaker trips
        circuit_breaker_penalty = 0
        for m in metrics:
            if m.circuit_breaker_state == "open":
                circuit_breaker_penalty += 0.1
        
        reliability = max(0.0, success_rate - circuit_breaker_penalty)
        return min(1.0, reliability)
    
    def _create_fallback_metrics(self) -> AIMetrics:
        """Create fallback metrics when collection fails"""
        return AIMetrics(
            timestamp=datetime.utcnow(),
            request_count=0,
            success_count=0,
            error_count=0,
            average_response_time=0.0,
            total_tokens_used=0,
            cost_estimate=0.0,
            cache_hit_rate=0.0,
            circuit_breaker_state="unknown",
            active_tasks=0,
            completed_tasks=0
        )


# Global AI monitor instance
ai_monitor = AIMonitor()


async def get_ai_monitor() -> AIMonitor:
    """Get AI monitor instance"""
    return ai_monitor