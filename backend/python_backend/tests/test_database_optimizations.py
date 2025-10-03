import asyncio
import os
import json
import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, patch

from backend.python_backend.database import DatabaseManager, get_db

# Mark all tests in this file as asyncio
pytestmark = pytest.mark.asyncio

@pytest_asyncio.fixture
async def fresh_db():
    """Fixture to provide a fresh, isolated DatabaseManager instance for each test."""
    # Use a temporary directory for test data
    temp_data_dir = "backend/python_backend/tests/temp_data"
    if not os.path.exists(temp_data_dir):
        os.makedirs(temp_data_dir)

    emails_file = os.path.join(temp_data_dir, "test_emails.json")
    categories_file = os.path.join(temp_data_dir, "test_categories.json")
    users_file = os.path.join(temp_data_dir, "test_users.json")

    # Clean up any old test files
    for f in [emails_file, categories_file, users_file]:
        if os.path.exists(f):
            os.remove(f)

    db = DatabaseManager()
    db.emails_file = emails_file
    db.categories_file = categories_file
    db.users_file = users_file

    await db._ensure_initialized()

    yield db

    # Teardown: clean up the test files
    await db.shutdown() # Ensure data is written before cleanup if needed
    for f in [emails_file, categories_file, users_file]:
        if os.path.exists(f):
            os.remove(f)
    if os.path.exists(temp_data_dir):
        os.rmdir(temp_data_dir)


class TestDatabaseOptimizations:
    async def test_in_memory_indexing(self, fresh_db: DatabaseManager):
        """Test if in-memory indexes are built and used correctly."""
        # 1. Create a category and an email
        cat_data = {"name": "Test Category", "color": "#FF0000"}
        created_cat = await fresh_db.create_category(cat_data)
        assert created_cat is not None

        email_data = {
            "message_id": "test_msg_123",
            "subject": "Test Subject",
            "sender": "test@example.com",
            "content": "Test content",
            "category_id": created_cat['id'],
        }
        created_email = await fresh_db.create_email(email_data)
        assert created_email is not None

        # 2. Verify indexes are populated
        assert created_email['id'] in fresh_db.emails_by_id
        assert "test_msg_123" in fresh_db.emails_by_message_id
        assert created_cat['id'] in fresh_db.categories_by_id
        assert "test category" in fresh_db.categories_by_name

        # 3. Test direct lookup via indexes
        retrieved_by_id = await fresh_db.get_email_by_id(created_email['id'])
        assert retrieved_by_id is not None
        assert retrieved_by_id['id'] == created_email['id']

        retrieved_by_msg_id = await fresh_db.get_email_by_message_id("test_msg_123")
        assert retrieved_by_msg_id is not None
        assert retrieved_by_msg_id['message_id'] == "test_msg_123"

    async def test_incremental_category_counts(self, fresh_db: DatabaseManager):
        """Test that category counts are updated incrementally."""
        cat_data = {"name": "Promotions", "color": "#00FF00"}
        promo_cat = await fresh_db.create_category(cat_data)
        assert promo_cat is not None
        promo_cat_id = promo_cat['id']

        # Initial count should be 0
        assert fresh_db.category_counts[promo_cat_id] == 0

        # Add an email to the category
        await fresh_db.create_email({"message_id": "promo1", "category_id": promo_cat_id})
        assert fresh_db.category_counts[promo_cat_id] == 1

        # Add another email
        await fresh_db.create_email({"message_id": "promo2", "category_id": promo_cat_id})
        assert fresh_db.category_counts[promo_cat_id] == 2

        # Update an email, moving it out of the category
        email_to_update = await fresh_db.get_email_by_message_id("promo1")
        other_cat = await fresh_db.create_category({"name": "Social"})
        other_cat_id = other_cat['id']

        await fresh_db.update_email(email_to_update['id'], {"category_id": other_cat_id})

        # Check counts of both categories
        assert fresh_db.category_counts[promo_cat_id] == 1
        assert fresh_db.category_counts[other_cat_id] == 1

    async def test_write_behind_cache(self, fresh_db: DatabaseManager):
        """Test the write-behind caching mechanism."""
        # Mock the actual file writing method to check when it's called
        with patch.object(fresh_db, '_save_data_to_file', new_callable=AsyncMock) as mock_save:
            # Create a category - should mark data as dirty but not save immediately
            await fresh_db.create_category({"name": "Dirty Category"})

            # Assert that _save_data_to_file was NOT called
            mock_save.assert_not_called()
            assert 'categories' in fresh_db._dirty_data

            # Now, call shutdown, which should trigger the save
            await fresh_db.shutdown()

            # Assert that _save_data_to_file was called for 'categories'
            mock_save.assert_called_once_with('categories')
            assert not fresh_db._dirty_data # Dirty set should be cleared after shutdown

    async def test_data_persistence_after_shutdown(self, fresh_db: DatabaseManager):
        """Verify that data is correctly persisted to file on shutdown."""
        # 1. Create data
        cat_data = {"name": "Persistent Category", "color": "#123456"}
        created_cat = await fresh_db.create_category(cat_data)
        email_data = {"message_id": "persist_1", "category_id": created_cat['id'], "subject": "Persistence Test"}
        await fresh_db.create_email(email_data)

        # 2. Shutdown the db manager to trigger save
        await fresh_db.shutdown()

        # 3. Manually verify the file content
        assert os.path.exists(fresh_db.emails_file)
        assert os.path.exists(fresh_db.categories_file)

        with open(fresh_db.categories_file, 'r') as f:
            cats_from_file = json.load(f)
        with open(fresh_db.emails_file, 'r') as f:
            emails_from_file = json.load(f)

        assert len(cats_from_file) == 1
        assert cats_from_file[0]['name'] == "Persistent Category"
        # The count is updated in the object but saved on shutdown
        assert cats_from_file[0]['count'] == 1

        assert len(emails_from_file) == 1
        assert emails_from_file[0]['subject'] == "Persistence Test"