"""
Component for analyzing the urgency of an email.

This module contains the `UrgencyModel` class, which is responsible for
assessing the urgency of a given text (e.g., 'critical', 'high', 'low').
It uses a pre-trained machine learning model if available, and falls back to a
regex-based analysis if the model is not present.
"""

import logging
import re
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class UrgencyModel:
    """
    Analyzes email text to determine its urgency level.

    This class orchestrates the urgency analysis process, prioritizing a
    machine learning model and using a regex-based fallback for robustness.

    Attributes:
        model: The pre-trained scikit-learn model for urgency classification.
        logger: A logger for recording events and errors.
    """

    def __init__(self, urgency_model: Optional[Any]):
        """
        Initializes the UrgencyModel.

        Args:
            urgency_model: A pre-trained scikit-learn compatible model for
                           urgency classification, or None if not available.
        """
        self.model = urgency_model
        self.logger = logging.getLogger(__name__)

    def _analyze_model(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Analyzes urgency using the loaded scikit-learn model.

        Args:
            text: The text to be analyzed.

        Returns:
            A dictionary with the predicted urgency and confidence score, or
            None if the model is not available or an error occurs.
        """
        if not self.model:
            return None
        try:
            prediction = self.model.predict([text])[0]
            probabilities = self.model.predict_proba([text])[0]
            confidence = float(max(probabilities))
            return {
                "urgency": str(prediction),
                "confidence": confidence,
                "method_used": "model_urgency",
            }
        except Exception as e:
            self.logger.error(f"Error using urgency model: {e}. Trying fallback.")
            return None

    def _analyze_regex(self, text: str) -> Dict[str, Any]:
        """
        Analyzes urgency using regex pattern matching as a fallback.

        Args:
            text: The text to be analyzed.

        Returns:
            A dictionary with the predicted urgency and a heuristic confidence score.
        """
        text_lower = text.lower()
        if re.search(r"\b(emergency|urgent|asap|immediately|critical)\b", text_lower):
            return {
                "urgency": "critical",
                "confidence": 0.9,
                "method_used": "fallback_regex_urgency",
            }
        elif re.search(r"\b(soon|quickly|priority|important|deadline)\b", text_lower):
            return {"urgency": "high", "confidence": 0.8, "method_used": "fallback_regex_urgency"}
        elif re.search(r"\b(next week|upcoming|scheduled)\b", text_lower):
            return {"urgency": "medium", "confidence": 0.6, "method_used": "fallback_regex_urgency"}
        else:
            return {"urgency": "low", "confidence": 0.5, "method_used": "fallback_regex_urgency"}

    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Assesses the urgency of the email using the best available method.

        It first attempts to use the machine learning model. If the model is
        not available or fails, it falls back to a regex-based analysis.

        Args:
            text: The email text to analyze.

        Returns:
            A dictionary containing the analysis results, including the
            detected urgency and a confidence score.
        """
        if analysis_result := self._analyze_model(text):
            self.logger.info("Urgency analysis performed using ML model.")
            return analysis_result
        self.logger.info("Urgency analysis performed using regex matching.")
        return self._analyze_regex(text)
