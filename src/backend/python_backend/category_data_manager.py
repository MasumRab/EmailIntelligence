"""
DEPRECATED: This module is part of the deprecated `backend` package.
It will be removed in a future release.

Category-specific data management functionality
"""

import asyncio
import gzip
import json
import logging
import os
from datetime import datetime, timezone
from functools import partial
from pathlib import Path
from typing import Any, Dict, List, Optional

from .constants import DEFAULT_CATEGORIES, DEFAULT_CATEGORY_COLOR

# File paths - now configurable via environment variable
DATA_DIR = Path(os.getenv("DATA_DIR", "./data"))
CATEGORIES_FILE = DATA_DIR / "categories.json.gz"

# Data types
DATA_TYPE_CATEGORIES = "categories"

# Field names
FIELD_ID = "id"
FIELD_NAME = "name"
FIELD_COUNT = "count"
FIELD_COLOR = "color"


class CategoryDataManager:
    """Manages category-specific data operations"""

    def __init__(self, categories_file=CATEGORIES_FILE):
        self.categories_file = categories_file

        # In-memory data stores
        self.categories_data: List[Dict[str, Any]] = []

        # In-memory indexes
        self.categories_by_id: Dict[int, Dict[str, Any]] = {}
        self.categories_by_name: Dict[str, Dict[str, Any]] = {}
        self.category_counts: Dict[int, int] = {}

        # State
        self._dirty_data: set[str] = set()

    def _build_indexes(self) -> None:
        """Builds or rebuilds category indexes from the loaded data."""
        logger = logging.getLogger(__name__)
        logger.info("Building category indexes...")
        self.categories_by_id = {cat[FIELD_ID]: cat for cat in self.categories_data}
        self.categories_by_name = {cat[FIELD_NAME].lower(): cat for cat in self.categories_data}
        self.category_counts = {cat_id: 0 for cat_id in self.categories_by_id}
        logger.info("Category indexes built successfully.")

    async def get_all_categories(self) -> List[Dict[str, Any]]:
        """Get all categories with their counts from cache."""
        for cat_id, count in self.category_counts.items():
            if cat_id in self.categories_by_id:
                self.categories_by_id[cat_id][FIELD_COUNT] = count
        return sorted(self.categories_by_id.values(), key=lambda c: c.get(FIELD_NAME, ""))

    async def create_category(self, category_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new category and update indexes."""
        logger = logging.getLogger(__name__)

        category_name_lower = category_data.get(FIELD_NAME, "").lower()
        if category_name_lower in self.categories_by_name:
            logger.warning(
                f"Category with name '{category_data.get(FIELD_NAME)}' already exists. Returning existing."
            )
            return self.categories_by_name[category_name_lower]

        new_id = self._generate_id(self.categories_data)
        category_record = {
            FIELD_ID: new_id,
            FIELD_NAME: category_data[FIELD_NAME],
            "description": category_data.get("description"),
            FIELD_COLOR: category_data.get(FIELD_COLOR, DEFAULT_CATEGORY_COLOR),
            FIELD_COUNT: 0,
        }
        self.categories_data.append(category_record)
        self.categories_by_id[new_id] = category_record
        self.categories_by_name[category_name_lower] = category_record
        self.category_counts[new_id] = 0
        await self._save_data(DATA_TYPE_CATEGORIES)
        return category_record

    async def _update_category_count(
        self, category_id: int, increment: bool = False, decrement: bool = False
    ) -> None:
        """Incrementally update category email count in the cache."""
        logger = logging.getLogger(__name__)

        if category_id not in self.category_counts:
            logger.warning(f"Attempted to update count for non-existent category ID: {category_id}")
            return
        if increment:
            self.category_counts[category_id] += 1
        if decrement:
            self.category_counts[category_id] -= 1
        self._dirty_data.add(DATA_TYPE_CATEGORIES)

    def _generate_id(self, data_list: List[Dict[str, Any]]) -> int:
        """Generates a new unique integer ID."""
        if not data_list:
            return 1
        return max(item.get(FIELD_ID, 0) for item in data_list) + 1

    async def _save_data(self, data_type: str) -> None:
        """Marks data as dirty for write-behind saving."""
        self._dirty_data.add(data_type)
