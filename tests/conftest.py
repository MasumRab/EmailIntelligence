"""
Pytest configuration and fixtures for EmailIntelligence CLI tests.
"""

import pytest
import asyncio
import shutil
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, AsyncMock

from src.core.config import settings
from src.core.interfaces import IMetadataStore, IConflictDetector


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def temp_repo(temp_dir):
    """Create a temporary git repository."""
    repo_path = temp_dir / "test_repo"
    repo_path.mkdir()
    
    # Initialize git repo (mock or real depending on test needs)
    # For unit tests, we often just need the directory structure
    (repo_path / ".git").mkdir()
    
    return repo_path


@pytest.fixture
def mock_metadata_store():
    """Create a mock metadata store."""
    store = MagicMock(spec=IMetadataStore)
    store.save_conflict = AsyncMock(return_value="conflict-123")
    store.get_conflict = AsyncMock(return_value=None)
    store.save_analysis = AsyncMock(return_value="conflict-123")
    store.get_analysis = AsyncMock(return_value=None)
    return store


@pytest.fixture
def mock_conflict_detector():
    """Create a mock conflict detector."""
    detector = MagicMock(spec=IConflictDetector)
    detector.detect_conflicts = AsyncMock(return_value=[])
    detector.detect_conflicts_between_branches = AsyncMock(return_value=[])
    return detector


@pytest.fixture
def test_settings():
    """Override settings for testing."""
    original_env = settings.environment
    settings.environment = "testing"
    settings.metadata_storage_backend = "file"
    
    yield settings
    
    settings.environment = original_env
