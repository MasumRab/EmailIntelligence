"""
It will be removed in a future release.

AI Engine Adapter for Python Backend
Bridges FastAPI backend with existing AI/NLP services
"""

import logging
import os
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional

if TYPE_CHECKING:
    from .database import DatabaseManager

from .model_manager import ModelManager

logger = logging.getLogger(__name__)


class AIAnalysisResult:
    """AI analysis result wrapper"""

    def __init__(self, data: Dict[str, Any]):
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
    """Optimized Advanced AI engine that uses a model manager for dynamic model loading."""

    def __init__(self, model_manager: ModelManager):
        self.model_manager = model_manager
        self.category_lookup_map: Dict[str, Dict[str, Any]] = {}

    def initialize(self):
        """Initialize AI engine."""
        try:
            self.health_check()
            logger.info("AI Engine initialized successfully")
        except Exception as e:
            logger.error(f"AI Engine initialization failed: {e}")

    async def _build_category_lookup(self, db) -> None:
        """Builds a normalized lookup map for categories."""
        all_db_categories = await db.get_all_categories()
        self.category_lookup_map = {cat["name"].lower(): cat for cat in all_db_categories}
        logger.info("Built category lookup map.")

    async def _match_category_id(self, ai_categories: List[str], db) -> Optional[int]:
        """Matches AI suggested categories to DB categories using a lookup map."""
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
                logger.info(
                    f"Matched AI category '{ai_cat_str}' to DB category '{matched_cat['name']}' (ID: {matched_cat['id']})"
                )
                return matched_cat["id"]

        logger.info(f"No direct match for AI categories: {ai_categories} against DB categories.")
        return None

    async def analyze_email(
        self,
        subject: str,
        content: str,
        models_to_use: Dict[str, str],
        db: Optional["DatabaseManager"] = None,
    ) -> AIAnalysisResult:
        """Analyze email content with AI using a dynamic set of models specified by the workflow."""
        log_subject = subject[:50] + "..." if len(subject) > 50 else subject
        logger.info(f"Initiating AI analysis for email subject: '{log_subject}'")

        try:
            # 1. Get active models from ModelManager based on the workflow's configuration
            sentiment_model_name = models_to_use.get("sentiment")
            topic_model_name = models_to_use.get("topic")

            if not sentiment_model_name or not topic_model_name:
                raise ValueError(
                    "Workflow configuration must specify 'sentiment' and 'topic' models."
                )

            sentiment_model = self.model_manager.get_model(sentiment_model_name)
            topic_model = self.model_manager.get_model(topic_model_name)

            # 2. Perform analysis using the loaded models
            full_text = f"{subject}\n{content}"
            sentiment_result = sentiment_model.analyze(full_text)
            topic_result = topic_model.analyze(full_text)

            # 3. Combine results
            analysis_data = {
                "topic": topic_result.get("topic", "unknown"),
                "sentiment": sentiment_result.get("sentiment", "neutral"),
                "intent": "informational",  # Placeholder
                "urgency": "low",  # Placeholder
                "confidence": (
                    sentiment_result.get("confidence", 0.5) + topic_result.get("confidence", 0.5)
                )
                / 2,
                "categories": [
                    topic_result.get("topic", "unknown")
                ],  # Use topic as category for now
                "keywords": [],  # Placeholder
                "reasoning": f"Sentiment model: {sentiment_model_name} ({sentiment_result.get('method_used')}), Topic model: {topic_model_name} ({topic_result.get('method_used')})",
                "suggested_labels": [
                    topic_result.get("topic", "unknown").lower().replace(" ", "_")
                ],
                "risk_flags": [],
            }

            # 4. Match categories to database
            ai_categories = analysis_data.get("categories")
            if db and ai_categories:
                matched_category_id = await self._match_category_id(ai_categories, db)
                analysis_data["category_id"] = matched_category_id
            else:
                analysis_data["category_id"] = None

            logger.info(f"Analysis complete. Category ID: {analysis_data.get('category_id')}")
            return AIAnalysisResult(analysis_data)

        except Exception as e:
            logger.error(f"An unexpected error occurred during AI analysis: {e}", exc_info=True)
            return AIAnalysisResult({"reasoning": f"Critical failure in AI engine: {e}"})

    def health_check(self) -> Dict[str, Any]:
        """Check AI engine health by inspecting the ModelManager."""
        try:
            all_models = self.model_manager.list_models()
            loaded_models = [m for m in all_models if m.get("status") == "loaded"]

            status = "ok" if loaded_models else "degraded"

            return {
                "status": status,
                "total_models": len(all_models),
                "loaded_models": len(loaded_models),
                "loaded_model_names": [m["name"] for m in loaded_models],
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"AI health check failed: {e}", exc_info=True)
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    def cleanup(self):
        """Cleanup AI engine resources (e.g., unload models)."""
        logger.info("Cleaning up AI Engine resources...")
        for model_meta in self.model_manager.list_models():
            if model_meta.get("status") == "loaded":
                self.model_manager.unload_model(model_meta["name"])
        logger.info("AI Engine cleanup completed.")
