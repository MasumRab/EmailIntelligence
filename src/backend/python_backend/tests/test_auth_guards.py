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

    # Pop explicit overrides
    app.dependency_overrides.pop(get_current_active_user, None)
    
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
            
        methods = list(route.methods)
        if not methods:
            continue
            
        method = methods[0]
        if method == "OPTIONS":
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
    
def test_auth_guard_invalid_token(unauth_client):
    app = unauth_client.app
    target_path, target_method = None, None
    
    for route in app.routes:
        if not hasattr(route, "endpoint") or not hasattr(route.endpoint, "__module__"): continue
        if any(target in route.endpoint.__module__ for target in target_modules):
            methods = list(route.methods)
            if methods and methods[0] != "OPTIONS" and route.path not in ["/docs", "/redoc", "/openapi.json"]:
                target_path = route.path
                target_method = methods[0]
                break
                
    assert target_path is not None, "No target route found"
    
    headers = {"Authorization": "Bearer not-a-real-token"}
    
    if target_method == "GET": resp = unauth_client.get(target_path, headers=headers)
    else: resp = unauth_client.post(target_path, headers=headers)
    
    assert resp.status_code == 401, f"Expected 401 for invalid token on {target_method} {target_path}, got {resp.status_code}"
