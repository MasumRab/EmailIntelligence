import asyncio
import os
import json
import gzip
import time
import shutil
import sys

# Add src to path
sys.path.insert(0, os.path.abspath("src"))

from core.database import DatabaseManager, DatabaseConfig

# Setup temp data dir
TEST_DIR = "test_data_perf"

async def setup_data():
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)
    os.makedirs(TEST_DIR)

    config = DatabaseConfig(data_dir=TEST_DIR)
    db = DatabaseManager(config)
    await db._ensure_initialized()

    # Create 200 emails
    # 100 match in subject (fast)
    # 100 match in content only (slow path)

    print("Generating data...")
    for i in range(200):
        email_data = {
            "subject": f"Subject {i}",
            "sender": "sender@example.com",
            "message_id": f"msg_{i}",
            "content": f"This is the content of email {i}. SEARCH_TARGET" if i >= 100 else f"This is the content of email {i}."
        }
        # For first 100, put SEARCH_TARGET in subject
        if i < 100:
            email_data["subject"] += " SEARCH_TARGET"

        await db.create_email(email_data)

    print("Data generated.")
    return db

async def run_test():
    db = await setup_data()

    start_time = time.time()
    results = await db.search_emails_with_limit("SEARCH_TARGET", limit=200)
    end_time = time.time()

    print(f"Search took: {end_time - start_time:.4f} seconds")
    print(f"Found {len(results)} emails")

    # Cleanup
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)

if __name__ == "__main__":
    asyncio.run(run_test())
