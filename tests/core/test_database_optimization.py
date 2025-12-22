import pytest
from src.core.database import DatabaseManager, DatabaseConfig, FIELD_ID
import os

@pytest.fixture
def db_config(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    return DatabaseConfig(data_dir=str(data_dir))

@pytest.mark.asyncio
async def test_create_email_populates_index(db_config):
    manager = DatabaseManager(config=db_config)
    await manager._ensure_initialized()

    email_data = {
        "messageId": "msg123",
        "subject": "Optimization Test",
        "sender": "Bolt",
        "sender_email": "bolt@example.com",
        "content": "Body"
    }

    # Create email
    result = await manager.create_email(email_data)

    # Verify created
    assert result is not None
    email_id = result[FIELD_ID]

    # Verify index
    assert email_id in manager._search_index
    search_text = manager._search_index[email_id]
    assert "optimization test" in search_text
    assert "bolt" in search_text
    assert "bolt@example.com" in search_text

    # Verify redundancy removal didn't break functionality
    # (Checking if update also works)

    update_data = {
        "subject": "Updated Subject"
    }
    await manager.update_email(email_id, update_data)

    search_text_updated = manager._search_index[email_id]
    assert "updated subject" in search_text_updated
    assert "optimization test" not in search_text_updated
