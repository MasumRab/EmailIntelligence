"""
Database dependency injection for FastAPI applications.

This module provides dependency injection utilities for database management
in FastAPI applications, supporting both singleton and factory patterns.
"""

import os
from typing import Annotated, Optional
from fastapi import Depends

from .database import DatabaseManager, DatabaseConfig, create_database_manager


def get_database_config() -> DatabaseConfig:
    """
    Create a database configuration from environment variables.
    
    Returns:
        DatabaseConfig: Configuration instance with environment-based settings
    """
    return DatabaseConfig(
        data_dir=os.getenv("DATA_DIR", "data"),
    )


async def get_database_manager(
    config: Annotated[DatabaseConfig, Depends(get_database_config)]
) -> DatabaseManager:
    """
    FastAPI dependency for getting a database manager instance.
    
    Args:
        config: Database configuration
        
    Returns:
        DatabaseManager: Initialized database manager
    """
    return await create_database_manager(config)


# Type alias for easier usage
DatabaseDep = Annotated[DatabaseManager, Depends(get_database_manager)]


def get_database_manager_factory(config: DatabaseConfig):
    """
    Factory function for creating database manager dependencies with custom config.
    
    Args:
        config: Custom database configuration
        
    Returns:
        Dependency function that returns DatabaseManager
    """
    async def _get_db() -> DatabaseManager:
        return await create_database_manager(config)
    
    return _get_db