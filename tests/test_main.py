"""Tests for src.main.create_app() — FastAPI app factory and Gradio UI integration."""

from unittest.mock import patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def app():
    """Create the app once per module (Gradio/ModuleManager init is expensive)."""
    from src.main import create_app

    return create_app()


@pytest.fixture
def client(app):
    """TestClient wrapping the create_app() FastAPI instance."""
    with TestClient(app) as c:
        yield c


class TestCreateApp:
    """Verify create_app() returns a properly configured FastAPI instance."""

    def test_returns_fastapi_instance(self, app):
        assert isinstance(app, FastAPI)

    def test_app_title(self, app):
        assert app.title == "Email Intelligence Platform"

    def test_app_version(self, app):
        assert app.version == "3.0.0"

    def test_app_description(self, app):
        assert "email processing" in app.description.lower()


class TestCORSMiddleware:
    """Verify CORS is configured with an explicit origin allowlist."""

    def test_cors_middleware_present(self, app):
        from starlette.middleware.cors import CORSMiddleware

        cors_found = any(
            isinstance(m.cls, type) and issubclass(m.cls, CORSMiddleware)
            for m in app.user_middleware
        )
        assert cors_found, "CORSMiddleware not found in app middleware stack"

    def test_cors_not_wildcard(self, app):
        """CORS must not use '*' origins with credentials."""
        for m in app.user_middleware:
            if m.kwargs.get("allow_origins") is not None:
                origins = m.kwargs["allow_origins"]
                assert "*" not in origins, (
                    "Wildcard origins with allow_credentials=True is invalid"
                )


class TestSecurityMiddleware:
    """Verify security middleware classes (not instances) are registered."""

    def test_security_middleware_present(self, app):
        from src.core.middleware import SecurityMiddleware

        found = any(m.cls is SecurityMiddleware for m in app.user_middleware)
        assert found, "SecurityMiddleware not registered"

    def test_security_headers_middleware_present(self, app):
        from src.core.middleware import SecurityHeadersMiddleware

        found = any(m.cls is SecurityHeadersMiddleware for m in app.user_middleware)
        assert found, "SecurityHeadersMiddleware not registered"


class TestExceptionHandlers:
    """Verify exception handlers are registered."""

    def test_validation_exception_handler(self, app):
        from pydantic import ValidationError

        assert ValidationError in app.exception_handlers

    def test_http_exception_handler(self, app):
        from fastapi import HTTPException

        assert HTTPException in app.exception_handlers

    def test_general_exception_handler(self, app):
        assert Exception in app.exception_handlers


class TestRoutes:
    """Verify core routes exist."""

    def test_root_redirect(self, client):
        response = client.get("/", follow_redirects=False)
        assert response.status_code in (302, 307)
        assert "/ui" in response.headers.get("location", "")

    def test_ui_route_exists(self, client):
        response = client.get("/ui", follow_redirects=False)
        # Gradio mount returns 200 or redirects to /ui/
        assert response.status_code in (200, 302, 307)


class TestTabFunctions:
    """Verify the three tab functions are wired into create_app()."""

    def test_system_status_tab_wired(self, app):
        """create_system_status_tab should be called during create_app()."""
        with patch("src.main.create_system_status_tab") as mock:
            from src.main import create_app

            create_app()
            mock.assert_called_once()

    def test_ai_lab_tab_wired(self, app):
        """create_ai_lab_tab should be called during create_app()."""
        with patch("src.main.create_ai_lab_tab") as mock:
            from src.main import create_app

            create_app()
            mock.assert_called_once()

    def test_gmail_integration_tab_wired(self, app):
        """create_gmail_integration_tab should be called during create_app()."""
        with patch("src.main.create_gmail_integration_tab") as mock:
            from src.main import create_app

            create_app()
            mock.assert_called_once()
