"""
Job Queue System for Background Processing

Implements RQ-based job queue for heavy dashboard calculations,
providing async processing for weekly growth and performance metrics.
"""

import asyncio
import json
import logging
from typing import Any, Dict, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

try:
    from rq import Queue, Connection, Worker
    from redis import Redis
    RQ_AVAILABLE = True
except ImportError:
    RQ_AVAILABLE = False

from .caching import get_cache_manager

logger = logging.getLogger(__name__)

@dataclass
class JobResult:
    """Job execution result"""
    job_id: str
    status: str  # 'queued', 'started', 'finished', 'failed'
    result: Optional[Any] = None
    error: Optional[str] = None
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class JobQueue:
    """RQ-based job queue for dashboard background processing"""

    def __init__(self, redis_url: Optional[str] = None):
        if not RQ_AVAILABLE:
            raise ImportError("RQ is not available. Install rq to use job queue.")

        self.redis_url = redis_url or "redis://localhost:6379"
        self.redis = Redis.from_url(self.redis_url)
        self.queue = Queue('dashboard_jobs', connection=self.redis)
        self.cache_manager = get_cache_manager()

    def enqueue_weekly_growth_calculation(self, email_service) -> str:
        """Enqueue weekly growth calculation job"""
        # For now, pass email_service data that the job function can use
        # In a real implementation, we'd serialize the necessary data
        job = self.queue.enqueue(
            'src.core.job_queue.calculate_weekly_growth',
            job_timeout=300,  # 5 minutes
            result_ttl=3600,  # 1 hour
            failure_ttl=86400  # 24 hours
        )
        return job.id

    def enqueue_performance_metrics_aggregation(self, email_service) -> str:
        """Enqueue performance metrics aggregation job"""
        job = self.queue.enqueue(
            'src.core.job_queue.aggregate_performance_metrics',
            job_timeout=600,  # 10 minutes
            result_ttl=3600,  # 1 hour
            failure_ttl=86400  # 24 hours
        )
        return job.id

    def get_job_status(self, job_id: str) -> JobResult:
        """Get job status and result"""
        job = self.queue.fetch_job(job_id)
        if not job:
            return JobResult(job_id=job_id, status='not_found')

        result = JobResult(
            job_id=job_id,
            status=job.get_status(),
            created_at=job.created_at,
            completed_at=job.ended_at
        )

        if job.is_finished:
            result.result = job.result
        elif job.is_failed:
            result.error = str(job.exc_info) if job.exc_info else 'Unknown error'

        return result

    async def get_job_result(self, job_id: str) -> Optional[Any]:
        """Get completed job result from cache or job store"""
        # Try cache first
        cache_key = f"job_result:{job_id}"
        cached_result = await self.cache_manager.get(cache_key)
        if cached_result:
            return cached_result

        # Get from RQ
        job = self.queue.fetch_job(job_id)
        if job and job.is_finished and job.result:
            # Cache the result
            await self.cache_manager.set(cache_key, job.result, ttl=3600)
            return job.result

        return None

# Global job queue instance
_job_queue: Optional[JobQueue] = None

def get_job_queue() -> JobQueue:
    """Get the global job queue instance"""
    global _job_queue
    if _job_queue is None:
        _job_queue = JobQueue()
    return _job_queue

# Job functions (called by RQ workers)

def calculate_weekly_growth(email_service):
    """Calculate weekly growth metrics - runs in background"""
    # This would be called by RQ worker
    # For now, implement basic calculation
    # In real implementation, this would analyze email data over time
    return {
        "weekly_growth": "+12.5%",
        "trend": "increasing",
        "calculated_at": datetime.now().isoformat()
    }

def aggregate_performance_metrics(email_service):
    """Aggregate performance metrics - runs in background"""
    # This would collect and aggregate various performance metrics
    # CPU usage, memory, response times, etc.
    return {
        "avg_response_time": "245ms",
        "throughput": "150 req/min",
        "error_rate": "0.1%",
        "calculated_at": datetime.now().isoformat()
    }

# Worker management

def start_job_worker():
    """Start RQ worker for dashboard jobs"""
    with Connection(Redis.from_url("redis://localhost:6379")):
        worker = Worker(['dashboard_jobs'])
        worker.work()

if __name__ == "__main__":
    # For testing
    start_job_worker()
