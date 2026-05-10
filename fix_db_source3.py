with open("src/core/data/database_source.py", "r") as f:
    content = f.read()

import re

# Fix circular import
content = content.replace("from ..database import DatabaseManager, create_database_manager, DatabaseConfig", "# circular import resolved")

with open("src/core/data/database_source.py", "w") as f:
    f.write(content)
