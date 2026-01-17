
import pytest
import asyncio
from unittest.mock import MagicMock, patch
from src.core.database import DatabaseManager, DatabaseConfig, FIELD_ID, FIELD_SUBJECT

@pytest.mark.asyncio
async def test_search_emails_uses_content_index():
    # Setup
    config = DatabaseConfig(data_dir="test_data_search_opt")
    db = DatabaseManager(config)

    # Populate with dummy emails (light data only)
    db.emails_data = [
        {
            FIELD_ID: i,
            FIELD_SUBJECT: "Hello",
            "sender": "John",
            "sender_email": "john@example.com",
            "message_id": f"msg_{i}"
        }
        for i in range(100)
    ]

    # Mock _build_indexes to ensure we start clean (although we just manually populated emails_data)
    # We need to call _build_indexes to populate emails_by_id etc.
    # But we want to simulate _content_available_index being empty initially.

    # Mock os.listdir to return empty list so _content_available_index is empty
    with patch("os.listdir", return_value=[]):
        db._build_indexes()

    assert len(db._content_available_index) == 0

    # Mock os.path.exists
    with patch("os.path.exists") as mock_exists, \
         patch("builtins.open", MagicMock()), \
         patch("gzip.open", MagicMock()):

        mock_exists.return_value = False # Content files don't exist

        # Search for something NOT in subject
        await db.search_emails_with_limit("FindMe", limit=10)

        # Since _content_available_index is empty, it should NOT check disk
        assert mock_exists.call_count == 0

@pytest.mark.asyncio
async def test_search_emails_checks_disk_if_in_index():
    # Setup
    config = DatabaseConfig(data_dir="test_data_search_opt_2")
    db = DatabaseManager(config)

    db.emails_data = [
        {
            FIELD_ID: 1,
            FIELD_SUBJECT: "Hello",
            "sender": "John",
            "sender_email": "john@example.com",
            "message_id": "msg_1"
        }
    ]

    # Manually populate index
    db._content_available_index.add(1)
    db._build_indexes() # rebuilding will wipe it if we don't mock listdir.
    # But wait, _build_indexes rebuilds it from disk.

    # Let's mock listdir to return file for ID 1
    with patch("os.listdir", return_value=["1.json.gz"]):
        db._build_indexes()

    assert 1 in db._content_available_index

    # Mock os.path.exists
    with patch("os.path.exists") as mock_exists, \
         patch("builtins.open", MagicMock()), \
         patch("gzip.open", MagicMock()) as mock_gzip:

        mock_exists.return_value = True

        # Setup mock content to match query
        mock_content = '{"content": "FindMe here"}'

        file_obj = MagicMock()
        mock_gzip.return_value.__enter__.return_value = file_obj

        # We can patch json.load instead
        with patch("json.load", return_value={"content": "FindMe here"}):
             results = await db.search_emails_with_limit("FindMe", limit=10)

        # Should have checked disk because it was in index
        # And because we mocked exists=True.
        # Note: logic is: if in index -> check exists -> open.
        # Actually my code does: if in index -> continue? No.
        # if email_id not in self._content_available_index: continue
        # So if in index, it proceeds to check exists.

        # Wait, strictly speaking, if we trust index, we might skip exists check?
        # But my implementation kept exists check.
        # So it SHOULD call exists.

        # The exact implementation:
        # if email_id not in self._content_available_index: continue
        # content_path = ...
        # if os.path.exists(content_path): ...

        # So verify exists is called (or at least we got result)
        assert len(results) == 1
        assert results[0][FIELD_ID] == 1
