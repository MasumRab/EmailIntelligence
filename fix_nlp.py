with open("src/backend/python_nlp/tests/test_nlp_engine.py", "r") as f:
    content = f.read()

# Replace any `@patch("backend.python_nlp.nlp_engine.pipeline")` if already there
import re
content = re.sub(r'def test_([a-zA-Z0-9_]+)\(\):', r'@patch("backend.python_nlp.nlp_engine.pipeline")\ndef test_\1(mock_pipeline):', content)

with open("src/backend/python_nlp/tests/test_nlp_engine.py", "w") as f:
    f.write(content)
