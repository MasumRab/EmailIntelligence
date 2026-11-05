import pytest
from src.core.database import DatabaseManager, DatabaseConfig, FIELD_ID

@pytest.fixture
def db_config(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    return DatabaseConfig(data_dir=str(data_dir))

@pytest.fixture
def db_manager(db_config):
    manager = DatabaseManager(config=db_config)
    # We want real caching manager behavior for this test, not a mock
    # because we are testing the integration with caching manager
    return manager

@pytest.mark.asyncio
async def test_search_query_caching_integration(db_manager):
    """Test that search queries are cached and invalidated correctly."""
    await db_manager._ensure_initialized()

    # Create test data
    await db_manager.create_email({
        "messageId": "msg-1",
        "subject": "Test Subject 1",
        "sender": "sender@example.com",
        "content": "Content 1"
    })

    # First search (Cold)
    results1 = await db_manager.search_emails_with_limit("Test", limit=10)
    assert len(results1) == 1

    # Verify it's in the cache
    cache_key = "search:test:10"
    assert db_manager.caching_manager.get_query_result(cache_key) is not None

    # Second search (Warm) - should be identical
    results2 = await db_manager.search_emails_with_limit("Test", limit=10)
    assert len(results2) == 1
    assert results2 == results1

    # Update email -> Should invalidate cache
    await db_manager.update_email(results1[0][FIELD_ID], {"subject": "Updated Subject 1"})

    # Verify cache is cleared
    assert db_manager.caching_manager.get_query_result(cache_key) is None

    # Search again (Cold again due to invalidation)
    results3 = await db_manager.search_emails_with_limit("Updated", limit=10)
    assert len(results3) == 1

    # Verify new cache entry
    new_cache_key = "search:updated:10"
    assert db_manager.caching_manager.get_query_result(new_cache_key) is not None


def test_query_result_cache_capacity():
    """Test that QueryResultCache respects the capacity limit and evicts LRU."""
    from src.core.enhanced_caching import QueryResultCache

    cache = QueryResultCache(ttl_seconds=300, capacity=3)

    # Add 3 items
    cache.put("key1", "value1")
    cache.put("key2", "value2")
    cache.put("key3", "value3")

    assert cache.get("key1") == "value1"
    assert cache.get("key2") == "value2"
    assert cache.get("key3") == "value3"
    assert len(cache.cache) == 3

    # Add a 4th item, exceeding capacity. "key1" should be evicted because
    # it was the least recently used since "key2" and "key3" were accessed later
    # Actually wait: we accessed them in order key1, key2, key3.
    # So key1 is the least recently accessed.
    cache.put("key4", "value4")

    assert cache.get("key1") is None
    assert cache.get("key4") == "value4"
    assert len(cache.cache) == 3

    # Access key2 to make it recently used, then add key5
    cache.get("key2")
    cache.put("key5", "value5")

    # "key3" should be evicted now
    assert cache.get("key3") is None
    assert cache.get("key2") == "value2"
    assert cache.get("key5") == "value5"
    assert len(cache.cache) == 3
