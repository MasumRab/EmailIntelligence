import os
import sys
import configparser

# Monkey-patch for notmuch library compatibility with Python 3.12+
configparser.SafeConfigParser = configparser.ConfigParser

# Set a dummy SECRET_KEY for testing purposes
os.environ["SECRET_KEY"] = "test_secret_key"

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
import subprocess
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from fastapi import FastAPI

from src.main import create_app
from src.core.database import get_db
from src.core.factory import get_data_source


@pytest.fixture(scope="session", autouse=True)
def download_nltk_data():
    """Download NLTK data before running tests."""
    try:
        import nltk
        # Use NLTK's programmatic download for better reliability
        packages = ["punkt", "punkt_tab", "stopwords", "wordnet", "averaged_perceptron_tagger"]
        for package in packages:
            try:
                nltk.download(package, quiet=True)
            except Exception as e:
                # Some packages might fail, continue with others
                pass
    except ImportError:
        # NLTK not available, skip
        pass

    # Download TextBlob corpora if textblob is available
    try:
        import textblob
        try:
            # Use textblob's programmatic download
            from textblob import download_corpora
            download_corpora()
        except Exception as e:
            # Try command line approach as fallback
            try:
                subprocess.run([sys.executable, "-c", "from textblob import download_corpora; download_corpora()"],
                             check=True, timeout=60)
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                # TextBlob corpora download failed - skip silently
                pass
    except ImportError:
        # TextBlob not available, skip
        pass


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


from src.core.auth import get_current_active_user


from src.core.factory import get_email_repository


@pytest.fixture
def client(mock_db_manager: AsyncMock):
    """
    Provides a TestClient with the database dependency overridden.
    This fixture ensures that API endpoints use the mock_db_manager instead of a real database.
    """
    app = create_app()

    def get_test_user():
        return {"username": "testuser", "role": "admin"}

    async def get_mock_dashboard_aggregates():
        return {
            "total_emails": 100,
            "unread_count": 10,
            "auto_labeled": 50,
            "categories_count": 5,
            "weekly_growth": {"emails": 10, "percentage": 0.1},
        }

    async def get_mock_category_breakdown(limit: int):
        return {"Test": 10}

    mock_email_repository = AsyncMock()
    mock_email_repository.get_dashboard_aggregates.side_effect = get_mock_dashboard_aggregates
    mock_email_repository.get_category_breakdown.side_effect = get_mock_category_breakdown

    app.dependency_overrides[get_db] = lambda: mock_db_manager
    app.dependency_overrides[get_data_source] = lambda: mock_db_manager
    app.dependency_overrides[get_current_active_user] = get_test_user
    app.dependency_overrides[get_email_repository] = lambda: mock_email_repository

    with TestClient(app) as test_client:
        yield test_client

    del app.dependency_overrides[get_db]
    del app.dependency_overrides[get_data_source]
    del app.dependency_overrides[get_current_active_user]
    del app.dependency_overrides[get_email_repository]
