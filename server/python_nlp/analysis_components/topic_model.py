import logging
import re
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class TopicModel:
    def __init__(self, topic_model: Optional[Any]):
        self.model = topic_model
        self.logger = logging.getLogger(__name__)

    def _analyze_model(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Analyze topic using the loaded sklearn model.
        """
        if not self.model:
            return None

        try:
            prediction = self.model.predict([text])[0]
            probabilities = self.model.predict_proba([text])[0]
            confidence = float(max(probabilities))

            return {
                'topic': str(prediction),
                'confidence': confidence,
                'method_used': 'model_topic'
            }
        except Exception as e:
            self.logger.error(f"Error using topic model: {e}. Trying fallback.")
            return None

    def _analyze_keyword(self, text: str) -> Dict[str, Any]:
        """
        Analyze topic using keyword matching as a fallback method.
        """
        topics = {
            'Work & Business': [
                'meeting', 'conference', 'project', 'deadline', 'client',
                'presentation', 'report', 'proposal'
            ],
            'Finance & Banking': [
                'payment', 'invoice', 'bill', 'statement', 'account',
                'credit', 'debit', 'transfer', 'money', 'financial'
            ],
            'Personal & Family': [
                'family', 'personal', 'friend', 'birthday', 'anniversary',
                'vacation', 'holiday', 'weekend', 'dinner', 'lunch'
            ],
            'Health & Wellness': [
                'doctor', 'medical', 'health', 'hospital', 'clinic',
                'appointment', 'prescription', 'medicine', 'treatment', 'therapy'
            ],
            'Travel & Leisure': [
                'travel', 'flight', 'hotel', 'booking', 'reservation',
                'trip', 'vacation', 'destination', 'airport', 'airline'
            ]
        }

        topic_scores = {}
        text_lower = text.lower()
        for topic, keywords in topics.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            topic_scores[topic] = score

        if any(score > 0 for score in topic_scores.values()):
            best_topic = max(topic_scores, key=topic_scores.get)
            confidence = min(topic_scores[best_topic] / 5.0, 0.9) # Heuristic

            return {
                'topic': best_topic,
                'confidence': max(0.1, confidence),
                'method_used': 'fallback_keyword_topic'
            }
        else:
            return {
                'topic': 'General',
                'confidence': 0.5,
                'method_used': 'fallback_keyword_topic'
            }

    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Identify the main topic of the email using available methods.
        """
        # Try model-based analysis first
        analysis_result = self._analyze_model(text)
        if analysis_result:
            self.logger.info("Topic analysis performed using ML model.")
            return analysis_result

        # Use keyword matching as fallback
        self.logger.info("Topic analysis performed using keyword matching.")
        return self._analyze_keyword(text)
