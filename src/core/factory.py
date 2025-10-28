import os

from .data_source import DataSource
from .database import DatabaseManager
from .notmuch_data_source import NotmuchDataSource
from .data.repository import DatabaseEmailRepository, EmailRepository

_data_source_instance = None
_email_repository_instance = None


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
