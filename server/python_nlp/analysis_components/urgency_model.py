import logging
import re
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class UrgencyModel:
    def __init__(self, urgency_model: Optional[Any]):
        self.model = urgency_model
        self.logger = logging.getLogger(__name__)

    def _analyze_model(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Analyze urgency using the loaded sklearn model.
        """
        if not self.model:
            return None

        try:
            prediction = self.model.predict([text])[0]
            probabilities = self.model.predict_proba([text])[0]
            confidence = float(max(probabilities))

            return {
                'urgency': str(prediction),
                'confidence': confidence,
                'method_used': 'model_urgency'
            }
        except Exception as e:
            self.logger.error(f"Error using urgency model: {e}. Trying fallback.")
            return None

    def _analyze_regex(self, text: str) -> Dict[str, Any]:
        """
        Analyze urgency using regex pattern matching as a fallback method.
        """
        text_lower = text.lower()

        if re.search(r'\b(emergency|urgent|asap|immediately|critical|crisis|disaster)\b', text_lower):
            urgency_label = 'critical'
            confidence = 0.9
        elif re.search(r'\b(soon|quickly|priority|important|deadline|time-sensitive)\b', text_lower):
            urgency_label = 'high'
            confidence = 0.8
        elif re.search(r'\b(when you can|next week|upcoming|planned|scheduled)\b', text_lower):
            urgency_label = 'medium'
            confidence = 0.6
        else:
            urgency_label = 'low'
            confidence = 0.5

        return {
            'urgency': urgency_label,
            'confidence': confidence,
            'method_used': 'fallback_regex_urgency'
        }

    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Assess the urgency level of the email using available methods.
        """
        # Try model-based analysis first
        analysis_result = self._analyze_model(text)
        if analysis_result:
            self.logger.info("Urgency analysis performed using ML model.")
            return analysis_result

        # Use regex matching as fallback
        self.logger.info("Urgency analysis performed using regex matching.")
        return self._analyze_regex(text)
