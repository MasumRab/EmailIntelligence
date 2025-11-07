import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.backend.python_backend.ai_engine import AdvancedAIEngine, AIAnalysisResult
from src.backend.python_backend.model_manager import ModelManager

# This mock is for the database, which is used for category lookups
mock_db_manager_for_ai_engine = MagicMock()
mock_db_manager_for_ai_engine.get_all_categories = AsyncMock()


@pytest.fixture
def mock_model_manager():
    """Fixture for a mocked ModelManager that returns mock models."""
    manager = MagicMock(spec=ModelManager)

    # Create mock models for sentiment and topic
    mock_sentiment_model = MagicMock()
    mock_sentiment_model.analyze.return_value = {
        "sentiment": "neutral",
        "confidence": 0.8,
        "method_used": "mock_sentiment",
    }

    mock_topic_model = MagicMock()
    mock_topic_model.analyze.return_value = {
        "topic": "General",
        "confidence": 0.9,
        "method_used": "mock_topic",
    }

    # Configure get_model to return the correct mock model
    def get_model_side_effect(model_name):
        if model_name == "sentiment-default":
            return mock_sentiment_model
        if model_name == "topic-default":
            return mock_topic_model
        return MagicMock()

    manager.get_model.side_effect = get_model_side_effect

    # Add the mock models to the manager instance so we can assert on them
    manager.mock_sentiment_model = mock_sentiment_model
    manager.mock_topic_model = mock_topic_model

    return manager


@pytest.fixture
def ai_engine_instance(mock_model_manager):
    """Fixture to provide an AdvancedAIEngine instance with a mocked ModelManager."""
    # Reset mocks before each test
    mock_db_manager_for_ai_engine.get_all_categories.reset_mock()
    mock_db_manager_for_ai_engine.get_all_categories.side_effect = None
    mock_model_manager.get_model.reset_mock()
    mock_model_manager.mock_sentiment_model.analyze.reset_mock()
    mock_model_manager.mock_topic_model.analyze.reset_mock()

    engine = AdvancedAIEngine(model_manager=mock_model_manager)
    return engine


# Define a default model configuration for the tests
DEFAULT_MODELS_TO_USE = {
    "sentiment": "sentiment-default",
    "topic": "topic-default",
}


@pytest.mark.asyncio
async def test_analyze_email_no_db_provided(
    ai_engine_instance: AdvancedAIEngine, mock_model_manager
):
    subject = "Test Subject"
    content = "Test Content"
    full_text = f"{subject}\n{content}"

    result = await ai_engine_instance.analyze_email(
        subject, content, models_to_use=DEFAULT_MODELS_TO_USE, db=None
    )

    assert isinstance(result, AIAnalysisResult)
    assert result.topic == "General"
    assert result.sentiment == "neutral"
    assert result.category_id is None

    mock_model_manager.get_model.assert_any_call("sentiment-default")
    mock_model_manager.get_model.assert_any_call("topic-default")
    mock_model_manager.mock_sentiment_model.analyze.assert_called_once_with(full_text)
    mock_model_manager.mock_topic_model.analyze.assert_called_once_with(full_text)


@pytest.mark.asyncio
async def test_analyze_email_with_db_category_match(
    ai_engine_instance: AdvancedAIEngine, mock_model_manager
):
    subject = "Work Email"
    content = "Project discussion about work."

    mock_model_manager.mock_topic_model.analyze.return_value = {
        "topic": "Work Related",
        "confidence": 0.95,
        "method_used": "mock_topic",
    }

    mock_db_categories = [{"id": 5, "name": "Work Related"}]
    mock_db_manager_for_ai_engine.get_all_categories.return_value = mock_db_categories

    result = await ai_engine_instance.analyze_email(
        subject, content, models_to_use=DEFAULT_MODELS_TO_USE, db=mock_db_manager_for_ai_engine
    )

    assert isinstance(result, AIAnalysisResult)
    assert result.category_id == 5
    assert result.categories == ["Work Related"]
    mock_db_manager_for_ai_engine.get_all_categories.assert_called_once()


@pytest.mark.asyncio
async def test_analyze_email_with_db_no_category_match(ai_engine_instance: AdvancedAIEngine):
    subject = "Unique Topic"
    content = "Content about something new."

    mock_db_categories = [{"id": 1, "name": "Personal"}]
    mock_db_manager_for_ai_engine.get_all_categories.return_value = mock_db_categories

    result = await ai_engine_instance.analyze_email(
        subject, content, models_to_use=DEFAULT_MODELS_TO_USE, db=mock_db_manager_for_ai_engine
    )

    assert isinstance(result, AIAnalysisResult)
    assert result.category_id is None


@pytest.mark.asyncio
async def test_analyze_email_model_failure(
    ai_engine_instance: AdvancedAIEngine, mock_model_manager
):
    subject = "Test Subject"
    content = "Test Content"

    mock_model_manager.mock_sentiment_model.analyze.side_effect = Exception("Model exploded")

    result = await ai_engine_instance.analyze_email(
        subject, content, models_to_use=DEFAULT_MODELS_TO_USE
    )

    assert isinstance(result, AIAnalysisResult)
    assert "Critical failure" in result.reasoning
    assert "Model exploded" in result.reasoning
