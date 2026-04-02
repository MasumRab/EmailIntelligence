"""
Tests for src/core/performance_monitor.py
"""

import pytest
import time
from src.core.performance_monitor import (
    ProcessingEvent,
    AggregatedMetric,
)


class TestProcessingEvent:
    """Tests for ProcessingEvent dataclass."""

    def test_processing_event_minimal(self):
        """Test ProcessingEvent creation with minimal required fields."""
        event = ProcessingEvent(
            event_type="model_load",
            model_name="sentiment_model",
            workflow_name=None,
            start_time=1705312200.0,
            end_time=None,
            success=True,
            details={},
        )

        assert event.event_type == "model_load"
        assert event.model_name == "sentiment_model"
        assert event.workflow_name is None
        assert event.success is True
        assert event.end_time is None

    def test_processing_event_complete(self):
        """Test ProcessingEvent creation with all fields."""
        event = ProcessingEvent(
            event_type="workflow_execute",
            model_name=None,
            workflow_name="email_processing",
            start_time=1705312200.0,
            end_time=1705312210.0,
            success=True,
            details={"nodes_executed": 5, "total_time": 10.0},
        )

        assert event.event_type == "workflow_execute"
        assert event.workflow_name == "email_processing"
        assert event.end_time == 1705312210.0
        assert event.success is True
        assert event.details == {"nodes_executed": 5, "total_time": 10.0}

    def test_processing_event_failed(self):
        """Test ProcessingEvent for failed event."""
        event = ProcessingEvent(
            event_type="model_unload",
            model_name="topic_model",
            workflow_name=None,
            start_time=1705312200.0,
            end_time=1705312205.0,
            success=False,
            details={"error": "memory_error"},
        )

        assert event.success is False
        assert event.details["error"] == "memory_error"

    def test_processing_event_types(self):
        """Test ProcessingEvent field types."""
        event = ProcessingEvent(
            event_type="api_call",
            model_name="urgency_model",
            workflow_name=None,
            start_time=1705312200.0,
            end_time=1705312202.0,
            success=True,
            details={},
        )

        assert isinstance(event.event_type, str)
        assert isinstance(event.model_name, str)
        assert isinstance(event.start_time, float)
        assert isinstance(event.end_time, float)
        assert isinstance(event.success, bool)
        assert isinstance(event.details, dict)

    def test_processing_event_multiple_workflows(self):
        """Test ProcessingEvent for different workflow types."""
        workflows = [
            "email_categorization",
            "smart_filter_generation",
            "batch_email_processing",
        ]

        for workflow_name in workflows:
            event = ProcessingEvent(
                event_type="workflow_execute",
                model_name=None,
                workflow_name=workflow_name,
                start_time=time.time(),
                end_time=None,
                success=True,
                details={},
            )
            assert event.workflow_name == workflow_name

    def test_processing_event_event_types(self):
        """Test various event types are accepted."""
        event_types = [
            "model_load",
            "model_unload",
            "workflow_execute",
            "workflow_error",
            "api_call",
            "cache_hit",
            "cache_miss",
        ]

        for event_type in event_types:
            event = ProcessingEvent(
                event_type=event_type,
                model_name="test_model",
                workflow_name=None,
                start_time=time.time(),
                end_time=None,
                success=True,
                details={},
            )
            assert event.event_type == event_type


class TestAggregatedMetric:
    """Tests for AggregatedMetric dataclass."""

    def test_aggregated_metric_creation(self):
        """Test AggregatedMetric creation."""
        metric = AggregatedMetric(
            name="response_time",
            count=100,
            sum=25.0,
            avg=0.25,
            min=0.01,
            max=2.5,
            p95=0.6,
            p99=1.5,
            timestamp=1705312200.0,
            tags={"endpoint": "api"},
        )

        assert metric.name == "response_time"
        assert metric.count == 100
        assert metric.sum == 25.0
        assert metric.avg == 0.25
        assert metric.min == 0.01
        assert metric.max == 2.5

    def test_aggregated_metric_percentiles(self):
        """Test AggregatedMetric percentile fields."""
        metric = AggregatedMetric(
            name="latency",
            count=50,
            sum=25.0,
            avg=0.5,
            min=0.0,
            max=1.0,
            p95=0.85,
            p99=0.95,
            timestamp=1705312200.0,
            tags={},
        )

        assert metric.p95 == 0.85
        assert metric.p99 == 0.95

    def test_aggregated_metric_types(self):
        """Test AggregatedMetric field types."""
        metric = AggregatedMetric(
            name="test_metric",
            count=10,
            sum=55.0,
            avg=5.5,
            min=1.0,
            max=10.0,
            p95=9.0,
            p99=9.9,
            timestamp=1705312200.0,
            tags={"test": "value"},
        )

        assert isinstance(metric.name, str)
        assert isinstance(metric.count, int)
        assert isinstance(metric.avg, float)
        assert isinstance(metric.timestamp, float)
        assert isinstance(metric.tags, dict)