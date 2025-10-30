"""
Database module for email filter persistence.
"""

import json
import logging
import os
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional

from .filter_models import EmailFilter

# Define paths for data storage
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
DEFAULT_DB_PATH = os.path.join(DATA_DIR, "smart_filters.db")


class FilterDatabase:
    """
    Handles database operations for email filters.
    """

    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        self.db_path = db_path
        self._ensure_directory_exists()
        self._initialize_db()

    def _ensure_directory_exists(self):
        """Ensure the directory for the database file exists."""
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)

    def _initialize_db(self):
        """Initialize the database with the necessary tables."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS filters (
                    filter_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    criteria TEXT NOT NULL,
                    actions TEXT NOT NULL,
                    priority INTEGER DEFAULT 1,
                    effectiveness_score REAL DEFAULT 0.0,
                    created_date TEXT,
                    last_used TEXT,
                    usage_count INTEGER DEFAULT 0,
                    false_positive_rate REAL DEFAULT 0.0,
                    performance_metrics TEXT
                )
            ''')
            conn.commit()

    def save_filter(self, filter_obj: EmailFilter) -> bool:
        """
        Save a filter to the database.

        Args:
            filter_obj: The EmailFilter object to save.

        Returns:
            True if the operation was successful, False otherwise.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO filters (
                        filter_id, name, description, criteria, actions, priority,
                        effectiveness_score, created_date, last_used, usage_count,
                        false_positive_rate, performance_metrics
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    filter_obj.filter_id,
                    filter_obj.name,
                    filter_obj.description,
                    json.dumps(filter_obj.criteria),
                    json.dumps(filter_obj.actions),
                    filter_obj.priority,
                    filter_obj.effectiveness_score,
                    filter_obj.created_date.isoformat() if filter_obj.created_date else None,
                    filter_obj.last_used.isoformat() if filter_obj.last_used else None,
                    filter_obj.usage_count,
                    filter_obj.false_positive_rate,
                    json.dumps(filter_obj.performance_metrics)
                ))
                conn.commit()
            return True
        except Exception as e:
            logging.error(f"Error saving filter {filter_obj.filter_id} to database: {e}")
            return False

    def get_filter(self, filter_id: str) -> Optional[EmailFilter]:
        """
        Retrieve a filter from the database by its ID.

        Args:
            filter_id: The ID of the filter to retrieve.

        Returns:
            The EmailFilter object if found, None otherwise.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM filters WHERE filter_id = ?', (filter_id,))
                row = cursor.fetchone()
                if row:
                    return self._row_to_filter(row)
            return None
        except Exception as e:
            logging.error(f"Error retrieving filter {filter_id} from database: {e}")
            return None

    def get_all_filters(self) -> List[EmailFilter]:
        """
        Retrieve all filters from the database.

        Returns:
            A list of EmailFilter objects.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM filters ORDER BY priority DESC')
                rows = cursor.fetchall()
                return [self._row_to_filter(row) for row in rows]
        except Exception as e:
            logging.error(f"Error retrieving all filters from database: {e}")
            return []

    def delete_filter(self, filter_id: str) -> bool:
        """
        Delete a filter from the database.

        Args:
            filter_id: The ID of the filter to delete.

        Returns:
            True if the operation was successful, False otherwise.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM filters WHERE filter_id = ?', (filter_id,))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            logging.error(f"Error deleting filter {filter_id} from database: {e}")
            return False

    def _row_to_filter(self, row: tuple) -> EmailFilter:
        """
        Convert a database row to an EmailFilter object.

        Args:
            row: A tuple representing a row from the filters table.

        Returns:
            An EmailFilter object.
        """
        return EmailFilter(
            filter_id=row[0],
            name=row[1],
            description=row[2],
            criteria=json.loads(row[3]),
            actions=json.loads(row[4]),
            priority=row[5],
            effectiveness_score=row[6],
            created_date=datetime.fromisoformat(row[7]) if row[7] else None,
            last_used=datetime.fromisoformat(row[8]) if row[8] else None,
            usage_count=row[9],
            false_positive_rate=row[10],
            performance_metrics=json.loads(row[11]) if row[11] else {}
        )

    def update_filter_usage(self, filter_id: str, success: bool = True) -> bool:
        """
        Update usage statistics for a filter.

        Args:
            filter_id: The ID of the filter to update.
            success: Whether the filter application was successful.

        Returns:
            True if the operation was successful, False otherwise.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get current stats
                cursor.execute('SELECT usage_count, last_used FROM filters WHERE filter_id = ?', (filter_id,))
                result = cursor.fetchone()
                if not result:
                    return False
                
                usage_count, last_used = result
                new_usage_count = int(usage_count) + 1 if usage_count else 1
                new_last_used = datetime.now().isoformat()
                
                # Update the record
                cursor.execute('''
                    UPDATE filters 
                    SET last_used = ?, usage_count = ?
                    WHERE filter_id = ?
                ''', (new_last_used, new_usage_count, filter_id))
                conn.commit()
            return True
        except Exception as e:
            logging.error(f"Error updating filter {filter_id} usage: {e}")
            return False