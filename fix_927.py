import sys

with open('src/backend/python_backend/workflow_manager.py', 'r') as f:
    content = f.read()

load_old = """            from .utils import sanitize_path
            filepath = sanitize_path(filename, self.workflows_dir)
            if filepath is None:
                return False

            if not filepath.exists():"""
load_new = """            from .utils import sanitize_path
            filepath = sanitize_path(filename, self.workflows_dir)
            if filepath is None:
                return None

            if not filepath.exists():"""

content = content.replace(load_old, load_new)

with open('src/backend/python_backend/workflow_manager.py', 'w') as f:
    f.write(content)
print("Patched successfully")
