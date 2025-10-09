"""
Tests for training routes.
"""

from unittest.mock import MagicMock, patch

import pytest

from backend.python_backend.training_routes import run_training


def test_start_training(client):
    """Test starting a training job."""
    config = {
        "model_name": "test_model",
        "model_type": "classification",
        "training_data_path": "/path/to/data",
        "parameters": {"epochs": 5},
    }

    with patch("backend.python_backend.training_routes.BackgroundTasks") as mock_bg:
        response = client.post("/api/training/start", json=config)
        assert response.status_code == 200
        data = response.json()
        assert "job_id" in data
        assert data["status"] == "running"


def test_get_training_status(client):
    """Test getting training status."""
    # First start a job
    config = {
        "model_name": "test_model",
        "model_type": "classification",
        "training_data_path": "/path/to/data",
        "parameters": {"epochs": 5},
    }

    with patch("backend.python_backend.training_routes.BackgroundTasks"):
        start_response = client.post("/api/training/start", json=config)
        job_id = start_response.json()["job_id"]

    # Check status
    response = client.get(f"/api/training/status/{job_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"
    assert "progress" in data


def test_get_training_status_not_found(client):
    """Test getting status for non-existent job."""
    response = client.get("/api/training/status/nonexistent")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_run_training():
    """Test the background training function."""
    from backend.python_nlp.ai_training import ModelConfig

    config = ModelConfig(
        model_name="test",
        model_type="classification",
        training_data_path="dummy",
        parameters={"epochs": 1},
    )

    # Mock the training_jobs dict
    with patch("backend.python_backend.training_routes.training_jobs") as mock_jobs:
        mock_jobs.__setitem__ = MagicMock()
        mock_jobs.__getitem__ = MagicMock(return_value={"status": "running"})

        # Mock sklearn and joblib to avoid actual training in tests
        with (
            patch("backend.python_backend.training_routes.LogisticRegression"),
            patch("backend.python_backend.training_routes.TfidfVectorizer"),
            patch("backend.python_backend.training_routes.joblib.dump"),
        ):

            await run_training("test_job", config)

            # Check that status was updated to completed
            calls = mock_jobs.__setitem__.call_args_list
            status_updates = [call for call in calls if call[0][1].get("status") == "completed"]
            assert len(status_updates) > 0
