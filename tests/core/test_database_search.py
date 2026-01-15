
import asyncio
import os
import json
import pytest
import pytest_asyncio
from unittest.mock import MagicMock, patch
from src.core.database import DatabaseManager, FIELD_ID, FIELD_SUBJECT, FIELD_SENDER, FIELD_SENDER_EMAIL, FIELD_CONTENT, FIELD_CATEGORY_ID

@pytest_asyncio.fixture
async def db_manager():
    # Setup a DatabaseManager with mocked config/file paths to avoid real disk I/O
    # We will mock the caching manager too to verify interactions

    with patch('src.core.database.EnhancedCachingManager') as MockCaching:
        db = DatabaseManager()
        # Mock internal storage
        db.emails_data = []
        db.emails_by_id = {}
        db._search_index = {}
        db._content_available_index = set()

        # Real caching manager logic is complex to mock fully,
        # so we let it use the mock we injected or a real one if we want integration test.
        # But for unit testing the database logic, we want to assert on caching calls.

        # Actually, let's use the real CachingManager but mock the put/get methods if needed
        # Or just verify side effects.
        # The db_manager creates its own caching_manager.

        # Let's mock the caching manager instance attached to db
        db.caching_manager = MagicMock()
        db.caching_manager.get_query_result.return_value = None

        yield db

@pytest.mark.asyncio
async def test_build_indexes(db_manager):
    # Setup data
    email1 = {FIELD_ID: 1, FIELD_SUBJECT: "Hello World", FIELD_SENDER: "Alice"}
    email2 = {FIELD_ID: 2, FIELD_SUBJECT: "Foo Bar", FIELD_SENDER: "Bob"}
    db_manager.emails_data = [email1, email2]

    # Mock os.listdir to populate content index
    with patch('os.path.exists', return_value=True), \
         patch('os.listdir', return_value=["1.json.gz"]):

        db_manager._build_indexes()

        # Verify search index
        assert 1 in db_manager._search_index
        assert "hello world" in db_manager._search_index[1]
        assert "alice" in db_manager._search_index[1]

        assert 2 in db_manager._search_index
        assert "foo bar" in db_manager._search_index[2]

        # Verify content available index
        assert 1 in db_manager._content_available_index
        assert 2 not in db_manager._content_available_index

@pytest.mark.asyncio
async def test_search_uses_cache(db_manager):
    db_manager.caching_manager.get_query_result.return_value = [{"id": 1}]

    result = await db_manager.search_emails_with_limit("test")

    assert result == [{"id": 1}]
    db_manager.caching_manager.get_query_result.assert_called_once()
    # Should not access internal data if cache hit
    # (Hard to prove unless we spy on _sort_and_paginate_emails or similar,
    # but we can rely on the return value being what the cache returned)

@pytest.mark.asyncio
async def test_search_uses_index(db_manager):
    # Setup
    email1 = {FIELD_ID: 1, FIELD_SUBJECT: "FoundMe", FIELD_SENDER: "Alice"}
    email2 = {FIELD_ID: 2, FIELD_SUBJECT: "HideMe", FIELD_SENDER: "Bob"}
    db_manager.emails_data = [email1, email2]

    # Manually populate index (simulate build_indexes)
    db_manager._search_index = {
        1: "foundme alice",
        2: "hideme bob"
    }

    # Search
    result = await db_manager.search_emails_with_limit("Found")

    assert len(result) == 1
    assert result[0][FIELD_ID] == 1

    # Verify cache was populated
    db_manager.caching_manager.put_query_result.assert_called_once()

@pytest.mark.asyncio
async def test_search_checks_content_index(db_manager):
    # Setup
    email1 = {FIELD_ID: 1, FIELD_SUBJECT: "NoMatch", "content_available": False}
    email2 = {FIELD_ID: 2, FIELD_SUBJECT: "NoMatch", "content_available": True}
    db_manager.emails_data = [email1, email2]
    db_manager._search_index = {
        1: "nomatch",
        2: "nomatch"
    }
    db_manager._content_available_index = {2}

    # Mock disk read
    with patch('src.core.database.DatabaseManager._get_email_content_path') as mock_path, \
         patch('gzip.open', create=True) as mock_gzip, \
         patch('json.load') as mock_json_load:

        mock_json_load.return_value = {FIELD_CONTENT: "Here is the Secret"}

        # Search for "Secret" which is only in content of email 2
        result = await db_manager.search_emails_with_limit("Secret")

        assert len(result) == 1
        assert result[0][FIELD_ID] == 2

        # Should have opened file for email 2
        # Should NOT have opened file for email 1 (because not in _content_available_index)
        # We can verify call count of gzip.open
        assert mock_gzip.call_count == 1

@pytest.mark.asyncio
async def test_create_email_updates_index_and_clears_cache(db_manager):
    # Setup
    db_manager.emails_data = []
    db_manager._search_index = {}

    email_data = {FIELD_SUBJECT: "New Email", FIELD_SENDER: "Sender"}

    # We need to mock _save_heavy_content to avoid disk write,
    # but we also want to verify it updates content index.
    # However, create_email calls _save_heavy_content.

    with patch('src.core.database.DatabaseManager._save_heavy_content') as mock_save, \
         patch('src.core.database.DatabaseManager._save_data') as mock_save_data:

        await db_manager.create_email(email_data)

        # Verify cache cleared
        db_manager.caching_manager.clear_query_cache.assert_called_once()

        # Verify search index updated
        assert len(db_manager._search_index) == 1
        new_id = list(db_manager._search_index.keys())[0]
        assert "new email" in db_manager._search_index[new_id]

@pytest.mark.asyncio
async def test_update_email_updates_index_and_clears_cache(db_manager):
    # Setup
    email1 = {FIELD_ID: 1, FIELD_SUBJECT: "Old Subject", FIELD_SENDER: "Alice"}
    db_manager.emails_data = [email1]
    db_manager.emails_by_id = {1: email1}
    db_manager._search_index = {1: "old subject alice"}

    update_data = {FIELD_SUBJECT: "New Subject"}

    with patch('src.core.database.DatabaseManager._save_heavy_content'), \
         patch('src.core.database.DatabaseManager._save_data'):

        await db_manager.update_email(1, update_data)

        # Verify cache cleared
        db_manager.caching_manager.clear_query_cache.assert_called_once()

        # Verify search index updated
        assert "new subject" in db_manager._search_index[1]

@pytest.mark.asyncio
async def test_save_heavy_content_updates_content_index(db_manager):
    email_id = 1
    email_data = {FIELD_CONTENT: "Heavy Content"}

    with patch('gzip.open', create=True), \
         patch('asyncio.to_thread'):

        await db_manager._save_heavy_content(email_id, email_data)

        assert email_id in db_manager._content_available_index
