"""Tests for core constants module."""

import pytest  # noqa: F401
from src.core.constants import DEFAULT_CATEGORY_COLOR, DEFAULT_CATEGORIES


class TestConstants:
    """Test constants module."""

    def test_default_category_color(self):
        """Test default category color is a valid hex color."""
        assert DEFAULT_CATEGORY_COLOR == "#6366f1"
        assert DEFAULT_CATEGORY_COLOR.startswith("#")
        assert len(DEFAULT_CATEGORY_COLOR) == 7

    def test_default_categories_is_list(self):
        """Test DEFAULT_CATEGORIES is a list."""
        assert isinstance(DEFAULT_CATEGORIES, list)
        assert len(DEFAULT_CATEGORIES) > 0

    def test_default_categories_count(self):
        """Test there are 5 default categories."""
        assert len(DEFAULT_CATEGORIES) == 5

    def test_category_structure(self):
        """Test each category has required fields."""
        for category in DEFAULT_CATEGORIES:
            assert "name" in category
            assert "description" in category
            assert "color" in category
            assert "count" in category

    def test_category_names(self):
        """Test category names are correct."""
        names = [cat["name"] for cat in DEFAULT_CATEGORIES]
        assert "Primary" in names
        assert "Promotions" in names
        assert "Social" in names
        assert "Updates" in names
        assert "Forums" in names

    def test_category_colors_are_hex(self):
        """Test all category colors are valid hex colors."""
        for category in DEFAULT_CATEGORIES:
            color = category["color"]
            assert color.startswith("#")
            assert len(color) == 7

    def test_category_counts_are_zero(self):
        """Test all default category counts start at zero."""
        for category in DEFAULT_CATEGORIES:
            assert category["count"] == 0