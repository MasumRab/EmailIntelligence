import asyncio
import os
import shutil
import time
import pytest
import pytest_asyncio
import gzip
from unittest.mock import patch, MagicMock
from src.core.database import DatabaseManager, DatabaseConfig

@pytest_asyncio.fixture
async def db_instance():
    temp_dir = "temp_search_perf_test_data"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)

    config = DatabaseConfig(data_dir=temp_dir)
    db = DatabaseManager(config=config)
    await db._ensure_initialized()

    yield db

    # Cleanup
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

# Helper to check call count on gzip.open
class GzipOpenSpy:
    def __init__(self):
        self.call_count = 0
        self.original_open = gzip.open

    def open(self, filename, mode="rb", *args, **kwargs):
        # Only count if reading content files (which contain "email_content")
        if isinstance(filename, str) and "email_content" in filename and "r" in mode:
            self.call_count += 1
        return self.original_open(filename, mode, *args, **kwargs)

@pytest.mark.asyncio
async def test_search_early_exit(db_instance):
    db = db_instance

    # Create 50 emails
    # Email 49 (newest) matches in content (heavy)
    # Email 0 (oldest) matches in content (heavy)
    # Others don't match
    target_keyword = "special_keyword_123"

    # We want strictly increasing timestamps
    base_time = time.time()

    for i in range(50):
        content = "Regular content"
        if i == 0 or i == 49:
            content = f"Content with {target_keyword}"

        await db.create_email({
            "subject": f"Email {i}",
            "sender": "sender@example.com",
            "sender_email": "sender@example.com",
            "content": content,
            # Force timestamp to ensure order
            "created_at": base_time + i
        })
        # Update internal timestamp to match loop index for sorting reliability
        db.emails_data[-1]["created_at"] = (base_time + i)

    spy = GzipOpenSpy()

    with patch("gzip.open", side_effect=spy.open):
        # Search with limit=1.
        # Should find the newest one (index 49) immediately and stop.
        # So we expect 1 content file read (for index 49).
        results = await db.search_emails_with_limit(target_keyword, limit=1)

    assert len(results) == 1
    # Check subject to confirm it's the newest (Email 49)
    assert results[0]["subject"] == "Email 49"

    print(f"gzip.open called {spy.call_count} times")

    # Without optimization: It iterates all 50 emails. checks content for all. call_count == 50.
    # With optimization: checks email 49 (newest), matches, stops. call_count == 1.
    # We assert it's significantly less than 50
    assert spy.call_count < 10

@pytest.mark.asyncio
async def test_search_sorts_correctly(db_instance):
    """Verify that we still get the correct sorted results even with optimization."""
    db = db_instance
    target_keyword = "common_keyword"

    base_time = time.time()

    # Create 10 emails, all matching in content
    for i in range(10):
        await db.create_email({
            "subject": f"Email {i}",
            "content": f"Content with {target_keyword}",
             "created_at": base_time + i
        })
        # Force strict ordering in memory
        db.emails_data[-1]["created_at"] = base_time + i

    # Search limit 5
    results = await db.search_emails_with_limit(target_keyword, limit=5)

    assert len(results) == 5
    # Should be 9, 8, 7, 6, 5
    assert results[0]["subject"] == "Email 9"
    assert results[4]["subject"] == "Email 5"
