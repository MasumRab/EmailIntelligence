import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch
from src.core.smart_filter_manager import SmartFilterManager, EmailFilter
import json
from datetime import datetime

@pytest.mark.asyncio
async def test_apply_filters_uses_precomputed_data():
    """
    Verifies that apply_filters_to_email calculates precomputed data
    and passes it to _apply_filter_to_email.
    """
    manager = SmartFilterManager(db_path=":memory:")
    manager.caching_manager = MagicMock()
    manager.caching_manager.get = AsyncMock(return_value=None)
    manager.caching_manager.set = AsyncMock()
    manager.caching_manager.delete = AsyncMock()
    manager.caching_manager._ensure_initialized = AsyncMock()

    # Create a filter
    query = """
    INSERT INTO email_filters (
        filter_id, name, description, criteria, actions, priority,
        effectiveness_score, created_at, last_used, usage_count,
        false_positive_rate, performance_metrics, is_active
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    now_str = datetime.now().isoformat()
    manager._db_execute(query, (
        "f1", "Filter 1", "desc",
        json.dumps({"subject_keywords": ["test"]}),
        json.dumps({}),
        10, 0.0, now_str, now_str, 0, 0.0, "{}", 1
    ))

    # Spy on _apply_filter_to_email
    with patch.object(manager, '_apply_filter_to_email', wraps=manager._apply_filter_to_email) as mock_apply:
        email_data = {
            "subject": "This is a TEST subject",
            "content": "Content",
            "sender": "user@EXAMPLE.com"
        }
        await manager.apply_filters_to_email(email_data)

        # Verify call arguments
        assert mock_apply.called
        call_args = mock_apply.call_args
        kwargs = call_args.kwargs
        precomputed = kwargs.get('precomputed_email')

        assert precomputed is not None
        assert precomputed['subject_lower'] == "this is a test subject"
        assert precomputed['sender_lower'] == "user@example.com"
        assert precomputed['sender_domain'] == "example.com"

    await manager.cleanup()

@pytest.mark.asyncio
async def test_email_filter_precomputes_criteria():
    """Verifies that EmailFilter precomputes criteria on instantiation."""
    criteria = {
        "subject_keywords": ["Test", "URGENT"],
        "sender_domain": "Example.COM"
    }

    filter_obj = EmailFilter(
        filter_id="id",
        name="name",
        description="desc",
        criteria=criteria,
        actions={},
        priority=1,
        effectiveness_score=0.0,
        created_at=datetime.now(),
        last_used=datetime.now(),
        usage_count=0,
        false_positive_rate=0.0,
        performance_metrics={}
    )

    # Check _precomputed populated
    assert filter_obj._precomputed is not None
    assert filter_obj._precomputed["subject_keywords_lower"] == ["test", "urgent"]
    assert filter_obj._precomputed["sender_domain_lower"] == "example.com"
