
import pytest
import sqlite3
import asyncio
from unittest.mock import AsyncMock
from datetime import datetime, timezone
from src.core.smart_filter_manager import SmartFilterManager, EmailFilter

@pytest.fixture
def real_db_manager():
    # Use in-memory database
    manager = SmartFilterManager(db_path=":memory:")
    # Mock caching manager
    manager.caching_manager = AsyncMock()
    manager.caching_manager.delete = AsyncMock()
    return manager

@pytest.mark.asyncio
async def test_batch_update_filter_usage_real_db(real_db_manager):
    """Verify that _batch_update_filter_usage correctly updates records in SQLite."""

    # Create some filters
    filters = []
    for i in range(5):
        filter_obj = EmailFilter(
            filter_id=f"f{i}",
            name=f"Filter {i}",
            description="Test",
            criteria={},
            actions={},
            priority=5,
            effectiveness_score=0.0,
            created_at=datetime.now(timezone.utc),
            last_used=datetime(2000, 1, 1, tzinfo=timezone.utc), # Old date
            usage_count=10,
            false_positive_rate=0.0,
            performance_metrics={},
            is_active=True
        )
        await real_db_manager._save_filter_async(filter_obj)
        filters.append(filter_obj)

    # Verify initial state
    rows = real_db_manager._db_fetchall("SELECT filter_id, usage_count, last_used FROM email_filters ORDER BY filter_id")
    for i, row in enumerate(rows):
        assert row["usage_count"] == 10
        # Check last_used is old
        assert str(row["last_used"]).startswith("2000-01-01")

    # Run batch update
    await real_db_manager._batch_update_filter_usage(filters)

    # Verify updates in DB
    rows = real_db_manager._db_fetchall("SELECT filter_id, usage_count, last_used FROM email_filters ORDER BY filter_id")
    for i, row in enumerate(rows):
        assert row["usage_count"] == 11
        # Check last_used is recent (not 2000)
        assert not str(row["last_used"]).startswith("2000-01-01")

    # Verify objects in memory are updated
    for f in filters:
        assert f.usage_count == 11
        assert f.last_used.year > 2000

@pytest.mark.asyncio
async def test_batch_update_filter_usage_empty(real_db_manager):
    """Verify empty list handling."""
    await real_db_manager._batch_update_filter_usage([])
    # Should not raise error

@pytest.mark.asyncio
async def test_batch_update_filter_usage_large_batch(real_db_manager):
    """Verify batching logic with more items than the batch size."""
    # Create 600 filters (batch size is 500)
    filters = []

    # Optimization: insert directly to DB for speed in test setup
    conn = real_db_manager._get_db_connection()
    now = datetime.now(timezone.utc).isoformat()

    for i in range(600):
        f_id = f"large_{i}"
        conn.execute(
            "INSERT INTO email_filters (filter_id, name, description, criteria, actions, created_at, last_used, usage_count, is_active) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (f_id, "n", "d", "{}", "{}", now, now, 0, 1)
        )
        filters.append(EmailFilter(
            filter_id=f_id,
            name="n",
            description="d",
            criteria={},
            actions={},
            priority=5,
            effectiveness_score=0.0,
            created_at=datetime.now(timezone.utc),
            last_used=datetime.now(timezone.utc),
            usage_count=0,
            false_positive_rate=0.0,
            performance_metrics={},
            is_active=True
        ))
    conn.commit()

    # Update
    await real_db_manager._batch_update_filter_usage(filters)

    # Verify count
    count = real_db_manager._db_fetchone("SELECT sum(usage_count) FROM email_filters")[0]
    assert count == 600
