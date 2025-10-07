"""
Database management for Gmail AI email processing using aiosqlite.
"""

import asyncio
import json
import logging
import os
import shutil
import time
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Dict, List, Optional

import aiosqlite

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Async database manager for email data using aiosqlite."""

    def __init__(self, db_url: Optional[str] = None):
        raw_db_url = db_url or os.getenv("DATABASE_URL")

        if raw_db_url:
            if raw_db_url.startswith("sqlite:"):
                path_part = raw_db_url.split(":", 1)[1]
                if path_part.startswith("//"):
                    path_part = path_part[2:]
                self.db_path = path_part
            else:
                self.db_path = raw_db_url
        else:
            self.db_path = "./sqlite.db"

        logger.info(f"DatabaseManager initialized with SQLite path: {self.db_path}")
        self._db = None
        self._category_cache: Optional[List[Dict[str, Any]]] = None
        self._email_write_cache = asyncio.Queue()
        self._last_write_time = asyncio.get_event_loop().time()
        self._write_lock = asyncio.Lock()
        self._backup_dir = "db_backups"
        self._last_backup_time = 0
        os.makedirs(self._backup_dir, exist_ok=True)

    async def connect(self):
        """Establish a database connection."""
        if self._db is None:
            self._db = await aiosqlite.connect(self.db_path)
            self._db.row_factory = aiosqlite.Row
            await self._db.execute("PRAGMA foreign_keys = ON;")
            await self._db.commit()
            logger.info(f"Connected to SQLite database at {self.db_path}")

    async def close(self):
        """Close the database connection."""
        if self._db:
            await self._flush_email_cache(force=True)
            await self._db.close()
            self._db = None
            logger.info("Disconnected from SQLite database.")

    @asynccontextmanager
    async def get_cursor(self):
        """Async context manager for getting a database cursor."""
        if not self._db:
            await self.connect()

        async with self._db.cursor() as cursor:
            yield cursor

    async def init_database(self):
        """
        Initializes the database schema. This is an async method.
        """
        if not self._db:
            await self.connect()

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
            to_addresses TEXT,
            cc_addresses TEXT,
            bcc_addresses TEXT,
            reply_to TEXT,
            "time" TEXT NOT NULL,
            internal_date TEXT,
            label_ids TEXT,
            labels TEXT,
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
            "references" TEXT,
            is_first_in_thread INTEGER DEFAULT 1,
            category_id INTEGER,
            confidence INTEGER DEFAULT 95,
            analysis_metadata TEXT,
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
            details TEXT,
            "timestamp" TEXT NOT NULL,
            icon TEXT NOT NULL,
            icon_bg TEXT NOT NULL
        );
        """
        async with self.get_cursor() as cur:
            await cur.execute(create_users_table)
            await cur.execute(create_categories_table)
            await cur.execute(create_emails_table)
            await cur.execute(create_activities_table)
            await cur.execute(
                "CREATE INDEX IF NOT EXISTS idx_emails_category_id ON emails (category_id);"
            )
            await cur.execute('CREATE INDEX IF NOT EXISTS idx_emails_time ON emails ("time");')
        await self._db.commit()
        logger.info("Database tables and indexes initialized/verified for SQLite.")

    def _parse_json_fields(self, row: aiosqlite.Row, fields: List[str]) -> Dict[str, Any]:
        if not row:
            return None
        row_dict = dict(row)
        for field in fields:
            if field in row_dict and isinstance(row_dict[field], str):
                try:
                    row_dict[field] = json.loads(row_dict[field])
                except json.JSONDecodeError:
                    logger.warning(
                        f"Failed to parse JSON for field {field} in row {row_dict.get('id')}"
                    )
                    row_dict[field] = {} if field in ("analysisMetadata", "metadata") else []
        return row_dict

    async def create_email(self, email_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Add an email to the write cache and trigger a flush if needed."""
        await self._email_write_cache.put(email_data)
        await self._flush_email_cache()
        return email_data

    async def create_emails_batch(self, emails_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Add a batch of emails to the write cache."""
        for email_data in emails_data:
            await self._email_write_cache.put(email_data)
        await self._flush_email_cache()
        return emails_data

    async def update_emails_batch(self, email_ids: List[int], updates: Dict[str, Any]) -> bool:
        """Update a batch of emails with the same data."""
        if not email_ids or not updates:
            return False

        set_clauses = []
        params = []
        for key, value in updates.items():
            column_name = "".join(["_" + i.lower() if i.isupper() else i for i in key]).lstrip("_")
            set_clauses.append(f"{column_name} = ?")
            params.append(value)

        if not set_clauses:
            return False

        set_clauses.append("updated_at = datetime('now')")

        placeholders = ",".join("?" for _ in email_ids)
        query = f"UPDATE emails SET {', '.join(set_clauses)} WHERE id IN ({placeholders})"

        params.extend(email_ids)

        try:
            async with self.get_cursor() as cur:
                await cur.execute(query, tuple(params))
                await self._db.commit()

            if "categoryId" in updates or "category_id" in updates:
                self._category_cache = None

            logger.info(f"Successfully updated batch of {len(email_ids)} emails.")
            return True
        except aiosqlite.Error as e:
            logger.error(f"Failed to update email batch: {e}")
            return False

    async def get_email_by_id(self, email_id: int) -> Optional[Dict[str, Any]]:
        await self._flush_email_cache(force=True)
        query = "SELECT e.*, c.name as categoryName, c.color as categoryColor FROM emails e LEFT JOIN categories c ON e.category_id = c.id WHERE e.id = ?"
        async with self.get_cursor() as cur:
            await cur.execute(query, (email_id,))
            row = await cur.fetchone()
        return self._parse_json_fields(
            row,
            [
                "labels",
                "analysisMetadata",
                "to_addresses",
                "cc_addresses",
                "bcc_addresses",
                "label_ids",
                "references",
            ],
        )

    async def get_all_categories(self) -> List[Dict[str, Any]]:
        """Get all categories with their counts."""
        if self._category_cache is not None:
            logger.info("Returning categories from cache.")
            return self._category_cache

        logger.info("Fetching categories from database.")
        query = "SELECT id, name, description, color, count FROM categories ORDER BY name"
        async with self.get_cursor() as cur:
            await cur.execute(query)
            rows = await cur.fetchall()

        self._category_cache = [dict(row) for row in rows]
        return self._category_cache

    async def create_category(self, category_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        query = "INSERT INTO categories (name, description, color, count) VALUES (?, ?, ?, ?)"
        params = (
            category_data["name"],
            category_data.get("description"),
            category_data.get("color", "#6366f1"),
            0,
        )
        try:
            async with self.get_cursor() as cur:
                await cur.execute(query, params)
                category_id = cur.lastrowid
                await self._db.commit()
            self._category_cache = None
            return {"id": category_id, **category_data, "count": 0}
        except aiosqlite.Error as e:
            logger.error(f"Failed to create category {category_data.get('name')}: {e}")
            return None

    async def _update_category_count(self, category_id: int, increment: bool):
        operator = "+" if increment else "-"
        query = f"UPDATE categories SET count = count {operator} 1 WHERE id = ?"
        async with self.get_cursor() as cur:
            await cur.execute(query, (category_id,))
            await self._db.commit()
        self._category_cache = None

    async def _flush_email_cache(self, force: bool = False):
        """Write emails from the cache to the database if conditions are met or if forced."""
        now = asyncio.get_event_loop().time()
        should_flush = (
            force or self._email_write_cache.qsize() >= 10 or (now - self._last_write_time) > 5
        )

        if not should_flush or self._email_write_cache.empty():
            return

        async with self._write_lock:
            if self._email_write_cache.empty():
                return

            emails_to_write = []
            while not self._email_write_cache.empty():
                emails_to_write.append(self._email_write_cache.get_nowait())

            if not emails_to_write:
                return

            query = """
                INSERT INTO emails (
                    message_id, thread_id, subject, sender, sender_email, content,
                    snippet, labels, "time", is_unread, category_id, confidence,
                    analysis_metadata, history_id, content_html,
                    preview, to_addresses, cc_addresses, bcc_addresses, reply_to,
                    internal_date, label_ids, category, is_starred, is_important,
                    is_draft, is_sent, is_spam, is_trash, is_chat, has_attachments,
                    attachment_count, size_estimate, spf_status, dkim_status,
                    dmarc_status, is_encrypted, is_signed, priority, is_auto_reply,
                    mailing_list, in_reply_to, "references", is_first_in_thread
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            params_list = [
                (
                    email.get("message_id"),
                    email.get("thread_id"),
                    email.get("subject"),
                    email.get("sender"),
                    email.get("sender_email"),
                    email.get("content"),
                    email.get("snippet"),
                    json.dumps(email.get("labels", [])),
                    email.get("time"),
                    not email.get("is_read", False),
                    email.get("category_id"),
                    email.get("confidence", 0),
                    json.dumps(email.get("analysis_metadata", {})),
                    email.get("history_id"),
                    email.get("content_html"),
                    email.get("preview"),
                    json.dumps(email.get("to_addresses", [])),
                    json.dumps(email.get("cc_addresses", [])),
                    json.dumps(email.get("bcc_addresses", [])),
                    email.get("reply_to"),
                    email.get("internal_date"),
                    json.dumps(email.get("label_ids", [])),
                    email.get("category"),
                    email.get("is_starred", False),
                    email.get("is_important", False),
                    email.get("is_draft", False),
                    email.get("is_sent", False),
                    email.get("is_spam", False),
                    email.get("is_trash", False),
                    email.get("is_chat", False),
                    email.get("has_attachments", False),
                    email.get("attachment_count", 0),
                    email.get("size_estimate"),
                    email.get("spf_status"),
                    email.get("dkim_status"),
                    email.get("dmarc_status"),
                    email.get("is_encrypted", False),
                    email.get("is_signed", False),
                    email.get("priority", "normal"),
                    email.get("is_auto_reply", False),
                    email.get("mailing_list"),
                    email.get("in_reply_to"),
                    json.dumps(email.get("references", [])),
                    email.get("is_first_in_thread", True),
                )
                for email in emails_to_write
            ]

            try:
                async with self.get_cursor() as cur:
                    await cur.executemany(query, params_list)
                    await self._db.commit()

                logger.info(f"Flushed {len(emails_to_write)} emails to the database.")
                self._last_write_time = now

                category_ids = {
                    email.get("category_id")
                    for email in emails_to_write
                    if email.get("category_id")
                }
                for category_id in category_ids:
                    await self._update_category_count(category_id, increment=True)

            except aiosqlite.Error as e:
                logger.error(f"Failed to flush email cache: {e}")

    async def get_emails(
        self,
        limit: int = 50,
        offset: int = 0,
        category_id: Optional[int] = None,
        is_unread: Optional[bool] = None,
    ) -> List[Dict[str, Any]]:
        await self._flush_email_cache(force=True)
        params = []
        base_query = "SELECT e.*, c.name as categoryName, c.color as categoryColor FROM emails e LEFT JOIN categories c ON e.category_id = c.id"
        where_clauses = []
        if category_id is not None:
            where_clauses.append("e.category_id = ?")
            params.append(category_id)
        if is_unread is not None:
            where_clauses.append("e.is_unread = ?")
            params.append(is_unread)

        if where_clauses:
            base_query += " WHERE " + " AND ".join(where_clauses)

        base_query += ' ORDER BY e."time" DESC LIMIT ? OFFSET ?'
        params.extend([limit, offset])

        async with self.get_cursor() as cur:
            await cur.execute(base_query, tuple(params))
            rows = await cur.fetchall()

        json_fields = [
            "labels",
            "analysisMetadata",
            "to_addresses",
            "cc_addresses",
            "bcc_addresses",
            "label_ids",
            "references",
        ]
        return [self._parse_json_fields(row, json_fields) for row in rows]

    async def update_email(
        self, email_id: int, update_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        original_email = await self.get_email_by_id(email_id)
        if not original_email:
            return None
        original_category_id = original_email.get("category_id")

        set_clauses = []
        params = []
        for key, value in update_data.items():
            if key == "id":
                continue
            column_name = "".join(["_" + i.lower() if i.isupper() else i for i in key]).lstrip("_")
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            set_clauses.append(f"{column_name} = ?")
            params.append(value)

        if not set_clauses:
            return original_email

        set_clauses.append("updated_at = datetime('now')")
        query = f"UPDATE emails SET {', '.join(set_clauses)} WHERE id = ?"
        params.append(email_id)

        async with self.get_cursor() as cur:
            await cur.execute(query, tuple(params))
            await self._db.commit()

        new_category_id = update_data.get("categoryId")
        if new_category_id is not None and new_category_id != original_category_id:
            if original_category_id is not None:
                await self._update_category_count(original_category_id, increment=False)
            await self._update_category_count(new_category_id, increment=True)

        return await self.get_email_by_id(email_id)

    def _cleanup_old_backups(self, keep=7):
        """Removes old backup files, keeping the most recent `keep` number of backups."""
        try:
            backups = sorted(
                [os.path.join(self._backup_dir, f) for f in os.listdir(self._backup_dir)],
                key=os.path.getmtime,
                reverse=True,
            )
            if len(backups) > keep:
                for old_backup in backups[keep:]:
                    os.remove(old_backup)
                    logger.info(f"Removed old backup: {old_backup}")
        except Exception as e:
            logger.error(f"Error cleaning up old backups: {e}")

    async def backup_database(self):
        """Creates a backup of the database if it hasn't been backed up in the last 24 hours."""
        now = time.time()
        if (now - self._last_backup_time) > 86400:
            logger.info("Starting scheduled database backup...")
            backup_file_name = f"backup_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')}.db"
            backup_path = os.path.join(self._backup_dir, backup_file_name)

            try:
                await self._flush_email_cache(force=True)

                await asyncio.to_thread(shutil.copy, self.db_path, backup_path)

                self._last_backup_time = now
                logger.info(f"Database backup created successfully at {backup_path}")
                self._cleanup_old_backups()
            except Exception as e:
                logger.error(f"Failed to create database backup: {e}")


db_manager = DatabaseManager()


async def get_db() -> DatabaseManager:
    return db_manager
