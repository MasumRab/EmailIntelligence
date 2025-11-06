
import pytest
from fastapi.testclient import TestClient
from src.main import create_app
from unittest.mock import AsyncMock

@pytest.fixture
def app():
    app = create_app()
    return app

@pytest.fixture
def client(app):
    return TestClient(app)

@pytest.fixture
def mock_db_manager():
    return AsyncMock()
