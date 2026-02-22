
import pytest
from unittest.mock import MagicMock
from datetime import datetime, timedelta
from src.core.database import DatabaseManager, DatabaseConfig, FIELD_ID, FIELD_CREATED_AT, FIELD_IS_UNREAD

@pytest.fixture
def db_config(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    return DatabaseConfig(data_dir=str(data_dir))

import pytest_asyncio

@pytest_asyncio.fixture
async def db_manager(db_config):
    manager = DatabaseManager(config=db_config)
    await manager._ensure_initialized()
    return manager

@pytest.mark.asyncio
async def test_get_emails_pagination_and_filtering(db_manager):
    """
    Verify get_emails handles filtering and pagination correctly.
    Using monotonically increasing timestamps to ensure stable sort order.
    """
    base_time = datetime(2023, 1, 1, 12, 0, 0)

    # Create 10 emails with distinct timestamps
    for i in range(10):
        # Even IDs are unread, Odd are read
        is_unread = (i % 2 == 0)
        # Each email 1 hour apart
        created_at = (base_time + timedelta(hours=i)).isoformat()

        await db_manager.create_email({
            FIELD_ID: i, # Explicit ID if supported, or rely on order
            "subject": f"Email {i}",
            FIELD_IS_UNREAD: is_unread,
            FIELD_CREATED_AT: created_at,
            "messageId": f"msg_{i}"
        })

    # Filter unread: IDs 0, 2, 4, 6, 8 (all have distinct timestamps)
    # Sorted by created_at DESC (default in get_emails usually): 8, 6, 4, 2, 0

    # Test pagination: limit 2, offset 1
    # Full list (desc): [8, 6, 4, 2, 0]
    # Offset 1: starts at 6
    # Limit 2: [6, 4]

    emails = await db_manager.get_emails(is_unread=True, limit=2, offset=1)

    assert len(emails) == 2
    assert emails[0]["subject"] == "Email 6"
    assert emails[1]["subject"] == "Email 4"
