"""
Urgency analysis model.
"""

import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class UrgencyModel:
    """A basic urgency model."""

    def __init__(self, urgency_model=None):
        logger.info("UrgencyModel instance created.")
        self.model = urgency_model

    def analyze(self, text: str) -> Dict[str, Any]:
        """Analyze urgency."""
        return {"urgency": "low", "confidence": 0.0}