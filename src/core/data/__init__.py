"""
<<<<<<< HEAD
Data module for the Email Intelligence Platform.

This module provides data access components and repository patterns
for managing different data sources.
"""

# Import data components
from .data_source import DataSource
from .database_source import DatabaseDataSource as DatabaseSource
from .repository import EmailRepository as Repository
from ..notmuch_data_source import NotmuchDataSource  # Import from parent directory
from .factory import DataSourceFactory

__all__ = [
    "DataSource",
    "DatabaseSource",
    "NotmuchDataSource",
    "Repository",
    "DataSourceFactory",
]
=======
Data package for the Email Intelligence Platform.
Contains repository patterns for data access.
"""
>>>>>>> scientific
