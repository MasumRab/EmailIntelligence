import logging
from typing import Any, Dict, List, Optional
from abc import ABC, abstractmethod

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

class BaseAIEngine(ABC):
    @abstractmethod
    async def analyze_email(
        self,
        subject: str,
        content: str,
        models_to_use: Dict[str, str],
        db: Optional[Any] = None,
    ) -> AIAnalysisResult:
        pass

_active_ai_engine = None

def set_active_ai_engine(engine: BaseAIEngine):
    global _active_ai_engine
    _active_ai_engine = engine

def get_active_ai_engine() -> Optional[BaseAIEngine]:
    return _active_ai_engine
