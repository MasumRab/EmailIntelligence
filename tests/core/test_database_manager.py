
import pytest
import asyncio
import os
import json
import gzip
import shutil
from src.core.database import DatabaseManager, DatabaseConfig, FIELD_SUBJECT, FIELD_SENDER, FIELD_SENDER_EMAIL, FIELD_ID

TEST_DATA_DIR = "test_data_db_manager"

@pytest.fixture
async def db_manager():
    if os.path.exists(TEST_DATA_DIR):
        shutil.rmtree(TEST_DATA_DIR)

    config = DatabaseConfig(data_dir=TEST_DATA_DIR)
    manager = DatabaseManager(config)
    await manager._ensure_initialized()
    yield manager

    if os.path.exists(TEST_DATA_DIR):
        shutil.rmtree(TEST_DATA_DIR)

@pytest.mark.asyncio
async def test_search_index_population(db_manager):
    """Test that search index is populated correctly."""
    email_data = {
        FIELD_ID: 1,
        FIELD_SUBJECT: "Hello World",
        FIELD_SENDER: "John Doe",
        FIELD_SENDER_EMAIL: "john@example.com",
        "message_id": "msg1"
    }
    await db_manager.create_email(email_data)

    # Wait, in main branch _search_index might be cleared or not exposed directly?
    # I should check if it exists.
    assert hasattr(db_manager, "_search_index")
    assert 1 in db_manager._search_index
    assert "hello world" in db_manager._search_index[1]

@pytest.mark.asyncio
async def test_content_availability_index(db_manager):
    """Test that content availability index is updated."""
    email_data = {
        FIELD_ID: 1,
        FIELD_SUBJECT: "Subject",
        "message_id": "msg1",
        "content": "Secret Content"
    }
    # This should trigger content saving and index update
    await db_manager.create_email(email_data)

    assert hasattr(db_manager, "_content_available_index")
    assert 1 in db_manager._content_available_index
    assert os.path.exists(os.path.join(TEST_DATA_DIR, "email_content", "1.json.gz"))

@pytest.mark.asyncio
async def test_search_uses_index(db_manager):
    """Test that search works using the index."""
    email_data = {
        FIELD_ID: 1,
        FIELD_SUBJECT: "FindMe",
        "message_id": "msg1"
    }
    await db_manager.create_email(email_data)

    # Search for "findme"
    results = await db_manager.search_emails_with_limit("findme")
    assert len(results) == 1
    assert results[0][FIELD_ID] == 1

    # Search for non-existent
    results = await db_manager.search_emails_with_limit("missing")
    assert len(results) == 0

@pytest.mark.asyncio
async def test_search_content_optimization(db_manager):
    """Test that content is searched only when necessary."""
    # Email 1: Metadata match
    await db_manager.create_email({
        FIELD_ID: 1,
        FIELD_SUBJECT: "Secret metadata",
        "message_id": "msg1"
    })

    # Email 2: Content match
    await db_manager.create_email({
        FIELD_ID: 2,
        FIELD_SUBJECT: "Boring subject",
        "message_id": "msg2",
        "content": "Hidden Secret"
    })

    # Email 3: No match
    await db_manager.create_email({
        FIELD_ID: 3,
        FIELD_SUBJECT: "Boring subject",
        "message_id": "msg3",
        "content": "Nothing here"
    })

    results = await db_manager.search_emails_with_limit("secret")
    assert len(results) == 2
    ids = [r[FIELD_ID] for r in results]
    assert 1 in ids
    assert 2 in ids
    assert 3 not in ids
