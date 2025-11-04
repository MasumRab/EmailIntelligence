"""
Refactored AI Engine for Email Intelligence Platform
"""

import asyncio
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from .model_provider import (
    BaseModelProvider, 
    get_active_provider,
    register_provider,
    RuleBasedModelProvider
)
from .dynamic_model_provider import DynamicModelProvider
from ..dynamic_model_manager import DynamicModelManager
from ..performance_monitor import log_performance

logger = logging.getLogger(__name__)


class AIAnalysisResult:
    """
    A standardized data structure for the results of an AI email analysis.
    This ensures that all AI engines, regardless of their implementation,
    return data in a consistent format.
    """

    def __init__(self, data: Dict[str, Any]):
        self.topic: str = data.get("topic", "unknown")
        self.sentiment: str = data.get("sentiment", "neutral")
        self.intent: str = data.get("intent", "unknown")
        self.urgency: str = data.get("urgency", "low")
        self.confidence: float = data.get("confidence", 0.0)
        self.categories: List[str] = data.get("categories", [])
        self.keywords: List[str] = data.get("keywords", [])
        self.reasoning: str = data.get("reasoning", "")
        self.suggested_labels: List[str] = data.get("suggested_labels", [])
        self.risk_flags: List[str] = data.get("risk_flags", [])
        self.category_id: Optional[int] = data.get("category_id")
        self.model_used: str = data.get("model_used", "unknown")
        self.processing_time: float = data.get("processing_time", 0.0)

    def to_dict(self) -> Dict[str, Any]:
        """Converts the analysis result to a dictionary."""
        return self.__dict__


class AdvancedAIEngine:
    """
    Advanced AI Engine with pluggable model providers and enhanced features.

    This engine provides:
    - Pluggable model providers (rule-based, transformer-based, etc.)
    - Async analysis operations
    - Model management integration
    - Comprehensive error handling
    - Performance monitoring
    """

    def __init__(self, model_manager: Optional[DynamicModelManager] = None):
        self._model_manager = model_manager
        self._initialized = False
        self._active_provider: Optional[BaseModelProvider] = None
        logger.info("AdvancedAIEngine initialized")

    async def initialize(self):
        """
        Initialize the AI engine with required resources and providers.
        """
        if self._initialized:
            return

        try:
            # Register the rule-based provider as default
            rule_provider = RuleBasedModelProvider()
            register_provider("rule_based", rule_provider)
            
            # If a model manager is provided, register the dynamic model provider
            if self._model_manager:
                dynamic_provider = DynamicModelProvider(self._model_manager)
                await dynamic_provider.initialize()
                register_provider("dynamic", dynamic_provider)
                
                # Set the dynamic provider as active if available
                from .model_provider import set_active_provider
                set_active_provider("dynamic")
            else:
                # Default to rule-based provider
                from .model_provider import set_active_provider
                set_active_provider("rule_based")
            
            self._initialized = True
            logger.info("AdvancedAIEngine fully initialized with model providers")
            
        except Exception as e:
            logger.error(f"Failed to initialize AdvancedAIEngine: {e}")
            # Continue with basic functionality
            self._initialized = True
            logger.warning("AdvancedAIEngine initialized with basic functionality")

    def get_active_provider(self) -> Optional[BaseModelProvider]:
        """
        Get the currently active model provider.
        
        Returns:
            The active model provider or None if not initialized
        """
        if not self._initialized:
            raise RuntimeError("AI Engine not initialized")
        
        return get_active_provider()

    @log_performance(operation="analyze_email")
    async def analyze_email(
        self, subject: str, content: str, categories: Optional[List[Dict[str, Any]]] = None
    ) -> AIAnalysisResult:
        """
        Analyze the content of an email to extract insights.

        Args:
            subject: The subject of the email.
            content: The body of the email.
            categories: An optional list of category dictionaries for category matching.

        Returns:
            An AIAnalysisResult object containing the analysis.
        """
        if not self._initialized:
            raise RuntimeError("AI Engine not initialized")

        try:
            # Combine subject and content for analysis
            full_text = f"{subject} {content}"

            # Get the active provider
            provider = self.get_active_provider()
            if not provider:
                raise RuntimeError("No active model provider available")

            # Perform analysis using the provider
            sentiment_task = provider.analyze_sentiment(full_text)
            topic_task = provider.analyze_topics(full_text)
            intent_task = provider.analyze_intent(full_text)
            urgency_task = provider.analyze_urgency(full_text)

            # Run all analysis tasks concurrently
            sentiment_result, topic_result, intent_result, urgency_result = await asyncio.gather(
                sentiment_task, topic_task, intent_task, urgency_task
            )

            # Calculate overall confidence as average of component confidences
            confidences = [
                sentiment_result.get("confidence", 0.5),
                topic_result.get("topic_confidences", {}).get(topic_result.get("topics", [""])[0], 0.5) if topic_result.get("topics") else 0.5,
                intent_result.get("confidence", 0.5),
                urgency_result.get("confidence", 0.5)
            ]
            overall_confidence = sum(confidences) / len(confidences)

            # Extract topics (take first topic if available)
            topics = topic_result.get("topics", [])
            main_topic = topics[0] if topics else "general"

            # Generate comprehensive result
            result_data = {
                "sentiment": sentiment_result.get("sentiment", "neutral"),
                "topic": main_topic,
                "intent": intent_result.get("intent", "unknown"),
                "urgency": urgency_result.get("urgency", "low"),
                "confidence": overall_confidence,
                "categories": topics,
                "keywords": self._extract_keywords(full_text),
                "reasoning": (
                    f"Analysis performed using {type(provider).__name__} with "
                    f"sentiment: {sentiment_result.get('method_used', 'unknown')}, "
                    f"topic: {topic_result.get('method_used', 'unknown')}, "
                    f"intent: {intent_result.get('method_used', 'unknown')}, "
                    f"urgency: {urgency_result.get('method_used', 'unknown')}"
                ),
                "suggested_labels": self._generate_suggested_labels(
                    sentiment_result, topic_result, intent_result, urgency_result
                ),
                "risk_flags": self._assess_risks(sentiment_result, urgency_result),
                "model_used": f"{type(provider).__name__}",
                "processing_time": max(
                    sentiment_result.get("processing_time", 0),
                    topic_result.get("processing_time", 0),
                    intent_result.get("processing_time", 0),
                    urgency_result.get("processing_time", 0)
                )
            }

            return AIAnalysisResult(result_data)

        except Exception as e:
            logger.error(f"Error analyzing email: {e}")
            # Return minimal result on error
            return AIAnalysisResult({
                "sentiment": "neutral",
                "topic": "unknown",
                "intent": "unknown",
                "urgency": "low",
                "confidence": 0.0,
                "reasoning": f"Analysis failed: {str(e)}",
                "model_used": "error_fallback",
                "processing_time": 0.0
            })

    def _extract_keywords(self, text: str) -> List[str]:
        """
        Extract important keywords from text.
        """
        # Simple keyword extraction - could be enhanced with NLP
        words = text.lower().split()
        # Filter out common stop words and short words
        stop_words = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", 
            "to", "for", "of", "with", "by", "is", "are", "was", 
            "were", "be", "been", "being", "have", "has", "had", 
            "do", "does", "did", "will", "would", "could", "should"
        }
        keywords = [word for word in words if len(word) > 3 and word not in stop_words]
        return list(set(keywords))[:10]  # Return unique keywords, max 10

    def _generate_suggested_labels(self, sentiment, topics, intent, urgency) -> List[str]:
        """
        Generate suggested labels based on analysis.
        """
        labels = []

        # Add sentiment-based labels
        sentiment_label = sentiment.get("sentiment")
        if sentiment_label and sentiment_label != "neutral":
            labels.append(f"sentiment:{sentiment_label}")

        # Add topic-based labels
        topic_list = topics.get("topics", [])
        for topic in topic_list[:2]:  # Limit to first 2 topics
            labels.append(f"topic:{topic}")

        # Add intent-based labels
        intent_type = intent.get("intent")
        if intent_type:
            labels.append(f"intent:{intent_type}")

        # Add urgency-based labels
        urgency_level = urgency.get("urgency")
        if urgency_level == "high":
            labels.append("urgent")

        return labels

    def _assess_risks(self, sentiment, urgency) -> List[str]:
        """
        Assess potential risks based on analysis.
        """
        risks = []

        sentiment_label = sentiment.get("sentiment")
        if sentiment_label == "negative":
            risks.append("negative_sentiment")

        urgency_level = urgency.get("urgency")
        if urgency_level == "high":
            risks.append("high_urgency")

        return risks

    async def health_check(self) -> Dict[str, Any]:
        """
        Perform a comprehensive health check of the AI engine.
        """
        health_status = {
            "engine": "AdvancedAIEngine",
            "status": "healthy" if self._initialized else "unhealthy",
            "initialized": self._initialized,
            "components": {},
            "issues": [],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        # Check provider availability
        try:
            providers = await asyncio.get_event_loop().run_in_executor(
                None, lambda: __import__('src.core.ai.model_provider', fromlist=['list_providers']).list_providers()
            )
            health_status["components"]["model_providers"] = {
                "status": "healthy",
                "providers_available": len(providers),
                "provider_names": providers
            }
        except Exception as e:
            health_status["components"]["model_providers"] = {
                "status": "unhealthy",
                "error": str(e),
            }
            health_status["issues"].append(f"Model provider registry error: {e}")

        # Check active provider
        try:
            active_provider = self.get_active_provider()
            if active_provider:
                provider_health = await active_provider.health_check()
                health_status["components"]["active_provider"] = provider_health
            else:
                health_status["components"]["active_provider"] = {
                    "status": "unhealthy",
                    "error": "No active provider"
                }
                health_status["issues"].append("No active provider")
        except Exception as e:
            health_status["components"]["active_provider"] = {
                "status": "unhealthy",
                "error": str(e),
            }
            health_status["issues"].append(f"Active provider error: {e}")

        # Check if basic analysis works
        try:
            # Quick test with simple text
            test_result = await self.analyze_email("test", "test content")
            health_status["components"]["analysis_engine"] = {
                "status": "healthy",
                "test_result": "passed",
                "model_used": test_result.model_used
            }
        except Exception as e:
            health_status["components"]["analysis_engine"] = {
                "status": "unhealthy",
                "error": str(e),
            }
            health_status["issues"].append(f"Analysis engine error: {e}")

        # Overall status
        component_statuses = [
            comp.get("status", "unknown") 
            for comp in health_status["components"].values() 
            if isinstance(comp, dict) and "status" in comp
        ]
        if "unhealthy" in component_statuses:
            health_status["status"] = "unhealthy"
        elif not self._initialized:
            health_status["status"] = "unhealthy"
        else:
            health_status["status"] = "healthy"

        return health_status

    def cleanup(self):
        """
        Clean up resources.
        """
        logger.info("AdvancedAIEngine cleanup completed")


# Global AI engine instance
_ai_engine_instance = None


async def get_ai_engine(model_manager: Optional[DynamicModelManager] = None) -> AdvancedAIEngine:
    """
    Get the singleton instance of the AdvancedAIEngine.
    """
    global _ai_engine_instance
    if _ai_engine_instance is None:
        _ai_engine_instance = AdvancedAIEngine(model_manager)
        await _ai_engine_instance.initialize()
    return _ai_engine_instance


def get_active_ai_engine() -> AdvancedAIEngine:
    """
    Get the currently active AI engine instance.
    """
    if _ai_engine_instance is None:
        raise RuntimeError("AI Engine has not been initialized.")
    return _ai_engine_instance