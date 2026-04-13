with open("src/backend/python_nlp/smart_filters.py", "r") as f:
    content = f.read()

# Add a check to ensure the directory exists before trying to connect
# This is a common issue when running tests that instantiate the class which writes to the default DB
# Wait, if db_path is DEFAULT_DB_PATH, os.path.dirname(db_path) must exist.
content = content.replace("        if self.db_path == \":memory:\":\n            self.conn = sqlite3.connect(\":memory:\")\n            self.conn.row_factory = sqlite3.Row\n        self._init_filter_db()", """        if self.db_path == ":memory:":
            self.conn = sqlite3.connect(":memory:")
            self.conn.row_factory = sqlite3.Row
        else:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_filter_db()""")

with open("src/backend/python_nlp/smart_filters.py", "w") as f:
    f.write(content)
