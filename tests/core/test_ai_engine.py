
import pytest
from src.core.ai_engine import ModernAIEngine, AIAnalysisResult

@pytest.mark.asyncio
async def test_analyze_email_basic():
    engine = ModernAIEngine()
    engine.initialize()

    subject = "Test Subject"
    content = "This is a test content with positive words like love and happy."

    result = await engine.analyze_email(subject, content)

    assert isinstance(result, AIAnalysisResult)
    assert result.sentiment == "positive"
    assert "positive_sentiment" not in result.risk_flags

@pytest.mark.asyncio
async def test_analyze_email_negative_urgent():
    engine = ModernAIEngine()
    engine.initialize()

    subject = "URGENT: Critical Issue"
    content = "This is terrible and bad. We have a problem."

    result = await engine.analyze_email(subject, content)

    assert result.sentiment == "negative"
    assert result.urgency == "high"
    assert "negative_sentiment" in result.risk_flags
    assert "high_urgency" in result.risk_flags

@pytest.mark.asyncio
async def test_analyze_email_intent_question():
    engine = ModernAIEngine()
    engine.initialize()

    subject = "Question"
    content = "How do I reset my password?"

    result = await engine.analyze_email(subject, content)

    assert result.intent == "question"

@pytest.mark.asyncio
async def test_analyze_email_topics():
    engine = ModernAIEngine()
    engine.initialize()

    subject = "Project Update"
    content = "We have a meeting about the database deadline."

    result = await engine.analyze_email(subject, content)

    assert "work" in result.categories or "technical" in result.categories
