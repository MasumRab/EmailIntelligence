with open("src/backend/python_nlp/smart_filters.py", "r") as f:
    content = f.read()

import re

# In src/backend/python_nlp/smart_filters.py
content = content.replace("        if db_path is None:\n            db_path = DEFAULT_DB_PATH\n        elif not os.path.isabs(db_path):", "        if db_path is None:\n            db_path = DEFAULT_DB_PATH\n        if db_path != \":memory:\" and not os.path.isabs(db_path):")
# wait, my previous regex was:
content = content.replace("elif not os.path.isabs(db_path):", "elif db_path != \":memory:\" and not os.path.isabs(db_path):")

with open("src/backend/python_nlp/smart_filters.py", "w") as f:
    f.write(content)

