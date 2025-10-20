"""
Database management for Gmail AI email processing
JSON file storage implementation.
"""

import asyncio
import gzip
import json
import logging
import os
from datetime import datetime, timezone
from functools import partial
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

from .constants import DEFAULT_CATEGORIES, DEFAULT_CATEGORY_COLOR
from .performance_monitor import log_performance

logger = logging.getLogger(__name__)

# File paths - now configurable via environment variable
# Use a more general default that works across different deployment scenarios
DATA_DIR = Path(os.getenv("DATA_DIR", "./data"))
EMAIL_CONTENT_DIR = DATA_DIR / "email_content"
EMAILS_FILE = DATA_DIR / "emails.json.gz"
CATEGORIES_FILE = DATA_DIR / "categories.json.gz"
USERS_FILE = DATA_DIR / "users.json.gz"
SETTINGS_FILE = DATA_DIR / "settings.json"

# Data types
DATA_TYPE_EMAILS = "emails"
DATA_TYPE_CATEGORIES = "categories"
DATA_TYPE_USERS = "users"

# Field names
FIELD_ID = "id"
FIELD_MESSAGE_ID = "message_id"
FIELD_CATEGORY_ID = "category_id"
FIELD_IS_UNREAD = "is_unread"
FIELD_ANALYSIS_METADATA = "analysis_metadata"
FIELD_CREATED_AT = "created_at"
FIELD_UPDATED_AT = "updated_at"
FIELD_NAME = "name"
FIELD_COLOR = "color"
FIELD_COUNT = "count"
FIELD_TIME = "time"
FIELD_CONTENT = "content"
FIELD_SUBJECT = "subject"
FIELD_SENDER = "sender"
FIELD_SENDER_EMAIL = "sender_email"
HEAVY_EMAIL_FIELDS = [FIELD_CONTENT, "content_html"]


# UI field names
FIELD_CATEGORY_NAME = "categoryName"
FIELD_CATEGORY_COLOR = "categoryColor"


class DatabaseManager:
    """
    Optimized async database manager with in-memory caching, write-behind,
    and hybrid on-demand content loading.

    This class provides an asynchronous interface for all CRUD (Create, Read,
    Update, Delete) operations. It handles loading data from files into memory
    on initialization and saving data back to files when modifications occur.
    It is designed to be used as a singleton within the application.

    Attributes:
        emails_file (str): Path to the emails JSON file.
        categories_file (str): Path to the categories JSON file.
        users_file (str): Path to the users JSON file.
        emails_data (List[Dict[str, Any]]): In-memory cache of email records.
        categories_data (List[Dict[str, Any]]): In-memory cache of category records.
        users_data (List[Dict[str, Any]]): In-memory cache of user records.
    """

    def __init__(self):
        """Initializes the DatabaseManager, setting up file paths and data caches."""
        self.emails_file = EMAILS_FILE
        self.categories_file = CATEGORIES_FILE
        self.users_file = USERS_FILE
        self.email_content_dir = EMAIL_CONTENT_DIR

        # In-memory data stores
        self.emails_data: List[Dict[str, Any]] = []  # Stores light email records
        self.categories_data: List[Dict[str, Any]] = []
        self.users_data: List[Dict[str, Any]] = []

        # In-memory indexes
        self.emails_by_id: Dict[int, Dict[str, Any]] = {}
        self.emails_by_message_id: Dict[str, Dict[str, Any]] = {}
        self.categories_by_id: Dict[int, Dict[str, Any]] = {}
        self.categories_by_name: Dict[str, Dict[str, Any]] = {}
        self.category_counts: Dict[int, int] = {}

        # State
        self._dirty_data: set[str] = set()
        self._initialized = False

        # Ensure directories exist
        if not os.path.exists(self.email_content_dir):
            os.makedirs(self.email_content_dir)
            logger.info(f"Created email content directory: {self.email_content_dir}")

    def _get_email_content_path(self, email_id: int) -> str:
        return os.path.join(self.email_content_dir, f"{email_id}.json.gz")

    async def _load_and_merge_content(self, email_light: Dict[str, Any]) -> Dict[str, Any]:
        full_email = email_light.copy()
        email_id = full_email.get(FIELD_ID)
        if not email_id:
            return full_email

        content_path = self._get_email_content_path(email_id)
        if os.path.exists(content_path):
            try:
                with gzip.open(content_path, "rt", encoding="utf-8") as f:
                    heavy_data = await asyncio.to_thread(json.load, f)
                    full_email.update(heavy_data)
            except (IOError, json.JSONDecodeError) as e:
                logger.error(f"Error loading content for email {email_id}: {e}")
        return full_email

    async def _ensure_initialized(self) -> None:

        if not self._initialized:
            await self._load_data()
            self._build_indexes()
            self._initialized = True

    @log_performance(operation="build_indexes")
    def _build_indexes(self) -> None:
        logger.info("Building in-memory indexes...")
        self.emails_by_id = {email[FIELD_ID]: email for email in self.emails_data}
        self.emails_by_message_id = {
            email[FIELD_MESSAGE_ID]: email
            for email in self.emails_data
            if FIELD_MESSAGE_ID in email
        }
        self.categories_by_id = {cat[FIELD_ID]: cat for cat in self.categories_data}
        self.categories_by_name = {cat[FIELD_NAME].lower(): cat for cat in self.categories_data}
        self.category_counts = {cat_id: 0 for cat_id in self.categories_by_id}
        for email in self.emails_data:
            cat_id = email.get(FIELD_CATEGORY_ID)
            if cat_id in self.category_counts:
                self.category_counts[cat_id] += 1
        for cat_id, count in self.category_counts.items():
            if (
                cat_id in self.categories_by_id
                and self.categories_by_id[cat_id].get(FIELD_COUNT) != count
            ):
                self.categories_by_id[cat_id][FIELD_COUNT] = count
                self._dirty_data.add(DATA_TYPE_CATEGORIES)
        logger.info("In-memory indexes built successfully.")

    @log_performance("load_data")
    async def _load_data(self) -> None:
        for data_type, file_path, data_list_attr in [
            (DATA_TYPE_EMAILS, self.emails_file, "emails_data"),
            (DATA_TYPE_CATEGORIES, self.categories_file, "categories_data"),
            (DATA_TYPE_USERS, self.users_file, "users_data"),
        ]:
            try:
                if os.path.exists(file_path):
                    with gzip.open(file_path, "rt", encoding="utf-8") as f:
                        data = await asyncio.to_thread(json.load, f)
                        setattr(self, data_list_attr, data)
                    logger.info(f"Loaded {len(data)} items from compressed file: {file_path}")
                else:
                    setattr(self, data_list_attr, [])
                    await self._save_data_to_file(data_type)
                    logger.info(f"Created empty data file: {file_path}")
            except (IOError, json.JSONDecodeError) as e:
                logger.error(
                    f"Error loading data from {file_path}: {e}. Initializing with empty list."
                )
                setattr(self, data_list_attr, [])

    @log_performance(operation="save_data_to_file")
    async def _save_data_to_file(self, data_type: Literal["emails", "categories", "users"]) -> None:
        """Saves the specified in-memory data list to its JSON file."""
        file_path, data_to_save = "", []
        if data_type == DATA_TYPE_EMAILS:
            file_path, data_to_save = self.emails_file, self.emails_data
        elif data_type == DATA_TYPE_CATEGORIES:
            for cat in self.categories_data:
                if cat["id"] in self.category_counts:
                    cat["count"] = self.category_counts[cat["id"]]
            file_path, data_to_save = self.categories_file, self.categories_data
        elif data_type == DATA_TYPE_USERS:
            file_path, data_to_save = self.users_file, self.users_data
        else:
            logger.error(f"Unknown data type for saving: {data_type}")
            return

        try:
            with gzip.open(file_path, "wt", encoding="utf-8") as f:
                dump_func = partial(json.dump, data_to_save, f, indent=4)
                await asyncio.to_thread(dump_func)
            logger.info(f"Persisted {len(data_to_save)} items to compressed file: {file_path}")
        except IOError as e:
            logger.error(f"Error saving data to {file_path}: {e}")

    async def _save_data(self, data_type: Literal["emails", "categories", "users"]) -> None:
        """Marks data as dirty for write-behind saving."""
        self._dirty_data.add(data_type)

    async def shutdown(self) -> None:
        logger.info("DatabaseManager shutting down. Saving dirty data...")
        for data_type in list(self._dirty_data):
            await self._save_data_to_file(data_type)
        self._dirty_data.clear()
        logger.info("Shutdown complete.")

    def _generate_id(self, data_list: List[Dict[str, Any]]) -> int:
    def _generate_id(self, data_list: List[Dict[str, Any]]) -> int:
        """
        Generates a new unique integer ID for a record.

        Args:
            data_list: The list of records to scan for the current maximum ID.

        Returns:
            A new unique integer ID.
        """
        if not data_list:
            return 1
        return max(item.get(FIELD_ID, 0) for item in data_list) + 1

    def _parse_json_fields(self, row: Dict[str, Any], fields: List[str]) -> Dict[str, Any]:
    def _parse_json_fields(self, row: Dict[str, Any], fields: List[str]) -> Dict[str, Any]:
        """
        Parses fields in a data row that are stored as JSON strings.

        Args:
            row: The data record (dictionary).
            fields: A list of field names to parse.

        Returns:
            The modified data record with parsed fields.
        """
        if not row:
            return row
        for field in row:
            if field in row and isinstance(row[field], str):
                try:
                    row[field] = json.loads(row[field])
                except json.JSONDecodeError:
                    logger.warning(
                        f"Failed to parse JSON for field {field} in row {row.get(FIELD_ID)}"
                    )
                    if field in (FIELD_ANALYSIS_METADATA, "metadata"):
                        row[field] = {}
                    else:
                        row[field] = []
        return row

    def _add_category_details(self, email: Dict[str, Any]) -> Dict[str, Any]:
        if not email:
            return email
        category_id = email.get(FIELD_CATEGORY_ID)
        if category_id is not None:
            category = self.categories_by_id.get(category_id)
            if category:
                email[FIELD_CATEGORY_NAME] = category.get(FIELD_NAME)
                email[FIELD_CATEGORY_COLOR] = category.get(FIELD_COLOR)
        return self._parse_json_fields(email, [FIELD_ANALYSIS_METADATA])

    async def create_email(self, email_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        message_id = email_data.get(FIELD_MESSAGE_ID, email_data.get("messageId"))
        if await self.get_email_by_message_id(message_id, include_content=False):
            logger.warning(f"Email with messageId {message_id} already exists. Updating.")
            return await self.update_email_by_message_id(message_id, email_data)

        new_id = self._generate_id(self.emails_data)
        now = datetime.now(timezone.utc).isoformat()

        analysis_metadata = email_data.get(
            FIELD_ANALYSIS_METADATA, email_data.get("analysisMetadata", {})
        )
        if isinstance(analysis_metadata, str):
            try:
                analysis_metadata = json.loads(analysis_metadata)
            except json.JSONDecodeError:
                analysis_metadata = {}

        full_email_record = email_data.copy()
        full_email_record.update(
            {
                FIELD_ID: new_id,
                FIELD_MESSAGE_ID: message_id,
                FIELD_CREATED_AT: now,
                FIELD_UPDATED_AT: now,
                FIELD_ANALYSIS_METADATA: analysis_metadata,
            }
        )

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
        await self._save_data(DATA_TYPE_EMAILS)

        content_path = self._get_email_content_path(new_id)
        try:
            with gzip.open(content_path, "wt", encoding="utf-8") as f:
                dump_func = partial(json.dump, heavy_data, f, indent=4)
                await asyncio.to_thread(dump_func)
        except IOError as e:
            logger.error(f"Error saving heavy content for email {new_id}: {e}")

        category_id = light_email_record.get(FIELD_CATEGORY_ID)
        if category_id is not None:
            await self._update_category_count(category_id, increment=True)

        return self._add_category_details(light_email_record)

    async def get_email_by_id(
        self, email_id: int, include_content: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Get email by ID using in-memory index, with option to load heavy content."""
        email_light = self.emails_by_id.get(email_id)
        if not email_light:
            return None

        if include_content:
            email_full = await self._load_and_merge_content(email_light)
            return self._add_category_details(email_full)
        else:
            return self._add_category_details(email_light.copy())

    async def get_all_categories(self) -> List[Dict[str, Any]]:

        for cat_id, count in self.category_counts.items():
            if cat_id in self.categories_by_id:
                self.categories_by_id[cat_id][FIELD_COUNT] = count
        return sorted(self.categories_by_id.values(), key=lambda c: c.get(FIELD_NAME, ""))

    async def create_category(self, category_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new category and update indexes."""
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
        if category_id not in self.category_counts:
            logger.warning(f"Attempted to update count for non-existent category ID: {category_id}")
            return
        if increment:
            self.category_counts[category_id] += 1
        if decrement:
            self.category_counts[category_id] -= 1
        self._dirty_data.add(DATA_TYPE_CATEGORIES)

    async def get_emails(
        self,
        limit: int = 50,
        offset: int = 0,
        category_id: Optional[int] = None,
        is_unread: Optional[bool] = None,
    ) -> List[Dict[str, Any]]:
        """Get emails with pagination and filtering."""
        filtered_emails = self.emails_data
        if category_id is not None:
            filtered_emails = [
                e for e in filtered_emails if e.get(FIELD_CATEGORY_ID) == category_id
            ]
        if is_unread is not None:
            filtered_emails = [e for e in filtered_emails if e.get(FIELD_IS_UNREAD) == is_unread]
        try:
            filtered_emails = sorted(
                filtered_emails,
                key=lambda e: e.get(FIELD_TIME, e.get(FIELD_CREATED_AT, "")),
                reverse=True,
            )
        except TypeError:
            logger.warning(
                f"Sorting emails by {FIELD_TIME} failed due to incomparable types. Using '{FIELD_CREATED_AT}'."
            )
            filtered_emails = sorted(
                filtered_emails, key=lambda e: e.get(FIELD_CREATED_AT, ""), reverse=True
            )
        paginated_emails = filtered_emails[offset : offset + limit]
        result_emails = [self._add_category_details(email) for email in paginated_emails]
        logger.info(
            f"Email retrieval completed. Found {len(result_emails)} emails."
        )
        return result_emails

    async def update_email_by_message_id(
        self, message_id: str, update_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Update email by messageId, handling separated content."""
        email_to_update = await self.get_email_by_message_id(message_id, include_content=True)
        if not email_to_update:
            logger.warning(f"Email with {FIELD_MESSAGE_ID} {message_id} not found for update.")
            return None

        original_category_id = email_to_update.get(FIELD_CATEGORY_ID)
        changed_fields = False
        for key, value in update_data.items():
            if key in email_to_update and email_to_update[key] != value:
                email_to_update[key] = value
                changed_fields = True
            elif key not in email_to_update:
                email_to_update[key] = value
                changed_fields = True

        if changed_fields:
            email_to_update[FIELD_UPDATED_AT] = datetime.now(timezone.utc).isoformat()
            heavy_data = {
                field: email_to_update.pop(field)
                for field in HEAVY_EMAIL_FIELDS
                if field in email_to_update
            }
            email_id = email_to_update[FIELD_ID]
            content_path = self._get_email_content_path(email_id)
            try:
                with gzip.open(content_path, "wt", encoding="utf-8") as f:
                    dump_func = partial(json.dump, heavy_data, f, indent=4)
                    await asyncio.to_thread(dump_func)
            except IOError as e:
                logger.error(f"Error updating heavy content for email {email_id}: {e}")

            self.emails_by_id[email_id] = email_to_update
            if email_to_update.get(FIELD_MESSAGE_ID):
                self.emails_by_message_id[email_to_update[FIELD_MESSAGE_ID]] = email_to_update
            idx = next(
                (i for i, e in enumerate(self.emails_data) if e.get(FIELD_ID) == email_id), -1
            )
            if idx != -1:
                self.emails_data[idx] = email_to_update
            await self._save_data(DATA_TYPE_EMAILS)

            new_category_id = email_to_update.get(FIELD_CATEGORY_ID)
            if original_category_id != new_category_id:
                if original_category_id is not None:
                    await self._update_category_count(original_category_id, decrement=True)
                if new_category_id is not None:
                    await self._update_category_count(new_category_id, increment=True)
        return self._add_category_details(email_to_update)

    async def get_email_by_message_id(
        self, message_id: str, include_content: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Get email by messageId using in-memory index, with option to load heavy content."""
        if not message_id:
            return None
        email_light = self.emails_by_message_id.get(message_id)
        if not email_light:
            return None
        if include_content:
            email_full = await self._load_and_merge_content(email_light)
            return self._add_category_details(email_full)
        else:
            return self._add_category_details(email_light.copy())

    async def get_all_emails(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
    async def get_all_emails(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """Retrieves all emails with pagination."""
        return await self.get_emails(limit=limit, offset=offset)

    async def get_emails_by_category(
        self, category_id: int, limit: int = 50, offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Get emails by category"""
        return await self.get_emails(limit=limit, offset=offset, category_id=category_id)

    @log_performance(operation="search_emails")
    async def search_emails(self, search_term: str, limit: int = 50) -> List[Dict[str, Any]]:
        if not search_term:
            return await self.get_emails(limit=limit, offset=0)
        search_term_lower = search_term.lower()
        filtered_emails = []
        logger.info(
            f"Starting email search for term: '{search_term_lower}'. This may be slow if searching content."
        )
        for email_light in self.emails_data:
            found_in_light = (
                search_term_lower in email_light.get(FIELD_SUBJECT, "").lower()
                or search_term_lower in email_light.get(FIELD_SENDER, "").lower()
                or search_term_lower in email_light.get(FIELD_SENDER_EMAIL, "").lower()
            )
            if found_in_light:
                filtered_emails.append(email_light)
                continue
            email_id = email_light.get(FIELD_ID)
            content_path = self._get_email_content_path(email_id)
            if os.path.exists(content_path):
                try:
                    with gzip.open(content_path, "rt", encoding="utf-8") as f:
                        heavy_data = json.load(f)
                        content = heavy_data.get(FIELD_CONTENT, "")
                        if isinstance(content, str) and search_term_lower in content.lower():
                            filtered_emails.append(email_light)
                except (IOError, json.JSONDecodeError) as e:
                    logger.error(f"Could not search content for email {email_id}: {e}")
        try:
            total_emails = len(self.emails_data)
            auto_labeled = sum(1 for email in self.emails_data if email.get("category"))
            categories_count = len(self.categories_data)

            # Calculate time saved (rough estimate: 30 seconds per auto-labeled email)
            time_saved_seconds = auto_labeled * 30
            time_saved = f"{time_saved_seconds // 3600}h {(time_saved_seconds % 3600) // 60}m"

            # Weekly growth (simplified - just return current total)
            weekly_growth = {"emails": total_emails}

            return {
                "totalEmails": total_emails,
                "autoLabeled": auto_labeled,
                "categories": categories_count,
                "timeSaved": time_saved,
                "weeklyGrowth": weekly_growth,
            }
        except Exception as e:
            logger.error(f"Error calculating dashboard stats: {e}")
            return {
                "totalEmails": 0,
                "autoLabeled": 0,
                "categories": 0,
                "timeSaved": "0h 0m",
                "weeklyGrowth": {"emails": 0},
            }

    async def update_email(
        self, email_id: int, update_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Update email by its internal ID, handling separated content."""
        email_to_update = await self.get_email_by_id(email_id, include_content=True)
        if not email_to_update:
            logger.warning(f"Email with {FIELD_ID} {email_id} not found for update.")
            return None

        original_category_id = email_to_update.get(FIELD_CATEGORY_ID)
        changed_fields = False
        for key, value in update_data.items():
            if key == FIELD_ID:
                continue
            if key in email_to_update and email_to_update[key] != value:
                email_to_update[key] = value
                changed_fields = True
            elif key not in email_to_update:
                email_to_update[key] = value
                changed_fields = True

        if changed_fields:
            email_to_update[FIELD_UPDATED_AT] = datetime.now(timezone.utc).isoformat()
            heavy_data = {
                field: email_to_update.pop(field)
                for field in HEAVY_EMAIL_FIELDS
                if field in email_to_update
            }
            content_path = self._get_email_content_path(email_id)
            try:
                with gzip.open(content_path, "wt", encoding="utf-8") as f:
                    dump_func = partial(json.dump, heavy_data, f, indent=4)
                    await asyncio.to_thread(dump_func)
            except IOError as e:
                logger.error(f"Error updating heavy content for email {email_id}: {e}")

            self.emails_by_id[email_id] = email_to_update
            if email_to_update.get(FIELD_MESSAGE_ID):
                self.emails_by_message_id[email_to_update[FIELD_MESSAGE_ID]] = email_to_update
            idx = next(
                (i for i, e in enumerate(self.emails_data) if e.get(FIELD_ID) == email_id), -1
            )
            if idx != -1:
                self.emails_data[idx] = email_to_update
            await self._save_data(DATA_TYPE_EMAILS)

            new_category_id = email_to_update.get(FIELD_CATEGORY_ID)
            if original_category_id != new_category_id:
                if original_category_id is not None:
                    await self._update_category_count(original_category_id, decrement=True)
                if new_category_id is not None:
                    await self._update_category_count(new_category_id, increment=True)
        return self._add_category_details(email_to_update)


# Module-level variable to store the database manager instance
# This is initialized via FastAPI startup event
_db_manager_instance = None


async def get_db() -> DatabaseManager:
async def get_db() -> DatabaseManager:
    """
    Provides the singleton instance of the DatabaseManager.

    This function is used for dependency injection in FastAPI routes. It ensures
    that only one instance of the DatabaseManager is used throughout the

    application's lifecycle.

    Returns:
        The singleton DatabaseManager instance.
    """
    global _db_manager_instance
    if _db_manager_instance is None:
        # This should ideally not be reached if startup event is properly set
        _db_manager_instance = DatabaseManager()
        await _db_manager_instance._ensure_initialized()
    return _db_manager_instance


async def initialize_db():
    """Initialize the database manager. Should be called during application startup."""
    global _db_manager_instance
    if _db_manager_instance is None:
        _db_manager_instance = DatabaseManager()
        await _db_manager_instance._ensure_initialized()
