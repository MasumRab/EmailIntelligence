
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
