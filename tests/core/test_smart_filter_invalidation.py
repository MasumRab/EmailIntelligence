
import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock, call
from src.core.smart_filter_manager import SmartFilterManager, EmailFilter, _EmailContext

@pytest.fixture
def manager_with_mock_cache():
    manager = SmartFilterManager(db_path=":memory:")
    manager.caching_manager = AsyncMock()
    # Mock methods that are called
    manager.caching_manager.get.return_value = None
    manager.caching_manager.delete = AsyncMock()
    return manager

@pytest.mark.asyncio
async def test_batch_invalidation(manager_with_mock_cache):
    """Verify that applying multiple filters results in single cache invalidation."""

    # Create two filters that will match
    filter1 = EmailFilter(
        filter_id="f1",
        name="Filter 1",
        description="desc",
        criteria={"subject_keywords": ["match"]},
        actions={},
        priority=10,
        effectiveness_score=0.0,
        created_at=None,
        last_used=None,
        usage_count=0,
        false_positive_rate=0.0,
        performance_metrics={},
        is_active=True
    )

    filter2 = EmailFilter(
        filter_id="f2",
        name="Filter 2",
        description="desc",
        criteria={"subject_keywords": ["match"]},
        actions={},
        priority=5,
        effectiveness_score=0.0,
        created_at=None,
        last_used=None,
        usage_count=0,
        false_positive_rate=0.0,
        performance_metrics={},
        is_active=True
    )

    # Mock get_active_filters_sorted to return these filters
    manager_with_mock_cache.get_active_filters_sorted = AsyncMock(return_value=[filter1, filter2])

    # Mock _apply_filter_to_email to return True
    manager_with_mock_cache._apply_filter_to_email = AsyncMock(return_value=True)

    # Mock _db_execute to avoid DB errors
    manager_with_mock_cache._db_execute = MagicMock()

    email_data = {"subject": "match", "sender": "test@example.com", "id": "e1"}

    await manager_with_mock_cache.apply_filters_to_email(email_data)

    # Verify that caching_manager.delete was called exactly ONCE for "active_filters_sorted"
    # It might be called for other things (though current impl doesn't), but we care about this specific key

    delete_calls = manager_with_mock_cache.caching_manager.delete.call_args_list
    sorted_invalidation_calls = [c for c in delete_calls if c[0][0] == "active_filters_sorted"]

    assert len(sorted_invalidation_calls) == 1, f"Expected 1 invalidation, got {len(sorted_invalidation_calls)}"
