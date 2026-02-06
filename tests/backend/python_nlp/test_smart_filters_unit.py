import os
import shutil
import pytest
import time
import uuid
from unittest.mock import patch
from src.backend.python_nlp.smart_filters import SmartFilterManager, EmailFilter
from datetime import datetime

# Use a temporary directory for tests
TEST_DATA_DIR = "tests/test_data_filters"

@pytest.fixture
def filter_manager():
    # Make sure TEST_DATA_DIR is absolute for safety
    abs_test_dir = os.path.abspath(TEST_DATA_DIR)

    if not os.path.exists(abs_test_dir):
        os.makedirs(abs_test_dir)

    db_filename = f"test_filters_{uuid.uuid4()}.db"
    db_path = os.path.join(abs_test_dir, db_filename)

    # Patch DATA_DIR in the module so PathValidator allows our test path
    with patch("src.backend.python_nlp.smart_filters.DATA_DIR", abs_test_dir):
        manager = SmartFilterManager(db_path=db_path)
        yield manager
        manager.close()

    if os.path.exists(db_path):
        os.remove(db_path)

# Clean up directory at the end of session (optional, or rely on OS temp)
@pytest.fixture(scope="session", autouse=True)
def cleanup_test_dir():
    yield
    if os.path.exists(TEST_DATA_DIR):
        shutil.rmtree(TEST_DATA_DIR)

def test_add_filter_caching(filter_manager):
    # Add a filter
    filter_manager.add_custom_filter(
        name="Test Filter",
        description="Test",
        criteria={"subject_keywords": ["test"]},
        actions={"mark_read": True},
        priority=1
    )

    # Get filters - should populate cache
    filters1 = filter_manager.get_active_filters_sorted()
    assert len(filters1) == 1
    assert filters1[0].name == "Test Filter"

    # Check that cache is set
    assert filter_manager._active_filters_cache is not None

    # Modify DB directly to simulate external change (cache should hide it)
    conn = filter_manager._get_db_connection()
    conn.execute("UPDATE email_filters SET name = 'Modified Name' WHERE name = 'Test Filter'")
    conn.commit()
    conn.close()

    # Get filters again - should be cached (original name)
    filters2 = filter_manager.get_active_filters_sorted()
    assert filters2[0].name == "Test Filter"

    # Invalidate cache manually
    filter_manager._active_filters_cache = None

    # Get filters - should be fresh
    filters3 = filter_manager.get_active_filters_sorted()
    assert filters3[0].name == "Modified Name"

def test_regex_compilation(filter_manager):
    filter_manager.add_custom_filter(
        name="Regex Filter",
        description="Test Regex",
        criteria={"from_patterns": ["^noreply.*", ".*@spam.com"]},
        actions={"mark_read": True},
        priority=1
    )

    filters = filter_manager.get_active_filters_sorted()
    assert len(filters) == 1
    f = filters[0]

    # Check if patterns are compiled
    assert hasattr(f, "_compiled_patterns")
    assert "from_patterns" in f._compiled_patterns
    assert len(f._compiled_patterns["from_patterns"]) == 2
    assert f._compiled_patterns["from_patterns"][0].pattern == "^noreply.*"

def test_apply_filter_with_compiled_regex(filter_manager):
    filter_manager.add_custom_filter(
        name="Regex Filter",
        description="Test Regex",
        criteria={"from_patterns": ["^noreply.*"]},
        actions={"mark_read": True},
        priority=1
    )

    # Force load (and compile)
    filter_manager.get_active_filters_sorted()

    email_match = {"senderEmail": "noreply@example.com", "subject": "Hello"}
    email_no_match = {"senderEmail": "user@example.com", "subject": "Hello"}

    res_match = filter_manager.apply_filters_to_email_data(email_match)
    assert "Regex Filter" in res_match["filters_matched"]

    res_no_match = filter_manager.apply_filters_to_email_data(email_no_match)
    assert "Regex Filter" not in res_no_match["filters_matched"]
