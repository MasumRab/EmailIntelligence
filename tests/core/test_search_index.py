
import os
import shutil
import pytest
from src.core.database import DatabaseManager, DatabaseConfig


@pytest.fixture
def temp_db():
    temp_dir = "temp_smoke_test_data"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)

    config = DatabaseConfig(data_dir=temp_dir)
    db = DatabaseManager(config=config)

    yield db

    shutil.rmtree(temp_dir)


@pytest.mark.asyncio
async def test_database_smoke(temp_db):
    db = temp_db
    await db._ensure_initialized()

    # Test Create
    email_data = {
        "subject": "Test Email",
        "sender": "sender@example.com",
        "sender_email": "sender@example.com",
        "content": "This is content."
    }
    created_email = await db.create_email(email_data)
    assert created_email is not None
    assert created_email["subject"] == "Test Email"
    email_id = created_email["id"]

    # Test Search Index Population
    assert email_id in db.email_search_index
    assert "test email" in db.email_search_index[email_id]

    # Test Get
    fetched_email = await db.get_email_by_id(email_id)
    assert fetched_email["subject"] == "Test Email"

    # Test Search
    results = await db.search_emails_with_limit("Test")
    assert len(results) == 1
    assert results[0]["id"] == email_id

    # Test Update
    updated_data = {"subject": "Updated Subject"}
    updated_email = await db.update_email(email_id, updated_data)
    assert updated_email["subject"] == "Updated Subject"

    # Test Index Update
    assert "updated subject" in db.email_search_index[email_id]

    # Test Search after update
    results_updated = await db.search_emails_with_limit("Updated")
    assert len(results_updated) == 1

    results_old = await db.search_emails_with_limit("Test Email")
    # Should NOT find it by old subject
    # But wait, we lowered subject, sender, sender_email.
    # Sender is still "sender@example.com".
    # So "Test Email" shouldn't match "updated subject sender...".
    assert len(results_old) == 0

    # Test Message ID Update
    msg_id = "msg123"
    await db.update_email(email_id, {"message_id": msg_id})

    await db.update_email_by_message_id(msg_id, {"subject": "Message ID Update"})
    assert "message id update" in db.email_search_index[email_id]
