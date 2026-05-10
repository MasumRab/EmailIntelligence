with open("src/core/data/database_source.py", "r") as f:
    content = f.read()

content = content.replace("def __init__(self, db_manager: DatabaseManager):", "def __init__(self, db_manager: Any):")

with open("src/core/data/database_source.py", "w") as f:
    f.write(content)
