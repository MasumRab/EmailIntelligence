import pytest
from unittest.mock import AsyncMock, patch
from backend.python_backend.ai_engine import AIAnalysisResult


@pytest.fixture
def mock_ai_engine():
    """Fixture to mock the AdvancedAIEngine used in the action routes."""
    with patch("backend.python_backend.action_routes.ai_engine", new_callable=AsyncMock) as mock_ae:
        yield mock_ae


def test_extract_actions_from_text_success(client, mock_ai_engine):
    """Test successful extraction of action items from text."""
    mock_action_item_data = [
        {
            "action_phrase": "Please review the document by tomorrow",
            "verb": "review",
            "object": "document",
            "raw_due_date_text": "by tomorrow",
            "context": "A test sentence. Please review the document by tomorrow. Thank you.",
        }
    ]
    mock_ai_result = AIAnalysisResult(data={"action_items": mock_action_item_data})
    mock_ai_engine.analyze_email.return_value = mock_ai_result

    request_payload = {
        "subject": "Meeting Follow-up",
        "content": "Please review the document by tomorrow.",
    }
    response = client.post("/api/actions/extract-from-text", json=request_payload)

    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)
    assert len(response_data) == 1
    assert response_data[0]["action_phrase"] == "Please review the document by tomorrow"
    mock_ai_engine.analyze_email.assert_called_once_with(
        subject=request_payload["subject"], content=request_payload["content"], db=None
    )


def test_extract_actions_no_actions_found(client, mock_ai_engine):
    """Test case where no action items are found in the text."""
    mock_ai_result = AIAnalysisResult(data={"action_items": []})
    mock_ai_engine.analyze_email.return_value = mock_ai_result
    request_payload = {"subject": "General Update", "content": "This is just a general update."}

    response = client.post("/api/actions/extract-from-text", json=request_payload)

    assert response.status_code == 200
    assert response.json() == []


def test_extract_actions_missing_content(client):
    """Test request with missing content field, expecting a validation error."""
    request_payload = {"subject": "Missing content"}
    response = client.post("/api/actions/extract-from-text", json=request_payload)
    assert response.status_code == 422


def test_extract_actions_ai_engine_exception(client, mock_ai_engine):
    """Test handling of an exception from the AI engine."""
    mock_ai_engine.analyze_email.side_effect = Exception("AI Engine error")
    request_payload = {"subject": "Test Error", "content": "This content will cause an error."}

    response = client.post("/api/actions/extract-from-text", json=request_payload)

    assert response.status_code == 500
    assert "Failed to extract action items" in response.json()["detail"]
