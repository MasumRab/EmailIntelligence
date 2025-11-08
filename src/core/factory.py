import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from .data_source import DataSource
from .database import DatabaseManager
from .ai_engine import ModernAIEngine
from .data.repository import DatabaseEmailRepository, CachingEmailRepository, EmailRepository
from .caching import init_cache_manager, CacheConfig, CacheBackend
from .dynamic_model_manager import DynamicModelManager
from .model_registry import ModelRegistry
from .smart_filter_manager import SmartFilterManager

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
    Provides a ModernAIEngine instance with proper dependency injection.
    """
    model_registry = ModelRegistry()
    model_manager = DynamicModelManager(registry=model_registry)
    engine = ModernAIEngine(model_manager=model_manager)

    try:
        await engine.initialize()
        yield engine
    finally:
        engine.cleanup()

@asynccontextmanager
async def get_smart_filter_manager() -> AsyncGenerator[SmartFilterManager, None]:
    """
    Provides a SmartFilterManager instance.
    """
    manager = SmartFilterManager()
    try:
        yield manager
    finally:
        await manager.close()


async def get_data_source() -> DataSource:
    """
    Provides the singleton instance of the DataSource.
    """
    global _data_source_instance
    if _data_source_instance is None:
        source_type = os.environ.get("DATA_SOURCE_TYPE", "default")

        # The DatabaseManager may be used by multiple data sources, so we create it upfront.
        from .database import DatabaseConfig, create_database_manager
        config = DatabaseConfig()
        db_manager = await create_database_manager(config)

        if source_type == "notmuch":
            if not NOTMUCH_AVAILABLE:
                raise ImportError(
                    "NotmuchDataSource requested but notmuch library is not available. "
                    "Install with: pip install notmuch"
                )
            # NotmuchDataSource uses a DatabaseManager for caching.
            _data_source_instance = NotmuchDataSource(db_manager=db_manager)
        else:
            # The default data source is the database manager itself.
            _data_source_instance = db_manager
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