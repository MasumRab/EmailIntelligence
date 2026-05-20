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
    assert result == [{"key": "ISSUE-1"}]
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

@patch("src.core.integrations.sonarqube_api.SonarQubeClient._make_request")
def test_search_issues_missing_project_key(mock_request):
    mock_request.return_value = {"issues": []}
    client = SonarQubeClient(project_key=None)
    result = client.search_issues()
    assert result == []


def test_get_issues_stops_at_limit_and_truncates(sonar_client):
    # limit smaller than total; ensure we stop early and truncate
    limit = 150
    calls = []

    def fake_search_issues(**params):
        calls.append(params)
        page = params.get("page_index", 1)
        page_size = params.get("page_size", 100)

        if page == 1:
            issues = [{"key": f"ISSUE-{i}"} for i in range(1, page_size + 1)]
            total = 300  # more than limit
        elif page == 2:
            issues = [{"key": f"ISSUE-{100 + i}"} for i in range(1, page_size + 1)]
            total = 300
        else:
            issues = []
            total = 300

        return {
            "issues": issues,
            "paging": {
                "pageIndex": page,
                "pageSize": page_size,
                "total": total,
            },
        }

    sonar_client.search_issues = MagicMock(side_effect=fake_search_issues)

    issues = sonar_client.get_issues(severities="MAJOR", types="BUG", limit=limit)

    # We should have exactly `limit` issues even though more are available
    assert len(issues) == limit

    # Should only call for page 1 and 2, not page 3
    page_indexes = [c["page_index"] for c in calls]
    assert page_indexes == [1, 2]

    # Page size should be min(limit, 100) == 100 on first page
    assert calls[0]["page_size"] == 100
    # Second page should still be 100, but get_issues should truncate to 50 from it


def test_get_issues_aggregates_multiple_pages(sonar_client):
    # Verify it aggregates multiple pages with adjusted total
    limit = 250
    calls = []

    def fake_search_issues(**params):
        calls.append(params)
        page = params.get("page_index", 1)
        page_size = params.get("page_size", 100)

        if page == 1:
            issues = [{"key": f"ISSUE-{i}"} for i in range(1, page_size + 1)]
            total = 180  # total smaller than limit, will require only two pages
        elif page == 2:
            remaining = 80
            issues = [{"key": f"ISSUE-{100 + i}"} for i in range(1, remaining + 1)]
            total = 180
        else:
            issues = []
            total = 180

        return {
            "issues": issues,
            "paging": {
                "pageIndex": page,
                "pageSize": page_size,
                "total": total,
            },
        }

    sonar_client.search_issues = MagicMock(side_effect=fake_search_issues)

    issues = sonar_client.get_issues(severities="MAJOR", types="BUG", limit=limit)

    # We should get all issues up to total (180), not the limit (250)
    assert len(issues) == 180

    # Should only call for page 1 and 2
    page_indexes = [c["page_index"] for c in calls]
    assert page_indexes == [1, 2]

    # First call page size should be 100
    assert calls[0]["page_size"] == 100
    # Second call page size remains 100 (the API's page size), but fewer issues returned


def test_get_issues_stops_when_total_less_than_limit(sonar_client):
    # When total < limit, ensure no extra calls beyond final page
    limit = 200
    calls = []

    def fake_search_issues(**params):
        calls.append(params)
        page = params.get("page_index", 1)
        page_size = params.get("page_size", 100)

        if page == 1:
            issues = [{"key": f"ISSUE-{i}"} for i in range(1, 52)]
            total = 51  # Only 51 issues in total
        else:
            issues = []
            total = 51

        return {
            "issues": issues,
            "paging": {
                "pageIndex": page,
                "pageSize": page_size,
                "total": total,
            },
        }

    sonar_client.search_issues = MagicMock(side_effect=fake_search_issues)

    issues = sonar_client.get_issues(severities="MAJOR", types="BUG", limit=limit)

    # We should get all available issues (51), not the limit (200)
    assert len(issues) == 51

    # Only first page should be requested because total < limit and < page_size
    page_indexes = [c["page_index"] for c in calls]
    assert page_indexes == [1]

    # Page size should still respect min(limit, 100)
    assert calls[0]["page_size"] == 100
