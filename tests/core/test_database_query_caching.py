
import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch
from src.core.database import DatabaseManager, DatabaseConfig, FIELD_ID, FIELD_SUBJECT

@pytest.fixture
def db_config(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    return DatabaseConfig(data_dir=str(data_dir))

@pytest.fixture
def db_manager(db_config):
    manager = DatabaseManager(config=db_config)
    # Use real CachingManager but mock its internals if needed,
    # but here we want to test integration with it.
    # However, DatabaseManager initializes its own caching_manager.
    # We will let it use the real one to test the caching logic.

    manager.emails_data = []
    manager.emails_by_id = {}
    manager._search_index = {}
    manager._sorted_emails_cache = None
    manager._initialized = True
    return manager

@pytest.mark.asyncio
async def test_search_emails_caching(db_manager):
    """Test that repeated searches return cached results."""
    # Setup data
    email_id = 1
    email_light = {FIELD_ID: email_id, "subject": "Test Subject"}
    db_manager.emails_data = [email_light]
    db_manager._build_indexes() # Build search index

    # Spy on caching manager
    with patch.object(db_manager.caching_manager, 'get_query_result', wraps=db_manager.caching_manager.get_query_result) as mock_get_cache:
        with patch.object(db_manager.caching_manager, 'put_query_result', wraps=db_manager.caching_manager.put_query_result) as mock_put_cache:

            # First search: Cache Miss
            results1 = await db_manager.search_emails_with_limit("subject", limit=10)
            assert len(results1) == 1
            assert results1[0][FIELD_ID] == email_id

            # Verify cache miss
            assert mock_get_cache.return_value is None or mock_get_cache.call_count >= 1
            mock_put_cache.assert_called_once()

            # Second search: Cache Hit
            results2 = await db_manager.search_emails_with_limit("subject", limit=10)
            assert len(results2) == 1
            assert results2 == results1

            # Verify cache hit (we can't easily check return value on spy for second call without capturing,
            # but we can check if underlying cache has it)
            query_key = "search:subject:10"
            assert db_manager.caching_manager.get_query_result(query_key) is not None

@pytest.mark.asyncio
async def test_cache_invalidation_on_create(db_manager):
    """Test that creating an email invalidates the query cache."""
    # 1. Search and cache
    db_manager.emails_data = []
    await db_manager.search_emails_with_limit("new", limit=10)
    query_key = "search:new:10"

    # Manually populate cache to be sure
    db_manager.caching_manager.put_query_result(query_key, [])
    assert db_manager.caching_manager.get_query_result(query_key) is not None

    # 2. Create Email
    new_email = {FIELD_ID: 1, "messageId": "msg1", "subject": "New Email"}
    with patch.object(db_manager, '_save_data', new_callable=AsyncMock):
        with patch.object(db_manager, '_save_heavy_content', new_callable=AsyncMock):
             await db_manager.create_email(new_email)

    # 3. Verify Cache Invalidated
    assert db_manager.caching_manager.get_query_result(query_key) is None

@pytest.mark.asyncio
async def test_cache_invalidation_on_update(db_manager):
    """Test that updating an email invalidates the query cache."""
    # Setup
    email = {FIELD_ID: 1, "messageId": "msg1", "subject": "Old Subject"}
    db_manager.emails_data = [email]
    db_manager.emails_by_id = {1: email}
    db_manager.emails_by_message_id = {"msg1": email}

    # 1. Search and cache
    await db_manager.search_emails_with_limit("old", limit=10)
    query_key = "search:old:10"
    assert db_manager.caching_manager.get_query_result(query_key) is not None

    # 2. Update Email
    with patch.object(db_manager, '_save_data', new_callable=AsyncMock):
        with patch.object(db_manager, '_save_heavy_content', new_callable=AsyncMock):
            await db_manager.update_email(1, {"subject": "New Subject"})

    # 3. Verify Cache Invalidated
    assert db_manager.caching_manager.get_query_result(query_key) is None
