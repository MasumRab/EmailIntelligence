from http.client import HTTPResponse
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from googleapiclient.errors import HttpError


@pytest.fixture
def mock_gmail_service():
    """Fixture to mock the GmailAIService used in the gmail routes."""
    with patch(
        "backend.python_backend.gmail_routes.gmail_service", new_callable=AsyncMock
    ) as mock_gs:
        yield mock_gs


@pytest.fixture
def mock_performance_monitor_gmail():
    """Fixture to mock the PerformanceMonitor used in the gmail routes."""
    with patch(
        "backend.python_backend.gmail_routes.performance_monitor", new_callable=AsyncMock
    ) as mock_pm:
        mock_pm.track = lambda func: func
        mock_pm.record_sync_performance = AsyncMock()
        yield mock_pm


def test_sync_gmail_success(client, mock_gmail_service, mock_performance_monitor_gmail):
    """Test successful Gmail sync."""
    request_payload = {"maxEmails": 10}
    mock_sync_result = {
        "success": True,
        "processed_count": 10,
        "emailsCreated": 10,
        "batch_info": {},
        "statistics": {},
        "error": None,
    }
    mock_gmail_service.sync_gmail_emails.return_value = mock_sync_result

    response = client.post("/api/gmail/sync", json=request_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["success"]
    assert data["processedCount"] == 10
    mock_gmail_service.sync_gmail_emails.assert_called_once()
    mock_performance_monitor_gmail.record_sync_performance.assert_called_once()


def test_sync_gmail_api_error(client, mock_gmail_service, mock_performance_monitor_gmail):
    """Test handling of Google API errors during sync."""
    request_payload = {"maxEmails": 10}
    mock_resp = MagicMock(spec=HTTPResponse)
    mock_resp.status = 401
    mock_resp.reason = "Unauthorized"
    error_content = b'{"error": {"message": "Auth error"}}'
    mock_gmail_service.sync_gmail_emails.side_effect = HttpError(
        resp=mock_resp, content=error_content
    )

    response = client.post("/api/gmail/sync", json=request_payload)

    assert response.status_code == 401
    assert "Gmail API authentication failed" in response.json()["detail"]


def test_smart_retrieval_success(client, mock_gmail_service, mock_performance_monitor_gmail):
    """Test successful smart retrieval."""
    request_payload = {"strategies": ["urgent"]}
    mock_retrieval_result = {"success": True, "totalEmails": 50}
    mock_gmail_service.execute_smart_retrieval.return_value = mock_retrieval_result

    response = client.post("/api/gmail/smart-retrieval", json=request_payload)

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["totalEmails"] == 50
    mock_gmail_service.execute_smart_retrieval.assert_called_once()


def test_get_retrieval_strategies_success(
    client, mock_gmail_service, mock_performance_monitor_gmail
):
    """Test successful retrieval of strategies."""
    mock_strategies_data = [{"name": "urgent"}, {"name": "follow-up"}]
    mock_gmail_service.get_retrieval_strategies.return_value = mock_strategies_data

    response = client.get("/api/gmail/strategies")

    assert response.status_code == 200
    assert response.json()["strategies"] == mock_strategies_data
    mock_gmail_service.get_retrieval_strategies.assert_called_once()


def test_get_gmail_performance_success(client, mock_gmail_service, mock_performance_monitor_gmail):
    """Test successful retrieval of performance metrics."""
    mock_performance_data = {"status": "healthy", "metrics": {"api_calls": 100}}
    mock_gmail_service.get_performance_metrics.return_value = mock_performance_data

    response = client.get("/api/gmail/performance")

    assert response.status_code == 200
    assert response.json() == mock_performance_data
    mock_gmail_service.get_performance_metrics.assert_called_once()
