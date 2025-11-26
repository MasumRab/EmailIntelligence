import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from .data_source import DataSource
from .database import DatabaseManager
from .ai_engine import ModernAIEngine
from .data.repository import DatabaseEmailRepository, EmailRepository

# Optional import for NotmuchDataSource
try:
    from .notmuch_data_source import NotmuchDataSource
    NOTMUCH_AVAILABLE = True
except ImportError:
    NOTMUCH_AVAILABLE = False
    NotmuchDataSource = None

_data_source_instance = None
_email_repository_instance = None


@asynccontextmanager
async def get_ai_engine() -> AsyncGenerator[ModernAIEngine, None]:
    """
    Provides a ModernAIEngine instance with SOTA async generator pattern.

    This implementation provides:
    - Automatic resource management
    - Request-scoped engine instances
    - Proper cleanup and error handling
    - FastAPI dependency injection compatibility
    """
    engine = None
    try:
        # Create and initialize the AI engine
        engine = ModernAIEngine()
        engine.initialize()

        # Yield the engine for use in route handlers
        yield engine

    except Exception as e:
        # Log initialization errors
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Failed to provide AI engine: {e}")
        raise

    finally:
        # Ensure cleanup happens
        if engine:
            try:
                engine.cleanup()
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"Error during AI engine cleanup: {e}")


async def get_data_source() -> DataSource:
    """
    Provides the singleton instance of the DataSource.
    """
    global _data_source_instance
    if _data_source_instance is None:
        source_type = os.environ.get("DATA_SOURCE_TYPE", "default")
        if source_type == "notmuch":
            # Import only when needed to avoid requiring notmuch in test environments
            from .notmuch_data_source import NotmuchDataSource
            _data_source_instance = NotmuchDataSource()
        else:
            _data_source_instance = DatabaseManager()
            await _data_source_instance.initialize()
    return _data_source_instance


async def get_email_repository() -> EmailRepository:
    """
    Provides the singleton instance of the EmailRepository.
    """
    global _email_repository_instance
    if _email_repository_instance is None:
        data_source = await get_data_source()
        _email_repository_instance = DatabaseEmailRepository(data_source)
    return _email_repository_instance