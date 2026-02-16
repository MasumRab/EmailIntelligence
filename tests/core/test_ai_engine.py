import pytest
import pytest_asyncio
from unittest.mock import AsyncMock
from src.core.ai_engine import ModernAIEngine

@pytest_asyncio.fixture
async def engine():
    mock_manager = AsyncMock()
    # Mock initialize on the manager
    mock_manager.initialize = AsyncMock()
    engine = ModernAIEngine(model_manager=mock_manager)
    await engine.initialize()
    return engine

@pytest.mark.asyncio
async def test_simple_sentiment_analysis(engine):
    # Positive
    result = await engine._simple_sentiment_analysis("I love this great product")
    assert result["label"] == "positive"

    # Negative
    result = await engine._simple_sentiment_analysis("I hate this terrible bug")
    assert result["label"] == "negative"

    # Neutral
    result = await engine._simple_sentiment_analysis("This is a meeting")
    assert result["label"] == "neutral"

@pytest.mark.asyncio
async def test_rule_based_topics(engine):
    # Work
    topics = await engine._rule_based_topics("Let's have a meeting about the project deadline")
    assert "work" in topics

    # Finance
    topics = await engine._rule_based_topics("Please pay the invoice for the bill")
    assert "finance" in topics

    # Technical
    topics = await engine._rule_based_topics("The database server has a bug in the api")
    assert "technical" in topics

@pytest.mark.asyncio
async def test_simple_intent_analysis(engine):
    # Question
    intent = await engine._simple_intent_analysis("What is the status?")
    assert intent["type"] == "question"

    # Request (avoid '?' to prevent it being classified as question)
    intent = await engine._simple_intent_analysis("Please help me")
    assert intent["type"] == "request"

    # Gratitude
    intent = await engine._simple_intent_analysis("Thank you very much")
    assert intent["type"] == "gratitude"

@pytest.mark.asyncio
async def test_simple_urgency_analysis(engine):
    # High urgency
    urgency = await engine._simple_urgency_analysis("This is urgent and critical")
    assert urgency["level"] == "high"

    # Low urgency
    urgency = await engine._simple_urgency_analysis("Just a regular update")
    assert urgency["level"] == "low"

@pytest.mark.asyncio
async def test_extract_keywords(engine):
    text = "The quick brown fox jumps over the lazy dog"
    # Stop words "the", "over" should be removed. Short words "fox", "dog" might be kept if > 3 chars
    # "fox" is 3 chars, so it might be removed if condition is > 3 (so 4+ chars)
    # "brown", "quick", "jumps", "lazy" are > 3
    keywords = engine._extract_keywords(text)

    assert "brown" in keywords
    assert "quick" in keywords
    assert "jumps" in keywords
    assert "lazy" in keywords
    assert "the" not in keywords
