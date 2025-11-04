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
from .enhanced_caching import EnhancedCachingManager
from .enhanced_error_reporting import (
    log_error, 
    ErrorSeverity, 
    ErrorCategory, 
    create_error_context
)
from .constants import DEFAULT_CATEGORY_COLOR, DEFAULT_CATEGORIES
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

logger = logging.getLogger(__name__)


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


# Import DataSource locally to avoid circular imports
from .data.data_source import DataSource

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

        # Enhanced caching system
        self.caching_manager = EnhancedCachingManager()

        # State
        self._dirty_data: set[str] = set()
        self._initialized = False

        # Ensure directories exist
        os.makedirs(self.email_content_dir, exist_ok=True)
        # Create backup directory if using legacy approach
        if hasattr(self, "backup_dir"):
            os.makedirs(self.backup_dir, exist_ok=True)

    # Notes on refactor progress:
    # TODO(P1, 12h): Refactor to eliminate global state and singleton pattern per functional_analysis_report.md
    # Pseudo code for eliminating global state:
    # - Remove singleton pattern entirely
    # - Make DatabaseManager a regular class that can be instantiated multiple times if needed
    # - Use FastAPI's dependency injection system to provide instances
    # - Store instance in request state or application state instead of global
    # - Add proper lifecycle management (startup/shutdown events)
    #
    # COMPLETED: Dependency injection approach implemented
    # - DatabaseManager now supports both approaches (config-based and legacy)
    # - create_database_manager factory function handles initialization
    # - Backward compatible get_db() provided for existing code
    # - Global singleton approach preserved for compatibility but can be phased out

    def _get_email_content_path(self, email_id: int) -> str:
        """Returns the path for an individual email's content file."""
        return os.path.join(self.email_content_dir, f"{email_id}.json.gz")

    async def _load_and_merge_content(self, email_light: Dict[str, Any]) -> Dict[str, Any]:
        """Loads heavy content for a given light email record and merges them."""
        full_email = email_light.copy()
        email_id = full_email.get(FIELD_ID)
        if not email_id:
            return full_email

        # Check content cache first
        cached_content = self.caching_manager.get_email_content(email_id)
        if cached_content is not None:
            full_email.update(cached_content)
            return full_email

        content_path = self._get_email_content_path(email_id)
        if os.path.exists(content_path):
            try:
                with gzip.open(content_path, "rt", encoding="utf-8") as f:
                    heavy_data = await asyncio.to_thread(json.load, f)
                    full_email.update(heavy_data)
                    
                    # Cache the content
                    self.caching_manager.put_email_content(email_id, heavy_data)
            except (IOError, json.JSONDecodeError) as e:
                error_context = create_error_context(
                    component="DatabaseManager",
                    operation="_load_and_merge_content",
                    additional_context={"email_id": email_id, "content_path": content_path}
                )
                error_id = log_error(
                    e,
                    severity=ErrorSeverity.WARNING,
                    category=ErrorCategory.DATA,
                    context=error_context,
                    details={"error_type": type(e).__name__}
                )
                logger.error(f"Error loading content for email {email_id}: {e}. Error ID: {error_id}")
        return full_email

    async def _ensure_initialized(self) -> None:
        """Ensure data is loaded and indexes are built."""
        if not self._initialized:
            # Perform schema migration if needed (as part of initialization)
            # await self.migrate_schema()  # Commented out for now, can be called explicitly if needed
            await self._load_data()
            self._build_indexes()
            self._initialized = True

    # TODO(P1, 4h): Remove hidden side effects from initialization per functional_analysis_report.md
    # Pseudo code for removing hidden side effects:
    # - Make _ensure_initialized() a public async initialize() method
    # - Require explicit initialization before use
    # - Add _is_initialized property to check state
    # - Remove automatic initialization from methods - raise error if not initialized
    # - Make initialization idempotent but explicit
    # TODO(P2, 3h): Implement lazy loading strategy that is more predictable and testable
    # Pseudo code for lazy loading:
    # - Add LazyLoader class to handle on-demand data loading
    # - Implement load_emails_lazy(), load_categories_lazy() methods
    # - Use asyncio.Lock to prevent concurrent loading
    # - Add _loaded_data: set[str] to track what data types are loaded
    # - Make _load_data() private and called only by lazy loaders
    # - Add tests to verify loading behavior
    #
    # PARTIALLY COMPLETED: Initialization is now explicit via factory function
    # - create_database_manager ensures initialization
    # - Backward compatible get_db maintains implicit initialization for existing code
    # - TODO: Consider making initialization more explicit in future refactoring

    @log_performance(operation="build_indexes")
    def _build_indexes(self) -> None:
        """Builds or rebuilds all in-memory indexes from the loaded data."""
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

    @log_performance(operation="load_data")
    async def _load_data(self) -> None:
        """
        Loads data from JSON files into memory.
        If a data file does not exist, it creates an empty one.
        """
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
                error_context = create_error_context(
                    component="DatabaseManager",
                    operation="_load_data",
                    additional_context={"data_type": data_type, "file_path": file_path}
                )
                error_id = log_error(
                    e,
                    severity=ErrorSeverity.ERROR,
                    category=ErrorCategory.DATA,
                    context=error_context,
                    details={"error_type": type(e).__name__}
                )
                logger.error(
                    f"Error loading data from {file_path}: {e}. Error ID: {error_id}. Initializing with empty list."
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
            error_context = create_error_context(
                component="DatabaseManager",
                operation="_save_data_to_file",
                additional_context={"data_type": data_type}
            )
            error_id = log_error(
                f"Unknown data type for saving: {data_type}",
                severity=ErrorSeverity.ERROR,
                category=ErrorCategory.VALIDATION,
                context=error_context
            )
            logger.error(f"Unknown data type for saving: {data_type}. Error ID: {error_id}")
            return

        try:
            with gzip.open(file_path, "wt", encoding="utf-8") as f:
                dump_func = partial(json.dump, data_to_save, f, indent=4)
                await asyncio.to_thread(dump_func)
            logger.info(f"Persisted {len(data_to_save)} items to compressed file: {file_path}")
        except IOError as e:
            error_context = create_error_context(
                component="DatabaseManager",
                operation="_save_data_to_file",
                additional_context={"data_type": data_type, "file_path": file_path}
            )
            error_id = log_error(
                e,
                severity=ErrorSeverity.ERROR,
                category=ErrorCategory.DATA,
                context=error_context,
                details={"error_type": type(e).__name__}
            )
            logger.error(f"Error saving data to {file_path}: {e}. Error ID: {error_id}")

    async def _save_data(self, data_type: Literal["emails", "categories", "users"]) -> None:
        """Marks data as dirty for write-behind saving."""
        self._dirty_data.add(data_type)

    async def delete_email(self, email_id: int) -> bool:
        """Delete an email by its internal ID."""
        for i, email in enumerate(self.emails_data):
            if email.get(FIELD_ID) == email_id:
                deleted_email = self.emails_data.pop(i)
                self._dirty_data.add(DATA_TYPE_EMAILS)
                # Update category count if email had a category
                if FIELD_CATEGORY_ID in deleted_email:
                    await self._update_category_count(
                        deleted_email[FIELD_CATEGORY_ID], decrement=True
                    )
                logger.info(f"Deleted email with ID {email_id}")
                return True
        logger.warning(f"Email with ID {email_id} not found for deletion")
        return False

    async def shutdown(self) -> None:
        """Saves all dirty data to files before shutting down."""
        logger.info("DatabaseManager shutting down. Saving dirty data...")
        for data_type in list(self._dirty_data):
            await self._save_data_to_file(data_type)
        self._dirty_data.clear()
        
        # Log cache statistics
        cache_stats = self.caching_manager.get_cache_statistics()
        logger.info(f"Cache statistics: {cache_stats}")
        
        logger.info("Shutdown complete.")

    # Data validation methods (work-in-progress features)
    def _validate_email_data(self, email_data: Dict[str, Any]) -> bool:
        """Validates email data before storage."""
        required_fields = {FIELD_MESSAGE_ID}  # messageId is required
        if any(field not in email_data for field in required_fields):
            logger.warning(f"Missing required fields in email data: {email_data}")
            return False

        # Validate message ID format
        message_id = email_data.get(FIELD_MESSAGE_ID)
        if not isinstance(message_id, str) or not message_id.strip():
            logger.warning(f"Invalid message ID format: {message_id}")
            return False

        # Additional validation can be added here
        return True

    def _validate_category_data(self, category_data: Dict[str, Any]) -> bool:
        """Validates category data before storage."""
        required_fields = {FIELD_NAME}
        if any(field not in category_data for field in required_fields):
            logger.warning(f"Missing required fields in category data: {category_data}")
            return False

        # Validate category name
        name = category_data.get(FIELD_NAME)
        if not isinstance(name, str) or not name.strip():
            logger.warning(f"Invalid category name: {name}")
            return False

        return True

    def _validate_user_data(self, user_data: Dict[str, Any]) -> bool:
        """Validates user data before storage."""
        required_fields = {"username", "hashed_password"}
        if any(field not in user_data for field in required_fields):
            logger.warning(f"Missing required fields in user data: {user_data}")
            return False

        # Validate username
        username = user_data.get("username")
        if not isinstance(username, str) or not username.strip():
            logger.warning(f"Invalid username: {username}")
            return False

        # Validate password hash
        password_hash = user_data.get("hashed_password")
        if not isinstance(password_hash, str) or len(password_hash) < 10:  # Basic check
            logger.warning(f"Invalid password hash: {password_hash}")
            return False

        return True

    # Backup and recovery methods (work-in-progress features)
    async def create_backup(self) -> str:
        """Creates a backup of the current data files."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}"
        backup_path = os.path.join(self.backup_dir, backup_name)
        os.makedirs(backup_path, exist_ok=True)

        # Copy data files to backup location
        files_to_backup = [
            (self.emails_file, os.path.join(backup_path, "emails.json.gz")),
            (self.categories_file, os.path.join(backup_path, "categories.json.gz")),
            (self.users_file, os.path.join(backup_path, "users.json.gz")),
        ]

        for source, dest in files_to_backup:
            if os.path.exists(source):
                shutil.copy2(source, dest)
                logger.info(f"Backed up {source} to {dest}")

        # Also backup email content directory
        content_backup_path = os.path.join(backup_path, "email_content")
        if os.path.exists(self.email_content_dir):
            shutil.copytree(self.email_content_dir, content_backup_path)
            logger.info(f"Backed up email content to {content_backup_path}")

        logger.info(f"Backup created at {backup_path}")
        return backup_path

    async def restore_from_backup(self, backup_path: str) -> bool:
        """Restores data from a backup."""
        if not os.path.exists(backup_path):
            logger.error(f"Backup path does not exist: {backup_path}")
            return False

        # Files to restore
        files_to_restore = [
            (os.path.join(backup_path, "emails.json.gz"), self.emails_file),
            (os.path.join(backup_path, "categories.json.gz"), self.categories_file),
            (os.path.join(backup_path, "users.json.gz"), self.users_file),
        ]

        try:
            for source, dest in files_to_restore:
                if os.path.exists(source):
                    # Make a safety copy of current data before overwriting
                    if os.path.exists(dest):
                        shutil.copy2(dest, f"{dest}.restore_backup")

                    shutil.copy2(source, dest)
                    logger.info(f"Restored {source} to {dest}")

            # Restore email content directory
            content_source_path = os.path.join(backup_path, "email_content")
            if os.path.exists(content_source_path):
                # Remove current content and copy from backup
                if os.path.exists(self.email_content_dir):
                    shutil.rmtree(self.email_content_dir)
                shutil.copytree(content_source_path, self.email_content_dir)
                logger.info(f"Restored email content from {content_source_path}")

            # Reload data after restore
            await self._load_data()
            self._build_indexes()
            logger.info(f"Data restored from {backup_path}")
            return True
        except Exception as e:
            logger.error(f"Error during restore: {e}")
            # Attempt to restore from safety copies if available
            for source, dest in files_to_restore:
                safety_copy = f"{dest}.restore_backup"
                if os.path.exists(safety_copy):
                    shutil.move(safety_copy, dest)
            return False

    # Schema migration methods (work-in-progress features)
    def _get_schema_version(self) -> str:
        """Gets the current schema version from file."""
        if os.path.exists(self.schema_version_file):
            try:
                with open(self.schema_version_file, "r") as f:
                    data = json.load(f)
                    return data.get("version", "1.0")
            except Exception as e:
                logger.warning(f"Could not read schema version file: {e}")
                return "1.0"
        return "1.0"

    def _set_schema_version(self, version: str) -> None:
        """Sets the schema version in file."""
        with open(self.schema_version_file, "w") as f:
            json.dump({"version": version, "updated_at": datetime.now().isoformat()}, f)
        logger.info(f"Schema version set to {version}")

    async def migrate_schema(self) -> bool:
        """Performs database schema migration if needed."""
        current_version = self._get_schema_version()
        logger.info(f"Current schema version: {current_version}, target: {CURRENT_SCHEMA_VERSION}")

        if current_version == CURRENT_SCHEMA_VERSION:
            logger.info("Schema is up to date")
            return True

        logger.info(f"Starting migration from {current_version} to {CURRENT_SCHEMA_VERSION}")

        # Create backup before migration
        backup_path = await self.create_backup()
        logger.info(f"Created backup before migration at: {backup_path}")

        # Perform migration steps here
        # Currently just updating schema version, but in the future this can include
        # data transformations, index updates, etc.
        try:
            # Example: migrate data formats or structures if needed
            # await self._migrate_emails_data()
            # await self._migrate_categories_data()
            # await self._migrate_users_data()

            # Update schema version to current
            self._set_schema_version(CURRENT_SCHEMA_VERSION)
            logger.info("Schema migration completed successfully")
            return True
        except Exception as e:
            logger.error(f"Schema migration failed: {e}")
            # Attempt to restore from backup
            await self.restore_from_backup(backup_path)
            return False

    def _get_file_checksum(self, file_path: str) -> str:
        """Calculates the checksum of a file for integrity verification."""
        if not os.path.exists(file_path):
            return ""

        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            # Read the file in chunks to handle large files efficiently
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()

    async def verify_data_integrity(self) -> Dict[str, Any]:
        """Verifies the integrity of the data files."""
        logger.info("Starting data integrity verification...")

        results = {}

        # Check each data file
        files_to_check = [
            ("emails", self.emails_file),
            ("categories", self.categories_file),
            ("users", self.users_file),
        ]

        for name, file_path in files_to_check:
            if os.path.exists(file_path):
                try:
                    # Check if the file can be loaded
                    with gzip.open(file_path, "rt", encoding="utf-8") as f:
                        data = json.load(f)

                    # Verify it's a valid JSON structure
                    is_valid = isinstance(data, list)  # Expecting list for our data types
                    checksum = self._get_file_checksum(file_path)

                    results[name] = {
                        "exists": True,
                        "valid": is_valid,
                        "item_count": len(data) if is_valid else 0,
                        "checksum": checksum,
                    }
                except (IOError, json.JSONDecodeError) as e:
                    logger.error(f"Integrity check failed for {name}: {e}")
                    results[name] = {"exists": True, "valid": False, "error": str(e)}
            else:
                results[name] = {"exists": False, "valid": False, "error": "File does not exist"}

        logger.info("Data integrity verification completed")
        return results

    def _generate_id(self, data_list: List[Dict[str, Any]]) -> int:
        """
        Generates a new unique integer ID for a record.
        """
        if not data_list:
            return 1
        return max(item.get(FIELD_ID, 0) for item in data_list) + 1

    def _parse_json_fields(self, row: Dict[str, Any], fields: List[str]) -> Dict[str, Any]:
        """
        Parses fields in a data row that are stored as JSON strings.
        """
        if not row:
            return row
        for field in fields:
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
        """Add category name and color to an email using cached category data."""
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
        """Create a new email record, separating heavy and light content."""
        # Validation functionality is enabled to maintain data integrity
        if not self._validate_email_data(email_data):
            logger.warning(f"Email data validation failed: {email_data}")
            return None

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

        # Cache the new email
        self.caching_manager.put_email_record(new_id, light_email_record)
        if heavy_data:
            self.caching_manager.put_email_content(new_id, heavy_data)

        return self._add_category_details(light_email_record)

    async def get_email_by_id(
        self, email_id: int, include_content: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Get email by ID using in-memory index, with option to load heavy content."""
        # Check cache first
        cached_email = self.caching_manager.get_email_record(email_id)
        if cached_email is not None and not include_content:
            return self._add_category_details(cached_email.copy())
        
        email_light = self.emails_by_id.get(email_id)
        if not email_light:
            return None

        if include_content:
            # Check content cache
            cached_content = self.caching_manager.get_email_content(email_id)
            if cached_content is not None:
                email_full = email_light.copy()
                email_full.update(cached_content)
                return self._add_category_details(email_full)
            
            email_full = await self._load_and_merge_content(email_light)
            
            # Cache the content
            heavy_fields = {k: v for k, v in email_full.items() if k in HEAVY_EMAIL_FIELDS}
            if heavy_fields:
                self.caching_manager.put_email_content(email_id, heavy_fields)
            
            result = self._add_category_details(email_full)
        else:
            result = self._add_category_details(email_light.copy())
        
        # Cache the email record
        self.caching_manager.put_email_record(email_id, email_light)
        return result

    async def get_all_categories(self) -> List[Dict[str, Any]]:
        """Get all categories with their counts from cache."""
        for cat_id, count in self.category_counts.items():
            if cat_id in self.categories_by_id:
                self.categories_by_id[cat_id][FIELD_COUNT] = count
        return sorted(self.categories_by_id.values(), key=lambda c: c.get(FIELD_NAME, ""))

    async def create_category(self, category_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new category and update indexes."""
        # Validation functionality is enabled to maintain data integrity
        if not self._validate_category_data(category_data):
            logger.warning(f"Category data validation failed: {category_data}")
            return None

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
            self.emails_by_message_id[message_id] = email_to_update
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
            
            # Invalidate cache for this email
            self.caching_manager.invalidate_email_record(email_id)
            
        return self._add_category_details(email_to_update)

    async def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username from the users data."""
        for user in self.users_data:
            if user.get("username") == username:
                return user
        return None

    async def create_user(self, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new user and save to the users data."""
        # Validation functionality is enabled to maintain data integrity
        if not self._validate_user_data(user_data):
            logger.warning(f"User data validation failed: {user_data}")
            return None

        # Check if user already exists
        existing_user = await self.get_user_by_username(user_data.get("username", ""))
        if existing_user:
            return None

        # Generate ID for the user
        new_id = self._generate_id(self.users_data)
        user_record = {
            "id": new_id,
            "username": user_data["username"],
            "hashed_password": user_data["hashed_password"],
            "role": user_data.get("role", "user"),
            "permissions": user_data.get("permissions", []),
            "mfa_enabled": user_data.get("mfa_enabled", False),
            "mfa_secret": user_data.get("mfa_secret", None),
            "mfa_backup_codes": user_data.get("mfa_backup_codes", []),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        self.users_data.append(user_record)
        await self._save_data(DATA_TYPE_USERS)
        return user_record

    async def get_email_by_message_id(
        self, message_id: str, include_content: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Get email by messageId using in-memory index, with option to load heavy content."""
        if not message_id:
            return None
            
        # Find email_id from message_id to use with caching
        email_light = self.emails_by_message_id.get(message_id)
        if not email_light:
            return None
            
        email_id = email_light.get(FIELD_ID)
        if not email_id:
            # Fallback to original method if no ID
            if include_content:
                email_full = await self._load_and_merge_content(email_light)
                return self._add_category_details(email_full)
            else:
                return self._add_category_details(email_light.copy())
        
        # Use the enhanced caching with email_id
        return await self.get_email_by_id(email_id, include_content)

    # Backward compatibility and advanced initialization
    # The following code provides both legacy singleton access and new factory approach

    # Backward compatibility and advanced initialization
    # The following code provides both legacy singleton access and new factory approach

    async def get_all_emails(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Retrieves all emails with pagination.
        """
        return await self.get_emails(limit=limit, offset=offset)

    async def get_emails_by_category(
        self, category_id: int, limit: int = 50, offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Get emails by category"""
        return await self.get_emails(limit=limit, offset=offset, category_id=category_id)

    async def search_emails(self, query: str) -> List[Dict[str, Any]]:
        """Searches for emails matching a query."""
        return await self.search_emails_with_limit(query, limit=50)
    
    async def search_emails_with_limit(self, search_term: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Search emails with limit parameter. Searches subject/sender in-memory, and content on-disk."""
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
            sorted_emails = sorted(
                filtered_emails,
                key=lambda e: e.get(FIELD_TIME, e.get(FIELD_CREATED_AT, "")),
                reverse=True,
            )
        except TypeError:
            logger.warning(
                f"Sorting search results by {FIELD_TIME} failed. Using '{FIELD_CREATED_AT}'."
            )
            sorted_emails = sorted(
                filtered_emails, key=lambda e: e.get(FIELD_CREATED_AT, ""), reverse=True
            )
        paginated_emails = sorted_emails[:limit]
        result_emails = [self._add_category_details(email) for email in paginated_emails]
        return result_emails

    # TODO(P1, 6h): Optimize search performance to avoid disk I/O per STATIC_ANALYSIS_REPORT.md
    # Pseudo code for optimizing search performance:
    # - Pre-index searchable fields (subject, sender, sender_email) in memory
    # - Create inverted index: Dict[str, Set[int]] for word -> email_ids
    # - Use asyncio.to_thread for content search to avoid blocking
    # - Implement batched content loading for multiple emails
    # - Add search result pagination to limit memory usage
    # - Use mmap or memory-mapped files for large content searches
    # TODO(P2, 4h): Implement search indexing to improve query performance
    # Pseudo code for search indexing:
    # - Create SearchIndex class with build_index() and search() methods
    # - Index structure: {word: {email_id: positions}} for phrase search
    # - Support fuzzy matching with difflib or similar
    # - Add index persistence to avoid rebuild on restart
    # - Implement incremental index updates on email changes
    # - Add stemming/lemmatization for better matching
    # TODO(P3, 3h): Add support for search result caching
    # Pseudo code for search result caching:
    # - Add LRU cache: Dict[str, List[Dict]] with max size limit
    # - Cache key: f"{search_term}:{limit}:{include_content}"
    # - Invalidate cache on email updates/deletes
    # - Add cache TTL for time-based expiration
    # - Implement cache warming for common searches
    # - Add cache statistics (hits, misses) for monitoring

    async def update_email(
        self, email_id: int, update_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update email by its internal ID, handling separated content."""
        email_to_update = await self.get_email_by_id(email_id, include_content=True)
        if not email_to_update:
            logger.warning(f"Email with {FIELD_ID} {email_id} not found for update.")
            return {}

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
            
            # Invalidate cache for this email
            self.caching_manager.invalidate_email_record(email_id)
            
        return self._add_category_details(email_to_update)

    async def add_tags(self, email_id: Any, tags: List[str]) -> bool:
        """Adds tags to an email."""
        # Convert email_id to int if it's a string
        if isinstance(email_id, str):
            try:
                email_id = int(email_id)
            except ValueError:
                return False

        email = await self.get_email_by_id(email_id)
        if not email:
            return False

        existing_tags = email.get("tags", [])
        new_tags = list(set(existing_tags + tags))

        updated_email = await self.update_email(email_id, {"tags": new_tags})
        return bool(updated_email)  # Return True if update was successful (not empty dict)

    async def remove_tags(self, email_id: Any, tags: List[str]) -> bool:
        """Removes tags from an email."""
        # Convert email_id to int if it's a string
        if isinstance(email_id, str):
            try:
                email_id = int(email_id)
            except ValueError:
                return False
        
    async def remove_tags(self, email_id: Any, tags: List[str]) -> bool:
        """Removes tags from an email."""
        # Convert email_id to int if it's a string
        if isinstance(email_id, str):
            try:
                email_id = int(email_id)
            except ValueError:
                return False

        email = await self.get_email_by_id(email_id)
        if not email:
            return False

        existing_tags = email.get("tags", [])
        updated_tags = [tag for tag in existing_tags if tag not in tags]

        updated_email = await self.update_email(email_id, {"tags": updated_tags})
        return bool(updated_email)  # Return True if update was successful (not empty dict)

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


# Factory functions and configuration management (work-in-progress)
async def create_database_manager(config: DatabaseConfig) -> DatabaseManager:
    """
    Factory function to create and initialize a DatabaseManager instance.
    This implements the dependency injection approach mentioned in the refactoring notes.
    """
    manager = DatabaseManager(config=config)
    await manager._ensure_initialized()
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
