
import pytest
import re
from src.core.smart_filter_manager import EmailFilter
from dataclasses import asdict

def test_email_filter_precomputed_population():
    criteria = {
        "subject_keywords": ["Urgent", "IMPORTANT"],
        "content_keywords": ["Action", "ReQuired"],
        "from_patterns": ["^noreply.*", "admin@.*"]
    }

    ef = EmailFilter(
        filter_id="test1",
        name="Test Filter",
        description="desc",
        criteria=criteria,
        actions={},
        priority=1,
        effectiveness_score=0.0,
        created_at=None,
        last_used=None,
        usage_count=0,
        false_positive_rate=0.0,
        performance_metrics={},
        is_active=True
    )

    # Check _precomputed existence
    assert hasattr(ef, "_precomputed")

    # Check subject keywords (lowercased)
    assert "urgent" in ef._precomputed["subject_keywords"]
    assert "important" in ef._precomputed["subject_keywords"]
    assert "Urgent" not in ef._precomputed["subject_keywords"]

    # Check content keywords (lowercased)
    assert "action" in ef._precomputed["content_keywords"]
    assert "required" in ef._precomputed["content_keywords"]

    # Check regex patterns
    patterns = ef._precomputed["from_patterns"]
    assert len(patterns) == 2
    assert patterns[0].pattern == "^noreply.*"
    assert patterns[0].flags & re.IGNORECASE

def test_email_filter_invalid_regex():
    criteria = {
        "from_patterns": ["[invalid_regex"]
    }

    ef = EmailFilter(
        filter_id="test2",
        name="Invalid Regex Filter",
        description="desc",
        criteria=criteria,
        actions={},
        priority=1,
        effectiveness_score=0.0,
        created_at=None,
        last_used=None,
        usage_count=0,
        false_positive_rate=0.0,
        performance_metrics={},
        is_active=True
    )

    # Should not crash, and list should be empty (or skipped)
    assert hasattr(ef, "_precomputed")
    assert "from_patterns" in ef._precomputed
    # The invalid regex should be skipped
    assert len(ef._precomputed["from_patterns"]) == 0
