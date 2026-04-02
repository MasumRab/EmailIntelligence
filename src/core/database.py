"""
Database management for the Email Intelligence Platform.
JSON file storage implementation with in-memory caching and indexing.
"""

import asyncio
import gzip
import json
import logging
import os
import shutil
from datetime import datetime, timezone
from functools import partial
from typing import Any, Dict, List, Literal, Optional
import hashlib

# NOTE: These dependencies will be moved to the core framework as well.
# For now, we are assuming they will be available in the new location.
from .performance_monitor import log_performance
from .constants import DEFAULT_CATEGORY_COLOR, DEFAULT_CATEGORIES
from .data.data_source import DataSource

from .security import validate_path_safety, sanitize_path

logger = logging.getLogger(__name__)

# Globalized data directory at the project root
DATA_DIR = os.environ.get("DATA_DIR", "data")
EMAIL_CONTENT_DIR = os.path.join(DATA_DIR, "email_content")
EMAILS_FILE = os.path.join(DATA_DIR, "emails.json.gz")
CATEGORIES_FILE = os.path.join(DATA_DIR, "categories.json.gz")
USERS_FILE = os.path.join(DATA_DIR, "users.json.gz")
BACKUP_DIR = os.path.join(DATA_DIR, "backups")
SCHEMA_VERSION_FILE = os.path.join(DATA_DIR, "schema_version.json")

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(EMAIL_CONTENT_DIR, exist_ok=True)
os.makedirs(BACKUP_DIR, exist_ok=True)

# Schema version for migration tracking
CURRENT_SCHEMA_VERSION = "1.0"

# TODO(P1, 6h): Refactor global state management to use dependency injection
# Pseudo code for dependency injection:
# - Create a DatabaseConfig class to hold configuration (data_dir, file_paths, etc.)
# - Modify DatabaseManager.__init__ to accept DatabaseConfig instance
# - Update get_db() to be a factory function that takes config and returns initialized instance
# - In FastAPI app, create config from env vars and inject via Depends(get_db_factory(config))
# - Remove global _db_manager_instance and _db_init_lock
# TODO(P2, 4h): Make data directory configurable via environment variables or settings
# Pseudo code for configurable data directory:
# - Add DATA_DIR environment variable support: os.getenv('DATA_DIR', 'data')
# - Update DatabaseConfig to accept data_dir parameter
# - Modify file path construction to use config.data_dir
# - Add validation to ensure directory exists or can be created

from .security import validate_path_safety, sanitize_path


class DatabaseConfig:
    """Configuration for the DatabaseManager."""

    def __init__(
        self,
        data_dir: Optional[str] = None,
        emails_file: Optional[str] = None,
        categories_file: Optional[str] = None,
        users_file: Optional[str] = None,
        email_content_dir: Optional[str] = None,
    ):
        # Make data directory configurable via environment variable
        self.data_dir = data_dir or os.getenv("DATA_DIR", "data")

        # Validate data directory path
        if not validate_path_safety(self.data_dir):
            raise ValueError(f"Unsafe data directory path: {self.data_dir}")

        self.emails_file = emails_file or os.path.join(self.data_dir, "emails.json.gz")
        self.categories_file = categories_file or os.path.join(self.data_dir, "categories.json.gz")
        self.users_file = users_file or os.path.join(self.data_dir, "users.json.gz")
        self.email_content_dir = email_content_dir or os.path.join(self.data_dir, "email_content")

        # Validate all file paths
        for path_attr in ["emails_file", "categories_file", "users_file", "email_content_dir"]:
            path_value = getattr(self, path_attr)
            if not validate_path_safety(path_value, self.data_dir):
                raise ValueError(f"Unsafe {path_attr} path: {path_value}")

        # Ensure directories exist
        os.makedirs(self.email_content_dir, exist_ok=True)


# COMPLETED: Refactored global state management to use dependency injection
# - Created DatabaseConfig class to hold configuration
# - Modified DatabaseManager.__init__ to accept DatabaseConfig instance
# - Created create_database_manager factory function
# - Removed global _db_manager_instance and _db_init_lock (replaced with backward compatible version)

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


class DatabaseManager(DataSource):
    """Optimized async database manager with in-memory caching, write-behind,
    and hybrid on-demand content loading."""

    def __init__(self, config: DatabaseConfig = None, data_dir: Optional[str] = None):
        """Initializes the DatabaseManager, setting up file paths and data caches."""
        # Support both new config-based initialization and legacy initialization
        if config is not None:
            # New approach: Use provided DatabaseConfig
            self.config = config
            self.emails_file = config.emails_file
            self.categories_file = config.categories_file
            self.users_file = config.users_file
            self.email_content_dir = config.email_content_dir
            # Derive data_dir from config for backup and schema files if needed
            if hasattr(config, "data_dir") and config.data_dir:
                self.data_dir = config.data_dir
            else:
                # Try to derive from file paths
                self.data_dir = os.path.dirname(os.path.dirname(self.emails_file))
        else:
            # Legacy approach: Direct data directory initialization
            self.data_dir = data_dir or DATA_DIR
            self.emails_file = os.path.join(self.data_dir, "emails.json.gz")
            self.categories_file = os.path.join(self.data_dir, "categories.json.gz")
            self.users_file = os.path.join(self.data_dir, "users.json.gz")
            self.email_content_dir = os.path.join(self.data_dir, "email_content")

        # Always ensure backup and schema directories are set
        self.backup_dir = os.path.join(self.data_dir, "backups")
        self.schema_version_file = os.path.join(self.data_dir, "schema_version.json")

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

        # State tracking
        self._dirty_data: set[str] = set()
        self._initialized: bool = False
        self._init_lock = asyncio.Lock()

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

        # State tracking
        self._dirty_data: set[str] = set()
        self._initialized: bool = False
        self._init_lock = asyncio.Lock()

        # Initialize default categories if needed
        self._default_categories_initialized = False

    async def initialize(self):
        """Initialize the database by loading data from files."""
        async with self._init_lock:
            if self._initialized:
                return

            await self._load_data()
            await self._initialize_default_categories()
            self._initialized = True

    async def _load_data(self):
        """Load data from JSON files into memory."""
        # Load emails
        if os.path.exists(self.emails_file):
            try:
                with gzip.open(self.emails_file, 'rt', encoding='utf-8') as f:
                    self.emails_data = json.load(f)
                self._build_emails_indexes()
            except Exception as e:
                logger.error(f"Error loading emails: {e}")
                self.emails_data = []

        # Load categories
        if os.path.exists(self.categories_file):
            try:
                with gzip.open(self.categories_file, 'rt', encoding='utf-8') as f:
                    self.categories_data = json.load(f)
                self._build_categories_indexes()
            except Exception as e:
                logger.error(f"Error loading categories: {e}")
                self.categories_data = []
                # Initialize with default categories if file is missing/corrupted

        # Load users
        if os.path.exists(self.users_file):
            try:
                with gzip.open(self.users_file, 'rt', encoding='utf-8') as f:
                    self.users_data = json.load(f)
            except Exception as e:
                logger.error(f"Error loading users: {e}")
                self.users_data = []

    def _build_emails_indexes(self):
        """Build in-memory indexes for emails."""
        self.emails_by_id.clear()
        self.emails_by_message_id.clear()
        
        for email in self.emails_data:
            email_id = email.get(FIELD_ID)
            if email_id is not None:
                self.emails_by_id[email_id] = email
            
            message_id = email.get(FIELD_MESSAGE_ID)
            if message_id:
                self.emails_by_message_id[message_id] = email

    def _build_categories_indexes(self):
        """Build in-memory indexes for categories."""
        self.categories_by_id.clear()
        self.categories_by_name.clear()
        self.category_counts.clear()
        
        for category in self.categories_data:
            cat_id = category.get(FIELD_ID)
            if cat_id is not None:
                self.categories_by_id[cat_id] = category
            
            name = category.get(FIELD_NAME)
            if name:
                self.categories_by_name[name.lower()] = category

    async def _save_data(self, data_type: str):
        """Save data to JSON file."""
        if data_type == DATA_TYPE_EMAILS:
            file_path = self.emails_file
            data = self.emails_data
        elif data_type == DATA_TYPE_CATEGORIES:
            file_path = self.categories_file
            data = self.categories_data
        elif data_type == DATA_TYPE_USERS:
            file_path = self.users_file
            data = self.users_data
        else:
            raise ValueError(f"Unknown data type: {data_type}")

        # Create backup of the current file
        if os.path.exists(file_path):
            backup_path = os.path.join(self.backup_dir, f"{data_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json.gz")
            shutil.copy2(file_path, backup_path)

        # Write data to file
        with gzip.open(file_path, 'wt', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        # Mark as saved
        self._dirty_data.discard(data_type)

    async def get_all_emails(self) -> List[Dict[str, Any]]:
        """Get all emails from memory."""
        await self._ensure_initialized()
        return self.emails_data.copy()

    async def get_email_by_id(self, email_id: int) -> Optional[Dict[str, Any]]:
        """Get email by ID from memory."""
        await self._ensure_initialized()
        return self.emails_by_id.get(email_id)

    async def get_email_by_message_id(self, message_id: str) -> Optional[Dict[str, Any]]:
        """Get email by message ID from memory."""
        await self._ensure_initialized()
        return self.emails_by_message_id.get(message_id)

    async def create_email(self, email_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new email record."""
        await self._ensure_initialized()
        
        # Generate a unique ID
        new_id = max([email.get(FIELD_ID, 0) for email in self.emails_data], default=0) + 1
        email_data[FIELD_ID] = new_id
        
        # Set creation timestamp
        email_data[FIELD_CREATED_AT] = datetime.now(timezone.utc).isoformat()
        email_data[FIELD_UPDATED_AT] = datetime.now(timezone.utc).isoformat()
        
        # Add to data store
        self.emails_data.append(email_data)
        self.emails_by_id[new_id] = email_data
        message_id = email_data.get(FIELD_MESSAGE_ID)
        if message_id:
            self.emails_by_message_id[message_id] = email_data
        
        # Update category counts if applicable
        category_id = email_data.get(FIELD_CATEGORY_ID)
        if category_id:
            self.category_counts[category_id] = self.category_counts.get(category_id, 0) + 1
        
        # Mark as dirty to be saved later
        self._dirty_data.add(DATA_TYPE_EMAILS)
        
        return email_data

    async def update_email(self, email_id: int, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an existing email record."""
        await self._ensure_initialized()
        
        email = await self.get_email_by_id(email_id)
        if not email:
            return None
        
        # Update fields
        for key, value in update_data.items():
            email[key] = value
        
        # Set update timestamp
        email[FIELD_UPDATED_AT] = datetime.now(timezone.utc).isoformat()
        
        # Mark as dirty to be saved later
        self._dirty_data.add(DATA_TYPE_EMAILS)
        
        return email

    async def get_all_categories(self) -> List[Dict[str, Any]]:
        """Get all categories from memory."""
        await self._ensure_initialized()
        return self.categories_data.copy()

    async def get_category_by_id(self, category_id: int) -> Optional[Dict[str, Any]]:
        """Get category by ID from memory."""
        await self._ensure_initialized()
        return self.categories_by_id.get(category_id)

    async def get_category_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get category by name from memory."""
        await self._ensure_initialized()
        return self.categories_by_name.get(name.lower())

    async def create_category(self, category_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new category."""
        await self._ensure_initialized()
        
        # Generate a unique ID
        new_id = max([cat.get(FIELD_ID, 0) for cat in self.categories_data], default=0) + 1
        category_data[FIELD_ID] = new_id
        
        # Set creation timestamp
        category_data[FIELD_CREATED_AT] = datetime.now(timezone.utc).isoformat()
        category_data[FIELD_UPDATED_AT] = datetime.now(timezone.utc).isoformat()
        
        # Add to data store
        self.categories_data.append(category_data)
        self.categories_by_id[new_id] = category_data
        name = category_data.get(FIELD_NAME)
        if name:
            self.categories_by_name[name.lower()] = category_data
        
        # Mark as dirty to be saved later
        self._dirty_data.add(DATA_TYPE_CATEGORIES)
        
        return category_data

    async def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username from memory."""
        await self._ensure_initialized()
        for user in self.users_data:
            if user.get("username") == username:
                return user
        return None

    async def create_user(self, username: str, password: str) -> bool:
        """Create a new user."""
        await self._ensure_initialized()
        
        # Check if user already exists
        if await self.get_user_by_username(username):
            return False
        
        from .auth import hash_password
        hashed_password = hash_password(password)
        
        user_data = {
            "id": len(self.users_data) + 1,
            "username": username,
            "hashed_password": hashed_password,
            "role": "user",
            "permissions": [],
            "mfa_enabled": False,
            "mfa_secret": None,
            "mfa_backup_codes": []
        }
        
        self.users_data.append(user_data)
        self._dirty_data.add(DATA_TYPE_USERS)
        
        return True

    async def _initialize_default_categories(self):
        """Initialize default categories if they don't exist."""
        if self._default_categories_initialized:
            return

        if not self.categories_data:
            # Add default categories
            for cat_name in DEFAULT_CATEGORIES:
                if not await self.get_category_by_name(cat_name):
                    await self.create_category({
                        "name": cat_name,
                        "description": f"Default {cat_name} category",
                        "color": DEFAULT_CATEGORY_COLOR
                    })
        
        self._default_categories_initialized = True

    async def _ensure_initialized(self):
        """Ensure the database is initialized."""
        if not self._initialized:
            await self.initialize()

    # Methods for email tagging functionality
    async def add_tags_to_email(self, email_id: int, tags: List[str]) -> Optional[Dict[str, Any]]:
        """Add tags to an email."""
        await self._ensure_initialized()
        email = await self.get_email_by_id(email_id)
        if not email:
            return None

        existing_tags = email.get("tags", [])
        updated_tags = list(set(existing_tags + tags))  # Avoid duplicates

        updated_email = await self.update_email(email_id, {"tags": updated_tags})
        return updated_email

    async def remove_tags_from_email(self, email_id: int, tags: List[str]) -> bool:
        """Remove tags from an email."""
        await self._ensure_initialized()
        email = await self.get_email_by_id(email_id)
        if not email:
            return False

        existing_tags = email.get("tags", [])
        updated_tags = [tag for tag in existing_tags if tag not in tags]

        updated_email = await self.update_email(email_id, {"tags": updated_tags})
        return updated_email is not None

    async def get_dashboard_aggregates(self) -> Dict[str, Any]:
        """Retrieves aggregated dashboard statistics for efficient server-side calculations."""
        await self._ensure_initialized()

        # Get basic counts
        total_emails = len(self.emails_data)
        auto_labeled = sum(1 for email in self.emails_data if email.get(self.FIELD_CATEGORY_ID))
        categories_count = len(self.categories_data)
        unread_count = sum(1 for email in self.emails_data if not email.get('is_read', False))

        # Calculate weekly growth (simplified - in production this would be more sophisticated)
        # For now, return placeholder values
        weekly_growth = {
            "emails": total_emails,  # This should be emails added in the last week
            "percentage": 0.0  # This should be week-over-week growth percentage
        }

        return {
            "total_emails": total_emails,
            "auto_labeled": auto_labeled,
            "categories_count": categories_count,
            "unread_count": unread_count,
            "weekly_growth": weekly_growth
        }

    async def get_category_breakdown(self, limit: int = 10) -> Dict[str, int]:
        """Retrieves category breakdown statistics with configurable limit."""
        await self._ensure_initialized()

        # Count emails by category
        category_counts = {}
        for email in self.emails_data:
            category = email.get('category', 'Uncategorized')
            category_counts[category] = category_counts.get(category, 0) + 1

        # Sort by count descending and apply limit
        sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_categories[:limit])


# Factory functions and configuration management 
async def create_database_manager(config: DatabaseConfig) -> DatabaseManager:
    """
    Factory function to create and initialize a DatabaseManager instance.
    This implements the dependency injection approach mentioned in the refactoring notes.
    """
    manager = DatabaseManager(config=config)
    await manager.initialize()
    return manager


# Backward compatibility: default get_db using default config
# Preserves the original singleton pattern while allowing new approaches
_db_manager_instance: Optional[DatabaseManager] = None
_db_init_lock = asyncio.Lock()


async def get_db() -> DatabaseManager:
    """
    Provides a default singleton instance for backward compatibility.
    For new implementations, consider using create_database_manager with explicit configuration.
    
    WARNING: This function uses a global singleton pattern which is deprecated.
    Please migrate to using DatabaseConfig and create_database_manager for new code.
    """
    import warnings
    warnings.warn(
        "get_db() uses a global singleton pattern which is deprecated. "
        "Please migrate to using DatabaseConfig and create_database_manager for new code.",
        DeprecationWarning,
        stacklevel=2
    )
    
    global _db_manager_instance
    if _db_manager_instance is None:
        async with _db_init_lock:
            if _db_manager_instance is None:
                # Use default configuration for backward compatibility
                config = DatabaseConfig()
                _db_manager_instance = DatabaseManager(config=config)
                await _db_manager_instance.initialize()
    return _db_manager_instance