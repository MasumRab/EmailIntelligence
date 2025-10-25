import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

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
