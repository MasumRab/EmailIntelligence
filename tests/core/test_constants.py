"""
Tests for src/core/constants.py
"""

import pytest
from src.core.constants import (
    DEFAULT_CATEGORY_COLOR,
    DEFAULT_CATEGORIES,
)


class TestConstants:
    """Tests for core constants."""

    def test_default_category_color_is_valid_hex(self):
        """Test that default category color is a valid hex color."""
        # Hex color should start with # and have 7 characters
        assert DEFAULT_CATEGORY_COLOR.startswith("#")
        assert len(DEFAULT_CATEGORY_COLOR) == 7

    def test_default_categories_is_list(self):
        """Test that default categories is a list."""
        assert isinstance(DEFAULT_CATEGORIES, list)
        assert len(DEFAULT_CATEGORIES) > 0

    def test_default_categories_have_required_fields(self):
        """Test that each category has required fields."""
        required_fields = ["name", "description", "color", "count"]
        
        for category in DEFAULT_CATEGORIES:
            for field in required_fields:
                assert field in category, f"Category missing field: {field}"

    def test_default_categories_have_valid_hex_colors(self):
        """Test that all category colors are valid hex colors."""
        for category in DEFAULT_CATEGORIES:
            color = category.get("color", "")
            assert color.startswith("#"), f"Invalid color format: {color}"
            assert len(color) == 7, f"Invalid color length: {color}"

    def test_default_categories_count_starts_at_zero(self):
        """Test that all default categories start with count 0."""
        for category in DEFAULT_CATEGORIES:
            assert category.get("count") == 0

    def test_default_categories_are_unique(self):
        """Test that category names are unique."""
        names = [cat["name"] for cat in DEFAULT_CATEGORIES]
        assert len(names) == len(set(names)), "Duplicate category names found"