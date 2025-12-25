import pytest
import asyncio
import os
import json
import gzip
from unittest.mock import MagicMock, AsyncMock, patch
from src.core.database import DatabaseManager, DatabaseConfig, FIELD_CONTENT, FIELD_ID, FIELD_CREATED_AT

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
async def test_search_emails_offloads_io(db_manager, tmp_path):
    """Test that search offloads file I/O to a thread."""
    # Setup
    email_id = 2
    email_light = {FIELD_ID: email_id, "subject": "Test Subject 2"}
    db_manager.emails_data = [email_light]

    # Mock cache miss
    db_manager.caching_manager.get_email_content.return_value = None

    # Create real file
    content_dir = tmp_path / "data" / "email_content"
    content_dir.mkdir(parents=True, exist_ok=True)
    content_path = content_dir / f"{email_id}.json.gz"

    heavy_data = {FIELD_CONTENT: "This has the hidden keyword"}
    with gzip.open(content_path, "wt", encoding="utf-8") as f:
        json.dump(heavy_data, f)

    # Spy on asyncio.to_thread
    with patch("asyncio.to_thread", side_effect=asyncio.to_thread) as mock_to_thread:
        # Execute
        results = await db_manager.search_emails_with_limit("hidden", limit=10)

        # Verify
        assert len(results) == 1
        assert results[0][FIELD_ID] == email_id

        # Verify to_thread was called with the helper
        found_call = False
        for call in mock_to_thread.call_args_list:
            if call.args and getattr(call.args[0], "__name__", "") == "_read_content_sync":
                found_call = True
                break

        assert found_call, "asyncio.to_thread should have been called with _read_content_sync"

@pytest.mark.asyncio
async def test_search_emails_stops_early(db_manager):
    """Test that search stops processing once limit is reached."""
    # Setup many emails that match the content search
    limit = 5
    total_emails = 50
    emails = []
    for i in range(total_emails):
        emails.append({
            FIELD_ID: i,
            "subject": "Generic Subject",
            FIELD_CREATED_AT: f"2023-01-{i+1:02d}T00:00:00Z" # Sorted by date ascending
        })

    # Sort descending to match _get_sorted_emails order (which we use in search_emails_with_limit)
    emails.reverse()

    db_manager.emails_data = emails
    db_manager._build_indexes()

    # Mock content cache miss
    db_manager.caching_manager.get_email_content.return_value = None

    # Mock content read to always match "secret"
    with patch.object(db_manager, '_read_content_sync', return_value={FIELD_CONTENT: "secret content"}) as mock_read:
        with patch("os.path.exists", return_value=True):
             results = await db_manager.search_emails_with_limit("secret", limit=limit)

    assert len(results) == limit
    # With early exit, we should only inspect 'limit' emails because they all match
    assert mock_read.call_count == limit
