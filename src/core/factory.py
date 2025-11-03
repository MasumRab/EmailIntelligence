import os

from .data_source import DataSource
from .database import DatabaseManager
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


_data_source_instance = None


async def get_data_source() -> DataSource:
    """
    Provides the singleton instance of the DataSource.
    """
    global _data_source_instance
    if _data_source_instance is None:
        source_type = os.environ.get("DATA_SOURCE_TYPE", "default")
        if source_type == "notmuch":
            _data_source_instance = NotmuchDataSource()
        else:
            _data_source_instance = DatabaseManager()
            await _data_source_instance._ensure_initialized()
    return _data_source_instance
