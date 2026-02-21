
import pytest
import pytest_asyncio
import asyncio
from unittest.mock import MagicMock, AsyncMock
from src.core.database import DatabaseManager, DatabaseConfig, FIELD_ID, FIELD_CONTENT, FIELD_SUBJECT
from src.core.enhanced_caching import EnhancedCachingManager

@pytest.fixture
def db_config(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    return DatabaseConfig(data_dir=str(data_dir))

@pytest_asyncio.fixture
async def db_manager(db_config):
    manager = DatabaseManager(config=db_config)
    await manager._ensure_initialized()
    return manager

@pytest.mark.asyncio
async def test_search_emails_caches_results(db_manager):
    """Test that search results are cached and reused."""
    # Setup - Create an email that matches
    await db_manager.create_email({
        "subject": "Test Search Subject",
        "sender": "sender@example.com",
        FIELD_CONTENT: "Content with keyword"
    })

    # First search (should miss cache)
    results1 = await db_manager.search_emails_with_limit("keyword", limit=10)
    assert len(results1) == 1

    # Verify it's in cache
    cache_key = "search:keyword:10"
    assert db_manager.caching_manager.get_query_result(cache_key) is not None

    # Verify returned result is a copy (list) not the internal cache object (if implementation supports it)
    cached_obj = db_manager.caching_manager.get_query_result(cache_key)
    # Compare content, allowing type difference (list vs tuple)
    assert tuple(results1) == tuple(cached_obj)
    assert results1 is not cached_obj # Should be a copy/different object

    # Modify cache and verify subsequent search gets modified result
    fake_result = [{"fake": "data"}]
    db_manager.caching_manager.put_query_result(cache_key, fake_result)

    results2 = await db_manager.search_emails_with_limit("keyword", limit=10)
    assert results2 == fake_result
    assert results2 is not fake_result # Should be a copy

@pytest.mark.asyncio
async def test_search_cache_invalidation_on_create(db_manager):
    """Test that search cache is invalidated when new email is created."""
    # Setup
    await db_manager.create_email({
        "subject": "First email",
        FIELD_CONTENT: "keyword"
    })

    # Cache the search
    await db_manager.search_emails_with_limit("keyword", limit=10)
    cache_key = "search:keyword:10"
    assert db_manager.caching_manager.get_query_result(cache_key) is not None

    # Create new email
    await db_manager.create_email({
        "subject": "Second email",
        FIELD_CONTENT: "keyword"
    })

    # Verify cache is cleared
    assert db_manager.caching_manager.get_query_result(cache_key) is None

    # Search again should find both
    results = await db_manager.search_emails_with_limit("keyword", limit=10)
    assert len(results) == 2

@pytest.mark.asyncio
async def test_search_cache_invalidation_on_update(db_manager):
    """Test that search cache is invalidated when email is updated."""
    # Setup
    email = await db_manager.create_email({
        "subject": "First email",
        FIELD_CONTENT: "keyword"
    })
    email_id = email[FIELD_ID]

    # Cache the search
    await db_manager.search_emails_with_limit("keyword", limit=10)
    cache_key = "search:keyword:10"
    assert db_manager.caching_manager.get_query_result(cache_key) is not None

    # Update email
    await db_manager.update_email(email_id, {"subject": "Updated Subject"})

    # Verify cache is cleared
    assert db_manager.caching_manager.get_query_result(cache_key) is None

@pytest.mark.asyncio
async def test_search_cache_case_insensitive_key(db_manager):
    """Test that cache key uses lowercase search term."""
    await db_manager.create_email({
        "subject": "Subject",
        FIELD_CONTENT: "Keyword"
    })

    await db_manager.search_emails_with_limit("Keyword", limit=10)

    # Key should be lowercased
    cache_key = "search:keyword:10"
    assert db_manager.caching_manager.get_query_result(cache_key) is not None

@pytest.mark.asyncio
async def test_search_emails_cache_respects_limit(db_manager):
    """Test that cache keys differ when only the limit changes."""
    # Setup - create more than 10 emails that match the same keyword
    for i in range(12):
        await db_manager.create_email({
            "subject": f"Keyword Email {i}",
            "sender": f"sender{i}@example.com",
            FIELD_CONTENT: "This content includes the keyword term"
        })

    # Warm cache with a smaller limit
    results_limit_5 = await db_manager.search_emails_with_limit("keyword", limit=5)
    assert len(results_limit_5) == 5

    # Call again with a larger limit; results should not be truncated to 5
    results_limit_10 = await db_manager.search_emails_with_limit("keyword", limit=10)
    assert len(results_limit_10) == 10

    # Verify different cache keys were used (implicitly via result count)
    # Check cache keys directly
    assert db_manager.caching_manager.get_query_result("search:keyword:5") is not None
    assert db_manager.caching_manager.get_query_result("search:keyword:10") is not None

    # Ensure the result sets differ, confirming they are not the same cached entry
    ids_limit_5 = {email[FIELD_ID] for email in results_limit_5}
    ids_limit_10 = {email[FIELD_ID] for email in results_limit_10}
    assert ids_limit_5.issubset(ids_limit_10)
    assert ids_limit_5 != ids_limit_10
