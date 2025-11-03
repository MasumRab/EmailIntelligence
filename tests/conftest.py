import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
import subprocess
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient

from src.main import create_app
from src.core.database import get_db

try:
    from src.core.factory import get_data_source
    HAS_NOTMUCH = True
except ImportError:
    HAS_NOTMUCH = False
    get_data_source = None


@pytest.fixture(scope="session", autouse=True)
def download_nltk_data():
    """Download NLTK data before running tests."""
    packages = ["punkt", "stopwords"]
    for package in packages:
        subprocess.run([sys.executable, "-m", "nltk.downloader", package], check=True)
    subprocess.run([sys.executable, "-m", "textblob.download_corpora"], check=True)


@pytest.fixture
def mock_db_manager():
    """
    Provides a mock DatabaseManager instance.
    This mock is reset for each test function, ensuring test isolation.
    """
    mock = AsyncMock()
    # Pre-configure all database methods as AsyncMocks
    mock.get_all_categories = AsyncMock()
    mock.create_category = AsyncMock()
    mock.get_email_by_id = AsyncMock()
    mock.get_all_emails = AsyncMock()
    mock.search_emails = AsyncMock()
    mock.get_emails_by_category = AsyncMock()
    mock.create_email = AsyncMock()
    mock.update_email = AsyncMock()
    mock.get_dashboard_stats = AsyncMock()
    mock.get_recent_emails = AsyncMock()
    return mock


@pytest.fixture
def client(mock_db_manager: AsyncMock):
    """
    Provides a TestClient with the database dependency overridden.
    This fixture ensures that API endpoints use the mock_db_manager instead of a real database.
    """
    app = create_app()
    app.dependency_overrides[get_db] = lambda: mock_db_manager
    if HAS_NOTMUCH:
        app.dependency_overrides[get_data_source] = lambda: mock_db_manager

    with TestClient(app) as test_client:
        yield test_client

    del app.dependency_overrides[get_db]
    if HAS_NOTMUCH:
        del app.dependency_overrides[get_data_source]
