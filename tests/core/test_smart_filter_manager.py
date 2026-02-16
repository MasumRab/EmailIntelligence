<<<<<<< HEAD
import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch
from datetime import datetime
import json
import sqlite3

# Import SmartFilterManager.
# Note: We assume the environment is set up such that imports work.
from src.core.smart_filter_manager import SmartFilterManager, EmailFilter

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
    manager._db_execute(query, (
        "f1", "Filter 1", "desc",
        json.dumps({"subject_keywords": ["test"]}),
        json.dumps({}),
        10, 0.0, now_str, now_str, 0, 0.0, "{}", 1
    ))

    # Filter 2 matches "email" in subject
    manager._db_execute(query, (
        "f2", "Filter 2", "desc",
        json.dumps({"subject_keywords": ["email"]}),
        json.dumps({}),
        10, 0.0, now_str, now_str, 0, 0.0, "{}", 1
    ))

    # Spy on _db_execute to count calls
    with patch.object(manager, '_db_execute', wraps=manager._db_execute) as mock_db_execute:
        # Action: Apply filters to an email that matches both
        email_data = {"subject": "This is a test email"}
        await manager.apply_filters_to_email(email_data)

        # Verification

        # Identify calls that update usage stats
        update_calls = [
            call for call in mock_db_execute.call_args_list
            if "UPDATE email_filters" in call[0][0] and "usage_count" in call[0][0]
        ]

        # In the optimized version, this should be 1 (batched update)
        assert len(update_calls) == 1, f"Expected 1 update call, got {len(update_calls)}"

        # Verify cache invalidation
        # Count how many times "active_filters_sorted" was deleted
        # Should be called exactly once
        delete_calls = [
            call for call in manager.caching_manager.delete.call_args_list
            if call[0][0] == "active_filters_sorted"
        ]
        assert len(delete_calls) == 1, f"Expected 1 cache invalidation, got {len(delete_calls)}"

    await manager.cleanup()
=======

import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock
from datetime import datetime, timezone
import json

from src.core.smart_filter_manager import SmartFilterManager, EmailFilter, _EmailContext

@pytest.fixture
def mock_db_manager():
    manager = SmartFilterManager(db_path=":memory:")
    manager.caching_manager = AsyncMock()
    manager._db_execute = MagicMock()
    manager._db_fetchall = MagicMock()
    manager._ensure_initialized = AsyncMock()
    manager._update_filter_usage = AsyncMock()

    # Mock methods that are called
    manager.get_active_filters_sorted = AsyncMock()

    return manager

@pytest.mark.asyncio
async def test_apply_filters_to_email_context_creation(mock_db_manager):
    """Verify that _EmailContext is correctly created and used."""

    # Setup a filter
    filter_obj = EmailFilter(
        filter_id="test_filter",
        name="Test Filter",
        description="Test",
        criteria={"subject_keywords": ["test"]},
        actions={"add_label": "Test"},
        priority=5,
        effectiveness_score=0.0,
        created_at=datetime.now(timezone.utc),
        last_used=datetime.now(timezone.utc),
        usage_count=0,
        false_positive_rate=0.0,
        performance_metrics={},
        is_active=True
    )

    mock_db_manager.get_active_filters_sorted.return_value = [filter_obj]

    email_data = {
        "id": "e1",
        "sender": "user@example.com",
        "subject": "This is a TEST email",
        "body": "Some content"
    }

    # We want to spy on _apply_filter_to_email to check arguments
    # But since it's a method on the instance we're testing, we can wrap it
    original_apply = mock_db_manager._apply_filter_to_email
    mock_db_manager._apply_filter_to_email = AsyncMock(side_effect=original_apply)

    result = await mock_db_manager.apply_filters_to_email(email_data)

    assert len(result["filters_matched"]) == 1
    assert result["filters_matched"][0]["filter_id"] == "test_filter"

    # Verify call args
    call_args = mock_db_manager._apply_filter_to_email.call_args
    assert call_args is not None
    filter_arg, context_arg = call_args[0]

    assert filter_arg == filter_obj
    assert isinstance(context_arg, _EmailContext)
    assert context_arg.subject_lower == "this is a test email"
    assert context_arg.sender_domain == "example.com"

@pytest.mark.asyncio
async def test_apply_filter_backward_compatibility(mock_db_manager):
    """Verify _apply_filter_to_email still works with a dictionary."""

    filter_obj = EmailFilter(
        filter_id="test_filter",
        name="Test Filter",
        description="Test",
        criteria={"subject_keywords": ["test"]},
        actions={"add_label": "Test"},
        priority=5,
        effectiveness_score=0.0,
        created_at=datetime.now(timezone.utc),
        last_used=datetime.now(timezone.utc),
        usage_count=0,
        false_positive_rate=0.0,
        performance_metrics={},
        is_active=True
    )

    email_data = {
        "sender": "user@example.com",
        "subject": "This is a TEST email",
        "body": "Some content"
    }

    # Pass dict directly
    result = await mock_db_manager._apply_filter_to_email(filter_obj, email_data)
    assert result is True

    # Fail case
    email_fail = {
        "sender": "user@example.com",
        "subject": "No match",
        "body": "Some content"
    }
    result_fail = await mock_db_manager._apply_filter_to_email(filter_obj, email_fail)
    assert result_fail is False

@pytest.mark.asyncio
async def test_batch_update_filter_usage(mock_db_manager):
    """Verify that _batch_update_filter_usage uses _db_executemany."""
    # Mock _db_executemany
    mock_db_manager._db_executemany = MagicMock()

    filters = [
        EmailFilter(
            filter_id=f"f{i}",
            name=f"Filter {i}",
            description="Test",
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
        ) for i in range(3)
    ]

    await mock_db_manager._batch_update_filter_usage(filters)

    # Verify _db_executemany was called once
    mock_db_manager._db_executemany.assert_called_once()

    # Verify arguments
    call_args = mock_db_manager._db_executemany.call_args
    query, params = call_args[0]

    assert "UPDATE email_filters" in query
    assert len(params) == 3
    assert params[0][1] == "f0"
    assert params[1][1] == "f1"
    assert params[2][1] == "f2"

    # Verify cache invalidation
    assert mock_db_manager.caching_manager.delete.call_count == 3
>>>>>>> 3809f0f3a2e942466dc0ff196cd81b50bb948e4c
