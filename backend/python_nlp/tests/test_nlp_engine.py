import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Ensure the root directory is in the Python path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.python_nlp.nlp_engine import NLPEngine


@pytest.fixture
def nlp_engine_with_mocks():
    """
    Fixture for NLPEngine with mocked sub-analyzers and internal methods.
    """
    with (
        patch("backend.python_nlp.nlp_engine.pipeline", MagicMock(return_value=MagicMock())),
        patch("backend.python_nlp.nlp_engine.HAS_NLTK", True),
        patch(
            "backend.python_nlp.nlp_engine.NLPEngine._analyze_sentiment",
            MagicMock(return_value={"sentiment": "neutral", "confidence": 0.9, "method_used": "mock"}),
        ) as mock_sentiment,
        patch(
            "backend.python_nlp.nlp_engine.NLPEngine._analyze_topic",
            MagicMock(return_value={"topic": "general", "confidence": 0.9, "method_used": "mock"}),
        ) as mock_topic,
        patch(
            "backend.python_nlp.nlp_engine.NLPEngine._analyze_intent",
            MagicMock(return_value={"intent": "informational", "confidence": 0.9, "method_used": "mock"}),
        ) as mock_intent,
        patch(
            "backend.python_nlp.nlp_engine.NLPEngine._analyze_urgency",
            MagicMock(return_value={"urgency": "low", "confidence": 0.9, "method_used": "mock"}),
        ) as mock_urgency,
        patch(
            "backend.python_nlp.nlp_engine.NLPEngine._extract_keywords",
            MagicMock(return_value=["mock_keyword"]),
        ) as mock_keywords,
    ):
        engine = NLPEngine()
        engine._analyze_sentiment = mock_sentiment
        engine._analyze_topic = mock_topic
        engine._analyze_intent = mock_intent
        engine._analyze_urgency = mock_urgency
        engine._extract_keywords = mock_keywords
        yield engine


def test_analyze_email_orchestration(nlp_engine_with_mocks):
    """
    Test that analyze_email correctly orchestrates calls to its sub-components.
    """
    subject = "Test Subject"
    content = "This is a test email."

    result = nlp_engine_with_mocks.analyze_email(subject, content)

    nlp_engine_with_mocks._analyze_sentiment.assert_called_once()
    nlp_engine_with_mocks._analyze_topic.assert_called_once()
    nlp_engine_with_mocks._analyze_intent.assert_called_once()
    nlp_engine_with_mocks._analyze_urgency.assert_called_once()
    nlp_engine_with_mocks._extract_keywords.assert_called_once()

    assert isinstance(result, dict)
    expected_keys = ["topic", "sentiment", "intent", "urgency", "confidence", "keywords", "reasoning"]
    for key in expected_keys:
        assert key in result, f"Expected key '{key}' not found."

    assert result["keywords"] == ["mock_keyword"]
