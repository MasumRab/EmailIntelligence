import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Ensure the root directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from backend.python_nlp.nlp_engine import NLPEngine

@pytest.fixture
def nlp_engine_with_mocks():
    """
    Fixture for NLPEngine with mocked sub-analyzers and internal methods.
    This allows testing the orchestration logic of NLPEngine's analyze_email method.
    """
    # Patch all external dependencies and methods that perform heavy lifting or I/O
    with patch('backend.python_nlp.nlp_engine.joblib.load', MagicMock(return_value=MagicMock())), \
         patch('backend.python_nlp.nlp_engine.HAS_NLTK', True), \
         patch('backend.python_nlp.nlp_engine.HAS_SKLEARN_AND_JOBLIB', True), \
         patch('backend.python_nlp.nlp_engine.NLPEngine._analyze_sentiment', MagicMock(return_value={'sentiment': 'neutral', 'confidence': 0.9, 'method_used': 'mock'})) as mock_sentiment, \
         patch('backend.python_nlp.nlp_engine.NLPEngine._analyze_topic', MagicMock(return_value={'topic': 'general', 'confidence': 0.9, 'method_used': 'mock'})) as mock_topic, \
         patch('backend.python_nlp.nlp_engine.NLPEngine._analyze_intent', MagicMock(return_value={'intent': 'informational', 'confidence': 0.9, 'method_used': 'mock'})) as mock_intent, \
         patch('backend.python_nlp.nlp_engine.NLPEngine._analyze_urgency', MagicMock(return_value={'urgency': 'low', 'confidence': 0.9, 'method_used': 'mock'})) as mock_urgency, \
         patch('backend.python_nlp.nlp_engine.NLPEngine._extract_keywords', MagicMock(return_value=["mock_keyword"])) as mock_keywords, \
         patch('backend.python_nlp.nlp_engine.NLPEngine._categorize_content', MagicMock(return_value=["Mock Category"])) as mock_categorize:

        # Instantiate the engine within the patch context
        engine = NLPEngine()

        # Attach mocks to the instance for easy access in tests
        engine._analyze_sentiment = mock_sentiment
        engine._analyze_topic = mock_topic
        engine._analyze_intent = mock_intent
        engine._analyze_urgency = mock_urgency
        engine._extract_keywords = mock_keywords
        engine._categorize_content = mock_categorize

        yield engine

def test_analyze_email_orchestration(nlp_engine_with_mocks):
    """
    Test that analyze_email correctly orchestrates calls to its sub-components.
    """
    subject = "Test Subject"
    content = "This is a test email."

    result = nlp_engine_with_mocks.analyze_email(subject, content)

    # Verify that all mocked components were called once
    nlp_engine_with_mocks._analyze_sentiment.assert_called_once()
    nlp_engine_with_mocks._analyze_topic.assert_called_once()
    nlp_engine_with_mocks._analyze_intent.assert_called_once()
    nlp_engine_with_mocks._analyze_urgency.assert_called_once()
    nlp_engine_with_mocks._extract_keywords.assert_called_once()
    nlp_engine_with_mocks._categorize_content.assert_called_once()

    # Verify the structure of the final response
    assert isinstance(result, dict)
    expected_keys = [
        "topic", "sentiment", "intent", "urgency", "confidence",
        "categories", "keywords", "reasoning", "suggested_labels",
        "risk_flags", "validation", "details"
    ]
    for key in expected_keys:
        assert key in result, f"Expected key '{key}' not found in analysis result."

    # Verify that the 'details' key contains the results from the mocked analyzers
    assert "sentiment_analysis" in result["details"]
    assert result["details"]["sentiment_analysis"]["sentiment"] == "neutral"
    assert "topic_analysis" in result["details"]
    assert result["details"]["topic_analysis"]["topic"] == "general"

    # Verify that results from other mocked methods are in the main payload
    assert result["keywords"] == ["mock_keyword"]
    assert result["categories"] == ["Mock Category"]

def test_sentiment_analysis_fallback_logic():
    """
    Test the internal fallback logic of the _analyze_sentiment method directly.
    """
    with patch('backend.python_nlp.nlp_engine.HAS_NLTK', True):
        engine = NLPEngine()
        # Mock the internal analysis methods to control the fallback flow
        with patch.object(engine, '_analyze_sentiment_model', return_value=None) as mock_model, \
             patch.object(engine, '_analyze_sentiment_textblob', return_value=None) as mock_textblob, \
             patch.object(engine, '_analyze_sentiment_keyword', return_value={'method_used': 'fallback_keyword_sentiment'}) as mock_keyword:

            result = engine._analyze_sentiment("A test sentence.")

            # Assert that the methods were called in the correct order
            mock_model.assert_called_once()
            mock_textblob.assert_called_once()
            mock_keyword.assert_called_once()

            # Assert that the final result is from the last fallback
            assert result['method_used'] == 'fallback_keyword_sentiment'