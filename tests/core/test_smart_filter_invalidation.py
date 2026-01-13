import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from src.core.smart_filter_manager import SmartFilterManager, EmailFilter
from src.core.enhanced_caching import EnhancedCachingManager
from datetime import datetime, timezone

# Mock log_performance decorator to avoid issues
def mock_log_performance(operation=None):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
        return wrapper
    return decorator

@pytest.fixture
def mock_caching_manager():
    mock = AsyncMock(spec=EnhancedCachingManager)
    mock.get = AsyncMock(return_value=None)
    mock.set = AsyncMock()
    mock.delete = AsyncMock()
    mock._ensure_initialized = AsyncMock()
    return mock

@pytest.mark.asyncio
async def test_update_filter_usage_invalidation_behavior(mock_caching_manager):
    """
    Verifies that updating filter usage does NOT invalidate the global active filter list.
    (This tests the optimization/fix)
    """
    # 1. Setup Manager with in-memory DB
    with patch("src.core.smart_filter_manager.log_performance", mock_log_performance):
        manager = SmartFilterManager(":memory:")
        manager.caching_manager = mock_caching_manager

        # Initialize DB
        await manager._ensure_initialized()

        now = datetime.now(timezone.utc)

        # 2. Create a test filter
        filter_obj = EmailFilter(
            filter_id="test_filter_1",
            name="Test Filter",
            description="Test",
            criteria={"subject_keywords": ["test"]},
            actions={"add_label": "test"},
            priority=10,
            effectiveness_score=0.0,
            created_at=now,
            last_used=now,
            usage_count=0,
            false_positive_rate=0.0,
            performance_metrics={},
            is_active=True
        )

        # Insert raw valid data for filter
        await manager._save_filter_async(filter_obj) # this uses caching_manager.set

        # Reset mock calls from setup
        mock_caching_manager.delete.reset_mock()

        # 3. Trigger _update_filter_usage via apply_filters_to_email
        # We need apply_filters_to_email to actually match
        # Mock get_active_filters_sorted to return our filter
        manager.get_active_filters_sorted = AsyncMock(return_value=[filter_obj])

        email_data = {"id": 1, "subject": "This is a test email", "body": "content"}

        # 4. Run the method under test
        await manager.apply_filters_to_email(email_data)

        # 5. Check if delete was called for "active_filters_sorted"
        # Before optimization: it SHOULD be called.
        # After optimization: it SHOULD NOT be called.

        delete_calls = [call.args[0] for call in mock_caching_manager.delete.call_args_list]

        # We assert that "active_filters_sorted" is NOT in the delete calls
        # This assert WILL FAIL until we apply the fix
        assert "active_filters_sorted" not in delete_calls, \
            "Optimization Failure: active_filters_sorted cache was invalidated during usage update (N+1 bottleneck)"
