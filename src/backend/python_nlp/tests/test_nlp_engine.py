from unittest.mock import MagicMock, patch

import pytest

from backend.python_nlp.nlp_engine import NLPEngine

# Ensure the root directory is in the Python path


@pytest.fixture
def nlp_engine_with_mocks():
    """
    Fixture for NLPEngine with mocked sub-analyzers and internal methods.
    This allows testing the orchestration logic of NLPEngine's analyze_email method.
    """
    # Patch all external dependencies and methods that perform heavy lifting or I/O
    with (
        patch("joblib.load", MagicMock(return_value=MagicMock())),
        patch("backend.python_nlp.nlp_engine.HAS_NLTK", True),
        patch("backend.python_nlp.nlp_engine.HAS_SKLEARN_AND_JOBLIB", True),
        patch(
            "backend.python_nlp.nlp_engine.NLPEngine._analyze_sentiment",
            MagicMock(
                return_value={
                    "sentiment": "neutral",
                    "confidence": 0.9,
                    "method_used": "mock",
                }
            ),
        ) as mock_sentiment,
        patch(
            "backend.python_nlp.nlp_engine.NLPEngine._analyze_topic",
            MagicMock(
                return_value={
                    "topic": "general",
                    "confidence": 0.9,
                    "method_used": "mock",
                }
            ),
        ) as mock_topic,
        patch(
            "backend.python_nlp.nlp_engine.NLPEngine._analyze_intent",
            MagicMock(
                return_value={
                    "intent": "informational",
                    "confidence": 0.9,
                    "method_used": "mock",
                }
            ),
        ) as mock_intent,
        patch(
            "backend.python_nlp.nlp_engine.NLPEngine._analyze_urgency",
            MagicMock(
                return_value={
                    "urgency": "low",
                    "confidence": 0.9,
                    "method_used": "mock",
                }
            ),
        ) as mock_urgency,
        patch(
            "backend.python_nlp.nlp_engine.NLPEngine._extract_keywords",
            MagicMock(return_value=["mock_keyword"]),
        ) as mock_keywords,
        patch(
            "backend.python_nlp.nlp_engine.NLPEngine._categorize_content",
            MagicMock(return_value=["Mock Category"]),
        ) as mock_categorize,
    ):
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
        "topic",
        "sentiment",
        "intent",
        "urgency",
        "confidence",
        "categories",
        "keywords",
        "reasoning",
        "suggested_labels",
        "risk_flags",
        "validation",
        "details",
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
    with patch("backend.python_nlp.nlp_engine.HAS_NLTK", True):
        engine = NLPEngine()
        # Mock the internal analysis methods to control the fallback flow
        with (
            patch.object(
                engine, "_analyze_sentiment_model", return_value=None
            ) as mock_model,
            patch.object(
                engine, "_analyze_sentiment_textblob", return_value=None
            ) as mock_textblob,
            patch.object(
                engine,
                "_analyze_sentiment_keyword",
                return_value={"method_used": "fallback_keyword_sentiment"},
            ) as mock_keyword,
        ):
            result = engine._analyze_sentiment("A test sentence.")

            # Assert that the methods were called in the correct order
            mock_model.assert_called_once()
            mock_textblob.assert_called_once()
            mock_keyword.assert_called_once()

            # Assert that the final result is from the last fallback
            assert result["method_used"] == "fallback_keyword_sentiment"


@patch("backend.python_nlp.nlp_engine.NLPEngine._load_model", return_value=None)
def test_analyze_email_success_path(mock_load_model):
    """
    Test the successful, standard analysis flow of the analyze_email method.
    """
    with (
        patch("backend.python_nlp.nlp_engine.HAS_SKLEARN_AND_JOBLIB", True),
        patch("backend.python_nlp.nlp_engine.HAS_NLTK", True),
        patch(
            "backend.python_nlp.nlp_engine.NLPEngine._categorize_content",
            return_value=["Work & Business"],
        ),
        patch(
            "backend.python_nlp.nlp_engine.NLPEngine._extract_keywords",
            return_value=["project", "deadline"],
        ),
        patch(
            "backend.python_nlp.nlp_engine.NLPEngine._analyze_sentiment"
        ) as mock_sentiment,
        patch("backend.python_nlp.nlp_engine.NLPEngine._analyze_topic") as mock_topic,
        patch("backend.python_nlp.nlp_engine.NLPEngine._analyze_intent") as mock_intent,
        patch(
            "backend.python_nlp.nlp_engine.NLPEngine._analyze_urgency"
        ) as mock_urgency,
    ):
        mock_sentiment.return_value = {
            "sentiment": "positive",
            "confidence": 0.9,
            "method_used": "model_sentiment",
        }
        mock_topic.return_value = {
            "topic": "work_business",
            "confidence": 0.85,
            "method_used": "model_topic",
        }
        mock_intent.return_value = {
            "intent": "follow_up",
            "confidence": 0.95,
            "method_used": "model_intent",
        }
        mock_urgency.return_value = {
            "urgency": "high",
            "confidence": 0.7,
            "method_used": "model_urgency",
        }

        engine = NLPEngine()
        subject = "Project Update"
        content = "What is the status of the new project? We need to meet the deadline."
        result = engine.analyze_email(subject, content)

        assert result["sentiment"] == "positive"
        assert result["topic"] == "work_business"
        assert result["intent"] == "follow_up"
        assert result["urgency"] == "high"
        assert "work" in result["reasoning"].lower()
        assert "positive" in result["reasoning"].lower()
        assert "high" in result["reasoning"].lower()
        assert "High Priority" in result["suggested_labels"]


@patch("backend.python_nlp.nlp_engine.NLPEngine._load_model", return_value=None)
def test_analyze_email_full_fallback_on_exception(mock_load_model):
    """
    Test that a generic exception during analysis triggers the full fallback.
    """
    with (
        patch("backend.python_nlp.nlp_engine.HAS_SKLEARN_AND_JOBLIB", True),
        patch("backend.python_nlp.nlp_engine.HAS_NLTK", True),
        patch.object(
            NLPEngine, "_preprocess_text", side_effect=Exception("Unexpected error")
        ) as mock_preprocess,
    ):
        engine = NLPEngine()
        result = engine.analyze_email("Test", "Test")

        mock_preprocess.assert_called_once()
        assert result["topic"] == "General"
        assert result["sentiment"] == "neutral"
        assert result["risk_flags"] == ["analysis_failed"]
        assert "Unexpected error" in result["reasoning"]
        assert result["validation"]["method"] == "fallback"


def test_analyze_topic_model_path():
    """Test _analyze_topic uses the model path when available."""
    with (
        patch(
            "backend.python_nlp.nlp_engine.NLPEngine._analyze_topic_model"
        ) as mock_model,
        patch(
            "backend.python_nlp.nlp_engine.NLPEngine._analyze_topic_keyword"
        ) as mock_fallback,
    ):
        mock_model.return_value = {"topic": "model_topic", "confidence": 0.9}
        engine = NLPEngine()
        result = engine._analyze_topic("some text")
        mock_model.assert_called_once_with("some text")
        mock_fallback.assert_not_called()
        assert result["topic"] == "model_topic"


def test_analyze_topic_fallback_path():
    """Test _analyze_topic uses the fallback path when the model is unavailable."""
    with (
        patch(
            "backend.python_nlp.nlp_engine.NLPEngine._analyze_topic_model"
        ) as mock_model,
        patch(
            "backend.python_nlp.nlp_engine.NLPEngine._analyze_topic_keyword"
        ) as mock_fallback,
    ):
        mock_model.return_value = None
        mock_fallback.return_value = {"topic": "fallback_topic", "confidence": 0.5}
        engine = NLPEngine()
        result = engine._analyze_topic("some text")
        mock_model.assert_called_once_with("some text")
        mock_fallback.assert_called_once_with("some text")
        assert result["topic"] == "fallback_topic"


def test_analyze_intent_model_path():
    """Test _analyze_intent uses the model path when available."""
    with (
        patch(
            "backend.python_nlp.nlp_engine.NLPEngine._analyze_intent_model"
        ) as mock_model,
        patch(
            "backend.python_nlp.nlp_engine.NLPEngine._analyze_intent_regex"
        ) as mock_fallback,
    ):
        mock_model.return_value = {"intent": "model_intent", "confidence": 0.9}
        engine = NLPEngine()
        result = engine._analyze_intent("some text")
        mock_model.assert_called_once_with("some text")
        mock_fallback.assert_not_called()
        assert result["intent"] == "model_intent"


def test_analyze_intent_fallback_path():
    """Test _analyze_intent uses the fallback path when the model is unavailable."""
    with (
        patch(
            "backend.python_nlp.nlp_engine.NLPEngine._analyze_intent_model"
        ) as mock_model,
        patch(
            "backend.python_nlp.nlp_engine.NLPEngine._analyze_intent_regex"
        ) as mock_fallback,
    ):
        mock_model.return_value = None
        mock_fallback.return_value = {"intent": "fallback_intent", "confidence": 0.5}
        engine = NLPEngine()
        result = engine._analyze_intent("some text")
        mock_model.assert_called_once_with("some text")
        mock_fallback.assert_called_once_with("some text")
        assert result["intent"] == "fallback_intent"


def test_analyze_urgency_model_path():
    """Test _analyze_urgency uses the model path when available."""
    with (
        patch(
            "backend.python_nlp.nlp_engine.NLPEngine._analyze_urgency_model"
        ) as mock_model,
        patch(
            "backend.python_nlp.nlp_engine.NLPEngine._analyze_urgency_regex"
        ) as mock_fallback,
    ):
        mock_model.return_value = {"urgency": "model_urgency", "confidence": 0.9}
        engine = NLPEngine()
        result = engine._analyze_urgency("some text")
        mock_model.assert_called_once_with("some text")
        mock_fallback.assert_not_called()
        assert result["urgency"] == "model_urgency"


def test_analyze_urgency_fallback_path():
    """Test _analyze_urgency uses the fallback path when the model is unavailable."""
    with (
        patch(
            "backend.python_nlp.nlp_engine.NLPEngine._analyze_urgency_model"
        ) as mock_model,
        patch(
            "backend.python_nlp.nlp_engine.NLPEngine._analyze_urgency_regex"
        ) as mock_fallback,
    ):
        mock_model.return_value = None
        mock_fallback.return_value = {"urgency": "fallback_urgency", "confidence": 0.5}
        engine = NLPEngine()
        result = engine._analyze_urgency("some text")
        mock_model.assert_called_once_with("some text")
        mock_fallback.assert_called_once_with("some text")
        assert result["urgency"] == "fallback_urgency"
