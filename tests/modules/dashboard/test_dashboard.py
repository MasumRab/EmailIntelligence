import pytest
from fastapi.testclient import TestClient


def test_read_main(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_get_dashboard_data(client: TestClient):
    response = client.get("/api/dashboard/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_emails" in data
    assert "categorized_emails" in data
    assert "unread_emails" in data


def test_get_performance_metrics(client: TestClient):
    response = client.get("/api/dashboard/performance")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
