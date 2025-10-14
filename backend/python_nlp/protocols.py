"""
Protocol definitions to avoid circular dependencies between modules.
"""

<<<<<<< HEAD
=======
from typing import TYPE_CHECKING, Any, Dict, List, Optional
>>>>>>> main
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Dict, List, Optional

if TYPE_CHECKING:
    from ..python_backend.ai_engine import AdvancedAIEngine
    from ..python_backend.database import DatabaseManager


class DatabaseProtocol(ABC):
    """Protocol/Interface for database operations to avoid circular import"""

    @abstractmethod
    async def get_all_categories(self) -> List[Dict[str, Any]]:
        pass


class AIEngineProtocol(ABC):
    """Protocol/Interface for AI engine operations to avoid circular import"""

    @abstractmethod
    async def analyze_email(
        self, subject: str, content: str, db: Optional[DatabaseProtocol] = None
    ) -> Any:
        pass
