import os

from .data_source import DataSource
from .database import DatabaseManager
<<<<<<< HEAD
from .notmuch_data_source import NotmuchDataSource


class DataSourceFactory:
    """
    Factory class for creating DataSource instances.
    """
    
    @staticmethod
    async def create_data_source(source_type: str = "database") -> DataSource:
        """
        Creates a DataSource instance based on the specified type.
        
        Args:
            source_type: The type of data source to create ("database", "notmuch", etc.)
            
        Returns:
            A DataSource instance
        """
        if source_type == "database":
            db_manager = DatabaseManager()
            await db_manager._ensure_initialized()
            return db_manager
        elif source_type == "notmuch":
            return NotmuchDataSource()
        else:
            # Default to database
            db_manager = DatabaseManager()
            await db_manager._ensure_initialized()
            return db_manager

=======
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
>>>>>>> scientific

_data_source_instance = None


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
<<<<<<< HEAD
            _data_source_instance = DatabaseManager()
            await _data_source_instance._ensure_initialized()
    return _data_source_instance
=======
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
>>>>>>> scientific
