"""Model manager module."""

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class ModelManager:
    """Stub ModelManager class for AI engine compatibility."""

    def __init__(self):
        pass

    def get_active_models(self) -> List[Dict[str, Any]]:
        """Get active models. Stub implementation."""
        return []

    def check_health(self) -> bool:
        """Check model manager health. Stub implementation."""
        return True

    def discover_models(self):
        """Discover available models. Stub implementation."""
        pass

    def list_models(self) -> List[Dict[str, Any]]:
        """List available models. Stub implementation."""
        return []

    def load_model(self, model_name: str) -> bool:
        """Load a specific model. Stub implementation."""
        return False

    def get_model(self, model_name: str) -> Any:
        """Get a loaded model. Stub implementation."""
        return None

    def unload_model(self, model_name: str) -> bool:
        """Unload a specific model. Stub implementation."""
        return False

model_manager = ModelManager()
