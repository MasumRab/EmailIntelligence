with open("src/core/data/database_source.py", "r") as f:
    content = f.read()

import re

# Fix __init__ definition issue
content = content.replace('''    def __init__(self, db_manager):
    def __init__(self, db_manager: DatabaseManager):''', '''    def __init__(self, db_manager: DatabaseManager):''')

with open("src/core/data/database_source.py", "w") as f:
    f.write(content)
