
import pytest
import pytest_asyncio
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch
from src.core.database import DatabaseManager, DatabaseConfig, FIELD_SUBJECT, FIELD_ID
from src.core.enhanced_caching import EnhancedCachingManager

@pytest.fixture
def db_config(tmp_path):
    config = DatabaseConfig(data_dir=str(tmp_path))
    return config

@pytest_asyncio.fixture
async def db_manager(db_config):
    manager = DatabaseManager(config=db_config)
    await manager._ensure_initialized()
    return manager

@pytest.mark.asyncio
async def test_search_caching(db_manager):
    # Add some data
    email1 = {
        "id": 1,
        "subject": "Test Email 1",
        "sender": "sender1@example.com",
        "content": "Content 1",
        "message_id": "msg1"
    }
    await db_manager.create_email(email1)

    # Mock the caching manager to verify calls
    # We can't easily mock the whole thing because DatabaseManager creates it internally.
    # But we can inspect the real one.

    cache_manager = db_manager.caching_manager
    query_cache = cache_manager.query_cache

    # Initial state
    assert query_cache.hits == 0
    assert query_cache.misses == 0
    assert len(query_cache.cache) == 0

    # 1. Perform search
    term = "Test"
    results1 = await db_manager.search_emails_with_limit(term, limit=10)
    assert len(results1) == 1

    # Verify cache miss and populate
    assert query_cache.misses == 1
    assert query_cache.hits == 0
    assert len(query_cache.cache) == 1

    # 2. Perform same search again
    results2 = await db_manager.search_emails_with_limit(term, limit=10)
    assert len(results2) == 1
    assert results1 == results2

    # Verify cache hit
    assert query_cache.misses == 1
    assert query_cache.hits == 1

    # 3. Add new email (should invalidate cache)
    email2 = {
        "id": 2,
        "subject": "Test Email 2",
        "sender": "sender2@example.com",
        "content": "Content 2",
        "message_id": "msg2"
    }
    await db_manager.create_email(email2)

    # Verify cache cleared
    assert len(query_cache.cache) == 0

    # 4. Search again
    results3 = await db_manager.search_emails_with_limit(term, limit=10)
    assert len(results3) == 2

    # Verify cache miss again (fresh search)
    assert len(query_cache.cache) == 1
    # Note: query_cache.clear() resets hits/misses to 0
    assert query_cache.misses == 1
    assert query_cache.hits == 0

@pytest.mark.asyncio
async def test_search_caching_invalidation_update(db_manager):
    email1 = {
        "id": 1,
        "subject": "Test Email 1",
        "sender": "sender1@example.com",
        "content": "Content 1",
        "message_id": "msg1"
    }
    await db_manager.create_email(email1)

    term = "Test"
    await db_manager.search_emails_with_limit(term, limit=10)

    # Verify cache populated
    assert len(db_manager.caching_manager.query_cache.cache) == 1

    # Update email
    await db_manager.update_email(1, {"subject": "Updated Test Email"})

    # Verify cache cleared
    assert len(db_manager.caching_manager.query_cache.cache) == 0
