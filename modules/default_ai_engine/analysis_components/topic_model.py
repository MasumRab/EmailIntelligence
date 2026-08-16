"""
Component for analyzing the topic of an email.

This module contains the `TopicModel` class, which is responsible for
identifying the main topic of a given text (e.g., 'Work & Business',
'Finance & Banking'). It uses a pre-trained machine learning model if
available, and falls back to a keyword-based analysis if the model is not
present.
"""

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class TopicModel:
    """
    Analyzes email text to determine its main topic.

    This class orchestrates the topic analysis process, prioritizing a
    machine learning model and using a keyword-based fallback for robustness.

    Attributes:
        model: The pre-trained scikit-learn model for topic classification.
        logger: A logger for recording events and errors.
    """

    def __init__(self, topic_model: Optional[Any]):
        """
        Initializes the TopicModel.

        Args:
            topic_model: A pre-trained scikit-learn compatible model for
                         topic classification, or None if not available.
        """
        self.model = topic_model
        self.logger = logging.getLogger(__name__)

    def _analyze_model(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Analyzes the topic using the loaded scikit-learn model.

        Args:
            text: The text to be analyzed.

        Returns:
            A dictionary with the predicted topic and confidence score, or
            None if the model is not available or an error occurs.
        """
        if not self.model:
            return None
        try:
            prediction = self.model.predict([text])[0]
            probabilities = self.model.predict_proba([text])[0]
            confidence = float(max(probabilities))
            return {
                "topic": str(prediction),
                "confidence": confidence,
                "method_used": "model_topic",
            }
        except Exception as e:
            self.logger.error(f"Error using topic model: {e}. Trying fallback.")
            return None

    def _analyze_keyword(self, text: str) -> Dict[str, Any]:
        """
        Analyzes the topic using keyword matching as a fallback.

        Args:
            text: The text to be analyzed.

        Returns:
            A dictionary with the predicted topic and a heuristic confidence score.
        """
        topics = {
            "Work & Business": ["meeting", "project", "deadline", "client"],
            "Finance & Banking": ["payment", "invoice", "statement", "account"],
            "Personal & Family": ["family", "friend", "birthday", "vacation"],
            "Health & Wellness": ["doctor", "medical", "appointment", "prescription"],
            "Travel & Leisure": ["travel", "flight", "hotel", "booking"],
        }
        text_lower = text.lower()
        topic_scores = {
            topic: sum(1 for keyword in keywords if keyword in text_lower)
            for topic, keywords in topics.items()
        }

        if any(topic_scores.values()):
            best_topic = max(topic_scores, key=topic_scores.get)
            confidence = min(topic_scores[best_topic] / 5.0, 0.9)
            return {
                "topic": best_topic,
                "confidence": max(0.1, confidence),
                "method_used": "fallback_keyword_topic",
            }
        else:
            return {
                "topic": "General",
                "confidence": 0.5,
                "method_used": "fallback_keyword_topic",
            }

    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Identifies the main topic of the email using the best available method.

        It first attempts to use the machine learning model. If the model is
        not available or fails, it falls back to a keyword-based analysis.

        Args:
            text: The email text to analyze.

        Returns:
            A dictionary containing the analysis results, including the
            detected topic and a confidence score.
        """
        if analysis_result := self._analyze_model(text):
            self.logger.info("Topic analysis performed using ML model.")
            return analysis_result
        self.logger.info("Topic analysis performed using keyword matching.")
        return self._analyze_keyword(text)
