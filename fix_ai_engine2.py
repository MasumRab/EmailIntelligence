import re

file_path = "modules/default_ai_engine/engine.py"
with open(file_path, "r") as f:
    content = f.read()

content = content.replace("from backend.python_nlp.text_utils import clean_text", "from src.backend.python_nlp.text_utils import clean_text")
content = content.replace("from backend.python_nlp.smart_filters", "from src.backend.python_nlp.smart_filters")
content = content.replace("from backend.python_backend.models", "from src.backend.python_backend.models")

with open(file_path, "w") as f:
    f.write(content)
