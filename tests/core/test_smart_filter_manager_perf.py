
import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch
from src.core.smart_filter_manager import SmartFilterManager, EmailFilter, _EmailContext

@pytest.fixture
def mock_caching_manager():
    with patch("src.core.smart_filter_manager.EnhancedCachingManager") as MockClass:
        mock_instance = MockClass.return_value
        mock_instance.get = AsyncMock(return_value=None)  # Cache miss by default
        mock_instance.set = AsyncMock()
        mock_instance.delete = AsyncMock()
        mock_instance._ensure_initialized = AsyncMock()
        mock_instance.close = AsyncMock()
        yield mock_instance

@pytest.fixture
def smart_filter_manager(mock_caching_manager):
    # Use memory db
    manager = SmartFilterManager(db_path=":memory:")
    # Mock _db_execute to count calls
    manager._original_db_execute = manager._db_execute
    manager._db_execute = MagicMock(side_effect=manager._original_db_execute)
    return manager

@pytest.mark.asyncio
async def test_apply_filters_n_plus_one_update(smart_filter_manager):
    await smart_filter_manager._ensure_initialized()

    # Create multiple filters that will match
    # We'll create 5 filters that look for "test" in subject
    for i in range(5):
        await smart_filter_manager.add_custom_filter(
            name=f"Filter {i}",
            description="Test filter",
            criteria={"subject_keywords": ["test"]},
            actions={"add_label": "Test"},
            priority=10
        )

    # Reset mock counts (add_custom_filter calls _db_execute)
    smart_filter_manager._db_execute.reset_mock()
    smart_filter_manager.caching_manager.delete.reset_mock()

    # Apply filters to an email that matches all of them
    email_data = {
        "id": "email_1",
        "subject": "This is a test email",
        "content": "Content",
        "sender": "sender@example.com"
    }

    await smart_filter_manager.apply_filters_to_email(email_data)

    # We expect 5 updates to usage_count (one per filter)
    # Plus potentially other queries?
    # _update_filter_usage calls _db_execute once per filter.

    # Count how many UPDATE email_filters calls happened
    update_calls = 0
    for call in smart_filter_manager._db_execute.call_args_list:
        query = call[0][0]
        if "UPDATE email_filters" in query and "usage_count" in query:
            update_calls += 1

    print(f"Update calls: {update_calls}")

    # Count cache invalidations
    # _update_filter_usage calls delete("active_filters_sorted")
    cache_delete_calls = smart_filter_manager.caching_manager.delete.call_count
    print(f"Cache delete calls: {cache_delete_calls}")

    # Assert batched behavior (1 update call, 1 cache invalidation)
    assert update_calls == 1, f"Expected 1 update call, got {update_calls}"
    assert cache_delete_calls == 1, f"Expected 1 cache delete call, got {cache_delete_calls}"

    await smart_filter_manager.close()
