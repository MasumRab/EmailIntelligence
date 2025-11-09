"""
Protocol definitions to avoid circular dependencies between modules.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Dict, List, Optional

if TYPE_CHECKING:
    pass


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
