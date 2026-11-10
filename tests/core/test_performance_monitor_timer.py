"""`time_function(...)` used as a context manager must record its metric.

`PerformanceMonitor.time_function(name)` returns a `TimerContext` when it is
called with a metric name. `TimerContext.__exit__` recorded the timing with
`self.record_metric(...)` — but `self` there is the context object, not the
monitor, so exiting the context raised `AttributeError` and no metric was ever
written. `SecurityMiddleware` drives exactly this path for every request whose
performance monitoring is enabled, so the failure was not hypothetical.
"""

import pytest

from src.core.performance_monitor import OptimizedPerformanceMonitor


@pytest.fixture
def monitor(tmp_path):
    m = OptimizedPerformanceMonitor(log_file=str(tmp_path / "perf.jsonl"))
    yield m
    m.shutdown()


def test_time_function_context_manager_records_metric(monitor):
    """Exiting the context must record one metric, not raise."""
    with monitor.time_function("unit_test_operation", sample_rate=1.0):
        pass

    metrics = monitor.get_recent_metrics("unit_test_operation")
    assert len(metrics) == 1
    assert metrics[0].name == "unit_test_operation"
    assert metrics[0].unit == "ms"
    assert metrics[0].value >= 0


def test_time_function_context_manager_records_on_exception(monitor):
    """An exception inside the block still records, then propagates."""
    with pytest.raises(RuntimeError):
        with monitor.time_function("unit_test_raises", sample_rate=1.0):
            raise RuntimeError("boom")

    assert len(monitor.get_recent_metrics("unit_test_raises")) == 1


def test_time_function_context_carries_tags(monitor):
    """Tags passed to time_function reach the recorded metric."""
    with monitor.time_function(
        "unit_test_tagged", tags={"endpoint": "/x"}, sample_rate=1.0
    ):
        pass

    metrics = monitor.get_recent_metrics("unit_test_tagged")
    assert len(metrics) == 1
    assert metrics[0].tags == {"endpoint": "/x"}
