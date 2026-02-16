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
<<<<<<< HEAD


# Create a global instance for backward compatibility
model_manager = ModelManager()
=======
>>>>>>> 3809f0f3a2e942466dc0ff196cd81b50bb948e4c
