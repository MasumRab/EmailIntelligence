with open("src/backend/python_nlp/tests/test_nlp_engine.py", "r") as f:
    content = f.read()

import re
# We need to mock `pipeline` when we create `NLPEngine()`.
content = re.sub(r'def test_([a-zA-Z0-9_]+)\(\):', r'@patch("backend.python_nlp.nlp_engine.pipeline")\ndef test_\1(mock_pipeline):', content)

# Also fix the existing patched tests
content = content.replace("def test_analyze_email_success_path(mock_load_model):", "@patch('backend.python_nlp.nlp_engine.pipeline')\ndef test_analyze_email_success_path(mock_pipeline, mock_load_model):")
content = content.replace("def test_analyze_email_full_fallback_on_exception(mock_load_model):", "@patch('backend.python_nlp.nlp_engine.pipeline')\ndef test_analyze_email_full_fallback_on_exception(mock_pipeline, mock_load_model):")
content = content.replace("def test_analyze_email_orchestration(mock_load_model):", "@patch('backend.python_nlp.nlp_engine.pipeline')\ndef test_analyze_email_orchestration(mock_pipeline, mock_load_model):")

with open("src/backend/python_nlp/tests/test_nlp_engine.py", "w") as f:
    f.write(content)
