with open("src/backend/python_nlp/tests/test_nlp_engine.py", "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "yield engine" in line:
        pass # it was probably returning engine? Wait, the fixture yields engine?
    new_lines.append(line)

# Let's see what nlp_engine_with_mocks does
import re
with open("src/backend/python_nlp/tests/test_nlp_engine.py", "r") as f:
    content = f.read()

# Oh, the fixture uses `engine = NLPEngine()` and then `yield engine`.
# But wait, if we added an argument `mock_pipeline` to `nlp_engine_with_mocks`, pytest treats it as a fixture request.
# But `mock_pipeline` isn't a pytest fixture, it's from `@patch`!
# You cannot easily combine `@pytest.fixture` with `@patch` decorator if the patched argument comes in.
# Well, actually `patch` is evaluated at definition time.
# Let's just mock pipeline using `patch` context manager inside the fixture.

content = content.replace("@patch('backend.python_nlp.nlp_engine.pipeline')\ndef nlp_engine_with_mocks(mock_pipeline):", "def nlp_engine_with_mocks():")
content = content.replace("patch(\"backend.python_nlp.nlp_engine.HAS_SKLEARN_AND_JOBLIB\", True),", "patch(\"backend.python_nlp.nlp_engine.HAS_SKLEARN_AND_JOBLIB\", True),\n            patch(\"backend.python_nlp.nlp_engine.pipeline\", MagicMock()),")

with open("src/backend/python_nlp/tests/test_nlp_engine.py", "w") as f:
    f.write(content)
