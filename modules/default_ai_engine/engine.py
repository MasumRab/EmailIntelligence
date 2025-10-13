import logging
from typing import Any, Dict, List, Optional

# Core framework components
from src.core.ai_engine import AIAnalysisResult, BaseAIEngine

# Module-specific components
from .nlp_engine import NLPEngine

logger = logging.getLogger(__name__)


class DefaultAIEngine(BaseAIEngine):
    """
    The default AI engine implementation, based on the original NLPEngine.

    This class serves as the concrete implementation of the BaseAIEngine interface,
    providing a fully functional AI analysis engine out-of-the-box.
    """

    def __init__(self):
        self.nlp_engine = NLPEngine()
        self.category_lookup_map: Dict[str, Dict[str, Any]] = {}

    def initialize(self):
        """Initializes the NLP engine and pre-compiles patterns."""
        try:
            self.nlp_engine.initialize_patterns()
            self.health_check()
            logger.info("Default AI Engine initialized successfully.")
        except Exception as e:
            logger.error(f"Default AI Engine initialization failed: {e}", exc_info=True)

    def _build_category_lookup(self, categories: List[Dict[str, Any]]) -> None:
        """Builds a normalized lookup map for categories."""
        self.category_lookup_map = {cat["name"].lower(): cat for cat in categories}
        logger.info("Built category lookup map for the default AI engine.")

    def _match_category_id(self, ai_categories: List[str]) -> Optional[int]:
        """Matches AI-suggested categories to provided categories."""
        if not ai_categories:
            return None

        if not self.category_lookup_map:
            return None

        for ai_cat_str in ai_categories:
            ai_cat_lower = ai_cat_str.lower()
            if ai_cat_lower in self.category_lookup_map:
                matched_cat = self.category_lookup_map[ai_cat_lower]
                return matched_cat["id"]
        return None

    async def analyze_email(
        self, subject: str, content: str, categories: Optional[List[Dict[str, Any]]] = None
    ) -> AIAnalysisResult:
        """Analyzes email content and returns a standardized analysis result."""
        try:
            analysis_data = self.nlp_engine.analyze_email(subject, content)

            if categories:
                self._build_category_lookup(categories)
                ai_categories = analysis_data.get("categories", [])
                matched_category_id = self._match_category_id(ai_categories)
                analysis_data["category_id"] = matched_category_id

            return AIAnalysisResult(analysis_data)
        except Exception as e:
            logger.error(f"An error occurred during AI analysis: {e}", exc_info=True)
            # Return a fallback result in case of error
            return AIAnalysisResult(
                {"reasoning": f"AI analysis error: {e}", "risk_flags": ["ai_analysis_failed"]}
            )

    def health_check(self) -> Dict[str, Any]:
        """Performs a health check on the underlying NLP engine."""
        # This can be expanded to be more detailed if needed.
        return self.nlp_engine._get_simple_fallback_analysis("health check", "health check")

    def cleanup(self):
        """Cleans up resources used by the NLP engine."""
        # The original cleanup logic can be added here if needed.
        logger.info("Default AI Engine cleanup complete.")

    def train_models(self, training_data: Optional[Dict[str, Any]] = None):
        """Trains or retrains the AI models using sample data or provided training data."""
        try:
            import os

            import joblib
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.linear_model import LogisticRegression
            from sklearn.pipeline import Pipeline

            logger.info("Starting AI model training...")

            # Sample training data if none provided
            if training_data is None:
                training_data = {
                    "sentiment": {
                        "texts": [
                            "I love this product",
                            "This is amazing",
                            "Great job",
                            "This is terrible",
                            "I hate this",
                            "Worst experience",
                        ],
                        "labels": [
                            "positive",
                            "positive",
                            "positive",
                            "negative",
                            "negative",
                            "negative",
                        ],
                    },
                    "topic": {
                        "texts": [
                            "Meeting scheduled for tomorrow",
                            "Project deadline approaching",
                            "Invoice payment due",
                            "Bank statement ready",
                            "How are you doing?",
                            "Let's catch up soon",
                        ],
                        "labels": [
                            "work_business",
                            "work_business",
                            "finance_banking",
                            "finance_banking",
                            "personal_communication",
                            "personal_communication",
                        ],
                    },
                    "intent": {
                        "texts": [
                            "Please review this document",
                            "Can you help me?",
                            "Schedule a meeting",
                            "What's the status?",
                            "Thank you for your help",
                        ],
                        "labels": [
                            "request",
                            "request",
                            "informational",
                            "informational",
                            "informational",
                        ],
                    },
                    "urgency": {
                        "texts": [
                            "URGENT: Action required now",
                            "Please respond ASAP",
                            "Normal update",
                            "Take your time",
                            "No rush",
                        ],
                        "labels": ["high", "high", "low", "low", "low"],
                    },
                }

            # Train sentiment model
            if "sentiment" in training_data:
                logger.info("Training sentiment model...")
                pipeline = Pipeline(
                    [
                        ("tfidf", TfidfVectorizer(max_features=1000)),
                        ("clf", LogisticRegression(random_state=42)),
                    ]
                )
                pipeline.fit(
                    training_data["sentiment"]["texts"], training_data["sentiment"]["labels"]
                )
                model_path = os.path.join(os.path.dirname(__file__), "sentiment_model.pkl")
                joblib.dump(pipeline, model_path)
                logger.info(f"Sentiment model saved to {model_path}")

            # Train topic model
            if "topic" in training_data:
                logger.info("Training topic model...")
                pipeline = Pipeline(
                    [
                        ("tfidf", TfidfVectorizer(max_features=1000)),
                        ("clf", LogisticRegression(random_state=42)),
                    ]
                )
                pipeline.fit(training_data["topic"]["texts"], training_data["topic"]["labels"])
                model_path = os.path.join(os.path.dirname(__file__), "topic_model.pkl")
                joblib.dump(pipeline, model_path)
                logger.info(f"Topic model saved to {model_path}")

            # Train intent model
            if "intent" in training_data:
                logger.info("Training intent model...")
                pipeline = Pipeline(
                    [
                        ("tfidf", TfidfVectorizer(max_features=1000)),
                        ("clf", LogisticRegression(random_state=42)),
                    ]
                )
                pipeline.fit(training_data["intent"]["texts"], training_data["intent"]["labels"])
                model_path = os.path.join(os.path.dirname(__file__), "intent_model.pkl")
                joblib.dump(pipeline, model_path)
                logger.info(f"Intent model saved to {model_path}")

            # Train urgency model
            if "urgency" in training_data:
                logger.info("Training urgency model...")
                pipeline = Pipeline(
                    [
                        ("tfidf", TfidfVectorizer(max_features=1000)),
                        ("clf", LogisticRegression(random_state=42)),
                    ]
                )
                pipeline.fit(training_data["urgency"]["texts"], training_data["urgency"]["labels"])
                model_path = os.path.join(os.path.dirname(__file__), "urgency_model.pkl")
                joblib.dump(pipeline, model_path)
                logger.info(f"Urgency model saved to {model_path}")

            logger.info("AI model training completed successfully.")

        except Exception as e:
            logger.error(f"Error during AI model training: {e}")
            raise
