<<<<<<< HEAD
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from .data_source import DataSource
from .database import DatabaseManager
from .ai_engine import ModernAIEngine
from .data.repository import DatabaseEmailRepository, CachingEmailRepository, EmailRepository
from .caching import init_cache_manager, CacheConfig, CacheBackend

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
            if not NOTMUCH_AVAILABLE:
                raise ImportError("NotmuchDataSource requested but notmuch library is not available. Install with: pip install notmuch")
            _data_source_instance = NotmuchDataSource()
        else:
            # Create DatabaseManager with proper configuration
            from .database import DatabaseConfig, create_database_manager
            config = DatabaseConfig()
            _data_source_instance = await create_database_manager(config)
    return _data_source_instance


async def get_email_repository() -> EmailRepository:
    """
    Provides the singleton instance of the EmailRepository with Redis/memory caching.
    """
    global _email_repository_instance
    if _email_repository_instance is None:
        # Initialize cache manager with Redis backend
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        cache_config = CacheConfig(
                backend=CacheBackend.REDIS,
            redis_url=redis_url,
            default_ttl=600,  # 10 minutes for dashboard data
            enable_monitoring=True
        )
        init_cache_manager(cache_config)

        data_source = await get_data_source()
        base_repository = DatabaseEmailRepository(data_source)
        _email_repository_instance = CachingEmailRepository(base_repository)
    return _email_repository_instance
=======
>>>>>>> 837f0b4c3be0be620537c058dd8dba25d8ac010d
