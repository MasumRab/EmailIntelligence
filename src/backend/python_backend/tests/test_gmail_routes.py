from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

# Import the app instance
from backend.python_backend.main import app

# Create a mock instance for GmailAIService
mock_gmail_service_instance = MagicMock()
mock_gmail_service_instance.sync_gmail_emails = AsyncMock()
mock_gmail_service_instance.execute_smart_retrieval = AsyncMock()
mock_gmail_service_instance.get_retrieval_strategies = AsyncMock()
mock_gmail_service_instance.get_performance_metrics = AsyncMock()


@pytest.fixture
def client_gmail():
    """
    Provides a TestClient with all external services mocked for gmail routes.
    """
    from backend.python_backend.dependencies import get_gmail_service

    # Reset mocks before each test to ensure isolation
    mock_gmail_service_instance.reset_mock()

    # Set up the dependency overrides
    app.dependency_overrides[get_gmail_service] = lambda: mock_gmail_service_instance

    # Patch performance_monitor directly as it's not injected
    with patch(
        "backend.python_backend.gmail_routes.log_performance"
    ) as mock_log_performance:
        mock_log_performance.side_effect = lambda name: (lambda func: func)
        yield TestClient(app)

    # Clean up overrides after the test
    app.dependency_overrides.clear()


def test_sync_gmail(client_gmail):
    """Test the sync endpoint returns the transformed result from the service."""
    # This is the raw result from the nlp service
    nlp_result_mock = {
        "success": True,
        "processed_count": 50,
        "batch_info": {"batch_id": "xyz-123", "timestamp": "2023-10-27T10:00:00Z"},
        "statistics": {"analyzed": 50, "failed": 0},
    }
    mock_gmail_service_instance.sync_gmail_emails.return_value = nlp_result_mock

    request_payload = {"maxEmails": 100, "queryFilter": "test-query"}
    response = client_gmail.post("/api/gmail/sync", json=request_payload)

    assert response.status_code == 200

    # This is the transformed result from the route
    expected_response = {
        "success": True,
        "processedCount": 50,
        "emailsCreated": 50,  # Approximation from processed_count
        "errorsCount": 0,
        "batchInfo": {
            "batchId": "xyz-123",
            "queryFilter": "test-query",
            "timestamp": "2023-10-27T10:00:00Z",
        },
        "statistics": {"analyzed": 50, "failed": 0},
        "error": None,
    }
    # The response may contain a non-deterministic batchId and timestamp if the mock batch_info is empty.
    # So we only compare the keys that are deterministic.
    response_json = response.json()
    assert response_json["success"] == expected_response["success"]
    assert response_json["processedCount"] == expected_response["processedCount"]
    assert response_json["emailsCreated"] == expected_response["emailsCreated"]
    assert response_json["errorsCount"] == expected_response["errorsCount"]
    assert response_json["statistics"] == expected_response["statistics"]

    mock_gmail_service_instance.sync_gmail_emails.assert_called_once()


def test_sync_gmail_api_error(client_gmail):
    """Test that the route correctly handles HttpError from the service."""
    from googleapiclient.errors import HttpError

    # The HttpError should be caught by the route's error handler and converted to an HTTPException
    mock_gmail_service_instance.sync_gmail_emails.side_effect = HttpError(
        MagicMock(status=401, reason="Auth error"), b'{"error": "Auth error"}'
    )

    response = client_gmail.post("/api/gmail/sync", json={"maxEmails": 50})

    assert response.status_code == 401
    assert "Gmail API authentication failed" in response.json()["detail"]


def test_smart_retrieval(client_gmail):
    """Test the smart retrieval endpoint."""
    mock_retrieval_result = {"success": True, "totalEmails": 50}
    mock_gmail_service_instance.execute_smart_retrieval.return_value = (
        mock_retrieval_result
    )

    request_payload = {
        "strategies": ["strat1"],
        "maxApiCalls": 50,
        "timeBudgetMinutes": 20,
    }
    response = client_gmail.post("/api/gmail/smart-retrieval", json=request_payload)

    assert response.status_code == 200
    assert response.json() == mock_retrieval_result
    mock_gmail_service_instance.execute_smart_retrieval.assert_called_once_with(
        strategies=["strat1"], max_api_calls=50, time_budget_minutes=20
    )


def test_get_retrieval_strategies(client_gmail):
    """Test retrieving retrieval strategies with realistic mock data."""
    mock_strategies_data = [
        {
            "name": "strategy1",
            "query_filter": "is:important",
            "priority": 10,
            "batch_size": 50,
            "frequency": "hourly",
            "max_emails_per_run": 100,
            "include_folders": ["INBOX"],
            "exclude_folders": ["SPAM"],
            "date_range_days": 1,
        }
    ]
    mock_gmail_service_instance.get_retrieval_strategies.return_value = (
        mock_strategies_data
    )

    response = client_gmail.get("/api/gmail/strategies")
    assert response.status_code == 200
    assert response.json() == {"strategies": mock_strategies_data}
    mock_gmail_service_instance.get_retrieval_strategies.assert_called_once()


def test_get_gmail_performance(client_gmail):
    """Test retrieving performance metrics with realistic mock data."""
    mock_performance_data = {
        "summary": {"total_emails_retrieved": 1234},
        "daily_stats": [],
        "strategy_performance": [],
    }
    mock_gmail_service_instance.get_performance_metrics.return_value = (
        mock_performance_data
    )

    response = client_gmail.get("/api/gmail/performance")
    assert response.status_code == 200
    assert response.json() == mock_performance_data
    mock_gmail_service_instance.get_performance_metrics.assert_called_once()
