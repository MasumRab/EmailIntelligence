#!/usr/bin/env python3
"""
An enhanced NLP engine for comprehensive email analysis.
"""

import argparse
import json
import logging
import os
import re
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

from .analysis_components.intent_model import IntentModel
from .analysis_components.sentiment_model import SentimentModel
from .analysis_components.topic_model import TopicModel
from .analysis_components.urgency_model import UrgencyModel
from .text_utils import clean_text

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

try:
    import joblib
    import nltk
    from textblob import TextBlob

    HAS_NLTK = True
    HAS_SKLEARN_AND_JOBLIB = True
except ImportError:
    HAS_NLTK = False
    HAS_SKLEARN_AND_JOBLIB = False
    print(
        "Warning: NLTK, scikit-learn or joblib not available. Advanced NLP features will be disabled.",
        file=sys.stderr,
    )


class NLPEngine:
    """
    Orchestrates NLP tasks for email analysis.
    """

    CATEGORY_PATTERNS = {
        "Work & Business": [
            r"\b(meeting|conference|project|deadline|client|presentation|report|proposal|budget|team|colleague|office|work|business|professional|corporate|company|organization)\b",
            r"\b(employee|staff|manager|supervisor|director|executive|department|division|quarterly|annual|monthly|weekly|daily)\b",
        ],
        "Finance & Banking": [
            r"\b(bank|payment|transaction|invoice|bill|statement|account|credit|debit|transfer|money|financial|insurance|investment|loan|mortgage)\b",
            r"\$[\d,]+|\b\d+\s?(dollars?|USD|EUR|GBP)\b",
            r"\b(tax|taxes|irs|refund|audit|accountant|bookkeeping|overdraft|bankruptcy)\b",
        ],
    }

    def __init__(self):
        """Initializes the NLP engine and loads all necessary models and resources."""
        model_dir = os.getenv("NLP_MODEL_DIR", os.path.dirname(__file__))
        self.sentiment_model_path = os.path.join(model_dir, "sentiment_model.pkl")
        self.topic_model_path = os.path.join(model_dir, "topic_model.pkl")
        self.intent_model_path = os.path.join(model_dir, "intent_model.pkl")
        self.urgency_model_path = os.path.join(model_dir, "urgency_model.pkl")
        self.compiled_patterns = {}

        if HAS_NLTK:
            try:
                nltk.data.find("corpora/stopwords")
                self.stop_words = set(nltk.corpus.stopwords.words("english"))
            except LookupError:
                logger.info("Downloading NLTK 'stopwords' resource...")
                try:
                    nltk.download("stopwords", quiet=True)
                    self.stop_words = set(nltk.corpus.stopwords.words("english"))
                except Exception as e:
                    logger.error(f"Failed to download NLTK stopwords: {e}. Using empty stopwords set.")
                    self.stop_words = set()
            except Exception as e:
                logger.error(f"Error loading NLTK stopwords: {e}. Using empty stopwords set.")
                self.stop_words = set()
        else:
            self.stop_words = set()

        _sentiment_model_obj, _topic_model_obj, _intent_model_obj, _urgency_model_obj = (None,) * 4
        if HAS_SKLEARN_AND_JOBLIB:
            self.sentiment_model = self._load_model(self.sentiment_model_path)
            self.topic_model = self._load_model(self.topic_model_path)
            self.intent_model = self._load_model(self.intent_model_path)
            self.urgency_model = self._load_model(self.urgency_model_path)
            _sentiment_model_obj = self.sentiment_model
            _topic_model_obj = self.topic_model
            _intent_model_obj = self.intent_model
            _urgency_model_obj = self.urgency_model

        self.sentiment_analyzer = SentimentModel(
            sentiment_model=_sentiment_model_obj, has_nltk_installed=HAS_NLTK
        )
        self.topic_analyzer = TopicModel(topic_model=_topic_model_obj)
        self.intent_analyzer = IntentModel(intent_model=_intent_model_obj)
        self.urgency_analyzer = UrgencyModel(urgency_model=_urgency_model_obj)

    def initialize_patterns(self):
        self.compiled_patterns = {
            category: [re.compile(p) for p in patterns]
            for category, patterns in self.CATEGORY_PATTERNS.items()
        }

    def _load_model(self, model_path: str) -> Optional[Any]:
        try:
            if os.path.exists(model_path):
                return joblib.load(model_path)
        except Exception as e:
            logger.error(f"Error loading model from {model_path}: {e}")
        return None

    def _preprocess_text(self, text: str) -> str:
        return clean_text(text)

    def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        return self.sentiment_analyzer.analyze(text)

    def _analyze_topic(self, text: str) -> Dict[str, Any]:
        return self.topic_analyzer.analyze(text)

    def _analyze_intent(self, text: str) -> Dict[str, Any]:
        return self.intent_analyzer.analyze(text)

    def _analyze_urgency(self, text: str) -> Dict[str, Any]:
        return self.urgency_analyzer.analyze(text)

    def _extract_keywords(self, text: str) -> List[str]:
        if not HAS_NLTK:
            return [word for word in text.lower().split() if len(word) > 4][:10]
        blob = TextBlob(text)
        keywords = [p for p in blob.noun_phrases if len(p.split()) <= 3]
        words = [w for w in blob.words if len(w) > 3 and w.lower() not in self.stop_words]
        keywords.extend(words[:10])
        return list(set(keywords))[:15]

    def _categorize_content(self, text: str) -> List[str]:
        text_lower = text.lower()
        if not self.compiled_patterns:
            self.initialize_patterns()
        category_scores = {
            category: sum(len(p.findall(text_lower)) for p in patterns)
            for category, patterns in self.compiled_patterns.items()
        }
        if not any(category_scores.values()):
            return ["General"]
        return sorted(category_scores, key=category_scores.get, reverse=True)[:3]

    def _calculate_confidence(self, analysis_results: List[Dict[str, Any]]) -> float:
        if not analysis_results:
            return 0.5
        return min(
            sum(r.get("confidence", 0.0) for r in analysis_results) / len(analysis_results), 0.95
        )

    def _generate_reasoning(self, sentiment, topic, intent, urgency) -> str:
        parts = []
        if sentiment and sentiment.get("sentiment") != "neutral":
            parts.append(f"Sentiment is {sentiment['sentiment']}")
        if topic and topic.get("topic") != "General":
            parts.append(f"Topic is {topic['topic']}")
        if intent and intent.get("intent") != "informational":
            parts.append(f"Intent is {intent['intent']}")
        if urgency and urgency.get("urgency") != "low":
            parts.append(f"Urgency is {urgency['urgency']}")
        return ". ".join(parts) + "." if parts else "No significant insights."

    def _suggest_labels(self, categories: List[str], urgency: str) -> List[str]:
        labels = categories.copy()
        if urgency in ["high", "critical"]:
            labels.append(f"{urgency.title()} Priority")
        return list(set(labels))[:6]

    def _detect_risk_factors(self, text: str) -> List[str]:
        flags = []
        if re.search(r"\b(free|winner|prize|lottery)\b", text, re.IGNORECASE):
            flags.append("potential_spam")
        if re.search(r"\b(confidential|password|ssn)\b", text, re.IGNORECASE):
            flags.append("sensitive_data")
        return flags

    def _validate_analysis(self, results: Dict[str, Any]) -> Dict[str, Any]:
        confidence = self._calculate_confidence(list(results.values()))
        is_reliable = confidence > 0.7
        return {
            "reliable": is_reliable,
            "feedback": "High confidence." if is_reliable else "Moderate confidence.",
        }

    def _get_fallback_analysis(self, error_msg: str) -> Dict[str, Any]:
        return {
            "reasoning": f"Fallback due to error: {error_msg}",
            "risk_flags": ["analysis_failed"],
            "topic": "General",
            "sentiment": "neutral",
            "intent": "informational",
            "urgency": "low",
            "confidence": 0.5,
            "categories": ["General"],
            "keywords": [],
            "suggested_labels": ["General"],
        }

    def _get_simple_fallback_analysis(self, subject: str, content: str) -> Dict[str, Any]:
        text = f"{subject} {content}".lower()
        sentiment = (
            "positive" if "thank" in text else "negative" if "problem" in text else "neutral"
        )
        urgency = "high" if "urgent" in text else "low"
        topic = "work_business" if "meeting" in text else "general_communication"
        categories = [topic]
        confidence_value = 0.6
        return {
            "topic": topic,
            "sentiment": sentiment,
            "intent": "informational",
            "urgency": urgency,
            "confidence": confidence_value,
            "categories": categories,
            "keywords": [],
            "reasoning": "Basic keyword matching.",
            "suggested_labels": categories,
            "risk_flags": [],
        }

    def analyze_email(self, subject: str, content: str) -> Dict[str, Any]:
        try:
            if not HAS_NLTK or not HAS_SKLEARN_AND_JOBLIB:
                return self._get_simple_fallback_analysis(subject, content)
            full_text = f"{subject} {content}"
            cleaned_text = self._preprocess_text(full_text)
            sentiment = self._analyze_sentiment(cleaned_text)
            topic = self._analyze_topic(cleaned_text)
            intent = self._analyze_intent(cleaned_text)
            urgency = self._analyze_urgency(cleaned_text)
            risk_flags = self._detect_risk_factors(cleaned_text)
            keywords = self._extract_keywords(cleaned_text)
            categories = self._categorize_content(cleaned_text)
            return self._build_final_analysis_response(
                sentiment, topic, intent, urgency, categories, keywords, risk_flags
            )
        except Exception as e:
            logger.exception(f"NLP analysis failed: {e}")
            return self._get_fallback_analysis(str(e))

    def _build_final_analysis_response(
        self, sentiment, topic, intent, urgency, categories, keywords, risk_flags
    ) -> Dict[str, Any]:
        """
        Helper function to consolidate analysis results and build the final response dictionary.

        Args:
            sentiment: Sentiment analysis result.
            topic: Topic analysis result.
            intent: Intent analysis result.
            urgency: Urgency analysis result.
            categories: List of identified categories.
            keywords: List of extracted keywords.
            risk_flags: List of identified risk flags.

        Returns:
            A dictionary containing the final, aggregated analysis.
        """
        analysis_results = [res for res in [sentiment, topic, intent, urgency] if res]
        confidence = self._calculate_confidence(analysis_results)
        reasoning = self._generate_reasoning(sentiment, topic, intent, urgency)
        suggested_labels = self._suggest_labels(categories, urgency.get("urgency", "low"))
        validation = self._validate_analysis(
            {"sentiment": sentiment, "topic": topic, "intent": intent, "urgency": urgency}
        )

        return {
            "topic": topic.get("topic", "General") if topic else "General",
            "sentiment": sentiment.get("sentiment", "neutral") if sentiment else "neutral",
            "intent": intent.get("intent", "informational") if intent else "informational",
            "urgency": urgency.get("urgency", "low") if urgency else "low",
            "confidence": confidence,
            "categories": categories,
            "keywords": keywords,
            "reasoning": reasoning,
            "suggested_labels": suggested_labels,
            "risk_flags": risk_flags,
            "validation": validation,
            "details": {
                "sentiment_analysis": sentiment,
                "topic_analysis": topic,
                "intent_analysis": intent,
                "urgency_analysis": urgency,
            },
        }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NLP Engine for Email Analysis")
    parser.add_argument("--subject", type=str, default="", help="Email subject")
    parser.add_argument("--content", type=str, default="", help="Email content")
    args = parser.parse_args()
    engine = NLPEngine()
    result = engine.analyze_email(args.subject, args.content)
    print(json.dumps(result, indent=2))
