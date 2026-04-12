import os

files_to_fix = [
    "src/backend/python_nlp/smart_filters.py",
    "src/backend/python_nlp/gmail_integration.py"
]

for filepath in files_to_fix:
    with open(filepath, "r") as f:
        content = f.read()

    content = content.replace("validate_database_path", "validate_and_resolve_db_path")

    with open(filepath, "w") as f:
        f.write(content)
