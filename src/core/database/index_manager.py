"""
Indexing functionality for Email Intelligence Platform Database
"""

import logging
from typing import Any, Dict, List

from .constants import (
    FIELD_ID,
    FIELD_MESSAGE_ID,
    FIELD_CATEGORY_ID,
    FIELD_NAME,
    FIELD_COUNT
)
from ..performance_monitor import log_performance

logger = logging.getLogger(__name__)


class IndexManager:
    """Manages in-memory indexes for fast data access."""

    def __init__(self):
        # In-memory indexes
        self.emails_by_id: Dict[int, Dict[str, Any]] = {}
        self.emails_by_message_id: Dict[str, Dict[str, Any]] = {}
        self.categories_by_id: Dict[int, Dict[str, Any]] = {}
        self.categories_by_name: Dict[str, Dict[str, Any]] = {}
        self.category_counts: Dict[int, int] = {}

    @log_performance(operation="build_indexes")
    def build_indexes(self, emails_data: List[Dict[str, Any]], 
                     categories_data: List[Dict[str, Any]]) -> None:
        """Build in-memory indexes from data."""
        logger.info("Building in-memory indexes...")
        
        # Build email indexes
        self.emails_by_id = {email[FIELD_ID]: email for email in emails_data}
        self.emails_by_message_id = {
            email[FIELD_MESSAGE_ID]: email
            for email in emails_data
            if FIELD_MESSAGE_ID in email
        }
        
        # Build category indexes
        self.categories_by_id = {cat[FIELD_ID]: cat for cat in categories_data}
        self.categories_by_name = {cat[FIELD_NAME].lower(): cat for cat in categories_data}
        self.category_counts = {cat_id: 0 for cat_id in self.categories_by_id}
        
        # Count emails per category
        for email in emails_data:
            cat_id = email.get(FIELD_CATEGORY_ID)
            if cat_id in self.category_counts:
                self.category_counts[cat_id] += 1
        
        # Update category counts in category data
        for cat_id, count in self.category_counts.items():
            if (
                cat_id in self.categories_by_id
                and self.categories_by_id[cat_id].get(FIELD_COUNT) != count
            ):
                self.categories_by_id[cat_id][FIELD_COUNT] = count
                
        logger.info("In-memory indexes built successfully.")

    def get_email_by_id(self, email_id: int) -> Dict[str, Any]:
        """Get email by ID using in-memory index."""
        return self.emails_by_id.get(email_id)

    def get_email_by_message_id(self, message_id: str) -> Dict[str, Any]:
        """Get email by message ID using in-memory index."""
        return self.emails_by_message_id.get(message_id)

    def get_category_by_id(self, category_id: int) -> Dict[str, Any]:
        """Get category by ID using in-memory index."""
        return self.categories_by_id.get(category_id)

    def get_category_by_name(self, category_name: str) -> Dict[str, Any]:
        """Get category by name using in-memory index."""
        return self.categories_by_name.get(category_name.lower())

    def get_category_count(self, category_id: int) -> int:
        """Get the count of emails in a category."""
        return self.category_counts.get(category_id, 0)

    def update_category_count(self, category_id: int, increment: bool = False, 
                             decrement: bool = False) -> None:
        """Incrementally update category email count in the cache."""
        if category_id not in self.category_counts:
            logger.warning(f"Attempted to update count for non-existent category ID: {category_id}")
            return
        if increment:
            self.category_counts[category_id] += 1
        if decrement:
            self.category_counts[category_id] -= 1

    def add_email_index(self, email: Dict[str, Any]) -> None:
        """Add email to indexes."""
        email_id = email.get(FIELD_ID)
        if email_id:
            self.emails_by_id[email_id] = email
            
        message_id = email.get(FIELD_MESSAGE_ID)
        if message_id:
            self.emails_by_message_id[message_id] = email

    def remove_email_index(self, email_id: int, message_id: str = None) -> None:
        """Remove email from indexes."""
        if email_id in self.emails_by_id:
            del self.emails_by_id[email_id]
            
        if message_id and message_id in self.emails_by_message_id:
            del self.emails_by_message_id[message_id]

    def add_category_index(self, category: Dict[str, Any]) -> None:
        """Add category to indexes."""
        category_id = category.get(FIELD_ID)
        if category_id:
            self.categories_by_id[category_id] = category
            
        category_name = category.get(FIELD_NAME)
        if category_name:
            self.categories_by_name[category_name.lower()] = category
            self.category_counts[category_id] = 0

    def remove_category_index(self, category_id: int, category_name: str = None) -> None:
        """Remove category from indexes."""
        if category_id in self.categories_by_id:
            del self.categories_by_id[category_id]
            
        if category_name and category_name.lower() in self.categories_by_name:
            del self.categories_by_name[category_name.lower()]
            
        if category_id in self.category_counts:
            del self.category_counts[category_id]