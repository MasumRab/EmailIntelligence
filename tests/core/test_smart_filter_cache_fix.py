
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from src.core.smart_filter_manager import SmartFilterManager, EmailFilter
from datetime import datetime, timezone

@pytest.fixture
def mock_cache_manager():
    with patch("src.core.smart_filter_manager.get_cache_manager") as mock_get:
        mock_cache = AsyncMock()
        mock_get.return_value = mock_cache
        yield mock_cache

@pytest.mark.asyncio
async def test_smart_filter_initialization(mock_cache_manager):
    """Verify that SmartFilterManager initializes correctly with CacheManager."""
    manager = SmartFilterManager(db_path=":memory:")
    assert manager.caching_manager == mock_cache_manager

    # It should NOT call _ensure_initialized on cache manager anymore
    await manager._ensure_initialized()

    # Check that _ensure_initialized was NOT called on the mock
    # (AsyncMock creates children automatically when accessed)
    # If the code tried to call it, it would be recorded.
    # Since we removed the call, it should be empty (or not awaited).
    # However, simply accessing it on the mock creates it.
    # But we can check calls.
    # But wait, if the code was `await self.caching_manager._ensure_initialized()`,
    # it accesses the attribute and then awaits the result.
    # We can check mock_calls.

    # Note: _ensure_initialized is NOT a standard method of CacheManager,
    # so accessing it on the mock is the only way it would exist.
    # We want to ensure it is NOT called.
    assert len(mock_cache_manager._ensure_initialized.mock_calls) == 0

@pytest.mark.asyncio
async def test_batch_update_optimization(mock_cache_manager):
    """Verify concurrent cache invalidation."""
    manager = SmartFilterManager(db_path=":memory:")
    # Mock _db_executemany to avoid database errors
    manager._db_executemany = MagicMock()

    filters = [
        EmailFilter(
            filter_id=f"f{i}",
            name=f"Filter {i}",
            description="Test",
            criteria={},
            actions={},
            priority=5,
            effectiveness_score=0.0,
            created_at=datetime.now(timezone.utc),
            last_used=datetime.now(timezone.utc),
            usage_count=0,
            false_positive_rate=0.0,
            performance_metrics={},
            is_active=True
        ) for i in range(5)
    ]

    await manager._batch_update_filter_usage(filters)

    # Verify delete was called 5 times
    assert mock_cache_manager.delete.call_count == 5

    # Verify calls
    expected_calls = [(f"filter_f{i}",) for i in range(5)]
    # The order might vary because of asyncio.gather if it wasn't a list comprehension passed to gather *args
    # But here we passed a generator/list to gather, but gather runs them concurrently.
    # However, call_args_list should contain all of them.

    actual_calls = [c[0] for c in mock_cache_manager.delete.call_args_list]
    for call in expected_calls:
        assert call in actual_calls
