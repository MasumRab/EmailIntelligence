import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.main import create_app


@pytest.fixture
def real_client():
    """
    Fixture that provides a TestClient using the real application factory.
    Mocks necessary external calls to prevent side effects during startup.
    """
    with patch("src.main.requests.get") as mock_get:
        # Mock requests.get to return a dummy response for system status check
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        # Mock ModuleManager to avoid loading heavy modules during simple app test
        with patch("src.main.ModuleManager") as MockModuleManager:
            instance = MockModuleManager.return_value
            instance.load_modules.return_value = None

            app = create_app()
            with TestClient(app) as client:
                yield client


def test_app_startup(real_client: TestClient):
    """
    Tests that the main application starts up correctly and the Gradio UI is mounted.
    """
    # TestClient follows redirects by default, so getting "/" should land on "/ui" (200)
    # or return 307 if follow_redirects=False.
    # We'll assume default behavior (follow).
    response = real_client.get("/")
    assert response.status_code == 200
    # The response text should contain Gradio content
    # Note: Gradio mounts a full SPA, so we check for some identifying HTML/JS
    assert "gradio" in response.text.lower() or "window.gradio_config" in response.text


def test_api_docs_are_available(real_client: TestClient):
    """
    Tests that the auto-generated FastAPI documentation is available.
    This confirms that the FastAPI app is running correctly.
    """
    response = real_client.get("/docs")
    assert response.status_code == 200
    assert "swagger" in response.text.lower()
