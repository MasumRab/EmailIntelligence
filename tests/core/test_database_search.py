
import asyncio
import gzip
import json
import os
import shutil
import tempfile
import time
import pytest
from src.core.database import DatabaseManager, DatabaseConfig

@pytest.fixture
def temp_db_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.mark.asyncio
async def test_search_performance_bottleneck(temp_db_dir):
    config = DatabaseConfig(data_dir=temp_db_dir)
    db = DatabaseManager(config)
    await db._ensure_initialized()

    # Create a large number of emails
    num_emails = 1000
    search_term = "findingnemo"

    # Generate emails
    for i in range(num_emails):
        # 10% have the term in content, others don't
        has_term = (i % 10) == 0
        content = f"This is the content of email {i}. " + (search_term if has_term else "nothing here")

        email_data = {
            "subject": f"Subject {i}",
            "sender": f"sender{i}@example.com",
            "content": content,
            "messageId": f"msg-{i}"
        }
        await db.create_email(email_data)

    # Measure search time (first run)
    start_time = time.time()
    results = await db.search_emails_with_limit(search_term, limit=100)
    end_time = time.time()

    duration = end_time - start_time
    print(f"\nSearch time for {num_emails} emails (first run): {duration:.4f} seconds")

    # Measure search time (second run - should be cached)
    start_time = time.time()
    results_2 = await db.search_emails_with_limit(search_term, limit=100)
    end_time = time.time()

    duration_2 = end_time - start_time
    print(f"Search time for {num_emails} emails (cached): {duration_2:.4f} seconds")

    assert len(results) > 0
    assert len(results_2) == len(results)
    assert duration_2 < duration # Cached should be faster

    # Verify content available index works (checking logs manually or inference)
    # If we delete a content file but don't update index, it should handle error gracefully
    # If we use search term that is NOT in content index, it shouldn't check disk.

    # Test term not in light data, not in any content
    start_time = time.time()
    await db.search_emails_with_limit("nonexistenttermXYZ", limit=100)
    end_time = time.time()
    print(f"Search time for nonexistent term: {end_time - start_time:.4f} seconds")
