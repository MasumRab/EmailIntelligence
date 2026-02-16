import pytest
import asyncio
from unittest.mock import MagicMock
from src.core.database import DatabaseManager, DatabaseConfig, FIELD_ID, FIELD_CATEGORY_ID, FIELD_IS_UNREAD

@pytest.fixture
def db_config(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    return DatabaseConfig(data_dir=str(data_dir))

@pytest.fixture
def db_manager(db_config):
    manager = DatabaseManager(config=db_config)
    manager.caching_manager = MagicMock()
    # Mock category cache
    manager.categories_by_id = {}
    manager.emails_data = []
    manager._initialized = True
    return manager

@pytest.mark.asyncio
async def test_get_emails_filtering(db_manager):
    # Setup 10 emails
    # IDs 0-9.
    # Evens are unread.
    # ID 5 has category 1.

    emails = []
    for i in range(10):
        emails.append({
            FIELD_ID: i,
            FIELD_CATEGORY_ID: 1 if i == 5 else 0,
            FIELD_IS_UNREAD: i % 2 == 0,
            "created_at": "2023-01-01T00:00:00Z"
        })
    db_manager.emails_data = emails
    # _get_sorted_emails uses emails_data if cache is None
    db_manager._sorted_emails_cache = None

    # Test filtering by category
    results = await db_manager.get_emails(category_id=1, limit=10)
    assert len(results) == 1
    assert results[0][FIELD_ID] == 5

    # Test filtering by unread
    # Should get 0, 2, 4, 6, 8 (5 items)
    results = await db_manager.get_emails(is_unread=True, limit=10)
    assert len(results) == 5
    ids = sorted([r[FIELD_ID] for r in results])
    assert ids == [0, 2, 4, 6, 8]

    # Test combined
    # Unread and Category 0.
    # Unread: 0, 2, 4, 6, 8.
    # Category 0: All except 5.
    # So expected: 0, 2, 4, 6, 8.
    results = await db_manager.get_emails(category_id=0, is_unread=True, limit=10)
    assert len(results) == 5

    # Test offset and limit
    # Unread: 0, 2, 4, 6, 8.
    # Offset 1, Limit 2. -> 2, 4.
    results = await db_manager.get_emails(is_unread=True, limit=2, offset=1)
    assert len(results) == 2
    assert results[0][FIELD_ID] == 2
    assert results[1][FIELD_ID] == 4
