"""
Data loading functionality for Email Intelligence Platform Database
"""

import asyncio
import gzip
import json
import logging
import os
from functools import partial
from typing import Any, Dict, List, Literal

from .constants import (
    DATA_TYPE_CATEGORIES,
    DATA_TYPE_EMAILS,
    DATA_TYPE_USERS,
    EMAILS_FILE,
    CATEGORIES_FILE,
    USERS_FILE
)
from ..performance_monitor import log_performance

logger = logging.getLogger(__name__)


class DataLoader:
    """Handles loading and saving data to/from files."""

    def __init__(self):
        self.emails_file = EMAILS_FILE
        self.categories_file = CATEGORIES_FILE
        self.users_file = USERS_FILE

    @log_performance("load_data")
    async def load_data(self, data_type: Literal["emails", "categories", "users"]) -> List[Dict[str, Any]]:
        """Load data from file for the specified data type."""
        file_path = self._get_file_path(data_type)
        
        try:
            if os.path.exists(file_path):
                with gzip.open(file_path, "rt", encoding="utf-8") as f:
                    data = await asyncio.to_thread(json.load, f)
                logger.info(f"Loaded {len(data)} items from compressed file: {file_path}")
                return data
            else:
                logger.info(f"Data file {file_path} does not exist. Will create empty file.")
                await self._create_empty_file(data_type)
                return []
        except (IOError, json.JSONDecodeError) as e:
            logger.error(
                f"Error loading data from {file_path}: {e}. Initializing with empty list."
            )
            return []

    async def _create_empty_file(self, data_type: Literal["emails", "categories", "users"]) -> None:
        """Create an empty data file for the specified data type."""
        file_path = self._get_file_path(data_type)
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Create empty file
            with gzip.open(file_path, "wt", encoding="utf-8") as f:
                dump_func = partial(json.dump, [], f, indent=4)
                await asyncio.to_thread(dump_func)
            logger.info(f"Created empty data file: {file_path}")
        except IOError as e:
            logger.error(f"Error creating empty data file {file_path}: {e}")

    @log_performance(operation="save_data_to_file")
    async def save_data_to_file(self, data_type: Literal["emails", "categories", "users"], 
                               data_to_save: List[Dict[str, Any]], 
                               category_counts: Dict[int, int] = None) -> None:
        """Save data to file for the specified data type."""
        file_path = self._get_file_path(data_type)
        
        # For categories, update counts before saving
        if data_type == DATA_TYPE_CATEGORIES and category_counts:
            for cat in data_to_save:
                if cat["id"] in category_counts:
                    cat["count"] = category_counts[cat["id"]]

        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with gzip.open(file_path, "wt", encoding="utf-8") as f:
                dump_func = partial(json.dump, data_to_save, f, indent=4)
                await asyncio.to_thread(dump_func)
            logger.info(f"Persisted {len(data_to_save)} items to compressed file: {file_path}")
        except IOError as e:
            logger.error(f"Error saving data to {file_path}: {e}")

    def _get_file_path(self, data_type: Literal["emails", "categories", "users"]) -> str:
        """Get the file path for the specified data type."""
        if data_type == DATA_TYPE_EMAILS:
            return self.emails_file
        elif data_type == DATA_TYPE_CATEGORIES:
            return self.categories_file
        elif data_type == DATA_TYPE_USERS:
            return self.users_file
        else:
            raise ValueError(f"Unknown data type: {data_type}")