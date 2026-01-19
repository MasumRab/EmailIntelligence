import pytest
import pytest_asyncio
import asyncio
from src.core.database import DatabaseManager, DatabaseConfig, FIELD_ID, FIELD_SUBJECT, FIELD_MESSAGE_ID

@pytest.fixture
def db_config(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    return DatabaseConfig(data_dir=str(data_dir))

@pytest_asyncio.fixture
async def db_manager(db_config):
    manager = DatabaseManager(config=db_config)
    # We need to initialize it to set up internal structures
    await manager._ensure_initialized()
    return manager

@pytest.mark.asyncio
async def test_search_caching_flow(db_manager):
    """Test the full flow of search caching: Miss -> Hit -> Invalidate -> Miss."""

    # 1. Setup initial data
    await db_manager.create_email({
        FIELD_MESSAGE_ID: "msg1",
        FIELD_SUBJECT: "Apple Banana Cherry",
        "sender": "test@example.com"
    })

    # Get initial stats
    initial_stats = db_manager.caching_manager.get_cache_statistics()
    initial_hits = initial_stats["query_cache"]["hits"]
    initial_misses = initial_stats["query_cache"]["misses"]

    # 2. First search for "Banana" - Should be a MISS (or at least result in a put)
    results1 = await db_manager.search_emails_with_limit("Banana", limit=10)
    assert len(results1) == 1
    assert results1[0][FIELD_MESSAGE_ID] == "msg1"

    stats1 = db_manager.caching_manager.get_cache_statistics()
    # We expect a put operation
    assert stats1["operations"]["query_result_put"] > initial_stats["operations"]["query_result_put"]

    # 3. Second search for "Banana" - Should be a HIT
    results2 = await db_manager.search_emails_with_limit("Banana", limit=10)
    assert len(results2) == 1

    stats2 = db_manager.caching_manager.get_cache_statistics()
    assert stats2["query_cache"]["hits"] > stats1["query_cache"]["hits"], "Should have hit the cache"
    assert stats2["query_cache"]["misses"] == stats1["query_cache"]["misses"], "Should not have missed"

    # 4. Modify data (Add new email matching query) - Should invalidate cache
    await db_manager.create_email({
        FIELD_MESSAGE_ID: "msg2",
        FIELD_SUBJECT: "Banana Date Elderberry",
        "sender": "test2@example.com"
    })

    # Verify cache size is 0 (or cleared) - wait, clear() empties the dict
    stats_after_update = db_manager.caching_manager.get_cache_statistics()
    assert stats_after_update["query_cache"]["size"] == 0, "Query cache should be empty after update"

    # 5. Third search for "Banana" - Should be a MISS (re-fetch) and find 2 results
    results3 = await db_manager.search_emails_with_limit("Banana", limit=10)
    assert len(results3) == 2

    stats3 = db_manager.caching_manager.get_cache_statistics()
    # Note: query_cache.clear() resets internal hit/miss counters on the cache object
    # So we expect 1 miss (from this search)
    assert stats3["query_cache"]["misses"] == 1, "Should have missed after invalidation (counters were reset)"

    # However, 'operations' in EnhancedCachingManager are NOT reset by clear_query_cache()
    # because they are tracked in self.cache_operations dict which is only reset by clear_all_caches()
    assert stats3["operations"]["query_result_put"] > stats1["operations"]["query_result_put"], "Should have re-cached"

@pytest.mark.asyncio
async def test_search_cache_different_queries(db_manager):
    """Test that different queries are cached separately."""
    await db_manager.create_email({
        FIELD_MESSAGE_ID: "msg1",
        FIELD_SUBJECT: "Common Word",
        "sender": "test@example.com"
    })

    # Search 1
    await db_manager.search_emails_with_limit("Common", limit=10)
    stats1 = db_manager.caching_manager.get_cache_statistics()
    assert stats1["query_cache"]["size"] == 1

    # Search 2 (different term)
    await db_manager.search_emails_with_limit("Word", limit=10)
    stats2 = db_manager.caching_manager.get_cache_statistics()
    assert stats2["query_cache"]["size"] == 2

    # Search 3 (same term, different limit)
    await db_manager.search_emails_with_limit("Common", limit=5)
    stats3 = db_manager.caching_manager.get_cache_statistics()
    assert stats3["query_cache"]["size"] == 3
