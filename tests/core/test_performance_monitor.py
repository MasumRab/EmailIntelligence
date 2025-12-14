
import pytest
import asyncio
from unittest.mock import MagicMock, patch
from src.core.performance_monitor import performance_monitor, PerformanceMonitor, log_performance

@pytest.fixture
def clean_monitor():
    # Reset monitor state
    monitor = PerformanceMonitor()
    yield monitor
    monitor.shutdown()

@pytest.mark.asyncio
async def test_log_performance_decorator_async():
    @log_performance(operation="test_async_op")
    async def async_op():
        return "success"

    # Patch the global monitor instance to verify it receives the call
    with patch('src.core.performance_monitor.performance_monitor') as mock_monitor:
        result = await async_op()
        assert result == "success"
        # It should call log_performance
        assert mock_monitor.log_performance.called
        # Check args
        args = mock_monitor.log_performance.call_args[0][0]
        assert args['operation'] == "test_async_op"
        assert 'duration_seconds' in args

def test_log_performance_decorator_sync():
    @log_performance(operation="test_sync_op")
    def sync_op():
        return "success"

    with patch('src.core.performance_monitor.performance_monitor') as mock_monitor:
        result = sync_op()
        assert result == "success"
        assert mock_monitor.log_performance.called
        args = mock_monitor.log_performance.call_args[0][0]
        assert args['operation'] == "test_sync_op"

def test_record_metric():
    monitor = PerformanceMonitor()
    monitor.record_metric("test_metric", 100)

    metrics = monitor.get_recent_metrics("test_metric")
    assert len(metrics) == 1
    assert metrics[0].value == 100
    monitor.shutdown()

def test_log_performance_legacy_mapping():
    monitor = PerformanceMonitor()
    entry = {
        "operation": "legacy_op",
        "duration_seconds": 0.5,
        "timestamp": "2023-01-01T00:00:00Z"
    }

    monitor.log_performance(entry)

    # Should be recorded as 'operation_duration'
    metrics = monitor.get_recent_metrics("operation_duration")
    assert len(metrics) == 1
    assert metrics[0].value == 500.0  # converted to ms
    assert metrics[0].tags['operation'] == "legacy_op"
    monitor.shutdown()
