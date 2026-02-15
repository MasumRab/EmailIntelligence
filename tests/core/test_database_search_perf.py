import pytest
import asyncio
import os
import json
import gzip
from unittest.mock import MagicMock, AsyncMock, patch
from src.core.database import DatabaseManager, DatabaseConfig, FIELD_CONTENT, FIELD_ID

@pytest.fixture
def db_config(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    return DatabaseConfig(data_dir=str(data_dir))

@pytest.fixture
def db_manager(db_config):
    manager = DatabaseManager(config=db_config)
    # Mock caching manager to isolate behavior
    manager.caching_manager = MagicMock()
    manager.caching_manager.get_email_content.return_value = None
    manager.caching_manager.get_query_result.return_value = None
    manager.emails_data = []
    manager.emails_by_id = {}
    # Ensure initialized to avoid side effects
    manager._initialized = True
    return manager

@pytest.mark.asyncio
async def test_search_emails_uses_cache(db_manager):
    """Test that search checks cache before hitting disk."""
    # Setup
    email_id = 1
    email_light = {FIELD_ID: email_id, "subject": "Test Subject"}
    db_manager.emails_data = [email_light]

    # Mock cache hit
    cached_content = {FIELD_CONTENT: "This contains the secret keyword"}
    db_manager.caching_manager.get_email_content.return_value = cached_content

    # Mock disk path existence to ensure we rely on cache and not fall through
    with patch("os.path.exists", return_value=True) as mock_exists:
        # Execute
        results = await db_manager.search_emails_with_limit("secret", limit=10)

    # Verify
    assert len(results) == 1
    assert results[0][FIELD_ID] == email_id
    # Verify cache was checked
    db_manager.caching_manager.get_email_content.assert_called_with(email_id)

@pytest.mark.asyncio
async def test_search_emails_yields_periodically(db_manager, tmp_path):
    """Test that search uses sync I/O and yields periodically."""
    # Setup - Create enough emails to trigger yield
    # SEARCH_YIELD_FREQUENCY is 10, so we need more than 10 processed items
    num_emails = 15
    db_manager.emails_data = []

    content_dir = tmp_path / "data" / "email_content"
    content_dir.mkdir(parents=True, exist_ok=True)

    for i in range(num_emails):
        email_id = i + 100
        email_light = {FIELD_ID: email_id, "subject": f"Subject {i}"}
        db_manager.emails_data.append(email_light)

        # Create real content file
        content_path = content_dir / f"{email_id}.json.gz"
        heavy_data = {FIELD_CONTENT: f"Content for {i} without keyword"}

        # The last one will have the keyword
        if i == num_emails - 1:
            heavy_data[FIELD_CONTENT] = "This has the hidden keyword"

        with gzip.open(content_path, "wt", encoding="utf-8") as f:
            json.dump(heavy_data, f)

    # Mock cache miss for all
    db_manager.caching_manager.get_email_content.return_value = None

    # Spy on asyncio.sleep and to_thread
    with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep, \
         patch("asyncio.to_thread", side_effect=asyncio.to_thread) as mock_to_thread:

        # Execute
        results = await db_manager.search_emails_with_limit("hidden", limit=10)

        # Verify
        assert len(results) == 1
        assert results[0][FIELD_ID] == num_emails - 1 + 100

        # Verify asyncio.sleep(0) was called at least once (since 15 > 10)
        assert mock_sleep.call_count >= 1
        mock_sleep.assert_called_with(0)

        # Verify to_thread was NOT called with _read_content_sync
        found_call = False
        for call in mock_to_thread.call_args_list:
            if call.args and getattr(call.args[0], "__name__", "") == "_read_content_sync":
                found_call = True
                break

        assert not found_call, "asyncio.to_thread should NOT have been called with _read_content_sync"
