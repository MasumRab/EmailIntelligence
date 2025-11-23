# Notmuch Integration Documentation

## Overview

The Notmuch integration provides advanced email indexing and search capabilities for the Email Intelligence Platform. Notmuch is a fast, tag-based email search system that uses the Xapian search engine for efficient full-text search across large email archives.

## Architecture

### Key Components

#### 1. NotmuchDataSource (`src/core/notmuch_data_source.py`)
Core data source implementation for Notmuch integration with the platform's data abstraction layer.

#### 2. Notmuch UI Module (`modules/notmuch/`)
Gradio-based user interface for interactive email search and browsing.

#### 3. Notmuch Library Integration
Direct integration with the Python `notmuch` library for database operations.

### Data Flow
```
Notmuch Database → NotmuchDataSource → Search Queries → UI Display
      ↓                    ↓                        ↓
   Email Indexing    Data Abstraction         User Interaction
   (Xapian)         (DataSource Interface)   (Gradio Components)
```

### Integration Points
- **Data Source Abstraction:** Implements `DataSource` interface for unified email access
- **Factory Pattern:** Registered as "notmuch" data source type
- **UI Integration:** Gradio tab for interactive search and browsing
- **Search Capabilities:** Full-text search with advanced query syntax

## Core Classes & Functions

### NotmuchDataSource

#### Main Class
```python
class NotmuchDataSource(DataSource):
    """
    A data source for Notmuch, implementing the DataSource interface.
    This implementation is read-only for the initial phase.
    """

    def __init__(self, db_path: Optional[str] = None):
        try:
            self.db = notmuch.Database(db_path)
        except Exception as e:
            print(f"Error opening notmuch database: {e}")
            self.db = None
```

#### Search Functionality
```python
async def search_emails(self, search_term: str, limit: int = 50) -> List[Dict[str, Any]]:
    """Searches emails using a notmuch query string.

    Args:
        search_term: Notmuch query string (e.g., "from:john subject:meeting")
        limit: Maximum number of results to return

    Returns:
        List of email dictionaries with metadata
    """
    if not self.db:
        return []

    # Create query and search
    query = self.db.create_query(search_term)
    messages = query.search_messages()

    results = []
    for message in list(messages)[:limit]:
        results.append({
            "id": message.get_message_id(),
            "message_id": message.get_message_id(),
            "subject": message.get_header("subject"),
            "sender": message.get_header("from"),
            "date": message.get_date(),
            "tags": list(message.get_tags()),
        })

    return results
```

#### Email Retrieval
```python
async def get_email_by_message_id(
    self, message_id: str, include_content: bool = True
) -> Optional[Dict[str, Any]]:
    """Retrieves an email by its notmuch message ID.

    Args:
        message_id: The notmuch message ID
        include_content: Whether to include full email content

    Returns:
        Email data dictionary or None if not found
    """
    if not self.db:
        return None

    query = self.db.create_query(f"id:{message_id}")
    messages = list(query.search_messages())

    if not messages:
        return None

    message = messages[0]

    email_data = {
        "id": message.get_message_id(),
        "message_id": message.get_message_id(),
        "subject": message.get_header("subject"),
        "sender": message.get_header("from"),
        "to": message.get_header("to"),
        "cc": message.get_header("cc"),
        "bcc": message.get_header("bcc"),
        "date": message.get_date(),
        "tags": list(message.get_tags()),
    }

    if include_content:
        # Get full message content
        email_data["body"] = self._get_message_content(message)

    return email_data
```

#### Helper Methods
```python
def _get_message_content(self, message) -> str:
    """Extract full message content from a notmuch message."""
    content_parts = []

    # Get all message parts
    for part in message.get_message_parts():
        if part.get_content_type() == "text/plain":
            content_parts.append(part.get_payload())
        elif part.get_content_type() == "text/html":
            # Could add HTML parsing here if needed
            pass

    return "\n".join(content_parts)

def get_database_info(self) -> Dict[str, Any]:
    """Get information about the notmuch database."""
    if not self.db:
        return {"status": "disconnected"}

    return {
        "status": "connected",
        "path": self.db.get_path(),
        "message_count": self.db.count_messages(""),
        "last_modified": self.db.get_revision(),
    }
```

### UI Components

#### Notmuch Search Interface
```python
def create_notmuch_ui():
    """Creates the Gradio UI for notmuch email search."""

    with gr.Blocks() as notmuch_tab:
        gr.Markdown("## Notmuch Email Search")

        with gr.Row():
            search_bar = gr.Textbox(
                label="Search Query",
                placeholder="Enter notmuch query..."
            )
            search_button = gr.Button("Search")

        # Data storage
        email_data_df = gr.DataFrame(visible=False)

        # Results display
        results_list = gr.DataFrame(
            headers=["Subject", "From", "Date", "Tags"],
            label="Search Results",
            interactive=True
        )

        # Email content viewer
        email_viewer = gr.Textbox(
            label="Email Content",
            lines=20,
            interactive=False
        )

        # Event handlers
        search_button.click(
            fn=lambda q: asyncio.run(search_notmuch(q)),
            inputs=search_bar,
            outputs=email_data_df
        ).then(
            fn=display_search_results,
            inputs=email_data_df,
            outputs=[email_data_df, results_list]
        )

        results_list.select(
            fn=on_select,
            inputs=[email_data_df],
            outputs=email_viewer
        )

    return notmuch_tab
```

## Configuration

### Environment Variables
```bash
# Data source configuration
DATA_SOURCE_TYPE=notmuch

# Notmuch database path
NOTMUCH_DATABASE_PATH=/home/user/.mail  # Default: ~/.mail

# Search configuration
NOTMUCH_DEFAULT_LIMIT=50
NOTMUCH_SEARCH_TIMEOUT=30
NOTMUCH_INCLUDE_CONTENT=true
```

### Database Setup
```bash
# Initialize notmuch database
notmuch new

# Index existing emails
notmuch new

# Add tags to emails
notmuch tag +inbox folder:inbox
notmuch tag +sent folder:sent

# Verify database
notmuch count
notmuch search "*"
```

### Runtime Configuration
```python
from src.core.notmuch_data_source import NotmuchDataSource

# Initialize with custom database path
notmuch_ds = NotmuchDataSource(db_path="/path/to/mail/database")

# Or use default path
notmuch_ds = NotmuchDataSource()
```

## Usage Examples

### Basic Email Search

```python
import asyncio
from src.core.factory import get_data_source

async def search_emails():
    """Search emails using notmuch."""
    # Get notmuch data source
    data_source = await get_data_source()

    # Search for emails
    results = await data_source.search_emails("from:john subject:meeting")

    print(f"Found {len(results)} emails:")
    for email in results:
        print(f"- {email['subject']} (from: {email['sender']})")

asyncio.run(search_emails())
```

### Advanced Query Examples

```python
# Search examples
queries = [
    "from:boss",                    # Emails from boss
    "subject:meeting",              # Meeting-related emails
    "tag:inbox and date:yesterday", # Yesterday's inbox emails
    "attachment:pdf",               # Emails with PDF attachments
    "folder:sent and date:2024",    # Sent emails from 2024
    "to:team@company.com",          # Emails to team address
    "not tag:spam",                 # Non-spam emails
]

for query in queries:
    results = await data_source.search_emails(query, limit=10)
    print(f"Query '{query}': {len(results)} results")
```

### Email Content Retrieval

```python
async def get_email_details(message_id: str):
    """Get full email content by message ID."""
    email = await data_source.get_email_by_message_id(message_id, include_content=True)

    if email:
        print(f"Subject: {email['subject']}")
        print(f"From: {email['sender']}")
        print(f"Date: {email['date']}")
        print(f"Tags: {', '.join(email['tags'])}")
        print(f"Content length: {len(email['body'])} characters")
        print("---")
        print(email['body'][:500] + "..." if len(email['body']) > 500 else email['body'])
    else:
        print("Email not found")

# Usage
await get_email_details("message-id@example.com")
```

### Tag-Based Organization

```python
async def organize_emails():
    """Demonstrate tag-based email organization."""

    # Search emails by tags
    important = await data_source.search_emails("tag:important")
    work = await data_source.search_emails("tag:work")
    personal = await data_source.search_emails("tag:personal")

    print(f"Important: {len(important)} emails")
    print(f"Work: {len(work)} emails")
    print(f"Personal: {len(personal)} emails")

    # Find untagged emails
    untagged = await data_source.search_emails("not tag:*")
    print(f"Untagged: {len(untagged)} emails")

asyncio.run(organize_emails())
```

## Notmuch Query Syntax

### Basic Queries
```bash
# Simple text search
meeting

# Field-specific search
from:john
to:team@company.com
subject:project
date:2024-01-01..2024-12-31

# Tag-based search
tag:inbox
tag:important
tag:work

# Boolean operations
from:john and subject:meeting
tag:inbox or tag:important
not tag:spam
```

### Advanced Queries
```bash
# Date ranges
date:yesterday
date:1w..now          # Last week
date:2024-01-01..2024-12-31

# Attachment search
attachment:pdf
attachment:image

# Thread search
thread:thread-id

# Folder/location search
folder:inbox
path:~/mail/work

# Complex combinations
(from:boss or subject:urgent) and date:today and not tag:processed
tag:inbox and attachment:* and date:1d..now
```

### Query Performance Tips
```python
# Efficient queries
good_queries = [
    "tag:inbox and date:today",      # Uses indexes
    "from:specific@email.com",       # Field-specific search
    "subject:(meeting OR review)",   # Specific terms
]

# Less efficient queries
slow_queries = [
    "any",                           # Searches all content
    "date:1y..now",                  # Large date ranges
    "*",                             # Wildcard searches
]
```

## Performance Considerations

### Indexing and Search Performance
- **Xapian Backend:** Fast full-text search with stemming and relevance ranking
- **Tag Indexing:** Efficient tag-based filtering and organization
- **Incremental Updates:** Fast database updates for new emails
- **Memory Usage:** Low memory footprint compared to full email storage

### Optimization Strategies
```python
# Query optimization
class OptimizedNotmuchSearch:
    """Optimized search patterns for better performance."""

    def __init__(self, data_source):
        self.data_source = data_source

    async def efficient_search(self, criteria: Dict[str, Any]) -> List[Dict]:
        """Perform efficient searches with proper indexing."""

        # Build optimized query
        query_parts = []

        # Prefer indexed fields
        if 'tag' in criteria:
            query_parts.append(f"tag:{criteria['tag']}")

        if 'from' in criteria:
            query_parts.append(f"from:{criteria['from']}")

        if 'date_range' in criteria:
            start, end = criteria['date_range']
            query_parts.append(f"date:{start}..{end}")

        # Add text search last
        if 'text' in criteria:
            query_parts.append(criteria['text'])

        # Execute optimized query
        query_str = " and ".join(query_parts)
        return await self.data_source.search_emails(query_str, limit=100)

# Usage
searcher = OptimizedNotmuchSearch(data_source)
results = await searcher.efficient_search({
    'tag': 'inbox',
    'from': 'important@company.com',
    'text': 'quarterly review'
})
```

### Benchmarking
```python
import time
import asyncio

async def benchmark_search():
    """Benchmark notmuch search performance."""

    queries = [
        "tag:inbox",
        "from:boss",
        "subject:meeting",
        "date:today",
        "attachment:pdf"
    ]

    for query in queries:
        start_time = time.time()
        results = await data_source.search_emails(query, limit=100)
        duration = time.time() - start_time

        print(f"Query '{query}': {len(results)} results in {duration:.3f}s")

asyncio.run(benchmark_search())
```

## Security Considerations

### Access Control
- **Database Permissions:** Proper file system permissions on notmuch database
- **Query Sanitization:** Input validation for search queries
- **Path Security:** Database path validation to prevent traversal attacks

### Data Protection
```python
# Secure query validation
def validate_notmuch_query(query: str) -> bool:
    """Validate notmuch query for security."""
    # Prevent dangerous patterns
    dangerous_patterns = [
        r'\.\./',      # Directory traversal
        r';',          # Command injection
        r'\|',         # Pipe operations
        r'`',          # Command substitution
    ]

    for pattern in dangerous_patterns:
        if re.search(pattern, query):
            return False

    return True

# Usage
if validate_notmuch_query(user_query):
    results = await data_source.search_emails(user_query)
else:
    raise ValueError("Invalid search query")
```

### Audit Logging
```python
# Search operation logging
async def logged_search(query: str, user_id: str) -> List[Dict]:
    """Search with audit logging."""
    logger.info(f"User {user_id} searching: {query}")

    start_time = time.time()
    results = await data_source.search_emails(query)
    duration = time.time() - start_time

    logger.info(f"Search completed: {len(results)} results in {duration:.3f}s")

    return results
```

## Troubleshooting

### Common Issues

#### Database Connection Issues
```
Error: Error opening notmuch database
```

**Diagnosis:**
```bash
# Check database path
ls -la ~/.mail

# Verify notmuch installation
which notmuch
notmuch --version

# Check database integrity
notmuch count
```

**Solutions:**
```bash
# Reinitialize database
notmuch new

# Repair database
notmuch repair

# Set correct path
export NOTMUCH_DATABASE_PATH=/correct/path/to/mail
```

#### Search Performance Issues
```
Symptom: Searches taking too long
```

**Diagnosis:**
```bash
# Check database statistics
notmuch count

# Analyze query performance
time notmuch search "tag:inbox"

# Check disk I/O
iotop -o
```

**Solutions:**
```bash
# Optimize database
notmuch optimize

# Reindex database
notmuch reindex "*"

# Add more memory for indexing
export NOTMUCH_CACHE_SIZE=512M
```

#### Missing Search Results
```
Symptom: Expected emails not found
```

**Diagnosis:**
```bash
# Check email indexing
notmuch new

# Verify tags
notmuch search "tag:*" | head -10

# Test specific queries
notmuch search "from:specific@email.com"
```

**Solutions:**
```bash
# Rebuild index
rm -rf ~/.mail/.notmuch
notmuch new

# Add missing tags
notmuch tag +inbox folder:inbox
notmuch tag +sent folder:sent
```

### Debug Mode

```python
import logging

# Enable detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Enable notmuch data source debugging
notmuch_ds = NotmuchDataSource()
notmuch_ds.logger.setLevel(logging.DEBUG)

# Debug search operations
import asyncio

async def debug_search():
    with notmuch_ds.debug_context():
        results = await notmuch_ds.search_emails("tag:inbox", limit=5)
        print(f"Debug info: {notmuch_ds.get_debug_info()}")
        return results

results = asyncio.run(debug_search())
```

## Development Notes

### Testing

```bash
# Unit tests
pytest tests/core/test_notmuch_data_source.py -v

# Integration tests
pytest tests/integration/test_notmuch_integration.py -v

# Mock notmuch for testing (if not installed)
pytest tests/mocks/test_notmuch_mock.py -v

# UI tests
pytest tests/modules/notmuch/test_ui.py -v
```

### Dependencies

```python
# Required packages
pip install notmuch

# For development
pip install pytest-asyncio pandas gradio
```

### Code Style

```python
# Notmuch integration best practices
class NotmuchIntegration:
    """Best practices for Notmuch integration."""

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self._connection_pool = None

    async def robust_search(
        self,
        query: str,
        limit: int = 50,
        retry_count: int = 3
    ) -> List[Dict[str, Any]]:
        """Perform robust search with error handling and retries."""

        for attempt in range(retry_count):
            try:
                # Validate query
                if not self._validate_query(query):
                    raise ValueError(f"Invalid query: {query}")

                # Execute search
                results = await self._execute_search(query, limit)

                # Validate results
                if not self._validate_results(results):
                    self.logger.warning("Search returned invalid results")

                return results

            except notmuch.NotmuchError as e:
                if attempt < retry_count - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    self.logger.warning(
                        f"Search attempt {attempt + 1} failed, retrying in {wait_time}s: {e}"
                    )
                    await asyncio.sleep(wait_time)
                else:
                    self.logger.error(f"All search attempts failed: {e}")
                    raise

    def _validate_query(self, query: str) -> bool:
        """Validate notmuch query syntax."""
        # Basic validation - could be enhanced
        if not query or len(query.strip()) == 0:
            return False
        return True

    def _validate_results(self, results: List[Dict]) -> bool:
        """Validate search results structure."""
        if not isinstance(results, list):
            return False

        required_fields = ['id', 'subject', 'sender', 'date']
        for result in results:
            if not all(field in result for field in required_fields):
                return False

        return True
```

### Contributing

1. **Query Optimization:** Improve search query performance
2. **Error Handling:** Add more specific error types and recovery
3. **UI Enhancement:** Improve Gradio interface with more features
4. **Integration:** Better integration with other email sources
5. **Documentation:** Add more query examples and use cases

## Migration Guide

### From Other Email Search Systems

#### From IMAP Search
```python
# IMAP-style search (limited)
imap_queries = [
    "FROM john@example.com",
    "SUBJECT meeting",
    "SINCE 01-Jan-2024"
]

# Equivalent Notmuch queries
notmuch_queries = [
    "from:john@example.com",
    "subject:meeting",
    "date:2024-01-01..now"
]
```

#### From Local Email Clients
```python
# Thunderbird/Gmail search syntax
client_queries = [
    "from:john subject:meeting has:attachment",
    "label:important is:unread"
]

# Notmuch equivalents
notmuch_equivalents = [
    "from:john and subject:meeting and attachment:*",
    "tag:important and not tag:read"
]
```

### Configuration Migration

```python
# Old IMAP configuration
imap_config = {
    "server": "imap.gmail.com",
    "port": 993,
    "ssl": True,
    "username": "user@gmail.com"
}

# New Notmuch configuration
notmuch_config = {
    "database_path": "~/.mail",
    "search_timeout": 30,
    "default_limit": 50,
    "include_content": True
}
```

## Changelog

### Version 2.0.0
- **Added:** Complete Notmuch data source implementation
- **Added:** Gradio UI for interactive email search
- **Added:** Tag-based email organization and filtering
- **Added:** Full-text search with advanced query syntax
- **Added:** Integration with platform data abstraction layer

### Version 1.5.0
- **Added:** Basic notmuch database connectivity
- **Added:** Simple search functionality
- **Added:** Message ID-based email retrieval

### Version 1.0.0
- **Added:** Initial Notmuch integration
- **Added:** Basic query support
- **Added:** Data source interface implementation

---

*Module Version: 2.0.0*
*Last Updated: 2025-10-31*
*Notmuch Version: Compatible with 0.38+*
*Database: Xapian-based full-text search*
*UI: Gradio-based interactive search*
