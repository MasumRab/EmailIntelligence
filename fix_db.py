with open("src/core/database.py", "r") as f:
    content = f.read()

import re

# Fix circular import
content = content.replace("from .data.data_source import DataSource", "")

with open("src/core/database.py", "w") as f:
    f.write(content)
