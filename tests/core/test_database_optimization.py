import pytest
import asyncio
from unittest.mock import MagicMock
from src.core.database import DatabaseManager, FIELD_ID, FIELD_CATEGORY_ID, FIELD_IS_UNREAD, FIELD_CREATED_AT

@pytest.fixture
def db_manager():
    manager = DatabaseManager()
    manager.caching_manager = MagicMock()
    manager.caching_manager.get_email_content.return_value = None
    manager.emails_data = []
    manager._initialized = True
    return manager

@pytest.mark.asyncio
async def test_get_emails_filtering_pagination(db_manager):
    # Setup 100 emails
    # 0-49: Category 1
    # 50-99: Category 2
    # Even: Unread
    # Odd: Read

    # We add them in reverse order of ID to simulate "latest first" if sorted by ID,
    # but let's just rely on sort.
    # Note: _get_sorted_emails sorts by FIELD_TIME or FIELD_CREATED_AT reverse.

    emails = []
    for i in range(100):
        emails.append({
            FIELD_ID: i,
            FIELD_CATEGORY_ID: 1 if i < 50 else 2,
            FIELD_IS_UNREAD: i % 2 == 0,
            FIELD_CREATED_AT: f"2023-01-01T00:0{i//10}:{i%10}0Z" # ensure sort order matches ID order roughly
        })

    # Sort them by time reverse explicitly to know the order
    # Later times are first. i=99 is latest.
    # So order is 99, 98, ..., 0

    db_manager.emails_data = emails

    # Verify order without filters
    results = await db_manager.get_emails(limit=10, offset=0)
    assert len(results) == 10
    assert results[0][FIELD_ID] == 99
    assert results[9][FIELD_ID] == 90

    # Test Category Filter (Category 2 is 50-99)
    # Order: 99, 98, ..., 50
    results = await db_manager.get_emails(limit=10, offset=0, category_id=2)
    assert len(results) == 10
    assert results[0][FIELD_ID] == 99
    assert results[9][FIELD_ID] == 90

    # Test Pagination with Filter
    # Category 2 items are 50 items (50-99).
    # Page 2 (offset 10, limit 10) -> 89...80
    results = await db_manager.get_emails(limit=10, offset=10, category_id=2)
    assert len(results) == 10
    assert results[0][FIELD_ID] == 89
    assert results[9][FIELD_ID] == 80

    # Test Unread Filter
    # Even numbers are unread.
    # Order: 99(Read), 98(Unread), 97(R), 96(U)...
    # Filtered stream: 98, 96, 94...
    results = await db_manager.get_emails(limit=5, offset=0, is_unread=True)
    assert len(results) == 5
    assert results[0][FIELD_ID] == 98
    assert results[1][FIELD_ID] == 96

    # Test Offset with Unread Filter
    # Offset 5 means skip 98, 96, 94, 92, 90. Start at 88.
    results = await db_manager.get_emails(limit=5, offset=5, is_unread=True)
    assert len(results) == 5
    assert results[0][FIELD_ID] == 88

    # Test Both Filters
    # Category 1 (0-49), Unread (Even).
    # IDs: 49(R), 48(U), 47(R), 46(U)... 0(U)
    # Stream: 48, 46, 44... 0
    results = await db_manager.get_emails(limit=5, offset=0, category_id=1, is_unread=True)
    assert len(results) == 5
    assert results[0][FIELD_ID] == 48

    # Edge case: Limit > Remaining
    # Only 25 items match Category 1 + Unread (0, 2, ... 48)
    # We ask for limit 50.
    results = await db_manager.get_emails(limit=50, offset=0, category_id=1, is_unread=True)
    assert len(results) == 25
    assert results[0][FIELD_ID] == 48
    assert results[-1][FIELD_ID] == 0

    # Edge case: Offset > Total Matches
    results = await db_manager.get_emails(limit=10, offset=100, category_id=1)
    assert len(results) == 0
