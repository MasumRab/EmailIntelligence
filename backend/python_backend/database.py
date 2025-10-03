"""
Database management for Gmail AI email processing
JSON file storage implementation.
"""

import asyncio
import json
import logging
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Literal
from functools import partial
from .constants import DEFAULT_CATEGORY_COLOR, DEFAULT_CATEGORIES

logger = logging.getLogger(__name__)

# File paths
DATA_DIR = "backend/data"
EMAILS_FILE = os.path.join(DATA_DIR, "emails.json")
CATEGORIES_FILE = os.path.join(DATA_DIR, "categories.json")
USERS_FILE = os.path.join(DATA_DIR, "users.json")

# Data types
DATA_TYPE_EMAILS = 'emails'
DATA_TYPE_CATEGORIES = 'categories'
DATA_TYPE_USERS = 'users'

# Field names
FIELD_ID = 'id'
FIELD_MESSAGE_ID = 'message_id'
FIELD_CATEGORY_ID = 'category_id'
FIELD_IS_UNREAD = 'is_unread'
FIELD_ANALYSIS_METADATA = 'analysis_metadata'
FIELD_CREATED_AT = 'created_at'
FIELD_UPDATED_AT = 'updated_at'
FIELD_NAME = 'name'
FIELD_COLOR = 'color'
FIELD_COUNT = 'count'
FIELD_TIME = 'time'
FIELD_CONTENT = 'content'
FIELD_SUBJECT = 'subject'
FIELD_SENDER = 'sender'
FIELD_SENDER_EMAIL = 'sender_email'

# UI field names
FIELD_CATEGORY_NAME = 'categoryName'
FIELD_CATEGORY_COLOR = 'categoryColor'

class DatabaseManager:
    """Optimized async database manager with in-memory caching and write-behind."""

    def __init__(self):
        self.emails_file = EMAILS_FILE
        self.categories_file = CATEGORIES_FILE
        self.users_file = USERS_FILE

        # In-memory data stores
        self.emails_data: List[Dict[str, Any]] = []
        self.categories_data: List[Dict[str, Any]] = []
        self.users_data: List[Dict[str, Any]] = []

        # In-memory indexes for O(1) lookups
        self.emails_by_id: Dict[int, Dict[str, Any]] = {}
        self.emails_by_message_id: Dict[str, Dict[str, Any]] = {}
        self.categories_by_id: Dict[int, Dict[str, Any]] = {}
        self.categories_by_name: Dict[str, Dict[str, Any]] = {}

        # In-memory cache for category counts
        self.category_counts: Dict[int, int] = {}

        # Write-behind cache state
        self._dirty_data: set[Literal['emails', 'categories', 'users']] = set()

        # Ensure data directory exists
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
            logger.info(f"Created data directory: {DATA_DIR}")

        self._initialized = False

    async def _ensure_initialized(self) -> None:
        """Ensure data is loaded and indexes are built."""
        if not self._initialized:
            await self._load_data()
            self._build_indexes()
            self._initialized = True

    def _build_indexes(self) -> None:
        """Builds or rebuilds all in-memory indexes from the loaded data."""
        logger.info("Building in-memory indexes...")
        # Index emails
        self.emails_by_id = {email[FIELD_ID]: email for email in self.emails_data}
        self.emails_by_message_id = {email[FIELD_MESSAGE_ID]: email for email in self.emails_data if FIELD_MESSAGE_ID in email}

        # Index categories
        self.categories_by_id = {cat[FIELD_ID]: cat for cat in self.categories_data}
        self.categories_by_name = {cat[FIELD_NAME].lower(): cat for cat in self.categories_data}

        # Cache category counts
        self.category_counts = {cat_id: 0 for cat_id in self.categories_by_id}
        for email in self.emails_data:
            cat_id = email.get(FIELD_CATEGORY_ID)
            if cat_id in self.category_counts:
                self.category_counts[cat_id] += 1

        for cat_id, count in self.category_counts.items():
            if self.categories_by_id[cat_id].get(FIELD_COUNT) != count:
                 self.categories_by_id[cat_id][FIELD_COUNT] = count
                 self._dirty_data.add(DATA_TYPE_CATEGORIES)


        logger.info("In-memory indexes built successfully.")


    async def _load_data(self) -> None:
        """Loads data from JSON files into memory. Creates files if they don't exist."""
        for data_type, file_path, data_list_attr in [
            (DATA_TYPE_EMAILS, self.emails_file, 'emails_data'),
            (DATA_TYPE_CATEGORIES, self.categories_file, 'categories_data'),
            (DATA_TYPE_USERS, self.users_file, 'users_data')
        ]:
            try:
                if os.path.exists(file_path):
                    with open(file_path, 'r') as f:
                        data = await asyncio.to_thread(json.load, f)
                        setattr(self, data_list_attr, data)
                    logger.info(f"Loaded {len(data)} items from {file_path}")
                else:
                    setattr(self, data_list_attr, [])
                    await self._save_data_to_file(data_type) # Create file with empty list
                    logger.info(f"Created empty data file: {file_path}")
            except (IOError, json.JSONDecodeError) as e:
                logger.error(f"Error loading data from {file_path}: {e}. Initializing with empty list.")
                setattr(self, data_list_attr, [])

    async def _save_data_to_file(self, data_type: Literal['emails', 'categories', 'users']) -> None:
        """Saves the specified in-memory data list to its JSON file."""
        file_path, data_to_save = "", []
        if data_type == DATA_TYPE_EMAILS:
            file_path, data_to_save = self.emails_file, self.emails_data
        elif data_type == DATA_TYPE_CATEGORIES:
            # Before saving, ensure the counts in categories_data are up-to-date from the cache
            for cat in self.categories_data:
                if cat['id'] in self.category_counts:
                    cat['count'] = self.category_counts[cat['id']]
            file_path, data_to_save = self.categories_file, self.categories_data
        elif data_type == DATA_TYPE_USERS:
            file_path, data_to_save = self.users_file, self.users_data
        else:
            logger.error(f"Unknown data type for saving: {data_type}")
            return

        try:
            with open(file_path, 'w') as f:
                dump_func = partial(json.dump, data_to_save, f, indent=4)
                await asyncio.to_thread(dump_func)
            logger.info(f"Persisted {len(data_to_save)} items to {file_path}")
        except IOError as e:
            logger.error(f"Error saving data to {file_path}: {e}")

    async def _save_data(self, data_type: Literal['emails', 'categories', 'users']) -> None:
        """Marks data as dirty for write-behind saving."""
        self._dirty_data.add(data_type)

    async def shutdown(self) -> None:
        """Saves all dirty data to files before shutting down."""
        logger.info("DatabaseManager shutting down. Saving dirty data...")
        for data_type in list(self._dirty_data):
            await self._save_data_to_file(data_type)
        self._dirty_data.clear()
        logger.info("Shutdown complete.")

    def _generate_id(self, data_list: List[Dict[str, Any]]) -> int:
        """Generates a new unique integer ID."""
        if not data_list:
            return 1
        return max(item.get(FIELD_ID, 0) for item in data_list) + 1

    async def initialize(self) -> None:
        """
        Initializes the database by ensuring data files and directory exist.
        Default categories can be seeded here if needed.
        """
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
            logger.info(f"Created data directory during initialization: {DATA_DIR}")

        await self._load_data()  # Ensure files are loaded/created

        # Seed default categories if categories.json is empty
        if not self.categories_data:
            for cat_data in DEFAULT_CATEGORIES:
                await self.create_category(cat_data)
            logger.info("Seeded default categories.")


    def _parse_json_fields(self, row: Dict[str, Any], fields: List[str]) -> Dict[str, Any]:
        """Helper to parse stringified JSON fields in a row."""
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
                    if field in (FIELD_ANALYSIS_METADATA, "metadata"):  # "metadata" for compatibility
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
        """Create a new email record."""
        # Check for existing email by message_id
        message_id = email_data.get(FIELD_MESSAGE_ID, email_data.get("messageId"))
        existing_email = await self.get_email_by_message_id(message_id)
        if existing_email:
            logger.warning(f"Email with messageId {message_id} already exists. Updating.")
            # Convert camelCase to snake_case for update_data if necessary
            update_payload = {k: v for k, v in email_data.items()}
            return await self.update_email_by_message_id(message_id, update_payload)

        new_id = self._generate_id(self.emails_data)
        now = datetime.now(timezone.utc).isoformat()

        # Ensure analysisMetadata is a dict, not a string, before storing
        analysis_metadata = email_data.get(FIELD_ANALYSIS_METADATA, email_data.get("analysisMetadata", {}))
        if isinstance(analysis_metadata, str):
            try:
                analysis_metadata = json.loads(analysis_metadata)
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse {FIELD_ANALYSIS_METADATA} string, defaulting to {{}}")
                analysis_metadata = {}

        email_record = {
            FIELD_ID: new_id,
            FIELD_MESSAGE_ID: email_data.get(FIELD_MESSAGE_ID, email_data.get("messageId")),
            "thread_id": email_data.get("thread_id", email_data.get("threadId")),
            FIELD_SUBJECT: email_data.get(FIELD_SUBJECT),
            FIELD_SENDER: email_data.get(FIELD_SENDER),
            FIELD_SENDER_EMAIL: email_data.get(FIELD_SENDER_EMAIL, email_data.get("senderEmail")),
            FIELD_CONTENT: email_data.get(FIELD_CONTENT),
            "snippet": email_data.get("snippet"),
            "labels": email_data.get("labels", []),
            FIELD_TIME: email_data.get(FIELD_TIME, email_data.get("timestamp", now)),
            FIELD_IS_UNREAD: not email_data.get("is_read", False),
            FIELD_CATEGORY_ID: email_data.get(FIELD_CATEGORY_ID, email_data.get("categoryId")),
            "confidence": email_data.get("confidence", 0),
            FIELD_ANALYSIS_METADATA: analysis_metadata,
            FIELD_CREATED_AT: now,
            FIELD_UPDATED_AT: now,
            "history_id": email_data.get("history_id", email_data.get("historyId")),
            "content_html": email_data.get("content_html", email_data.get("contentHtml")),
            "preview": email_data.get("preview", email_data.get("snippet")),  # Using snippet as fallback
            "to_addresses": email_data.get("to_addresses", email_data.get("toAddresses", [])),
            "cc_addresses": email_data.get("cc_addresses", email_data.get("ccAddresses", [])),
            "bcc_addresses": email_data.get("bcc_addresses", email_data.get("bccAddresses", [])),
            "reply_to": email_data.get("reply_to", email_data.get("replyTo")),
            "internal_date": email_data.get("internal_date", email_data.get("internalDate")),
            "label_ids": email_data.get("label_ids", email_data.get("labelIds", [])),
            "category": email_data.get("category"),  # This might be redundant if category_id is used
            "is_starred": email_data.get("is_starred", email_data.get("isStarred", False)),
            "is_important": email_data.get("is_important", email_data.get("isImportant", False)),
            "is_draft": email_data.get("is_draft", email_data.get("isDraft", False)),
            "is_sent": email_data.get("is_sent", email_data.get("isSent", False)),
            "is_spam": email_data.get("is_spam", email_data.get("isSpam", False)),
            "is_trash": email_data.get("is_trash", email_data.get("isTrash", False)),
            "is_chat": email_data.get("is_chat", email_data.get("isChat", False)),
            "has_attachments": email_data.get("has_attachments", email_data.get("hasAttachments", False)),
            "attachment_count": email_data.get("attachment_count", email_data.get("attachmentCount", 0)),
            "size_estimate": email_data.get("size_estimate", email_data.get("sizeEstimate")),
            "spf_status": email_data.get("spf_status", email_data.get("spfStatus")),
            "dkim_status": email_data.get("dkim_status", email_data.get("dkimStatus")),
            "dmarc_status": email_data.get("dmarc_status", email_data.get("dmarcStatus")),
            "is_encrypted": email_data.get("is_encrypted", email_data.get("isEncrypted", False)),
            "is_signed": email_data.get("is_signed", email_data.get("isSigned", False)),
            "priority": email_data.get("priority", "normal"),
            "is_auto_reply": email_data.get("is_auto_reply", email_data.get("isAutoReply", False)),
            "mailing_list": email_data.get("mailing_list", email_data.get("mailingList")),
            "in_reply_to": email_data.get("in_reply_to", email_data.get("inReplyTo")),
            "references": email_data.get("references", []),
            "is_first_in_thread": email_data.get("is_first_in_thread", email_data.get("isFirstInThread", True)),
        }
        self.emails_data.append(email_record)
        self.emails_by_id[new_id] = email_record
        if FIELD_MESSAGE_ID in email_record:
            self.emails_by_message_id[email_record[FIELD_MESSAGE_ID]] = email_record

        await self._save_data(DATA_TYPE_EMAILS)

        category_id = email_record.get(FIELD_CATEGORY_ID)
        if category_id is not None:
            await self._update_category_count(category_id, increment=True)

        return self._add_category_details(email_record)

    async def get_email_by_id(self, email_id: int) -> Optional[Dict[str, Any]]:
        """Get email by ID using in-memory index."""
        email = self.emails_by_id.get(email_id)
        if email:
            return self._add_category_details(email)
        return None

    async def get_all_categories(self) -> List[Dict[str, Any]]:
        """Get all categories with their counts from cache."""
        # Update counts from cache before returning
        for cat_id, count in self.category_counts.items():
            if cat_id in self.categories_by_id:
                self.categories_by_id[cat_id][FIELD_COUNT] = count

        # Return sorted list of category values
        return sorted(self.categories_by_id.values(), key=lambda c: c.get(FIELD_NAME, ''))

    async def create_category(self, category_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new category and update indexes."""
        category_name_lower = category_data.get(FIELD_NAME, '').lower()
        if category_name_lower in self.categories_by_name:
            logger.warning(f"Category with name '{category_data.get(FIELD_NAME)}' already exists. Returning existing.")
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

    async def _update_category_count(self, category_id: int, increment: bool = False, decrement: bool = False) -> None:
        """Incrementally update category email count in the cache."""
        if category_id not in self.category_counts:
            logger.warning(f"Attempted to update count for non-existent category ID: {category_id}")
            return

        if increment:
            self.category_counts[category_id] += 1
        if decrement:
            self.category_counts[category_id] -= 1

        # Mark categories as dirty to be saved later
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
            filtered_emails = [e for e in filtered_emails if e.get(FIELD_CATEGORY_ID) == category_id]

        if is_unread is not None:
            filtered_emails = [e for e in filtered_emails if e.get(FIELD_IS_UNREAD) == is_unread]

        # Sort by time descending
        try:
            # Attempt to sort by 'time' if it exists and is valid.
            # Fallback to 'created_at' or no sort if 'time' is problematic.
            filtered_emails = sorted(
                filtered_emails, 
                key=lambda e: e.get(FIELD_TIME, e.get(FIELD_CREATED_AT, '')), 
                reverse=True
            )
        except TypeError:  # Handles cases where 'time' might be None or not comparable
            logger.warning(f"Sorting emails by {FIELD_TIME} failed due to incomparable types. Using '{FIELD_CREATED_AT}'.")
            filtered_emails = sorted(
                filtered_emails, 
                key=lambda e: e.get(FIELD_CREATED_AT, ''), 
                reverse=True
            )

        paginated_emails = filtered_emails[offset : offset + limit]

        # Add category details and parse JSON fields
        result_emails = []
        for email in paginated_emails:
            result_emails.append(self._add_category_details(email))
        return result_emails


    async def update_email_by_message_id(
        self, message_id: str, update_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Update email by messageId."""
        email_to_update = await self.get_email_by_message_id(message_id)
        if not email_to_update:
            logger.warning(f"Email with {FIELD_MESSAGE_ID} {message_id} not found for update.")
            return None

        original_category_id = email_to_update.get(FIELD_CATEGORY_ID)
        changed_fields = False

        for key, value in update_data.items():
            # Normalize keys (e.g. messageId -> message_id)
            snake_key = key.replace("Id", "_id").replace("Html", "_html").replace("Addresses", "_addresses")
            snake_key = ''.join(['_'+i.lower() if i.isupper() else i for i in snake_key]).lstrip('_')

            if snake_key == FIELD_MESSAGE_ID:
                continue  # Cannot change message_id

            if snake_key == "is_read":
                if email_to_update.get(FIELD_IS_UNREAD) == value:  # is_read=True means is_unread=False
                    email_to_update[FIELD_IS_UNREAD] = not value
                    changed_fields = True
            elif snake_key == FIELD_ANALYSIS_METADATA:
                if isinstance(value, str):
                    try:
                        value = json.loads(value)
                    except json.JSONDecodeError:
                        logger.warning(f"Invalid JSON string for {FIELD_ANALYSIS_METADATA}: {value}")
                        value = email_to_update.get(snake_key, {})  # Keep old if new is invalid
                if email_to_update.get(snake_key) != value:
                    email_to_update[snake_key] = value
                    changed_fields = True
            elif snake_key in email_to_update:  # Check if the key exists in the email dict
                if email_to_update.get(snake_key) != value:
                    email_to_update[snake_key] = value
                    changed_fields = True
            else:
                # If the key doesn't exist, it might be a new field or a typo
                known_fields = list(email_to_update.keys())  # Get all current fields
                if snake_key not in known_fields and key not in [FIELD_ID, FIELD_CREATED_AT, FIELD_UPDATED_AT]:
                    email_to_update[snake_key] = value  # Add as new field
                    changed_fields = True
                    logger.info(f"Added new field '{snake_key}' to email {message_id}")

        if changed_fields:
            email_to_update[FIELD_UPDATED_AT] = datetime.now(timezone.utc).isoformat()
            await self._save_data(DATA_TYPE_EMAILS)

            new_category_id = email_to_update.get(FIELD_CATEGORY_ID)
            if original_category_id != new_category_id:
                if original_category_id is not None:
                    await self._update_category_count(original_category_id, decrement=True)
                if new_category_id is not None:
                    await self._update_category_count(new_category_id, increment=True)

        return self._add_category_details(email_to_update)

    async def get_email_by_message_id(self, message_id: str) -> Optional[Dict[str, Any]]:
        """Get email by messageId using in-memory index."""
        if not message_id: 
            return None
        email = self.emails_by_message_id.get(message_id)
        if email:
            return self._add_category_details(email)
        return None

    async def get_all_emails(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """Get all emails with pagination"""
        return await self.get_emails(limit=limit, offset=offset)

    async def get_emails_by_category(
        self, category_id: int, limit: int = 50, offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Get emails by category"""
        return await self.get_emails(limit=limit, offset=offset, category_id=category_id)

    async def search_emails(self, search_term: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Search emails by content or subject (basic substring matching)."""
        if not search_term:
            return await self.get_emails(limit=limit, offset=0)

        search_term_lower = search_term.lower()
        # Filter by subject, content, sender, or sender email
        filtered_emails = [
            email for email in self.emails_data
            if (search_term_lower in email.get(FIELD_SUBJECT, '').lower() or
                (isinstance(email.get(FIELD_CONTENT), str) and 
                 search_term_lower in email.get(FIELD_CONTENT, '').lower()) or
                search_term_lower in email.get(FIELD_SENDER, '').lower() or
                search_term_lower in email.get(FIELD_SENDER_EMAIL, '').lower()
            )
        ]

        # Sort results
        try:
            sorted_emails = sorted(
                filtered_emails, 
                key=lambda e: e.get(FIELD_TIME, e.get(FIELD_CREATED_AT, '')), 
                reverse=True
            )
        except TypeError:
            logger.warning(f"Sorting search results by {FIELD_TIME} failed. Using '{FIELD_CREATED_AT}'.")
            sorted_emails = sorted(
                filtered_emails, 
                key=lambda e: e.get(FIELD_CREATED_AT, ''), 
                reverse=True
            )

        paginated_emails = sorted_emails[:limit]  # Simple slicing for limit, no offset for basic search

        # Add category details and parse JSON fields
        result_emails = []
        for email in paginated_emails:
            result_emails.append(self._add_category_details(email))
        return result_emails


    async def search_emails_by_category(self, search_term: str, category_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """Search emails within a specific category."""
        if not search_term:
            return await self.get_emails_by_category(category_id, limit=limit)

        search_term_lower = search_term.lower()

        # First, filter by category
        category_emails = [
            email for email in self.emails_data if email.get(FIELD_CATEGORY_ID) == category_id
        ]

        # Then, filter by search term
        filtered_emails = [
            email for email in category_emails
            if (search_term_lower in email.get(FIELD_SUBJECT, '').lower() or
                (isinstance(email.get(FIELD_CONTENT), str) and
                 search_term_lower in email.get(FIELD_CONTENT, '').lower()) or
                search_term_lower in email.get(FIELD_SENDER, '').lower() or
                search_term_lower in email.get(FIELD_SENDER_EMAIL, '').lower()
            )
        ]

        # Sort results
        try:
            sorted_emails = sorted(
                filtered_emails,
                key=lambda e: e.get(FIELD_TIME, e.get(FIELD_CREATED_AT, '')),
                reverse=True
            )
        except TypeError:
            logger.warning(f"Sorting search results by {FIELD_TIME} failed. Using '{FIELD_CREATED_AT}'.")
            sorted_emails = sorted(
                filtered_emails,
                key=lambda e: e.get(FIELD_CREATED_AT, ''),
                reverse=True
            )

        paginated_emails = sorted_emails[:limit]

        # Add category details
        result_emails = []
        for email in paginated_emails:
            result_emails.append(self._add_category_details(email))
        return result_emails


    async def get_recent_emails(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent emails for analysis, ordered by reception time."""
        return await self.get_emails(limit=limit, offset=0)

    async def update_email(
        self, email_id: int, update_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Update email by its internal ID."""
        email_to_update = await self.get_email_by_id(email_id)  # This already fetches category details
        if not email_to_update:
            logger.warning(f"Email with {FIELD_ID} {email_id} not found for update.")
            return None

        original_category_id = email_to_update.get(FIELD_CATEGORY_ID)
        changed_fields = False

        for key, value in update_data.items():
            if key == FIELD_ID:
                continue  # Cannot change id

            if key == "is_read":
                if email_to_update.get(FIELD_IS_UNREAD) == value:  # is_read=True means is_unread=False
                    email_to_update[FIELD_IS_UNREAD] = not value
                    changed_fields = True
            elif key == FIELD_ANALYSIS_METADATA:
                if isinstance(value, str):
                    try:
                        value = json.loads(value)
                    except json.JSONDecodeError:
                        logger.warning(f"Invalid JSON string for {FIELD_ANALYSIS_METADATA}: {value}")
                        value = email_to_update.get(key, {})
                if email_to_update.get(key) != value:
                    email_to_update[key] = value
                    changed_fields = True
            elif key in email_to_update:
                if email_to_update.get(key) != value:
                    email_to_update[key] = value
                    changed_fields = True
            else:
                # Add as new field if it's not a known protected field
                if key not in [FIELD_CREATED_AT, FIELD_UPDATED_AT]:
                    email_to_update[key] = value
                    changed_fields = True
                    logger.info(f"Added new field '{key}' to email ID {email_id} during update_email")

        if changed_fields:
            email_to_update[FIELD_UPDATED_AT] = datetime.now(timezone.utc).isoformat()
            # Find the index and update in self.emails_data
            idx = next((i for i, email in enumerate(self.emails_data) if email.get(FIELD_ID) == email_id), -1)
            if idx != -1:
                self.emails_data[idx] = email_to_update
                await self._save_data(DATA_TYPE_EMAILS)

                new_category_id = email_to_update.get(FIELD_CATEGORY_ID)
                if original_category_id != new_category_id:
                    if original_category_id is not None:
                        await self._update_category_count(original_category_id, decrement=True)
                    if new_category_id is not None:
                        await self._update_category_count(new_category_id, increment=True)
            else:
                logger.error(f"Email with ID {email_id} not found in self.emails_data for update.")
                return None

        return self._add_category_details(email_to_update)

    # --- User methods (basic implementation for future use) ---
    async def create_user(self, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not user_data.get("username"):  # Basic validation
            logger.error("Username is required to create a user.")
            return None

        existing_user = await self.get_user_by_username(user_data["username"])
        if existing_user:
            logger.warning(f"User with username '{user_data['username']}' already exists.")
            return existing_user

        new_id = self._generate_id(self.users_data)
        now = datetime.now(timezone.utc).isoformat()
        user_record = {
            FIELD_ID: new_id,
            FIELD_CREATED_AT: now,
            FIELD_UPDATED_AT: now,
            **user_data  # Spread other user data like username, password_hash, email etc.
        }
        self.users_data.append(user_record)
        await self._save_data(DATA_TYPE_USERS)
        return user_record

    async def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        return next((u for u in self.users_data if u.get('username') == username), None)

    async def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        return next((u for u in self.users_data if u.get(FIELD_ID) == user_id), None)

# Singleton instance
_db_manager_instance = None

async def get_db() -> DatabaseManager:
    """Dependency injection for database. Returns a singleton instance."""
    global _db_manager_instance
    if _db_manager_instance is None:
        _db_manager_instance = DatabaseManager()
        await _db_manager_instance._ensure_initialized()
    return _db_manager_instance
