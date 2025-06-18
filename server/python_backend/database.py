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

logger = logging.getLogger(__name__)

DATA_DIR = "server/python_backend/data"
EMAILS_FILE = os.path.join(DATA_DIR, "emails.json")
CATEGORIES_FILE = os.path.join(DATA_DIR, "categories.json")
USERS_FILE = os.path.join(DATA_DIR, "users.json") # For future use

class DatabaseManager:
    """Async database manager for email data using JSON file storage."""

    def __init__(self):
        self.emails_file = EMAILS_FILE
        self.categories_file = CATEGORIES_FILE
        self.users_file = USERS_FILE # For future use

        self.emails_data: List[Dict[str, Any]] = []
        self.categories_data: List[Dict[str, Any]] = []
        self.users_data: List[Dict[str, Any]] = [] # For future use

        # Ensure data directory exists
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
            logger.info(f"Created data directory: {DATA_DIR}")

        asyncio.run(self._load_data()) # Load data during initialization

    async def _load_data(self):
        """Loads data from JSON files into memory. Creates files if they don't exist."""
        for data_type, file_path, data_list_attr in [
            ('emails', self.emails_file, 'emails_data'),
            ('categories', self.categories_file, 'categories_data'),
            ('users', self.users_file, 'users_data')
        ]:
            try:
                if os.path.exists(file_path):
                    with open(file_path, 'r') as f:
                        data = await asyncio.to_thread(json.load, f)
                        setattr(self, data_list_attr, data)
                    logger.info(f"Loaded {len(data)} items from {file_path}")
                else:
                    setattr(self, data_list_attr, [])
                    await self._save_data(data_type) # Create file with empty list
                    logger.info(f"Created empty data file: {file_path}")
            except (IOError, json.JSONDecodeError) as e:
                logger.error(f"Error loading data from {file_path}: {e}. Initializing with empty list.")
                setattr(self, data_list_attr, [])


    async def _save_data(self, data_type: Literal['emails', 'categories', 'users']):
        """Saves the specified in-memory data list to its JSON file."""
        file_path = ""
        data_to_save: List[Dict[str, Any]] = []

        if data_type == 'emails':
            file_path = self.emails_file
            data_to_save = self.emails_data
        elif data_type == 'categories':
            file_path = self.categories_file
            data_to_save = self.categories_data
        elif data_type == 'users':
            file_path = self.users_file
            data_to_save = self.users_data
        else:
            logger.error(f"Unknown data type for saving: {data_type}")
            return

        try:
            with open(file_path, 'w') as f:
                await asyncio.to_thread(json.dump, data_to_save, f, indent=4)
            logger.debug(f"Saved {len(data_to_save)} items to {file_path}")
        except IOError as e:
            logger.error(f"Error saving data to {file_path}: {e}")

    def _generate_id(self, data_list: List[Dict[str, Any]]) -> int:
        """Generates a new unique integer ID."""
        if not data_list:
            return 1
        return max(item.get('id', 0) for item in data_list) + 1

    async def initialize(self):
        """
        Initializes the database by ensuring data files and directory exist.
        Default categories can be seeded here if needed.
        """
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
            logger.info(f"Created data directory during initialization: {DATA_DIR}")

        await self._load_data() # Ensure files are loaded/created

        # Example: Seed default categories if categories.json is empty
        if not self.categories_data:
            default_categories = [
                {"name": "Primary", "description": "Default primary category", "color": "#4CAF50", "count": 0},
                {"name": "Promotions", "description": "Promotional emails", "color": "#2196F3", "count": 0},
                {"name": "Social", "description": "Social media notifications", "color": "#FFC107", "count": 0},
                {"name": "Updates", "description": "Updates and notifications", "color": "#9C27B0", "count": 0},
                {"name": "Forums", "description": "Forum discussions", "color": "#795548", "count": 0},
            ]
            for cat_data in default_categories:
                await self.create_category(cat_data)
            logger.info("Seeded default categories.")


    def _parse_json_fields(self, row: Dict[str, Any], fields: List[str]) -> Dict[str, Any]:
        """Helper to parse stringified JSON fields in a row."""
        # This might still be needed if analysisMetadata is stored as a string
        if not row:
            return row
        for field in fields:
            if field in row and isinstance(row[field], str):
                try:
                    row[field] = json.loads(row[field])
                except json.JSONDecodeError:
                    logger.warning(
                        f"Failed to parse JSON for field {field} " f"in row {row.get('id')}"
                    )
                    if field in ("analysisMetadata", "metadata"): # "metadata" for compatibility
                        row[field] = {}
                    else:
                        row[field] = []
        return row

    async def create_email(self, email_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new email record."""
        # Check for existing email by message_id
        existing_email = await self.get_email_by_message_id(email_data.get("message_id", email_data.get("messageId")))
        if existing_email:
            logger.warning(f"Email with messageId {email_data.get('message_id', email_data.get('messageId'))} already exists. Updating.")
            # Convert camelCase to snake_case for update_data if necessary
            update_payload = {k: v for k, v in email_data.items()} # Assuming update_email_by_message_id handles keys
            return await self.update_email_by_message_id(email_data.get("message_id", email_data.get("messageId")), update_payload)

        new_id = self._generate_id(self.emails_data)
        now = datetime.now(timezone.utc).isoformat()

        # Ensure analysisMetadata is a dict, not a string, before storing
        analysis_metadata = email_data.get("analysis_metadata", email_data.get("analysisMetadata", {}))
        if isinstance(analysis_metadata, str):
            try:
                analysis_metadata = json.loads(analysis_metadata)
            except json.JSONDecodeError:
                logger.warning("Failed to parse analysis_metadata string, defaulting to {}")
                analysis_metadata = {}

        email_record = {
            "id": new_id,
            "message_id": email_data.get("message_id", email_data.get("messageId")),
            "thread_id": email_data.get("thread_id", email_data.get("threadId")),
            "subject": email_data.get("subject"),
            "sender": email_data.get("sender"),
            "sender_email": email_data.get("sender_email", email_data.get("senderEmail")),
            "content": email_data.get("content"),
            "snippet": email_data.get("snippet"),
            "labels": email_data.get("labels", []),
            "time": email_data.get("time", email_data.get("timestamp", now)),
            "is_unread": not email_data.get("is_read", False),
            "category_id": email_data.get("category_id", email_data.get("categoryId")),
            "confidence": email_data.get("confidence", 0),
            "analysis_metadata": analysis_metadata,
            "created_at": now,
            "updated_at": now,
            "history_id": email_data.get("history_id", email_data.get("historyId")),
            "content_html": email_data.get("content_html", email_data.get("contentHtml")),
            "preview": email_data.get("preview", email_data.get("snippet")), # Using snippet as fallback
            "to_addresses": email_data.get("to_addresses", email_data.get("toAddresses", [])),
            "cc_addresses": email_data.get("cc_addresses", email_data.get("ccAddresses", [])),
            "bcc_addresses": email_data.get("bcc_addresses", email_data.get("bccAddresses", [])),
            "reply_to": email_data.get("reply_to", email_data.get("replyTo")),
            "internal_date": email_data.get("internal_date", email_data.get("internalDate")),
            "label_ids": email_data.get("label_ids", email_data.get("labelIds", [])),
            "category": email_data.get("category"), # This might be redundant if category_id is used
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
        await self._save_data('emails')

        category_id = email_record.get("category_id")
        if category_id is not None: # Ensure category_id can be 0
            await self._update_category_count(category_id)

        return await self.get_email_by_id(new_id) # Fetch with category details

    async def get_email_by_id(self, email_id: int) -> Optional[Dict[str, Any]]:
        """Get email by ID."""
        email = next((e for e in self.emails_data if e.get('id') == email_id), None)
        if email:
            # Add category details if category_id exists
            category_id = email.get("category_id")
            if category_id is not None:
                category = next((c for c in self.categories_data if c.get('id') == category_id), None)
                if category:
                    email["categoryName"] = category.get("name")
                    email["categoryColor"] = category.get("color")
            return self._parse_json_fields(email, ["analysis_metadata"]) # Ensure analysis_metadata is parsed
        return None

    async def get_all_categories(self) -> List[Dict[str, Any]]:
        """Get all categories with their counts."""
        # Sort categories by name before returning
        return sorted(self.categories_data, key=lambda c: c.get('name', ''))


    async def create_category(self, category_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new category."""
        # Check if category with the same name already exists
        existing_category = next((c for c in self.categories_data if c.get('name', '').lower() == category_data.get('name', '').lower()), None)
        if existing_category:
            logger.warning(f"Category with name '{category_data.get('name')}' already exists. Returning existing.")
            return existing_category # Or update, or raise error, depending on desired behavior

        new_id = self._generate_id(self.categories_data)
        category_record = {
            "id": new_id,
            "name": category_data["name"],
            "description": category_data.get("description"),
            "color": category_data.get("color", "#6366f1"), # Default color
            "count": category_data.get("count", 0),
        }
        self.categories_data.append(category_record)
        await self._save_data('categories')
        return category_record

    async def _update_category_count(self, category_id: int):
        """Update category email count."""
        category = next((c for c in self.categories_data if c.get('id') == category_id), None)
        if category:
            count = sum(1 for email in self.emails_data if email.get('category_id') == category_id)
            if category.get('count') != count:
                 category['count'] = count
                 await self._save_data('categories')
        else:
            logger.warning(f"Attempted to update count for non-existent category ID: {category_id}")


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
            filtered_emails = [e for e in filtered_emails if e.get('category_id') == category_id]

        if is_unread is not None:
            filtered_emails = [e for e in filtered_emails if e.get('is_unread') == is_unread]

        # Sort by time descending (assuming 'time' is a comparable string like ISO format or timestamp)
        # More robust sorting would convert 'time' to datetime objects
        try:
            # Attempt to sort by 'time' if it exists and is valid.
            # Fallback to 'created_at' or no sort if 'time' is problematic.
            filtered_emails = sorted(filtered_emails, key=lambda e: e.get('time', e.get('created_at', '')), reverse=True)
        except TypeError: # Handles cases where 'time' might be None or not comparable
            logger.warning("Sorting emails by time failed due to incomparable types. Using 'created_at'.")
            filtered_emails = sorted(filtered_emails, key=lambda e: e.get('created_at', ''), reverse=True)


        paginated_emails = filtered_emails[offset : offset + limit]

        # Add category details and parse JSON fields
        result_emails = []
        for email in paginated_emails:
            cat_id = email.get("category_id")
            if cat_id is not None:
                category = next((c for c in self.categories_data if c.get('id') == cat_id), None)
                if category:
                    email["categoryName"] = category.get("name")
                    email["categoryColor"] = category.get("color")
            result_emails.append(self._parse_json_fields(email, ["analysis_metadata"]))
        return result_emails


    async def update_email_by_message_id(
        self, message_id: str, update_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Update email by messageId."""
        email_to_update = await self.get_email_by_message_id(message_id)
        if not email_to_update:
            logger.warning(f"Email with message_id {message_id} not found for update.")
            return None

        original_category_id = email_to_update.get("category_id")
        changed_fields = False

        for key, value in update_data.items():
            # Normalize keys (e.g. messageId -> message_id)
            snake_key = key.replace("Id", "_id").replace("Html", "_html").replace("Addresses", "_addresses")
            snake_key = ''.join(['_'+i.lower() if i.isupper() else i for i in snake_key]).lstrip('_')


            if snake_key == "message_id": continue # Cannot change message_id

            if snake_key == "is_read":
                if email_to_update.get("is_unread") == value: # is_read=True means is_unread=False
                    email_to_update["is_unread"] = not value
                    changed_fields = True
            elif snake_key == "analysis_metadata":
                if isinstance(value, str):
                    try:
                        value = json.loads(value)
                    except json.JSONDecodeError:
                        logger.warning(f"Invalid JSON string for analysis_metadata: {value}")
                        value = email_to_update.get(snake_key, {}) # Keep old if new is invalid
                if email_to_update.get(snake_key) != value:
                    email_to_update[snake_key] = value
                    changed_fields = True
            elif snake_key in email_to_update: # Check if the key exists in the email dict
                if email_to_update.get(snake_key) != value:
                    email_to_update[snake_key] = value
                    changed_fields = True
            else:
                # If the key doesn't exist, it might be a new field or a typo
                # For now, we'll add it if it's not a known field to ignore
                # This part might need refinement based on strictness of schema
                known_fields = list(email_to_update.keys()) # Get all current fields
                if snake_key not in known_fields and key not in ["id", "created_at", "updated_at"]: # don't add these
                     email_to_update[snake_key] = value # Add as new field
                     changed_fields = True
                     logger.info(f"Added new field '{snake_key}' to email {message_id}")


        if changed_fields:
            email_to_update["updated_at"] = datetime.now(timezone.utc).isoformat()
            await self._save_data('emails')

            new_category_id = email_to_update.get("category_id")
            if original_category_id != new_category_id:
                if original_category_id is not None:
                    await self._update_category_count(original_category_id)
                if new_category_id is not None:
                    await self._update_category_count(new_category_id)

        return await self.get_email_by_id(email_to_update["id"]) # Fetch with category details


    async def get_email_by_message_id(self, message_id: str) -> Optional[Dict[str, Any]]:
        """Get email by messageId"""
        if not message_id: return None
        email = next((e for e in self.emails_data if e.get('message_id') == message_id), None)
        if email:
            # Add category details
            category_id = email.get("category_id")
            if category_id is not None:
                category = next((c for c in self.categories_data if c.get('id') == category_id), None)
                if category:
                    email["categoryName"] = category.get("name")
                    email["categoryColor"] = category.get("color")
            return self._parse_json_fields(email, ["analysis_metadata"])
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
        # Filter by subject or content
        # A more sophisticated search might involve splitting terms, checking sender, etc.
        # For now, simple substring match on subject and content.
        # Also, ensure content is string before .lower()
        filtered_emails = [
            email for email in self.emails_data
            if (search_term_lower in email.get('subject', '').lower() or
                (isinstance(email.get('content'), str) and search_term_lower in email.get('content', '').lower()) or
                search_term_lower in email.get('sender', '').lower() or # Also search sender
                search_term_lower in email.get('sender_email', '').lower() # And sender email
            )
        ]

        # Sort results
        try:
            sorted_emails = sorted(filtered_emails, key=lambda e: e.get('time', e.get('created_at','')), reverse=True)
        except TypeError:
            logger.warning("Sorting search results by time failed. Using 'created_at'.")
            sorted_emails = sorted(filtered_emails, key=lambda e: e.get('created_at',''), reverse=True)

        paginated_emails = sorted_emails[:limit] # Simple slicing for limit, no offset for basic search

        # Add category details and parse JSON fields
        result_emails = []
        for email in paginated_emails:
            cat_id = email.get("category_id")
            if cat_id is not None:
                category = next((c for c in self.categories_data if c.get('id') == cat_id), None)
                if category:
                    email["categoryName"] = category.get("name")
                    email["categoryColor"] = category.get("color")
            result_emails.append(self._parse_json_fields(email, ["analysis_metadata"]))
        return result_emails


    async def get_recent_emails(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent emails for analysis, ordered by reception time."""
        return await self.get_emails(limit=limit, offset=0)

    async def update_email(
        self, email_id: int, update_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Update email by its internal ID."""
        email_to_update = await self.get_email_by_id(email_id) # This already fetches category details
        if not email_to_update:
            logger.warning(f"Email with id {email_id} not found for update.")
            return None

        original_category_id = email_to_update.get("category_id")
        changed_fields = False

        for key, value in update_data.items():
            if key == "id": continue # Cannot change id

            if key == "is_read":
                if email_to_update.get("is_unread") == value: # is_read=True means is_unread=False
                    email_to_update["is_unread"] = not value
                    changed_fields = True
            elif key == "analysis_metadata":
                if isinstance(value, str):
                    try:
                        value = json.loads(value)
                    except json.JSONDecodeError:
                        logger.warning(f"Invalid JSON string for analysis_metadata: {value}")
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
                 if key not in ["created_at", "updated_at"]:
                    email_to_update[key] = value
                    changed_fields = True
                    logger.info(f"Added new field '{key}' to email ID {email_id} during update_email")


        if changed_fields:
            email_to_update["updated_at"] = datetime.now(timezone.utc).isoformat()
            # Find the index and update in self.emails_data
            idx = next((i for i, email in enumerate(self.emails_data) if email.get('id') == email_id), -1)
            if idx != -1:
                self.emails_data[idx] = email_to_update
                await self._save_data('emails')

                new_category_id = email_to_update.get("category_id")
                if original_category_id != new_category_id:
                    if original_category_id is not None:
                        await self._update_category_count(original_category_id)
                    if new_category_id is not None:
                        await self._update_category_count(new_category_id)
            else: # Should not happen if get_email_by_id found it
                logger.error(f"Email with ID {email_id} found by get_email_by_id but not in self.emails_data for update.")
                return None

        # Return the updated email, ensuring category name/color are fresh
        updated_email_with_details = await self.get_email_by_id(email_id)
        return updated_email_with_details

    # --- User methods (basic implementation for future use) ---
    async def create_user(self, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not user_data.get("username"): # Basic validation
            logger.error("Username is required to create a user.")
            return None

        existing_user = await self.get_user_by_username(user_data["username"])
        if existing_user:
            logger.warning(f"User with username '{user_data['username']}' already exists.")
            return existing_user

        new_id = self._generate_id(self.users_data)
        now = datetime.now(timezone.utc).isoformat()
        user_record = {
            "id": new_id,
            "created_at": now,
            "updated_at": now,
            **user_data # Spread other user data like username, password_hash, email etc.
        }
        self.users_data.append(user_record)
        await self._save_data('users')
        return user_record

    async def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        return next((u for u in self.users_data if u.get('username') == username), None)

    async def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        return next((u for u in self.users_data if u.get('id') == user_id), None)

_db_manager_instance = None

async def get_db() -> DatabaseManager:
    """Dependency injection for database. Returns a singleton instance."""
    global _db_manager_instance
    if _db_manager_instance is None:
        _db_manager_instance = DatabaseManager()
        await _db_manager_instance.initialize() # Ensure it's initialized
    return _db_manager_instance

[end of server/python_backend/database.py]
