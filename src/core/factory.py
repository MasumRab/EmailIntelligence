from .data.database_source import DatabaseDataSource

def get_data_source(db_manager=None):
    return DatabaseDataSource(db_manager)
