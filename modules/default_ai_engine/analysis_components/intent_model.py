"""
Component for analyzing the intent of an email.

This module contains the `IntentModel` class, which is responsible for
determining the intent of a given text (e.g., 'request', 'inquiry',
'complaint'). It uses a pre-trained machine learning model if available,
and falls back to a regex-based analysis if the model is not present.
"""

import logging
import re
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class IntentModel:
    """
    Analyzes email text to determine its intent.

    This class orchestrates the intent analysis process, prioritizing a
    machine learning model and using a regex-based fallback for robustness.

    Attributes:
        model: The pre-trained scikit-learn model for intent classification.
        logger: A logger for recording events and errors.
    """

    def __init__(self, intent_model: Optional[Any]):
        """
        Initializes the IntentModel.

        Args:
            intent_model: A pre-trained scikit-learn compatible model for
                          intent classification, or None if not available.
        """
        self.model = intent_model
        self.logger = logging.getLogger(__name__)

    def _analyze_model(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Analyzes intent using the loaded scikit-learn model.

        Args:
            text: The text to be analyzed.

        Returns:
            A dictionary with the predicted intent and confidence score, or
            None if the model is not available or an error occurs.
        """
        if not self.model:
            return None
        try:
            prediction = self.model.predict([text])[0]
            probabilities = self.model.predict_proba([text])[0]
            confidence = float(max(probabilities))
            return {
                "intent": str(prediction),
                "confidence": confidence,
                "method_used": "model_intent",
            }
        except Exception as e:
            self.logger.error(f"Error using intent model: {e}. Trying fallback.")
            return None

    def _analyze_regex(self, text: str) -> Dict[str, Any]:
        """
        Analyzes intent using regex pattern matching as a fallback.

        Args:
            text: The text to be analyzed.

        Returns:
            A dictionary with the predicted intent and a heuristic confidence score.
        """
        intent_patterns = {
            "request": r"\b(please|could you|would you|can you|need|require|request)\b",
            "inquiry": r"\b(question|ask|wonder|curious|information|details|clarification)\b",
            "scheduling": r"\b(schedule|calendar|meeting|appointment|time|date|available)\b",
            "urgent_action": r"\b(urgent|asap|immediately|emergency|critical|priority)\b",
            "gratitude": r"\b(thank|thanks|grateful|appreciate)\b",
            "complaint": r"\b(complaint|complain|issue|problem|dissatisfied|unhappy)\b",
            "follow_up": r"\b(follow up|follow-up|checking in|status|update|progress)\b",
            "confirmation": r"\b(confirm|confirmation|verify|check|acknowledge)\b",
        }
        text_lower = text.lower()
        intent_scores = {
            intent: len(re.findall(pattern, text_lower))
            for intent, pattern in intent_patterns.items()
        }

        if any(intent_scores.values()):
            best_intent = max(intent_scores, key=intent_scores.get)
            confidence = min(intent_scores[best_intent] / 3.0, 0.9)
            return {
                "intent": best_intent,
                "confidence": max(0.1, confidence),
                "method_used": "fallback_regex_intent",
            }
        else:
            return {
                "intent": "informational",
                "confidence": 0.6,
                "method_used": "fallback_regex_intent",
            }

    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Determines the intent of the email using the best available method.

        It first attempts to use the machine learning model. If the model is
        not available or fails, it falls back to a regex-based analysis.

        Args:
            text: The email text to analyze.

        Returns:
            A dictionary containing the analysis results, including the
            detected intent and a confidence score.
        """
        if analysis_result := self._analyze_model(text):
            self.logger.info("Intent analysis performed using ML model.")
            return analysis_result
        self.logger.info(
            "Intent analysis performed using regex matching as a fallback."
        )
        return self._analyze_regex(text)
