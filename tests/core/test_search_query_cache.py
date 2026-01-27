import pytest
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
    # Mock caching manager
    manager.caching_manager = MagicMock()
    # Setup get_query_result to return None by default (miss)
    manager.caching_manager.get_query_result.return_value = None

    manager.emails_data = []
    manager.emails_by_id = {}
    manager._initialized = True
    return manager

@pytest.mark.asyncio
async def test_search_emails_caches_results(db_manager):
    """Test that search results are cached and retrieved."""
    # Setup data
    email_id = 1
    email_light = {FIELD_ID: email_id, FIELD_SUBJECT: "Test Subject", "sender": "me", "sender_email": "me@test.com"}
    db_manager.emails_data = [email_light]
    db_manager.emails_by_id = {email_id: email_light}
    # Pre-populate index
    db_manager._search_index = {email_id: "test subject me me@test.com"}

    # 1. First search (Cache Miss)
    search_term = "test"
    query_key = f"search:{search_term}:50"

    results1 = await db_manager.search_emails_with_limit(search_term, limit=50)

    assert len(results1) == 1
    db_manager.caching_manager.get_query_result.assert_called_with(query_key)
    db_manager.caching_manager.put_query_result.assert_called_once()

    # 2. Second search (Cache Hit simulation)
    # We manually set the mock to return the result to simulate a hit
    db_manager.caching_manager.get_query_result.return_value = results1
    db_manager.caching_manager.get_query_result.reset_mock()
    db_manager.caching_manager.put_query_result.reset_mock()

    results2 = await db_manager.search_emails_with_limit(search_term, limit=50)

    assert len(results2) == 1
    assert results2 == results1
    db_manager.caching_manager.get_query_result.assert_called_with(query_key)
    # Should not put again if hit
    db_manager.caching_manager.put_query_result.assert_not_called()

@pytest.mark.asyncio
async def test_create_email_clears_query_cache(db_manager):
    """Test that creating an email clears the query cache."""
    email_data = {
        "messageId": "msg1",
        "subject": "New Email",
        "sender": "sender",
        "sender_email": "sender@test.com",
        "content": "content"
    }

    with patch.object(db_manager, "_save_heavy_content", new_callable=AsyncMock), \
         patch.object(db_manager, "_save_data", new_callable=AsyncMock), \
         patch.object(db_manager, "_update_category_count", new_callable=AsyncMock):

        await db_manager.create_email(email_data)

        db_manager.caching_manager.clear_query_cache.assert_called_once()

@pytest.mark.asyncio
async def test_update_email_clears_query_cache(db_manager):
    """Test that updating an email clears the query cache."""
    email_id = 1
    email_data = {FIELD_ID: email_id, "subject": "Old Subject"}
    db_manager.emails_by_id = {email_id: email_data}

    # Mock caching manager get to return the email so update_email proceeds
    db_manager.caching_manager.get_email_record.return_value = email_data

    with patch.object(db_manager, "_save_heavy_content", new_callable=AsyncMock), \
         patch.object(db_manager, "_save_data", new_callable=AsyncMock), \
         patch.object(db_manager, "_update_email_indexes", new_callable=AsyncMock):

        await db_manager.update_email(email_id, {"subject": "New Subject"})

        db_manager.caching_manager.clear_query_cache.assert_called_once()
