import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from .enhanced_error_reporting import (
    log_error, 
    ErrorSeverity, 
    ErrorCategory, 
    create_error_context
)

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


class ModernAIEngine(BaseAIEngine):
    """
    A modern implementation of the AI engine that integrates with the
    latest NLP models and provides enhanced analysis capabilities.
    
    This engine includes:
    - Sentiment analysis
    - Topic classification
    - Intent recognition
    - Urgency detection
    - Smart filtering integration
    """
    
    def __init__(self):
        self.initialized = False
        self.models_loaded = False
        logger.info("ModernAIEngine initialized")
    
    def initialize(self):
        """
        Initializes the AI engine, loading models and preparing resources.
        This method is called once when the application starts.
        """
        logger.info("Initializing ModernAIEngine...")
        try:
            # In a real implementation, this would load models
            # For now, we'll just mark as initialized
            self.initialized = True
            self.models_loaded = True
            logger.info("ModernAIEngine initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize ModernAIEngine: {e}")
            raise
    
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
        if not self.initialized:
            raise RuntimeError("ModernAIEngine not initialized")
        
        # Combine subject and content for analysis
        full_text = f"{subject} {content}"
        
        # Mock analysis results - in a real implementation, this would call actual models
        analysis_data = {
            "topic": self.classify_topic(full_text),
            "sentiment": self.analyze_sentiment(full_text),
            "intent": self.recognize_intent(full_text),
            "urgency": self.detect_urgency(full_text),
            "confidence": 0.85,
            "categories": self.suggest_categories(full_text, categories),
            "keywords": self.extract_keywords(full_text),
            "reasoning": "Analysis performed using modern NLP techniques",
            "suggested_labels": self.suggest_labels(full_text),
            "risk_flags": self.detect_risks(full_text),
        }
        
        return AIAnalysisResult(analysis_data)
    
    def classify_topic(self, text: str) -> str:
        """Classify the topic of the text."""
        # Mock implementation
        topics = ["work", "personal", "finance", "meeting", "notification", "social"]
        # Simple heuristic - in reality would use ML model
        text_lower = text.lower()
        if any(word in text_lower for word in ["meeting", "schedule", "calendar", "appointment"]):
            return "meeting"
        elif any(word in text_lower for word in ["money", "payment", "invoice", "billing", "finance"]):
            return "finance"
        elif any(word in text_lower for word in ["urgent", "asap", "immediately", "critical"]):
            return "work"
        else:
            return "personal"
    
    def analyze_sentiment(self, text: str) -> str:
        """Analyze the sentiment of the text."""
        # Mock implementation
        text_lower = text.lower()
        if any(word in text_lower for word in ["happy", "good", "great", "excellent", "wonderful", "perfect"]):
            return "positive"
        elif any(word in text_lower for word in ["angry", "bad", "terrible", "awful", "hate", "worst"]):
            return "negative"
        else:
            return "neutral"
    
    def recognize_intent(self, text: str) -> str:
        """Recognize the intent of the text."""
        # Mock implementation
        text_lower = text.lower()
        if any(word in text_lower for word in ["schedule", "meeting", "calendar", "book", "appointment"]):
            return "schedule_meeting"
        elif any(word in text_lower for word in ["reply", "respond", "answer", "re:"]):
            return "reply_needed"
        elif any(word in text_lower for word in ["question", "help", "assist", "support"]):
            return "help_request"
        else:
            return "informational"
    
    def detect_urgency(self, text: str) -> str:
        """Detect the urgency of the text."""
        # Mock implementation
        text_lower = text.lower()
        if any(word in text_lower for word in ["urgent", "asap", "immediately", "critical", "emergency"]):
            return "high"
        elif any(word in text_lower for word in ["soon", "today", "tomorrow", "deadline"]):
            return "medium"
        else:
            return "low"
    
    def suggest_categories(self, text: str, categories: Optional[List[Dict[str, Any]]] = None) -> List[str]:
        """Suggest categories for the text."""
        # Mock implementation
        categories_list = categories or []
        suggestions = []
        
        # If categories are provided, try to match
        for cat in categories_list:
            if cat.get("name", "").lower() in text.lower():
                suggestions.append(cat.get("name", ""))
        
        # If no matches found, return a default suggestion
        if not suggestions:
            suggestions = [self.classify_topic(text)]
        
        return suggestions
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from the text."""
        # Mock implementation
        import re
        # Extract words that are at least 4 characters long
        words = re.findall(r'\b\w{4,}\b', text.lower())
        # Remove common stop words and return top 5
        stop_words = {"this", "that", "with", "from", "have", "they", "were", "been", "this"}
        keywords = [word for word in words if word not in stop_words][:5]
        return keywords
    
    def suggest_labels(self, text: str) -> List[str]:
        """Suggest labels for the text."""
        # Mock implementation
        text_lower = text.lower()
        labels = []
        if "urgent" in text_lower or "asap" in text_lower:
            labels.append("urgent")
        if any(word in text_lower for word in ["meeting", "schedule", "calendar"]):
            labels.append("meeting")
        if any(word in text_lower for word in ["finance", "payment", "invoice"]):
            labels.append("finance")
        if "todo" in text_lower or "action" in text_lower:
            labels.append("action-required")
        
        return labels if labels else ["inbox"]
    
    def detect_risks(self, text: str) -> List[str]:
        """Detect potential risks in the text."""
        # Mock implementation
        text_lower = text.lower()
        risks = []
        if any(word in text_lower for word in ["malware", "virus", "phishing", "scam", "suspicious"]):
            risks.append("security-risk")
        if any(word in text_lower for word in ["password", "login", "credentials", "account"]):
            risks.append("privacy-risk")
        
        return risks
    
    def health_check(self) -> Dict[str, Any]:
        """
        Performs a health check of the AI engine and its components.

        Returns:
            A dictionary containing the health status of the engine.
        """
        return {
            "status": "healthy" if self.initialized and self.models_loaded else "unhealthy",
            "initialized": self.initialized,
            "models_loaded": self.models_loaded,
            "engine_type": "ModernAIEngine"
        }
    
    def cleanup(self):
        """
        Cleans up any resources used by the AI engine.
        This method is called on application shutdown.
        """
        logger.info("Cleaning up ModernAIEngine resources")
        self.initialized = False
        self.models_loaded = False
    
    def train_models(self, training_data: Optional[Dict[str, Any]] = None):
        """
        Trains or retrains the AI models using provided training data.
        """
        logger.info("Training ModernAIEngine models")
        # In a real implementation, this would train the models
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
