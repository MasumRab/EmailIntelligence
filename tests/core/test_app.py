from fastapi.testclient import TestClient


def test_app_startup(client: TestClient):
    """
    Tests that the main application starts up correctly and the Gradio UI is mounted.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert "Gradio" in response.text  # Check for Gradio UI content


def test_api_docs_are_available(client: TestClient):
    """
    Tests that the auto-generated FastAPI documentation is available.
    This confirms that the FastAPI app is running correctly.
    """
    response = client.get("/docs")
    assert response.status_code == 200
    assert "Swagger UI" in response.text
