import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
import subprocess
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient

from src.core.database import get_db
from src.core.factory import get_data_source


@pytest.fixture(scope="session", autouse=True)
def download_nltk_data():
    """Download NLTK data before running tests."""
    packages = ["punkt", "stopwords"]
    for package in packages:
        try:
            subprocess.run([sys.executable, "-m", "nltk.downloader", package], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            # Continue even if NLTK data fails to download
            pass
    try:
        subprocess.run([sys.executable, "-m", "textblob.download_corpora"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        pass


@pytest.fixture
def mock_db_manager():
    """
    Provides a mock DatabaseManager instance.
    This mock is reset for each test function, ensuring test isolation.
    """
    return create_mock_db_manager()


@pytest.fixture
def client(mock_db_manager: AsyncMock):
    """
    Provides a TestClient with the database dependency overridden.
    This fixture ensures that API endpoints use the mock_db_manager instead of a real database.
    """
    from .test_config import create_test_client
    test_client = create_test_client(mock_db_manager)
    yield test_client
