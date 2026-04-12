with open("src/backend/python_nlp/tests/test_nlp_engine.py", "r") as f:
    content = f.read()

import re

# Need to patch `pipeline` in `nlp_engine_with_mocks`
content = content.replace("def nlp_engine_with_mocks():", "@pytest.fixture\n@patch('backend.python_nlp.nlp_engine.pipeline')\ndef nlp_engine_with_mocks(mock_pipeline):")
# But it already has @pytest.fixture right above it
content = content.replace("@pytest.fixture\n@pytest.fixture\n", "@pytest.fixture\n")

with open("src/backend/python_nlp/tests/test_nlp_engine.py", "w") as f:
    f.write(content)
