import re

file_path = "src/core/smart_filter_manager.py"
with open(file_path, "r") as f:
    content = f.read()

content = content.replace("from .database import DATA_DIR",
"""import os
DATA_DIR = os.environ.get("DATA_DIR", "data")""")

with open(file_path, "w") as f:
    f.write(content)
