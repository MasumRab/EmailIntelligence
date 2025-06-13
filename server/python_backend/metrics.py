"""
Metrics module for the EmailIntelligence backend.

This module provides Prometheus metrics for monitoring the application.
"""

import time
from typing import Callable, Dict, Optional

from fastapi import FastAPI, Request, Response
from prometheus_client import Counter, Gauge, Histogram, Summary, generate_latest

# Define metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status_code"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"]
)

REQUESTS_IN_PROGRESS = Gauge(
    "http_requests_in_progress",
    "Number of HTTP requests in progress",
    ["method", "endpoint"]
)

EMAIL_PROCESSING_TIME = Summary(
    "email_processing_seconds",
    "Time spent processing emails",
    ["operation"]
)

EMAIL_COUNT = Counter(
    "emails_processed_total",
    "Total number of emails processed",
    ["status", "category"]
)

AI_ANALYSIS_CONFIDENCE = Histogram(
    "ai_analysis_confidence",
    "Confidence scores of AI analysis",
    ["analysis_type"]
)

DATABASE_QUERY_TIME = Histogram(
    "database_query_seconds",
    "Time spent executing database queries",
    ["query_type"]
)

def setup_metrics(app: FastAPI) -> None:
    """
    Set up metrics middleware for the FastAPI application.
    
    Args:
        app: The FastAPI application
    """
    @app.middleware("http")
    async def metrics_middleware(request: Request, call_next: Callable) -> Response:
        # Record request start time
        start_time = time.time()
        
        # Increment in-progress requests
        REQUESTS_IN_PROGRESS.labels(
            method=request.method,
            endpoint=request.url.path
        ).inc()
        
        # Process the request
        try:
            response = await call_next(request)
            status_code = response.status_code
        except Exception as e:
            # Handle exceptions
            status_code = 500
            raise e
        finally:
            # Record request duration
            duration = time.time() - start_time
            REQUEST_LATENCY.labels(
                method=request.method,
                endpoint=request.url.path
            ).observe(duration)
            
            # Increment request count
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=request.url.path,
                status_code=status_code
            ).inc()
            
            # Decrement in-progress requests
            REQUESTS_IN_PROGRESS.labels(
                method=request.method,
                endpoint=request.url.path
            ).dec()
        
        return response
    
    @app.get("/api/metrics")
    async def metrics():
        """Endpoint to expose Prometheus metrics."""
        return Response(
            content=generate_latest(),
            media_type="text/plain"
        )

def record_email_processing(operation: str, duration: float) -> None:
    """
    Record the time spent processing an email.
    
    Args:
        operation: The type of operation (e.g., 'analyze', 'filter', 'categorize')
        duration: The time spent in seconds
    """
    EMAIL_PROCESSING_TIME.labels(operation=operation).observe(duration)

def record_email_processed(status: str, category: Optional[str] = None) -> None:
    """
    Record that an email has been processed.
    
    Args:
        status: The status of the processing (e.g., 'success', 'failure')
        category: The category of the email (if applicable)
    """
    EMAIL_COUNT.labels(
        status=status,
        category=category or "unknown"
    ).inc()

def record_ai_analysis_confidence(analysis_type: str, confidence: float) -> None:
    """
    Record the confidence score of an AI analysis.
    
    Args:
        analysis_type: The type of analysis (e.g., 'sentiment', 'topic', 'intent')
        confidence: The confidence score (0.0-1.0)
    """
    AI_ANALYSIS_CONFIDENCE.labels(analysis_type=analysis_type).observe(confidence)

def record_database_query_time(query_type: str, duration: float) -> None:
    """
    Record the time spent executing a database query.
    
    Args:
        query_type: The type of query (e.g., 'select', 'insert', 'update', 'delete')
        duration: The time spent in seconds
    """
    DATABASE_QUERY_TIME.labels(query_type=query_type).observe(duration)

class DatabaseMetricsMiddleware:
    """Middleware to record database query metrics."""
    
    def __init__(self):
        self.query_times: Dict[str, float] = {}
    
    def before_query(self, query_type: str) -> None:
        """Record the start time of a query."""
        self.query_times[query_type] = time.time()
    
    def after_query(self, query_type: str) -> None:
        """Record the duration of a query."""
        if query_type in self.query_times:
            duration = time.time() - self.query_times[query_type]
            record_database_query_time(query_type, duration)
            del self.query_times[query_type]