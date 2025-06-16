import logging
import re
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class IntentAnalyzer:
    def __init__(self, intent_model: Optional[Any]):
        self.model = intent_model
        self.logger = logging.getLogger(__name__)

    def _analyze_model(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Analyze intent using the loaded sklearn model.
        """
        if not self.model:
            return None

        try:
            prediction = self.model.predict([text])[0]
            probabilities = self.model.predict_proba([text])[0]
            confidence = float(max(probabilities))

            return {
                'intent': str(prediction),
                'confidence': confidence,
                'method_used': 'model_intent'
            }
        except Exception as e:
            self.logger.error(f"Error using intent model: {e}. Trying fallback.")
            return None

    def _analyze_regex(self, text: str) -> Dict[str, Any]:
        """
        Analyze intent using regex pattern matching as a fallback method.
        """
        intent_patterns = {
            'request': r'\b(please|could you|would you|can you|need|require|request)\b',
            'inquiry': r'\b(question|ask|wonder|curious|information|details|clarification)\b',
            'scheduling': r'\b(schedule|calendar|meeting|appointment|time|date|available)\b',
            'urgent_action': r'\b(urgent|asap|immediately|emergency|critical|priority)\b',
            'gratitude': r'\b(thank|thanks|grateful|appreciate)\b',
            'complaint': r'\b(complaint|complain|issue|problem|dissatisfied|unhappy)\b',
            'follow_up': r'\b(follow up|follow-up|checking in|status|update|progress)\b',
            'confirmation': r'\b(confirm|confirmation|verify|check|acknowledge)\b'
        }

        intent_scores = {}
        text_lower = text.lower()
        for intent, pattern in intent_patterns.items():
            matches = re.findall(pattern, text_lower)
            intent_scores[intent] = len(matches)

        if any(score > 0 for score in intent_scores.values()):
            best_intent = max(intent_scores, key=intent_scores.get)
            confidence = min(intent_scores[best_intent] / 3.0, 0.9) # Heuristic

            return {
                'intent': best_intent,
                'confidence': max(0.1, confidence),
                'method_used': 'fallback_regex_intent'
            }
        else:
            return {
                'intent': 'informational',
                'confidence': 0.6,
                'method_used': 'fallback_regex_intent'
            }

    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Determine the intent of the email using available methods.
        """
        # Try model-based analysis first
        analysis_result = self._analyze_model(text)
        if analysis_result:
            self.logger.info("Intent analysis performed using ML model.")
            return analysis_result

        # Use regex matching as fallback
        self.logger.info("Intent analysis performed using regex matching.")
        return self._analyze_regex(text)
