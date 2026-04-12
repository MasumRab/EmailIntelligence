with open("src/backend/python_nlp/tests/test_nlp_engine.py", "r") as f:
    content = f.read()

import re

# We should patch pipeline entirely.
content = content.replace("def test_analyze_email_success_path(mock_load_model):", "@patch('backend.python_nlp.nlp_engine.pipeline')\ndef test_analyze_email_success_path(mock_pipeline, mock_load_model):")
content = content.replace("def test_analyze_email_full_fallback_on_exception(mock_load_model):", "@patch('backend.python_nlp.nlp_engine.pipeline')\ndef test_analyze_email_full_fallback_on_exception(mock_pipeline, mock_load_model):")
content = content.replace("def test_analyze_email_orchestration(mock_load_model):", "@patch('backend.python_nlp.nlp_engine.pipeline')\ndef test_analyze_email_orchestration(mock_pipeline, mock_load_model):")
content = content.replace("def test_analyze_email_success_path():", "@patch('backend.python_nlp.nlp_engine.pipeline')\ndef test_analyze_email_success_path(mock_pipeline):")
content = content.replace("def test_analyze_email_full_fallback_on_exception():", "@patch('backend.python_nlp.nlp_engine.pipeline')\ndef test_analyze_email_full_fallback_on_exception(mock_pipeline):")
content = content.replace("def test_analyze_email_orchestration():", "@patch('backend.python_nlp.nlp_engine.pipeline')\ndef test_analyze_email_orchestration(mock_pipeline):")

with open("src/backend/python_nlp/tests/test_nlp_engine.py", "w") as f:
    f.write(content)
