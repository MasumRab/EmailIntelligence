"""
Unit tests for the constants module.
"""

import os
import pytest

# Import the constants module
from src.core.constants import (
    DATA_DIR,
    FIELD_NAME,
    FIELD_COLOR,
    FIELD_COUNT,
    DEFAULT_CATEGORY_COLOR,
    DEFAULT_CATEGORIES,
)


class TestConstants:
    """Test the constants module."""

    def test_data_dir_is_defined(self):
        """Test that DATA_DIR is defined."""
        assert DATA_DIR is not None
        assert isinstance(DATA_DIR, str)
        assert len(DATA_DIR) > 0

    def test_data_dir_default_value(self):
        """Test that DATA_DIR defaults to 'data' when env var not set."""
        # DATA_DIR should have been set at import time
        # Test the default value logic
        assert DATA_DIR == os.environ.get("DATA_DIR", "data")

    def test_data_dir_env_override(self):
        """Test that DATA_DIR can be overridden via environment variable."""
        # Store original value
        original = os.environ.get("DATA_DIR")
        
        try:
            # Set custom value
            os.environ["DATA_DIR"] = "/custom/path"
            # Reimport to get new value
            import importlib
            import src.core.constants as const_module
            importlib.reload(const_module)
            
            assert const_module.DATA_DIR == "/custom/path"
        finally:
            # Restore original
            if original is None:
                del os.environ["DATA_DIR"]
            else:
                os.environ["DATA_DIR"] = original
            
            # Reload again
            importlib.reload(const_module)


class TestFieldConstants:
    """Test field name constants."""

    def test_field_name_constant(self):
        """Test FIELD_NAME constant."""
        assert FIELD_NAME == "name"
        assert isinstance(FIELD_NAME, str)

    def test_field_color_constant(self):
        """Test FIELD_COLOR constant."""
        assert FIELD_COLOR == "color"
        assert isinstance(FIELD_COLOR, str)

    def test_field_count_constant(self):
        """Test FIELD_COUNT constant."""
        assert FIELD_COUNT == "count"
        assert isinstance(FIELD_COUNT, str)

    def test_field_constants_are_unique(self):
        """Test that field constants are unique."""
        constants = [FIELD_NAME, FIELD_COLOR, FIELD_COUNT]
        assert len(constants) == len(set(constants))


class TestDefaultCategoryColor:
    """Test default category color constant."""

    def test_default_category_color_is_hex(self):
        """Test that DEFAULT_CATEGORY_COLOR is a valid hex color."""
        assert DEFAULT_CATEGORY_COLOR.startswith("#")
        assert len(DEFAULT_CATEGORY_COLOR) == 7
        
        # Verify it's a valid hex
        hex_part = DEFAULT_CATEGORY_COLOR[1:]
        assert all(c in "0123456789ABCDEF" for c in hex_part.upper())

    def test_default_category_color_format(self):
        """Test DEFAULT_CATEGORY_COLOR is in expected format."""
        import re
        assert re.match(r"^#[0-9A-Fa-f]{6}$", DEFAULT_CATEGORY_COLOR)


class TestDefaultCategories:
    """Test default categories list."""

    def test_default_categories_is_list(self):
        """Test that DEFAULT_CATEGORIES is a list."""
        assert isinstance(DEFAULT_CATEGORIES, list)
        assert len(DEFAULT_CATEGORIES) > 0

    def test_default_categories_count(self):
        """Test that we have expected number of default categories."""
        assert len(DEFAULT_CATEGORIES) == 5

    def test_each_category_has_required_fields(self):
        """Test that each category has all required fields."""
        required_fields = [FIELD_NAME, FIELD_COLOR, FIELD_COUNT]
        
        for i, category in enumerate(DEFAULT_CATEGORIES):
            for field in required_fields:
                assert field in category, f"Category {i} missing field: {field}"

    def test_each_category_has_description(self):
        """Test that each category has a description."""
        for i, category in enumerate(DEFAULT_CATEGORIES):
            assert "description" in category, f"Category {i} missing description"
            assert isinstance(category["description"], str)

    def test_category_names_are_unique(self):
        """Test that category names are unique."""
        names = [cat[FIELD_NAME] for cat in DEFAULT_CATEGORIES]
        assert len(names) == len(set(names)), "Category names must be unique"

    def test_category_colors_are_valid_hex(self):
        """Test that all category colors are valid hex."""
        import re
        for i, category in enumerate(DEFAULT_CATEGORIES):
            color = category[FIELD_COLOR]
            assert re.match(r"^#[0-9A-Fa-f]{6}$", color), f"Category {i} has invalid color: {color}"

    def test_category_counts_are_zero(self):
        """Test that default categories start with count of 0."""
        for i, category in enumerate(DEFAULT_CATEGORIES):
            assert category[FIELD_COUNT] == 0, f"Category {i} should have count 0"

    def test_standard_category_names(self):
        """Test expected standard category names exist."""
        expected_names = ["Primary", "Social", "Promotions", "Updates", "Forums"]
        actual_names = [cat[FIELD_NAME] for cat in DEFAULT_CATEGORIES]
        assert set(expected_names) == set(actual_names)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])