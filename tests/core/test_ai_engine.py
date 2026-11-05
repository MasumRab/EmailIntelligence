import pytest
import pytest_asyncio
from unittest.mock import MagicMock
from src.core.ai_engine import ModernAIEngine
from src.core.dynamic_model_manager import DynamicModelManager

@pytest.fixture
def mock_model_manager():
    manager = MagicMock(spec=DynamicModelManager)

    async def return_none():
        return None

    manager.get_sentiment_model.side_effect = return_none
    manager.get_topic_model.side_effect = return_none
    manager.get_intent_model.side_effect = return_none
    manager.get_urgency_model.side_effect = return_none

    return manager

@pytest_asyncio.fixture
async def ai_engine(mock_model_manager):
    engine = ModernAIEngine(model_manager=mock_model_manager)
    await engine.initialize()
    return engine

@pytest.mark.asyncio
async def test_sentiment_analysis_fallback_positive(ai_engine):
    subject = "Great news"
    content = "I love this product, it is excellent and I am happy."
    result = await ai_engine.analyze_email(subject, content)
    assert result.sentiment == "positive"

@pytest.mark.asyncio
async def test_sentiment_analysis_fallback_negative(ai_engine):
    subject = "Bad news"
    content = "This is terrible, I hate it and it is a problem."
    result = await ai_engine.analyze_email(subject, content)
    assert result.sentiment == "negative"

@pytest.mark.asyncio
async def test_topic_analysis_fallback(ai_engine):
    subject = "Meeting"
    content = "Let's schedule a project deadline meeting at the office."
    result = await ai_engine.analyze_email(subject, content)
    assert "work" in result.categories

@pytest.mark.asyncio
async def test_intent_analysis_fallback_question(ai_engine):
    subject = "Question"
    content = "What is the status?"
    result = await ai_engine.analyze_email(subject, content)
    assert result.intent == "question"

@pytest.mark.asyncio
async def test_intent_analysis_fallback_request(ai_engine):
    subject = "Help"
    content = "Can you please help me?"
    result = await ai_engine.analyze_email(subject, content)
    assert result.intent == "question"
    # Logic note: "?" takes precedence in simple_intent_analysis.

@pytest.mark.asyncio
async def test_urgency_analysis_fallback_high(ai_engine):
    subject = "Urgent"
    content = "This is critical and needs to be done ASAP."
    result = await ai_engine.analyze_email(subject, content)
    assert result.urgency == "high"

@pytest.mark.asyncio
async def test_keywords_extraction(ai_engine):
    subject = "Test"
    content = "Banana Apple Orange Strawberry"
    result = await ai_engine.analyze_email(subject, content)
    # keywords: length > 3
    assert "banana" in result.keywords
    assert "apple" in result.keywords
