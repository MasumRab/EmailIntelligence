import asyncio
import os
import shutil
import pytest
import sqlite3
import json
import pytest_asyncio
from datetime import datetime, timezone
from src.core.smart_filter_manager import SmartFilterManager, EmailFilter
from src.core.database import DatabaseConfig

@pytest.fixture
def temp_db_path():
    """Create a temporary directory and database file for testing."""
    temp_dir = "temp_test_smart_filter_pytest"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)

    db_path = os.path.join(temp_dir, "smart_filters.db")
    yield db_path

    # Cleanup
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

@pytest_asyncio.fixture
async def smart_filter_manager(temp_db_path):
    """Initialize SmartFilterManager with a temporary database."""
    manager = SmartFilterManager(db_path=temp_db_path)
    await manager._ensure_initialized()
    yield manager
    await manager.cleanup()

@pytest.mark.asyncio
async def test_apply_filters_to_email_batch_update(smart_filter_manager):
    """Test that multiple matching filters are updated correctly in a batch."""

    # Create 3 matching filters
    filter_ids = []
    for i in range(3):
        f = await smart_filter_manager.add_custom_filter(
            name=f"Filter {i}",
            description="Test filter",
            criteria={"subject_keywords": ["test"]},
            actions={"add_label": f"Label_{i}"},
            priority=5
        )
        filter_ids.append(f.filter_id)

    email_data = {
        "id": 1,
        "subject": "This is a test email",
        "sender": "sender@example.com",
        "content": "Content"
    }

    # Verify initial usage count
    for fid in filter_ids:
        f = await smart_filter_manager.get_filter_by_id(fid)
        assert f.usage_count == 0

    # Apply filters
    summary = await smart_filter_manager.apply_filters_to_email(email_data)

    assert len(summary["filters_matched"]) == 3

    # Verify usage counts incremented
    active_filters = await smart_filter_manager.get_active_filters_sorted()
    for f in active_filters:
        if f.filter_id in filter_ids:
            assert f.usage_count == 1

@pytest.mark.asyncio
async def test_regex_keyword_extraction(smart_filter_manager):
    """Test the optimized regex keyword extraction."""
    text = "The quick brown fox jumps over the lazy dog."
    # Words >= 4 chars: quick, brown, jumps, over, lazy

    keywords = smart_filter_manager._extract_keywords(text)
    expected = ["quick", "brown", "jumps", "over", "lazy"]

    # Check that all expected keywords are present
    for kw in expected:
        assert kw in keywords

    # Check that short words are excluded
    assert "the" not in keywords
    assert "fox" not in keywords
    assert "dog" not in keywords

@pytest.mark.asyncio
async def test_regex_keyword_extraction_edge_cases(smart_filter_manager):
    """Test edge cases for keyword extraction."""
    # Empty string
    assert smart_filter_manager._extract_keywords("") == []

    # String with only short words
    assert smart_filter_manager._extract_keywords("a an the fox cat dog") == []

    # String with special characters
    assert "test" in smart_filter_manager._extract_keywords("test!")
    assert "test" in smart_filter_manager._extract_keywords("(test)")

    # Mixed case (should return lowercase as per implementation)
    keywords = smart_filter_manager._extract_keywords("TEST Case")
    assert "test" in keywords
    assert "case" in keywords
