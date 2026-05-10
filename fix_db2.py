with open("src/core/database.py", "r") as f:
    content = f.read()

import re

# Fix NameError
content = content.replace("class DatabaseManager(DataSource):", "class DatabaseManager:")

with open("src/core/database.py", "w") as f:
    f.write(content)
