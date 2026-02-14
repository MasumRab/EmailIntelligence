import asyncio
import os
import shutil
import time

import pytest

from src.core.database import DatabaseConfig, DatabaseManager


@pytest.fixture
def temp_db():
    temp_dir = "temp_benchmark_data_pytest"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)

    config = DatabaseConfig(data_dir=temp_dir)
    db = DatabaseManager(config=config)

    yield db

    shutil.rmtree(temp_dir)


@pytest.mark.asyncio
async def test_search_performance_caching(temp_db):
    db = temp_db
    await db._ensure_initialized()

    # Populate with some data
    print("Populating data...")
    for i in range(100):  # Reduce count for quick test
        await db.create_email(
            {
                "subject": f"Test Email {i}",
                "sender": "sender@example.com",
                "sender_email": "sender@example.com",
                "content": f"This is the content of email {i}. random_keyword_{i % 10}",
            }
        )

    search_term = "random_keyword_5"

    # First search (Uncached)
    start_time = time.perf_counter()
    results1 = await db.search_emails_with_limit(search_term)
    end_time = time.perf_counter()
    duration1 = end_time - start_time

    # Second search (Cached)
    start_time = time.perf_counter()
    results2 = await db.search_emails_with_limit(search_term)
    end_time = time.perf_counter()
    duration2 = end_time - start_time

    print(f"Duration 1: {duration1:.6f}, Duration 2: {duration2:.6f}")

    assert len(results1) == len(results2)

    # Check if caching is working (second search should be significantly faster or at least not slower)
    # Note: with only 100 items, difference might be small, but cache access should be instant.
    # We assert duration2 is very small
    assert duration2 < 0.01

    # Verify cache invalidation
    await db.create_email(
        {
            "subject": "New Email with keyword",
            "content": f"This is a new email with {search_term}",
        }
    )

    # Third search (Uncached after invalidation)
    start_time = time.perf_counter()
    results3 = await db.search_emails_with_limit(search_term)
    end_time = time.perf_counter()
    duration3 = end_time - start_time

    assert len(results3) == len(results1) + 1
