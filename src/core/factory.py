from src.core.data.database_source import get_database_data_source, DatabaseManager


async def get_data_source() -> DatabaseManager:
    """
    Factory function to get the data source implementation.
    This acts as a provider for the dependency injection system.
    """
    return await get_database_data_source()
