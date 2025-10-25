import asyncio
import gzip
import json
import os
from unittest.mock import AsyncMock, mock_open, patch

import pytest
import pytest_asyncio

from backend.python_backend.database import HEAVY_EMAIL_FIELDS, DatabaseManager
from backend.python_backend.performance_monitor import LOG_FILE

# Mark all tests in this file as asyncio
pytestmark = pytest.mark.asyncio


@pytest_asyncio.fixture
async def fresh_db():
    """Fixture to provide a fresh, isolated DatabaseManager instance for each test."""
    import os
    from pathlib import Path

    temp_data_dir = os.getenv("TEMP_DATA_DIR", "backend/python_backend/tests/temp_data")
    content_dir = os.path.join(temp_data_dir, "email_content")
    if not os.path.exists(content_dir):
        os.makedirs(content_dir)

    emails_file = os.path.join(temp_data_dir, "test_emails.json.gz")
    categories_file = os.path.join(temp_data_dir, "test_categories.json.gz")
    users_file = os.path.join(temp_data_dir, "test_users.json.gz")

    # Clean up any old test files
    for f in [emails_file, categories_file, users_file]:
        if os.path.exists(f):
            os.remove(f)
    for f in os.listdir(content_dir):
        os.remove(os.path.join(content_dir, f))

    db = DatabaseManager()
    db.emails_file = emails_file
    db.categories_file = categories_file
    db.users_file = users_file
    db.email_content_dir = content_dir

    await db._ensure_initialized()

    yield db

    # Teardown
    await db.shutdown()
    for f in [emails_file, categories_file, users_file]:
        if os.path.exists(f):
            os.remove(f)
    for f in os.listdir(content_dir):
        os.remove(os.path.join(content_dir, f))
    os.rmdir(content_dir)
    os.rmdir(temp_data_dir)


class TestDatabaseOptimizations:
    async def test_in_memory_indexing(self, fresh_db: DatabaseManager):
        """Test if in-memory indexes are built and used correctly."""
        cat_data = {"name": "Test Category", "color": "#FF0000"}
        created_cat = await fresh_db.create_category(cat_data)
        email_data = {"message_id": "test_msg_123", "subject": "Test Subject"}
        created_email = await fresh_db.create_email(email_data)

        assert created_email["id"] in fresh_db.emails_by_id
        assert "test_msg_123" in fresh_db.emails_by_message_id
        assert created_cat["id"] in fresh_db.categories_by_id

    async def test_incremental_category_counts(self, fresh_db: DatabaseManager):
        """Test that category counts are updated incrementally."""
        promo_cat = await fresh_db.create_category({"name": "Promotions"})
        promo_cat_id = promo_cat["id"]

        await fresh_db.create_email({"message_id": "promo1", "category_id": promo_cat_id})
        assert fresh_db.category_counts[promo_cat_id] == 1

        email_to_update = await fresh_db.get_email_by_message_id("promo1", include_content=False)
        await fresh_db.update_email(email_to_update["id"], {"category_id": None})
        assert fresh_db.category_counts[promo_cat_id] == 0

    async def test_write_behind_cache(self, fresh_db: DatabaseManager):
        """Test the write-behind caching mechanism."""
        with patch.object(fresh_db, "_save_data_to_file", new_callable=AsyncMock) as mock_save:
            await fresh_db.create_category({"name": "Dirty Category"})
            mock_save.assert_not_called()
            await fresh_db.shutdown()
            mock_save.assert_called_once_with("categories")

    async def test_data_persistence_after_shutdown(self, fresh_db: DatabaseManager):
        """Verify that data is correctly persisted to file on shutdown."""
        cat_data = {"name": "Persistent Category", "color": "#123456"}
        created_cat = await fresh_db.create_category(cat_data)
        email_data = {
            "message_id": "persist_1",
            "category_id": created_cat["id"],
            "subject": "Persistence Test",
            "content": "This is the heavy content.",
        }
        created_email = await fresh_db.create_email(email_data)
        email_id = created_email["id"]

        await fresh_db.shutdown()

        assert os.path.exists(fresh_db.emails_file)
        with gzip.open(fresh_db.emails_file, "rt", encoding="utf-8") as f:
            emails_from_file = json.load(f)
        assert len(emails_from_file) == 1
        assert emails_from_file[0]["subject"] == "Persistence Test"
        assert "content" not in emails_from_file[0]

        content_path = fresh_db._get_email_content_path(email_id)
        assert os.path.exists(content_path)
        with gzip.open(content_path, "rt", encoding="utf-8") as f:
            content_from_file = json.load(f)
        assert content_from_file["content"] == "This is the heavy content."

    async def test_hybrid_storage_and_on_demand_loading(self, fresh_db: DatabaseManager):
        """Test separation of heavy/light content and on-demand loading."""
        email_data = {
            "message_id": "hybrid_123",
            "subject": "Hybrid Subject",
            "content": "This is the very large email body.",
            "content_html": "<html><body><p>Large HTML</p></body></html>",
        }
        created_email = await fresh_db.create_email(email_data)
        email_id = created_email["id"]

        in_memory_email = fresh_db.emails_by_id.get(email_id)
        assert in_memory_email is not None
        for field in HEAVY_EMAIL_FIELDS:
            assert field not in in_memory_email

        content_path = fresh_db._get_email_content_path(email_id)
        assert os.path.exists(content_path)

        retrieved_light = await fresh_db.get_email_by_id(email_id, include_content=False)
        assert retrieved_light is not None
        for field in HEAVY_EMAIL_FIELDS:
            assert field not in retrieved_light

        retrieved_full = await fresh_db.get_email_by_id(email_id, include_content=True)
        assert retrieved_full is not None
        assert retrieved_full["content"] == "This is the very large email body."
        assert "Large HTML" in retrieved_full["content_html"]

    async def test_performance_logging(self, fresh_db: DatabaseManager):
        """Verify that the log_performance decorator writes to the log file."""
        with patch("backend.python_backend.performance_monitor.open", mock_open()) as mocked_file:
            await fresh_db.search_emails("test")


            handle = mocked_file()
            written_content = handle.write.call_args[0][0]  # The write call is the JSON + \n
            log_data = json.loads(written_content.rstrip("\n"))

            assert log_data["operation"] == "search_emails"
            assert "duration_seconds" in log_data
            assert isinstance(log_data["duration_seconds"], float)
