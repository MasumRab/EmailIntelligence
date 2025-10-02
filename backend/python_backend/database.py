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
    """
    Manages data persistence using JSON files for emails, categories, and users.

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

        self.emails_data: List[Dict[str, Any]] = []
        self.categories_data: List[Dict[str, Any]] = []
        self.users_data: List[Dict[str, Any]] = []

        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
            logger.info(f"Created data directory: {DATA_DIR}")

        self._initialized = False

    async def _ensure_initialized(self) -> None:
        """Ensures that the database has been initialized and data is loaded."""
        if not self._initialized:
            await self._load_data()
            self._initialized = True

    async def _load_data(self) -> None:
        """
        Loads data from JSON files into memory.

        If a data file does not exist, it creates an empty one.
        """
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
                    await self._save_data(data_type)
                    logger.info(f"Created empty data file: {file_path}")
            except (IOError, json.JSONDecodeError) as e:
                logger.error(f"Error loading data from {file_path}: {e}. Initializing with empty list.")
                setattr(self, data_list_attr, [])


    async def _save_data(self, data_type: Literal[DATA_TYPE_EMAILS, DATA_TYPE_CATEGORIES, DATA_TYPE_USERS]) -> None:
        """
        Saves a specific type of in-memory data to its corresponding JSON file.

        Args:
            data_type: The type of data to save ('emails', 'categories', or 'users').
        """
        file_path = ""
        data_to_save: List[Dict[str, Any]] = []

        if data_type == DATA_TYPE_EMAILS:
            file_path = self.emails_file
            data_to_save = self.emails_data
        elif data_type == DATA_TYPE_CATEGORIES:
            file_path = self.categories_file
            data_to_save = self.categories_data
        elif data_type == DATA_TYPE_USERS:
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

    async def initialize(self) -> None:
        """
        Initializes the database, creating the data directory and files if needed.

        If the categories file is empty, it seeds it with default categories.
        """
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
            logger.info(f"Created data directory during initialization: {DATA_DIR}")

        await self._load_data()

        if not self.categories_data:
            for cat_data in DEFAULT_CATEGORIES:
                await self.create_category(cat_data)
            logger.info("Seeded default categories.")


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
        """
        Enriches an email record with its category's name and color.

        Args:
            email: The email record to enrich.

        Returns:
            The enriched email record.
        """
        if not email:
            return email
            
        category_id = email.get(FIELD_CATEGORY_ID)
        if category_id is not None:
            category = next((c for c in self.categories_data if c.get(FIELD_ID) == category_id), None)
            if category:
                email[FIELD_CATEGORY_NAME] = category.get(FIELD_NAME)
                email[FIELD_CATEGORY_COLOR] = category.get(FIELD_COLOR)
                
        return self._parse_json_fields(email, [FIELD_ANALYSIS_METADATA])

    async def create_email(self, email_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Creates a new email record in the database.

        If an email with the same `message_id` already exists, it updates the
        existing record instead.

        Args:
            email_data: A dictionary containing the new email's data.

        Returns:
            The created or updated email record, or None on failure.
        """
        message_id = email_data.get(FIELD_MESSAGE_ID, email_data.get("messageId"))
        existing_email = await self.get_email_by_message_id(message_id)
        if existing_email:
            logger.warning(f"Email with messageId {message_id} already exists. Updating.")
            update_payload = {k: v for k, v in email_data.items()}
            return await self.update_email_by_message_id(message_id, update_payload)

        new_id = self._generate_id(self.emails_data)
        now = datetime.now(timezone.utc).isoformat()

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
            "preview": email_data.get("preview", email_data.get("snippet")),
            "to_addresses": email_data.get("to_addresses", email_data.get("toAddresses", [])),
            "cc_addresses": email_data.get("cc_addresses", email_data.get("ccAddresses", [])),
            "bcc_addresses": email_data.get("bcc_addresses", email_data.get("bccAddresses", [])),
            "reply_to": email_data.get("reply_to", email_data.get("replyTo")),
            "internal_date": email_data.get("internal_date", email_data.get("internalDate")),
            "label_ids": email_data.get("label_ids", email_data.get("labelIds", [])),
            "category": email_data.get("category"),
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
        await self._save_data(DATA_TYPE_EMAILS)

        category_id = email_record.get(FIELD_CATEGORY_ID)
        if category_id is not None:
            await self._update_category_count(category_id)

        return await self.get_email_by_id(new_id)

    async def get_email_by_id(self, email_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieves a single email by its internal database ID.

        Args:
            email_id: The internal ID of the email.

        Returns:
            The email record dictionary, or None if not found.
        """
        email = next((e for e in self.emails_data if e.get(FIELD_ID) == email_id), None)
        if email:
            return self._add_category_details(email)
        return None

    async def get_all_categories(self) -> List[Dict[str, Any]]:
        """
        Retrieves all categories from the database, sorted by name.

        Returns:
            A list of all category record dictionaries.
        """
        return sorted(self.categories_data, key=lambda c: c.get(FIELD_NAME, ''))


    async def create_category(self, category_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Creates a new category.

        If a category with the same name (case-insensitive) already exists,
        it returns the existing one without creating a duplicate.

        Args:
            category_data: A dictionary containing the new category's data.

        Returns:
            The created or existing category record.
        """
        existing_category = next(
            (c for c in self.categories_data 
             if c.get(FIELD_NAME, '').lower() == category_data.get(FIELD_NAME, '').lower()), 
            None
        )
        if existing_category:
            logger.warning(f"Category with name '{category_data.get(FIELD_NAME)}' already exists. Returning existing.")
            return existing_category

        new_id = self._generate_id(self.categories_data)
        category_record = {
            FIELD_ID: new_id,
            FIELD_NAME: category_data[FIELD_NAME],
            "description": category_data.get("description"),
            FIELD_COLOR: category_data.get(FIELD_COLOR, DEFAULT_CATEGORY_COLOR),
            FIELD_COUNT: category_data.get(FIELD_COUNT, 0),
        }
        self.categories_data.append(category_record)
        await self._save_data(DATA_TYPE_CATEGORIES)
        return category_record

    async def _update_category_count(self, category_id: int) -> None:
        """
        Recalculates and updates the email count for a specific category.

        Args:
            category_id: The ID of the category to update.
        """
        category = next((c for c in self.categories_data if c.get(FIELD_ID) == category_id), None)
        if category:
            count = sum(1 for email in self.emails_data if email.get(FIELD_CATEGORY_ID) == category_id)
            if category.get(FIELD_COUNT) != count:
                category[FIELD_COUNT] = count
                await self._save_data(DATA_TYPE_CATEGORIES)
        else:
            logger.warning(f"Attempted to update count for non-existent category ID: {category_id}")


    async def get_emails(
        self,
        limit: int = 50,
        offset: int = 0,
        category_id: Optional[int] = None,
        is_unread: Optional[bool] = None,
    ) -> List[Dict[str, Any]]:
        """
        Retrieves a list of emails with optional filtering and pagination.

        Args:
            limit: The maximum number of emails to return.
            offset: The number of emails to skip from the beginning.
            category_id: If provided, only returns emails from this category.
            is_unread: If provided, filters emails by their read/unread status.

        Returns:
            A list of email record dictionaries.
        """
        filtered_emails = self.emails_data

        if category_id is not None:
            filtered_emails = [e for e in filtered_emails if e.get(FIELD_CATEGORY_ID) == category_id]

        if is_unread is not None:
            filtered_emails = [e for e in filtered_emails if e.get(FIELD_IS_UNREAD) == is_unread]

        try:
            filtered_emails = sorted(
                filtered_emails, 
                key=lambda e: e.get(FIELD_TIME, e.get(FIELD_CREATED_AT, '')), 
                reverse=True
            )
        except TypeError:
            logger.warning(f"Sorting emails by {FIELD_TIME} failed due to incomparable types. Using '{FIELD_CREATED_AT}'.")
            filtered_emails = sorted(
                filtered_emails, 
                key=lambda e: e.get(FIELD_CREATED_AT, ''), 
                reverse=True
            )

        paginated_emails = filtered_emails[offset : offset + limit]

        result_emails = []
        for email in paginated_emails:
            result_emails.append(self._add_category_details(email))
        return result_emails


    async def update_email_by_message_id(
        self, message_id: str, update_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Updates an email record identified by its `message_id`.

        Args:
            message_id: The `message_id` of the email to update.
            update_data: A dictionary of fields to update.

        Returns:
            The updated email record, or None if not found.
        """
        email_to_update = await self.get_email_by_message_id(message_id)
        if not email_to_update:
            logger.warning(f"Email with {FIELD_MESSAGE_ID} {message_id} not found for update.")
            return None

        original_category_id = email_to_update.get(FIELD_CATEGORY_ID)
        changed_fields = False

        for key, value in update_data.items():
            snake_key = key.replace("Id", "_id").replace("Html", "_html").replace("Addresses", "_addresses")
            snake_key = ''.join(['_'+i.lower() if i.isupper() else i for i in snake_key]).lstrip('_')

            if snake_key == FIELD_MESSAGE_ID:
                continue

            if snake_key == "is_read":
                if email_to_update.get(FIELD_IS_UNREAD) == value:
                    email_to_update[FIELD_IS_UNREAD] = not value
                    changed_fields = True
            elif snake_key == FIELD_ANALYSIS_METADATA:
                if isinstance(value, str):
                    try:
                        value = json.loads(value)
                    except json.JSONDecodeError:
                        logger.warning(f"Invalid JSON string for {FIELD_ANALYSIS_METADATA}: {value}")
                        value = email_to_update.get(snake_key, {})
                if email_to_update.get(snake_key) != value:
                    email_to_update[snake_key] = value
                    changed_fields = True
            elif snake_key in email_to_update:
                if email_to_update.get(snake_key) != value:
                    email_to_update[snake_key] = value
                    changed_fields = True
            else:
                known_fields = list(email_to_update.keys())
                if snake_key not in known_fields and key not in [FIELD_ID, FIELD_CREATED_AT, FIELD_UPDATED_AT]:
                    email_to_update[snake_key] = value
                    changed_fields = True
                    logger.info(f"Added new field '{snake_key}' to email {message_id}")

        if changed_fields:
            email_to_update[FIELD_UPDATED_AT] = datetime.now(timezone.utc).isoformat()
            await self._save_data(DATA_TYPE_EMAILS)

            new_category_id = email_to_update.get(FIELD_CATEGORY_ID)
            if original_category_id != new_category_id:
                if original_category_id is not None:
                    await self._update_category_count(original_category_id)
                if new_category_id is not None:
                    await self._update_category_count(new_category_id)

        return await self.get_email_by_id(email_to_update[FIELD_ID])


    async def get_email_by_message_id(self, message_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves a single email by its `message_id`.

        Args:
            message_id: The `message_id` of the email.

        Returns:
            The email record dictionary, or None if not found.
        """
        if not message_id: 
            return None
        email = next((e for e in self.emails_data if e.get(FIELD_MESSAGE_ID) == message_id), None)
        if email:
            return self._add_category_details(email)
        return None

    async def get_all_emails(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Retrieves all emails with pagination.

        Args:
            limit: The maximum number of emails to return.
            offset: The number of emails to skip.

        Returns:
            A list of email record dictionaries.
        """
        return await self.get_emails(limit=limit, offset=offset)

    async def get_emails_by_category(
        self, category_id: int, limit: int = 50, offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Retrieves emails belonging to a specific category.

        Args:
            category_id: The ID of the category to filter by.
            limit: The maximum number of emails to return.
            offset: The number of emails to skip.

        Returns:
            A list of email record dictionaries from the specified category.
        """
        return await self.get_emails(limit=limit, offset=offset, category_id=category_id)

    async def search_emails(self, search_term: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Performs a basic search across all emails.

        The search is a case-insensitive substring match on the subject,
        content, sender, and sender's email address.

        Args:
            search_term: The term to search for.
            limit: The maximum number of search results to return.

        Returns:
            A list of matching email record dictionaries.
        """
        if not search_term:
            return await self.get_emails(limit=limit, offset=0)

        search_term_lower = search_term.lower()
        filtered_emails = [
            email for email in self.emails_data
            if (search_term_lower in email.get(FIELD_SUBJECT, '').lower() or
                (isinstance(email.get(FIELD_CONTENT), str) and 
                 search_term_lower in email.get(FIELD_CONTENT, '').lower()) or
                search_term_lower in email.get(FIELD_SENDER, '').lower() or
                search_term_lower in email.get(FIELD_SENDER_EMAIL, '').lower()
            )
        ]

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

        result_emails = []
        for email in paginated_emails:
            result_emails.append(self._add_category_details(email))
        return result_emails


    async def search_emails_by_category(self, search_term: str, category_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Performs a basic search within a specific category.

        Args:
            search_term: The term to search for.
            category_id: The ID of the category to search within.
            limit: The maximum number of search results to return.

        Returns:
            A list of matching email record dictionaries.
        """
        if not search_term:
            return await self.get_emails_by_category(category_id, limit=limit)

        search_term_lower = search_term.lower()

        category_emails = [
            email for email in self.emails_data if email.get(FIELD_CATEGORY_ID) == category_id
        ]

        filtered_emails = [
            email for email in category_emails
            if (search_term_lower in email.get(FIELD_SUBJECT, '').lower() or
                (isinstance(email.get(FIELD_CONTENT), str) and
                 search_term_lower in email.get(FIELD_CONTENT, '').lower()) or
                search_term_lower in email.get(FIELD_SENDER, '').lower() or
                search_term_lower in email.get(FIELD_SENDER_EMAIL, '').lower()
            )
        ]

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

        result_emails = []
        for email in paginated_emails:
            result_emails.append(self._add_category_details(email))
        return result_emails


    async def get_recent_emails(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Retrieves the most recent emails.

        Args:
            limit: The maximum number of recent emails to return.

        Returns:
            A list of the most recent email record dictionaries.
        """
        return await self.get_emails(limit=limit, offset=0)

    async def update_email(
        self, email_id: int, update_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Updates an email record identified by its internal database ID.

        Args:
            email_id: The internal ID of the email to update.
            update_data: A dictionary of fields to update.

        Returns:
            The updated email record, or None if not found.
        """
        email_to_update = await self.get_email_by_id(email_id)
        if not email_to_update:
            logger.warning(f"Email with {FIELD_ID} {email_id} not found for update.")
            return None

        original_category_id = email_to_update.get(FIELD_CATEGORY_ID)
        changed_fields = False

        for key, value in update_data.items():
            if key == FIELD_ID:
                continue

            if key == "is_read":
                if email_to_update.get(FIELD_IS_UNREAD) == value:
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
                if key not in [FIELD_CREATED_AT, FIELD_UPDATED_AT]:
                    email_to_update[key] = value
                    changed_fields = True
                    logger.info(f"Added new field '{key}' to email ID {email_id} during update_email")

        if changed_fields:
            email_to_update[FIELD_UPDATED_AT] = datetime.now(timezone.utc).isoformat()
            idx = next((i for i, email in enumerate(self.emails_data) if email.get(FIELD_ID) == email_id), -1)
            if idx != -1:
                self.emails_data[idx] = email_to_update
                await self._save_data(DATA_TYPE_EMAILS)

                new_category_id = email_to_update.get(FIELD_CATEGORY_ID)
                if original_category_id != new_category_id:
                    if original_category_id is not None:
                        await self._update_category_count(original_category_id)
                    if new_category_id is not None:
                        await self._update_category_count(new_category_id)
            else:
                logger.error(f"Email with ID {email_id} found by get_email_by_id but not in self.emails_data for update.")
                return None

        updated_email_with_details = await self.get_email_by_id(email_id)
        return updated_email_with_details

    # --- User methods (basic implementation for future use) ---
    async def create_user(self, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Creates a new user.

        Args:
            user_data: A dictionary containing the new user's data.

        Returns:
            The created user record, or the existing record if the user already exists.
        """
        if not user_data.get("username"):
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
            **user_data
        }
        self.users_data.append(user_record)
        await self._save_data(DATA_TYPE_USERS)
        return user_record

    async def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves a user by their username.

        Args:
            username: The username to search for.

        Returns:
            The user record dictionary, or None if not found.
        """
        return next((u for u in self.users_data if u.get('username') == username), None)

    async def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieves a user by their internal database ID.

        Args:
            user_id: The ID of the user.

        Returns:
            The user record dictionary, or None if not found.
        """
        return next((u for u in self.users_data if u.get(FIELD_ID) == user_id), None)

# Singleton instance
_db_manager_instance = None

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
        _db_manager_instance = DatabaseManager()
        await _db_manager_instance.initialize()
    return _db_manager_instance
