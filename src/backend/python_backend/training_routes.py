"""
DEPRECATED: This module is part of the deprecated `backend` package.
It will be removed in a future release.

Training Routes for AI Model Training

This module provides API endpoints for training AI models used in email analysis.
"""

import logging
from typing import Any, Dict

from fastapi import APIRouter, BackgroundTasks, HTTPException

from src.core.auth import get_current_active_user

from ..python_nlp.ai_training import ModelConfig
from .performance_monitor import log_performance

logger = logging.getLogger(__name__)
router = APIRouter()

# In-memory storage for training jobs (in production, use database)
training_jobs: Dict[str, Dict[str, Any]] = {}


@router.post("/api/training/start")
@log_performance(operation="start_training")
async def start_training(
    model_config: ModelConfig,
    background_tasks: BackgroundTasks,
    current_user: str = Depends(get_current_active_user),
):
    """
    Start training a model with the given configuration.

    Args:
        model_config: Configuration for the model to train
        current_user: The authenticated user making the request
        background_tasks: FastAPI background tasks

    Returns:
        Dict with job_id and status
    """
    import uuid

    job_id = str(uuid.uuid4())

    # Store job info
    training_jobs[job_id] = {
        "status": "running",
        "model_config": model_config,
        "progress": 0.0,
        "message": "Training started",
    }

    # Add background task for training
    background_tasks.add_task(run_training, job_id, model_config)

    logger.info(f"Started training job {job_id} for model {model_config.model_name}")
    return {"job_id": job_id, "status": "running"}


@router.get("/api/training/status/{job_id}")
@log_performance(operation="get_training_status")
async def get_training_status(job_id: str, current_user: str = Depends(get_current_active_user)):
    """
    Get the status of a training job.

    Args:
        job_id: The ID of the training job
        current_user: The authenticated user making the request

    Returns:
        Dict with job status information
    """
    if job_id not in training_jobs:
        raise HTTPException(status_code=404, detail="Training job not found")

    return training_jobs[job_id]


async def run_training(job_id: str, model_config: ModelConfig):
    """
    Background task to run model training.

    Args:
        job_id: The ID of the training job
        model_config: Configuration for the model
    """
    try:
        import os
        import random
        import time

        import pandas as pd
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics import accuracy_score
        from sklearn.model_selection import train_test_split

        # Update progress
        training_jobs[job_id]["progress"] = 0.1
        training_jobs[job_id]["message"] = "Loading training data..."

        # Load training data (dummy for now, in real scenario load from model_config.training_data_path)
        # For demo, create sample data
        sample_data = [
            ("I love this product", "positive"),
            ("This is amazing", "positive"),
            ("Great service", "positive"),
            ("I hate this", "negative"),
            ("This is terrible", "negative"),
            ("Worst experience ever", "negative"),
            ("It's okay", "neutral"),
            ("Not bad", "neutral"),
        ] * 50  # Multiply for more data

        df = pd.DataFrame(sample_data, columns=["text", "sentiment"])

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            df["text"], df["sentiment"], test_size=0.2, random_state=42
        )

        training_jobs[job_id]["progress"] = 0.3
        training_jobs[job_id]["message"] = "Vectorizing text..."

        # Vectorize text
        vectorizer = TfidfVectorizer(max_features=1000)
        X_train_vec = vectorizer.fit_transform(X_train)
        X_test_vec = vectorizer.transform(X_test)

        training_jobs[job_id]["progress"] = 0.5
        training_jobs[job_id]["message"] = "Training model..."

        # Train model
        model = LogisticRegression(random_state=42)
        model.fit(X_train_vec, y_train)

        training_jobs[job_id]["progress"] = 0.8
        training_jobs[job_id]["message"] = "Evaluating model..."

        # Evaluate
        y_pred = model.predict(X_test_vec)
        accuracy = accuracy_score(y_test, y_pred)

        training_jobs[job_id]["progress"] = 0.9
        training_jobs[job_id]["message"] = "Saving model..."

        # Save model (in real scenario, save to configured path)
        import joblib

        model_path = f"models/{model_config.model_name}_{job_id}.pkl"
        os.makedirs("models", exist_ok=True)
        joblib.dump((model, vectorizer), model_path)

        training_jobs[job_id]["status"] = "completed"
        training_jobs[job_id][
            "message"
        ] = f"Training completed successfully. Accuracy: {accuracy:.2f}"
        training_jobs[job_id]["accuracy"] = accuracy
        training_jobs[job_id]["model_path"] = model_path

        logger.info(f"Training job {job_id} completed with accuracy {accuracy}")

    except Exception as e:
        training_jobs[job_id]["status"] = "failed"
        training_jobs[job_id]["message"] = f"Training failed: {str(e)}"
        logger.error(f"Training job {job_id} failed: {e}")
