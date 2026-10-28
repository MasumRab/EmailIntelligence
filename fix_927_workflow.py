import re

with open('src/backend/python_backend/workflow_manager.py', 'r') as f:
    content = f.read()

content = content.replace("from .utils import sanitize_path", "from src.core.security import sanitize_path")

with open('src/backend/python_backend/workflow_manager.py', 'w') as f:
    f.write(content)
print("Patched successfully")
