import pytest
import asyncio
from unittest.mock import MagicMock, patch
from src.core.database import DatabaseManager, DatabaseConfig, FIELD_ID, FIELD_CREATED_AT, FIELD_CONTENT

@pytest.fixture
def db_config(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    return DatabaseConfig(data_dir=str(data_dir))

@pytest.fixture
def db_manager(db_config):
    manager = DatabaseManager(config=db_config)
    manager.caching_manager = MagicMock()
    # Always miss cache to force disk I/O
    manager.caching_manager.get_email_content.return_value = None
    manager._initialized = True
    return manager

@pytest.mark.asyncio
async def test_search_limit_optimization(db_manager):
    """
    Verifies that search_emails_with_limit stops scanning after finding enough results.
    """
    # Create 100 emails
    emails = []
    for i in range(100):
        emails.append({
            FIELD_ID: i,
            FIELD_CREATED_AT: f"2023-01-01T12:00:{i:02d}", # ensure sorted order helps/hurts
            # No subject/sender, so it MUST check content
        })

    # Pre-sort them in reverse chronological order (newest first)
    # 99, 98, ... 0
    emails.sort(key=lambda x: x[FIELD_CREATED_AT], reverse=True)
    db_manager.emails_data = emails

    # Force _sorted_emails_cache to be populated so we don't test sorting overhead
    db_manager._sorted_emails_cache = list(emails)

    # Mock file existence and content reading
    with patch("os.path.exists", return_value=True):
        # We mock _read_content_sync to return a match
        with patch.object(db_manager, "_read_content_sync") as mock_read:
            mock_read.return_value = {FIELD_CONTENT: "This contains the secret keyword"}

            # Search with limit 10
            results = await db_manager.search_emails_with_limit("secret", limit=10)

            assert len(results) == 10

            # CRITICAL ASSERTION:
            # Current implementation: Iterates ALL emails. Should be 100 calls.
            # Optimized implementation: Should be 10 calls.
            print(f"Read content called {mock_read.call_count} times")

            # We assert the optimization IS present
            # Should be exactly 10 because we stop after finding 10 matches
            assert mock_read.call_count == 10
