import pytest
import asyncio
from core.ai_engine import ModernAIEngine

@pytest.mark.asyncio
async def test_fallback_analysis_sentiment_positive():
    engine = ModernAIEngine()
    engine.initialize()
    engine._model_manager = None  # Force fallback

    # "Great" -> positive
    result = await engine.analyze_email("Update", "This is great work")
    assert result.sentiment == "positive"

@pytest.mark.asyncio
async def test_fallback_analysis_sentiment_negative():
    engine = ModernAIEngine()
    engine.initialize()
    engine._model_manager = None

    # "Terrible" -> negative
    result = await engine.analyze_email("Issue", "This is terrible")
    assert result.sentiment == "negative"

@pytest.mark.asyncio
async def test_fallback_analysis_topics():
    engine = ModernAIEngine()
    engine.initialize()
    engine._model_manager = None

    # "meeting" -> work, "invoice" -> finance
    result = await engine.analyze_email("Meeting", "Please check the invoice")
    assert "work" in result.categories or "finance" in result.categories
    # The current implementation might pick one or both depending on order and logic
    # _rule_based_topics iterates topic_patterns. "work" comes before "finance" in the dict usually?
    # Actually python 3.7+ dicts preserve insertion order.
    # work: meeting
    # finance: invoice
    # It finds all matching topics.

@pytest.mark.asyncio
async def test_fallback_analysis_intent_question():
    engine = ModernAIEngine()
    engine.initialize()
    engine._model_manager = None

    result = await engine.analyze_email("Question", "What is the status?")
    assert result.intent == "question"

@pytest.mark.asyncio
async def test_fallback_analysis_urgency_high():
    engine = ModernAIEngine()
    engine.initialize()
    engine._model_manager = None

    result = await engine.analyze_email("Urgent", "Please reply ASAP")
    assert result.urgency == "high"

@pytest.mark.asyncio
async def test_fallback_analysis_keywords():
    engine = ModernAIEngine()
    engine.initialize()
    engine._model_manager = None

    # "project", "deadline" should be keywords (len > 3, not stop words)
    result = await engine.analyze_email("Project", "The deadline is approaching")
    assert "project" in result.keywords or "deadline" in result.keywords
