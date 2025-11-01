# Database Configuration Documentation

## Overview

The Email Intelligence Platform now supports proper dependency injection for database management through the `DatabaseConfig` class and factory functions. This replaces the previous global singleton approach with a more flexible and testable configuration system.

## DatabaseConfig Class

The `DatabaseConfig` class holds all configuration options for the database manager:

```python
class DatabaseConfig:
    def __init__(
        self,
        data_dir: Optional[str] = None,
        emails_file: Optional[str] = None,
        categories_file: Optional[str] = None,
        users_file: Optional[str] = None,
        email_content_dir: Optional[str] = None,
    ):
```

### Configuration Options

1. **data_dir**: The root directory for all database files (default: "data" or value of DATA_DIR environment variable)
2. **emails_file**: Path to the emails data file (default: {data_dir}/emails.json.gz)
3. **categories_file**: Path to the categories data file (default: {data_dir}/categories.json.gz)
4. **users_file**: Path to the users data file (default: {data_dir}/users.json.gz)
5. **email_content_dir**: Path to the email content directory (default: {data_dir}/email_content)

## Environment Variables

The following environment variables can be used to configure the database:

- **DATA_DIR**: Root directory for all database files (default: "data")

## Usage Examples

### New Approach (Recommended)

```python
from src.core.database import DatabaseConfig, create_database_manager

# Create configuration
config = DatabaseConfig(
    data_dir="/path/to/data",
    # Other options will use defaults based on data_dir
)

# Create and initialize database manager
db_manager = await create_database_manager(config)

# Use the database manager
emails = await db_manager.get_emails()
```

### FastAPI Dependency Injection

```python
from fastapi import Depends
from src.core.factory import get_data_source
from src.core.data_source import DataSource

@app.get("/api/emails")
async def get_emails(data_source: DataSource = Depends(get_data_source)):
    return await data_source.get_emails()
```

### Backward Compatibility

The old `get_db()` function is still available for backward compatibility but will show a deprecation warning:

```python
from src.core.database import get_db

# This still works but shows a deprecation warning
db = await get_db()
```

## Migration Guide

To migrate from the old singleton approach to the new dependency injection approach:

1. Replace imports of `get_db` with imports from the factory
2. Update function signatures to accept DataSource dependencies
3. Use FastAPI's `Depends()` for automatic dependency injection

### Before (Old Approach)
```python
from src.core.database import get_db

async def get_emails():
    db = await get_db()
    return await db.get_emails()
```

### After (New Approach)
```python
from src.core.factory import get_data_source
from src.core.data_source import DataSource

async def get_emails(data_source: DataSource = Depends(get_data_source)):
    return await data_source.get_emails()
```

## Security Features

The new configuration system includes built-in security features:

1. **Path Validation**: All paths are validated using `validate_path_safety()` to prevent directory traversal attacks
2. **Directory Creation**: Required directories are automatically created with proper permissions
3. **Configuration Validation**: All configuration options are validated at initialization time

## Testing

The new approach makes testing much easier as you can create isolated database instances for each test:

```python
import pytest
from src.core.database import DatabaseConfig, create_database_manager

@pytest.fixture
async def test_db():
    # Create a test-specific configuration
    config = DatabaseConfig(data_dir="/tmp/test_data")
    db_manager = await create_database_manager(config)
    yield db_manager
    # Cleanup after test

async def test_email_creation(test_db):
    email = await test_db.create_email({"subject": "Test"})
    assert email is not None
```