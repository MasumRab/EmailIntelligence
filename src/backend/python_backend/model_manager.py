"""Model manager module."""

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class ModelManager:
    """Stub ModelManager class for AI engine compatibility."""

    def __init__(self):
        pass

    def get_active_models(self) -> List[Dict[str, Any]]:
        """Get active models. Stub implementation."""
        return []

    def discover_models(self) -> None:
        """Discover models. Stub implementation."""
        logger.info("Discovering models (stub)...")

    def list_models(self) -> List[Dict[str, Any]]:
        """List models. Stub implementation."""
        return []

    def check_health(self) -> bool:
        """Check model manager health. Stub implementation."""
        return True


# Create a global instance for backward compatibility
model_manager = ModelManager()
