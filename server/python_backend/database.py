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

import psycopg2
import psycopg2.extras  # For RealDictCursor

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Async database manager for email data using PostgreSQL"""

    def __init__(self, db_url: Optional[str] = None):
        self.database_url = db_url or os.getenv("DATABASE_URL")
        if not self.database_url:
            logger.error("DATABASE_URL environment variable not set.")
            raise ValueError("DATABASE_URL environment variable not set.")
        # self.init_database() # Table creation handled by Drizzle ORM
        # Seeding default data can be done here if needed.

    async def _execute_query(
        self,
        query: str,
        params: Optional[tuple] = None,
        fetch_one: bool = False,
        fetch_all: bool = False,
        commit: bool = False,
    ):
        """Helper to execute queries using asyncio.to_thread for sync psycopg2."""
        conn = await asyncio.to_thread(psycopg2.connect, self.database_url)
        try:
            cursor_factory = psycopg2.extras.RealDictCursor
            async with conn.cursor(cursor_factory=cursor_factory) as cur:
                await asyncio.to_thread(cur.execute, query, params)

                result = None
                if fetch_one:
                    result_row = await asyncio.to_thread(cur.fetchone)
                    result = dict(result_row) if result_row else None
                elif fetch_all:
                    result_rows = await asyncio.to_thread(cur.fetchall)
                    result = [dict(row) for row in result_rows]

                if commit:
                    await asyncio.to_thread(conn.commit)

                if (
                    query.strip().upper().startswith("INSERT")
                    and "RETURNING id" in query.lower()
                    and not result
                ):
                    # If RETURNING id used & fetch_one=False (e.g. for lastrowid).
                    # For psycopg2, RETURNING is standard. If ID needed &
                    # fetch_one=False, assume "INSERT...RETURNING id" and
                    # result should have been fetched.
                    # If fetch_one=True with RETURNING id, 'result' has it.
                    # For lastrowid, prefer RETURNING id and fetch_one.
                    pass

                return result
        except psycopg2.Error as e:
            logger.error(f"Database error: {e}")
            await asyncio.to_thread(conn.rollback)
            raise
        finally:
            await asyncio.to_thread(conn.close)

    def init_database(self):
        """
        Initializes the database with default categories.
        Table creation is assumed to be handled by Drizzle migrations.
        This method now only seeds default categories if they don't exist.
        """
        # Seeding is handled by the TypeScript side / Drizzle migrations.
        pass

    @asynccontextmanager
    async def get_connection(self):
        """Async context manager for database connections using psycopg2."""
        conn = None
        try:
            conn = await asyncio.to_thread(psycopg2.connect, self.database_url)
            conn.autocommit = False  # Ensure transactions are handled explicitly
            yield conn
        except psycopg2.Error as e:
            logger.error(f"Failed to connect to database: {e}")
            if conn:  # pragma: no cover
                await asyncio.to_thread(conn.rollback)
            raise
        finally:
            if conn:
                await asyncio.to_thread(conn.close)

    async def initialize(self):
        """Initialize database asynchronously (e.g., seed data)"""
        logger.info(
            "DatabaseManager initialized. Default categories seeding attempted."
        )
        pass

    def _parse_json_fields(
        self, row: Dict[str, Any], fields: List[str]
    ) -> Dict[str, Any]:
        """Helper to parse stringified JSON fields in a row."""
        if not row:
            return row
        for field in fields:
            if field in row and isinstance(row[field], str):
                try:
                    row[field] = json.loads(row[field])
                except json.JSONDecodeError:
                    logger.warning(
                        f"Failed to parse JSON for field {field} "
                        f"in row {row.get('id')}"
                    )
                    if field in ("analysisMetadata", "metadata"):
                        row[field] = {}
                    else:
                        row[field] = []
        return row

    async def create_email(
        self, email_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Create a new email record."""
        is_unread = not email_data.get("is_read", False)

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
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW(),
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            ) RETURNING id;
        """
        params = (
            email_data.get("message_id", email_data.get("messageId")),
            email_data.get("thread_id", email_data.get("threadId")),
            email_data.get("subject"),
            email_data.get("sender"),
            email_data.get("sender_email", email_data.get("senderEmail")),
            email_data.get("content"),
            email_data.get("snippet"),
            email_data.get("labels", []),
            email_data.get("time", email_data.get("timestamp")),
            is_unread,
            email_data.get("category_id", email_data.get("categoryId")),
            email_data.get("confidence", 0),
            json.dumps(email_data.get("analysis_metadata",
                                      email_data.get("analysisMetadata", {}))),
            email_data.get("history_id", email_data.get("historyId")),
            email_data.get("content_html", email_data.get("contentHtml")),
            email_data.get("preview", email_data.get("snippet")),
            email_data.get("to_addresses", email_data.get("toAddresses", [])),
            email_data.get("cc_addresses", email_data.get("ccAddresses", [])),
            email_data.get("bcc_addresses", email_data.get("bccAddresses", [])),
            email_data.get("reply_to", email_data.get("replyTo")),
            email_data.get("internal_date", email_data.get("internalDate")),
            email_data.get("label_ids", email_data.get("labelIds", [])),
            email_data.get("category"),
            email_data.get("is_starred", email_data.get("isStarred", False)),
            email_data.get("is_important", email_data.get("isImportant", False)),
            email_data.get("is_draft", email_data.get("isDraft", False)),
            email_data.get("is_sent", email_data.get("isSent", False)),
            email_data.get("is_spam", email_data.get("isSpam", False)),
            email_data.get("is_trash", email_data.get("isTrash", False)),
            email_data.get("is_chat", email_data.get("isChat", False)),
            email_data.get("has_attachments",
                           email_data.get("hasAttachments", False)),
            email_data.get("attachment_count",
                           email_data.get("attachmentCount", 0)),
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
            email_data.get("references", []),
            email_data.get("is_first_in_thread",
                           email_data.get("isFirstInThread", True)),
        )
        try:
            result = await self._execute_query(
                query, params, fetch_one=True, commit=True
            )
            if result and result.get("id"):
                email_id = result["id"]
                category_id = email_data.get(
                    "categoryId", email_data.get("category_id")
                )
                if category_id:
                    await self._update_category_count(category_id)
                return await self.get_email_by_id(email_id)
            return None
        except psycopg2.IntegrityError as e:
            logger.warning(
                f"Email with messageId {email_data.get('messageId')} "
                f"likely already exists: {e}"
            )
            return await self.update_email_by_message_id(
                email_data["messageId"], email_data
            )

    async def get_email_by_id(self, email_id: int) -> Optional[Dict[str, Any]]:
        """Get email by ID"""
        query = """
            SELECT e.*, c.name as "categoryName", c.color as "categoryColor"
            FROM emails e
            LEFT JOIN categories c ON e.category_id = c.id
            WHERE e.id = %s
        """
        row = await self._execute_query(query, (email_id,), fetch_one=True)
        return self._parse_json_fields(row, ["analysisMetadata"]) if row else None

    async def get_all_categories(self) -> List[Dict[str, Any]]: # Renamed for clarity
        """Get all categories with their counts."""
        query = """
            SELECT id, name, description, color, count
            FROM categories
            ORDER BY name
        """
        categories = await self._execute_query(query, fetch_all=True)
        return categories if categories else []

    async def create_category(
        self, category_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Create a new category."""
        query = """
            INSERT INTO categories (name, description, color, count)
            VALUES (%s, %s, %s, %s)
            RETURNING id, name, description, color, count;
        """
        params = (
            category_data["name"],
            category_data.get("description"),
            category_data.get("color", "#6366f1"),
            category_data.get("count", 0),
        )
        try:
            new_category = await self._execute_query(
                query, params, fetch_one=True, commit=True
            )
            return new_category
        except psycopg2.Error as e:
            logger.error(f"Failed to create category {category_data.get('name')}: {e}")
            return None

    async def _update_category_count(self, category_id: int):
        """Update category email count."""
        query = """
            UPDATE categories
            SET count = (SELECT COUNT(*) FROM emails WHERE category_id = %s)
            WHERE id = %s;
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
            where_clauses.append("e.category_id = %s")
            params.append(category_id)

        if is_unread is not None:
            where_clauses.append("e.is_unread = %s")
            params.append(is_unread)

        if where_clauses:
            base_query += " WHERE " + " AND ".join(where_clauses)

        base_query += ' ORDER BY e."time" DESC LIMIT %s OFFSET %s'
        params.extend([limit, offset])

        emails = await self._execute_query(base_query, tuple(params), fetch_all=True)
        if emails:
            return [
                self._parse_json_fields(email, ["analysisMetadata"])
                for email in emails
            ]
        return []

    async def update_email_by_message_id(
        self, message_id: str, update_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Update email by messageId."""
        set_clauses = []
        params = []

        for key, value in update_data.items():
            column_name = key
            if key == "message_id":
                continue
            if key == "is_read":
                column_name = "is_unread"
                value = not value
            elif key == "category_id":
                column_name = "category_id"
            elif key == "sender_email":
                column_name = "sender_email"
            elif key == "thread_id":
                column_name = "thread_id"
            elif key == "analysis_metadata":
                column_name = "analysis_metadata"
                value = json.dumps(value)
            elif key == "labels":
                column_name = "labels"
                if not isinstance(value, list):
                    logger.warning(
                        f"Labels value for update is not a list: {value}, "
                        "attempting to wrap."
                    )
                    value = [str(value)]
            elif key == "timestamp":
                column_name = '"time"'
            elif key == "historyId": column_name = "history_id"
            elif key == "contentHtml": column_name = "content_html"
            elif key == "toAddresses": column_name = "to_addresses"
            elif key == "ccAddresses": column_name = "cc_addresses"
            elif key == "bccAddresses": column_name = "bcc_addresses"
            elif key == "replyTo": column_name = "reply_to"
            elif key == "internalDate": column_name = "internal_date"
            elif key == "labelIds": column_name = "label_ids"
            elif key == "isStarred": column_name = "is_starred"
            elif key == "isImportant": column_name = "is_important"
            elif key == "isDraft": column_name = "is_draft"
            elif key == "isSent": column_name = "is_sent"
            elif key == "isSpam": column_name = "is_spam"
            elif key == "isTrash": column_name = "is_trash"
            elif key == "isChat": column_name = "is_chat"
            elif key == "hasAttachments": column_name = "has_attachments"
            elif key == "attachmentCount": column_name = "attachment_count"
            elif key == "sizeEstimate": column_name = "size_estimate"
            elif key == "spfStatus": column_name = "spf_status"
            elif key == "dkimStatus": column_name = "dkim_status"
            elif key == "dmarcStatus": column_name = "dmarc_status"
            elif key == "isEncrypted": column_name = "is_encrypted"
            elif key == "isSigned": column_name = "is_signed"
            elif key == "isAutoReply": column_name = "is_auto_reply"
            elif key == "mailingList": column_name = "mailing_list"
            elif key == "inReplyTo": column_name = "in_reply_to"
            elif key == "isFirstInThread": column_name = "is_first_in_thread"
            elif key in ["subject", "sender", "content", "snippet",
                         "category", "priority", "references"]:
                if key == "references" and not isinstance(value, list):
                    value = [str(value)]
                column_name = key
            else:
                logger.warning(
                    f"update_email_by_message_id: Unhandled key '{key}'. "
                    "Skipping update for this field."
                )
                continue
            set_clauses.append(f"{column_name} = %s")
            params.append(value)

        if not set_clauses:
            logger.warning(f"No valid fields to update for message_id: {message_id}")
            return await self.get_email_by_message_id(message_id)

        set_clauses.append("updated_at = NOW()")
        query = (
            f"UPDATE emails SET {', '.join(set_clauses)} "
            f"WHERE message_id = %s"
        )
        params.append(message_id)
        await self._execute_query(query, tuple(params), commit=True)
        return await self.get_email_by_message_id(message_id)

    async def get_email_by_message_id(
        self, message_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get email by messageId"""
        query = (
            "SELECT e.*, c.name as categoryName, c.color as categoryColor "
            "FROM emails e LEFT JOIN categories c ON e.category_id = c.id "
            "WHERE e.message_id = %s"
        )
        row = await self._execute_query(query, (message_id,), fetch_one=True)
        return self._parse_json_fields(row, ["analysisMetadata"]) if row else None

    async def create_activity(
        self, activity_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Create a new activity record."""
        query = """
            INSERT INTO activities
                (type, description, details, "timestamp", icon, icon_bg)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id, type, description, details, "timestamp", icon, icon_bg;
        """
        details_data = activity_data.get("metadata", {})
        if "email_id" in activity_data:
            details_data["emailId"] = activity_data["email_id"]
        if "email_subject" in activity_data:
            details_data["emailSubject"] = activity_data["email_subject"]

        params = (
            activity_data["type"],
            activity_data["description"],
            json.dumps(details_data) if details_data else None,
            activity_data.get("timestamp", datetime.now().isoformat()),
            activity_data.get("icon", "default_icon"),
            activity_data.get("icon_bg", activity_data.get("iconBg", "#ffffff")),
        )
        new_activity = await self._execute_query(
            query, params, fetch_one=True, commit=True
        )
        return (
            self._parse_json_fields(new_activity, ["details"]) if new_activity else None
        )

    async def get_recent_activities(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent activities"""
        query = (
            'SELECT id, type, description, details, "timestamp", icon, icon_bg '
            'FROM activities ORDER BY "timestamp" DESC LIMIT %s'
        )
        activities = await self._execute_query(query, (limit,), fetch_all=True)
        if activities:
            return [
                self._parse_json_fields(activity, ["details"])
                for activity in activities
            ]
        return []

    async def get_dashboard_stats(self) -> Dict[str, Any]:
        logger.warning("get_dashboard_stats not fully migrated to PostgreSQL yet.")
        results = await asyncio.gather(
            self._execute_query("SELECT COUNT(*) AS count FROM emails",
                                fetch_one=True),
            self._execute_query("SELECT COUNT(*) AS count FROM emails "
                                "WHERE is_unread = TRUE", fetch_one=True),
            self._execute_query("SELECT COUNT(*) AS count FROM emails "
                                "WHERE priority = %s", ("high",), fetch_one=True),
            self._execute_query("SELECT COUNT(*) AS count FROM emails "
                                "WHERE is_spam = TRUE", fetch_one=True),
            self._execute_query("SELECT COUNT(*) AS count FROM categories",
                                fetch_one=True),
            self._execute_query("SELECT name, color, count FROM categories "
                                "ORDER BY count DESC LIMIT 5", fetch_all=True),
        )

        total_emails = results[0]["count"] if results[0] else 0
        unread_emails = results[1]["count"] if results[1] else 0
        important_emails = results[2]["count"] if results[2] else 0
        spam_emails = results[3]["count"] if results[3] else 0
        total_category_types = results[4]["count"] if results[4] else 0
        top_categories_list = results[5] if results[5] else []

        return {
            "totalEmails": total_emails, "unreadEmails": unread_emails,
            "importantEmails": important_emails, "spamEmails": spam_emails,
            "totalCategoryTypes": total_category_types,
            "topCategories": top_categories_list,
            "autoLabeled": total_emails,  # Placeholder
            "timeSaved": "2.5 hours",  # Placeholder
            "weeklyGrowth": { # Placeholder for complex calculation
                "totalEmails": total_emails, "autoLabeled": total_emails,
                "categories": total_category_types, "timeSaved": 0,
            },
        }

    async def get_all_emails(
        self, limit: int = 50, offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Get all emails with pagination"""
        return await self.get_emails(limit=limit, offset=offset)

    async def get_emails_by_category(
        self, category_id: int, limit: int = 50, offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Get emails by category"""
        return await self.get_emails(
            limit=limit, offset=offset, category_id=category_id
        )

    async def search_emails(
        self, search_term: str, limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Search emails by content or subject."""
        query = (
            "SELECT e.*, c.name as categoryName, c.color as categoryColor "
            "FROM emails e LEFT JOIN categories c ON e.category_id = c.id "
            "WHERE e.subject ILIKE %s OR e.content ILIKE %s "
            'ORDER BY e."time" DESC LIMIT %s'
        )
        params = (f"%{search_term}%", f"%{search_term}%", limit)
        emails = await self._execute_query(query, params, fetch_all=True)
        if emails:
            return [
                self._parse_json_fields(email, ["analysisMetadata"]) for email in emails
            ]
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
                "subject", "content", "sender", "confidence",
                "snippet", "category", "priority",
            ]:
                column_name = key
            else:
                temp_col_name = key.replace("Id", "_id").replace("Html", "_html")
                import re
                temp_col_name = re.sub(r"(?<!^)(?=[A-Z])", "_", key).lower()
                if temp_col_name != key:
                    logger.info(
                        f"update_email: Converted key '{key}' to "
                        f"'{temp_col_name}' for SQL query.")
                    column_name = temp_col_name
                else:
                    logger.warning(
                        f"update_email: Unhandled key '{key}' or key not "
                        "directly updatable by internal ID method. Skipping."
                    )
                    continue

            set_clauses.append(f"{column_name} = %s")
            params.append(value)

        if not set_clauses:
            logger.info(f"No valid fields to update for email id: {email_id}")
            return await self.get_email_by_id(email_id)

        set_clauses.append("updated_at = NOW()")
        query = (
            f"UPDATE emails SET {', '.join(set_clauses)} WHERE id = %s"
        )
        params.append(email_id)
        await self._execute_query(query, tuple(params), commit=True)
        return await self.get_email_by_id(email_id)


async def get_db() -> DatabaseManager:
    """Dependency injection for database"""
    return DatabaseManager()
