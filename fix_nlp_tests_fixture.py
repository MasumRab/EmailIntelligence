with open("src/backend/python_nlp/tests/test_nlp_engine.py", "r") as f:
    content = f.read()

import re

# We need to mock `pipeline` when we create `NLPEngine()` inside the fixture `nlp_engine_with_mocks`.
content = content.replace("patch(\"backend.python_nlp.nlp_engine.HAS_SKLEARN_AND_JOBLIB\", True),", "patch(\"backend.python_nlp.nlp_engine.HAS_SKLEARN_AND_JOBLIB\", True),\n            patch(\"backend.python_nlp.nlp_engine.pipeline\", MagicMock()),")

with open("src/backend/python_nlp/tests/test_nlp_engine.py", "w") as f:
    f.write(content)
