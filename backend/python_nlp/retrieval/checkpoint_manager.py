"""
Module for managing sync checkpoints in email retrieval.
"""

import json
import logging
import os
import sqlite3
from datetime import datetime
from typing import Optional

from .retrieval_models import SyncCheckpoint

# Define the project's root directory and default path for the checkpoint database
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_CHECKPOINT_DB_PATH = os.path.join(PROJECT_ROOT, "data", "sync_checkpoints.db")


class CheckpointManager:
    """
    Manages synchronization checkpoints for email retrieval.
    """

    def __init__(self, db_path: str = DEFAULT_CHECKPOINT_DB_PATH):
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
                CREATE TABLE IF NOT EXISTS sync_checkpoints (
                    strategy_name TEXT PRIMARY KEY,
                    last_sync_date TEXT NOT NULL,
                    last_history_id TEXT,
                    processed_count INTEGER DEFAULT 0,
                    next_page_token TEXT,
                    errors_count INTEGER DEFAULT 0
                )
            ''')
            conn.commit()

    def save_checkpoint(self, checkpoint: SyncCheckpoint) -> bool:
        """
        Save a synchronization checkpoint to the database.

        Args:
            checkpoint: The SyncCheckpoint object to save.

        Returns:
            True if the operation was successful, False otherwise.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO sync_checkpoints (
                        strategy_name, last_sync_date, last_history_id, 
                        processed_count, next_page_token, errors_count
                    ) VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    checkpoint.strategy_name,
                    checkpoint.last_sync_date.isoformat(),
                    checkpoint.last_history_id,
                    checkpoint.processed_count,
                    checkpoint.next_page_token,
                    checkpoint.errors_count
                ))
                conn.commit()
            return True
        except Exception as e:
            logging.error(f"Error saving checkpoint for strategy {checkpoint.strategy_name}: {e}")
            return False

    def get_checkpoint(self, strategy_name: str) -> Optional[SyncCheckpoint]:
        """
        Retrieve a synchronization checkpoint from the database.

        Args:
            strategy_name: The name of the strategy whose checkpoint to retrieve.

        Returns:
            The SyncCheckpoint object if found, None otherwise.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM sync_checkpoints WHERE strategy_name = ?
                ''', (strategy_name,))
                row = cursor.fetchone()
                if row:
                    return SyncCheckpoint(
                        strategy_name=row[0],
                        last_sync_date=datetime.fromisoformat(row[1]),
                        last_history_id=row[2],
                        processed_count=row[3],
                        next_page_token=row[4],
                        errors_count=row[5]
                    )
            return None
        except Exception as e:
            logging.error(f"Error retrieving checkpoint for strategy {strategy_name}: {e}")
            return None

    def update_checkpoint(self, strategy_name: str, **updates) -> bool:
        """
        Update specific fields of a synchronization checkpoint.

        Args:
            strategy_name: The name of the strategy whose checkpoint to update.
            **updates: Key-value pairs of fields to update.

        Returns:
            True if the operation was successful, False otherwise.
        """
        try:
            # Get the current checkpoint
            current_checkpoint = self.get_checkpoint(strategy_name)
            if not current_checkpoint:
                # If no checkpoint exists, create a new one with default values
                current_checkpoint = SyncCheckpoint(
                    strategy_name=strategy_name,
                    last_sync_date=datetime.now(),
                    last_history_id="",
                    processed_count=0,
                    next_page_token=None,
                    errors_count=0
                )

            # Update the fields with the provided values
            for field, value in updates.items():
                if hasattr(current_checkpoint, field):
                    setattr(current_checkpoint, field, value)

            # Save the updated checkpoint
            return self.save_checkpoint(current_checkpoint)
        except Exception as e:
            logging.error(f"Error updating checkpoint for strategy {strategy_name}: {e}")
            return False