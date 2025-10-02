from unittest.mock import patch, MagicMock
import plotly.graph_objects as go
from backend.python_backend.gradio_app import (
    analyze_email_interface,
    create_sentiment_chart,
    create_topic_chart
)

def test_analyze_email_interface_success():
    """
    Test the successful analysis path of the Gradio interface function.
    """
    mock_analysis = {
        "topic": "work",
        "sentiment": "positive",
        "intent": "question",
        "urgency": "high",
        "reasoning": "This is a test.",
        "details": {
            "sentiment_analysis": {"polarity": 0.8},
            "topic_analysis": {"topic": "work", "confidence": 0.9}
        }
    }
    with patch("backend.python_backend.gradio_app.nlp_engine") as mock_engine:
        mock_engine.analyze_email.return_value = mock_analysis

        full_json, topic, sentiment, intent, urgency, reasoning, sentiment_chart, topic_chart = analyze_email_interface("Subject", "Content")

        mock_engine.analyze_email.assert_called_once_with("Subject", "Content")
        assert topic == "work"
        assert sentiment == "positive"
        assert intent == "question"
        assert urgency == "high"
        assert reasoning == "This is a test."
        assert isinstance(sentiment_chart, go.Figure)
        assert isinstance(topic_chart, go.Figure)
        assert full_json == mock_analysis

def test_analyze_email_interface_empty_input():
    """
    Test the interface function's handling of empty subject and content.
    """
    with patch("backend.python_backend.gradio_app.nlp_engine") as mock_engine:
        result = analyze_email_interface("", "")

        mock_engine.analyze_email.assert_not_called()
        assert "error" in result[0]
        assert "cannot both be empty" in result[0]["error"]

def test_analyze_email_interface_exception():
    """
    Test the interface function's exception handling.
    """
    with patch("backend.python_backend.gradio_app.nlp_engine") as mock_engine:
        mock_engine.analyze_email.side_effect = Exception("Test Exception")

        result = analyze_email_interface("Subject", "Content")

        assert "error" in result[0]
        assert "Test Exception" in result[0]["error"]

def test_create_sentiment_chart():
    """
    Test the creation of the sentiment chart.
    """
    mock_analysis = {
        "sentiment": "positive",
        "details": {"sentiment_analysis": {"polarity": 0.8}}
    }
    fig = create_sentiment_chart(mock_analysis)
    assert isinstance(fig, go.Figure)
    assert fig.layout.title.text == 'Sentiment Polarity'

def test_create_topic_chart():
    """
    Test the creation of the topic chart.
    """
    mock_analysis = {
        "details": {"topic_analysis": {"topic": "work_business", "confidence": 0.9}}
    }
    fig = create_topic_chart(mock_analysis)
    assert isinstance(fig, go.Figure)
    assert fig.layout.title.text == 'Topic Confidence'