"""
Intent analysis model.
"""

import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class IntentModel:
    """A basic intent model."""

    def __init__(self, intent_model=None):
        logger.info("IntentModel instance created.")
        self.model = intent_model

    def analyze(self, text: str) -> Dict[str, Any]:
        """Analyze intent."""
        return {"intent": "unknown", "confidence": 0.0}