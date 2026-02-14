import asyncio
import json
import sqlite3
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Import SmartFilterManager.
# Note: We assume the environment is set up such that imports work.
from src.core.smart_filter_manager import EmailFilter, SmartFilterManager


@pytest.mark.asyncio
async def test_apply_filters_to_email_optimized_behavior():
    """
    Verifies that the optimized implementation performs a single batched DB update and cache invalidation
    when multiple filters match.
    """
    # Setup with in-memory DB
    manager = SmartFilterManager(db_path=":memory:")

    # Mock caching manager completely to avoid issues with missing methods or backends
    manager.caching_manager = MagicMock()
    manager.caching_manager.get = AsyncMock(return_value=None)
    manager.caching_manager.set = AsyncMock()
    manager.caching_manager.delete = AsyncMock()
    manager.caching_manager._ensure_initialized = AsyncMock()
    manager.caching_manager.close = AsyncMock()

    # Pre-populate DB with 2 filters that will match
    # We use direct SQL to avoid side effects of helper methods
    query = """
    INSERT INTO email_filters (
        filter_id, name, description, criteria, actions, priority,
        effectiveness_score, created_at, last_used, usage_count,
        false_positive_rate, performance_metrics, is_active
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    now_str = datetime.now().isoformat()

    # Filter 1 matches "test" in subject
    manager._db_execute(
        query,
        (
            "f1",
            "Filter 1",
            "desc",
            json.dumps({"subject_keywords": ["test"]}),
            json.dumps({}),
            10,
            0.0,
            now_str,
            now_str,
            0,
            0.0,
            "{}",
            1,
        ),
    )

    # Filter 2 matches "email" in subject
    manager._db_execute(
        query,
        (
            "f2",
            "Filter 2",
            "desc",
            json.dumps({"subject_keywords": ["email"]}),
            json.dumps({}),
            10,
            0.0,
            now_str,
            now_str,
            0,
            0.0,
            "{}",
            1,
        ),
    )

    # Spy on _db_execute to count calls
    with patch.object(
        manager, "_db_execute", wraps=manager._db_execute
    ) as mock_db_execute:
        # Action: Apply filters to an email that matches both
        email_data = {"subject": "This is a test email"}
        await manager.apply_filters_to_email(email_data)

        # Verification

        # Identify calls that update usage stats
        update_calls = [
            call
            for call in mock_db_execute.call_args_list
            if "UPDATE email_filters" in call[0][0] and "usage_count" in call[0][0]
        ]

        # In the optimized version, this should be 1 (batched update)
        assert (
            len(update_calls) == 1
        ), f"Expected 1 update call, got {len(update_calls)}"

        # Verify cache invalidation
        # Count how many times "active_filters_sorted" was deleted
        # Should be called exactly once
        delete_calls = [
            call
            for call in manager.caching_manager.delete.call_args_list
            if call[0][0] == "active_filters_sorted"
        ]
        assert (
            len(delete_calls) == 1
        ), f"Expected 1 cache invalidation, got {len(delete_calls)}"

    await manager.cleanup()
