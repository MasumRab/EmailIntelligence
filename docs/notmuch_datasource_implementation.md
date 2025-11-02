# NotmuchDataSource Implementation Documentation

## Overview

The `NotmuchDataSource` class provides a functional implementation of the `DataSource` interface for integrating with the Notmuch email indexing system. This implementation allows the Email Intelligence Platform to work with Notmuch-indexed email data while maintaining compatibility with the abstract data source interface.

## Key Features

1. **Full Interface Compliance**: Implements all methods defined in the `DataSource` abstract base class
2. **Tag-Based Category Mapping**: Maps Notmuch tags to email categories for consistent API usage
3. **Content Extraction**: Properly extracts email content from Notmuch message files
4. **Dashboard Statistics**: Implements efficient dashboard statistics methods using Notmuch queries
5. **Error Handling**: Comprehensive error handling with proper logging
6. **Read-Only Design**: Designed as a read-only data source to work with Notmuch's indexing approach

## Implementation Details

### Content Extraction

The implementation properly extracts email content by:
1. Retrieving the message file path from Notmuch
2. Parsing the email file using Python's standard `email` library
3. Extracting both headers and body content
4. Handling multipart messages correctly
5. Providing fallback mechanisms for content decoding

### Tag-Based Categories

In Notmuch, categories are implemented as tags. The implementation:
1. Treats all user-defined tags as categories
2. Filters out common system tags (inbox, unread, sent, etc.)
3. Provides category counts and breakdowns
4. Maps tag-based queries to category-based API calls

### Dashboard Statistics

The dashboard methods provide efficient statistics:
1. `get_dashboard_aggregates()`: Returns email counts, unread counts, auto-labeled counts, and category counts
2. `get_category_breakdown()`: Returns email counts per category (tag) with configurable limits
3. Uses optimized Notmuch queries for performance

### Error Handling

All methods include proper error handling:
1. Graceful degradation when the Notmuch database is unavailable
2. Detailed logging of errors for debugging
3. Safe fallback values for dashboard statistics
4. Exception handling for file operations and content parsing

## Limitations

1. **Read-Only Operations**: Write operations return None/False as Notmuch is primarily an indexing system
2. **Integer ID Mapping**: Notmuch uses string message IDs rather than integer IDs, so some methods are not fully implemented
3. **Category ID Mapping**: Notmuch uses string tags rather than integer category IDs

## Testing

The implementation includes comprehensive unit tests that:
1. Mock the Notmuch library to avoid external dependencies
2. Test all interface methods
3. Verify error handling behavior
4. Test dashboard statistics methods
5. Validate content extraction functionality

## Usage

To use the NotmuchDataSource:

```python
# Set environment variable to use notmuch data source
import os
os.environ["DATA_SOURCE_TYPE"] = "notmuch"

# The factory will automatically provide the NotmuchDataSource
from src.core.factory import get_data_source

# Use as a dependency in FastAPI routes
async def get_emails(data_source = Depends(get_data_source)):
    return await data_source.get_emails()
```

## Dependencies

- `notmuch` Python bindings
- Standard Python `email` library for content parsing
- Standard Python `logging` library for error reporting

## Version Compatibility

Note: The Notmuch Python bindings may have compatibility issues with newer Python versions (3.12+). It's recommended to use Python 3.11 or earlier for full compatibility.