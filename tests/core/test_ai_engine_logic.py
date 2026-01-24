import pytest
import asyncio
from src.core.ai_engine import ModernAIEngine

@pytest.mark.asyncio
async def test_analyze_email_logic():
    engine = ModernAIEngine()
    engine.initialize()

    # Test sentiment
    result = await engine.analyze_email("Subject", "I love this product, it is great!")
    assert result.sentiment == "positive"

    result = await engine.analyze_email("Subject", "This is terrible and I hate it.")
    assert result.sentiment == "negative"

    # Test intent
    # Note: "Can you please help me with this?" contains "?" so it is classified as question by the simple logic.
    result = await engine.analyze_email("Subject", "Please help me with this")
    assert result.intent == "request"

    result = await engine.analyze_email("Subject", "What is the status?")
    assert result.intent == "question"

    # Test urgency
    result = await engine.analyze_email("Subject", "This is urgent deadline ASAP.")
    assert result.urgency == "high"

    # Test topic
    result = await engine.analyze_email("Subject", "We need to discuss the project deadline in the office.")
    assert "work" in result.categories

    result = await engine.analyze_email("Subject", "Here is the invoice for payment.")
    assert "finance" in result.categories

@pytest.mark.asyncio
async def test_extract_keywords():
    engine = ModernAIEngine()
    engine.initialize()

    text = "The quick brown fox jumps over the lazy dog."

    result = await engine.analyze_email("Subject", "The quick brown fox jumps over the lazy dog.")
    keywords = result.keywords

    assert "quick" in keywords
    assert "brown" in keywords
    assert "jumps" in keywords
    assert "lazy" in keywords
    assert "over" in keywords

@pytest.mark.asyncio
async def test_analyze_email_empty():
    engine = ModernAIEngine()
    engine.initialize()

    result = await engine.analyze_email("", "")
    assert result.sentiment == "neutral"
    assert result.intent == "information" # Default fallback
    assert result.urgency == "low"
