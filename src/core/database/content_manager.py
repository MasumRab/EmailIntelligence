"""
Content management functionality for Email Intelligence Platform Database
"""

import asyncio
import gzip
import json
import logging
import os
from functools import partial
from pathlib import Path
from typing import Any, Dict

from .constants import FIELD_ID, FIELD_CONTENT, HEAVY_EMAIL_FIELDS
from ..performance_monitor import log_performance

logger = logging.getLogger(__name__)


class ContentManager:
    """Manages heavy content loading and storage."""

    def __init__(self, email_content_dir: Path):
        self.email_content_dir = email_content_dir
        # Ensure directory exists
        if not os.path.exists(self.email_content_dir):
            os.makedirs(self.email_content_dir)
            logger.info(f"Created email content directory: {self.email_content_dir}")

    def get_email_content_path(self, email_id: int) -> str:
        """Get the file path for email content."""
        return os.path.join(self.email_content_dir, f"{email_id}.json.gz")

    async def load_and_merge_content(self, email_light: Dict[str, Any]) -> Dict[str, Any]:
        """Load heavy content and merge with light email record."""
        full_email = email_light.copy()
        email_id = full_email.get(FIELD_ID)
        if not email_id:
            return full_email

        content_path = self.get_email_content_path(email_id)
        if os.path.exists(content_path):
            try:
                with gzip.open(content_path, "rt", encoding="utf-8") as f:
                    heavy_data = await asyncio.to_thread(json.load, f)
                    full_email.update(heavy_data)
            except (IOError, json.JSONDecodeError) as e:
                logger.error(f"Error loading content for email {email_id}: {e}")
        return full_email

    async def save_email_content(self, email_id: int, email_data: Dict[str, Any]) -> bool:
        """Save heavy email content to file."""
        # Extract heavy data
        heavy_data = {
            field: email_data.pop(field)
            for field in HEAVY_EMAIL_FIELDS
            if field in email_data
        }

        if not heavy_data:
            # No heavy data to save
            return True

        content_path = self.get_email_content_path(email_id)
        try:
            with gzip.open(content_path, "wt", encoding="utf-8") as f:
                dump_func = partial(json.dump, heavy_data, f, indent=4)
                await asyncio.to_thread(dump_func)
        except IOError as e:
            logger.error(f"Error saving heavy content for email {email_id}: {e}")
            return False

        return True

    async def update_email_content(self, email_id: int, email_data: Dict[str, Any]) -> bool:
        """Update heavy email content in file."""
        return await self.save_email_content(email_id, email_data)

    def content_exists(self, email_id: int) -> bool:
        """Check if content exists for an email."""
        content_path = self.get_email_content_path(email_id)
        return os.path.exists(content_path)

    def delete_email_content(self, email_id: int) -> bool:
        """Delete content file for an email."""
        content_path = self.get_email_content_path(email_id)
        if os.path.exists(content_path):
            try:
                os.remove(content_path)
                return True
            except OSError as e:
                logger.error(f"Error deleting content for email {email_id}: {e}")
                return False
        return True  # File doesn't exist, so considered deleted