"""
AI Engine Adapter for Python Backend
Bridges FastAPI backend with existing AI/NLP services
"""

import asyncio
import json
import logging
# import sys # No longer needed for subprocess
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

# from .utils.async_utils import _execute_async_command # Commented out
from server.python_nlp.nlp_engine import NLPEngine  # Changed import alias

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
        self.action_items = data.get("action_items", [])  # Added action_items

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
            "action_items": self.action_items,  # Added action_items
        }


class AdvancedAIEngine:
    """Advanced AI engine with async support"""

    def __init__(self):
        # Removed: self.python_nlp_path, self.ai_training_script, self.nlp_service_script
        # Instantiate the NLP engine for fallback analysis
        self.nlp_engine = NLPEngine()  # Renamed from self.fallback_nlp_engine
        # DatabaseManager instance will be passed if needed for category matching
        # Or use FastAPI's Depends if AIEngine methods become FastAPI path operations directly

    def initialize(self):  # Changed to synchronous
        """Initialize AI engine"""
        try:
            # Test connection to NLP services
            self.health_check()  # Changed to synchronous call
            logger.info("AI Engine initialized successfully")
        except Exception as e:
            logger.error(f"AI Engine initialization failed: {e}")

    async def _match_category_id(
        self, ai_categories: List[str], db: "DatabaseManager"
    ) -> Optional[int]:
        """Matches AI suggested category strings to database categories."""
        if not ai_categories:
            return None

        # This import is problematic for circular deps if DatabaseManager imports AIEngine.
        # Consider moving DatabaseManager to a more common place or restructuring.
        # For now, assuming DatabaseManager can be imported or passed.
        # from .database import DatabaseManager # This would be circular if DB imports AIEngine

        try:
            all_db_categories = (
                await db.get_all_categories()
            )  # db.get_all_categories() was adapted from get_categories
            if not all_db_categories:
                return None

            for ai_cat_str in ai_categories:
                for db_cat in all_db_categories:
                    # Simple case-insensitive matching (can be improved)
                    if (
                        db_cat["name"].lower() in ai_cat_str.lower()
                        or ai_cat_str.lower() in db_cat["name"].lower()
                    ):
                        logger.info(
                            f"Matched AI category '{ai_cat_str}' to DB category '{db_cat['name']}' (ID: {db_cat['id']})"
                        )
                        return db_cat["id"]
            logger.info(
                f"No direct match found for AI categories: {ai_categories} against DB categories."
            )
        except Exception as e:
            logger.error(f"Error during category matching: {e}", exc_info=True)
        return None

    async def analyze_email(
        self, subject: str, content: str, db: Optional["DatabaseManager"] = None
    ) -> AIAnalysisResult:  # Added db param
        """Analyze email content with AI, including matching to DB categories if db is provided."""
        logger.info(
            f"Initiating AI analysis for email with subject: '{subject[:50]}...'"
        )
        try:
            analysis_data = self.nlp_engine.analyze_email(subject, content)

            if "action_items" not in analysis_data:  # Should be present from NLPEngine
                analysis_data["action_items"] = []

            # If a DatabaseManager instance is provided, attempt to match category_id
            if db and analysis_data.get("categories"):
                matched_category_id = await self._match_category_id(
                    analysis_data["categories"], db
                )
                if matched_category_id:
                    analysis_data["category_id"] = matched_category_id
                else:
                    # Ensure category_id is None if no match, or keep NLPEngine's default if any
                    analysis_data["category_id"] = analysis_data.get(
                        "category_id"
                    )  # Keep if NLPEngine set it, else None

            logger.info(
                f"Successfully received analysis from NLPEngine. Category ID: {analysis_data.get('category_id')}"
            )
            return AIAnalysisResult(analysis_data)
        except Exception as e:
            logger.error(
                f"An unexpected error occurred during AI analysis: {e}", exc_info=True
            )
            return self._get_fallback_analysis(
                subject, content, f"AI analysis error: {str(e)}"
            )

    def train_models(
        self, training_emails: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:  # Changed to synchronous
        """Train AI models with email data - Currently not functional with direct NLPEngine integration."""
        logger.warning(
            "train_models is not currently functional with direct NLPEngine integration. The ai_training.py script logic needs to be integrated into NLPEngine."
        )

        # Path might need adjustment if os.path.dirname(__file__) is not appropriate in all contexts
        # Assuming this file remains in server/python_backend/
        training_file_path = os.path.join(
            os.path.dirname(__file__), "..", "python_nlp", "temp_training_data.json"
        )

        # Create dummy training_data.json if training_emails provided, to simulate old behavior for cleanup test
        if training_emails:
            try:
                with open(training_file_path, "w") as f:
                    json.dump(training_emails, f)
            except IOError as e:
                logger.error(
                    f"Error creating temporary training file {training_file_path}: {e}"
                )

        # Cleanup temporary file if created (or if it exists from a previous run)
        if os.path.exists(training_file_path):
            try:
                os.remove(training_file_path)
                logger.info(f"Removed temporary training file: {training_file_path}")
            except OSError as e:
                logger.error(
                    f"Error removing temporary training file {training_file_path}: {e}"
                )

        return {
            "success": False,
            "error": "Model training via direct NLPEngine call is not implemented. Requires ai_training.py logic integration.",
            "modelsTrained": [],
            "trainingAccuracy": {},
            "validationAccuracy": {},
            "trainingTime": 0,
            "emailsProcessed": len(training_emails) if training_emails else 0,
        }

    def health_check(self) -> Dict[str, Any]:  # Changed to synchronous
        """Check AI engine health by inspecting the NLPEngine instance."""
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

            # Accessing HAS_NLTK and HAS_SKLEARN_AND_JOBLIB from nlp_engine instance
            # These are class attributes in NLPEngine, so they are accessible via instance.
            nltk_available = self.nlp_engine.HAS_NLTK
            sklearn_available = self.nlp_engine.HAS_SKLEARN_AND_JOBLIB

            status = "ok"
            if not all_models_loaded:
                status = "degraded"
            if not nltk_available or not sklearn_available:
                status = "degraded"  # Or "unhealthy" depending on severity

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

    def cleanup(self):  # Changed to synchronous (was async but did sync operations)
        """Cleanup AI engine resources"""
        try:
            # Cleanup any temporary files or resources
            # Path might need adjustment if os.path.dirname(__file__) is not appropriate in all contexts
            training_file_path = os.path.join(
                os.path.dirname(__file__), "..", "python_nlp", "temp_training_data.json"
            )

            temp_files_to_check = [training_file_path]  # Add other temp files if any

            for temp_file in temp_files_to_check:
                if os.path.exists(temp_file):
                    try:
                        os.remove(temp_file)
                        logger.info(
                            f"Removed temporary file during cleanup: {temp_file}"
                        )
                    except OSError as e:
                        logger.error(
                            f"Error removing temporary file {temp_file} during cleanup: {e}"
                        )

            logger.info("AI Engine cleanup completed")
        except Exception as e:
            logger.error(f"AI Engine cleanup failed: {e}")

    def _get_fallback_analysis(
        self, subject: str, content: str, error_context: Optional[str] = None
    ) -> AIAnalysisResult:
        """
        Provides a basic fallback analysis if the primary NLPEngine script fails or returns an error.
        This uses the in-memory NLPEngine instance.
        """
        reason = "Fallback analysis due to AI service error"
        if error_context:
            reason += f": {error_context}"

        logger.warning(f"{reason}. Subject: {subject[:50]}...")

        try:
            # Use the _get_simple_fallback_analysis from the NLPEngine instance
            # This method provides: topic, sentiment, intent (default), urgency,
            # confidence (default), categories, keywords (empty), reasoning.
            fallback_data = self.nlp_engine._get_simple_fallback_analysis(
                subject, content
            )  # Use self.nlp_engine

            # Override reasoning if a specific error context was provided
            if error_context:
                fallback_data["reasoning"] = reason

            # Adapt the result to AIAnalysisResult structure.
            # Most fields should align or have sensible defaults from _get_simple_fallback_analysis.
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
                        "reasoning", "Fallback analysis - AI service unavailable"
                    ),
                    "suggested_labels": fallback_data.get(
                        "suggested_labels", ["general"]
                    ),
                    "risk_flags": fallback_data.get(
                        "risk_flags", ["ai_analysis_failed"]
                    ),
                    "category_id": None,
                    "action_items": [],  # Ensure action_items is in the fallback
                }
            )
        except Exception as e:
            logger.error(
                f"Error generating fallback analysis itself: {e}", exc_info=True
            )
            # If even the fallback engine fails, return a very minimal structure
            return AIAnalysisResult(
                {
                    "topic": "unknown",
                    "sentiment": "neutral",
                    "intent": "unknown",
                    "urgency": "low",
                    "confidence": 0.1,
                    "categories": ["general"],
                    "keywords": [],
                    "reasoning": f"Critical failure in AI analysis and fallback: {e}",
                    "suggested_labels": ["general"],
                    "risk_flags": ["ai_analysis_critically_failed"],
                    "category_id": None,
                    "action_items": [],  # Ensure action_items is in the critical fallback
                }
            )
