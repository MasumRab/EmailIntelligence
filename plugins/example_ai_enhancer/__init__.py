"""
Example AI Enhancer Plugin for EmailIntelligence.

This plugin demonstrates how to extend the platform's AI capabilities
with custom analysis, hooks, and UI enhancements.
"""

import logging
from typing import Any, Dict, List

from src.core.plugin_base import PluginInterface, PluginMetadata, PluginSecurityLevel

logger = logging.getLogger(__name__)


class ExampleAiEnhancerPlugin(PluginInterface):
    """
    Example plugin that enhances AI analysis capabilities.

    This plugin demonstrates:
    - Custom AI analysis hooks
    - Data preprocessing
    - Result enhancement
    - UI integration
    """

    def __init__(self):
        self._initialized = False
        self._config = {}
        self._enhancement_stats = {
            "emails_processed": 0,
            "enhancements_applied": 0,
            "average_confidence_boost": 0.0,
        }

    def get_metadata(self) -> PluginMetadata:
        """Return plugin metadata."""
        return PluginMetadata(
            plugin_id="example_ai_enhancer",
            name="AI Analysis Enhancer",
            version="1.0.0",
            author="EmailIntelligence Team",
            description="Enhances AI analysis with additional processing and insights",
            security_level=PluginSecurityLevel.STANDARD,
            permissions=["ai_access", "data_read"],
            tags=["ai", "enhancement", "analysis"],
        )

    async def initialize(self, config: Dict[str, Any]) -> bool:
        """Initialize the plugin with configuration."""
        try:
            self._config = config
            self._initialized = True

            # Register hooks for AI analysis enhancement
            # This would be done through the plugin manager's hook system
            logger.info("Example AI Enhancer plugin initialized")

            # Set up default configuration
            self._config.setdefault("enhance_sentiment", True)
            self._config.setdefault("add_keywords", True)
            self._config.setdefault("confidence_threshold", 0.5)

            return True

        except Exception as e:
            logger.error(f"Failed to initialize AI Enhancer plugin: {e}")
            return False

    async def shutdown(self) -> bool:
        """Shutdown the plugin and cleanup resources."""
        try:
            logger.info(
                f"AI Enhancer plugin shutdown. Stats: {self._enhancement_stats}"
            )
            self._initialized = False
            return True
        except Exception as e:
            logger.error(f"Error during AI Enhancer plugin shutdown: {e}")
            return False

    def get_capabilities(self) -> List[str]:
        """Return list of plugin capabilities."""
        return [
            "ai_analysis_enhancement",
            "sentiment_boost",
            "keyword_extraction",
            "confidence_scoring",
            "data_preprocessing",
        ]

    def get_required_permissions(self) -> List[str]:
        """Return list of required permissions."""
        return ["ai_access", "data_read"]

    async def enhance_analysis(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance an AI analysis result with additional processing."""
        if not self._initialized:
            return analysis_result

        try:
            enhanced_result = analysis_result.copy()

            # Add confidence scoring if below threshold
            confidence = analysis_result.get("confidence", 0.0)
            if confidence < self._config.get("confidence_threshold", 0.5):
                enhanced_result["confidence_boost"] = True
                enhanced_result["original_confidence"] = confidence
                enhanced_result["confidence"] = min(confidence + 0.1, 1.0)

            # Add keyword extraction if enabled
            if self._config.get("add_keywords", True):
                text = analysis_result.get("text", "")
                keywords = self._extract_keywords(text)
                if keywords:
                    enhanced_result["extracted_keywords"] = keywords

            # Add sentiment enhancement if enabled
            if self._config.get("enhance_sentiment", True):
                sentiment = analysis_result.get("sentiment", "")
                enhanced_sentiment = self._enhance_sentiment(sentiment, text)
                if enhanced_sentiment != sentiment:
                    enhanced_result["original_sentiment"] = sentiment
                    enhanced_result["enhanced_sentiment"] = enhanced_sentiment

            # Update statistics
            self._enhancement_stats["emails_processed"] += 1
            if enhanced_result != analysis_result:
                self._enhancement_stats["enhancements_applied"] += 1

            return enhanced_result

        except Exception as e:
            logger.error(f"Error enhancing analysis: {e}")
            return analysis_result

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text."""
        if not text:
            return []

        # Simple keyword extraction (could be enhanced with NLP)
        words = text.lower().split()
        stop_words = {
            "the",
            "a",
            "an",
            "and",
            "or",
            "but",
            "in",
            "on",
            "at",
            "to",
            "for",
            "of",
            "with",
            "by",
            "is",
            "are",
            "was",
            "were",
        }
        keywords = [word for word in words if len(word) > 3 and word not in stop_words]

        # Return top 5 unique keywords
        return list(set(keywords))[:5]

    def _enhance_sentiment(self, sentiment: str, text: str) -> str:
        """Enhance sentiment analysis with additional context."""
        if not text:
            return sentiment

        text_lower = text.lower()

        # Look for sentiment indicators that might have been missed
        positive_indicators = [
            "great",
            "excellent",
            "wonderful",
            "fantastic",
            "amazing",
            "love",
            "awesome",
        ]
        negative_indicators = [
            "terrible",
            "awful",
            "horrible",
            "hate",
            "worst",
            "disaster",
            "problem",
        ]

        has_positive = any(indicator in text_lower for indicator in positive_indicators)
        has_negative = any(indicator in text_lower for indicator in negative_indicators)

        # Only override if we have strong indicators and current sentiment is neutral
        if sentiment.lower() == "neutral":
            if has_positive and not has_negative:
                return "positive"
            elif has_negative and not has_positive:
                return "negative"

        return sentiment

    def get_stats(self) -> Dict[str, Any]:
        """Get plugin statistics."""
        return {
            "enhancement_stats": self._enhancement_stats.copy(),
            "configuration": self._config.copy(),
            "capabilities": self.get_capabilities(),
        }

    async def preprocess_email(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """Preprocess email data before analysis."""
        if not self._initialized:
            return email_data

        try:
            processed_data = email_data.copy()

            # Add preprocessing metadata
            processed_data["preprocessed_by"] = "example_ai_enhancer"
            processed_data["preprocessing_timestamp"] = __import__("time").time()

            # Basic text cleaning (could be enhanced)
            if "content" in processed_data:
                content = processed_data["content"]
                # Remove excessive whitespace
                content = " ".join(content.split())
                processed_data["content"] = content

            return processed_data

        except Exception as e:
            logger.error(f"Error preprocessing email: {e}")
            return email_data
