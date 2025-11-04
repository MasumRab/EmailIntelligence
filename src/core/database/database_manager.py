"""
Refactored Database Manager for Email Intelligence Platform
"""

import logging
from typing import Any, Dict, List, Optional

from .constants import (
    DATA_TYPE_CATEGORIES,
    DATA_TYPE_EMAILS,
    DATA_TYPE_USERS,
    FIELD_ID,
    FIELD_MESSAGE_ID,
    FIELD_CATEGORY_ID,
    FIELD_ANALYSIS_METADATA,
    FIELD_CREATED_AT,
    FIELD_UPDATED_AT,
    FIELD_NAME,
    FIELD_COUNT,
    HEAVY_EMAIL_FIELDS
)
from .data_loader import DataLoader
from .index_manager import IndexManager
from .content_manager import ContentManager
from ..performance_monitor import log_performance

logger = logging.getLogger(__name__)

# Global database manager instance
_db_manager_instance = None


class DatabaseManager:
    """
    Refactored database manager with separated concerns.
    
    This class coordinates the different components of the database system:
    - DataLoader: Handles file I/O operations
    - IndexManager: Manages in-memory indexes for fast access
    - ContentManager: Manages heavy email content storage
    """

    def __init__(self):
        """Initialize the database manager with its components."""
        from .constants import EMAIL_CONTENT_DIR
        
        # Initialize components
        self.data_loader = DataLoader()
        self.index_manager = IndexManager()
        self.content_manager = ContentManager(EMAIL_CONTENT_DIR)

        # In-memory data stores
        self.emails_data: List[Dict[str, Any]] = []
        self.categories_data: List[Dict[str, Any]] = []
        self.users_data: List[Dict[str, Any]] = []

        # State
        self._dirty_data: set[str] = set()
        self._initialized = False

    async def _ensure_initialized(self) -> None:
        """Ensure the database is initialized."""
        if not self._initialized:
            await self._load_data()
            self.index_manager.build_indexes(self.emails_data, self.categories_data)
            self._initialized = True

    async def _load_data(self) -> None:
        """Load all data from files."""
        self.emails_data = await self.data_loader.load_data(DATA_TYPE_EMAILS)
        self.categories_data = await self.data_loader.load_data(DATA_TYPE_CATEGORIES)
        self.users_data = await self.data_loader.load_data(DATA_TYPE_USERS)

    async def _save_data(self, data_type: str) -> None:
        """Mark data as dirty for write-behind saving."""
        self._dirty_data.add(data_type)

    async def shutdown(self) -> None:
        """Shutdown the database manager, saving any dirty data."""
        logger.info("DatabaseManager shutting down. Saving dirty data...")
        for data_type in list(self._dirty_data):
            await self._save_data_to_file(data_type)
        self._dirty_data.clear()
        logger.info("Shutdown complete.")

    async def _save_data_to_file(self, data_type: str) -> None:
        """Save data to file."""
        if data_type == DATA_TYPE_EMAILS:
            await self.data_loader.save_data_to_file(DATA_TYPE_EMAILS, self.emails_data)
        elif data_type == DATA_TYPE_CATEGORIES:
            await self.data_loader.save_data_to_file(
                DATA_TYPE_CATEGORIES, self.categories_data, self.index_manager.category_counts
            )
        elif data_type == DATA_TYPE_USERS:
            await self.data_loader.save_data_to_file(DATA_TYPE_USERS, self.users_data)
        else:
            logger.error(f"Unknown data type for saving: {data_type}")
            return

        # Remove from dirty set after successful save
        self._dirty_data.discard(data_type)

    def _generate_id(self, data_list: List[Dict[str, Any]]) -> int:
        """Generate a new unique integer ID."""
        if not data_list:
            return 1
        return max(item.get(FIELD_ID, 0) for item in data_list) + 1

    def _parse_json_fields(self, row: Dict[str, Any], fields: List[str]) -> Dict[str, Any]:
        """Parse fields in a data row that are stored as JSON strings."""
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
        """Add category details to an email record."""
        if not email:
            return email
        category_id = email.get(FIELD_CATEGORY_ID)
        if category_id is not None:
            category = self.index_manager.get_category_by_id(category_id)
            if category:
                email["categoryName"] = category.get(FIELD_NAME)
                email["categoryColor"] = category.get("color")
        return self._parse_json_fields(email, [FIELD_ANALYSIS_METADATA])

    async def create_email(self, email_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new email record."""
        await self._ensure_initialized()
        
        message_id = email_data.get(FIELD_MESSAGE_ID, email_data.get("messageId"))
        if self.index_manager.get_email_by_message_id(message_id):
            logger.warning(f"Email with messageId {message_id} already exists. Updating.")
            return await self.update_email_by_message_id(message_id, email_data)

        new_id = self._generate_id(self.emails_data)
        from datetime import datetime, timezone
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

        # Save heavy content separately
        await self.content_manager.save_email_content(new_id, full_email_record)
        
        # Keep only light data in memory
        light_email_record = {
            k: v for k, v in full_email_record.items() 
            if k not in HEAVY_EMAIL_FIELDS
        }
        
        # Add to data and indexes
        self.emails_data.append(light_email_record)
        self.index_manager.add_email_index(light_email_record)
        
        await self._save_data(DATA_TYPE_EMAILS)

        category_id = light_email_record.get(FIELD_CATEGORY_ID)
        if category_id is not None:
            self.index_manager.update_category_count(category_id, increment=True)
            await self._save_data(DATA_TYPE_CATEGORIES)

        return self._add_category_details(light_email_record)

    async def get_email_by_id(
        self, email_id: int, include_content: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Get email by ID."""
        await self._ensure_initialized()
        email_light = self.index_manager.get_email_by_id(email_id)
        if not email_light:
            return None

        if include_content:
            email_full = await self.content_manager.load_and_merge_content(email_light)
            return self._add_category_details(email_full)
        else:
            return self._add_category_details(email_light.copy())

    async def get_all_categories(self) -> List[Dict[str, Any]]:
        """Get all categories."""
        await self._ensure_initialized()
        return sorted(self.index_manager.categories_by_id.values(), key=lambda c: c.get(FIELD_NAME, ""))

    async def create_category(self, category_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new category."""
        await self._ensure_initialized()
        
        category_name_lower = category_data.get(FIELD_NAME, "").lower()
        if self.index_manager.get_category_by_name(category_name_lower):
            logger.warning(
                f"Category with name '{category_data.get(FIELD_NAME)}' already exists. Returning existing."
            )
            return self.index_manager.get_category_by_name(category_name_lower)

        new_id = self._generate_id(self.categories_data)
        category_record = {
            FIELD_ID: new_id,
            FIELD_NAME: category_data[FIELD_NAME],
            "description": category_data.get("description"),
            "color": category_data.get("color", "#6366f1"),
            FIELD_COUNT: 0,
        }
        self.categories_data.append(category_record)
        self.index_manager.add_category_index(category_record)
        await self._save_data(DATA_TYPE_CATEGORIES)
        return category_record

    async def update_category(
        self, category_id: int, update_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Update a category by its ID."""
        await self._ensure_initialized()
        
        category_to_update = self.index_manager.get_category_by_id(category_id)
        if not category_to_update:
            logger.warning(f"Category with {FIELD_ID} {category_id} not found for update.")
            return None

        changed_fields = False
        for key, value in update_data.items():
            if key == FIELD_ID:
                continue
            if key in category_to_update and category_to_update[key] != value:
                category_to_update[key] = value
                changed_fields = True
            elif key not in category_to_update:
                category_to_update[key] = value
                changed_fields = True

        if changed_fields:
            category_name_lower = category_to_update[FIELD_NAME].lower()
            self.index_manager.categories_by_name[category_name_lower] = category_to_update
            await self._save_data(DATA_TYPE_CATEGORIES)

        return category_to_update

    async def delete_category(self, category_id: int) -> bool:
        """Delete a category by its ID."""
        await self._ensure_initialized()
        
        category_to_delete = self.index_manager.get_category_by_id(category_id)
        if not category_to_delete:
            logger.warning(f"Category with {FIELD_ID} {category_id} not found for deletion.")
            return False

        category_name = category_to_delete.get(FIELD_NAME)
        
        # Remove from data list
        self.categories_data = [
            cat for cat in self.categories_data if cat.get(FIELD_ID) != category_id
        ]

        # Remove from indexes
        self.index_manager.remove_category_index(category_id, category_name)
        
        # Save the updated data
        await self._save_data(DATA_TYPE_CATEGORIES)
        return True

    async def get_emails(
        self,
        limit: int = 50,
        offset: int = 0,
        category_id: Optional[int] = None,
        is_unread: Optional[bool] = None,
    ) -> List[Dict[str, Any]]:
        """Get emails with pagination and filtering."""
        await self._ensure_initialized()
        
        filtered_emails = self.emails_data
        if category_id is not None:
            filtered_emails = [
                e for e in filtered_emails if e.get(FIELD_CATEGORY_ID) == category_id
            ]
        if is_unread is not None:
            filtered_emails = [e for e in filtered_emails if e.get("is_unread") == is_unread]
            
        try:
            filtered_emails = sorted(
                filtered_emails,
                key=lambda e: e.get("time", e.get(FIELD_CREATED_AT, "")),
                reverse=True,
            )
        except TypeError:
            logger.warning(
                f"Sorting emails by time failed due to incomparable types. Using '{FIELD_CREATED_AT}'."
            )
            filtered_emails = sorted(
                filtered_emails, key=lambda e: e.get(FIELD_CREATED_AT, ""), reverse=True
            )
            
        paginated_emails = filtered_emails[offset : offset + limit]
        result_emails = [self._add_category_details(email) for email in paginated_emails]
        logger.info(f"Email retrieval completed. Found {len(result_emails)} emails.")
        return result_emails

    async def update_email_by_message_id(
        self, message_id: str, update_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Update email by messageId."""
        await self._ensure_initialized()
        
        email_to_update = self.index_manager.get_email_by_message_id(message_id)
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
            
            # Update heavy content
            email_id = email_to_update[FIELD_ID]
            await self.content_manager.update_email_content(email_id, email_to_update)

            # Update indexes
            self.index_manager.emails_by_id[email_id] = email_to_update
            if email_to_update.get(FIELD_MESSAGE_ID):
                self.index_manager.emails_by_message_id[email_to_update[FIELD_MESSAGE_ID]] = email_to_update
                
            idx = next(
                (i for i, e in enumerate(self.emails_data) if e.get(FIELD_ID) == email_id), -1
            )
            if idx != -1:
                self.emails_data[idx] = email_to_update
                
            await self._save_data(DATA_TYPE_EMAILS)

            new_category_id = email_to_update.get(FIELD_CATEGORY_ID)
            if original_category_id != new_category_id:
                if original_category_id is not None:
                    self.index_manager.update_category_count(original_category_id, decrement=True)
                if new_category_id is not None:
                    self.index_manager.update_category_count(new_category_id, increment=True)
                await self._save_data(DATA_TYPE_CATEGORIES)
                
        return self._add_category_details(email_to_update)

    async def get_email_by_message_id(
        self, message_id: str, include_content: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Get email by messageId."""
        await self._ensure_initialized()
        
        if not message_id:
            return None
        email_light = self.index_manager.get_email_by_message_id(message_id)
        if not email_light:
            return None
        if include_content:
            email_full = await self.content_manager.load_and_merge_content(email_light)
            return self._add_category_details(email_full)
        else:
            return self._add_category_details(email_light.copy())

    async def get_all_emails(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """Get all emails with pagination."""
        return await self.get_emails(limit=limit, offset=offset)

    async def get_emails_by_category(
        self, category_id: int, limit: int = 50, offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Get emails by category."""
        return await self.get_emails(limit=limit, offset=offset, category_id=category_id)

    @log_performance(operation="search_emails")
    async def search_emails(self, search_term: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Search emails by term."""
        await self._ensure_initialized()
        
        if not search_term:
            return await self.get_emails(limit=limit, offset=0)
        search_term_lower = search_term.lower()
        filtered_emails = []
        logger.info(
            f"Starting email search for term: '{search_term_lower}'. This may be slow if searching content."
        )
        for email_light in self.emails_data:
            found_in_light = (
                search_term_lower in email_light.get("subject", "").lower()
                or search_term_lower in email_light.get("sender", "").lower()
                or search_term_lower in email_light.get("sender_email", "").lower()
            )
            if found_in_light:
                filtered_emails.append(email_light)
                continue
            email_id = email_light.get(FIELD_ID)
            if self.content_manager.content_exists(email_id):
                try:
                    email_full = await self.content_manager.load_and_merge_content(email_light)
                    content = email_full.get(FIELD_CONTENT, "")
                    if isinstance(content, str) and search_term_lower in content.lower():
                        filtered_emails.append(email_light)
                except Exception as e:
                    logger.error(f"Could not search content for email {email_id}: {e}")
        return filtered_emails[:limit]

    async def update_email(
        self, email_id: int, update_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Update email by its internal ID."""
        await self._ensure_initialized()
        
        email_to_update = self.index_manager.get_email_by_id(email_id)
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
            from datetime import datetime, timezone
            email_to_update[FIELD_UPDATED_AT] = datetime.now(timezone.utc).isoformat()
            
            # Update heavy content
            await self.content_manager.update_email_content(email_id, email_to_update)

            # Update indexes
            self.index_manager.emails_by_id[email_id] = email_to_update
            if email_to_update.get(FIELD_MESSAGE_ID):
                self.index_manager.emails_by_message_id[email_to_update[FIELD_MESSAGE_ID]] = email_to_update
                
            idx = next(
                (i for i, e in enumerate(self.emails_data) if e.get(FIELD_ID) == email_id), -1
            )
            if idx != -1:
                self.emails_data[idx] = email_to_update
                
            await self._save_data(DATA_TYPE_EMAILS)

            new_category_id = email_to_update.get(FIELD_CATEGORY_ID)
            if original_category_id != new_category_id:
                if original_category_id is not None:
                    self.index_manager.update_category_count(original_category_id, decrement=True)
                if new_category_id is not None:
                    self.index_manager.update_category_count(new_category_id, increment=True)
                await self._save_data(DATA_TYPE_CATEGORIES)
                
        return self._add_category_details(email_to_update)

    async def get_total_emails_count(self) -> int:
        """Get the total count of emails in the system."""
        await self._ensure_initialized()
        return len(self.emails_data)

    async def get_auto_labeled_count(self) -> int:
        """Get the count of emails that have been auto-labeled."""
        await self._ensure_initialized()
        return sum(1 for email in self.emails_data if email.get(FIELD_CATEGORY_ID))

    async def get_categories_count(self) -> int:
        """Get the total number of categories."""
        await self._ensure_initialized()
        return len(self.categories_data)

    async def get_weekly_growth(self) -> Dict[str, Any]:
        """Get the weekly growth statistics."""
        await self._ensure_initialized()
        total_count = len(self.emails_data)
        return {"emails": total_count, "percentage": 0.0}


# Dependency injection functions
async def get_db() -> DatabaseManager:
    """
    Provides the singleton instance of the DatabaseManager.
    """
    global _db_manager_instance
    if _db_manager_instance is None:
        _db_manager_instance = DatabaseManager()
        await _db_manager_instance._ensure_initialized()
    return _db_manager_instance


async def initialize_db():
    """Initialize the database manager."""
    global _db_manager_instance
    if _db_manager_instance is None:
        _db_manager_instance = DatabaseManager()
        await _db_manager_instance._ensure_initialized()