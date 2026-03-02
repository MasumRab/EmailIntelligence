with open("src/backend/python_nlp/smart_filters.py", "r", encoding="utf-8") as f:
    text = f.read()

# Fix the project root calculation because it resolves to /app/src instead of /app
import re
text = text.replace(
    'PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))',
    'PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))'
)

# And also ensure the DATA_DIR actually exists
text = text.replace(
    'DATA_DIR = os.path.join(PROJECT_ROOT, "data")',
    'DATA_DIR = os.path.join(PROJECT_ROOT, "data")\nos.makedirs(DATA_DIR, exist_ok=True)'
)

with open("src/backend/python_nlp/smart_filters.py", "w", encoding="utf-8") as f:
    f.write(text)
