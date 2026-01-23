import pytest
import asyncio
from src.core.database import DatabaseManager, DatabaseConfig, FIELD_ID

@pytest.fixture
def db_config(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    return DatabaseConfig(data_dir=str(data_dir))

@pytest.fixture
async def db_manager(db_config):
    manager = DatabaseManager(config=db_config)
    # Ensure initialized
    await manager._ensure_initialized()
    return manager

@pytest.mark.asyncio
async def test_search_caching(db_manager):
    """Test that search results are cached and invalidated correctly."""

    # 1. Create some data
    await db_manager.create_email({"subject": "UniqueKeyword test email 1", "sender": "me"})
    await db_manager.create_email({"subject": "Other email", "sender": "you"})

    # Manually clear cache stats to start clean
    db_manager.caching_manager.clear_all_caches()

    # 2. First search - should miss cache and execute search
    results1 = await db_manager.search_emails("UniqueKeyword")
    assert len(results1) == 1
    assert results1[0]["subject"] == "UniqueKeyword test email 1"

    stats1 = db_manager.caching_manager.get_cache_statistics()
    # Expect 1 miss (get) and 1 put
    assert stats1["operations"]["query_result_get"] == 1
    assert stats1["operations"]["query_result_put"] == 1
    assert stats1["query_cache"]["misses"] == 1
    assert stats1["query_cache"]["hits"] == 0

    # 3. Second search - should hit cache
    results2 = await db_manager.search_emails("UniqueKeyword")
    assert len(results2) == 1

    stats2 = db_manager.caching_manager.get_cache_statistics()
    # Expect 2 gets (1 new), 1 put (no new put)
    assert stats2["operations"]["query_result_get"] == 2
    assert stats2["operations"]["query_result_put"] == 1
    # Hits should increase
    assert stats2["query_cache"]["hits"] == 1

    # 4. Create new email that matches - should invalidate cache
    await db_manager.create_email({"subject": "UniqueKeyword test email 2", "sender": "me"})

    # Cache should be cleared (hits/misses reset on clear() in QueryResultCache)
    stats3 = db_manager.caching_manager.get_cache_statistics()
    assert stats3["query_cache"]["size"] == 0
    assert stats3["query_cache"]["hits"] == 0
    assert stats3["query_cache"]["misses"] == 0

    # 5. Search again - should re-execute and return 2 results
    results3 = await db_manager.search_emails("UniqueKeyword")
    assert len(results3) == 2

    stats4 = db_manager.caching_manager.get_cache_statistics()
    assert stats4["operations"]["query_result_get"] == 3
    assert stats4["operations"]["query_result_put"] == 2
    assert stats4["query_cache"]["misses"] == 1

    # 6. Update email - should invalidate cache
    email_id = results3[0][FIELD_ID]
    await db_manager.update_email(email_id, {"subject": "Changed Subject"})

    stats5 = db_manager.caching_manager.get_cache_statistics()
    assert stats5["query_cache"]["size"] == 0

    # 7. Search again - should reflect update
    results4 = await db_manager.search_emails("UniqueKeyword")
    assert len(results4) == 1 # One matches now (the other was renamed)

    stats6 = db_manager.caching_manager.get_cache_statistics()
    assert stats6["operations"]["query_result_get"] == 4
    assert stats6["operations"]["query_result_put"] == 3
