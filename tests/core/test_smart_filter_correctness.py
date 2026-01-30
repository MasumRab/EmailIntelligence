import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock
from src.core.smart_filter_manager import SmartFilterManager, EmailFilter
import json
import re

@pytest.mark.asyncio
async def test_filter_matching_correctness():
    """
    Verifies that filters match correctly against email data.
    This test covers:
    - Sender domain matching
    - Subject keyword matching
    - Content keyword matching
    - From patterns (regex) matching
    """
    manager = SmartFilterManager(db_path=":memory:")
    # Mock caching
    manager.caching_manager = MagicMock()
    manager.caching_manager.get = AsyncMock(return_value=None)
    manager.caching_manager.set = AsyncMock()
    manager.caching_manager.delete = AsyncMock()
    manager.caching_manager._ensure_initialized = AsyncMock()
    manager.caching_manager.close = AsyncMock()

    # Create filters manually

    # 1. Domain filter
    f1 = EmailFilter(
        filter_id="f1", name="Domain Filter", description="",
        criteria={"sender_domain": "example.com"}, actions={}, priority=10,
        effectiveness_score=0.0, created_at=None, last_used=None, usage_count=0,
        false_positive_rate=0.0, performance_metrics={}, is_active=True
    )

    # 2. Subject keyword filter (substring)
    f2 = EmailFilter(
        filter_id="f2", name="Subject Filter", description="",
        criteria={"subject_keywords": ["urgent", "Alert"]}, actions={}, priority=10,
        effectiveness_score=0.0, created_at=None, last_used=None, usage_count=0,
        false_positive_rate=0.0, performance_metrics={}, is_active=True
    )

    # 3. Content keyword filter
    f3 = EmailFilter(
        filter_id="f3", name="Content Filter", description="",
        criteria={"content_keywords": ["secret", "Confidential"]}, actions={}, priority=10,
        effectiveness_score=0.0, created_at=None, last_used=None, usage_count=0,
        false_positive_rate=0.0, performance_metrics={}, is_active=True
    )

    # 4. From pattern filter (regex)
    f4 = EmailFilter(
        filter_id="f4", name="Regex Filter", description="",
        criteria={"from_patterns": [r"^no-?reply@.*"]}, actions={}, priority=10,
        effectiveness_score=0.0, created_at=None, last_used=None, usage_count=0,
        false_positive_rate=0.0, performance_metrics={}, is_active=True
    )

    # Insert filters into DB
    for f in [f1, f2, f3, f4]:
         query = """
            INSERT INTO email_filters (
                filter_id, name, description, criteria, actions, priority,
                effectiveness_score, created_at, last_used, usage_count,
                false_positive_rate, performance_metrics, is_active
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
         """
         # Dummy timestamps
         ts = "2024-01-01T00:00:00"
         manager._db_execute(query, (
             f.filter_id, f.name, f.description, json.dumps(f.criteria), json.dumps(f.actions),
             f.priority, f.effectiveness_score, ts, ts, f.usage_count,
             f.false_positive_rate, json.dumps(f.performance_metrics), f.is_active
         ))

    # Test Case 1: Matching Domain
    email1 = {"sender_email": "user@example.com", "subject": "Hello", "content": "World"}
    res1 = await manager.apply_filters_to_email(email1)
    matched_ids1 = [m["filter_id"] for m in res1["filters_matched"]]
    assert "f1" in matched_ids1
    assert "f2" not in matched_ids1
    assert "f3" not in matched_ids1
    assert "f4" not in matched_ids1

    # Test Case 2: Matching Subject (case insensitive)
    email2 = {"sender_email": "user@other.com", "subject": "This is very URGENT", "content": "World"}
    res2 = await manager.apply_filters_to_email(email2)
    matched_ids2 = [m["filter_id"] for m in res2["filters_matched"]]
    assert "f2" in matched_ids2

    # Test Case 3: Matching Content
    email3 = {"sender_email": "user@other.com", "subject": "Hi", "content": "Top SECRET info"}
    res3 = await manager.apply_filters_to_email(email3)
    matched_ids3 = [m["filter_id"] for m in res3["filters_matched"]]
    assert "f3" in matched_ids3

    # Test Case 4: Matching Regex
    email4 = {"sender_email": "no-reply@service.com", "subject": "Hi", "content": "Info"}
    res4 = await manager.apply_filters_to_email(email4)
    matched_ids4 = [m["filter_id"] for m in res4["filters_matched"]]
    assert "f4" in matched_ids4

    # Test Case 5: Matching Regex Variant
    email5 = {"sender_email": "noreply@service.com", "subject": "Hi", "content": "Info"}
    res5 = await manager.apply_filters_to_email(email5)
    matched_ids5 = [m["filter_id"] for m in res5["filters_matched"]]
    assert "f4" in matched_ids5

    await manager.cleanup()
