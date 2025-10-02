import logging
from unittest.mock import MagicMock, patch

import pytest

from backend.python_nlp.nlp_engine import NLPEngine

# Suppress logging for tests
logging.disable(logging.CRITICAL)


def test_analyze_email_success_path():
    """
    Test the successful, standard analysis flow of the analyze_email method.
    """
    with patch("backend.python_nlp.nlp_engine.HAS_SKLEARN_AND_JOBLIB", True), \
         patch("backend.python_nlp.nlp_engine.HAS_NLTK", True), \
         patch("backend.python_nlp.nlp_engine.NLPEngine._categorize_content", return_value=["Work & Business"]), \
         patch("backend.python_nlp.nlp_engine.NLPEngine._extract_keywords", return_value=["project", "deadline"]), \
         patch("backend.python_nlp.nlp_engine.UrgencyModel") as mock_urgency, \
         patch("backend.python_nlp.nlp_engine.IntentModel") as mock_intent, \
         patch("backend.python_nlp.nlp_engine.TopicModel") as mock_topic, \
         patch("backend.python_nlp.nlp_engine.SentimentModel") as mock_sentiment:

        # Mock the analyzer components' return values
        mock_sentiment.return_value.analyze.return_value = {
            "sentiment": "positive", "confidence": 0.9, "method_used": "model_sentiment"
        }
        mock_topic.return_value.analyze.return_value = {
            "topic": "work_business", "confidence": 0.85, "method_used": "model_topic"
        }
        mock_intent.return_value.analyze.return_value = {
            "intent": "question", "confidence": 0.95, "method_used": "model_intent"
        }
        mock_urgency.return_value.analyze.return_value = {
            "urgency": "high", "confidence": 0.7, "method_used": "model_urgency"
        }

        engine = NLPEngine()
        subject = "Project Update"
        content = "What is the status of the new project? We need to meet the deadline."
        result = engine.analyze_email(subject, content)

        assert result["sentiment"] == "positive"
        assert result["topic"] == "work_business"
        assert result["intent"] == "question"
        assert result["urgency"] == "high"
        assert "work" in result["reasoning"].lower()
        assert "positive" in result["reasoning"].lower()
        assert "high" in result["reasoning"].lower()
        assert "High Priority" in result["suggested_labels"]


def test_analyze_email_simple_fallback_when_deps_missing():
    """
    Test that analyze_email uses the simple keyword-based fallback
    when major dependencies like NLTK and sklearn are missing.
    """
    with patch("backend.python_nlp.nlp_engine.HAS_SKLEARN_AND_JOBLIB", False), \
         patch("backend.python_nlp.nlp_engine.HAS_NLTK", False):
        engine = NLPEngine()
        subject = "Urgent meeting required"
        content = "We need to discuss the project budget ASAP."
        result = engine.analyze_email(subject, content)

        assert result["urgency"] == "high"
        assert result["topic"] == "work_business"
        assert "keyword matching" in result["reasoning"]
        assert result["validation"]["method"] == "basic_fallback"


def test_analyze_email_full_fallback_on_exception():
    """
    Test that a generic exception during analysis triggers the full fallback.
    """
    with patch("backend.python_nlp.nlp_engine.HAS_SKLEARN_AND_JOBLIB", True), \
         patch("backend.python_nlp.nlp_engine.HAS_NLTK", True), \
         patch.object(NLPEngine, "_preprocess_text", side_effect=Exception("Unexpected error")) as mock_preprocess:
        engine = NLPEngine()
        result = engine.analyze_email("Test", "Test")

        mock_preprocess.assert_called_once()
        assert result["topic"] == "General"
        assert result["sentiment"] == "neutral"
        assert result["risk_flags"] == ["analysis_failed"]
        assert "Unexpected error" in result["reasoning"]
        assert result["validation"]["method"] == "fallback"


def test_build_final_response_structure():
    """
    Verify that the final response dictionary has the correct structure and keys.
    """
    with patch("backend.python_nlp.nlp_engine.TopicModel") as mock_topic, \
         patch("backend.python_nlp.nlp_engine.SentimentModel") as mock_sentiment:

        mock_sentiment.return_value.analyze.return_value = {"sentiment": "neutral", "confidence": 0.5}
        mock_topic.return_value.analyze.return_value = {"topic": "General", "confidence": 0.5}

        engine = NLPEngine()
        response = engine._build_final_analysis_response(
            sentiment_analysis={"sentiment": "neutral", "confidence": 0.5},
            topic_analysis={"topic": "General", "confidence": 0.5},
            intent_analysis=None,
            urgency_analysis=None,
            categories=["General"],
            keywords=[],
            risk_analysis_flags=[],
        )

        expected_keys = [
            "topic", "sentiment", "intent", "urgency", "confidence",
            "categories", "keywords", "reasoning", "suggested_labels",
            "risk_flags", "validation", "details"
        ]
        for key in expected_keys:
            assert key in response

        assert isinstance(response["details"], dict)
        assert "sentiment_analysis" in response["details"]


def test_analyze_topic_with_analyzer():
    """Test _analyze_topic when the analyzer is available."""
    with patch.object(NLPEngine, "_analyze_topic_keyword") as mock_fallback:
        engine = NLPEngine()
        # Mock the analyzer component
        engine.topic_analyzer = MagicMock()
        engine.topic_analyzer.analyze.return_value = {"topic": "test_topic"}

        result = engine._analyze_topic("some text")

        engine.topic_analyzer.analyze.assert_called_once_with("some text")
        mock_fallback.assert_not_called()
        assert result["topic"] == "test_topic"


def test_analyze_topic_without_analyzer():
    """Test _analyze_topic fallback when the analyzer is missing."""
    with patch.object(NLPEngine, "_analyze_topic_keyword") as mock_fallback:
        mock_fallback.return_value = {"topic": "fallback_topic"}
        engine = NLPEngine()
        engine.topic_analyzer = None  # Ensure analyzer is not available

        result = engine._analyze_topic("some text")

        mock_fallback.assert_called_once_with("some text")
        assert result["topic"] == "fallback_topic"


def test_analyze_intent_with_analyzer():
    """Test _analyze_intent when the analyzer is available."""
    engine = NLPEngine()
    engine.intent_analyzer = MagicMock()
    engine.intent_analyzer.analyze.return_value = {"intent": "test_intent"}

    result = engine._analyze_intent("some text")

    engine.intent_analyzer.analyze.assert_called_once_with("some text")
    assert result["intent"] == "test_intent"


def test_analyze_intent_without_analyzer():
    """Test _analyze_intent returns None when the analyzer is missing."""
    engine = NLPEngine()
    engine.intent_analyzer = None

    result = engine._analyze_intent("some text")
    assert result is None


def test_analyze_urgency_with_analyzer():
    """Test _analyze_urgency when the analyzer is available."""
    engine = NLPEngine()
    engine.urgency_analyzer = MagicMock()
    engine.urgency_analyzer.analyze.return_value = {"urgency": "test_urgency"}

    result = engine._analyze_urgency("some text")

    engine.urgency_analyzer.analyze.assert_called_once_with("some text")
    assert result["urgency"] == "test_urgency"


def test_analyze_urgency_without_analyzer():
    """Test _analyze_urgency returns None when the analyzer is missing."""
    engine = NLPEngine()
    engine.urgency_analyzer = None

    result = engine._analyze_urgency("some text")
    assert result is None