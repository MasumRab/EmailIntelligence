import asyncio
import unittest
from unittest.mock import MagicMock, patch
import pytest
from src.core.database import DatabaseManager

class TestDatabaseSearchPerformance(unittest.TestCase):
    def setUp(self):
        # Mock the config object expected by DatabaseManager
        mock_config = MagicMock()
        mock_config.emails_file = ":memory:"
        mock_config.index_file = ":memory:"

        self.db_manager = DatabaseManager(mock_config)

        # Initialize internal structures
        self.db_manager.index = {
            "msg1": {"id": "msg1", "date": "2023-01-01", "subject": "Test 1", "file_path": "/tmp/1.json"},
            "msg2": {"id": "msg2", "date": "2023-01-02", "subject": "Test 2", "file_path": "/tmp/2.json"},
            "msg3": {"id": "msg3", "date": "2023-01-03", "subject": "Test 3", "file_path": "/tmp/3.json"},
            "msg4": {"id": "msg4", "date": "2023-01-04", "subject": "Test 4", "file_path": "/tmp/4.json"},
            "msg5": {"id": "msg5", "date": "2023-01-05", "subject": "Test 5", "file_path": "/tmp/5.json"},
        }
        self.db_manager.email_cache = {}
        for mid, data in self.db_manager.index.items():
            self.db_manager.email_cache[mid] = data

        # Also populate emails_data which is used by the optimized search
        self.db_manager.emails_data = [
            {"id": 1, "created_at": "2023-01-01", "subject": "Test 1", "message_id": "msg1"},
            {"id": 2, "created_at": "2023-01-02", "subject": "Test 2", "message_id": "msg2"},
            {"id": 3, "created_at": "2023-01-03", "subject": "Test 3", "message_id": "msg3"},
            {"id": 4, "created_at": "2023-01-04", "subject": "Test 4", "message_id": "msg4"},
            {"id": 5, "created_at": "2023-01-05", "subject": "Test 5", "message_id": "msg5"},
        ]
        self.db_manager.email_content_dir = "/tmp"

    @patch("src.core.database.os.path.exists", return_value=True)
    @patch("src.core.database.json.load", return_value={"id": "test", "subject": "match", "content": "this matches the query"})
    @patch("src.core.database.gzip.open")
    def test_search_limit_optimization(self, mock_gzip_open, mock_json_load, mock_exists):
        """
        Verify that search_emails_with_limit stops reading files once limit is reached.
        """
        mock_file = MagicMock()
        mock_file.__enter__.return_value = mock_file
        mock_gzip_open.return_value = mock_file

        # Note: DatabaseManager sorts by date desc (newest first).
        # So it should process msg5, msg4, then stop.

        criteria = "match"
        results = asyncio.run(self.db_manager.search_emails_with_limit(criteria, limit=2))

        self.assertEqual(len(results), 2)

        # Verify file open count
        # We expect at most 2 opens because the first 2 sorted messages (msg5, msg4) match.
        self.assertLessEqual(mock_gzip_open.call_count, 2)

    @patch("src.core.database.os.path.exists", return_value=True)
    @patch("src.core.database.json.load", return_value={"id": "test", "subject": "match", "content": "this matches the query"})
    @patch("src.core.database.gzip.open")
    def test_search_pagination_optimization(self, mock_gzip_open, mock_json_load, mock_exists):
        """Verify offset and limit efficiency."""
        mock_file = MagicMock()
        mock_file.__enter__.return_value = mock_file
        mock_gzip_open.return_value = mock_file

        # Limit 2, Offset 2.
        # Optimized search:
        # 1. Sorts 5 emails.
        # 2. Iterates.
        # 3. Item 1 (msg5): Reads (1 open), Matches. Skipped count 0 < offset 2. Incr skipped.
        # 4. Item 2 (msg4): Reads (2 open), Matches. Skipped count 1 < offset 2. Incr skipped.
        # 5. Item 3 (msg3): Reads (3 open), Matches. Skipped count 2 == offset 2. Add to results.
        # 6. Item 4 (msg2): Reads (4 open), Matches. Add to results.
        # 7. Len results == 2 == limit. Stop.
        # Total opens = 4.

        criteria = "match"
        results = asyncio.run(self.db_manager.search_emails_with_limit(criteria, limit=2, offset=2))

        self.assertEqual(len(results), 2)

        self.assertLessEqual(mock_gzip_open.call_count, 4)
