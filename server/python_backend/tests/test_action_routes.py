from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from server.python_backend.main import app
from server.python_backend.models import \
    ActionItem  # For response type hint if needed

# Mock AdvancedAIEngine methods
# ai_engine is instantiated at module level in action_routes.py
mock_ai_engine_action = MagicMock()
# analyze_email in AIEngine is now async
mock_ai_engine_action.analyze_email = AsyncMock()

# Mock PerformanceMonitor
mock_performance_monitor_action_instance = MagicMock()

@pytest.fixture(scope="module", autouse=True)
def mock_action_dependencies():
    patches = [
        patch('server.python_backend.action_routes.ai_engine', mock_ai_engine_action),
        patch('server.python_backend.action_routes.performance_monitor', mock_performance_monitor_action_instance)
    ]
    for p in patches:
        p.start()
    yield
    for p in patches:
        p.stop()

@pytest.fixture
def client_action():
    # No db override needed as action_routes.ai_engine.analyze_email is called with db=None
    return TestClient(app)

def test_extract_actions_from_text(client_action):
    request_data = {"content": "Please follow up on this task by Friday."}

    # Mock the AIAnalysisResult object that ai_engine.analyze_email would return
    mock_ai_result = MagicMock()
    # This is a list of dicts, which will be converted to List[ActionItem] by Pydantic
    mock_ai_result.action_items = [
        {"action_phrase": "follow up on this task", "context": "Please follow up on this task by Friday."}
    ]
    mock_ai_engine_action.analyze_email.return_value = mock_ai_result

    response = client_action.post("/api/actions/extract-from-text", json=request_data)

    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 1
    assert response_data[0]["action_phrase"] == "follow up on this task"

    mock_ai_engine_action.analyze_email.assert_called_once_with(
        subject="", # subject defaults to "" if None in request_model and passed as ""
        content=request_data["content"],
        db=None # action_routes passes db=None
    )

def test_extract_actions_from_text_with_subject(client_action):
    request_data = {"subject": "Meeting Follow-up", "content": "Action: review the report."}
    mock_ai_result = MagicMock()
    mock_ai_result.action_items = [
        {"action_phrase": "review the report", "context": "Action: review the report."}
    ]
    mock_ai_engine_action.analyze_email.return_value = mock_ai_result

    response = client_action.post("/api/actions/extract-from-text", json=request_data)

    assert response.status_code == 200
    assert response.json()[0]["action_phrase"] == "review the report"
    mock_ai_engine_action.analyze_email.assert_called_once_with(
        subject=request_data["subject"],
        content=request_data["content"],
        db=None
    )

def test_extract_actions_from_text_ai_error(client_action):
    request_data = {"content": "Some text"}
    mock_ai_engine_action.analyze_email.side_effect = Exception("AI processing error")

    response = client_action.post("/api/actions/extract-from-text", json=request_data)

    assert response.status_code == 500
    assert "Failed to extract action items: AI processing error" in response.json()["detail"]

[end of server/python_backend/tests/test_action_routes.py]
