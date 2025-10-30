import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
import subprocess
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from fastapi import FastAPI

# Create a minimal test app without gradio dependencies
def create_test_app():
    """Create a minimal FastAPI app for testing without gradio."""
    app = FastAPI(title="Test App", version="1.0.0")

    # Add basic CORS
    from fastapi.middleware.cors import CORSMiddleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add a simple health endpoint
    @app.get("/health")
    async def health():
        return {"status": "healthy"}

    return app

# Use the test app instead of the main app
from tests.conftest import create_test_app as create_app
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


@pytest.fixture
def client(mock_db_manager: AsyncMock):
    """
    Provides a TestClient with the database dependency overridden.
    This fixture ensures that API endpoints use the mock_db_manager instead of a real database.
    """
    app = create_app()
    app.dependency_overrides[get_db] = lambda: mock_db_manager
    app.dependency_overrides[get_data_source] = lambda: mock_db_manager

    with TestClient(app) as test_client:
        yield test_client

    del app.dependency_overrides[get_db]
    del app.dependency_overrides[get_data_source]
