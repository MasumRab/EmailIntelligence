"""
A simple, placeholder sentiment analysis model.
"""
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class SentimentModel:
    """A basic sentiment model for demonstration purposes."""

    def __init__(self, sentiment_model=None, has_nltk_installed=False):
        logger.info("SentimentModel instance created.")
        self.model = sentiment_model
        self.has_nltk = has_nltk_installed

    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Performs a very basic sentiment analysis.
        """
        logger.info(f"Analyzing sentiment for: '{text[:30]}...'")
        text_lower = text.lower()
        if "bad" in text_lower or "error" in text_lower:
            sentiment = "negative"
        elif "good" in text_lower or "great" in text_lower:
            sentiment = "positive"
        else:
            sentiment = "neutral"

        return {
            "sentiment": sentiment,
            "confidence": 0.5,  # Placeholder confidence
            "method_used": "simple_keyword_sentiment",
        }
