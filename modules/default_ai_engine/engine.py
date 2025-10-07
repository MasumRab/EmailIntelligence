import logging
from typing import Any, Dict, List, Optional

# Core framework components
from src.core.ai_engine import BaseAIEngine, AIAnalysisResult
from src.core.database import DatabaseManager

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

    async def _build_category_lookup(self, db: "DatabaseManager") -> None:
        """Builds a normalized lookup map for categories from the database."""
        all_db_categories = await db.get_all_categories()
        self.category_lookup_map = {cat["name"].lower(): cat for cat in all_db_categories}
        logger.info("Built category lookup map for the default AI engine.")

    async def _match_category_id(
        self, ai_categories: List[str], db: "DatabaseManager"
    ) -> Optional[int]:
        """Matches AI-suggested categories to database categories."""
        if not ai_categories:
            return None

        if not self.category_lookup_map:
            await self._build_category_lookup(db)

        if not self.category_lookup_map:
            return None

        for ai_cat_str in ai_categories:
            ai_cat_lower = ai_cat_str.lower()
            if ai_cat_lower in self.category_lookup_map:
                matched_cat = self.category_lookup_map[ai_cat_lower]
                return matched_cat["id"]
        return None

    async def analyze_email(
        self, subject: str, content: str, db: Optional[DatabaseManager] = None
    ) -> AIAnalysisResult:
        """Analyzes email content and returns a standardized analysis result."""
        try:
            analysis_data = self.nlp_engine.analyze_email(subject, content)

            if db:
                ai_categories = analysis_data.get("categories", [])
                matched_category_id = await self._match_category_id(ai_categories, db)
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
