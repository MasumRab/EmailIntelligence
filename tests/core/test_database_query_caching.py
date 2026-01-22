import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch
from src.core.database import DatabaseManager, DatabaseConfig, FIELD_ID

@pytest.fixture
def db_config(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    return DatabaseConfig(data_dir=str(data_dir))

@pytest.fixture
def db_manager(db_config):
    manager = DatabaseManager(config=db_config)
    # Mock caching manager
    manager.caching_manager = MagicMock()
    # Default behavior: no cache hit
    manager.caching_manager.get_query_result.return_value = None

    manager.emails_data = []
    manager.emails_by_id = {}
    manager._initialized = True
    return manager

@pytest.mark.asyncio
async def test_search_emails_caches_results(db_manager):
    """Test that search results are cached."""
    # Setup
    email_id = 1
    email_light = {FIELD_ID: email_id, "subject": "Test Subject"}
    db_manager.emails_data = [email_light]
    db_manager._search_index = {email_id: "test subject"}

    # First search - should miss cache and execute search
    results1 = await db_manager.search_emails_with_limit("test", limit=10)

    assert len(results1) == 1
    assert results1[0][FIELD_ID] == email_id

    # Verify cache check
    db_manager.caching_manager.get_query_result.assert_called_with("search:test:10")

    # Verify cache put
    db_manager.caching_manager.put_query_result.assert_called()
    call_args = db_manager.caching_manager.put_query_result.call_args
    assert call_args[0][0] == "search:test:10"
    assert len(call_args[0][1]) == 1
    assert call_args[0][1][0][FIELD_ID] == email_id

@pytest.mark.asyncio
async def test_search_emails_uses_cached_results(db_manager):
    """Test that search uses cached results if available."""
    # Setup cache hit
    cached_results = [{FIELD_ID: 99, "subject": "Cached Email"}]
    db_manager.caching_manager.get_query_result.return_value = cached_results

    # Execute search
    results = await db_manager.search_emails_with_limit("cached", limit=10)

    # Verify results from cache
    assert len(results) == 1
    assert results[0][FIELD_ID] == 99

    # Verify we didn't search (emails_data is empty in fixture)
    assert db_manager.caching_manager.get_query_result.called
