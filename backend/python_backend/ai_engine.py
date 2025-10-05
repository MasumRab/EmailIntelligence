"""
AI Engine Adapter for Python Backend.

This module provides a bridge between the FastAPI backend and the AI/NLP
services. It encapsulates the logic for analyzing email content, matching
categories, and managing the AI model's lifecycle.
"""
import logging
import os
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ..python_nlp.nlp_engine import NLPEngine

if TYPE_CHECKING:
    from .database import DatabaseManager


logger = logging.getLogger(__name__)


class AIAnalysisResult:
    """
    A wrapper for the results of an AI analysis of an email.

    This class standardizes the structure of the analysis data returned by the
    AI engine.

    Attributes:
        topic (str): The identified topic of the email.
        sentiment (str): The sentiment of the email (e.g., positive, neutral, negative).
        intent (str): The perceived intent of the email (e.g., informational, marketing).
        urgency (str): The urgency level of the email (e.g., low, medium, high).
        confidence (float): The confidence score of the analysis.
        categories (List[str]): A list of suggested categories for the email.
        keywords (List[str]): A list of extracted keywords from the email.
        reasoning (str): An explanation of how the analysis was derived.
        suggested_labels (List[str]): A list of suggested labels to apply to the email.
        risk_flags (List[str]): A list of identified risk factors.
        category_id (Optional[int]): The ID of the matched database category, if any.
    """

    def __init__(self, data: Dict[str, Any]):
        """
        Initializes the AIAnalysisResult object.

        Args:
            data (Dict[str, Any]): A dictionary containing the AI analysis data.
        """
        self.topic = data.get("topic", "unknown")
        self.sentiment = data.get("sentiment", "neutral")
        self.intent = data.get("intent", "unknown")
        self.urgency = data.get("urgency", "low")
        self.confidence = data.get("confidence", 0.0)
        self.categories = data.get("categories", [])
        self.keywords = data.get("keywords", [])
        self.reasoning = data.get("reasoning", "")
        self.suggested_labels = data.get("suggested_labels", [])
        self.risk_flags = data.get("risk_flags", [])
        self.category_id = data.get("category_id")

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the AIAnalysisResult object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the analysis result.
        """
        return {
            "topic": self.topic,
            "sentiment": self.sentiment,
            "intent": self.intent,
            "urgency": self.urgency,
            "confidence": self.confidence,
            "categories": self.categories,
            "keywords": self.keywords,
            "reasoning": self.reasoning,
            "suggested_labels": self.suggested_labels,
            "risk_flags": self.risk_flags,
            "category_id": self.category_id,
        }


class AdvancedAIEngine:
    """Optimized Advanced AI engine with async support and caching."""

    This class integrates with an NLP engine to perform analysis and includes
    methods for health checks, cleanup, and fallback mechanisms.

    Attributes:
        nlp_engine (NLPEngine): An instance of the NLP engine for text analysis.
    """

    def __init__(self):
        self.nlp_engine = NLPEngine()
        # Cache for category lookup map
        self.category_lookup_map: Dict[str, Dict[str, Any]] = {}

    def initialize(self):
        """Initialize AI engine and pre-compile patterns."""
        try:
            self.nlp_engine.initialize_patterns() # Pre-compile regex
            self.health_check()
            logger.info("AI Engine initialized successfully")
        except Exception as e:
            logger.error(f"AI Engine initialization failed: {e}")

    async def _build_category_lookup(self, db) -> None:
        """Builds a normalized lookup map for categories."""
        all_db_categories = await db.get_all_categories()
        self.category_lookup_map = {cat['name'].lower(): cat for cat in all_db_categories}
        logger.info("Built category lookup map.")

    async def _match_category_id(
        self, ai_categories: List[str], db
    ) -> Optional[int]:
        """Matches AI suggested categories to DB categories using a lookup map."""
        if not ai_categories:
            return None

        # Build the lookup map if it's empty
        if not self.category_lookup_map:
            await self._build_category_lookup(db)

        if not self.category_lookup_map:
            return None

        for ai_cat_str in ai_categories:
            ai_cat_lower = ai_cat_str.lower()
            # O(1) lookup
            if ai_cat_lower in self.category_lookup_map:
                matched_cat = self.category_lookup_map[ai_cat_lower]
                logger.info(f"Matched AI category '{ai_cat_str}' to DB category '{matched_cat['name']}' (ID: {matched_cat['id']})")
                return matched_cat['id']

        logger.info(f"No direct match for AI categories: {ai_categories} against DB categories.")
        return None

    async def analyze_email(
        self, subject: str, content: str, db: Optional["DatabaseProtocol"] = None
    ) -> AIAnalysisResult:
        """
        Analyzes the content of an email to extract insights.

        This method uses the integrated NLP engine to analyze the email's subject
        and content. If a database manager is provided, it also attempts to
        match the analysis results to a predefined category.

        Args:
            subject (str): The subject of the email.
            content (str): The body content of the email.
            db (Optional[DatabaseManager]): An optional database manager for category matching.

        Returns:
            AIAnalysisResult: An object containing the analysis results.
        """
        log_subject = subject[:50] + "..." if len(subject) > 50 else subject
        logger.info(f"Initiating AI analysis for email subject: '{log_subject}'")
        try:
            analysis_data = self.nlp_engine.analyze_email(subject, content)

            ai_categories = analysis_data.get("categories")
            if db and ai_categories:
                matched_category_id = await self._match_category_id(ai_categories, db)
                if matched_category_id:
                    analysis_data["category_id"] = matched_category_id

            if "category_id" not in analysis_data:
                analysis_data["category_id"] = None

            logger.info(
                f"Successfully received analysis from NLPEngine. "
                f"Category ID: {analysis_data.get('category_id')}"
            )
            return AIAnalysisResult(analysis_data)
        except Exception as e:
<<<<<<< HEAD
            logger.error(f"An unexpected error occurred during AI analysis: {e}", exc_info=True)
            return self._get_fallback_analysis(subject, content, f"AI analysis error: {str(e)}")


=======
            logger.error(
                f"An unexpected error occurred during AI analysis: {e}", exc_info=True
            )
            return self._get_fallback_analysis(
                subject, content, f"AI analysis error: {str(e)}"
            )
>>>>>>> origin/feature/git-history-analysis-report

    def health_check(self) -> Dict[str, Any]:
        """
        Performs a health check of the AI engine and its components.

        This method checks the availability of the underlying NLP models and
        dependencies like NLTK and scikit-learn.

        Returns:
            Dict[str, Any]: A dictionary containing the health status, including
                            available models and dependencies.
        """
        try:
            models_available = []
            if self.nlp_engine.sentiment_model:
                models_available.append("sentiment")
            if self.nlp_engine.topic_model:
                models_available.append("topic")
            if self.nlp_engine.intent_model:
                models_available.append("intent")
            if self.nlp_engine.urgency_model:
                models_available.append("urgency")

            all_models_loaded = all(
                model is not None
                for model in [
                    self.nlp_engine.sentiment_model,
                    self.nlp_engine.topic_model,
                    self.nlp_engine.intent_model,
                    self.nlp_engine.urgency_model,
                ]
            )

            nltk_available = self.nlp_engine.HAS_NLTK
            sklearn_available = self.nlp_engine.HAS_SKLEARN_AND_JOBLIB

            status = "ok"
            if not all_models_loaded:
                status = "degraded"
            if not nltk_available or not sklearn_available:
                status = "degraded"

            return {
                "status": status,
                "models_available": models_available,
                "nltk_available": nltk_available,
                "sklearn_available": sklearn_available,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(
                f"AI health check failed during direct inspection: {e}", exc_info=True
            )
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    def cleanup(self):
        """
        Cleans up resources used by the AI engine.

        This method should be called on application shutdown to remove any
        temporary files that were created.
        """
        try:
            current_dir = os.path.dirname(__file__)
            training_file_path = os.path.join(
                current_dir, "..", "python_nlp", "temp_training_data.json"
            )

            temp_files_to_check = [training_file_path]

            for temp_file in temp_files_to_check:
                if os.path.exists(temp_file):
                    try:
                        os.remove(temp_file)
                        logger.info(f"Removed temp file during cleanup: {temp_file}")
                    except OSError as e:
                        logger.error(
                            f"Error removing temp file {temp_file} "
                            f"during cleanup: {e}"
                        )

            logger.info("AI Engine cleanup completed")
        except Exception as e:
            logger.error(f"AI Engine cleanup failed: {e}")

    def _get_fallback_analysis(
        self, subject: str, content: str, error_context: Optional[str] = None
    ) -> AIAnalysisResult:
        """
        Provides a basic fallback analysis if the primary analysis fails.

        This method is used as a safeguard to ensure that some level of analysis
        is always returned, even when the primary NLP engine encounters an error.

        Args:
            subject (str): The subject of the email.
            content (str): The body content of the email.
            error_context (Optional[str]): A string describing the error that
                                           triggered the fallback.

        Returns:
            AIAnalysisResult: A basic analysis result object.
        """
        reason = "Fallback analysis due to AI service error"
        if error_context:
            reason += f": {error_context}"

        logger.warning(f"{reason}. Subject: {subject[:50]}...")

        try:
            fallback_data = self.nlp_engine._get_simple_fallback_analysis(
                subject, content
            )

            if error_context:
                fallback_data["reasoning"] = reason

            return AIAnalysisResult(
                {
                    "topic": fallback_data.get("topic", "general_communication"),
                    "sentiment": fallback_data.get("sentiment", "neutral"),
                    "intent": fallback_data.get("intent", "informational"),
                    "urgency": fallback_data.get("urgency", "low"),
                    "confidence": fallback_data.get("confidence", 0.3),
                    "categories": fallback_data.get("categories", ["general"]),
                    "keywords": fallback_data.get("keywords", []),
                    "reasoning": fallback_data.get(
                        "reasoning", "Fallback: AI service unavailable"
                    ),
                    "suggested_labels": fallback_data.get(
                        "suggested_labels", ["general"]
                    ),
                    "risk_flags": fallback_data.get(
                        "risk_flags", ["ai_analysis_failed"]
                    ),
                    "category_id": None,
                }
            )
        except Exception as e:
            logger.error(
                f"Error generating fallback analysis itself: {e}", exc_info=True
            )
            return AIAnalysisResult(
                {
                    "topic": "unknown",
                    "sentiment": "neutral",
                    "intent": "unknown",
                    "urgency": "low",
                    "confidence": 0.1,
                    "categories": ["general"],
                    "keywords": [],
                    "reasoning": f"Critical failure in AI and fallback: {e}",
                    "suggested_labels": ["general"],
                    "risk_flags": ["ai_analysis_critically_failed"],
                    "category_id": None,
                }
            )
