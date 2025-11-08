import pytest
import os
from src.core.database import DatabaseManager, DatabaseConfig

def test_database_manager_legacy_mode():
    """Tests that DatabaseManager initializes correctly in legacy mode."""
    # Act
    db_legacy = DatabaseManager()

    # Assert
    assert db_legacy.emails_file.endswith('data/emails.json.gz'), "Legacy path incorrect"

def test_database_manager_config_mode(tmp_path):
    """Tests that DatabaseManager initializes correctly with a config object."""
    # Arrange
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    config = DatabaseConfig(
        data_dir=str(data_dir),
        emails_file=str(data_dir / 'test_emails.json.gz'),
        categories_file=str(data_dir / 'test_categories.json.gz'),
        users_file=str(data_dir / 'test_users.json.gz')
    )

    # Act
    db_config = DatabaseManager(config)

    # Assert
    assert db_config.emails_file == str(data_dir / 'test_emails.json.gz'), "Config mode failed"

@pytest.mark.asyncio
async def test_database_manager_data_operations(tmp_path):
    """Tests that basic data operations can be performed without errors."""
    # Arrange
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    config = DatabaseConfig(
        data_dir=str(data_dir),
        emails_file=str(data_dir / 'test_emails.json.gz'),
        categories_file=str(data_dir / 'test_categories.json.gz'),
        users_file=str(data_dir / 'test_users.json.gz')
    )
    db = DatabaseManager(config)

    # Act & Assert
    try:
        await db.get_all_emails()
        await db.create_email({"messageId": "test-id-123", "subject": "test"})
        await db.shutdown()
    except Exception as e:
        pytest.fail(f"Data operations test failed with an exception: {e}")
