"""
Component for analyzing the sentiment of an email.

This module provides the `SentimentModel` class, which uses a hierarchical
approach to determine sentiment. It prioritizes a pre-trained machine
learning model, falls back to TextBlob for lexical analysis, and finally uses
a keyword-based approach if other methods are unavailable.
"""

import logging
from typing import Any, Dict, Optional

try:
    from textblob import TextBlob

    HAS_NLTK = True
except ImportError:
    TextBlob = None
    HAS_NLTK = False

logger = logging.getLogger(__name__)


class SentimentModel:
    """
    Analyzes email text to determine its sentiment.

    This class orchestrates the sentiment analysis process, using a
    multi-layered approach for robustness.

    Attributes:
        model: A pre-trained scikit-learn model for sentiment classification.
        has_nltk: A boolean indicating if NLTK and TextBlob are installed.
        logger: A logger for recording events and errors.
    """

    def __init__(self, sentiment_model: Optional[Any], has_nltk_installed: bool):
        """
        Initializes the SentimentModel.

        Args:
            sentiment_model: A pre-trained scikit-learn compatible model for
                             sentiment classification.
            has_nltk_installed: A boolean indicating if NLTK is available.
        """
        self.model = sentiment_model
        self.has_nltk = has_nltk_installed
        self.logger = logging.getLogger(__name__)

    def _analyze_model(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Analyzes sentiment using the loaded scikit-learn model.

        Args:
            text: The text to be analyzed.

        Returns:
            A dictionary with the predicted sentiment and confidence, or None
            if the model is not available or fails.
        """
        if not self.model:
            return None
        try:
            prediction = self.model.predict([text])[0]
            probabilities = self.model.predict_proba([text])[0]
            confidence = float(max(probabilities))
            polarity = (
                confidence
                if prediction == "positive"
                else -confidence
                if prediction == "negative"
                else 0.0
            )
            return {
                "sentiment": str(prediction),
                "polarity": polarity,
                "subjectivity": 0.5,
                "confidence": confidence,
                "method_used": "model_sentiment",
            }
        except Exception as e:
            self.logger.error(f"Error using sentiment model: {e}. Trying fallback.")
            return None

    def _analyze_textblob(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Analyzes sentiment using TextBlob as a fallback.

        Args:
            text: The text to be analyzed.

        Returns:
            A dictionary with the sentiment analysis, or None if TextBlob
            is not available or fails.
        """
        if not self.has_nltk or not TextBlob:
            self.logger.warning(
                "TextBlob analysis skipped: NLTK or TextBlob not available."
            )
            return None
        try:
            blob = TextBlob(text)
            polarity, subjectivity = blob.sentiment
            if polarity > 0.1:
                sentiment, confidence = "positive", min(polarity + 0.5, 1.0)
            elif polarity < -0.1:
                sentiment, confidence = "negative", min(abs(polarity) + 0.5, 1.0)
            else:
                sentiment, confidence = "neutral", 0.7
            return {
                "sentiment": sentiment,
                "polarity": polarity,
                "subjectivity": subjectivity,
                "confidence": confidence,
                "method_used": "fallback_textblob_sentiment",
            }
        except Exception as e:
            self.logger.error(f"Error during TextBlob analysis: {e}")
            return None

    def _analyze_keyword(self, text: str) -> Dict[str, Any]:
        """
        Analyzes sentiment using keyword matching as a final fallback.

        Args:
            text: The text to be analyzed.

        Returns:
            A dictionary with the sentiment analysis based on keywords.
        """
        text_lower = text.lower()
        positive_words = ["good", "great", "excellent", "thank", "happy", "love"]
        negative_words = ["bad", "terrible", "problem", "issue", "error", "hate"]
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)

        if pos_count > neg_count:
            return {
                "sentiment": "positive",
                "polarity": 0.5,
                "subjectivity": 0.5,
                "confidence": 0.6,
                "method_used": "fallback_keyword_sentiment",
            }
        elif neg_count > pos_count:
            return {
                "sentiment": "negative",
                "polarity": -0.5,
                "subjectivity": 0.5,
                "confidence": 0.6,
                "method_used": "fallback_keyword_sentiment",
            }
        else:
            return {
                "sentiment": "neutral",
                "polarity": 0.0,
                "subjectivity": 0.5,
                "confidence": 0.5,
                "method_used": "fallback_keyword_sentiment",
            }

    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Performs sentiment analysis using the best available method.

        It attempts to use the ML model first, then TextBlob, and finally
        a keyword-based approach as a fallback.

        Args:
            text: The email text to analyze.

        Returns:
            A dictionary containing the detailed sentiment analysis.
        """
        if result := self._analyze_model(text):
            self.logger.info("Sentiment analysis performed using ML model.")
            return result
        if result := self._analyze_textblob(text):
            self.logger.info("Sentiment analysis performed using TextBlob.")
            return result
        self.logger.info("Sentiment analysis performed using keyword matching.")
        return self._analyze_keyword(text)
