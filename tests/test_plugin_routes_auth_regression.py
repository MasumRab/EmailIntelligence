import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from src.core.plugin_routes import router as plugin_router
from src.core.model_routes import router as model_router

app = FastAPI()
app.include_router(plugin_router)
app.include_router(model_router)

client = TestClient(app)

def test_plugin_routes_require_auth():
    # Attempt to access a plugin route without authentication
    response = client.get("/api/plugins/")
    assert response.status_code in (401, 403), f"Expected 401 or 403, got {response.status_code}"

def test_model_routes_require_auth():
    # Attempt to access a model route without authentication
    response = client.get("/api/models/")
    assert response.status_code in (401, 403), f"Expected 401 or 403, got {response.status_code}"
