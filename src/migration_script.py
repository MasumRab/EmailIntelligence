#!/usr/bin/env python3
"""
Data Migration Script: SQLite to JSON

This script migrates email data from SQLite database to JSON format.
It handles the conversion of emails, categories, and users data with proper
schema mapping and data validation.

Usage:
    python src/migration_script.py --sqlite-db data/emails.sqlite3 --output-dir data/processed
"""

import argparse
import json
import logging
import os
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataMigrationError(Exception):
    """Exception raised when data migration fails."""
    pass


class SQLiteToJSONMigrator:
    """Migrator class for converting SQLite data to JSON format."""

    def __init__(self, sqlite_db_path: str, output_dir: str):
        """
        Initialize the migrator.

        Args:
            sqlite_db_path: Path to the SQLite database file
            output_dir: Directory to output JSON files
        """
        self.sqlite_db_path = sqlite_db_path
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Validate SQLite database exists
        if not os.path.exists(sqlite_db_path):
            raise DataMigrationError(f"SQLite database not found: {sqlite_db_path}")

    def connect_db(self) -> sqlite3.Connection:
        """Connect to SQLite database with row factory."""
        conn = sqlite3.connect(self.sqlite_db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def migrate_emails(self) -> List[Dict[str, Any]]:
        """
        Migrate emails data from SQLite to JSON format.

        Returns:
            List of email dictionaries in JSON format
        """
        logger.info("Migrating emails data...")

        conn = self.connect_db()
        try:
            cursor = conn.cursor()

            # Query emails with category information
            cursor.execute('''
                SELECT
                    e.id,
                    e.message_id,
                    e.subject,
                    e.sender,
                    e.sender_email,
                    e.content,
                    e.content_html,
                    e.category_id,
                    c.name as category_name,
                    c.color as category_color,
                    e.is_unread,
                    e.analysis_metadata,
                    e.created_at,
                    e.updated_at
                FROM emails e
                LEFT JOIN categories c ON e.category_id = c.id
                ORDER BY e.created_at DESC
            ''')

            emails = []
            for row in cursor.fetchall():
                # Parse analysis_metadata JSON if it exists
                analysis_metadata = None
                if row['analysis_metadata']:
                    try:
                        analysis_metadata = json.loads(row['analysis_metadata'])
                    except json.JSONDecodeError:
                        logger.warning(f"Invalid JSON in analysis_metadata for email {row['id']}")
                        analysis_metadata = None

                email_dict = {
                    'id': row['id'],
                    'message_id': row['message_id'],
                    'subject': row['subject'],
                    'sender': row['sender'],
                    'sender_email': row['sender_email'],
                    'content': row['content'],
                    'content_html': row['content_html'],
                    'category_id': row['category_id'],
                    'categoryName': row['category_name'],  # UI field name
                    'categoryColor': row['category_color'],  # UI field name
                    'is_unread': bool(row['is_unread']),
                    'analysis_metadata': analysis_metadata,
                    'created_at': row['created_at'],
                    'updated_at': row['updated_at']
                }
                emails.append(email_dict)

            logger.info(f"Migrated {len(emails)} emails")
            return emails

        finally:
            conn.close()

    def migrate_categories(self) -> List[Dict[str, Any]]:
        """
        Migrate categories data from SQLite to JSON format.

        Returns:
            List of category dictionaries in JSON format
        """
        logger.info("Migrating categories data...")

        conn = self.connect_db()
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name, description, color, count FROM categories ORDER BY id')

            categories = []
            for row in cursor.fetchall():
                category_dict = {
                    'id': row['id'],
                    'name': row['name'],
                    'description': row['description'],
                    'color': row['color'],
                    'count': row['count']
                }
                categories.append(category_dict)

            logger.info(f"Migrated {len(categories)} categories")
            return categories

        finally:
            conn.close()

    def migrate_users(self) -> List[Dict[str, Any]]:
        """
        Migrate users data from SQLite to JSON format.

        Returns:
            List of user dictionaries in JSON format
        """
        logger.info("Migrating users data...")

        conn = self.connect_db()
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT id, username, email, created_at FROM users ORDER BY id')

            users = []
            for row in cursor.fetchall():
                user_dict = {
                    'id': row['id'],
                    'username': row['username'],
                    'email': row['email'],
                    'created_at': row['created_at']
                }
                users.append(user_dict)

            logger.info(f"Migrated {len(users)} users")
            return users

        finally:
            conn.close()

    def get_database_stats(self) -> Dict[str, int]:
        """
        Get statistics about the SQLite database.

        Returns:
            Dictionary with table row counts
        """
        logger.info("Collecting database statistics...")

        conn = self.connect_db()
        try:
            cursor = conn.cursor()

            stats = {}
            tables = ['emails', 'categories', 'users']

            for table in tables:
                cursor.execute(f'SELECT COUNT(*) FROM {table}')
                stats[table] = cursor.fetchone()[0]

            logger.info(f"Database stats: {stats}")
            return stats

        finally:
            conn.close()

    def validate_migration(self, original_stats: Dict[str, int], migrated_data: Dict[str, List]) -> Dict[str, Any]:
        """
        Validate that migration was successful by comparing counts.

        Args:
            original_stats: Original database statistics
            migrated_data: Migrated JSON data

        Returns:
            Validation results dictionary
        """
        logger.info("Validating migration...")

        validation_results = {
            'success': True,
            'issues': [],
            'stats': {
                'original': original_stats,
                'migrated': {k: len(v) for k, v in migrated_data.items()}
            }
        }

        # Check counts match
        for table_name in original_stats.keys():
            original_count = original_stats[table_name]
            migrated_count = len(migrated_data[table_name])

            if original_count != migrated_count:
                validation_results['success'] = False
                validation_results['issues'].append(
                    f"Count mismatch for {table_name}: {original_count} -> {migrated_count}"
                )

        if validation_results['success']:
            logger.info("Migration validation passed")
        else:
            logger.warning(f"Migration validation found issues: {validation_results['issues']}")

        return validation_results

    def save_json_file(self, data: List[Dict[str, Any]], filename: str) -> str:
        """
        Save data to JSON file.

        Args:
            data: Data to save
            filename: Output filename

        Returns:
            Path to saved file
        """
        output_path = self.output_dir / filename

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)

        logger.info(f"Saved {len(data)} records to {output_path}")
        return str(output_path)

    def migrate_all(self) -> Dict[str, Any]:
        """
        Perform complete migration from SQLite to JSON.

        Returns:
            Migration results dictionary
        """
        logger.info("Starting complete data migration...")

        try:
            # Get original database statistics
            original_stats = self.get_database_stats()

            # Migrate all data
            emails = self.migrate_emails()
            categories = self.migrate_categories()
            users = self.migrate_users()

            migrated_data = {
                'emails': emails,
                'categories': categories,
                'users': users
            }

            # Validate migration
            validation = self.validate_migration(original_stats, migrated_data)

            # Save JSON files
            saved_files = {}
            saved_files['email_data.json'] = self.save_json_file(emails, 'email_data.json')
            saved_files['categories.json'] = self.save_json_file(categories, 'categories.json')
            saved_files['users.json'] = self.save_json_file(users, 'users.json')

            # Create migration report
            migration_report = {
                'timestamp': datetime.now().isoformat(),
                'sqlite_database': self.sqlite_db_path,
                'output_directory': str(self.output_dir),
                'original_stats': original_stats,
                'migrated_stats': {k: len(v) for k, v in migrated_data.items()},
                'validation': validation,
                'saved_files': saved_files,
                'schema_mapping': self.get_schema_mapping_documentation()
            }

            # Save migration report
            report_path = self.output_dir / 'migration_report.json'
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(migration_report, f, indent=2, ensure_ascii=False, default=str)

            logger.info("Migration completed successfully")
            return migration_report

        except Exception as e:
            logger.error(f"Migration failed: {e}")
            raise DataMigrationError(f"Migration failed: {str(e)}")

    def get_schema_mapping_documentation(self) -> Dict[str, Any]:
        """
        Generate documentation about the schema mapping.

        Returns:
            Schema mapping documentation
        """
        return {
            'sqlite_to_json_mapping': {
                'emails_table': {
                    'id': {'type': 'INTEGER PRIMARY KEY', 'maps_to': 'id', 'json_type': 'number'},
                    'message_id': {'type': 'TEXT UNIQUE', 'maps_to': 'message_id', 'json_type': 'string'},
                    'subject': {'type': 'TEXT', 'maps_to': 'subject', 'json_type': 'string'},
                    'sender': {'type': 'TEXT', 'maps_to': 'sender', 'json_type': 'string'},
                    'sender_email': {'type': 'TEXT', 'maps_to': 'sender_email', 'json_type': 'string'},
                    'content': {'type': 'TEXT', 'maps_to': 'content', 'json_type': 'string'},
                    'content_html': {'type': 'TEXT', 'maps_to': 'content_html', 'json_type': 'string'},
                    'category_id': {'type': 'INTEGER FK', 'maps_to': 'category_id', 'json_type': 'number'},
                    'is_unread': {'type': 'BOOLEAN', 'maps_to': 'is_unread', 'json_type': 'boolean'},
                    'analysis_metadata': {'type': 'TEXT (JSON)', 'maps_to': 'analysis_metadata', 'json_type': 'object'},
                    'created_at': {'type': 'TIMESTAMP', 'maps_to': 'created_at', 'json_type': 'string'},
                    'updated_at': {'type': 'TIMESTAMP', 'maps_to': 'updated_at', 'json_type': 'string'},
                    'category_name': {'source': 'JOIN categories.name', 'maps_to': 'categoryName', 'json_type': 'string'},
                    'category_color': {'source': 'JOIN categories.color', 'maps_to': 'categoryColor', 'json_type': 'string'}
                },
                'categories_table': {
                    'id': {'type': 'INTEGER PRIMARY KEY', 'maps_to': 'id', 'json_type': 'number'},
                    'name': {'type': 'TEXT', 'maps_to': 'name', 'json_type': 'string'},
                    'description': {'type': 'TEXT', 'maps_to': 'description', 'json_type': 'string'},
                    'color': {'type': 'TEXT', 'maps_to': 'color', 'json_type': 'string'},
                    'count': {'type': 'INTEGER', 'maps_to': 'count', 'json_type': 'number'}
                },
                'users_table': {
                    'id': {'type': 'INTEGER PRIMARY KEY', 'maps_to': 'id', 'json_type': 'number'},
                    'username': {'type': 'TEXT UNIQUE', 'maps_to': 'username', 'json_type': 'string'},
                    'email': {'type': 'TEXT UNIQUE', 'maps_to': 'email', 'json_type': 'string'},
                    'created_at': {'type': 'TIMESTAMP', 'maps_to': 'created_at', 'json_type': 'string'}
                }
            },
            'data_transformations': [
                'analysis_metadata TEXT field parsed as JSON object',
                'is_unread INTEGER converted to boolean',
                'Timestamps converted to ISO format strings',
                'Category information joined and flattened into email records'
            ],
            'potential_issues': [
                'Large content fields may impact JSON file size',
                'analysis_metadata JSON parsing errors handled gracefully',
                'Foreign key relationships preserved but denormalized in JSON'
            ]
        }


def main():
    """Main entry point for the migration script."""
    parser = argparse.ArgumentParser(description='Migrate data from SQLite to JSON format')
    parser.add_argument('--sqlite-db', required=True, help='Path to SQLite database file')
    parser.add_argument('--output-dir', required=True, help='Output directory for JSON files')
    parser.add_argument('--validate-only', action='store_true', help='Only validate migration without saving files')

    args = parser.parse_args()

    try:
        migrator = SQLiteToJSONMigrator(args.sqlite_db, args.output_dir)

        if args.validate_only:
            # Just validate the database
            stats = migrator.get_database_stats()
            logger.info(f"Database validation successful. Stats: {stats}")
        else:
            # Perform full migration
            result = migrator.migrate_all()
            logger.info(f"Migration completed. Report saved to: {result}")

    except DataMigrationError as e:
        logger.error(f"Migration error: {e}")
        exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        exit(1)


if __name__ == '__main__':
    main()