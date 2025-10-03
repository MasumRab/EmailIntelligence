import pytest
import asyncio
from server.python_backend.database import DatabaseManager

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
    category_data = {"name": "Test Category", "description": "A category for testing", "color": "#123456"}
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
    # 1. Create a category
    category_data = {"name": "Work", "description": "Work emails", "color": "#aabbcc"}
    work_category = await db_manager.create_category(category_data)
    assert work_category["count"] == 0

    # 2. Create an email in that category
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
    created_email = await db_manager.create_email(email_data)
    assert created_email is not None
    assert created_email["category_id"] == work_category["id"]

    # 3. Verify the category count was incremented
    all_categories = await db_manager.get_all_categories()
    assert len(all_categories) == 1
    assert all_categories[0]["id"] == work_category["id"]
    assert all_categories[0]["count"] == 1

@pytest.mark.asyncio
async def test_create_duplicate_email_updates(db_manager: DatabaseManager):
    """Test that creating an email with a duplicate message_id updates the existing record."""
    email_data_v1 = {
        "message_id": "duplicate_msg",
        "thread_id": "thread_dup",
        "subject": "Original Subject",
        "sender": "sender@example.com",
        "sender_email": "sender@example.com",
        "content": "Original content.",
        "preview": "Original content.",
        "time": "2025-01-02T10:00:00Z",
    }
    created_email_v1 = await db_manager.create_email(email_data_v1)
    assert created_email_v1["subject"] == "Original Subject"
    assert "id" in created_email_v1

    email_data_v2 = {
        "message_id": "duplicate_msg",
        "thread_id": "thread_dup",
        "subject": "Updated Subject", # Changed field
        "sender": "sender@example.com",
        "sender_email": "sender@example.com",
        "content": "Updated content.", # Changed field
        "preview": "Updated content.",
        "time": "2025-01-02T10:00:00Z",
    }
    updated_email = await db_manager.create_email(email_data_v2)

    assert updated_email is not None
    assert updated_email["id"] == created_email_v1["id"] # Should be the same email record
    assert updated_email["subject"] == "Updated Subject"
    assert updated_email["content"] == "Updated content."

    # Verify there's still only one email in the database
    async with db_manager.get_cursor() as cur:
        await cur.execute("SELECT COUNT(*) FROM emails WHERE message_id = ?", ("duplicate_msg",))
        count = await cur.fetchone()
        assert count[0] == 1

@pytest.mark.asyncio
async def test_category_caching(db_manager: DatabaseManager, caplog):
    """Test that categories are cached after the first fetch."""
    # 1. First call, should fetch from DB
    with caplog.at_level("INFO"):
        categories1 = await db_manager.get_all_categories()
        assert "Fetching categories from database" in caplog.text
        assert db_manager._category_cache is not None

    # 2. Second call, should use cache
    caplog.clear()
    with caplog.at_level("INFO"):
        categories2 = await db_manager.get_all_categories()
        assert "Returning categories from cache" in caplog.text
        assert "Fetching categories from database" not in caplog.text
        assert categories1 == categories2

@pytest.mark.asyncio
async def test_cache_invalidation_on_create(db_manager: DatabaseManager):
    """Test that the category cache is invalidated on create."""
    # 1. Populate cache
    await db_manager.get_all_categories()
    assert db_manager._category_cache is not None

    # 2. Create a new category
    await db_manager.create_category({"name": "New Category", "color": "#ffffff"})

    # 3. Check that cache is now None
    assert db_manager._category_cache is None

@pytest.mark.asyncio
async def test_cache_invalidation_on_update(db_manager: DatabaseManager):
    """Test that the category cache is invalidated on update."""
    # 1. Create a category and populate cache
    cat = await db_manager.create_category({"name": "Work", "color": "#ffffff"})
    await db_manager.get_all_categories()
    assert db_manager._category_cache is not None
    assert db_manager._category_cache[0]["count"] == 0

    # 2. Create an email, which triggers _update_category_count
    email_data = {
        "message_id": "test_msg_cache", "subject": "Test", "sender": "t@e.com",
        "sender_email": "t@e.com", "content": "Test", "preview": "Test",
        "time": "2025-01-01T12:00:00Z", "category_id": cat["id"],
    }
    await db_manager.create_email(email_data)

    # 3. Check that cache is invalidated
    assert db_manager._category_cache is None

    # 4. Fetch again and check for updated count
    categories = await db_manager.get_all_categories()
    assert len(categories) == 1
    assert categories[0]["count"] == 1