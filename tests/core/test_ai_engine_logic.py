
import pytest
from unittest.mock import MagicMock, AsyncMock
from src.core.ai_engine import ModernAIEngine
from src.core.dynamic_model_manager import DynamicModelManager

@pytest.mark.asyncio
async def test_analyze_email_simple_sentiment():
    """Test that analyze_email uses simple sentiment analysis correctly."""
    engine = ModernAIEngine(model_manager=None)
    engine._initialized = True

    # Test positive case
    result = await engine.analyze_email("Great news", "I am very happy with the results. Excellent work!")
    assert result.sentiment == "positive"
    assert "sentiment:positive" in result.suggested_labels

    # Test negative case
    result = await engine.analyze_email("Bad news", "I hate this problem. It is terrible.")
    assert result.sentiment == "negative"
    assert "sentiment:negative" in result.suggested_labels

    # Test neutral case
    result = await engine.analyze_email("Update", "The meeting is at 5pm.")
    assert result.sentiment == "neutral"

@pytest.mark.asyncio
async def test_analyze_email_simple_topics():
    """Test that analyze_email uses simple topic detection correctly."""
    engine = ModernAIEngine(model_manager=None)
    engine._initialized = True

    # Test work topic
    result = await engine.analyze_email("Meeting", "Let's discuss the project deadline.")
    assert "work" in result.categories
    assert result.topic == "work"

    # Test finance topic
    result = await engine.analyze_email("Invoice", "Please pay the bill.")
    assert "finance" in result.categories

    # Test general topic
    result = await engine.analyze_email("Hello", "How are you?")
    assert result.topic == "general"

@pytest.mark.asyncio
async def test_analyze_email_keywords():
    """Test keyword extraction."""
    engine = ModernAIEngine(model_manager=None)
    engine._initialized = True

    content = "The quick brown fox jumps over the lazy dog. Programming is fun."
    result = await engine.analyze_email("Subject", content)

    # "quick", "brown", "jumps", "lazy", "programming" should be keywords
    # "the", "over" are stop words or short
    assert "programming" in result.keywords
    assert "quick" in result.keywords
    assert "the" not in result.keywords

@pytest.mark.asyncio
async def test_analyze_email_with_mocked_model_manager():
    """Test analyze_email with a mocked model manager returning None (fallback path)."""
    mock_manager = MagicMock(spec=DynamicModelManager)
    # Important: Configure AsyncMock for async methods
    mock_manager.get_sentiment_model = AsyncMock(return_value=None)
    mock_manager.get_topic_model = AsyncMock(return_value=None)
    mock_manager.get_intent_model = AsyncMock(return_value=None)
    mock_manager.get_urgency_model = AsyncMock(return_value=None)

    engine = ModernAIEngine(model_manager=mock_manager)
    await engine.initialize()

    result = await engine.analyze_email("Test", "This is a test.")
    assert result.sentiment == "neutral"

    # Verify get_sentiment_model was called (and awaited properly)
    mock_manager.get_sentiment_model.assert_called_once()

@pytest.mark.asyncio
async def test_analyze_email_with_mocked_model_manager_returning_model():
    """Test analyze_email with a mocked model manager returning a model."""
    mock_manager = MagicMock(spec=DynamicModelManager)

    mock_sentiment_model = AsyncMock()
    mock_sentiment_model.analyze.return_value = {"label": "positive", "confidence": 0.9}

    mock_manager.get_sentiment_model = AsyncMock(return_value=mock_sentiment_model)
    mock_manager.get_topic_model = AsyncMock(return_value=None)
    mock_manager.get_intent_model = AsyncMock(return_value=None)
    mock_manager.get_urgency_model = AsyncMock(return_value=None)

    engine = ModernAIEngine(model_manager=mock_manager)
    await engine.initialize()

    result = await engine.analyze_email("Test", "This content doesn't matter as model is mocked.")

    # Should use the model result
    assert result.sentiment == "positive"
    mock_sentiment_model.analyze.assert_called_once()
