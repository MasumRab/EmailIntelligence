import logging
from typing import Any, Dict, Optional

# Try to import optional dependencies
try:
    import nltk  # Used by TextBlob and for stopwords
    from textblob import TextBlob

    # nltk.download('punkt') # Required for TextBlob
    # nltk.download('stopwords') # Required for keyword extraction in NLPEngine
    HAS_NLTK = True
except ImportError:
    HAS_NLTK = False

logger = logging.getLogger(__name__)


class SentimentModel:
    def __init__(self, sentiment_model: Optional[Any], has_nltk_installed: bool):
        self.model = sentiment_model
        self.has_nltk = has_nltk_installed
        self.logger = logging.getLogger(__name__)

    def _analyze_model(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Analyze sentiment using the loaded sklearn model.
        """
        if not self.model:
            return None

        try:
            prediction = self.model.predict([text])[0]
            probabilities = self.model.predict_proba([text])[0]
            confidence = max(probabilities)

            polarity = 0.0
            if prediction == "positive":
                polarity = confidence
            elif prediction == "negative":
                polarity = -confidence

            return {
                "sentiment": str(prediction),
                "polarity": polarity,
                "subjectivity": 0.5,  # Default subjectivity, model might not provide this
                "confidence": float(confidence),
                "method_used": "model_sentiment",
            }
        except Exception as e:
            self.logger.error(f"Error using sentiment model: {e}. Trying fallback.")
            return None

    def _analyze_textblob(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Analyze sentiment using TextBlob as a fallback method.
        """
        if not self.has_nltk:  # TextBlob relies on NLTK
            self.logger.warning("TextBlob analysis skipped: NLTK not available.")
            return None

        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity

            if polarity > 0.1:
                sentiment_label = "positive"
                confidence = min(polarity + 0.5, 1.0)
            elif polarity < -0.1:
                sentiment_label = "negative"
                confidence = min(abs(polarity) + 0.5, 1.0)
            else:
                sentiment_label = "neutral"
                confidence = 0.7  # Default confidence for TextBlob neutral

            return {
                "sentiment": sentiment_label,
                "polarity": polarity,
                "subjectivity": subjectivity,
                "confidence": confidence,
                "method_used": "fallback_textblob_sentiment",
            }
        except Exception as e:
            self.logger.error(f"Error during TextBlob sentiment analysis: {e}")
            return None

    def _analyze_keyword(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment using keyword matching as a final fallback method.
        """
        text_lower = text.lower()

        positive_words = [
            "good",
            "great",
            "excellent",
            "thank",
            "please",
            "welcome",
            "happy",
            "love",
        ]
        negative_words = [
            "bad",
            "terrible",
            "problem",
            "issue",
            "error",
            "failed",
            "hate",
            "angry",
        ]

        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)

        if positive_count > negative_count:
            sentiment_label = "positive"
            polarity = 0.5
            confidence = 0.6
        elif negative_count > positive_count:
            sentiment_label = "negative"
            polarity = -0.5
            confidence = 0.6
        else:
            sentiment_label = "neutral"
            polarity = 0.0
            confidence = 0.5  # Lower confidence for keyword-based neutral

        return {
            "sentiment": sentiment_label,
            "polarity": polarity,
            "subjectivity": 0.5,  # Default subjectivity for keyword method
            "confidence": confidence,
            "method_used": "fallback_keyword_sentiment",
        }

    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Perform sentiment analysis using available methods in order of preference.
        """
        # Try model-based analysis first
        analysis_result = self._analyze_model(text)
        if analysis_result:
            self.logger.info("Sentiment analysis performed using ML model.")
            return analysis_result

        # Try TextBlob analysis if model fails or not available
        analysis_result = self._analyze_textblob(text)
        if analysis_result:
            self.logger.info("Sentiment analysis performed using TextBlob.")
            return analysis_result

        # Use keyword matching as final fallback
        self.logger.info("Sentiment analysis performed using keyword matching.")
        return self._analyze_keyword(text)
