import re

with open("src/backend/python_backend/main.py", "r") as f:
    content = f.read()

# Fix routing E402
content = re.sub(r'^(from \.routes\.v1\.category_routes import router as category_router_v1)', r'\1  # noqa: E402', content, flags=re.MULTILINE)
content = re.sub(r'^(from \.routes\.v1\.email_routes import router as email_router_v1)', r'\1  # noqa: E402', content, flags=re.MULTILINE)
content = re.sub(r'^(from \.enhanced_routes import router as enhanced_router)', r'\1  # noqa: E402', content, flags=re.MULTILINE)
content = re.sub(r'^(from \.workflow_routes import router as workflow_router)', r'\1  # noqa: E402', content, flags=re.MULTILINE)
content = re.sub(r'^(from \.advanced_workflow_routes import router as advanced_workflow_router)', r'\1  # noqa: E402', content, flags=re.MULTILINE)
content = re.sub(r'^(from \.node_workflow_routes import router as node_workflow_router)', r'\1  # noqa: E402', content, flags=re.MULTILINE)

with open("src/backend/python_backend/main.py", "w") as f:
    f.write(content)
