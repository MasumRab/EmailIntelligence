"""
Tests for src/core/job_queue.py
"""

import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock
from src.core.job_queue import (
    JobResult,
    calculate_weekly_growth,
    aggregate_performance_metrics,
    RQ_AVAILABLE,
)


class TestJobResult:
    """Tests for JobResult dataclass."""

    def test_job_result_creation(self):
        """Test JobResult creation with required fields."""
        result = JobResult(job_id="test123", status="queued")
        
        assert result.job_id == "test123"
        assert result.status == "queued"
        assert result.result is None
        assert result.error is None
        assert result.created_at is None
        assert result.completed_at is None

    def test_job_result_with_all_fields(self):
        """Test JobResult creation with all fields."""
        created = datetime.now()
        completed = datetime.now()
        
        result = JobResult(
            job_id="test456",
            status="finished",
            result={"data": "test"},
            error=None,
            created_at=created,
            completed_at=completed,
        )
        
        assert result.job_id == "test456"
        assert result.status == "finished"
        assert result.result == {"data": "test"}
        assert result.error is None
        assert result.created_at == created
        assert result.completed_at == completed

    def test_job_result_with_error(self):
        """Test JobResult with error field."""
        result = JobResult(
            job_id="test789",
            status="failed",
            error="Some error occurred",
        )
        
        assert result.job_id == "test789"
        assert result.status == "failed"
        assert result.error == "Some error occurred"


class TestJobFunctions:
    """Tests for job queue functions."""

    def test_calculate_weekly_growth(self):
        """Test calculate_weekly_growth function."""
        # Pass None as email_service since we're testing the function directly
        result = calculate_weekly_growth(None)
        
        assert isinstance(result, dict)
        assert "weekly_growth" in result
        assert "trend" in result
        assert "calculated_at" in result
        assert result["weekly_growth"] == "+12.5%"
        assert result["trend"] == "increasing"

    def test_calculate_weekly_growth_has_timestamp(self):
        """Test calculate_weekly_growth returns valid ISO timestamp."""
        result = calculate_weekly_growth(None)
        
        # Should be able to parse the timestamp
        calculated_at = result["calculated_at"]
        datetime.fromisoformat(calculated_at)

    def test_aggregate_performance_metrics(self):
        """Test aggregate_performance_metrics function."""
        result = aggregate_performance_metrics(None)
        
        assert isinstance(result, dict)
        assert "avg_response_time" in result
        assert "throughput" in result
        assert "error_rate" in result
        assert "calculated_at" in result
        assert result["avg_response_time"] == "245ms"
        assert result["throughput"] == "150 req/min"
        assert result["error_rate"] == "0.1%"

    def test_aggregate_performance_metrics_has_timestamp(self):
        """Test aggregate_performance_metrics returns valid ISO timestamp."""
        result = aggregate_performance_metrics(None)
        
        # Should be able to parse the timestamp
        calculated_at = result["calculated_at"]
        datetime.fromisoformat(calculated_at)


class TestRQAvailability:
    """Tests for RQ availability check."""

    def test_rq_available_is_boolean(self):
        """Test RQ_AVAILABLE is a boolean."""
        assert isinstance(RQ_AVAILABLE, bool)

    @pytest.mark.skipif(not RQ_AVAILABLE, reason="RQ not available")
    def test_job_queue_import_when_rq_available(self):
        """Test JobQueue can be imported when RQ is available."""
        # This test is skipped if RQ is not available
        from src.core.job_queue import JobQueue
        assert JobQueue is not None