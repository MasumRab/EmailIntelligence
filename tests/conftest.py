import os
import sys
import pytest
from fastapi.testclient import TestClient

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.main import create_app


@pytest.fixture(scope="module")
def client():
    """
    A pytest fixture that provides a FastAPI TestClient for the application.
    This allows tests to make requests to the application without a live server.
    """
    app = create_app()
    with TestClient(app) as c:
        yield c
