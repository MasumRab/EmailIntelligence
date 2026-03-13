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

    def check_health(self) -> bool:
        """Check model manager health. Stub implementation."""
        return True

    def discover_models(self):
        pass

    def list_models(self):
        return []

    def load_model(self, model_name: str):
        pass

    def get_model(self, model_name: str):
        pass

    def unload_model(self, model_name: str):
        pass

model_manager = ModelManager()
