import pytest
import pytest_asyncio
import os
import shutil
import sys

# Ensure src is in path
sys.path.insert(0, os.path.abspath("src"))

from core.database import DatabaseManager, DatabaseConfig, HEAVY_EMAIL_FIELDS

pytestmark = pytest.mark.asyncio

@pytest_asyncio.fixture
async def fresh_db():
    TEST_DIR = "test_data_core_db"
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)
    os.makedirs(TEST_DIR)

    config = DatabaseConfig(data_dir=TEST_DIR)
    db = DatabaseManager(config)
    await db._ensure_initialized()

    yield db

    await db.shutdown()
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)

async def test_search_emails_parallel(fresh_db):
    # Create emails
    for i in range(10):
        await fresh_db.create_email({
            "subject": f"Subject {i}",
            "content": f"Content {i} SEARCH_TARGET",
            "message_id": f"msg_{i}"
        })

    # Search for SEARCH_TARGET (in content)
    results = await fresh_db.search_emails_with_limit("SEARCH_TARGET", limit=100)
    assert len(results) == 10

async def test_search_emails_metadata(fresh_db):
    # Create emails
    for i in range(10):
        await fresh_db.create_email({
            "subject": f"Subject {i} METADATA_TARGET",
            "content": f"Content {i}",
            "message_id": f"msg_{i}"
        })

    # Search for METADATA_TARGET (in subject)
    results = await fresh_db.search_emails_with_limit("METADATA_TARGET", limit=100)
    assert len(results) == 10

async def test_search_emails_mixed(fresh_db):
    # 5 matching metadata, 5 matching content
    for i in range(5):
        await fresh_db.create_email({
            "subject": f"Subject {i} MIXED_TARGET",
            "content": f"Content {i}",
            "message_id": f"msg_meta_{i}"
        })
    for i in range(5):
        await fresh_db.create_email({
            "subject": f"Subject {i}",
            "content": f"Content {i} MIXED_TARGET",
            "message_id": f"msg_content_{i}"
        })

    results = await fresh_db.search_emails_with_limit("MIXED_TARGET", limit=100)
    assert len(results) == 10
