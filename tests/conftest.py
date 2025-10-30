import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
import subprocess
from unittest.mock import AsyncMock
<<<<<<< HEAD

from .test_config import create_mock_db_manager, create_test_client
=======
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
>>>>>>> 73a8d1727b5a9766467abd3d090470711b0fdcb2


@pytest.fixture(scope="session", autouse=True)
def download_nltk_data():
    """Download NLTK data before running tests."""
    packages = ["punkt", "stopwords"]
    for package in packages:
<<<<<<< HEAD
        try:
            subprocess.run([sys.executable, "-m", "nltk.downloader", package], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            # Continue even if NLTK data fails to download
            pass
    try:
        subprocess.run([sys.executable, "-m", "textblob.download_corpora"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        pass
=======
        subprocess.run([sys.executable, "-m", "nltk.downloader", package], check=True)
    subprocess.run([sys.executable, "-m", "textblob.download_corpora"], check=True)
>>>>>>> 73a8d1727b5a9766467abd3d090470711b0fdcb2


@pytest.fixture
def mock_db_manager():
    """
    Provides a mock DatabaseManager instance.
    This mock is reset for each test function, ensuring test isolation.
    """
<<<<<<< HEAD
    return create_mock_db_manager()
=======
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
>>>>>>> 73a8d1727b5a9766467abd3d090470711b0fdcb2


@pytest.fixture
def client(mock_db_manager: AsyncMock):
    """
    Provides a TestClient with the database dependency overridden.
    This fixture ensures that API endpoints use the mock_db_manager instead of a real database.
    """
<<<<<<< HEAD
    test_client = create_test_client(mock_db_manager)
    yield test_client
=======
    app = create_app()
    app.dependency_overrides[get_db] = lambda: mock_db_manager
    app.dependency_overrides[get_data_source] = lambda: mock_db_manager

    with TestClient(app) as test_client:
        yield test_client

    del app.dependency_overrides[get_db]
    del app.dependency_overrides[get_data_source]
>>>>>>> 73a8d1727b5a9766467abd3d090470711b0fdcb2
