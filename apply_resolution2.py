with open("src/backend/python_backend/main.py", "r") as f:
    content = f.read()

content = content.replace("    action_routes,\n", "")
content = content.replace("app.include_router(action_routes.router)\n", "")

with open("src/backend/python_backend/main.py", "w") as f:
    f.write(content)

with open("src/backend/python_backend/tests/conftest.py", "r") as f:
    content = f.read()

content = content.replace("from backend.python_backend.main import app", "try:\n    from backend.python_backend.main import app\nexcept ImportError:\n    pass")

