from .database_source import get_database_data_source

async def get_data_source():
    """
    Factory function to get the appropriate data source.
    """
    # For now, we'll hardcode it to use the DatabaseDataSource.
    return await get_database_data_source()
