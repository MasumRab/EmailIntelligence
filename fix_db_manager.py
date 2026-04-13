filepath = "src/backend/python_backend/database.py"
with open(filepath, "r") as f:
    content = f.read()

content += "\n\n# Provide a default db_manager instance for backwards compatibility\ndb_manager = DatabaseManager()\n"

with open(filepath, "w") as f:
    f.write(content)

filepath_main = "src/backend/python_backend/main.py"
with open(filepath_main, "r") as f:
    content_main = f.read()

content_main = content_main.replace("await db_manager.connect()", "await db_manager._ensure_initialized()")
content_main = content_main.replace("await db_manager.close()", "pass")

with open(filepath_main, "w") as f:
    f.write(content_main)
