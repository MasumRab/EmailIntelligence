import pytest
import os
from unittest.mock import patch, MagicMock
from src.core.integrations.sonarqube_api import SonarQubeClient

@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("SONAR_HOST_URL", "https://mock-sonar.com")
    monkeypatch.setenv("SONAR_PROJECT_KEY", "mock-project")
    monkeypatch.setenv("SONAR_TOKEN", "mock-token")

@pytest.fixture
def sonar_client(mock_env):
    return SonarQubeClient()

def test_init_with_env_vars(sonar_client):
    assert sonar_client.host_url == "https://mock-sonar.com"
    assert sonar_client.project_key == "mock-project"
    assert sonar_client.token == "mock-token"
    assert sonar_client.session.auth == ("mock-token", "")

def test_init_defaults():
    # Clear env vars for this test
    if "SONAR_HOST_URL" in os.environ:
        del os.environ["SONAR_HOST_URL"]

    client = SonarQubeClient()
    assert client.host_url == "https://sonarcloud.io"

@patch('requests.Session.request')
def test_search_issues(mock_request, sonar_client):
    # Setup mock response
    mock_response = MagicMock()
    mock_response.json.return_value = {"issues": [{"key": "ISSUE-1"}]}
    mock_response.raise_for_status.return_value = None
    mock_request.return_value = mock_response

    # Call method
    result = sonar_client.search_issues(severities="MAJOR", types="BUG")

    # Assertions
    assert result == {"issues": [{"key": "ISSUE-1"}]}
    mock_request.assert_called_once_with(
        "GET",
        "https://mock-sonar.com/api/issues/search",
        params={
            "componentKeys": "mock-project",
            "ps": 100,
            "p": 1,
            "severities": "MAJOR",
            "types": "BUG",
            "resolved": "false"
        }
    )

@patch('requests.Session.request')
def test_get_issue_details(mock_request, sonar_client):
    # Setup mock response
    mock_response = MagicMock()
    mock_response.json.return_value = {"issues": [{"key": "ISSUE-1", "message": "Test"}]}
    mock_response.raise_for_status.return_value = None
    mock_request.return_value = mock_response

    # Call method
    result = sonar_client.get_issue_details("ISSUE-1")

    # Assertions
    assert result == {"key": "ISSUE-1", "message": "Test"}
    mock_request.assert_called_once_with(
        "GET",
        "https://mock-sonar.com/api/issues/search",
        params={"issues": "ISSUE-1"}
    )

def test_search_issues_missing_project_key():
    client = SonarQubeClient(project_key=None)
    with pytest.raises(ValueError, match="project_key must be configured"):
        client.search_issues()
