import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from src.core.auth import get_current_active_user

target_modules = [
    "node_workflow_routes",
    "advanced_workflow_routes",
    "enhanced_routes",
    "gmail_routes",
    "routes.v1.email_routes",
    "ai_routes",
    "dashboard_routes",
    "workflow_routes",
    "routes.v1.category_routes",
    "performance_routes"
]


@pytest.fixture
def unauth_client():
    from backend.python_backend.main import app
    
    # We must explicitly pop the conftest override inside the test if it's live, 
    # then restore it afterwards so we don't break the rest of the suite.
    original_override = app.dependency_overrides.get(get_current_active_user)
    app.dependency_overrides.pop(get_current_active_user, None)
    
    client = TestClient(app)
    yield client
    
    if original_override:
        app.dependency_overrides[get_current_active_user] = original_override


def test_auth_guards_structural(unauth_client):
    app = unauth_client.app
    tested_routes = 0
    exempted_paths = {
        "/docs": "OpenAPI documentation UI",
        "/redoc": "ReDoc documentation UI",
        "/openapi.json": "OpenAPI schema",
        "/health": "Healthcheck endpoint",
    }
    
    for route in app.routes:
        if not hasattr(route, "endpoint") or not hasattr(route.endpoint, "__module__"):
            continue
            
        module_name = route.endpoint.__module__
        if not any(target in module_name for target in target_modules):
            continue
            
        path = route.path
        if path in exempted_paths:
            print(f"Skipping {path}: {exempted_paths[path]}")
            continue
            
        for method in route.methods:
            if method in ("OPTIONS", "HEAD"):
                continue
                
            if method == "GET": resp = unauth_client.get(path)
            elif method == "POST": resp = unauth_client.post(path)
            elif method == "PUT": resp = unauth_client.put(path)
            elif method == "DELETE": resp = unauth_client.delete(path)
            elif method == "PATCH": resp = unauth_client.patch(path)
            else: resp = unauth_client.get(path)
                
            assert resp.status_code == 403, f"Expected 403 for {method} {path} in {module_name}, got {resp.status_code}"
            tested_routes += 1
            
    print(f"\nSuccessfully verified 403 status for {tested_routes} unauthenticated routes.")
    


def get_target_routes():
    from backend.python_backend.main import app
    collected = []
    exempted_paths = {"/docs", "/redoc", "/openapi.json", "/health"}
    
    for route in app.routes:
        if not hasattr(route, "endpoint") or not hasattr(route.endpoint, "__module__"): continue
        module_name = route.endpoint.__module__
        
        # Check against target modules strictly by explicit suffix matching
        is_target = any(module_name.endswith(f".{target}") or module_name == target for target in target_modules)
        
        if is_target and route.path not in exempted_paths:
            for method in route.methods:
                if method not in ("OPTIONS", "HEAD"):
                    collected.append((module_name, route.path, method))
                    
    return collected


@pytest.mark.parametrize("module_name, target_path, target_method", get_target_routes())
def test_auth_guard_invalid_token(unauth_client, module_name, target_path, target_method):
    headers = {"Authorization": "Bearer not-a-real-token"}
    
    if target_method == "GET": resp = unauth_client.get(target_path, headers=headers)
    elif target_method == "POST": resp = unauth_client.post(target_path, headers=headers)
    elif target_method == "PUT": resp = unauth_client.put(target_path, headers=headers)
    elif target_method == "DELETE": resp = unauth_client.delete(target_path, headers=headers)
    elif target_method == "PATCH": resp = unauth_client.patch(target_path, headers=headers)
    else: resp = unauth_client.get(target_path, headers=headers)
    
    assert resp.status_code == 401, f"Expected 401 for invalid token on {target_method} {target_path} in {module_name}, got {resp.status_code}"








def test_create_app_wiring():
    # Prove that the real application mounts the guarded routes by asserting the route table.
    from src.main import create_app
    app = create_app()
    paths = {r.path for r in app.routes if hasattr(r, "path")}
    assert {"/api/dashboard/stats", "/api/performance"} <= paths

def test_exempted_paths_remain_public():
    # Health checks behind auth are an outage waiting to happen. Ensure /health is NOT 403.
    # We use the same unauth_client to prove the middleware doesn't block it.
    from fastapi.testclient import TestClient
    from src.main import create_app
    from src.core.auth import get_current_active_user
    
    app = create_app()
    app.dependency_overrides.pop(get_current_active_user, None)
    client = TestClient(app)
    
    resp = client.get("/health")
    assert resp.status_code != 404, "Healthcheck endpoint is not mounted (404)"
    assert resp.status_code in (200, 503), f"Healthcheck is incorrectly guarded or failing! Status: {resp.status_code}"
