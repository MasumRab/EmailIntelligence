import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from src.core.plugin_routes import router as plugin_router
from src.core.model_routes import router as model_router
from src.core.auth import create_access_token

real_app = FastAPI()
real_app.include_router(plugin_router)
real_app.include_router(model_router)

real_client = TestClient(real_app, raise_server_exceptions=False)

def test_auth_runs_before_manager():
    r = real_client.get("/api/models/")
    assert r.status_code == 403, f"guard did not run first: {r.status_code}"

def test_routes_require_auth():
    # No token should yield 403 on ALL routes
    response = real_client.get("/api/plugins/")
    assert response.status_code == 403

    response = real_client.get("/api/models/")
    assert response.status_code == 403
    
    response = real_client.post("/api/models/register")
    assert response.status_code == 403
    
    response = real_client.delete("/api/models/m1")
    assert response.status_code == 403

def test_routes_require_admin():
    # Guest token
    guest_token = create_access_token({"sub": "guest_user", "role": "guest"})
    headers = {"Authorization": f"Bearer {guest_token}"}

    # Reading should be 500 (because manager fails), NOT 403
    response = real_client.get("/api/models/", headers=headers)
    assert response.status_code != 403

    # Mutating should be 403
    response = real_client.post("/api/plugins/nonexistent/load", headers=headers)
    assert response.status_code == 403
    
    response = real_client.post("/api/models/register", json={"model_id": "m1", "model_type": "text", "name": "m1", "version": "1", "framework": "pt"}, headers=headers)
    assert response.status_code == 403
