#!/usr/bin/env python3
"""
An enhanced NLP engine for comprehensive email analysis.

This module provides the `NLPEngine` class, which orchestrates various NLP
models and techniques to analyze email content for sentiment, topic, intent,
and urgency. It is designed to be robust, with fallbacks for when models or
dependencies are not available.
"""


import argparse
import json
import logging
import os
import re
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

from backend.python_nlp.text_utils import clean_text
from .analysis_components.intent_model import IntentModel
from .analysis_components.sentiment_model import SentimentModel
from .analysis_components.topic_model import TopicModel
from .analysis_components.urgency_model import UrgencyModel

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
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
    print("Warning: NLTK, scikit-learn or joblib not available. Advanced NLP features will be disabled.", file=sys.stderr)


class NLPEngine:
    """
    Orchestrates NLP tasks for email analysis.

    This engine integrates multiple analysis components to provide a holistic
    view of an email's content, including its sentiment, topic, intent, and
    urgency. It handles model loading, text preprocessing, and result aggregation.

    Attributes:
        sentiment_model_path: Path to the serialized sentiment model.
        topic_model_path: Path to the serialized topic model.
        intent_model_path: Path to the serialized intent model.
        urgency_model_path: Path to the serialized urgency model.
        stop_words: A set of English stopwords for text processing.
        sentiment_analyzer: Component for sentiment analysis.
        topic_analyzer: Component for topic analysis.
        intent_analyzer: Component for intent analysis.
        urgency_analyzer: Component for urgency analysis.
    """
    CATEGORY_PATTERNS = {
        "Work & Business": [
            r"\b(meeting|conference|project|deadline|client|presentation|report|proposal|budget|team|"
            r"colleague|office|work|business|professional|corporate|company|organization)\b",
            r"\b(employee|staff|manager|supervisor|director|executive|department|division|"
            r"quarterly|annual|monthly|weekly|daily)\b",
        ],
        "Finance & Banking": [
            r"\b(bank|payment|transaction|invoice|bill|statement|account|credit|debit|transfer|"
            r"money|financial|insurance|investment|loan|mortgage)\b",
            r"\$[\d,]+|\b\d+\s?(dollars?|USD|EUR|GBP)\b",
            r"\b(tax|taxes|irs|refund|audit|accountant|bookkeeping|overdraft|bankruptcy)\b",
        ],
        "Healthcare": [
            r"\b(doctor|medical|health|hospital|clinic|appointment|prescription|medicine|"
            r"treatment|therapy|checkup|surgery|dental|pharmacy)\b",
            r"\b(symptoms|diagnosis|patient|specialist|emergency|ambulance|insurance|"
            r"medicare|medicaid|covid|coronavirus|vaccine)\b",
        ],
        "Personal & Family": [
            r"\b(family|personal|friend|birthday|anniversary|vacation|holiday|weekend|"
            r"dinner|lunch|home|house|kids|children)\b",
            r"\b(mom|dad|mother|father|sister|brother|grandma|grandpa|wedding|"
            r"graduation|baby|party|celebration)\b",
        ],
        "Travel": [
            r"\b(travel|flight|hotel|booking|reservation|trip|vacation|destination|"
            r"airport|airline|passport|visa|itinerary)\b",
            r"\b(departure|arrival|check-in|luggage|baggage|cruise|resort|tour|"
            r"tickets|confirmation)\b",
        ],
        "Technology": [
            r"\b(software|hardware|computer|laptop|mobile|app|application|website|"
            r"internet|email|password|account|login)\b",
            r"\b(server|database|API|code|programming|development|tech|technical|"
            r"IT|support|troubleshoot|install)\b",
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
            except LookupError:
                logger.info("Downloading NLTK 'stopwords' resource...")
                nltk.download("stopwords", quiet=True)
            self.stop_words = set(nltk.corpus.stopwords.words("english"))
        else:
            self.stop_words = set()

<<<<<<< HEAD
        # Initialize model attributes
        self.sentiment_model = None
        self.topic_model = None
        self.intent_model = None
        self.urgency_model = None



        # Load models if dependencies are available
        # These attributes self.sentiment_model, self.topic_model etc. are the actual model objects (e.g. from joblib)
        _sentiment_model_obj = None
        _topic_model_obj = None
        _intent_model_obj = None
        _urgency_model_obj = None

=======
        _sentiment_model_obj, _topic_model_obj, _intent_model_obj, _urgency_model_obj = (None,) * 4
>>>>>>> origin/feature/git-history-analysis-report
        if HAS_SKLEARN_AND_JOBLIB:
            logger.info("Attempting to load NLP models...")
            self.sentiment_model = self._load_model(self.sentiment_model_path)
            self.topic_model = self._load_model(self.topic_model_path)
            self.intent_model = self._load_model(self.intent_model_path)
            self.urgency_model = self._load_model(self.urgency_model_path)
            _sentiment_model_obj = self.sentiment_model
            _topic_model_obj = self.topic_model
            _intent_model_obj = self.intent_model
            _urgency_model_obj = self.urgency_model
        else:
            logger.warning("Scikit-learn or joblib not available. Using fallback logic.")

<<<<<<< HEAD
        # Initialize SentimentModel (previously SentimentAnalyzer)
        # These attributes self.sentiment_analyzer, self.topic_analyzer etc. are instances of our analyzer/model classes
        # self.sentiment_analyzer = SentimentModel(
        #     sentiment_model=_sentiment_model_obj, has_nltk_installed=HAS_NLTK
        # )

        # Initialize TopicModel (previously TopicAnalyzer)
        # self.topic_analyzer = TopicModel(topic_model=_topic_model_obj) # This is now redundant

        # Initialize IntentModel (previously IntentAnalyzer)
        # self.intent_analyzer = IntentModel(intent_model=_intent_model_obj)

        # Initialize UrgencyModel (previously UrgencyAnalyzer)
        # self.urgency_analyzer = UrgencyModel(urgency_model=_urgency_model_obj)
=======
        self.sentiment_analyzer = SentimentModel(sentiment_model=_sentiment_model_obj, has_nltk_installed=HAS_NLTK)
        self.topic_analyzer = TopicModel(topic_model=_topic_model_obj)
        self.intent_analyzer = IntentModel(intent_model=_intent_model_obj)
        self.urgency_analyzer = UrgencyModel(urgency_model=_urgency_model_obj)
>>>>>>> origin/feature/git-history-analysis-report

    def initialize_patterns(self):
        """Pre-compiles regex patterns for categorization."""
        logger.info("Compiling regex patterns for categorization...")
        self.compiled_patterns = {
            category: [re.compile(p) for p in patterns]
            for category, patterns in self.CATEGORY_PATTERNS.items()
        }
        logger.info("Regex patterns compiled successfully.")

    def _load_model(self, model_path: str) -> Optional[Any]:
        """
        Safely loads a pickled model from the specified file path.

        Args:
            model_path: The path to the .pkl model file.

        Returns:
            The loaded model object, or None if loading fails.
        """
        try:
            if os.path.exists(model_path):
                model = joblib.load(model_path)
                logger.info(f"Successfully loaded model from {model_path}")
                return model
            logger.warning(f"Model file not found at {model_path}.")
        except Exception as e:
            logger.error(f"Error loading model from {model_path}: {e}")
        return None

    def _preprocess_text(self, text: str) -> str:
        """
        Applies basic text cleaning and normalization.

        Args:
            text: The raw text to be preprocessed.

        Returns:
            The cleaned and normalized text.
        """
        return clean_text(text)

    def _analyze_sentiment_model(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Analyze sentiment using the loaded sklearn model.
        """
        if not self.sentiment_model:
            return None

        try:
            prediction = self.sentiment_model.predict([text])[0]
            probabilities = self.sentiment_model.predict_proba([text])[0]
            confidence = max(probabilities)

            polarity = 0.0
            if prediction == "positive":
                polarity = confidence
            elif prediction == "negative":
                polarity = -confidence

            return {
                "sentiment": str(prediction),
                "polarity": polarity,
                "subjectivity": 0.5,
                "confidence": float(confidence),
                "method_used": "model_sentiment",
            }
        except Exception as e:
            logger.error(f"Error using sentiment model: {e}. Trying fallback.")
            return None

    def _analyze_sentiment_textblob(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Analyze sentiment using TextBlob as a fallback method.
        """
        if not HAS_NLTK:
            logger.warning("TextBlob analysis skipped: NLTK not available.")
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
                confidence = 0.7

            return {
                "sentiment": sentiment_label,
                "polarity": polarity,
                "subjectivity": subjectivity,
                "confidence": confidence,
                "method_used": "fallback_textblob_sentiment",
            }
        except Exception as e:
            logger.error(f"Error during TextBlob sentiment analysis: {e}")
            return None

    def _analyze_sentiment_keyword(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment using keyword matching as a final fallback method.
        """
        text_lower = text.lower()
        positive_words = ["good", "great", "excellent", "thank", "please", "welcome", "happy", "love"]
        negative_words = ["bad", "terrible", "problem", "issue", "error", "failed", "hate", "angry"]

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
            confidence = 0.5

        return {
            "sentiment": sentiment_label,
            "polarity": polarity,
            "subjectivity": 0.5,
            "confidence": confidence,
            "method_used": "fallback_keyword_sentiment",
        }

    def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
<<<<<<< HEAD
        Perform sentiment analysis using available methods in order of preference.
=======
        Performs sentiment analysis using the sentiment component.

        Args:
            text: The text to analyze.

        Returns:
            A dictionary containing the sentiment analysis results.
>>>>>>> origin/feature/git-history-analysis-report
        """
        analysis_result = self._analyze_sentiment_model(text)
        if analysis_result:
            logger.info("Sentiment analysis performed using ML model.")
            return analysis_result

        analysis_result = self._analyze_sentiment_textblob(text)
        if analysis_result:
            logger.info("Sentiment analysis performed using TextBlob as fallback.")
            return analysis_result

        logger.info("Sentiment analysis performed using keyword matching as final fallback.")
        return self._analyze_sentiment_keyword(text)

    def _analyze_topic_model(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Analyzes the topic of the text using a pre-trained scikit-learn model.

        Args:
            text: The text to analyze.

        Returns:
            A dictionary with the predicted topic and confidence score, or None if
            the model is not available or an error occurs.
        """
        if not self.topic_model:
            return None
        try:
            prediction = self.topic_model.predict([text])[0]
            probabilities = self.topic_model.predict_proba([text])[0]
            confidence = float(max(probabilities))
            return {"topic": str(prediction), "confidence": confidence, "method_used": "model_topic"}
        except Exception as e:
            logger.error(f"Error using topic model: {e}. Trying fallback.")
            return None

    def _analyze_topic_keyword(self, text: str) -> Dict[str, Any]:
        """
        Analyzes the topic of the text using keyword matching as a fallback.

        Args:
            text: The text to analyze.

        Returns:
            A dictionary with the predicted topic and a heuristic confidence score.
        """
        topics = {
            "Work & Business": ["meeting", "project", "deadline", "client"],
            "Finance & Banking": ["payment", "invoice", "bill", "statement"],
            "Personal & Family": ["family", "friend", "birthday", "weekend"],
            "Health & Wellness": ["doctor", "medical", "health", "appointment"],
            "Travel & Leisure": ["travel", "flight", "hotel", "booking"],
        }
        text_lower = text.lower()
        topic_scores = {topic: sum(1 for keyword in keywords if keyword in text_lower) for topic, keywords in topics.items()}
        if any(topic_scores.values()):
            best_topic = max(topic_scores, key=topic_scores.get)
            confidence = min(topic_scores[best_topic] / 5.0, 0.9)
            normalized_topic = best_topic.lower().replace(" & ", "_").replace(" ", "_")
            return {"topic": normalized_topic, "confidence": max(0.1, confidence), "method_used": "fallback_keyword_topic"}
        return {"topic": "general_communication", "confidence": 0.5, "method_used": "fallback_keyword_topic"}

    def _analyze_topic(self, text: str) -> Dict[str, Any]:
        """
<<<<<<< HEAD
        Identify the main topic of the email using available methods.
        It first tries the ML model and then falls back to keyword matching.
=======
        Identifies the main topic using the topic component.

        Args:
            text: The text to analyze.

        Returns:
            A dictionary containing the topic analysis results.
>>>>>>> origin/feature/git-history-analysis-report
        """
        # Try model-based analysis first
        analysis_result = self._analyze_topic_model(text)
        if analysis_result:
            logger.info("Topic analysis performed using ML model.")
            return analysis_result

        # Use keyword matching as fallback
        logger.info("Topic analysis performed using keyword matching as fallback.")
        return self._analyze_topic_keyword(text)

    def _analyze_intent_model(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Analyze intent using the loaded sklearn model.
        """
        if not self.intent_model:
            return None

        try:
            prediction = self.intent_model.predict([text])[0]
            probabilities = self.intent_model.predict_proba([text])[0]
            confidence = float(max(probabilities))

            return {
                "intent": str(prediction),
                "confidence": confidence,
                "method_used": "model_intent",
            }
        except Exception as e:
            logger.error(f"Error using intent model: {e}. Trying fallback.")
            return None

    def _analyze_intent_regex(self, text: str) -> Dict[str, Any]:
        """
        Analyze intent using regex pattern matching as a fallback method.
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

        intent_scores = {}
        text_lower = text.lower()
        for intent, pattern in intent_patterns.items():
            matches = re.findall(pattern, text_lower)
            intent_scores[intent] = len(matches)

        if any(score > 0 for score in intent_scores.values()):
            best_intent = max(intent_scores, key=intent_scores.get)
            confidence = min(intent_scores[best_intent] / 3.0, 0.9)  # Heuristic

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

    def _analyze_intent(self, text: str) -> Dict[str, Any]:
        """
<<<<<<< HEAD
        Determine the intent of the email using available methods.
=======
        Determines the email's intent using the intent component.

        Args:
            text: The text to analyze.

        Returns:
            A dictionary containing the intent analysis results.
>>>>>>> origin/feature/git-history-analysis-report
        """
        analysis_result = self._analyze_intent_model(text)
        if analysis_result:
            logger.info("Intent analysis performed using ML model.")
            return analysis_result

        logger.info("Intent analysis performed using regex matching as fallback.")
        return self._analyze_intent_regex(text)

    def _analyze_urgency_model(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Analyze urgency using the loaded sklearn model.
        """
        if not self.urgency_model:
            return None

        try:
            prediction = self.urgency_model.predict([text])[0]
            probabilities = self.urgency_model.predict_proba([text])[0]
            confidence = float(max(probabilities))

            return {
                "urgency": str(prediction),
                "confidence": confidence,
                "method_used": "model_urgency",
            }
        except Exception as e:
            logger.error(f"Error using urgency model: {e}. Trying fallback.")
            return None

    def _analyze_urgency_regex(self, text: str) -> Dict[str, Any]:
        """
        Analyze urgency using regex pattern matching as a fallback method.
        """
        text_lower = text.lower()

        if re.search(
            r"\b(emergency|urgent|asap|immediately|critical|crisis|disaster)\b",
            text_lower,
        ):
            urgency_label = "critical"
            confidence = 0.9
        elif re.search(
            r"\b(soon|quickly|priority|important|deadline|time-sensitive)\b", text_lower
        ):
            urgency_label = "high"
            confidence = 0.8
        elif re.search(r"\b(when you can|next week|upcoming|planned|scheduled)\b", text_lower):
            urgency_label = "medium"
            confidence = 0.6
        else:
            urgency_label = "low"
            confidence = 0.5

        return {
            "urgency": urgency_label,
            "confidence": confidence,
            "method_used": "fallback_regex_urgency",
        }

    def _analyze_urgency(self, text: str) -> Dict[str, Any]:
        """
<<<<<<< HEAD
        Assess the urgency level of the email using available methods.
=======
        Assesses the urgency level using the urgency component.

        Args:
            text: The text to analyze.

        Returns:
            A dictionary containing the urgency analysis results.
>>>>>>> origin/feature/git-history-analysis-report
        """
        analysis_result = self._analyze_urgency_model(text)
        if analysis_result:
            logger.info("Urgency analysis performed using ML model.")
            return analysis_result

        logger.info("Urgency analysis performed using regex matching as fallback.")
        return self._analyze_urgency_regex(text)

    def _extract_keywords(self, text: str) -> List[str]:
        """
        Extracts important keywords and noun phrases from the text.

        Args:
            text: The text from which to extract keywords.

        Returns:
            A list of extracted keywords.
        """
        if not HAS_NLTK:
            return [word for word in text.lower().split() if len(word) > 4][:10]
        blob = TextBlob(text)
        keywords = [p for p in blob.noun_phrases if len(p.split()) <= 3]
        words = [w for w in blob.words if len(w) > 3 and w.lower() not in self.stop_words]
        keywords.extend(words[:10])
        return list(set(keywords))[:15]

    def _categorize_content(self, text: str) -> List[str]:
        """
        Categorize email content based on pre-compiled keyword patterns.
        This method uses regex pattern matching to identify the categories
        that best match the email content.
        Args:
            text: Text to categorize
        Returns:
            A list of matched category names.
        """
        text_lower = text.lower()

        if not self.compiled_patterns:
            logger.warning("Regex patterns not compiled. Call initialize_patterns() first. Falling back to on-the-fly compilation.")
            self.initialize_patterns()

        category_scores = {}
        for category, patterns in self.compiled_patterns.items():
            score = sum(len(pattern.findall(text_lower)) for pattern in patterns)
            if score > 0:
                category_scores[category] = score

        if not category_scores:
            return ["General"]

        # Sort categories by score (descending) and return top 3
        sorted_categories = sorted(category_scores.keys(), key=lambda cat: category_scores[cat], reverse=True)
        return sorted_categories[:3]

    def _calculate_confidence(self, analysis_results: List[Dict[str, Any]]) -> float:
        """
        Computes an overall confidence score from individual analysis results.

        Args:
            analysis_results: A list of dictionaries from different analysis components.

        Returns:
            A single confidence score between 0.0 and 1.0.
        """
        if not analysis_results:
            return 0.5
        total_confidence = sum(result.get("confidence", 0.0) for result in analysis_results)
        return min(total_confidence / len(analysis_results), 0.95)

    def _generate_reasoning(self, sentiment, topic, intent, urgency) -> str:
        """
        Constructs a human-readable summary of the analysis findings.

        Args:
            sentiment: The sentiment analysis result.
            topic: The topic analysis result.
            intent: The intent analysis result.
            urgency: The urgency analysis result.

        Returns:
            A string explaining the analysis results.
        """
        parts = []
        if sentiment and sentiment.get("sentiment") != "neutral":
            parts.append(f"Sentiment is {sentiment['sentiment']}")
        if topic and topic.get("topic") != "General":
            parts.append(f"Topic is {topic['topic']}")
        if intent and intent.get("intent") != "informational":
            parts.append(f"Intent is {intent['intent']}")
        if urgency and urgency.get("urgency") != "low":
            parts.append(f"Urgency is {urgency['urgency']}")
        return ". ".join(parts) + "." if parts else "No significant insights detected."

    def _suggest_labels(self, categories: List[str], urgency: str) -> List[str]:
        """
        Suggests relevant labels based on the analysis.

        Args:
            categories: A list of identified categories.
            urgency: The assessed urgency level.

        Returns:
            A list of suggested string labels.
        """
        labels = categories.copy()
        if urgency in ["high", "critical"]:
            labels.append(f"{urgency.title()} Priority")
        return list(set(labels))[:6]

    def _detect_risk_factors(self, text: str) -> List[str]:
        """
        Scans the text for potential risk factors like spam or sensitive data.

        Args:
            text: The text to scan.

        Returns:
            A list of identified risk flags.
        """
        risk_flags = []
        if re.search(r"\b(free|winner|prize|lottery)\b", text, re.IGNORECASE):
            risk_flags.append("potential_spam")
        if re.search(r"\b(confidential|password|ssn)\b", text, re.IGNORECASE):
            risk_flags.append("sensitive_data")
        return risk_flags

    def _validate_analysis(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates the overall analysis based on confidence scores.

        Args:
            analysis_results: A dictionary of analysis results.

        Returns:
            A dictionary containing validation feedback.
        """
        confidence = self._calculate_confidence(list(analysis_results.values()))
        is_reliable = confidence > 0.7
        feedback = "Analysis completed with high confidence." if is_reliable else "Analysis completed with moderate confidence. Please review."
        return {"method": "confidence_threshold", "score": confidence, "reliable": is_reliable, "feedback": feedback}

    def _get_fallback_analysis(self, error_msg: str) -> Dict[str, Any]:
        """
        Provides a default analysis structure in case of a critical error.

        Args:
            error_msg: The error message to include in the reasoning.

        Returns:
            A dictionary with default analysis values.
        """
        return {
            "topic": "General",
            "sentiment": "neutral",
            "intent": "informational",
            "urgency": "low",
            "confidence": 0.5,
            "categories": ["General"],
            "keywords": [],
            "reasoning": f"Fallback analysis due to error: {error_msg}",
            "suggested_labels": ["General"],
            "risk_flags": ["analysis_failed"],  # Ensure this key exists
            "validation": {
                "method": "fallback",  # Ensure this key exists
                "score": 0.5,
                "reliable": False,
                "feedback": "Analysis failed, using fallback method",
            },
            # "action_items": [], # Removed
        }

    def _get_simple_fallback_analysis(self, subject: str, content: str) -> Dict[str, Any]:
        """
        Provides a basic, rule-based analysis when models are unavailable.

        Args:
            subject: The email subject.
            content: The email content.

        Returns:
            A dictionary with basic analysis results.
        """
        text = f"{subject} {content}".lower()
        sentiment = "positive" if "thank" in text else "negative" if "problem" in text else "neutral"
        urgency = "high" if "urgent" in text else "low"
        topic = "work_business" if "meeting" in text else "general_communication"
        return {
            "topic": topic,
            "sentiment": sentiment,
            "intent": "informational",
            "urgency": urgency,
            "confidence": confidence_value,  # Use calculated confidence
            "categories": categories,
            "keywords": [],
            "reasoning": "Basic analysis using keyword matching (NLTK not available)",
            "suggested_labels": categories,
            "risk_flags": [],
            "validation": {
                "method": "basic_fallback",  # Changed key for consistency
                "score": 0.6,
                "reliable": False,
                "feedback": "Basic analysis - NLTK/models not available or failed",
            },
            # "action_items": [], # Removed
        }

    def _analyze_action_items(self, text: str) -> List[Dict[str, Any]]:
        """
        Analyze text for action items using ActionItemExtractor.
        """
        logger.info("Action item analysis skipped (feature removed).")
        return []

    def analyze_email(self, subject: str, content: str) -> Dict[str, Any]:
        """
        Performs a comprehensive NLP analysis of an email.

        This is the main public method that orchestrates the entire analysis
        pipeline, from preprocessing to result aggregation.

        Args:
            subject: The subject line of the email.
            content: The body content of the email.

        Returns:
            A dictionary containing the detailed analysis results.
        """
        try:
            if not HAS_NLTK or not HAS_SKLEARN_AND_JOBLIB:
                logger.warning("Dependencies missing, using simple fallback analysis.")
                return self._get_simple_fallback_analysis(subject, content)

            full_text = f"{subject} {content}"
            cleaned_text = self._preprocess_text(full_text)

<<<<<<< HEAD
            # Multi-model analysis
            analyses = [
                ("sentiment", self._analyze_sentiment),
                ("topic", self._analyze_topic),
                ("intent", self._analyze_intent),
                ("urgency", self._analyze_urgency),
            ]
=======
            sentiment = self._analyze_sentiment(cleaned_text)
            topic = self._analyze_topic(cleaned_text)
            intent = self._analyze_intent(cleaned_text)
            urgency = self._analyze_urgency(cleaned_text)
            risk_flags = self._detect_risk_factors(cleaned_text)
            keywords = self._extract_keywords(cleaned_text)
            categories = self._categorize_content(cleaned_text)
>>>>>>> origin/feature/git-history-analysis-report

            results = {}
            for name, func in analyses:
                logger.info(f"Analyzing {name}...")
                result = func(cleaned_text)
                logger.info(f"{name.capitalize()} analysis completed. Method: {result.get('method_used', 'unknown')}")
                results[name] = result

            # This method is regex-based, no model to load for it currently per its implementation
            logger.info("Detecting risk factors...")
            risk_analysis_flags = self._detect_risk_factors(cleaned_text)
            logger.info(f"Risk factor detection completed. Flags: {risk_analysis_flags}")

            # Extract keywords and entities
            logger.info("Extracting keywords...")
            keywords = self._extract_keywords(cleaned_text)  # Uses TextBlob if available
            logger.info(f"Keyword extraction completed. Keywords: {keywords}")

            logger.info("Categorizing content...")
            categories = self._categorize_content(cleaned_text)  # Regex-based
            logger.info(f"Content categorization completed. Categories: {categories}")

            logger.info("Analyzing action items...")
            action_items = self._analyze_action_items(
                full_text
            )  # Use full_text for action items for broader context before cleaning for other models
            logger.info(
                f"Action item analysis completed. Found {len(action_items)} potential actions."
            )

            logger.info("Building final analysis response...")
            response = self._build_final_analysis_response(
                results["sentiment"],
                results["topic"],
                results["intent"],
                results["urgency"],
                categories,
                keywords,
                risk_analysis_flags,
                # action_items, # Removed - _analyze_action_items now returns empty list, but param removed from build
            )
            logger.info("Final analysis response built successfully.")
            return response

        except Exception as e:
            logger.exception(f"NLP analysis failed: {e}")
            return self._get_fallback_analysis(str(e))

    def _build_final_analysis_response(
        self,
        sentiment_analysis,
        topic_analysis,
        intent_analysis,
        urgency_analysis,
        categories,
        keywords,
        risk_analysis_flags,
        # action_items, # Removed param
    ) -> Dict[str, Any]:
        """Helper function to consolidate analysis results and build the final response dictionary."""

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
        validation = self._validate_analysis({"sentiment": sentiment, "topic": topic, "intent": intent, "urgency": urgency})

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
                "sentiment_analysis": sentiment_analysis,
                "topic_analysis": topic_analysis,
                "intent_analysis": intent_analysis,
                "urgency_analysis": urgency_analysis,
            },
            # "action_items": action_items, # Removed
        }


def main():
    """Provides a command-line interface for the NLP engine."""
    parser = argparse.ArgumentParser(description="NLP Engine for Email Analysis")
    parser.add_argument("--subject", type=str, default="", help="Email subject")
    parser.add_argument("--content", type=str, default="", help="Email content")
    parser.add_argument("--health-check", action="store_true", help="Perform a health check.")
    parser.add_argument("--output-format", type=str, default="text", choices=["json", "text"], help="Output format.")
    args = parser.parse_args()

    engine = NLPEngine()
    if args.health_check:
        _perform_health_check(engine, args.output_format)
    else:
        _perform_email_analysis_cli(engine, args.subject, args.content, args.output_format)


def _perform_health_check(engine: NLPEngine, output_format: str):
    """
    Performs a health check on the NLPEngine and its models.

    Args:
        engine: An instance of the NLPEngine.
        output_format: The desired output format ('json' or 'text').
    """
    models_available = []
    if engine.sentiment_model: models_available.append("sentiment")
    if engine.topic_model: models_available.append("topic")
    if engine.intent_model: models_available.append("intent")
    if engine.urgency_model: models_available.append("urgency")

    health_status = {
        "status": "ok" if models_available else "degraded",
        "models_available": models_available,
        "nltk_available": HAS_NLTK,
        "sklearn_available": HAS_SKLEARN_AND_JOBLIB,
        "timestamp": datetime.now().isoformat(),
    }
    if output_format == "json":
        print(json.dumps(health_status))
    else:
        print(json.dumps(health_status, indent=2))


def _perform_email_analysis_cli(engine: NLPEngine, subject: str, content: str, output_format: str):
    """
    Performs email analysis via the CLI.

    Args:
        engine: An instance of the NLPEngine.
        subject: The email subject.
        content: The email content.
        output_format: The desired output format.
    """
    result = engine.analyze_email(subject, content)
    if output_format == "json":
        print(json.dumps(result))
    else:
        print(json.dumps(result, indent=2))


def _handle_backward_compatible_cli_invocation(engine: NLPEngine, args: argparse.Namespace, argv: List[str]) -> bool:
    """
    Handles backward-compatible CLI calls with positional arguments.

    Args:
        engine: An instance of the NLPEngine.
        args: Parsed command-line arguments.
        argv: The list of command-line arguments.

    Returns:
        True if the old-style invocation was handled, False otherwise.
    """
    known_flags = ["--analyze-email", "--health-check", "--subject", "--content", "--output-format"]
    if any(flag in argv for flag in known_flags) or len(argv) < 2:
        return False

    subject_old = argv[1]
    content_old = argv[2] if len(argv) > 2 else ""
    _perform_email_analysis_cli(engine, subject_old, content_old, args.output_format)
    return True


if __name__ == "__main__":
    main()