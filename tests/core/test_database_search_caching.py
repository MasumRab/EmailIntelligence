
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.core.database import DatabaseManager
from src.core.enhanced_caching import EnhancedCachingManager

@pytest.fixture
def db_manager():
    db = DatabaseManager()
    # Mock internal data
    db.emails_data = [
        {"id": 1, "subject": "Test Email 1", "sender": "user1@example.com", "content": "content1"},
        {"id": 2, "subject": "Test Email 2", "sender": "user2@example.com", "content": "content2"},
    ]
    db._sort_and_paginate_emails = AsyncMock(side_effect=lambda emails, limit=50, offset=0: emails[:limit])
    db._initialized = True
    return db

@pytest.mark.asyncio
async def test_search_emails_with_limit_caching(db_manager):
    # Mock caching manager
    db_manager.caching_manager = MagicMock(spec=EnhancedCachingManager)
    db_manager.caching_manager.get_query_result.return_value = None

    # First call - cache miss
    result1 = await db_manager.search_emails_with_limit("Test", limit=10)

    # Verify get_query_result was called
    db_manager.caching_manager.get_query_result.assert_called_with("search:Test:10")

    # Verify put_query_result was called
    db_manager.caching_manager.put_query_result.assert_called_with("search:Test:10", result1)

    # Reset mock and set return value for cache hit
    db_manager.caching_manager.reset_mock()
    db_manager.caching_manager.get_query_result.return_value = result1

    # Second call - cache hit
    result2 = await db_manager.search_emails_with_limit("Test", limit=10)

    # Verify get_query_result was called
    db_manager.caching_manager.get_query_result.assert_called_with("search:Test:10")

    # Verify put_query_result was NOT called
    db_manager.caching_manager.put_query_result.assert_not_called()

    assert result1 == result2

@pytest.mark.asyncio
async def test_cache_invalidation_on_create(db_manager):
    db_manager.caching_manager = MagicMock(spec=EnhancedCachingManager)

    # Call create_email
    await db_manager.create_email({"subject": "New Email", "message_id": "new_msg_id"})

    # Verify clear_query_cache was called
    db_manager.caching_manager.clear_query_cache.assert_called_once()

@pytest.mark.asyncio
async def test_cache_invalidation_on_update(db_manager):
    db_manager.caching_manager = MagicMock(spec=EnhancedCachingManager)

    # Mock get_email_by_id to return an email
    db_manager.get_email_by_id = AsyncMock(return_value={"id": 1, "subject": "Old Subject"})
    db_manager._update_email_fields = AsyncMock(return_value=True)
    db_manager._save_heavy_content = AsyncMock()
    db_manager._update_email_indexes = AsyncMock()
    db_manager._save_data = AsyncMock()
    db_manager._add_category_details = MagicMock(return_value={"id": 1, "subject": "New Subject"})

    # Call update_email
    await db_manager.update_email(1, {"subject": "New Subject"})

    # Verify clear_query_cache was called
    db_manager.caching_manager.clear_query_cache.assert_called_once()
