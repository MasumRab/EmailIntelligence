#!/usr/bin/env python3
"""
Data Migration Utility for EmailIntelligence

This script provides utilities to migrate data between JSON file storage (scientific branch)
and SQLite database storage (sqlite branch).

Usage:
    python migration_utility.py [command] [options]

Commands:
    json-to-sqlite    - Convert JSON data to SQLite database
    sqlite-to-json    - Export SQLite data to JSON files
    validate-json     - Validate JSON data files
    validate-sqlite   - Validate SQLite database
"""

import argparse
import gzip
import json
import logging
import os
import sqlite3
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add src to path for imports (calculate relative to this script's location)
script_dir = Path(__file__).parent
project_root = script_dir.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))
from src.core.security import PathValidator, validate_path_safety

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("migration_utility")

# Default paths
DEFAULT_DATA_DIR = Path("./data")
DEFAULT_DB_PATH = Path("sqlite.db")
DEFAULT_EMAIL_CONTENT_DIR = DEFAULT_DATA_DIR / "email_content"
DEFAULT_EMAILS_FILE = DEFAULT_DATA_DIR / "emails.json.gz"
DEFAULT_CATEGORIES_FILE = DEFAULT_DATA_DIR / "categories.json.gz"
DEFAULT_USERS_FILE = DEFAULT_DATA_DIR / "users.json.gz"


def read_gzipped_json(file_path: Path) -> Optional[Any]:
    """Read data from a gzipped JSON file."""
    try:
        if not file_path.exists():
            logger.warning(f"File {file_path} does not exist")
            return None

        with gzip.open(file_path, "rt", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error reading {file_path}: {e}")
        return None


def write_gzipped_json(file_path: Path, data: Any) -> bool:
    """Write data to a gzipped JSON file."""
    try:
        # Create directory if it doesn't exist
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with gzip.open(file_path, "wt", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)
        return True
    except Exception as e:
        logger.error(f"Error writing {file_path}: {e}")
        return False


def connect_sqlite(db_path: Path) -> Optional[sqlite3.Connection]:
    """Connect to SQLite database."""
    try:
        # Validate the database path for security
        validated_path = PathValidator.validate_database_path(db_path)
        conn = sqlite3.connect(validated_path)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        logger.error(f"Error connecting to database {db_path}: {e}")
        return None


def initialize_sqlite_schema(conn: sqlite3.Connection) -> bool:
    """Initialize SQLite database schema."""
    try:
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

        cursor = conn.cursor()
        cursor.execute(create_users_table)
        cursor.execute(create_categories_table)
        cursor.execute(create_emails_table)
        cursor.execute(create_activities_table)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_emails_category_id ON emails (category_id);")
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_emails_time ON emails ("time");')
        conn.commit()
        logger.info("SQLite database schema initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Error initializing SQLite schema: {e}")
        return False


def migrate_json_to_sqlite(
    data_dir: Path = DEFAULT_DATA_DIR, db_path: Path = DEFAULT_DB_PATH
) -> bool:
    """Migrate data from JSON files to SQLite database."""
    logger.info(f"Starting migration from JSON files in {data_dir} to SQLite database {db_path}")

    # Connect to SQLite database
    conn = connect_sqlite(db_path)
    if not conn:
        return False

    # Initialize schema
    if not initialize_sqlite_schema(conn):
        conn.close()
        return False

    try:
        cursor = conn.cursor()

        # Migrate categories
        categories_file = data_dir / "categories.json.gz"
        categories_data = read_gzipped_json(categories_file)
        if categories_data:
            logger.info(f"Migrating {len(categories_data)} categories")
            for category in categories_data:
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO categories 
                    (id, name, description, color, count)
                    VALUES (?, ?, ?, ?, ?)
                """,
                    (
                        category.get("id"),
                        category.get("name"),
                        category.get("description"),
                        category.get("color", "#6366f1"),
                        category.get("count", 0),
                    ),
                )
            conn.commit()
            logger.info("Categories migrated successfully")

        # Migrate emails
        emails_file = data_dir / "emails.json.gz"
        emails_data = read_gzipped_json(emails_file)
        if emails_data:
            logger.info(f"Migrating {len(emails_data)} emails")

            # Prepare email data for insertion
            email_records = []
            for email in emails_data:
                # Convert lists and dicts to JSON strings for SQLite storage
                labels_json = json.dumps(email.get("labels", [])) if email.get("labels") else "[]"
                label_ids_json = (
                    json.dumps(email.get("label_ids", [])) if email.get("label_ids") else "[]"
                )
                to_addresses_json = (
                    json.dumps(email.get("to_addresses", [])) if email.get("to_addresses") else "[]"
                )
                cc_addresses_json = (
                    json.dumps(email.get("cc_addresses", [])) if email.get("cc_addresses") else "[]"
                )
                bcc_addresses_json = (
                    json.dumps(email.get("bcc_addresses", []))
                    if email.get("bcc_addresses")
                    else "[]"
                )
                references_json = (
                    json.dumps(email.get("references", [])) if email.get("references") else "[]"
                )
                analysis_metadata_json = (
                    json.dumps(email.get("analysis_metadata", {}))
                    if email.get("analysis_metadata")
                    else "{}"
                )

                email_records.append(
                    (
                        email.get("id"),
                        email.get("message_id"),
                        email.get("thread_id"),
                        email.get("history_id"),
                        email.get("sender"),
                        email.get("sender_email"),
                        email.get("subject"),
                        email.get("content"),
                        email.get("content_html"),
                        email.get("preview"),
                        email.get("snippet"),
                        to_addresses_json,
                        cc_addresses_json,
                        bcc_addresses_json,
                        email.get("reply_to"),
                        email.get("time"),
                        email.get("internal_date"),
                        label_ids_json,
                        labels_json,
                        email.get("category"),
                        email.get("is_unread", 1),
                        email.get("is_starred", 0),
                        email.get("is_important", 0),
                        email.get("is_draft", 0),
                        email.get("is_sent", 0),
                        email.get("is_spam", 0),
                        email.get("is_trash", 0),
                        email.get("is_chat", 0),
                        email.get("has_attachments", 0),
                        email.get("attachment_count", 0),
                        email.get("size_estimate"),
                        email.get("spf_status"),
                        email.get("dkim_status"),
                        email.get("dmarc_status"),
                        email.get("is_encrypted", 0),
                        email.get("is_signed", 0),
                        email.get("priority", "normal"),
                        email.get("is_auto_reply", 0),
                        email.get("mailing_list"),
                        email.get("in_reply_to"),
                        references_json,
                        email.get("is_first_in_thread", 1),
                        email.get("category_id"),
                        email.get("confidence", 95),
                        analysis_metadata_json,
                        email.get("is_read", 0),
                        email.get("created_at"),
                        email.get("updated_at"),
                    )
                )

            # Bulk insert emails
            cursor.executemany(
                """
                INSERT OR REPLACE INTO emails
                (id, message_id, thread_id, history_id, sender, sender_email, subject,
                content, content_html, preview, snippet, to_addresses, cc_addresses,
                bcc_addresses, reply_to, "time", internal_date, label_ids, labels,
                category, is_unread, is_starred, is_important, is_draft, is_sent,
                is_spam, is_trash, is_chat, has_attachments, attachment_count,
                size_estimate, spf_status, dkim_status, dmarc_status, is_encrypted,
                is_signed, priority, is_auto_reply, mailing_list, in_reply_to,
                "references", is_first_in_thread, category_id, confidence,
                analysis_metadata, is_read, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                ?, ?, ?, ?, ?, ?)
            """,
                email_records,
            )
            conn.commit()
            logger.info("Emails migrated successfully")

        # Migrate users (if exists)
        users_file = data_dir / "users.json.gz"
        users_data = read_gzipped_json(users_file)
        if users_data:
            logger.info(f"Migrating {len(users_data)} users")
            for user in users_data:
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO users 
                    (id, username, password)
                    VALUES (?, ?, ?)
                """,
                    (user.get("id"), user.get("username"), user.get("password")),
                )
            conn.commit()
            logger.info("Users migrated successfully")

        logger.info("JSON to SQLite migration completed successfully")
        return True

    except Exception as e:
        logger.error(f"Error during JSON to SQLite migration: {e}")
        return False
    finally:
        if conn:
            conn.close()


def migrate_sqlite_to_json(
    db_path: Path = DEFAULT_DB_PATH, data_dir: Path = DEFAULT_DATA_DIR
) -> bool:
    """Export data from SQLite database to JSON files."""
    logger.info(f"Starting export from SQLite database {db_path} to JSON files in {data_dir}")

    # Connect to SQLite database
    conn = connect_sqlite(db_path)
    if not conn:
        return False

    try:
        cursor = conn.cursor()

        # Export categories
        cursor.execute("SELECT * FROM categories")
        categories_rows = cursor.fetchall()
        categories_data = [dict(row) for row in categories_rows]

        categories_file = data_dir / "categories.json.gz"
        if write_gzipped_json(categories_file, categories_data):
            logger.info(f"Exported {len(categories_data)} categories to {categories_file}")
        else:
            logger.error("Failed to export categories")
            return False

        # Export emails
        cursor.execute("SELECT * FROM emails")
        emails_rows = cursor.fetchall()
        emails_data = []

        for row in emails_rows:
            email_dict = dict(row)
            # Parse JSON strings back to objects
            try:
                if email_dict.get("labels"):
                    email_dict["labels"] = json.loads(email_dict["labels"])
                if email_dict.get("label_ids"):
                    email_dict["label_ids"] = json.loads(email_dict["label_ids"])
                if email_dict.get("to_addresses"):
                    email_dict["to_addresses"] = json.loads(email_dict["to_addresses"])
                if email_dict.get("cc_addresses"):
                    email_dict["cc_addresses"] = json.loads(email_dict["cc_addresses"])
                if email_dict.get("bcc_addresses"):
                    email_dict["bcc_addresses"] = json.loads(email_dict["bcc_addresses"])
                if email_dict.get("references"):
                    email_dict["references"] = json.loads(email_dict["references"])
                if email_dict.get("analysis_metadata"):
                    email_dict["analysis_metadata"] = json.loads(email_dict["analysis_metadata"])
            except json.JSONDecodeError as e:
                logger.warning(f"Error parsing JSON fields for email {email_dict.get('id')}: {e}")

            emails_data.append(email_dict)

        emails_file = data_dir / "emails.json.gz"
        if write_gzipped_json(emails_file, emails_data):
            logger.info(f"Exported {len(emails_data)} emails to {emails_file}")
        else:
            logger.error("Failed to export emails")
            return False

        # Export users
        cursor.execute("SELECT * FROM users")
        users_rows = cursor.fetchall()
        users_data = [dict(row) for row in users_rows]

        if users_data:
            users_file = data_dir / "users.json.gz"
            if write_gzipped_json(users_file, users_data):
                logger.info(f"Exported {len(users_data)} users to {users_file}")
            else:
                logger.error("Failed to export users")
                return False

        logger.info("SQLite to JSON export completed successfully")
        return True

    except Exception as e:
        logger.error(f"Error during SQLite to JSON export: {e}")
        return False
    finally:
        if conn:
            conn.close()


def validate_json_data(data_dir: Path = DEFAULT_DATA_DIR) -> bool:
    """Validate JSON data files."""
    logger.info(f"Validating JSON data in {data_dir}")

    required_files = ["emails.json.gz", "categories.json.gz"]

    all_valid = True

    for filename in required_files:
        file_path = data_dir / filename
        if not file_path.exists():
            logger.warning(f"Required file {file_path} does not exist")
            all_valid = False
            continue

        try:
            data = read_gzipped_json(file_path)
            if data is None:
                logger.error(f"Unable to read {file_path}")
                all_valid = False
            else:
                logger.info(f"{file_path} is valid with {len(data)} records")
        except Exception as e:
            logger.error(f"Error validating {file_path}: {e}")
            all_valid = False

    if all_valid:
        logger.info("All JSON data files are valid")
    else:
        logger.error("Some JSON data files are invalid")

    return all_valid


def validate_sqlite_database(db_path: Path = DEFAULT_DB_PATH) -> bool:
    """Validate SQLite database."""
    logger.info(f"Validating SQLite database {db_path}")

    if not db_path.exists():
        logger.error(f"Database file {db_path} does not exist")
        return False

    conn = connect_sqlite(db_path)
    if not conn:
        return False

    try:
        cursor = conn.cursor()

        # Check if required tables exist
        required_tables = ["users", "categories", "emails", "activities"]
        for table in required_tables:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
            if not cursor.fetchone():
                logger.error(f"Required table '{table}' does not exist")
                return False

        # Count records in each table
        for table in required_tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            logger.info(f"Table '{table}' contains {count} records")

        logger.info("SQLite database validation completed successfully")
        return True

    except Exception as e:
        logger.error(f"Error validating SQLite database: {e}")
        return False
    finally:
        if conn:
            conn.close()


def main():
    """Main entry point for the migration utility."""
    parser = argparse.ArgumentParser(description="Data Migration Utility for EmailIntelligence")
    parser.add_argument(
        "command",
        choices=["json-to-sqlite", "sqlite-to-json", "validate-json", "validate-sqlite"],
        help="Migration command to execute",
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        default=str(DEFAULT_DATA_DIR),
        help="Path to data directory (for JSON files)",
    )
    parser.add_argument(
        "--db-path", type=str, default=str(DEFAULT_DB_PATH), help="Path to SQLite database file"
    )

    args = parser.parse_args()

    # Validate paths for security
    data_dir_str = args.data_dir
    db_path_str = args.db_path

    if not validate_path_safety(data_dir_str):
        logger.error(f"Unsafe data directory path: {data_dir_str}")
        sys.exit(1)

    if not validate_path_safety(db_path_str):
        logger.error(f"Unsafe database path: {db_path_str}")
        sys.exit(1)

    data_dir = Path(data_dir_str)
    db_path = Path(db_path_str)

    # Execute the command
    if args.command == "json-to-sqlite":
        success = migrate_json_to_sqlite(data_dir, db_path)
    elif args.command == "sqlite-to-json":
        success = migrate_sqlite_to_json(db_path, data_dir)
    elif args.command == "validate-json":
        success = validate_json_data(data_dir)
    elif args.command == "validate-sqlite":
        success = validate_sqlite_database(db_path)
    else:
        logger.error(f"Unknown command: {args.command}")
        success = False

    # Exit with appropriate status code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
