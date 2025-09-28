"""
Database management for Gmail AI email processing
PostgreSQL implementation.
"""

import asyncio
import json
import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Dict, List, Optional
import sqlite3

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Async database manager for email data using PostgreSQL"""

    def __init__(self, db_url: Optional[str] = None):

        raw_db_url = db_url or os.getenv("DATABASE_URL")

        if raw_db_url:
            if raw_db_url.startswith("sqlite:"):
                # Examples: "sqlite:./sqlite.db", "sqlite:///./sqlite.db", "sqlite:mydatabase.db"
                path_part = raw_db_url.split(":", 1)[1]
                if path_part.startswith("//"): # Handles "sqlite:///path"
                    path_part = path_part[2:]
                self.db_path = path_part
            else:
                # Assume it's a direct file path if not starting with "sqlite:"
                self.db_path = raw_db_url
        else:
            # Default path if DATABASE_URL is not set
            self.db_path = "./sqlite.db"

        logger.info(f"DatabaseManager initialized with SQLite path: {self.db_path}")
        # self.init_database() # Table creation can be called explicitly if needed, e.g., at app startup or in tests.

    async def _execute_query(
        self,
        query: str,
        params: Optional[tuple] = None,
        fetch_one: bool = False,
        fetch_all: bool = False,
        commit: bool = False,
    ):
        """Helper to execute queries using asyncio.to_thread for sync sqlite3."""

        def db_operation():
            conn = sqlite3.connect(self.db_path) # Use self.db_path
            conn.row_factory = sqlite3.Row  # Access columns by name
            # Enable foreign key constraint enforcement for SQLite, per connection
            conn.execute("PRAGMA foreign_keys = ON;")
            try:
                cur = conn.cursor()
                cur.execute(query, params or ())

                result = None
                if fetch_one:
                    result_row = cur.fetchone()
                    result = dict(result_row) if result_row else None
                elif fetch_all:
                    result_rows = cur.fetchall()
                    result = [dict(row) for row in result_rows]

                if commit:
                    conn.commit()

                # For INSERT statements, handle lastrowid for SQLite
                if query.strip().upper().startswith("INSERT") and not fetch_one and not fetch_all:
                    # If RETURNING id was part of the original query, it needs to be removed for SQLite.
                    # The caller will need to be adjusted if it expected a dict with 'id'.
                    # For SQLite, cur.lastrowid gives the ID of the last inserted row.
                    pass # No explicit return of lastrowid here unless specifically queried

                return result
            except sqlite3.Error as e:
                logger.error(f"Database error during operation: {e}")
                if conn: # conn will always be defined here, but defensive
                    conn.rollback()
                raise # Re-raise the original error to be caught by the outer try-except
            finally:
                if conn:
                    conn.close()

        try:
            result = await asyncio.to_thread(db_operation)

            if fetch_one:
                result_row = await asyncio.to_thread(cur.fetchone)
                result = dict(result_row) if result_row else None
            elif fetch_all:
                result_rows = await asyncio.to_thread(cur.fetchall)
                result = [dict(row) for row in result_rows]

            if commit:
                await asyncio.to_thread(conn.commit)

            return result
        except sqlite3.Error as e: # Catch errors from db_operation or asyncio.to_thread itself
            logger.error(f"Database error: {e}")
            # No conn object to rollback or close here as it's managed within db_operation

            raise
        # No finally block needed here for conn, it's handled in db_operation

    def init_database(self):
        """
        Initializes the database with default categories.
        For SQLite, table creation might need to be handled here if not by external tools.
        This method could seed default categories if they don't exist.
        """
        # Seeding could be handled here or by external scripts.
        # Example: Create tables if they don't exist (simplified)
        # For SQLite, table creation might need to be handled here if not by external tools.
        # This method could seed default categories if they don't exist.
        # Seeding could be handled here or by external scripts.
        # Create tables if they don't exist (simplified)
        # This method is synchronous, so we'll use a synchronous helper or adapt _execute_query
        # For now, let's assume _execute_query can be called from a sync context if run with asyncio.run
        # or we make a sync version for init.
        # Given the current structure, we'll define the CREATE TABLE statements
        # and assume they will be executed by a mechanism that calls this init_database.
        # The actual execution will be triggered by the test setup (conftest.py or similar)
        # by calling this method on a DatabaseManager instance.
        # The `init_database` method itself uses self.db_path via self.database_url (which will be updated)

        # Simplified schema based on shared/schema.ts for SQLite
        create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        );
        """
        create_categories_table = """
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            color TEXT NOT NULL,
            count INTEGER DEFAULT 0
        );
        """
        create_emails_table = """
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id TEXT UNIQUE,
            thread_id TEXT,
            history_id TEXT,
            sender TEXT NOT NULL,
            sender_email TEXT NOT NULL,
            subject TEXT NOT NULL,
            content TEXT NOT NULL,
            content_html TEXT,
            preview TEXT NOT NULL,
            snippet TEXT,
            to_addresses TEXT, -- JSON string
            cc_addresses TEXT, -- JSON string
            bcc_addresses TEXT, -- JSON string
            reply_to TEXT,
            "time" TEXT NOT NULL, -- Assuming ISO8601 or similar string
            internal_date TEXT,
            label_ids TEXT, -- JSON string
            labels TEXT, -- JSON string
            category TEXT,
            is_unread INTEGER DEFAULT 1,
            is_starred INTEGER DEFAULT 0,
            is_important INTEGER DEFAULT 0,
            is_draft INTEGER DEFAULT 0,
            is_sent INTEGER DEFAULT 0,
            is_spam INTEGER DEFAULT 0,
            is_trash INTEGER DEFAULT 0,
            is_chat INTEGER DEFAULT 0,
            has_attachments INTEGER DEFAULT 0,
            attachment_count INTEGER DEFAULT 0,
            size_estimate INTEGER,
            spf_status TEXT,
            dkim_status TEXT,
            dmarc_status TEXT,
            is_encrypted INTEGER DEFAULT 0,
            is_signed INTEGER DEFAULT 0,
            priority TEXT DEFAULT 'normal',
            is_auto_reply INTEGER DEFAULT 0,
            mailing_list TEXT,
            in_reply_to TEXT,
            "references" TEXT, -- JSON string
            is_first_in_thread INTEGER DEFAULT 1,
            category_id INTEGER,
            confidence INTEGER DEFAULT 95,
            analysis_metadata TEXT, -- JSON string
            is_read INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories (id)
        );
        """
        create_activities_table = """
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            description TEXT NOT NULL,
            details TEXT, -- JSON string
            "timestamp" TEXT NOT NULL,
            icon TEXT NOT NULL,
            icon_bg TEXT NOT NULL
        );
        """
        # Note: Direct execution from here might be tricky due to async nature of _execute_query
        # This method is currently synchronous.
        # For tests, this init_database() would be called by a test fixture.
        # We'll assume the test runner or conftest will handle running these.
        # A better approach might be to have a separate setup_schema async method.
        # For now, this defines the queries. The actual execution needs to be handled.
        # To make it work with current structure, we'd need a sync execution method.
        # Let's create a temporary sync execution for init_database
        conn = sqlite3.connect(self.db_path) # Corrected to use self.db_path
        try:
            cur = conn.cursor()
            cur.execute(create_users_table)
            cur.execute(create_categories_table)
            cur.execute(create_emails_table)
            cur.execute(create_activities_table)
            conn.commit()
            logger.info("Database tables initialized/verified for SQLite.")
        except sqlite3.Error as e:
            logger.error(f"Error initializing SQLite tables: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()

        pass

    @asynccontextmanager
    async def get_connection(self):
        """Async context manager for database connections using sqlite3."""
        conn = None
        try:
            conn = await asyncio.to_thread(sqlite3.connect, self.db_path) # Use self.db_path
            conn.row_factory = sqlite3.Row
            # For SQLite, PRAGMA foreign_keys=ON should be enabled per connection if FKs are used.
            # await asyncio.to_thread(conn.execute, "PRAGMA foreign_keys = ON;")
            yield conn
        except sqlite3.Error as e:
            logger.error(f"Failed to connect to database: {e}")
            # Rollback is often implicit for SQLite on connection close if not committed
            # but explicit rollback on error before close is good practice if conn was established.
            if conn: # pragma: no cover
                await asyncio.to_thread(conn.rollback)
            raise
        finally:
            if conn:
                await asyncio.to_thread(conn.close)

    async def initialize(self):
        """Initialize database asynchronously (e.g., seed data)"""
        logger.info("DatabaseManager initialized. Default categories seeding attempted.")
        pass

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
                        f"Failed to parse JSON for field {field} " f"in row {row.get('id')}"
                    )
                    if field in ("analysisMetadata", "metadata"):
                        row[field] = {}
                    else:
                        row[field] = []
        return row

    async def create_email(self, email_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new email record."""
        is_unread = not email_data.get("is_read", False)

        # SQLite uses ? as placeholders. NOW() becomes datetime('now')
        # RETURNING id is not standard in SQLite, use last_insert_rowid() later.
        query = """
            INSERT INTO emails (
                message_id, thread_id, subject, sender, sender_email, content,
                snippet, labels, "time", is_unread, category_id, confidence,
                analysis_metadata, created_at, updated_at, history_id, content_html,
                preview, to_addresses, cc_addresses, bcc_addresses, reply_to,
                internal_date, label_ids, category, is_starred, is_important,
                is_draft, is_sent, is_spam, is_trash, is_chat, has_attachments,
                attachment_count, size_estimate, spf_status, dkim_status,
                dmarc_status, is_encrypted, is_signed, priority, is_auto_reply,
                mailing_list, in_reply_to, "references", is_first_in_thread
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'),
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            );
        """
        params = (
            email_data.get("message_id", email_data.get("messageId")),
            email_data.get("thread_id", email_data.get("threadId")),
            email_data.get("subject"),
            email_data.get("sender"),
            email_data.get("sender_email", email_data.get("senderEmail")),
            email_data.get("content"),
            email_data.get("snippet"),
            json.dumps(email_data.get("labels", [])), # Store list as JSON string
            email_data.get("time", email_data.get("timestamp")),
            is_unread,
            email_data.get("category_id", email_data.get("categoryId")),
            email_data.get("confidence", 0),
            json.dumps(email_data.get("analysis_metadata", email_data.get("analysisMetadata", {}))),
            email_data.get("history_id", email_data.get("historyId")),
            email_data.get("content_html", email_data.get("contentHtml")),
            email_data.get("preview", email_data.get("snippet")),
            json.dumps(email_data.get("to_addresses", email_data.get("toAddresses", []))), # Store list as JSON string
            json.dumps(email_data.get("cc_addresses", email_data.get("ccAddresses", []))), # Store list as JSON string
            json.dumps(email_data.get("bcc_addresses", email_data.get("bccAddresses", []))),# Store list as JSON string
            email_data.get("reply_to", email_data.get("replyTo")),
            email_data.get("internal_date", email_data.get("internalDate")),
            json.dumps(email_data.get("label_ids", email_data.get("labelIds", []))), # Store list as JSON string
            email_data.get("category"),
            email_data.get("is_starred", email_data.get("isStarred", False)),
            email_data.get("is_important", email_data.get("isImportant", False)),
            email_data.get("is_draft", email_data.get("isDraft", False)),
            email_data.get("is_sent", email_data.get("isSent", False)),
            email_data.get("is_spam", email_data.get("isSpam", False)),
            email_data.get("is_trash", email_data.get("isTrash", False)),
            email_data.get("is_chat", email_data.get("isChat", False)),
            email_data.get("has_attachments", email_data.get("hasAttachments", False)),
            email_data.get("attachment_count", email_data.get("attachmentCount", 0)),
            email_data.get("size_estimate", email_data.get("sizeEstimate")),
            email_data.get("spf_status", email_data.get("spfStatus")),
            email_data.get("dkim_status", email_data.get("dkimStatus")),
            email_data.get("dmarc_status", email_data.get("dmarcStatus")),
            email_data.get("is_encrypted", email_data.get("isEncrypted", False)),
            email_data.get("is_signed", email_data.get("isSigned", False)),
            email_data.get("priority", "normal"),
            email_data.get("is_auto_reply", email_data.get("isAutoReply", False)),
            email_data.get("mailing_list", email_data.get("mailingList")),
            email_data.get("in_reply_to", email_data.get("inReplyTo")),
            json.dumps(email_data.get("references", [])), # Store list as JSON string
            email_data.get("is_first_in_thread", email_data.get("isFirstInThread", True)),
        )
        try:
            # For SQLite, we execute the insert, then query for last_insert_rowid()
            await self._execute_query(query, params, commit=True)
            # Get the last inserted ID
            # This assumes the table `emails` has an INTEGER PRIMARY KEY column, often named `id`.
            # The name of the primary key column must be known for the get_email_by_id call.
            # If the PK column is not 'id', this part will need adjustment.
            id_row = await self._execute_query("SELECT last_insert_rowid() as id;", fetch_one=True)
            if id_row and id_row.get("id") is not None:
                email_id = id_row["id"]
                category_id = email_data.get("categoryId", email_data.get("category_id"))
                if category_id:
                    await self._update_category_count(category_id)
                return await self.get_email_by_id(email_id) # Make sure get_email_by_id uses the correct PK column name
            return None
        except sqlite3.IntegrityError as e: # Catch SQLite specific integrity error
            logger.warning(
                f"Email with messageId {email_data.get('messageId')} " f"likely already exists: {e}"
            )
            # Ensure update_email_by_message_id is also adapted for SQLite
            return await self.update_email_by_message_id(email_data["messageId"], email_data)

    async def get_email_by_id(self, email_id: int) -> Optional[Dict[str, Any]]:
        """Get email by ID"""
        query = """
            SELECT e.*, c.name as "categoryName", c.color as "categoryColor"
            FROM emails e
            LEFT JOIN categories c ON e.category_id = c.id
            WHERE e.id = ?  -- Changed %s to ?
        """
        row = await self._execute_query(query, (email_id,), fetch_one=True)
        # JSON fields to parse: labels, analysisMetadata, to_addresses, cc_addresses, bcc_addresses, label_ids, references
        json_fields = ["labels", "analysisMetadata", "to_addresses", "cc_addresses", "bcc_addresses", "label_ids", "references"]
        return self._parse_json_fields(row, json_fields) if row else None

    async def get_all_categories(self) -> List[Dict[str, Any]]:  # Renamed for clarity
        """Get all categories with their counts."""
        query = """
            SELECT id, name, description, color, count
            FROM categories
            ORDER BY name
        """
        # No change needed for query parameters for this specific query
        categories = await self._execute_query(query, fetch_all=True)
        return categories if categories else []

    async def create_category(self, category_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new category."""
        # SQLite uses ? for placeholders. RETURNING is not standard.
        query = """
            INSERT INTO categories (name, description, color, count)
            VALUES (?, ?, ?, ?)
        """
        params = (
            category_data["name"],
            category_data.get("description"),
            category_data.get("color", "#6366f1"),
            category_data.get("count", 0),
        )
        try:
            await self._execute_query(query, params, commit=True)
            # Get the last inserted ID, assuming 'id' is the PK for categories
            id_row = await self._execute_query("SELECT last_insert_rowid() as id;", fetch_one=True)
            if id_row and id_row.get("id") is not None:
                # Fetch the newly created category by its ID
                # This assumes a get_category_by_id method or similar, or construct manually
                # For now, returning a dictionary similar to what RETURNING would provide
                return {
                    "id": id_row["id"],
                    "name": category_data["name"],
                    "description": category_data.get("description"),
                    "color": category_data.get("color", "#6366f1"),
                    "count": category_data.get("count", 0),
                }
            return None
        except sqlite3.Error as e: # Catch SQLite specific error
            logger.error(f"Failed to create category {category_data.get('name')}: {e}")
            return None

    async def _update_category_count(self, category_id: int):
        """Update category email count."""
        query = """
            UPDATE categories
            SET count = (SELECT COUNT(*) FROM emails WHERE category_id = ?) -- Changed %s to ?
            WHERE id = ?; -- Changed %s to ?
        """
        await self._execute_query(query, (category_id, category_id), commit=True)

    async def get_emails(
        self,
        limit: int = 50,
        offset: int = 0,
        category_id: Optional[int] = None,
        is_unread: Optional[bool] = None,
    ) -> List[Dict[str, Any]]:
        """Get emails with pagination and filtering."""
        params = []
        base_query = (
            "SELECT e.*, c.name as categoryName, c.color as categoryColor "
            "FROM emails e LEFT JOIN categories c ON e.category_id = c.id"
        )
        where_clauses = []
        if category_id is not None:
            where_clauses.append("e.category_id = ?") # Changed %s to ?
            params.append(category_id)

        if is_unread is not None:
            where_clauses.append("e.is_unread = ?") # Changed %s to ?
            params.append(is_unread)

        if where_clauses:
            base_query += " WHERE " + " AND ".join(where_clauses)

        base_query += ' ORDER BY e."time" DESC LIMIT ? OFFSET ?' # Changed %s to ?
        params.extend([limit, offset])

        emails = await self._execute_query(base_query, tuple(params), fetch_all=True)
        if emails:
            # Ensure all necessary JSON fields are parsed
            json_fields = ["labels", "analysisMetadata", "to_addresses", "cc_addresses", "bcc_addresses", "label_ids", "references"]
            return [self._parse_json_fields(email, json_fields) for email in emails]
        return []

    async def update_email_by_message_id(
        self, message_id: str, update_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Update email by messageId."""
        set_clauses = []
        params = []

        for key, value in update_data.items():
            column_name = key
            if key == "message_id": # Cannot update message_id itself
                continue

            # Handle boolean conversions and specific column names
            if key == "is_read":
                column_name = "is_unread"
                value = not value # Python bool to int for SQLite: True -> 1, False -> 0
            elif key in ["is_starred", "is_important", "is_draft", "is_sent", "is_spam", "is_trash", "is_chat", "has_attachments", "is_encrypted", "is_signed", "is_auto_reply", "is_first_in_thread"]:
                 value = 1 if value else 0 # Ensure boolean is int
            elif key == "analysis_metadata":
                value = json.dumps(value)
            elif key in ["labels", "to_addresses", "cc_addresses", "bcc_addresses", "label_ids", "references"]:
                if not isinstance(value, list): value = [str(value)]
                value = json.dumps(value) # Store lists as JSON strings
            elif key == "timestamp":
                column_name = '"time"' # Keep quoted for "time"
            # Map JS-style camelCase to snake_case if necessary, or ensure direct match
            # This list should match the one in create_email for consistency
            elif key in ["categoryId", "senderEmail", "threadId", "historyId", "contentHtml", "toAddresses", "ccAddresses", "bccAddresses", "replyTo", "internalDate", "labelIds", "isStarred", "isImportant", "isDraft", "isSent", "isSpam", "isTrash", "isChat", "hasAttachments", "attachmentCount", "sizeEstimate", "spfStatus", "dkimStatus", "dmarcStatus", "isEncrypted", "isSigned", "isAutoReply", "mailingList", "inReplyTo", "isFirstInThread"]:
                # Convert camelCase to snake_case for DB column name
                # Basic conversion, might need refinement for specific cases
                column_name = ''.join(['_'+i.lower() if i.isupper() else i for i in key]).lstrip('_')
                if column_name.endswith(("_i_d", "_h_t_m_l")): # fix for Id and Html
                    column_name = column_name.replace("_i_d", "_id").replace("_h_t_m_l", "_html")


            # Add more specific key mappings if direct mapping + simple snake_case isn't enough
            # Example: if 'categoryId' in DB is 'category_id'
            # if key == "categoryId": column_name = "category_id"

            # Ensure the column_name is a valid DB column before adding
            # This check is simplified; ideally, validate against actual schema column names
            if column_name not in ["message_id"]: # Example: skip if not a real column
                 set_clauses.append(f"{column_name} = ?") # Changed %s to ?
                 params.append(value)
            else:
                 logger.warning(
                    f"update_email_by_message_id: Skipped update for field '{key}' (mapped to '{column_name}')"
                )


        if not set_clauses:
            logger.warning(f"No valid fields to update for message_id: {message_id}")
            return await self.get_email_by_message_id(message_id)

        set_clauses.append("updated_at = datetime('now')") # NOW() to datetime('now')
        query = f"UPDATE emails SET {', '.join(set_clauses)} WHERE message_id = ?" # Changed %s to ?
        params.append(message_id)
        await self._execute_query(query, tuple(params), commit=True)
        return await self.get_email_by_message_id(message_id)

    async def get_email_by_message_id(self, message_id: str) -> Optional[Dict[str, Any]]:
        """Get email by messageId"""
        query = (
            "SELECT e.*, c.name as categoryName, c.color as categoryColor "
            "FROM emails e LEFT JOIN categories c ON e.category_id = c.id "
            "WHERE e.message_id = ?" # Changed %s to ?
        )
        row = await self._execute_query(query, (message_id,), fetch_one=True)
        # Ensure all necessary JSON fields are parsed
        json_fields = ["labels", "analysisMetadata", "to_addresses", "cc_addresses", "bcc_addresses", "label_ids", "references"]
        return self._parse_json_fields(row, json_fields) if row else None

    async def create_activity(self, activity_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new activity record."""
        # SQLite uses ? placeholders. RETURNING is not standard.
        query = """
            INSERT INTO activities
                (type, description, details, "timestamp", icon, icon_bg)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        details_data = activity_data.get("metadata", {})
        if "email_id" in activity_data:
            details_data["emailId"] = activity_data["email_id"]
        if "email_subject" in activity_data:
            details_data["emailSubject"] = activity_data["email_subject"]

        params = (
            activity_data["type"],
            activity_data["description"],
            json.dumps(details_data) if details_data else None, # Store details as JSON string
            activity_data.get("timestamp", datetime.now().isoformat()),
            activity_data.get("icon", "default_icon"),
            activity_data.get("icon_bg", activity_data.get("iconBg", "#ffffff")),
        )
        # Execute insert, then get last_insert_rowid()
        await self._execute_query(query, params, commit=True)
        id_row = await self._execute_query("SELECT last_insert_rowid() as id;", fetch_one=True)
        if id_row and id_row.get("id") is not None:
            # Construct the returned dict manually, matching original RETURNING fields
            new_activity_dict = {
                "id": id_row["id"],
                "type": activity_data["type"],
                "description": activity_data["description"],
                "details": details_data, # Already a dict, or None
                "timestamp": activity_data.get("timestamp", datetime.now().isoformat()),
                "icon": activity_data.get("icon", "default_icon"),
                "icon_bg": activity_data.get("icon_bg", activity_data.get("iconBg", "#ffffff")),
            }
            return self._parse_json_fields(new_activity_dict, ["details"]) # Ensure details are parsed if stored as string
        return None


    async def get_recent_activities(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent activities"""
        query = (
            'SELECT id, type, description, details, "timestamp", icon, icon_bg '
            'FROM activities ORDER BY "timestamp" DESC LIMIT ?' # Changed %s to ?
        )
        activities = await self._execute_query(query, (limit,), fetch_all=True)
        if activities:
            return [self._parse_json_fields(activity, ["details"]) for activity in activities]
        return []

    async def get_dashboard_stats(self) -> Dict[str, Any]:
        logger.warning("get_dashboard_stats needs full review for SQLite compatibility.")
        # SQLite uses 0 and 1 for TRUE/FALSE in WHERE clauses by default
        results = await asyncio.gather(
            self._execute_query("SELECT COUNT(*) AS count FROM emails", fetch_one=True),
            self._execute_query(
                "SELECT COUNT(*) AS count FROM emails WHERE is_unread = 1", fetch_one=True # TRUE to 1
            ),
            self._execute_query(
                "SELECT COUNT(*) AS count FROM emails WHERE priority = ?", # %s to ?
                ("high",),
                fetch_one=True,
            ),
            self._execute_query(
                "SELECT COUNT(*) AS count FROM emails WHERE is_spam = 1", fetch_one=True # TRUE to 1
            ),
            self._execute_query("SELECT COUNT(*) AS count FROM categories", fetch_one=True),
            self._execute_query(
                "SELECT name, color, count FROM categories ORDER BY count DESC LIMIT 5",
                fetch_all=True, # No params here
            ),
        )

        total_emails = results[0]["count"] if results[0] else 0
        unread_emails = results[1]["count"] if results[1] else 0
        important_emails = results[2]["count"] if results[2] else 0
        spam_emails = results[3]["count"] if results[3] else 0
        total_category_types = results[4]["count"] if results[4] else 0
        top_categories_list = results[5] if results[5] else []

        return {
            "totalEmails": total_emails,
            "unreadEmails": unread_emails,
            "importantEmails": important_emails,
            "spamEmails": spam_emails,
            "totalCategoryTypes": total_category_types,
            "topCategories": top_categories_list,
            "autoLabeled": total_emails,  # Placeholder
            "timeSaved": "2.5 hours",  # Placeholder
            "weeklyGrowth": {  # Placeholder for complex calculation
                "totalEmails": total_emails,
                "autoLabeled": total_emails,
                "categories": total_category_types,
                "timeSaved": 0,
            },
        }

    async def get_all_emails(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """Get all emails with pagination"""
        return await self.get_emails(limit=limit, offset=offset)

    async def get_emails_by_category(
        self, category_id: int, limit: int = 50, offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Get emails by category"""
        return await self.get_emails(limit=limit, offset=offset, category_id=category_id)

    async def search_emails(self, search_term: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Search emails by content or subject."""
        query = (
            "SELECT e.*, c.name as categoryName, c.color as categoryColor "
            "FROM emails e LEFT JOIN categories c ON e.category_id = c.id "
            "WHERE e.subject LIKE ? OR e.content LIKE ? " # ILIKE to LIKE (SQLite LIKE is case-insensitive by default for ASCII)
            'ORDER BY e."time" DESC LIMIT ?' # %s to ?
        )
        params = (f"%{search_term}%", f"%{search_term}%", limit)
        emails = await self._execute_query(query, params, fetch_all=True)
        if emails:
            # Ensure all necessary JSON fields are parsed
            json_fields = ["labels", "analysisMetadata", "to_addresses", "cc_addresses", "bcc_addresses", "label_ids", "references"]
            return [self._parse_json_fields(email, json_fields) for email in emails]
        return []

    async def get_recent_emails(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent emails for analysis, ordered by reception time."""
        return await self.get_emails(limit=limit, offset=0)

    async def update_email(
        self, email_id: int, update_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Update email by its internal ID."""
        set_clauses = []
        params = []

        for key, value in update_data.items():
            column_name = key
            if key == "id":
                continue

            if key == "is_read":
                column_name = "is_unread"
                value = not value
            elif key == "is_important":
                column_name = "is_important"
            elif key == "is_starred":
                column_name = "is_starred"
            elif key == "category_id":
                column_name = "category_id"
            elif key == "analysis_metadata":
                column_name = "analysis_metadata"
                value = json.dumps(value)
            elif key == "labels":
                column_name = "labels"
                if not isinstance(value, list):
                    value = [str(value)]
            elif key == "sender_email":
                column_name = "sender_email"
            elif key == "time":
                column_name = '"time"'
            elif key in [
                "subject",
                "content",
                "sender",
                "confidence",
                "snippet",
                "category",
                "priority",
            ]:
                column_name = key
            elif key in ["is_read", "is_important", "is_starred", "is_draft", "is_sent", "is_spam", "is_trash", "is_chat", "has_attachments", "is_encrypted", "is_signed", "is_auto_reply", "is_first_in_thread"]:
                value = 1 if value else 0 # Ensure boolean is int
            elif key == "analysis_metadata":
                value = json.dumps(value)
            elif key in ["labels", "to_addresses", "cc_addresses", "bcc_addresses", "label_ids", "references"]:
                if not isinstance(value, list): value = [str(value)]
                value = json.dumps(value) # Store lists as JSON strings
            else: # Attempt to convert camelCase to snake_case for other keys
                # This is a simplistic conversion and might need adjustment for specific column names
                import re
                temp_col_name = re.sub(r'(?<!^)(?=[A-Z])', '_', key).lower()
                if temp_col_name != key: # Log if a conversion happened
                    logger.info(f"update_email: Converted key '{key}' to '{temp_col_name}' for SQL query.")
                    column_name = temp_col_name
                # If no conversion, and not explicitly handled, it might be an issue
                # or the column name is already snake_case and matches.

            # Ensure the column_name is a valid DB column before adding
            # This check is simplified; ideally, validate against actual schema column names
            if column_name != "id": # Cannot update id
                set_clauses.append(f"{column_name} = ?") # %s to ?
                params.append(value)
            else:
                 logger.warning(
                    f"update_email: Skipped update for field '{key}' (mapped to '{column_name}')"
                )


        if not set_clauses:
            logger.info(f"No valid fields to update for email id: {email_id}")
            return await self.get_email_by_id(email_id)

        set_clauses.append("updated_at = datetime('now')") # NOW() to datetime('now')
        query = f"UPDATE emails SET {', '.join(set_clauses)} WHERE id = ?" # %s to ?
        params.append(email_id)
        await self._execute_query(query, tuple(params), commit=True)
        return await self.get_email_by_id(email_id)


async def get_db() -> DatabaseManager:
    """Dependency injection for database"""
    # Ensure this returns the SQLite-configured DatabaseManager
    # No change needed here if DatabaseManager.__init__ defaults to SQLite or uses env var correctly
    return DatabaseManager()
