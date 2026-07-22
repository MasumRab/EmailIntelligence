import sys
from unittest.mock import MagicMock
import warnings
warnings.filterwarnings("ignore")

# Mock dependencies that cause import errors
sys.modules['backend'] = MagicMock()
sys.modules['backend.python_nlp'] = MagicMock()
sys.modules['backend.python_nlp.gmail_service'] = MagicMock()
sys.modules['backend.python_nlp.smart_filters'] = MagicMock()
sys.modules['backend.plugins'] = MagicMock()
sys.modules['backend.plugins.plugin_manager'] = MagicMock()
sys.modules['backend.python_backend'] = MagicMock()
sys.modules['backend.python_backend.services'] = MagicMock()

# Import what we need
from fastapi.testclient import TestClient

try:
    from src.backend.python_backend.main import app
    client = TestClient(app)

    # Check OpenAPI schema
    schema = app.openapi()
    endpoint = schema['paths']['/token']['post']
    print("Successfully loaded OpenAPI schema.")
    print(f"Request body schema present: {'requestBody' in endpoint}")
    print(f"Query parameters present: {'parameters' in endpoint}")
except Exception as e:
    print(f"Could not load app for testing: {e}")
