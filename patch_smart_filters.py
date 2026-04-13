filepath = "src/backend/python_nlp/smart_filters.py"
with open(filepath, "r") as f:
    content = f.read()

import os

old_block = """DATA_DIR = os.path.join(PROJECT_ROOT, "data")"""
new_block = """DATA_DIR = os.path.join(PROJECT_ROOT, "data")
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR, exist_ok=True)"""

content = content.replace(old_block, new_block)

old_block2 = """        elif not os.path.isabs(db_path):
            # Secure path validation to prevent directory traversal
            filename = PathValidator.sanitize_filename(os.path.basename(db_path))
            db_path = os.path.join(DATA_DIR, filename)

        # Validate the final path
        self.db_path = str(PathValidator.validate_and_resolve_db_path(db_path, DATA_DIR))"""

new_block2 = """        elif db_path != ":memory:" and not os.path.isabs(db_path):
            # Secure path validation to prevent directory traversal
            filename = PathValidator.sanitize_filename(os.path.basename(db_path))
            db_path = os.path.join(DATA_DIR, filename)

        # Validate the final path
        self.db_path = str(PathValidator.validate_and_resolve_db_path(db_path, DATA_DIR)) if db_path != ":memory:" else ":memory:" """

content = content.replace(old_block2, new_block2)

with open(filepath, "w") as f:
    f.write(content)
