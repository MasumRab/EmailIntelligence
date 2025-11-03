import os

from .data_source import DataSource
from .database import DatabaseManager
from .notmuch_data_source import NotmuchDataSource

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
