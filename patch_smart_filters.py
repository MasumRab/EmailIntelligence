with open("src/backend/python_nlp/smart_filters.py", "r") as f:
    content = f.read()

content = content.replace("self.db_path = str(PathValidator.validate_and_resolve_db_path(db_path, DATA_DIR))", """if db_path != ":memory:":
            self.db_path = str(PathValidator.validate_and_resolve_db_path(db_path, DATA_DIR))
        else:
            self.db_path = db_path""")

with open("src/backend/python_nlp/smart_filters.py", "w") as f:
    f.write(content)
