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
        if not ai_categories or not self.category_lookup_map:
            return None

        for ai_cat_str in ai_categories:
            ai_cat_lower = ai_cat_str.lower()
            if ai_cat_lower in self.category_lookup_map:
                return self.category_lookup_map[ai_cat_lower]["id"]
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
                analysis_data["category_id"] = self._match_category_id(ai_categories)

            return AIAnalysisResult(analysis_data)
        except Exception as e:
            logger.error(f"An error occurred during AI analysis: {e}", exc_info=True)
            return AIAnalysisResult(
                {"reasoning": f"AI analysis error: {e}", "risk_flags": ["ai_analysis_failed"]}
            )

    def health_check(self) -> Dict[str, Any]:
        """Performs a health check on the underlying NLP engine."""
        return self.nlp_engine.analyze_email("health check", "health check")

    def cleanup(self):
        """Cleans up resources used by the NLP engine."""
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

            if training_data is None:
                # Define sample training data
                training_data = {
                    "sentiment": {"texts": ["I love this", "This is terrible"], "labels": ["positive", "negative"]},
                    "topic": {"texts": ["Meeting tomorrow", "Invoice due"], "labels": ["work_business", "finance_banking"]},
                }

            # Train and save models
            for model_type, data in training_data.items():
                logger.info(f"Training {model_type} model...")
                pipeline = Pipeline([("tfidf", TfidfVectorizer(max_features=1000)), ("clf", LogisticRegression())])
                pipeline.fit(data["texts"], data["labels"])
                model_path = os.path.join(self.nlp_engine.model_dir, f"{model_type}_model.pkl")
                joblib.dump(pipeline, model_path)
                logger.info(f"{model_type.capitalize()} model saved to {model_path}")

            logger.info("AI model training completed successfully.")
        except Exception as e:
            logger.error(f"Error during AI model training: {e}", exc_info=True)
            raise
