"""
Email-specific data management functionality extracted from DatabaseManager
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

from .constants import DEFAULT_CATEGORY_COLOR
from .performance_monitor import log_performance

# File paths - now configurable via environment variable
DATA_DIR = Path(os.getenv("DATA_DIR", "./data"))
EMAIL_CONTENT_DIR = DATA_DIR / "email_content"
EMAILS_FILE = DATA_DIR / "emails.json.gz"

# Data types
DATA_TYPE_EMAILS = 'emails'

# Field names
FIELD_ID = 'id'
FIELD_MESSAGE_ID = 'message_id'
FIELD_CATEGORY_ID = 'category_id'
FIELD_IS_UNREAD = 'is_unread'
FIELD_ANALYSIS_METADATA = 'analysis_metadata'
FIELD_CREATED_AT = 'created_at'
FIELD_UPDATED_AT = 'updated_at'
FIELD_CONTENT = 'content'
FIELD_SUBJECT = 'subject'
FIELD_SENDER = 'sender'
FIELD_SENDER_EMAIL = 'sender_email'
HEAVY_EMAIL_FIELDS = [FIELD_CONTENT, 'content_html']


class EmailDataManager:
    """Manages email-specific data operations"""
    
    def __init__(self, emails_file=EMAILS_FILE, email_content_dir=EMAIL_CONTENT_DIR):
        self.emails_file = emails_file
        self.email_content_dir = email_content_dir

        # In-memory data stores
        self.emails_data: List[Dict[str, Any]] = []  # Stores light email records

        # In-memory indexes
        self.emails_by_id: Dict[int, Dict[str, Any]] = {}
        self.emails_by_message_id: Dict[str, Dict[str, Any]] = {}

        # Ensure directories exist
        if not os.path.exists(self.email_content_dir):
            os.makedirs(self.email_content_dir)
            logging.getLogger(__name__).info(f"Created email content directory: {self.email_content_dir}")

    def _get_email_content_path(self, email_id: int) -> str:
        """Returns the path for an individual email's content file."""
        return os.path.join(self.email_content_dir, f"{email_id}.json.gz")

    async def _load_and_merge_content(self, email_light: Dict[str, Any]) -> Dict[str, Any]:
        """Loads heavy content for a given light email record and merges them."""
        full_email = email_light.copy()
        email_id = full_email.get(FIELD_ID)
        if not email_id:
            return full_email

        content_path = self._get_email_content_path(email_id)
        if os.path.exists(content_path):
            try:
                with gzip.open(content_path, 'rt', encoding='utf-8') as f:
                    heavy_data = await asyncio.to_thread(json.load, f)
                    full_email.update(heavy_data)
            except (IOError, json.JSONDecodeError) as e:
                logger = logging.getLogger(__name__)
                logger.error(f"Error loading content for email {email_id}: {e}")
        return full_email

    def _build_indexes(self) -> None:
        """Builds or rebuilds email indexes from the loaded data."""
        logger = logging.getLogger(__name__)
        logger.info("Building email indexes...")
        self.emails_by_id = {email[FIELD_ID]: email for email in self.emails_data}
        self.emails_by_message_id = {email[FIELD_MESSAGE_ID]: email for email in self.emails_data if FIELD_MESSAGE_ID in email}
        logger.info("Email indexes built successfully.")

    async def create_email(self, email_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new email record, separating heavy and light content."""
        logger = logging.getLogger(__name__)
        
        message_id = email_data.get(FIELD_MESSAGE_ID, email_data.get("messageId"))
        # We'll skip the update check for this simplified version
        # It would require a reference to the full database instance

        new_id = self._generate_id(self.emails_data)
        now = datetime.now(timezone.utc).isoformat()

        analysis_metadata = email_data.get(FIELD_ANALYSIS_METADATA, email_data.get("analysisMetadata", {}))
        if isinstance(analysis_metadata, str):
            try:
                analysis_metadata = json.loads(analysis_metadata)
            except json.JSONDecodeError:
                analysis_metadata = {}

        full_email_record = email_data.copy()
        full_email_record.update({
            FIELD_ID: new_id,
            FIELD_MESSAGE_ID: message_id,
            FIELD_CREATED_AT: now,
            FIELD_UPDATED_AT: now,
            FIELD_ANALYSIS_METADATA: analysis_metadata,
        })

        heavy_data = {
            field: full_email_record.pop(field)
            for field in HEAVY_EMAIL_FIELDS
            if field in full_email_record
        }
        light_email_record = full_email_record

        self.emails_data.append(light_email_record)
        self.emails_by_id[new_id] = light_email_record
        if message_id:
            self.emails_by_message_id[message_id] = light_email_record

        content_path = self._get_email_content_path(new_id)
        try:
            with gzip.open(content_path, 'wt', encoding='utf-8') as f:
                dump_func = partial(json.dump, heavy_data, f, indent=4)
                await asyncio.to_thread(dump_func)
        except IOError as e:
            logger.error(f"Error saving heavy content for email {new_id}: {e}")

        # For this simplified version, we'll return without category details
        # since categories are managed separately
        return light_email_record

    async def get_email_by_id(self, email_id: int, include_content: bool = True) -> Optional[Dict[str, Any]]:
        """Get email by ID using in-memory index, with option to load heavy content."""
        email_light = self.emails_by_id.get(email_id)
        if not email_light:
            return None

        if include_content:
            email_full = await self._load_and_merge_content(email_light)
            return email_full
        else:
            return email_light.copy()

    async def get_emails(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """Get emails with pagination."""
        try:
            sorted_emails = sorted(self.emails_data, key=lambda e: e.get('time', e.get(FIELD_CREATED_AT, '')), reverse=True)
        except TypeError:
            logger = logging.getLogger(__name__)
            logger.warning("Sorting emails failed due to incomparable types.")
            sorted_emails = sorted(self.emails_data, key=lambda e: e.get(FIELD_CREATED_AT, ''), reverse=True)
        paginated_emails = sorted_emails[offset : offset + limit]
        return paginated_emails

    async def get_email_by_message_id(self, message_id: str, include_content: bool = True) -> Optional[Dict[str, Any]]:
        """Get email by messageId using in-memory index, with option to load heavy content."""
        if not message_id:
            return None
        email_light = self.emails_by_message_id.get(message_id)
        if not email_light:
            return None
        if include_content:
            email_full = await self._load_and_merge_content(email_light)
            return email_full
        else:
            return email_light.copy()

    async def get_all_emails(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """Get all emails with pagination"""
        return await self.get_emails(limit=limit, offset=offset)

    @log_performance("search_emails")
    async def search_emails(self, search_term: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Search emails. Searches subject/sender in-memory, and content on-disk."""
        if not search_term:
            return await self.get_emails(limit=limit, offset=0)
        search_term_lower = search_term.lower()
        filtered_emails = []
        logger = logging.getLogger(__name__)
        
        logger.info(f"Starting email search for term: '{search_term_lower}'. This may be slow if searching content.")
        for email_light in self.emails_data:
            found_in_light = (
                search_term_lower in email_light.get(FIELD_SUBJECT, '').lower() or
                search_term_lower in email_light.get(FIELD_SENDER, '').lower() or
                search_term_lower in email_light.get(FIELD_SENDER_EMAIL, '').lower()
            )
            if found_in_light:
                filtered_emails.append(email_light)
                continue
            email_id = email_light.get(FIELD_ID)
            content_path = self._get_email_content_path(email_id)
            if os.path.exists(content_path):
                try:
                    with gzip.open(content_path, 'rt', encoding='utf-8') as f:
                        heavy_data = json.load(f)
                        content = heavy_data.get(FIELD_CONTENT, '')
                        if isinstance(content, str) and search_term_lower in content.lower():
                            filtered_emails.append(email_light)
                except (IOError, json.JSONDecodeError) as e:
                    logger.error(f"Could not search content for email {email_id}: {e}")
        try:
            sorted_emails = sorted(filtered_emails, key=lambda e: e.get('time', e.get(FIELD_CREATED_AT, '')), reverse=True)
        except TypeError:
            logger.warning("Sorting search results failed. Using created_at.")
            sorted_emails = sorted(filtered_emails, key=lambda e: e.get(FIELD_CREATED_AT, ''), reverse=True)
        paginated_emails = sorted_emails[:limit]
        return paginated_emails

    def _generate_id(self, data_list: List[Dict[str, Any]]) -> int:
        """Generates a new unique integer ID."""
        if not data_list:
            return 1
        return max(item.get(FIELD_ID, 0) for item in data_list) + 1