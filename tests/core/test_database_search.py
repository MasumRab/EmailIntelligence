
import pytest
import asyncio
import os
import shutil
import json
import gzip
from src.core.database import DatabaseManager, DatabaseConfig, FIELD_SUBJECT, FIELD_SENDER, FIELD_SENDER_EMAIL, FIELD_ID, FIELD_CONTENT, FIELD_MESSAGE_ID

TEST_DATA_DIR = "test_data_search"

@pytest.fixture
def db_manager():
    # Setup
    if os.path.exists(TEST_DATA_DIR):
        shutil.rmtree(TEST_DATA_DIR)
    os.makedirs(TEST_DATA_DIR)

    config = DatabaseConfig(data_dir=TEST_DATA_DIR)
    manager = DatabaseManager(config)

    yield manager

    # Teardown
    if os.path.exists(TEST_DATA_DIR):
        shutil.rmtree(TEST_DATA_DIR)

@pytest.mark.asyncio
async def test_search_index_building(db_manager):
    """Test that search index is built correctly."""
    email1 = {
        FIELD_ID: 1,
        FIELD_SUBJECT: "Hello World",
        FIELD_SENDER: "Alice",
        FIELD_SENDER_EMAIL: "alice@example.com",
        FIELD_MESSAGE_ID: "msg1"
    }
    email2 = {
        FIELD_ID: 2,
        FIELD_SUBJECT: "Meeting Update",
        FIELD_SENDER: "Bob",
        FIELD_SENDER_EMAIL: "bob@example.com",
        FIELD_MESSAGE_ID: "msg2"
    }

    db_manager.emails_data = [email1, email2]
    db_manager._build_indexes()

    assert 1 in db_manager._search_index
    assert 2 in db_manager._search_index

    assert "hello world" in db_manager._search_index[1]
    assert "alice" in db_manager._search_index[1]
    assert "alice@example.com" in db_manager._search_index[1]

    assert "meeting update" in db_manager._search_index[2]
    assert "bob" in db_manager._search_index[2]

@pytest.mark.asyncio
async def test_search_functionality(db_manager):
    """Test search matches correctly using the index."""
    email1 = {
        FIELD_ID: 1,
        FIELD_SUBJECT: "Project Alpha",
        FIELD_SENDER: "Manager",
        FIELD_SENDER_EMAIL: "manager@corp.com",
        FIELD_MESSAGE_ID: "msg1"
    }
    email2 = {
        FIELD_ID: 2,
        FIELD_SUBJECT: "Lunch Plan",
        FIELD_SENDER: "Colleague",
        FIELD_SENDER_EMAIL: "friend@corp.com",
        FIELD_MESSAGE_ID: "msg2"
    }

    db_manager.emails_data = [email1, email2]
    db_manager._build_indexes()

    # Test subject match
    results = await db_manager.search_emails_with_limit("Alpha")
    assert len(results) == 1
    assert results[0][FIELD_ID] == 1

    # Test sender match
    results = await db_manager.search_emails_with_limit("Colleague")
    assert len(results) == 1
    assert results[0][FIELD_ID] == 2

    # Test email match
    results = await db_manager.search_emails_with_limit("manager@corp.com")
    assert len(results) == 1
    assert results[0][FIELD_ID] == 1

    # Test case insensitive
    results = await db_manager.search_emails_with_limit("alpha")
    assert len(results) == 1

    # Test no match
    results = await db_manager.search_emails_with_limit("Zebra")
    assert len(results) == 0

@pytest.mark.asyncio
async def test_search_index_update(db_manager):
    """Test that search index updates when email is added/updated."""
    # Add email
    email = {
        FIELD_MESSAGE_ID: "msg1",
        FIELD_SUBJECT: "Initial Subject",
        FIELD_SENDER: "Sender",
        FIELD_SENDER_EMAIL: "sender@test.com"
    }
    await db_manager.create_email(email)

    results = await db_manager.search_emails_with_limit("Initial")
    assert len(results) == 1

    # Update email
    await db_manager.update_email_by_message_id("msg1", {FIELD_SUBJECT: "Updated Subject"})

    # Search for old subject should fail
    results = await db_manager.search_emails_with_limit("Initial")
    assert len(results) == 0

    # Search for new subject should succeed
    results = await db_manager.search_emails_with_limit("Updated")
    assert len(results) == 1
