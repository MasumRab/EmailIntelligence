import asyncio
import os
import shutil
import pytest
from src.core.database import DatabaseManager, DatabaseConfig, FIELD_ID


@pytest.fixture
def temp_db():
    temp_dir = "temp_search_correctness"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)

    config = DatabaseConfig(data_dir=temp_dir)
    db = DatabaseManager(config=config)

    yield db

    shutil.rmtree(temp_dir)


@pytest.mark.asyncio
async def test_search_correctness_and_pagination(temp_db):
    db = temp_db
    await db._ensure_initialized()

    # Create 100 emails
    # Emails with even ID match "even"
    # Emails with odd ID match "odd"
    # IDs 1 to 100.
    # Time is not explicitly set, so created_at will be used.
    # create_email adds them sequentially, so ID 1 is oldest, ID 100 is newest.
    # DatabaseManager generates IDs incrementing.

    for i in range(1, 101):
        content = "even" if i % 2 == 0 else "odd"
        await db.create_email(
            {
                "subject": f"Email {i}",
                "sender": "test@example.com",
                "content": f"Content {i} {content}",
                "created_at": f"2023-01-01T{i:02d}:00:00Z",  # This might be overwritten by create_email
            }
        )

    # Note: create_email overwrites created_at with current time.
    # Since we await properly, they should be in time order roughly.
    # ID 100 is newest.

    # Search for "even" with limit 10
    # Should return newest even IDs: 100, 98, ..., 82.
    results = await db.search_emails_with_limit("even", limit=10, offset=0)

    assert len(results) == 10
    # Check order (descending by time/ID)
    ids = [e[FIELD_ID] for e in results]
    assert ids == [100, 98, 96, 94, 92, 90, 88, 86, 84, 82]

    # Test Pagination (page 2)
    results_page2 = await db.search_emails_with_limit("even", limit=10, offset=10)
    assert len(results_page2) == 10
    ids_page2 = [e[FIELD_ID] for e in results_page2]
    assert ids_page2 == [80, 78, 76, 74, 72, 70, 68, 66, 64, 62]

    # Search for term that is only in content (to force disk read)
    # The content logic is: "Content {i} {content}"
    # "Content 100" is in email 100.

    # Let's search for "Content" which is in all 100.
    results_content = await db.search_emails_with_limit("Content", limit=5)
    assert len(results_content) == 5
    ids_content = [e[FIELD_ID] for e in results_content]
    assert ids_content == [100, 99, 98, 97, 96]

    # Search for something that matches fewer than limit
    # "Content 5" matches 5, 50, 51, 52... 59.
    # Actually "Content 5" string matches "Content 5", "Content 50", etc.
    # "Content 5 " (with space) matches "Content 5 even/odd". Only ID 5.

    results_specific = await db.search_emails_with_limit("Content 5 ", limit=50)
    assert len(results_specific) == 1
    assert results_specific[0][FIELD_ID] == 5
