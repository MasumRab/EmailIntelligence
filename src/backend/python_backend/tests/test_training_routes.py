"""
Tests for AI model training routes.
"""
<<<<<<< HEAD:src/backend/python_backend/tests/test_training_routes.py
from unittest.mock import patch
=======
from unittest.mock import MagicMock, patch
>>>>>>> cafdba94 (Refactor: Introduce EmailService, WorkflowEngine, and AdvancedAIEngine; update performance monitoring and documentation.):backend/python_backend/tests/test_training_routes.py

import numpy as np
import pandas as pd
import pytest

from backend.python_backend.training_routes import run_training, training_jobs
from backend.python_nlp.ai_training import ModelConfig


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
    assert data["status"] == "completed"
    assert "progress" in data


def test_get_training_status_not_found(client):
    """Test getting status for non-existent job."""
    response = client.get("/api/training/status/nonexistent")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_run_training():
    """Test the background training function."""
    config = ModelConfig(
        model_name="test",
        model_type="classification",
        training_data_path="dummy",
        parameters={"epochs": 1},
    )

    job_id = "test_job"
    training_jobs[job_id] = {"status": "running"}

    # Mock dependencies to avoid actual file I/O and heavy computation
    with patch("pandas.DataFrame") as mock_df, \
         patch("sklearn.model_selection.train_test_split") as mock_split, \
         patch("sklearn.feature_extraction.text.TfidfVectorizer") as mock_vectorizer, \
         patch("sklearn.linear_model.LogisticRegression") as mock_model, \
         patch("sklearn.metrics.accuracy_score") as mock_accuracy, \
         patch("joblib.dump"):

        # Setup mock return values
        mock_df.return_value = pd.DataFrame({
            "text": ["good", "bad"] * 50,
            "sentiment": ["positive", "negative"] * 50,
        })
        mock_split.return_value = (
            pd.Series(["train_text"] * 80), pd.Series(["test_text"] * 20),
            pd.Series(["train_label"] * 80), pd.Series(["test_label"] * 20)
        )
        mock_vectorizer_instance = mock_vectorizer.return_value
        mock_vectorizer_instance.fit_transform.return_value = np.random.rand(80, 10)
        mock_vectorizer_instance.transform.return_value = np.random.rand(20, 10)
        mock_model_instance = mock_model.return_value
        mock_model_instance.predict.return_value = np.array(["positive"] * 20)
        mock_accuracy.return_value = 0.95

        await run_training(job_id, config)

        assert training_jobs[job_id]["status"] == "completed"
