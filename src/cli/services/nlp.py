"""
NLP Service Module
"""

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

class NLPService:
    """
    Service for providing natural language processing capabilities.
    """

    def __init__(self):
        self._engine = None
        self._initialized = False

    def is_available(self) -> bool:
        try:
            import transformers
            import nltk
            return True
        except ImportError:
            return False

    def get_engine(self) -> Any:
        if not self._initialized:
            self._initialize_engine()
        return self._engine

    def _initialize_engine(self):
        try:
            from src.backend.python_nlp.nlp_engine import NLPEngine
            self._engine = NLPEngine()
            self._initialized = True
        except ImportError:
            self._engine = None
            self._initialized = True

    async def analyze_text(self, text: str) -> Dict[str, Any]:
        engine = self.get_engine()
        if engine:
            return engine.analyze(text)
        return {"length": len(text), "status": "basic_fallback"}
