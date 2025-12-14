import pytest
import pytest_asyncio
import os
import shutil
import asyncio
import sys

# Ensure src is in path
sys.path.insert(0, os.path.abspath("src"))

from core.database import DatabaseManager, DatabaseConfig, HEAVY_EMAIL_FIELDS

@pytest_asyncio.fixture
async def fresh_db():
    TEST_DIR = "test_data_perf_unit"
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)
    os.makedirs(TEST_DIR)

    config = DatabaseConfig(data_dir=TEST_DIR)
    db = DatabaseManager(config)
    await db._ensure_initialized()

    yield db

    # Cleanup
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)

@pytest.mark.asyncio
async def test_search_parallel_correctness(fresh_db):
    # Create emails
    # 1. Matches in subject
    # 2. Matches in content
    # 3. No match

    await fresh_db.create_email({
        "subject": "Apple Pie",
        "content": "Just food",
        "message_id": "1"
    })

    await fresh_db.create_email({
        "subject": "Banana Bread",
        "content": "Contains Apple slices",
        "message_id": "2"
    })

    await fresh_db.create_email({
        "subject": "Cherry Tart",
        "content": "No fruit mentioned",
        "message_id": "3"
    })

    # Search for "Apple"
    results = await fresh_db.search_emails_with_limit("Apple")

    # Should find 1 (Subject) and 2 (Content)
    assert len(results) == 2
    ids = sorted([e["message_id"] for e in results])
    assert ids == ["1", "2"]

@pytest.mark.asyncio
async def test_search_parallel_performance(fresh_db):
    # Create 100 emails with content match to trigger parallel path
    # We can't easily assert speed here without a baseline, but we can assert it completes successfully
    for i in range(100):
         await fresh_db.create_email({
            "subject": f"Subject {i}",
            "content": f"Content {i} SEARCH_TOKEN",
            "message_id": f"msg_{i}"
        })

    results = await fresh_db.search_emails_with_limit("SEARCH_TOKEN", limit=100)
    assert len(results) == 100
