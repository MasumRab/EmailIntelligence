
import asyncio
import sys
import os
import sqlite3
import time
from unittest.mock import MagicMock, patch

# Add src to path
sys.path.append(os.path.join(os.getcwd(), "src"))

try:
    from core.smart_filter_manager import SmartFilterManager
    from core.enhanced_caching import EnhancedCachingManager
except ImportError as e:
    print(f"Import failed: {e}")
    sys.exit(1)

async def benchmark_verification():
    print("Verifying Benchmark for SmartFilterManager...")

    # Setup
    manager = SmartFilterManager(db_path=":memory:")

    # We will spy on _db_fetchall to verify it's called only once for active filters
    original_fetchall = manager._db_fetchall
    manager._db_fetchall = MagicMock(side_effect=original_fetchall)

    # Create a test filter
    await manager.add_custom_filter(
        name="Test Filter",
        description="Test",
        criteria={"subject_keywords": ["test"]},
        actions={"add_label": "TestLabel"},
        priority=10
    )

    print("\n--- Running Verification ---")
    email_data = {"id": "1", "subject": "This is a test email", "sender": "test@example.com"}

    iterations = 50
    db_hits = 0

    # Pre-warm: Run once to fill cache
    await manager.apply_filters_to_email(email_data)
    manager._db_fetchall.reset_mock() # Reset count

    for i in range(iterations):
        await manager.apply_filters_to_email(email_data)

    # Check call args of _db_fetchall
    for call in manager._db_fetchall.call_args_list:
        args, _ = call
        query = args[0]
        # We are looking for the active filters query
        if "SELECT * FROM email_filters WHERE is_active = 1" in query:
            db_hits += 1

    print(f"Processed {iterations} emails.")
    print(f"DB Hits for active filters: {db_hits}")

    # Verify usage count updated in DB
    rows = manager._db_fetchall("SELECT usage_count FROM email_filters WHERE name='Test Filter'")
    usage_count = rows[0]["usage_count"]
    print(f"Filter usage count: {usage_count}")

    if db_hits == 0:
        print("SUCCESS: Zero DB hits for active filters (served from cache).")
        if usage_count == iterations + 1:
            print("SUCCESS: Usage count correctly updated in DB.")
        else:
            print(f"WARNING: Usage count mismatch (Expected {iterations + 1}, got {usage_count})")
    else:
        print(f"FAILURE: {db_hits} DB hits detected (Expected 0 after warm-up).")

if __name__ == "__main__":
    asyncio.run(benchmark_verification())
