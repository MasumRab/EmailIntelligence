
import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch
from src.core.database import DatabaseManager, DatabaseConfig, FIELD_ID, FIELD_SUBJECT, FIELD_CONTENT

@pytest.fixture
def db_config(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    return DatabaseConfig(data_dir=str(data_dir))

@pytest.fixture
def db_manager(db_config):
    manager = DatabaseManager(config=db_config)
    # Ensure initialized
    manager._initialized = True
    manager.emails_data = []
    manager.emails_by_id = {}
    manager._search_index = {}

    # We want to use the REAL caching manager for this test to verify the logic
    # But we can also mock it to verify interactions
    return manager

@pytest.mark.asyncio
async def test_search_cache_hit(db_manager):
    """Test that search uses cached result if available."""
    # Mock caching manager to control return values
    db_manager.caching_manager = MagicMock()

    # Setup cache hit
    expected_result = [{"id": 1, "subject": "Cached Result"}]
    db_manager.caching_manager.get_query_result.return_value = expected_result

    # Execute
    results = await db_manager.search_emails_with_limit("cached", limit=10)

    # Verify
    assert results == expected_result
    db_manager.caching_manager.get_query_result.assert_called_with("search:cached:10")
    # Should NOT perform search (which would require emails_data)

@pytest.mark.asyncio
async def test_search_cache_miss_and_populate(db_manager):
    """Test that search populates cache on miss."""
    # Mock caching manager
    db_manager.caching_manager = MagicMock()
    db_manager.caching_manager.get_query_result.return_value = None

    # Setup data
    email = {FIELD_ID: 1, FIELD_SUBJECT: "Test Match"}
    db_manager.emails_data = [email]
    db_manager._search_index = {1: "test match"}
    db_manager.emails_by_id = {1: email}

    # Execute
    results = await db_manager.search_emails_with_limit("match", limit=10)

    # Verify
    assert len(results) == 1
    assert results[0][FIELD_ID] == 1

    # Verify cache put
    db_manager.caching_manager.put_query_result.assert_called_once()
    args = db_manager.caching_manager.put_query_result.call_args
    assert args[0][0] == "search:match:10"
    assert args[0][1] == results

@pytest.mark.asyncio
async def test_search_cache_invalidation_create(db_manager):
    """Test that creating email invalidates query cache."""
    db_manager.caching_manager = MagicMock()

    # Execute
    await db_manager.create_email({FIELD_SUBJECT: "New Email", "messageId": "msg1"})

    # Verify
    db_manager.caching_manager.clear_query_cache.assert_called_once()

@pytest.mark.asyncio
async def test_search_cache_invalidation_update(db_manager):
    """Test that updating email invalidates query cache."""
    db_manager.caching_manager = MagicMock()

    # Setup email
    email = {FIELD_ID: 1, FIELD_SUBJECT: "Old Subject"}
    db_manager.emails_by_id = {1: email}
    # Mock get_email_by_id to return the email
    with patch.object(db_manager, 'get_email_by_id', return_value=email):
         # Execute
        await db_manager.update_email(1, {FIELD_SUBJECT: "New Subject"})

    # Verify
    db_manager.caching_manager.clear_query_cache.assert_called_once()
