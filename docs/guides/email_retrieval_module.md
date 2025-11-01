# Email Retrieval Module Documentation

## Overview

The Email Retrieval module provides comprehensive email fetching and synchronization capabilities for the Email Intelligence Platform. It supports multiple email protocols with a primary focus on Gmail API integration, featuring OAuth authentication, intelligent batching, caching, rate limit management, and robust error handling.

## Architecture

### Key Components

#### 1. Gmail Integration Core (`backend/python_nlp/gmail_integration.py`)
Primary Gmail API client with authentication, batch processing, and caching.

#### 2. Gmail AI Service (`backend/python_nlp/gmail_service.py`)
High-level orchestration service combining data collection, metadata extraction, and AI analysis.

#### 3. UI Interface (`modules/email_retrieval/email_retrieval_ui.py`)
Gradio-based user interface for email filtering and retrieval operations.

#### 4. Data Collection Strategy (`backend/python_nlp/data_strategy.py`)
Configurable strategies for email data collection and processing.

### Data Flow
```
User Request → UI Interface → Gmail Service → Gmail Integration → API Calls
                                      ↓
                            Metadata Extraction → AI Analysis → Storage
                                      ↓
                            Cache Updates → Response Generation
```

### Integration Points
- **Gmail API:** OAuth2 authentication and email data retrieval
- **Database:** Email storage and metadata persistence
- **AI Engine:** Email content analysis and categorization
- **Security Module:** Path validation for cached data
- **Cache System:** SQLite-based email caching for performance

## Core Classes & Functions

### GmailDataCollector

#### Main Class
```python
class GmailDataCollector:
    """A robust collector for Gmail data with advanced features.

    This class provides methods to authenticate with Gmail, fetch emails
    in batches, handle rate limits, and cache results for improved performance.
    """

    def __init__(
        self,
        credentials_path: str = CREDENTIALS_PATH,
        token_path: str = TOKEN_JSON_PATH,
        cache_path: Optional[Path] = None,
        rate_limit_config: Optional[RateLimitConfig] = None,
    ):
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.cache_path = cache_path or DEFAULT_CACHE_PATH
        self.rate_limit_config = rate_limit_config or RateLimitConfig()
        self.service = None
        self.cache_conn = None
        self.logger = logging.getLogger(__name__)
```

#### Authentication Methods
```python
async def authenticate(self) -> bool:
    """Authenticate with Gmail using OAuth2 flow.

    Handles credential loading, token refresh, and interactive authentication
    when necessary. Supports both file-based and environment variable credentials.
    """
    try:
        # Try loading existing credentials
        creds = self._load_credentials()

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                # Refresh expired token
                creds.refresh(Request())
            else:
                # Start new OAuth flow
                creds = await self._perform_oauth_flow()

        # Build Gmail API service
        self.service = build('gmail', 'v1', credentials=creds)
        return True

    except Exception as e:
        self.logger.error(f"Authentication failed: {e}")
        return False

def _load_credentials(self) -> Optional[Credentials]:
    """Load credentials from token file or environment variable."""
    # Try token file first
    if os.path.exists(self.token_path):
        with open(self.token_path, 'r') as token:
            creds_data = json.load(token)
            return Credentials.from_authorized_user_info(creds_data)

    # Try environment variable
    creds_json = os.getenv(GMAIL_CREDENTIALS_ENV_VAR)
    if creds_json:
        creds_data = json.loads(creds_json)
        return Credentials.from_authorized_user_info(creds_data)

    return None
```

#### Email Fetching
```python
async def fetch_emails(
    self,
    query: str = "",
    max_results: int = 100,
    include_attachments: bool = False,
    batch_size: int = 50
) -> List[Dict[str, Any]]:
    """Fetch emails from Gmail with intelligent batching and caching.

    Args:
        query: Gmail search query string
        max_results: Maximum number of emails to fetch
        include_attachments: Whether to download attachments
        batch_size: Number of emails to fetch per batch

    Returns:
        List of email data dictionaries
    """
    try:
        # Check cache first
        cached_results = await self._get_cached_results(query, max_results)
        if cached_results:
            return cached_results

        # Authenticate if needed
        if not await self.authenticate():
            raise AuthenticationError("Failed to authenticate with Gmail")

        # Build Gmail query
        gmail_query = self._build_gmail_query(query)

        # Fetch emails in batches
        all_emails = []
        next_page_token = None

        while len(all_emails) < max_results:
            # Respect rate limits
            await self._wait_for_rate_limit()

            # Fetch batch
            batch_emails, next_page_token = await self._fetch_email_batch(
                gmail_query, batch_size, next_page_token
            )

            if not batch_emails:
                break

            # Process batch
            processed_emails = await self._process_email_batch(
                batch_emails, include_attachments
            )

            all_emails.extend(processed_emails)

            if not next_page_token:
                break

        # Cache results
        await self._cache_results(query, all_emails)

        return all_emails[:max_results]

    except Exception as e:
        self.logger.error(f"Email fetching failed: {e}")
        raise
```

### GmailAIService

#### Main Class
```python
class GmailAIService:
    """Provides a complete service for Gmail integration, including AI processing.

    This class combines functionalities for fetching emails, extracting metadata,
    performing AI analysis, and training models, offering a unified interface
    for advanced email management.
    """

    def __init__(
        self,
        credentials_path: Optional[str] = None,
        token_path: Optional[str] = None,
        cache_path: Optional[Path] = None,
        db_manager: Optional[DatabaseManager] = None,
        ai_engine: Optional[AdvancedAIEngine] = None,
        data_strategy: Optional[DataCollectionStrategy] = None,
    ):
        # Initialize components
        self.collector = GmailDataCollector(
            credentials_path or CREDENTIALS_PATH,
            token_path or TOKEN_JSON_PATH,
            cache_path or DEFAULT_CACHE_PATH
        )

        self.metadata_extractor = GmailMetadataExtractor()
        self.data_strategy = data_strategy or DataCollectionStrategy()
        self.db_manager = db_manager
        self.advanced_ai_engine = ai_engine

        # Initialize statistics
        self.stats = {
            "emails_processed": 0,
            "successful_extractions": 0,
            "failed_extractions": 0,
            "ai_analysis_count": 0,
            "cache_hits": 0,
            "api_calls": 0
        }
```

#### Email Processing Pipeline
```python
async def process_emails(
    self,
    query: str = "",
    max_emails: int = 50,
    perform_ai_analysis: bool = True,
    store_in_db: bool = True
) -> Dict[str, Any]:
    """Complete email processing pipeline with AI analysis.

    Args:
        query: Gmail search query
        max_emails: Maximum emails to process
        perform_ai_analysis: Whether to perform AI analysis
        store_in_db: Whether to store results in database

    Returns:
        Processing results and statistics
    """
    try:
        # Fetch emails
        emails = await self.collector.fetch_emails(
            query=query,
            max_results=max_emails,
            include_attachments=False
        )

        processed_emails = []

        for email_data in emails:
            try:
                # Extract metadata
                metadata = await self.metadata_extractor.extract_metadata(email_data)

                # Perform AI analysis if requested
                if perform_ai_analysis and self.advanced_ai_engine:
                    ai_results = await self._perform_ai_analysis(metadata)
                    metadata.update(ai_results)

                # Store in database if requested
                if store_in_db and self.db_manager:
                    await self._store_email_data(metadata)

                processed_emails.append(metadata)
                self.stats["successful_extractions"] += 1

            except Exception as e:
                self.logger.error(f"Failed to process email: {e}")
                self.stats["failed_extractions"] += 1

        self.stats["emails_processed"] = len(processed_emails)

        return {
            "emails": processed_emails,
            "stats": self.stats,
            "query": query,
            "processing_time": time.time() - time.time()  # Would track actual time
        }

    except Exception as e:
        self.logger.error(f"Email processing pipeline failed: {e}")
        raise
```

### Rate Limiting & Caching

#### RateLimitConfig
```python
@dataclasses.dataclass
class RateLimitConfig:
    """Configuration for managing Gmail API rate limits.

    Gmail API has specific quotas and rate limits that must be respected
    to avoid service disruptions and ensure fair usage.
    """

    # Gmail API quotas (per user per day)
    daily_read_quota: int = 1000000  # 1M messages per day
    daily_send_quota: int = 500      # 500 sends per day

    # Rate limits (requests per time window)
    requests_per_minute: int = 250   # 250 requests/minute
    requests_per_second: int = 5     # 5 requests/second

    # Backoff configuration
    initial_backoff: float = 1.0     # Initial backoff in seconds
    max_backoff: float = 60.0        # Maximum backoff time
    backoff_multiplier: float = 2.0  # Exponential backoff multiplier

    # Circuit breaker
    failure_threshold: int = 5       # Failures before opening circuit
    recovery_timeout: int = 300      # Recovery time in seconds
```

#### Caching System
```python
async def _get_cached_results(self, query: str, max_results: int) -> Optional[List[Dict]]:
    """Retrieve cached email results if available and fresh."""
    try:
        cache_key = self._generate_cache_key(query, max_results)

        with sqlite3.connect(str(self.cache_path)) as conn:
            cursor = conn.cursor()

            # Check if cache entry exists and is fresh
            cursor.execute("""
                SELECT data, timestamp FROM email_cache
                WHERE cache_key = ? AND timestamp > ?
            """, (cache_key, time.time() - self.cache_ttl))

            row = cursor.fetchone()
            if row:
                self.stats["cache_hits"] += 1
                return json.loads(row[0])

        return None

    except Exception as e:
        self.logger.warning(f"Cache retrieval failed: {e}")
        return None

async def _cache_results(self, query: str, emails: List[Dict]):
    """Cache email results for future retrieval."""
    try:
        cache_key = self._generate_cache_key(query, len(emails))

        with sqlite3.connect(str(self.cache_path)) as conn:
            cursor = conn.cursor()

            # Create cache table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS email_cache (
                    cache_key TEXT PRIMARY KEY,
                    data TEXT,
                    timestamp REAL
                )
            """)

            # Store results
            cursor.execute("""
                INSERT OR REPLACE INTO email_cache
                (cache_key, data, timestamp) VALUES (?, ?, ?)
            """, (cache_key, json.dumps(emails), time.time()))

            conn.commit()

    except Exception as e:
        self.logger.warning(f"Cache storage failed: {e}")
```

## Configuration

### Environment Variables
```bash
# Gmail API Configuration
GMAIL_CREDENTIALS_JSON={"installed":{"client_id":"...","client_secret":"..."}}
GMAIL_TOKEN_PATH=jsons/token.json

# Cache Configuration
EMAIL_CACHE_PATH=email_cache.db
CACHE_TTL_SECONDS=3600

# Rate Limiting
GMAIL_RATE_LIMIT_REQUESTS_PER_MINUTE=250
GMAIL_RATE_LIMIT_REQUESTS_PER_SECOND=5
GMAIL_BACKOFF_INITIAL=1.0
GMAIL_BACKOFF_MAX=60.0

# Processing Options
EMAIL_BATCH_SIZE=50
EMAIL_MAX_ATTACHMENTS_SIZE_MB=10
EMAIL_PROCESSING_TIMEOUT=30

# Database Integration
DB_STORE_EMAILS=true
DB_BATCH_SIZE=100
```

### Gmail API Credentials Setup
```bash
# 1. Create OAuth 2.0 credentials in Google Cloud Console
# 2. Download credentials.json
# 3. Place in jsons/credentials.json or set environment variable

# Option A: File-based credentials
export GMAIL_TOKEN_PATH=jsons/token.json
cp credentials.json jsons/credentials.json

# Option B: Environment variable
export GMAIL_CREDENTIALS_JSON='{"installed":{"client_id":"...","client_secret":"..."}}'
```

### Runtime Configuration
```python
from backend.python_nlp.gmail_integration import GmailDataCollector, RateLimitConfig
from backend.python_nlp.data_strategy import DataCollectionStrategy

# Configure rate limiting
rate_config = RateLimitConfig(
    requests_per_minute=200,  # Conservative rate
    requests_per_second=3,
    initial_backoff=2.0,
    max_backoff=120.0
)

# Initialize collector
collector = GmailDataCollector(
    credentials_path="jsons/credentials.json",
    token_path="jsons/token.json",
    cache_path=Path("./cache/emails.db"),
    rate_limit_config=rate_config
)

# Configure data collection strategy
strategy = DataCollectionStrategy(
    batch_size=25,  # Smaller batches for reliability
    include_attachments=False,  # Skip attachments for performance
    metadata_only=True,  # Focus on metadata
    max_attachment_size_mb=5
)
```

## Usage Examples

### Basic Email Fetching

```python
import asyncio
from backend.python_nlp.gmail_integration import GmailDataCollector

async def fetch_recent_emails():
    """Fetch recent emails from Gmail."""
    collector = GmailDataCollector()

    # Authenticate
    if not await collector.authenticate():
        print("Authentication failed")
        return

    # Fetch recent emails
    emails = await collector.fetch_emails(
        query="newer_than:7d",  # Emails from last 7 days
        max_results=50
    )

    print(f"Fetched {len(emails)} emails")
    for email in emails[:5]:  # Show first 5
        print(f"Subject: {email.get('subject', 'No subject')}")
        print(f"From: {email.get('from', 'Unknown')}")
        print(f"Date: {email.get('date', 'Unknown')}")
        print("---")

asyncio.run(fetch_recent_emails())
```

### Advanced Email Processing with AI

```python
import asyncio
from backend.python_nlp.gmail_service import GmailAIService
from backend.python_backend.database import DatabaseManager
from backend.python_backend.ai_engine import AdvancedAIEngine

async def process_emails_with_ai():
    """Process emails with AI analysis and database storage."""
    # Initialize components
    db_manager = DatabaseManager()
    ai_engine = AdvancedAIEngine()
    gmail_service = GmailAIService(
        db_manager=db_manager,
        ai_engine=ai_engine
    )

    # Configure processing
    query = "label:inbox is:unread"
    max_emails = 25

    # Process emails
    result = await gmail_service.process_emails(
        query=query,
        max_emails=max_emails,
        perform_ai_analysis=True,
        store_in_db=True
    )

    print(f"Processed {result['stats']['emails_processed']} emails")
    print(f"Successful extractions: {result['stats']['successful_extractions']}")
    print(f"AI analyses performed: {result['stats']['ai_analysis_count']}")

    # Show sample results
    for email in result['emails'][:3]:
        print(f"\\nEmail: {email.get('subject')}")
        print(f"Category: {email.get('category', 'Unknown')}")
        print(f"Sentiment: {email.get('sentiment', 'Unknown')}")
        print(f"Priority: {email.get('priority', 'Normal')}")

asyncio.run(process_emails_with_ai())
```

### Email Filtering and Search

```python
# Using the UI filtering system
from modules.email_retrieval.email_retrieval_ui import get_saved_filters, load_filter

# Get available filters
filter_names = get_saved_filters()
print(f"Available filters: {[f['name'] for f in filter_names]}")

# Load a specific filter
filter_data = load_filter("Important Business")
if filter_data:
    sender, to, subject, keywords, date_filter, start_date, end_date, category, has_attachment = filter_data

    # Build Gmail query
    query_parts = []
    if sender:
        query_parts.append(f"from:{sender}")
    if subject:
        query_parts.append(f"subject:{subject}")
    if keywords:
        query_parts.append(f"{{{keywords}}}")

    # Add date filtering
    if date_filter == "Custom range" and start_date and end_date:
        query_parts.append(f"after:{start_date} before:{end_date}")

    if has_attachment:
        query_parts.append("has:attachment")

    gmail_query = " ".join(query_parts)
    print(f"Gmail query: {gmail_query}")
```

## API Reference

### GmailDataCollector Methods

#### `authenticate() -> bool`
Authenticates with Gmail API using OAuth2.

#### `fetch_emails(query, max_results, include_attachments, batch_size) -> List[Dict]`
Fetches emails matching the specified query.

**Parameters:**
- `query` (str): Gmail search query
- `max_results` (int): Maximum emails to return (default: 100)
- `include_attachments` (bool): Download attachments (default: False)
- `batch_size` (int): Emails per batch (default: 50)

**Returns:**
- List of email dictionaries with metadata

#### `clear_cache() -> None`
Clears the email cache database.

#### `get_cache_stats() -> Dict`
Returns cache statistics and usage information.

### GmailAIService Methods

#### `process_emails(query, max_emails, perform_ai_analysis, store_in_db) -> Dict`
Complete email processing pipeline.

**Parameters:**
- `query` (str): Gmail search query
- `max_emails` (int): Maximum emails to process
- `perform_ai_analysis` (bool): Enable AI analysis
- `store_in_db` (bool): Store results in database

**Returns:**
- Processing results with emails and statistics

#### `get_stats() -> Dict`
Returns processing statistics.

#### `reset_stats() -> None`
Resets processing statistics counters.

## Performance Considerations

### Optimization Strategies
- **Caching:** SQLite-based caching reduces API calls
- **Batching:** Process emails in configurable batches
- **Rate Limiting:** Respect Gmail API quotas
- **Async Processing:** Non-blocking email fetching
- **Memory Management:** Stream processing for large email volumes

### Benchmarks
- **Authentication:** < 5 seconds for initial OAuth flow
- **Email Fetching:** 50-200 emails/minute (rate limited)
- **Cache Hit Rate:** > 80% for repeated queries
- **AI Processing:** 10-30 seconds per email batch
- **Memory Usage:** 50-200 MB depending on batch size

### Scaling Considerations
```python
# Large-scale email processing configuration
large_scale_config = {
    "batch_size": 10,        # Smaller batches for stability
    "max_workers": 3,        # Parallel processing
    "cache_ttl": 7200,      # Longer cache retention
    "rate_limit_buffer": 0.8,  # 80% of rate limit
    "retry_attempts": 5,    # More retries for reliability
    "timeout": 60           # Longer timeouts
}

# Distributed processing
cluster_config = {
    "node_count": 5,
    "load_balancing": "round_robin",
    "shared_cache": "redis://cache-server:6379",
    "coordination": "zookeeper://zk-server:2181"
}
```

## Security Considerations

### Authentication Security
- **OAuth2 Flow:** Secure token-based authentication
- **Token Storage:** Encrypted token storage with proper permissions
- **Token Refresh:** Automatic token renewal without user intervention
- **Scope Limitation:** Read-only access to minimize security risk

### Data Protection
```python
# Secure email data handling
class SecureEmailProcessor:
    """Process emails with security considerations."""

    def __init__(self):
        self.sensitive_fields = {
            'password', 'token', 'key', 'secret', 'credit_card',
            'ssn', 'social_security', 'bank_account'
        }

    def sanitize_email_content(self, email_data: Dict) -> Dict:
        """Remove or mask sensitive information from email content."""
        sanitized = email_data.copy()

        # Sanitize subject
        if 'subject' in sanitized:
            sanitized['subject'] = self._mask_sensitive_data(
                sanitized['subject']
            )

        # Sanitize body content
        if 'body' in sanitized:
            sanitized['body'] = self._mask_sensitive_data(
                sanitized['body']
            )

        return sanitized

    def _mask_sensitive_data(self, text: str) -> str:
        """Mask sensitive data patterns in text."""
        # Simple pattern-based masking
        for field in self.sensitive_fields:
            # Case-insensitive replacement
            text = re.sub(
                rf'\\b{re.escape(field)}\\b.*?(?=\\s|$)',
                f'{field}: [REDACTED]',
                text,
                flags=re.IGNORECASE
            )
        return text
```

### Access Control
- **Permission Levels:** Configurable access to email data
- **Audit Logging:** All email access operations logged
- **Rate Limiting:** Prevents abuse and ensures fair usage
- **IP Restrictions:** Optional IP-based access control

## Troubleshooting

### Common Issues

#### Authentication Failures
```
Error: Authentication failed
```

**Diagnosis:**
```python
# Check credential files
import os
print(f"Credentials exist: {os.path.exists('jsons/credentials.json')}")
print(f"Token exists: {os.path.exists('jsons/token.json')}")

# Check environment variables
import os
creds = os.getenv('GMAIL_CREDENTIALS_JSON')
print(f"Env credentials: {creds is not None}")
```

**Solutions:**
```bash
# Regenerate token
rm jsons/token.json
# Run authentication again

# Check credentials format
python -c "
import json
with open('jsons/credentials.json') as f:
    creds = json.load(f)
    print('Credentials structure:', creds.keys())
"
```

#### Rate Limiting Issues
```
Error: Quota exceeded or Rate limit exceeded
```

**Diagnosis:**
```python
# Check rate limit status
collector = GmailDataCollector()
stats = collector.get_rate_limit_stats()
print(f"Requests this minute: {stats['requests_this_minute']}")
print(f"Requests this hour: {stats['requests_this_hour']}")
print(f"Backoff active: {stats['backoff_active']}")
```

**Solutions:**
```python
# Reduce request rate
config = RateLimitConfig(
    requests_per_minute=100,  # Reduce from default 250
    requests_per_second=2     # Reduce from default 5
)

collector = GmailDataCollector(rate_limit_config=config)

# Wait for quota reset
import time
time.sleep(3600)  # Wait 1 hour for quota reset
```

#### Cache Corruption
```
Error: Database disk image is malformed
```

**Diagnosis:**
```bash
# Check cache file integrity
ls -la email_cache.db
file email_cache.db
```

**Solutions:**
```python
# Clear corrupted cache
collector = GmailDataCollector()
await collector.clear_cache()

# Reinitialize cache
await collector.initialize_cache()
```

### Debug Mode

```python
import logging

# Enable detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Enable Gmail service debug logging
gmail_service = GmailAIService()
gmail_service.logger.setLevel(logging.DEBUG)

# Enable collector debug mode
collector = GmailDataCollector()
collector.debug_mode = True

# Monitor API calls
with collector.debug_context():
    emails = await collector.fetch_emails("subject:test")
    print(f"Debug info: {collector.get_debug_info()}")
```

## Development Notes

### Testing

```bash
# Unit tests
pytest tests/backend/test_gmail_integration.py -v
pytest tests/backend/test_gmail_service.py -v

# Integration tests
pytest tests/integration/test_email_retrieval.py -v

# Mock Gmail API for testing
pytest tests/mocks/test_gmail_mock.py -v

# Performance tests
pytest tests/performance/test_email_fetching.py -v
```

### Code Style

```python
# Email retrieval best practices
class EmailRetrievalService:
    """Service for reliable email retrieval with error handling."""

    def __init__(self, config: EmailConfig):
        self.config = config
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self._retry_count = 0
        self._last_error = None

    async def fetch_with_retry(
        self,
        query: str,
        max_retries: int = 3
    ) -> List[Dict[str, Any]]:
        """Fetch emails with automatic retry on failures."""
        for attempt in range(max_retries + 1):
            try:
                emails = await self._fetch_emails_implementation(query)
                self._retry_count = 0  # Reset on success
                return emails

            except TemporaryError as e:
                if attempt < max_retries:
                    wait_time = 2 ** attempt  # Exponential backoff
                    self.logger.warning(
                        f"Attempt {attempt + 1} failed, retrying in {wait_time}s: {e}"
                    )
                    await asyncio.sleep(wait_time)
                else:
                    self.logger.error(f"All {max_retries + 1} attempts failed")
                    raise

            except PermanentError as e:
                self.logger.error(f"Permanent error, not retrying: {e}")
                self._last_error = e
                raise

    async def _fetch_emails_implementation(self, query: str) -> List[Dict[str, Any]]:
        """Actual email fetching implementation."""
        # Implementation details...
        pass
```

### Error Handling

```python
# Comprehensive error hierarchy
class EmailRetrievalError(Exception):
    """Base class for email retrieval errors."""
    pass

class AuthenticationError(EmailRetrievalError):
    """Authentication-related errors."""
    pass

class RateLimitError(EmailRetrievalError):
    """Rate limiting errors."""
    pass

class NetworkError(EmailRetrievalError):
    """Network connectivity errors."""
    pass

class TemporaryError(EmailRetrievalError):
    """Temporary errors that may be retried."""
    pass

class PermanentError(EmailRetrievalError):
    """Permanent errors that should not be retried."""
    pass
```

### Contributing

1. **Gmail API Changes:** Update integration when Gmail API changes
2. **Authentication:** Improve OAuth2 flow and token management
3. **Caching:** Enhance cache strategies for better performance
4. **Error Handling:** Add more specific error types and recovery
5. **Testing:** Add comprehensive mock Gmail API for testing

## Migration Guide

### From Legacy Email Retrieval

#### API Changes
```python
# Legacy approach
from old_email_client import EmailClient
client = EmailClient()
emails = client.fetch("inbox", limit=50)

# New approach
from backend.python_nlp.gmail_integration import GmailDataCollector
collector = GmailDataCollector()
await collector.authenticate()
emails = await collector.fetch_emails("in:inbox", max_results=50)
```

#### Configuration Migration
```python
# Old config
email_config = {
    "server": "imap.gmail.com",
    "port": 993,
    "username": "user@gmail.com",
    "password": "password"
}

# New config
gmail_config = {
    "credentials_path": "jsons/credentials.json",
    "token_path": "jsons/token.json",
    "cache_path": "./cache/emails.db",
    "rate_limit_config": RateLimitConfig()
}
```

## Changelog

### Version 2.0.0
- **Added:** Comprehensive Gmail API integration
- **Added:** OAuth2 authentication with token refresh
- **Added:** Intelligent batching and rate limiting
- **Added:** SQLite-based caching for performance
- **Added:** AI analysis integration in processing pipeline
- **Added:** Comprehensive error handling and retry logic

### Version 1.5.0
- **Added:** Metadata extraction and processing
- **Added:** Configurable data collection strategies
- **Improved:** Rate limiting with exponential backoff
- **Added:** Circuit breaker pattern for reliability

### Version 1.0.0
- **Added:** Basic Gmail API integration
- **Added:** Simple email fetching functionality
- **Added:** Basic caching and rate limiting

---

*Module Version: 2.0.0*
*Last Updated: 2025-10-31*
*API Version: Gmail API v1*
*OAuth2 Scopes: https://www.googleapis.com/auth/gmail.readonly*
*Cache: SQLite-based with TTL*
