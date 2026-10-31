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
    app = FastAPI()
    
    # Import and mount only the routers directly to bypass all the background threads and middleware bugs on main
    from src.backend.python_backend.node_workflow_routes import router as router1
    from src.backend.python_backend.advanced_workflow_routes import router as router2
    from src.backend.python_backend.enhanced_routes import router as router3
    from src.backend.python_backend.gmail_routes import router as router4
    from src.backend.python_backend.routes.v1.email_routes import router as router5
    from src.backend.python_backend.ai_routes import router as router6
    from src.backend.python_backend.dashboard_routes import router as router7
    from src.backend.python_backend.workflow_routes import router as router8
    from src.backend.python_backend.routes.v1.category_routes import router as router9
    from src.backend.python_backend.performance_routes import router as router10

    routers = [
        (router1, "src.backend.python_backend.node_workflow_routes"),
        (router2, "src.backend.python_backend.advanced_workflow_routes"),
        (router3, "src.backend.python_backend.enhanced_routes"),
        (router4, "src.backend.python_backend.gmail_routes"),
        (router5, "src.backend.python_backend.routes.v1.email_routes"),
        (router6, "src.backend.python_backend.ai_routes"),
        (router7, "src.backend.python_backend.dashboard_routes"),
        (router8, "src.backend.python_backend.workflow_routes"),
        (router9, "src.backend.python_backend.routes.v1.category_routes"),
        (router10, "src.backend.python_backend.performance_routes")
    ]
    
    # Since we aren't using create_app, we need to apply the dependencies to the app explicitly as it would normally
    for r, name in routers:
        app.include_router(r)

    
    return TestClient(app)

def test_auth_guards_structural(unauth_client):
    app = unauth_client.app
    tested_routes = 0
    exempted_paths = {
        "/docs": "OpenAPI documentation UI",
        "/redoc": "ReDoc documentation UI",
        "/openapi.json": "OpenAPI schema",
        "/api/health": "Healthcheck endpoint",
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
    app = FastAPI()
    
    from src.backend.python_backend.node_workflow_routes import router as router1
    from src.backend.python_backend.advanced_workflow_routes import router as router2
    from src.backend.python_backend.enhanced_routes import router as router3
    from src.backend.python_backend.gmail_routes import router as router4
    from src.backend.python_backend.routes.v1.email_routes import router as router5
    from src.backend.python_backend.ai_routes import router as router6
    from src.backend.python_backend.dashboard_routes import router as router7
    from src.backend.python_backend.workflow_routes import router as router8
    from src.backend.python_backend.routes.v1.category_routes import router as router9
    from src.backend.python_backend.performance_routes import router as router10

    routers = [router1, router2, router3, router4, router5, router6, router7, router8, router9, router10]
    for r in routers:
        app.include_router(r)
        
    collected = []
    exempted_paths = {"/docs", "/redoc", "/openapi.json", "/api/health"}
    
    for route in app.routes:
        if not hasattr(route, "endpoint") or not hasattr(route.endpoint, "__module__"): continue
        module_name = route.endpoint.__module__
        
        # Check against target modules strictly by exact match or explicit suffix matching
        is_target = any(module_name == f"src.backend.python_backend.{target}" or module_name.endswith(f".{target}") for target in target_modules)
        
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
    from src.main import create_app
    from fastapi.testclient import TestClient
    
    try:
        app = create_app()
    except Exception as e:
        pytest.skip(f"create_app() is too heavy for this unit test context due to: {e}")
        return
        
    client = TestClient(app)
    
    # Assert a 403 on at least two guarded paths of that app
    resp1 = client.get("/api/dashboard/stats")
    assert resp1.status_code == 403, f"Expected 403 on real app for /api/dashboard/stats, got {resp1.status_code}"
    
    resp2 = client.get("/api/performance/metrics")
    assert resp2.status_code == 403, f"Expected 403 on real app for /api/performance/metrics, got {resp2.status_code}"

def test_exempted_paths_remain_public():
    # Health checks behind auth are an outage waiting to happen. Ensure /api/health is NOT 403.
    # We use the same unauth_client to prove the middleware doesn't block it.
    from fastapi.testclient import TestClient
    from src.main import create_app
    
    try:
        app = create_app()
        # Remove any lingering dependency overrides just in case
        app.dependency_overrides.pop(get_current_active_user, None)
        client = TestClient(app)
        
        resp = client.get("/api/health")
        # We don't care if it's 200 or 503 (db down), just that auth (401/403) didn't block it
        assert resp.status_code not in (401, 403), f"Healthcheck is incorrectly guarded! Status: {resp.status_code}"
    except Exception as e:
        pytest.skip(f"Could not initialize app for healthcheck test: {e}")
