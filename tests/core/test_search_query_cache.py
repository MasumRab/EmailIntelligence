import pytest
import pytest_asyncio
import asyncio
from unittest.mock import MagicMock
from src.core.database import DatabaseManager, DatabaseConfig, FIELD_ID, FIELD_SUBJECT

@pytest.fixture
def db_config(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    return DatabaseConfig(data_dir=str(data_dir))

@pytest_asyncio.fixture
async def db_manager(db_config):
    manager = DatabaseManager(config=db_config)
    await manager._ensure_initialized()
    return manager

@pytest.mark.asyncio
async def test_search_caching_flow(db_manager):
    """Test full flow: search (miss) -> cache hit -> update -> search (miss)."""

    # 1. Create an email
    email_data = {
        "messageId": "msg1",
        "subject": "Important Meeting",
        "sender": "boss@example.com",
        "content": "Let's meet tomorrow."
    }
    await db_manager.create_email(email_data)

    term = "meeting"
    limit = 10
    query_key = f"search:{term}:{limit}"

    # 2. First search - should be a miss
    # Check stats before
    misses_start = db_manager.caching_manager.query_cache.misses
    hits_start = db_manager.caching_manager.query_cache.hits

    results1 = await db_manager.search_emails_with_limit(term, limit=limit)

    assert len(results1) == 1
    assert results1[0]["subject"] == "Important Meeting"
    assert db_manager.caching_manager.query_cache.misses == misses_start + 1
    assert db_manager.caching_manager.query_cache.hits == hits_start

    # Verify it's in cache
    cached = db_manager.caching_manager.get_query_result(query_key)
    assert cached is not None
    assert len(cached) == 1
    assert cached[0]["id"] == results1[0]["id"]

    # 3. Second search - should be a hit
    results2 = await db_manager.search_emails_with_limit(term, limit=limit)

    assert len(results2) == 1
    assert results2[0]["id"] == results1[0]["id"]
    # hits increased by 2: one from explicit get_query_result() verification above, one from search_emails_with_limit()
    assert db_manager.caching_manager.query_cache.hits == hits_start + 2

    # Note: db_manager.caching_manager.get_query_result call in test incremented hits?
    # No, get_query_result calls query_cache.get.
    # In step 2 verification: `cached = db_manager.caching_manager.get_query_result(query_key)`
    # This calls query_cache.get, so it increments hits!

    # So hits should be hits_start + 1 (from verification) + 1 (from second search) = hits_start + 2.
    # Let's rely on relative increase.

    current_hits = db_manager.caching_manager.query_cache.hits

    results3 = await db_manager.search_emails_with_limit(term, limit=limit)

    assert db_manager.caching_manager.query_cache.hits == current_hits + 1

    # 4. Update email - should clear cache
    update_data = {"subject": "Updated Meeting"}
    await db_manager.update_email(results1[0]["id"], update_data)

    # Verify cache is cleared (size 0 or key missing)
    # The clear_query_cache clears EVERYTHING in query cache
    assert len(db_manager.caching_manager.query_cache.cache) == 0

    # 5. Search again - should be a miss
    misses_before = db_manager.caching_manager.query_cache.misses
    results4 = await db_manager.search_emails_with_limit(term, limit=limit)

    assert db_manager.caching_manager.query_cache.misses == misses_before + 1
    assert results4[0]["subject"] == "Updated Meeting"

    # Verify it is back in cache
    cached_new = db_manager.caching_manager.get_query_result(query_key)
    assert cached_new is not None
    assert cached_new[0]["subject"] == "Updated Meeting"

@pytest.mark.asyncio
async def test_create_email_clears_cache(db_manager):
    """Test that creating an email clears the query cache."""
    # Perform a search to populate cache
    await db_manager.search_emails_with_limit("test", limit=10)
    assert len(db_manager.caching_manager.query_cache.cache) > 0

    # Create new email
    await db_manager.create_email({"subject": "New Email", "messageId": "new1"})

    # Verify cache cleared
    assert len(db_manager.caching_manager.query_cache.cache) == 0

@pytest.mark.asyncio
async def test_update_by_message_id_clears_cache(db_manager):
    """Test that updating by message ID clears the query cache."""
    await db_manager.create_email({"subject": "Test", "messageId": "msg_id_1"})

    # Populate cache
    await db_manager.search_emails_with_limit("test", limit=10)
    assert len(db_manager.caching_manager.query_cache.cache) > 0

    # Update
    await db_manager.update_email_by_message_id("msg_id_1", {"subject": "Updated"})

    # Verify cache cleared
    assert len(db_manager.caching_manager.query_cache.cache) == 0
