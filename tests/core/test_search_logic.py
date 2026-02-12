import asyncio
import os
import shutil
import pytest
from unittest.mock import patch, MagicMock
from src.core.database import DatabaseManager, DatabaseConfig

@pytest.fixture
def db_config():
    temp_dir = "temp_search_opt_test"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    config = DatabaseConfig(data_dir=temp_dir)
    yield config
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

@pytest.mark.asyncio
async def test_search_early_exit(db_config):
    db = DatabaseManager(config=db_config)
    await db._ensure_initialized()

    # Create 50 emails.
    # The first 20 (most recent) have "target_keyword" in content.
    # The next 30 (older) also have "target_keyword" in content.
    # We want limit=10.
    # Ideal behavior: scan 10 most recent, find 10 matches, stop.
    # Worst case (current): scan all 50.

    # Note: create_email appends, so later emails are "newer" by default logic if IDs increment?
    # Actually create_email sets CREATED_AT to now().
    # To ensure order, we can rely on list order if timestamps are identical,
    # or just sleep a tiny bit? Or assume the sort key works.
    # Let's just create them.

    for i in range(50):
        await db.create_email({
            "subject": f"Email {i}",
            "sender": "sender@example.com",
            "content": f"Content with target_keyword for {i}"
        })

    # We mock gzip.open to count calls.
    # We need to wrap the real gzip.open to let it work, but count calls.
    import gzip
    real_gzip_open = gzip.open

    call_count = 0

    def side_effect(*args, **kwargs):
        nonlocal call_count
        # only count reads of content files
        if "email_content" in args[0] and "rt" in args[1]:
            call_count += 1
        return real_gzip_open(*args, **kwargs)

    with patch('gzip.open', side_effect=side_effect):
        # Search with limit 10
        # We expect to find the 10 most recent emails.
        # Since all 50 match, we should find 10 and stop.
        results = await db.search_emails_with_limit("target_keyword", limit=10)

        assert len(results) == 10

        # In current implementation, it scans ALL 50 because it builds the full list then sorts/slices.
        # So call_count should be 50.
        # With optimization, it should be closer to 10 (maybe a few more depending on implementation details).
        print(f"Gzip open calls: {call_count}")

        # If optimization works, this should be <= 15.
        # If not, it will be 50.
        assert call_count <= 15, f"Search should be efficient and stop early. Calls: {call_count}"

        # Verify results are the most recent ones (Email 49 down to 40)
        # Assuming higher ID = more recent/created later
        ids = [e['id'] for e in results]
        # Check if the IDs are the largest ones
        # We created 50 emails, IDs should be 1 to 50.
        # Top 10 should be 50 down to 41.
        assert min(ids) >= 41, f"Expected most recent emails, got IDs: {ids}"
