from .database_source import get_database_data_source
from .data_source import DataSource


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
            return await get_database_data_source()
        elif source_type == "notmuch":
            # Import locally to avoid circular imports
            from ..notmuch_data_source import NotmuchDataSource
            return NotmuchDataSource()
        else:
            # Default to database
            return await get_database_data_source()


async def get_data_source():
    """
    Factory function to get the appropriate data source.
    """
    # For now, we'll hardcode it to use the DatabaseDataSource.
    return await get_database_data_source()
