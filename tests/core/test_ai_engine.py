import pytest
from src.core.ai_engine import ModernAIEngine

@pytest.fixture
def engine():
    engine = ModernAIEngine()
    engine.initialize()
    return engine

def test_simple_sentiment_analysis(engine):
    # Positive
    result = engine._simple_sentiment_analysis("I love this great product")
    assert result["label"] == "positive"

    # Negative
    result = engine._simple_sentiment_analysis("I hate this terrible bug")
    assert result["label"] == "negative"

    # Neutral
    result = engine._simple_sentiment_analysis("This is a meeting")
    assert result["label"] == "neutral"

def test_rule_based_topics(engine):
    # Work
    topics = engine._rule_based_topics("Let's have a meeting about the project deadline")
    assert "work" in topics

    # Finance
    topics = engine._rule_based_topics("Please pay the invoice for the bill")
    assert "finance" in topics

    # Technical
    topics = engine._rule_based_topics("The database server has a bug in the api")
    assert "technical" in topics

def test_simple_intent_analysis(engine):
    # Question
    intent = engine._simple_intent_analysis("What is the status?")
    assert intent["type"] == "question"

    # Request (avoid '?' to prevent it being classified as question)
    intent = engine._simple_intent_analysis("Please help me")
    assert intent["type"] == "request"

    # Gratitude
    intent = engine._simple_intent_analysis("Thank you very much")
    assert intent["type"] == "gratitude"

def test_simple_urgency_analysis(engine):
    # High urgency
    urgency = engine._simple_urgency_analysis("This is urgent and critical")
    assert urgency["level"] == "high"

    # Low urgency
    urgency = engine._simple_urgency_analysis("Just a regular update")
    assert urgency["level"] == "low"

def test_extract_keywords(engine):
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
