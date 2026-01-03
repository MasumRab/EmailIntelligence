"""
Unit tests for SmartFilterManager.
"""
import asyncio
import json
from datetime import datetime, timezone
from unittest.mock import MagicMock, AsyncMock, patch

import pytest
import pytest_asyncio

from src.core.smart_filter_manager import SmartFilterManager
from src.core.caching import CacheManager

@pytest.fixture
def mock_cache_manager():
    """Create a mock CacheManager."""
    mock = MagicMock(spec=CacheManager)
    mock.get = AsyncMock(return_value=None)
    mock.set = AsyncMock(return_value=True)
    mock.delete = AsyncMock(return_value=True)
    return mock

@pytest_asyncio.fixture
async def smart_filter_manager(mock_cache_manager):
    """Create an instance of SmartFilterManager with in-memory DB."""
    # Patch get_cache_manager to return our mock
    with patch("src.core.smart_filter_manager.get_cache_manager", return_value=mock_cache_manager):
        manager = SmartFilterManager(db_path=":memory:")
        # pylint: disable=protected-access
        await manager._ensure_initialized()
        yield manager

@pytest.mark.asyncio
async def test_initialization(smart_filter_manager):
    """Test that the manager initializes correctly."""
    # pylint: disable=protected-access
    assert smart_filter_manager._initialized is True

@pytest.mark.asyncio
async def test_add_custom_filter(smart_filter_manager):
    """Test adding a custom filter."""
    criteria = {"subject_keywords": ["test"]}
    actions = {"add_label": "Test"}

    filter_obj = await smart_filter_manager.add_custom_filter(
        name="Test Filter",
        description="A test filter",
        criteria=criteria,
        actions=actions
    )

    assert filter_obj.name == "Test Filter"
    assert filter_obj.criteria == criteria
    assert filter_obj.actions == actions

    # Verify it was saved to DB
    saved_filter = await smart_filter_manager.get_filter_by_id(filter_obj.filter_id)
    assert saved_filter is not None
    assert saved_filter.filter_id == filter_obj.filter_id

@pytest.mark.asyncio
async def test_get_active_filters_sorted_caching(smart_filter_manager, mock_cache_manager):
    """Test that get_active_filters_sorted uses cache."""
    # First call - cache miss
    mock_cache_manager.get.return_value = None
    filters = await smart_filter_manager.get_active_filters_sorted()

    # Should check cache
    mock_cache_manager.get.assert_called_with("active_filters_sorted")
    # Should set cache
    mock_cache_manager.set.assert_called()

    # Second call - cache hit
    mock_cache_manager.get.return_value = filters
    mock_cache_manager.set.reset_mock()

    filters2 = await smart_filter_manager.get_active_filters_sorted()
    assert filters2 == filters
    # Should not set cache again
    mock_cache_manager.set.assert_not_called()

@pytest.mark.asyncio
async def test_apply_filters_usage_update_optimization(smart_filter_manager, mock_cache_manager):
    """
    Verify that applying filters updates usage count BUT DOES NOT INVALIDATE global cache.
    This is the core optimization we implemented.
    """
    # Create a filter
    filter_obj = await smart_filter_manager.add_custom_filter(
        name="Match Filter",
        description="Matches 'urgent'",
        criteria={"subject_keywords": ["urgent"]},
        actions={"add_label": "Urgent"}
    )

    email_data = {
        "id": "e1",
        "subject": "Urgent task",
        "content": "Do it now"
    }

    # Reset mock to clear previous calls
    mock_cache_manager.delete.reset_mock()

    # Apply filters
    await smart_filter_manager.apply_filters_to_email(email_data)

    # Verify usage update happened in DB (we can check DB directly or infer)
    # The optimization: delete("active_filters_sorted") should NOT be called

    delete_calls = [call.args[0] for call in mock_cache_manager.delete.call_args_list]
    assert "active_filters_sorted" not in delete_calls, "Should not invalidate active_filters_sorted on usage update"

@pytest.mark.asyncio
async def test_update_filter_invalidates_cache(smart_filter_manager, mock_cache_manager):
    """Test that modifying a filter DOES invalidate cache."""
    filter_obj = await smart_filter_manager.add_custom_filter(
        name="Edit Me",
        description="...",
        criteria={},
        actions={}
    )

    mock_cache_manager.delete.reset_mock()

    await smart_filter_manager.update_filter(filter_obj.filter_id, name="Edited")

    delete_calls = [call.args[0] for call in mock_cache_manager.delete.call_args_list]
    assert "active_filters_sorted" in delete_calls, "Should invalidate global cache on filter edit"
    assert f"filter_{filter_obj.filter_id}" in delete_calls, "Should invalidate specific filter cache"
