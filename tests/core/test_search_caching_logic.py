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
    manager.caching_manager.get_email_content.return_value = None
    manager.caching_manager.get_query_result.return_value = None

    manager.emails_data = []
    manager.emails_by_id = {}
    manager._initialized = True
    return manager

@pytest.mark.asyncio
async def test_search_results_are_cached(db_manager):
    """Test that search results are stored in cache."""
    # Setup
    email_id = 1
    email_light = {FIELD_ID: email_id, "subject": "Find me"}
    db_manager.emails_data = [email_light]
    db_manager.emails_by_id = {email_id: email_light}

    # Execute search
    results = await db_manager.search_emails_with_limit("find", limit=10)

    # Verify result
    assert len(results) == 1

    # Verify cache interactions
    cache_key = "search:find:10"
    db_manager.caching_manager.get_query_result.assert_called_with(cache_key)
    db_manager.caching_manager.put_query_result.assert_called_with(cache_key, results)

@pytest.mark.asyncio
async def test_search_uses_cached_result(db_manager):
    """Test that search returns cached result if available."""
    # Setup
    cached_data = [{"id": 1, "subject": "Cached Result"}]
    db_manager.caching_manager.get_query_result.return_value = cached_data

    # Execute search
    results = await db_manager.search_emails_with_limit("anything", limit=10)

    # Verify result is from cache
    assert results == cached_data

    # Verify we didn't search (no put)
    db_manager.caching_manager.put_query_result.assert_not_called()

@pytest.mark.asyncio
async def test_cache_invalidation_on_create(db_manager):
    """Test that creating an email invalidates query cache."""
    email_data = {"subject": "New Email", "message_id": "msg1"}

    # Mock internal methods to avoid side effects
    db_manager._prepare_new_email_record = AsyncMock(return_value={FIELD_ID: 1, **email_data})
    db_manager._save_heavy_content = AsyncMock()
    db_manager._add_email_to_indexes = AsyncMock()
    db_manager._save_data = AsyncMock()
    db_manager._update_category_count = AsyncMock()

    await db_manager.create_email(email_data)

    db_manager.caching_manager.clear_query_cache.assert_called_once()

@pytest.mark.asyncio
async def test_cache_invalidation_on_update(db_manager):
    """Test that updating an email invalidates query cache."""
    email_id = 1
    update_data = {"subject": "Updated"}

    # Mock get_email_by_id to return something
    db_manager.get_email_by_id = AsyncMock(return_value={FIELD_ID: email_id, "subject": "Old"})
    db_manager._update_email_fields = AsyncMock(return_value=True)
    db_manager._save_heavy_content = AsyncMock()
    db_manager._update_email_indexes = AsyncMock()
    db_manager._save_data = AsyncMock()

    await db_manager.update_email(email_id, update_data)

    db_manager.caching_manager.clear_query_cache.assert_called_once()

@pytest.mark.asyncio
async def test_cache_invalidation_on_update_by_message_id(db_manager):
    """Test that updating by message ID invalidates query cache."""
    message_id = "msg1"
    update_data = {"subject": "Updated"}

    db_manager.get_email_by_message_id = AsyncMock(return_value={FIELD_ID: 1, "subject": "Old", "category_id": None})
    db_manager._save_heavy_content = AsyncMock() # Not called directly but via dump
    db_manager._save_data = AsyncMock()

    # We need to mock open/dump for the heavy content update part, or mock the whole method?
    # update_email_by_message_id has complex logic.
    # Let's mock _get_email_content_path and open.

    with patch("src.core.database.gzip.open", MagicMock()) as mock_open:
        await db_manager.update_email_by_message_id(message_id, update_data)

    db_manager.caching_manager.clear_query_cache.assert_called_once()
