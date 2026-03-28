import asyncio
import time
import os
import shutil
import random
from src.core.database import DatabaseManager, DatabaseConfig, FIELD_CREATED_AT
from datetime import datetime, timedelta, timezone

async def run_benchmark():
    temp_dir = "benchmark_data"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)

    config = DatabaseConfig(data_dir=temp_dir)
    db = DatabaseManager(config=config)
    await db._ensure_initialized()

    # Generate 10000 emails
    # 100 with "common_term" in subject (recent)
    # 100 with "rare_term" in content (old)
    # Rest random

    print("Generating 10000 emails...")
    start_gen = time.perf_counter()

    now = datetime.now(timezone.utc)

    for i in range(10000):
        # Create varying timestamps to test sorting
        created_at = (now - timedelta(days=i)).isoformat()

        email_data = {
            "subject": f"Subject {i}",
            "sender": "sender@example.com",
            "sender_email": "sender@example.com",
            "content": f"Content {i}",
            "created_at": created_at,
            "time": created_at # Use both fields to be sure
        }

        if i < 100: # Most recent 100
            email_data["subject"] += " common_term"
        elif i >= 9900: # Oldest 100
             email_data["content"] += " rare_term"

        await db.create_email(email_data)

    end_gen = time.perf_counter()
    print(f"Generation took {end_gen - start_gen:.2f}s")

    # Benchmark 1: Search for "common_term" (should be fast with optimization)
    # Limit 50. Should find in first 50 items if sorted correctly.
    print("\n--- Benchmark 1: Common Term (Metadata, Recent) ---")
    start = time.perf_counter()
    results = await db.search_emails_with_limit("common_term", limit=50)
    end = time.perf_counter()
    print(f"Time: {end - start:.4f}s")
    print(f"Found: {len(results)}")

    # Benchmark 2: Search for "rare_term" (Content, Old)
    # Limit 50. Will scan everything and find only ~100.
    print("\n--- Benchmark 2: Rare Term (Content, Old) ---")
    start = time.perf_counter()
    results = await db.search_emails_with_limit("rare_term", limit=50)
    end = time.perf_counter()
    print(f"Time: {end - start:.4f}s")
    print(f"Found: {len(results)}")

    # Benchmark 3: Search for "nonexistent" (Worst case)
    print("\n--- Benchmark 3: Nonexistent ---")
    start = time.perf_counter()
    results = await db.search_emails_with_limit("nonexistent", limit=50)
    end = time.perf_counter()
    print(f"Time: {end - start:.4f}s")
    print(f"Found: {len(results)}")

    shutil.rmtree(temp_dir)

if __name__ == "__main__":
    asyncio.run(run_benchmark())
