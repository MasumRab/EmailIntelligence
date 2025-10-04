"""
Protocol definitions to avoid circular dependencies between modules.
"""
from typing import TYPE_CHECKING, Any, Dict, List, Optional
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from ..python_backend.database import DatabaseManager
    from ..python_backend.ai_engine import AdvancedAIEngine


class DatabaseProtocol(ABC):
    """Protocol/Interface for database operations to avoid circular import"""
    
    @abstractmethod
    async def get_all_categories(self) -> List[Dict[str, Any]]:
        pass


class AIEngineProtocol(ABC):
    """Protocol/Interface for AI engine operations to avoid circular import"""
    
    @abstractmethod
    async def analyze_email(self, subject: str, content: str, db: Optional[DatabaseProtocol] = None) -> Any:
        pass