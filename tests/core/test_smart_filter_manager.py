
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
    mock_db_manager._apply_filter_to_email = MagicMock(side_effect=original_apply)

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
    result = mock_db_manager._apply_filter_to_email(filter_obj, email_data)
    assert result is True

    # Fail case
    email_fail = {
        "sender": "user@example.com",
        "subject": "No match",
        "body": "Some content"
    }
    result_fail = mock_db_manager._apply_filter_to_email(filter_obj, email_fail)
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


@pytest.mark.asyncio
async def test_filter_compilation(mock_db_manager):
    """Verify that filters have their patterns compiled."""
    filter_obj = EmailFilter(
        filter_id="test_filter",
        name="Test Filter",
        description="Test",
        criteria={"from_patterns": ["^test.*"]},
        actions={},
        priority=5,
        effectiveness_score=0.0,
        created_at=datetime.now(timezone.utc),
        last_used=datetime.now(timezone.utc),
        usage_count=0,
        false_positive_rate=0.0,
        performance_metrics={},
        is_active=True
    )

    mock_db_manager._compile_filter_patterns(filter_obj)

    assert filter_obj._compiled_patterns is not None
    assert "from_patterns" in filter_obj._compiled_patterns
    assert len(filter_obj._compiled_patterns["from_patterns"]) == 1
    assert filter_obj._compiled_patterns["from_patterns"][0].pattern == "^test.*"
