<<<<<<< HEAD
import pytest
import asyncio
import os
import time
from src.core.database import DatabaseManager


@pytest.fixture
async def db_manager():
    """Fixture to set up an in-memory SQLite database for testing."""
    manager = DatabaseManager(db_url=":memory:")
    await manager.connect()
    await manager.init_database()
    yield manager
    await manager.close()


@pytest.mark.asyncio
async def test_create_and_get_category(db_manager: DatabaseManager):
    """Test creating and retrieving a category."""
    category_data = {
        "name": "Test Category",
        "description": "A category for testing",
        "color": "#123456",
    }
    created_category = await db_manager.create_category(category_data)

    assert created_category is not None
    assert created_category["name"] == "Test Category"
    assert "id" in created_category

    all_categories = await db_manager.get_all_categories()
    assert len(all_categories) == 1
    assert all_categories[0]["name"] == "Test Category"


@pytest.mark.asyncio
async def test_create_email_and_category_count(db_manager: DatabaseManager):
    """Test that creating an email correctly increments the category count."""
    category_data = {"name": "Work", "description": "Work emails", "color": "#aabbcc"}
    work_category = await db_manager.create_category(category_data)
    assert work_category["count"] == 0

    email_data = {
        "message_id": "test_msg_1",
        "thread_id": "thread_1",
        "subject": "Test Subject",
        "sender": "test@example.com",
        "sender_email": "test@example.com",
        "content": "This is a test email.",
        "preview": "This is a test email.",
        "time": "2025-01-01T12:00:00Z",
        "category_id": work_category["id"],
    }
    await db_manager.create_email(email_data)
    await db_manager._flush_email_cache(force=True)

    all_categories = await db_manager.get_all_categories()
    assert len(all_categories) == 1
    assert all_categories[0]["id"] == work_category["id"]
    assert all_categories[0]["count"] == 1


@pytest.mark.asyncio
async def test_write_behind_cache(db_manager: DatabaseManager):
    """Test the write-behind cache for email creation."""
    email_data = {
        "message_id": "test_cache_1",
        "subject": "Cache Test",
        "sender": "cache@test.com",
        "sender_email": "cache@test.com",
        "content": "Cache content",
        "preview": "Cache preview",
        "time": "2025-01-03T12:00:00Z",
    }
    await db_manager.create_email(email_data)
    assert db_manager._email_write_cache.qsize() == 1

    await db_manager._flush_email_cache(force=True)
    assert db_manager._email_write_cache.empty()

    async with db_manager.get_cursor() as cur:
        await cur.execute("SELECT COUNT(*) FROM emails WHERE message_id = ?", ("test_cache_1",))
        count = await cur.fetchone()
        assert count[0] == 1


@pytest.mark.asyncio
async def test_batch_email_creation(db_manager: DatabaseManager):
    """Test creating a batch of emails."""
    emails_data = [
        {
            "message_id": f"batch_{i}",
            "subject": f"Batch {i}",
            "sender": "batch@test.com",
            "sender_email": "batch@test.com",
            "content": "Batch content",
            "preview": "Batch preview",
            "time": "2025-01-04T12:00:00Z",
        }
        for i in range(5)
    ]
    await db_manager.create_emails_batch(emails_data)
    await db_manager._flush_email_cache(force=True)

    async with db_manager.get_cursor() as cur:
        await cur.execute("SELECT COUNT(*) FROM emails WHERE sender = ?", ("batch@test.com",))
        count = await cur.fetchone()
        assert count[0] == 5


@pytest.mark.asyncio
async def test_batch_email_update(db_manager: DatabaseManager):
    """Test updating a batch of emails."""
    emails_data = [
        {
            "message_id": f"update_{i}",
            "subject": "Update",
            "sender": "update@test.com",
            "sender_email": "update@test.com",
            "content": "Update content",
            "preview": "Update preview",
            "time": "2025-01-05T12:00:00Z",
            "is_read": False,
        }
        for i in range(3)
    ]
    await db_manager.create_emails_batch(emails_data)
    await db_manager._flush_email_cache(force=True)

    async with db_manager.get_cursor() as cur:
        await cur.execute("SELECT id FROM emails WHERE sender = ?", ("update@test.com",))
        rows = await cur.fetchall()
        email_ids = [row[0] for row in rows]

    assert len(email_ids) == 3

    await db_manager.update_emails_batch(email_ids, {"is_read": True})

    async with db_manager.get_cursor() as cur:
        await cur.execute(
            "SELECT COUNT(*) FROM emails WHERE sender = ? AND is_read = 1", ("update@test.com",)
        )
        count = await cur.fetchone()
        assert count[0] == 3


@pytest.mark.asyncio
async def test_database_backup(db_manager: DatabaseManager, tmp_path):
    """Test the database backup functionality."""
    db_manager.db_path = str(tmp_path / "test.db")
    db_manager._backup_dir = str(tmp_path / "backups")
    os.makedirs(db_manager._backup_dir, exist_ok=True)

    # Create a dummy file to back up
    with open(db_manager.db_path, "w") as f:
        f.write("test")

    await db_manager.backup_database()

    backups = os.listdir(db_manager._backup_dir)
    assert len(backups) == 1

    # Should not create another backup immediately
    await db_manager.backup_database()
    assert len(os.listdir(db_manager._backup_dir)) == 1

    # Force another backup by changing the last backup time
    db_manager._last_backup_time = 0
    await db_manager.backup_database()
    assert len(os.listdir(db_manager._backup_dir)) == 2

    # Test cleanup
    db_manager._cleanup_old_backups(keep=1)
    assert len(os.listdir(db_manager._backup_dir)) == 1
=======
>>>>>>> 837f0b4c3be0be620537c058dd8dba25d8ac010d
