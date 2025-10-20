#!/usr/bin/env python3
"""
Enhanced NLP Engine for Gmail AI Email Management.

This module provides advanced natural language processing capabilities with multiple AI models
and validation for analyzing email content.
"""

import argparse
import json
import logging
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

from .analysis_components.importance_model import ImportanceModel
from backend.python_nlp.text_utils import clean_text
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

try:
    import nltk
    from textblob import TextBlob
    HAS_NLTK = True
except ImportError:
    HAS_NLTK = False
    print("Warning: NLTK not available. Advanced NLP features will be disabled.", file=sys.stderr)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
logger = logging.getLogger(__name__)


class NLPEngine:
    """
    Natural Language Processing engine for email analysis.
    """
    CATEGORY_PATTERNS = {
        "Work & Business": [r"\b(meeting|project|deadline|client)\b"],
        "Finance & Banking": [r"\b(bank|payment|invoice|bill)\b"],
    }

    def __init__(self):
        """Initializes the NLP engine and loads all necessary models and resources."""
        model_dir = os.getenv("NLP_MODEL_DIR", "models")
        self.sentiment_model_path = os.path.join(model_dir, "sentiment")
        self.topic_model_path = os.path.join(model_dir, "topic")
        self.intent_model_path = os.path.join(model_dir, "intent")
        self.urgency_model_path = os.path.join(model_dir, "urgency")
        self.importance_model = ImportanceModel()
        self.compiled_patterns = {}

        if HAS_NLTK:
            try:
                nltk.data.find("corpora/stopwords")
            except LookupError:
                nltk.download("stopwords", quiet=True)
            self.stop_words = set(nltk.corpus.stopwords.words("english"))
        else:
            self.stop_words = set()

        logger.info("Attempting to load NLP models...")
        self.sentiment_analyzer = self._load_pipeline("sentiment-analysis", self.sentiment_model_path)
        self.topic_analyzer = self._load_pipeline("text-classification", self.topic_model_path)
        self.intent_analyzer = self._load_pipeline("text-classification", self.intent_model_path)
        self.urgency_analyzer = self._load_pipeline("text-classification", self.urgency_model_path)

    def _load_pipeline(self, task, path):
        try:
            if os.path.exists(path):
                return pipeline(task, model=path, tokenizer=path)
        except Exception as e:
            logger.error(f"Failed to load model from {path}: {e}")
        return None

    def initialize_patterns(self):
        """Pre-compiles regex patterns for categorization."""
        self.compiled_patterns = {cat: [re.compile(p) for p in patterns] for cat, patterns in self.CATEGORY_PATTERNS.items()}

    def _preprocess_text(self, text: str) -> str:
        return clean_text(text)

    def _analyze_with_model(self, analyzer, text: str, fallback_func, model_name: str) -> Dict[str, Any]:
        """Generic analysis function with model and fallback."""
        if analyzer:
            try:
                prediction = analyzer(text)[0]
                label_key = next((k for k in ['label', 'cat', 'topic'] if k in prediction), 'label')
                return {model_name: prediction[label_key], "confidence": prediction['score'], "method_used": f"model_{model_name}"}
            except Exception as e:
                logger.error(f"Error using {model_name} model: {e}. Trying fallback.")
        return fallback_func(text)

    def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        return self._analyze_with_model(self.sentiment_analyzer, text, self._analyze_sentiment_keyword, "sentiment")

    def _analyze_sentiment_keyword(self, text: str) -> Dict[str, Any]:
        text_lower = text.lower()
        if any(word in text_lower for word in ["good", "great", "excellent", "thank"]):
            return {"sentiment": "positive", "confidence": 0.6, "method_used": "fallback_keyword_sentiment"}
        if any(word in text_lower for word in ["bad", "terrible", "problem", "issue"]):
            return {"sentiment": "negative", "confidence": 0.6, "method_used": "fallback_keyword_sentiment"}
        return {"sentiment": "neutral", "confidence": 0.5, "method_used": "fallback_keyword_sentiment"}

    def _analyze_topic(self, text: str) -> Dict[str, Any]:
        return self._analyze_with_model(self.topic_analyzer, text, self._analyze_topic_keyword, "topic")

    def _analyze_topic_keyword(self, text: str) -> Dict[str, Any]:
        text_lower = text.lower()
        for topic, keywords in self.CATEGORY_PATTERNS.items():
            if any(re.search(kw, text_lower) for kw in keywords):
                return {"topic": topic, "confidence": 0.5, "method_used": "fallback_keyword_topic"}
        return {"topic": "general_communication", "confidence": 0.5, "method_used": "fallback_keyword_topic"}

    def _analyze_intent(self, text: str) -> Dict[str, Any]:
        return self._analyze_with_model(self.intent_analyzer, text, self._analyze_intent_regex, "intent")

    def _analyze_intent_regex(self, text: str) -> Dict[str, Any]:
        text_lower = text.lower()
        if re.search(r"\b(please|could you|need|require)\b", text_lower):
            return {"intent": "request", "confidence": 0.6, "method_used": "fallback_regex_intent"}
        if re.search(r"\b(question|ask|wonder)\b", text_lower):
            return {"intent": "inquiry", "confidence": 0.6, "method_used": "fallback_regex_intent"}
        return {"intent": "informational", "confidence": 0.5, "method_used": "fallback_regex_intent"}

    def _analyze_urgency(self, text: str) -> Dict[str, Any]:
        return self._analyze_with_model(self.urgency_analyzer, text, self._analyze_urgency_regex, "urgency")

    def _analyze_urgency_regex(self, text: str) -> Dict[str, Any]:
        text_lower = text.lower()
        if re.search(r"\b(urgent|asap|immediately|critical)\b", text_lower):
            return {"urgency": "critical", "confidence": 0.9, "method_used": "fallback_regex_urgency"}
        if re.search(r"\b(soon|quickly|priority)\b", text_lower):
            return {"urgency": "high", "confidence": 0.8, "method_used": "fallback_regex_urgency"}
        return {"urgency": "low", "confidence": 0.5, "method_used": "fallback_regex_urgency"}

    def _analyze_importance(self, text: str) -> Dict[str, Any]:
        return self.importance_model.analyze(text)

    def _extract_keywords(self, text: str) -> List[str]:
        if not HAS_NLTK:
            return [word for word in text.lower().split() if len(word) > 4][:5]
        blob = TextBlob(text)
        return list(set(p for p in blob.noun_phrases if len(p.split()) <= 2))[:10]

    def analyze_email(self, subject: str, content: str) -> Dict[str, Any]:
        full_text = f"{subject} {content}"
        cleaned_text = self._preprocess_text(full_text)

        sentiment = self._analyze_sentiment(cleaned_text)
        topic = self._analyze_topic(cleaned_text)
        intent = self._analyze_intent(cleaned_text)
        urgency = self._analyze_urgency(cleaned_text)
        importance = self._analyze_importance(cleaned_text)
        keywords = self._extract_keywords(cleaned_text)

        all_results = [sentiment, topic, intent, urgency, importance]
        confidence = sum(r['confidence'] for r in all_results) / len(all_results)

        return {
            "topic": topic.get('topic'), "sentiment": sentiment.get('sentiment'), "intent": intent.get('intent'),
            "urgency": urgency.get('urgency'), "isImportant": importance.get('is_important'),
            "confidence": confidence, "keywords": keywords, "reasoning": "Composite analysis from multiple models."
        }

def main():
    parser = argparse.ArgumentParser(description="NLP Engine for Email Analysis")
    parser.add_argument("--subject", type=str, default="", help="Email subject")
    parser.add_argument("--content", type=str, default="", help="Email content")
    parser.add_argument("--health-check", action="store_true", help="Perform a health check.")
    parser.add_argument("--output-format", type=str, default="text", choices=["json", "text"])
    args = parser.parse_args()

    engine = NLPEngine()

    if args.health_check:
        status = {"status": "ok", "models": ["sentiment", "topic", "intent", "urgency", "importance"], "nltk": HAS_NLTK}
        print(json.dumps(status, indent=2 if args.output_format == 'text' else None))
        return

    if args.subject or args.content:
        result = engine.analyze_email(args.subject, args.content)
        print(json.dumps(result, indent=2 if args.output_format == 'text' else None))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
