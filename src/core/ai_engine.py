import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import asyncio

logger = logging.getLogger(__name__)


# Constants for AI analysis
POSITIVE_WORDS = {"good", "great", "excellent", "happy", "love", "like", "thank"}
NEGATIVE_WORDS = {"bad", "terrible", "hate", "dislike", "sorry", "problem", "issue"}

TOPIC_PATTERNS = {
    "work": {"meeting", "project", "deadline", "office", "work", "business"},
    "finance": {"payment", "invoice", "bill", "account", "money", "bank"},
    "healthcare": {"doctor", "medical", "appointment", "health", "clinic"},
    "personal": {"family", "friend", "party", "vacation", "holiday"},
    "technical": {"software", "code", "bug", "server", "database", "api"},
}

INTENT_KEYWORDS = {
    "question": {"?", "what", "how", "when", "where", "why"},
    "request": {"please", "can you", "would you", "help"},
    "apology": {"sorry", "apologize", "mistake"},
    "gratitude": {"thank", "appreciate", "grateful"},
}

URGENCY_INDICATORS = {"urgent", "asap", "emergency", "immediately", "deadline", "critical"}

STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"
}


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

    def to_dict(self) -> Dict[str, Any]:
        """Converts the analysis result to a dictionary."""
        return self.__dict__


class BaseAIEngine(ABC):
    """
    Abstract base class for all AI engines in the platform.

    This class defines the standard interface that all AI engine modules must
    implement. This ensures that different models and backends can be plugged
    into the application seamlessly.
    """

    @abstractmethod
    def initialize(self):
        """
        Initializes the AI engine, loading models and preparing resources.
        This method is called once when the application starts.
        """
        pass

    @abstractmethod
    async def analyze_email(
        self, subject: str, content: str, categories: Optional[List[Dict[str, Any]]] = None
    ) -> AIAnalysisResult:
        """
        Analyzes the content of an email to extract insights.

        Args:
            subject: The subject of the email.
            content: The body of the email.
            categories: An optional list of category dictionaries for category matching.

        Returns:
            An AIAnalysisResult object containing the analysis.
        """
        pass

    @abstractmethod
    def health_check(self) -> Dict[str, Any]:
        """
        Performs a health check of the AI engine and its components.

        Returns:
            A dictionary containing the health status of the engine.
        """
        pass

    @abstractmethod
    def cleanup(self):
        """
        Cleans up any resources used by the AI engine.
        This method is called on application shutdown.
        """
        pass

    @abstractmethod
    def train_models(self, training_data: Optional[Dict[str, Any]] = None):
        """
        Trains or retrains the AI models using provided training data.
        """
        pass


# A placeholder for the active AI engine. In a real application, this would
# be managed by a service locator or dependency injection system.
_active_ai_engine: Optional[BaseAIEngine] = None


def set_active_ai_engine(engine: BaseAIEngine):
    """Sets the active AI engine for the application."""
    global _active_ai_engine
    logger.info(f"Setting active AI engine to: {type(engine).__name__}")
    _active_ai_engine = engine


def get_active_ai_engine() -> BaseAIEngine:
    """Gets the currently active AI engine."""
    if _active_ai_engine is None:
        raise RuntimeError("No AI engine has been set as active.")
    return _active_ai_engine


class ModernAIEngine(BaseAIEngine):
    """
    Modern AI Engine implementation with advanced features.

    This implementation provides:
    - Async analysis operations
    - Model management integration
    - Comprehensive error handling
    - Performance monitoring
    """

    def __init__(self):
        self._initialized = False
        self._model_manager = None
        logger.info("ModernAIEngine initialized")

    def initialize(self):
        """Initialize the AI engine with required resources."""
        if self._initialized:
            return

        try:
            # Import here to avoid circular dependencies
            from .model_manager import ModelManager

            self._model_manager = ModelManager()
            # Note: ModelManager.discover_models() may not exist, handle gracefully
            if hasattr(self._model_manager, "discover_models"):
                self._model_manager.discover_models()

            self._initialized = True
            logger.info("ModernAIEngine fully initialized with model manager")

        except (ImportError, AttributeError, RuntimeError) as e:
            logger.error(f"Failed to initialize ModernAIEngine: {e}")
            # Continue without model manager - use fallback methods
            self._model_manager = None
            self._initialized = True
            logger.warning(
                "ModernAIEngine initialized without model manager - using fallback methods"
            )

    def health_check(self) -> Dict[str, Any]:
        """Perform a comprehensive health check of the AI engine."""
        health_status = {
            "engine": "ModernAIEngine",
            "status": "healthy" if self._initialized else "unhealthy",
            "initialized": self._initialized,
            "components": {},
            "issues": [],
        }

        # Check model manager
        if self._model_manager:
            try:
                models_info = self._model_manager.get_available_models()
                health_status["components"]["model_manager"] = {
                    "status": "healthy",
                    "models_available": len(models_info) if models_info else 0,
                }
            except (AttributeError, RuntimeError, ConnectionError) as e:
                health_status["components"]["model_manager"] = {
                    "status": "unhealthy",
                    "error": str(e),
                }
                health_status["issues"].append(f"Model manager error: {e}")
        else:
            health_status["components"]["model_manager"] = {
                "status": "unhealthy",
                "error": "Model manager not initialized",
            }
            health_status["issues"].append("Model manager not available")

        # Check if basic analysis works
        try:
            # Quick test with simple text
            test_result = asyncio.run(self.analyze_email("test", "test content"))
            health_status["components"]["analysis_engine"] = {
                "status": "healthy",
                "test_result": "passed",
            }
        except (RuntimeError, ValueError, ConnectionError) as e:
            health_status["components"]["analysis_engine"] = {
                "status": "unhealthy",
                "error": str(e),
            }
            health_status["issues"].append(f"Analysis engine error: {e}")

        # Overall status
        component_statuses = [
            comp.get("status", "unknown") for comp in health_status["components"].values()
        ]
        if "unhealthy" in component_statuses:
            health_status["status"] = "unhealthy"
        elif not self._initialized:
            health_status["status"] = "unhealthy"
        else:
            health_status["status"] = "healthy"

        return health_status

    async def analyze_email(
        self, subject: str, content: str, categories: Optional[List[Dict[str, Any]]] = None
    ) -> AIAnalysisResult:
        """Analyze an email using modern AI techniques."""
        if not self._initialized:
            raise RuntimeError("AI Engine not initialized")

        try:
            # Combine subject and content for analysis
            full_text = f"{subject} {content}"

            # Perform analysis using available models
            sentiment = await self._analyze_sentiment(full_text)
            topics = await self._analyze_topics(full_text)
            intent = await self._analyze_intent(full_text)
            urgency = await self._analyze_urgency(full_text)

            # Generate comprehensive result
            result_data = {
                "sentiment": sentiment.get("label", "neutral") if sentiment else "neutral",
                "topic": topics[0] if topics else "general",
                "intent": intent.get("type", "unknown") if intent else "unknown",
                "urgency": urgency.get("level", "low") if urgency else "low",
                "confidence": self._calculate_overall_confidence(
                    sentiment, topics, intent, urgency
                ),
                "categories": topics if topics else [],
                "keywords": self._extract_keywords(full_text),
                "reasoning": "Analysis performed using ModernAIEngine with integrated model management",
                "suggested_labels": self._generate_suggested_labels(
                    sentiment, topics, intent, urgency
                ),
                "risk_flags": self._assess_risks(sentiment, urgency),
            }

            return AIAnalysisResult(result_data)

        except Exception as e:
            logger.error(f"Error analyzing email: {e}")
            # Return minimal result on error
            return AIAnalysisResult(
                {
                    "sentiment": "neutral",
                    "topic": "unknown",
                    "intent": "unknown",
                    "urgency": "low",
                    "confidence": 0.0,
                    "reasoning": f"Analysis failed: {str(e)}",
                }
            )

    async def _analyze_sentiment(self, text: str) -> Optional[Dict[str, Any]]:
        """Analyze sentiment using available models."""
        try:
            # Try to use sentiment model from model manager
            if self._model_manager and hasattr(self._model_manager, "get_sentiment_model"):
                model = self._model_manager.get_sentiment_model()
                if model:
                    return await model.analyze(text)
        except Exception as e:
            logger.debug(f"Sentiment model analysis failed: {e}")

        # Fallback to simple keyword-based analysis
        return self._simple_sentiment_analysis(text)

    async def _analyze_topics(self, text: str) -> List[str]:
        """Analyze topics using available models."""
        try:
            if self._model_manager and hasattr(self._model_manager, "get_topic_model"):
                model = self._model_manager.get_topic_model()
                if model:
                    result = await model.analyze(text)
                    return result.get("topics", [])
        except Exception as e:
            logger.debug(f"Topic model analysis failed: {e}")

        # Fallback to rule-based topic detection
        return self._rule_based_topics(text)

    async def _analyze_intent(self, text: str) -> Optional[Dict[str, Any]]:
        """Analyze intent using available models."""
        try:
            if self._model_manager and hasattr(self._model_manager, "get_intent_model"):
                model = self._model_manager.get_intent_model()
                if model:
                    return await model.analyze(text)
        except Exception as e:
            logger.debug(f"Intent model analysis failed: {e}")

        return self._simple_intent_analysis(text)

    async def _analyze_urgency(self, text: str) -> Optional[Dict[str, Any]]:
        """Analyze urgency using available models."""
        try:
            if self._model_manager and hasattr(self._model_manager, "get_urgency_model"):
                model = self._model_manager.get_urgency_model()
                if model:
                    return await model.analyze(text)
        except Exception as e:
            logger.debug(f"Urgency model analysis failed: {e}")

        return self._simple_urgency_analysis(text)

    def _simple_sentiment_analysis(self, text: str) -> Dict[str, Any]:
        """Simple keyword-based sentiment analysis."""
        text_lower = text.lower()
        positive_count = sum(1 for word in POSITIVE_WORDS if word in text_lower)
        negative_count = sum(1 for word in NEGATIVE_WORDS if word in text_lower)

        if positive_count > negative_count:
            sentiment = "positive"
        elif negative_count > positive_count:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        return {"label": sentiment, "confidence": 0.5}

    def _rule_based_topics(self, text: str) -> List[str]:
        """Rule-based topic detection."""
        text_lower = text.lower()
        topics = []

        for topic, keywords in TOPIC_PATTERNS.items():
            if any(keyword in text_lower for keyword in keywords):
                topics.append(topic)

        return topics[:3] if topics else ["general"]

    def _simple_intent_analysis(self, text: str) -> Dict[str, Any]:
        """Simple intent analysis based on keywords."""
        text_lower = text.lower()

        if any(word in text_lower for word in INTENT_KEYWORDS["question"]):
            intent_type = "question"
        elif any(word in text_lower for word in INTENT_KEYWORDS["request"]):
            intent_type = "request"
        elif any(word in text_lower for word in INTENT_KEYWORDS["apology"]):
            intent_type = "apology"
        elif any(word in text_lower for word in INTENT_KEYWORDS["gratitude"]):
            intent_type = "gratitude"
        else:
            intent_type = "information"

        return {"type": intent_type, "confidence": 0.6}

    def _simple_urgency_analysis(self, text: str) -> Dict[str, Any]:
        """Simple urgency analysis."""
        text_lower = text.lower()

        has_urgency = any(indicator in text_lower for indicator in URGENCY_INDICATORS)

        return {
            "level": "high" if has_urgency else "low",
            "confidence": 0.7 if has_urgency else 0.5,
        }

    def _calculate_overall_confidence(self, sentiment, topics, intent, urgency) -> float:
        """Calculate overall confidence score."""
        confidences = []
        if sentiment and "confidence" in sentiment:
            confidences.append(sentiment["confidence"])
        if intent and "confidence" in intent:
            confidences.append(intent["confidence"])
        if urgency and "confidence" in urgency:
            confidences.append(urgency["confidence"])

        return sum(confidences) / len(confidences) if confidences else 0.5

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text."""
        # Simple keyword extraction - could be enhanced with NLP
        words = text.lower().split()

        keywords = [word for word in words if len(word) > 3 and word not in STOP_WORDS]
        return list(set(keywords))[:10]  # Return unique keywords, max 10

    def _generate_suggested_labels(self, sentiment, topics, intent, urgency) -> List[str]:
        """Generate suggested labels based on analysis."""
        labels = []

        # Add sentiment-based labels
        if sentiment and sentiment.get("label") != "neutral":
            labels.append(f"sentiment:{sentiment['label']}")

        # Add topic-based labels
        if topics:
            labels.extend(f"topic:{topic}" for topic in topics[:2])

        # Add intent-based labels
        if intent and intent.get("type"):
            labels.append(f"intent:{intent['type']}")

        # Add urgency-based labels
        if urgency and urgency.get("level") == "high":
            labels.append("urgent")

        return labels

    def _assess_risks(self, sentiment, urgency) -> List[str]:
        """Assess potential risks based on analysis."""
        risks = []

        if sentiment and sentiment.get("label") == "negative":
            risks.append("negative_sentiment")

        if urgency and urgency.get("level") == "high":
            risks.append("high_urgency")

        return risks

    def cleanup(self):
        """Clean up resources."""
        if self._model_manager:
            # Cleanup model manager if needed
            pass
        logger.info("ModernAIEngine cleanup completed")

    def train_models(self, training_data: Optional[Dict[str, Any]] = None):
        """Train or retrain AI models."""
        # Implementation for model training
        logger.info("Model training requested but not yet implemented")
        pass
