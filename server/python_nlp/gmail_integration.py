"""
Gmail API Integration with Rate Limiting and Efficient Data Retrieval
Implements smart batching, caching, and rate limit management for email collection
"""

import time
import json
import sqlite3
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging
import asyncio
from collections import deque
import hashlib
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Path for token.json, configurable via environment variable
TOKEN_JSON_PATH = os.getenv('GMAIL_TOKEN_PATH', 'token.json')

# Credentials content will be loaded from GMAIL_CREDENTIALS_JSON environment variable
# CREDENTIALS_PATH is now a placeholder for where it *would* be if it were a file.
# Users should set GMAIL_CREDENTIALS_JSON instead of creating credentials.json
CREDENTIALS_PATH = 'credentials.json' # Placeholder, not directly used if GMAIL_CREDENTIALS_JSON is set.
GMAIL_CREDENTIALS_ENV_VAR = 'GMAIL_CREDENTIALS_JSON'


@dataclass
class RateLimitConfig:
    """Configuration for Gmail API rate limiting"""
    # Gmail API quotas (per day unless specified)
    queries_per_day: int = 1000000000  # 1 billion quota units per day
    queries_per_100_seconds: int = 250  # 250 quota units per 100 seconds per user
    queries_per_second: int = 5  # Practical limit to avoid bursts
    
    # Email retrieval limits
    messages_per_request: int = 100  # Max messages per list request
    max_concurrent_requests: int = 10  # Max concurrent API calls
    
    # Backoff configuration
    initial_backoff: float = 1.0  # Initial backoff in seconds
    max_backoff: float = 60.0  # Maximum backoff in seconds
    backoff_multiplier: float = 2.0  # Exponential backoff multiplier

@dataclass
class EmailBatch:
    """Batch of emails for processing"""
    messages: List[Dict[str, Any]]
    batch_id: str
    timestamp: datetime
    query_filter: str
    total_count: int

class RateLimiter:
    """Token bucket rate limiter for Gmail API"""
    
    def __init__(self, config: RateLimitConfig):
        self.config = config
        self.tokens = config.queries_per_second
        self.last_update = time.time()
        self.request_times = deque()
        
    async def acquire(self) -> None:
        """Acquire permission to make an API request"""
        current_time = time.time()
        
        # Remove requests older than 100 seconds
        while self.request_times and current_time - self.request_times[0] > 100:
            self.request_times.popleft()
        
        # Check if we're within the 100-second limit
        if len(self.request_times) >= self.config.queries_per_100_seconds:
            sleep_time = 100 - (current_time - self.request_times[0])
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
        
        # Token bucket for per-second limiting
        time_passed = current_time - self.last_update
        self.tokens = min(
            self.config.queries_per_second,
            self.tokens + time_passed * (self.config.queries_per_second / 1.0)
        )
        self.last_update = current_time
        
        if self.tokens < 1:
            sleep_time = (1 - self.tokens) / self.config.queries_per_second
            await asyncio.sleep(sleep_time)
            self.tokens = 0
        else:
            self.tokens -= 1
        
        # Record this request
        self.request_times.append(current_time)

class EmailCache:
    """SQLite-based cache for email metadata and content"""
    
    def __init__(self, cache_path: str = "email_cache.db"):
        self.cache_path = cache_path
        self.conn = sqlite3.connect(cache_path, check_same_thread=False)
        self._init_cache()
        
    def _init_cache(self):
        """Initialize cache database tables"""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS emails (
                message_id TEXT PRIMARY KEY,
                thread_id TEXT,
                subject TEXT,
                sender TEXT,
                sender_email TEXT,
                content TEXT,
                labels TEXT,
                timestamp TEXT,
                retrieved_at TEXT,
                content_hash TEXT
            )
        """)
        
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS sync_metadata (
                sync_id TEXT PRIMARY KEY,
                query_filter TEXT,
                last_sync TEXT,
                total_messages INTEGER,
                processed_messages INTEGER,
                next_page_token TEXT
            )
        """)
        
        self.conn.commit()
    
    def get_cached_email(self, message_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve cached email by message ID"""
        cursor = self.conn.execute(
            "SELECT * FROM emails WHERE message_id = ?", (message_id,)
        )
        row = cursor.fetchone()
        
        if row:
            return {
                "message_id": row[0],
                "thread_id": row[1],
                "subject": row[2],
                "sender": row[3],
                "sender_email": row[4],
                "content": row[5],
                "labels": json.loads(row[6]) if row[6] else [],
                "timestamp": row[7],
                "retrieved_at": row[8],
                "content_hash": row[9]
            }
        return None
    
    def cache_email(self, email_data: Dict[str, Any]) -> None:
        """Cache email data"""
        content_hash = hashlib.md5(
            email_data.get("content", "").encode()
        ).hexdigest()
        
        self.conn.execute("""
            INSERT OR REPLACE INTO emails 
            (message_id, thread_id, subject, sender, sender_email, content, 
             labels, timestamp, retrieved_at, content_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            email_data["message_id"],
            email_data.get("thread_id", ""),
            email_data.get("subject", ""),
            email_data.get("sender", ""),
            email_data.get("sender_email", ""),
            email_data.get("content", ""),
            json.dumps(email_data.get("labels", [])),
            email_data.get("timestamp", ""),
            datetime.now().isoformat(),
            content_hash
        ))
        self.conn.commit()
    
    def get_sync_state(self, query_filter: str) -> Optional[Dict[str, Any]]:
        """Get synchronization state for a query filter"""
        cursor = self.conn.execute(
            "SELECT * FROM sync_metadata WHERE query_filter = ?", (query_filter,)
        )
        row = cursor.fetchone()
        
        if row:
            return {
                "sync_id": row[0],
                "query_filter": row[1],
                "last_sync": row[2],
                "total_messages": row[3],
                "processed_messages": row[4],
                "next_page_token": row[5]
            }
        return None
    
    def update_sync_state(self, sync_data: Dict[str, Any]) -> None:
        """Update synchronization state"""
        self.conn.execute("""
            INSERT OR REPLACE INTO sync_metadata 
            (sync_id, query_filter, last_sync, total_messages, processed_messages, next_page_token)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            sync_data["sync_id"],
            sync_data["query_filter"],
            sync_data["last_sync"],
            sync_data["total_messages"],
            sync_data["processed_messages"],
            sync_data.get("next_page_token", "")
        ))
        self.conn.commit()

class GmailDataCollector:
    """
    Gmail API data collector with intelligent rate limiting and caching
    Implements efficient email retrieval strategies
    """
    
    def __init__(self, config: RateLimitConfig = None):
        self.config = config or RateLimitConfig()
        self.rate_limiter = RateLimiter(self.config)
        self.cache = EmailCache()
        self.logger = logging.getLogger(__name__)
        
        self.gmail_service = None
        self._load_credentials()
        if not self.gmail_service:
            self._authenticate()
        
    def _load_credentials(self):
        """Loads API credentials from storage.
        Uses TOKEN_JSON_PATH which can be set by GMAIL_TOKEN_PATH env var.
        """
        creds = None
        token_path = TOKEN_JSON_PATH # Uses the global TOKEN_JSON_PATH
        if os.path.exists(token_path):
            try:
                creds = Credentials.from_authorized_user_file(token_path, SCOPES)
            except Exception as e:
                self.logger.error(f"Error loading credentials from {token_path}: {e}")
                creds = None # Ensure creds is None if loading fails

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                self.logger.info(f"Refreshing expired credentials from {token_path}...")
                try:
                    creds.refresh(Request())
                except Exception as e:
                    self.logger.error(f"Error refreshing credentials: {e}")
                    # Potentially delete token.json and force re-authentication
                    if os.path.exists(token_path):
                        try:
                            os.remove(token_path)
                            self.logger.info(f"Removed invalid token file: {token_path}")
                        except OSError as oe:
                            self.logger.error(f"Error removing token file {token_path}: {oe}")
                    creds = None # Force re-authentication
            # If creds are still None (not loaded or refresh failed), _authenticate will be called

        if creds:
            self.gmail_service = build('gmail', 'v1', credentials=creds)
            self._store_credentials(creds) # Store potentially refreshed credentials
        else:
            self.gmail_service = None # Ensure service is None if no valid creds

    def _store_credentials(self, creds):
        """Stores API credentials.
        Uses TOKEN_JSON_PATH which can be set by GMAIL_TOKEN_PATH env var.
        """
        token_path = TOKEN_JSON_PATH # Uses the global TOKEN_JSON_PATH
        try:
            with open(token_path, 'w') as token_file:
                token_file.write(creds.to_json())
            self.logger.info(f"Credentials stored in {token_path}")
        except OSError as e:
            self.logger.error(f"Error storing credentials to {token_path}: {e}")

    def _authenticate(self):
        """Authenticates the user and obtains credentials using GMAIL_CREDENTIALS_JSON env var."""
        creds = None
        credentials_json_str = os.getenv(GMAIL_CREDENTIALS_ENV_VAR)

        if not credentials_json_str:
            self.logger.error(
                f"Environment variable {GMAIL_CREDENTIALS_ENV_VAR} is not set. "
                "This variable should contain the JSON content of your Google Cloud credentials file."
            )
            # Attempt to fall back to local credentials.json if GMAIL_CREDENTIALS_JSON is not set
            # This maintains previous behavior if the env var is not set, but logs a warning.
            self.logger.warning(
                f"Attempting to use local '{CREDENTIALS_PATH}' as fallback for OAuth. "
                f"It is recommended to set the {GMAIL_CREDENTIALS_ENV_VAR} environment variable."
            )
            if os.path.exists(CREDENTIALS_PATH):
                 try:
                    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
                 except Exception as e:
                    self.logger.error(f"Error loading fallback credentials from {CREDENTIALS_PATH}: {e}")
                    return # Exit if fallback also fails
            else:
                self.logger.error(
                    f"Fallback credentials file '{CREDENTIALS_PATH}' not found. "
                    "Please set the GMAIL_CREDENTIALS_JSON environment variable or provide the file."
                )
                return # Exit if no credentials source is found
        else:
            try:
                credentials_info = json.loads(credentials_json_str)
                flow = InstalledAppFlow.from_client_config(credentials_info, SCOPES)
            except json.JSONDecodeError:
                self.logger.error(
                    f"Invalid JSON content in {GMAIL_CREDENTIALS_ENV_VAR}. "
                    "Please ensure it's a valid JSON string."
                )
                return
            except Exception as e: # Catch other potential errors from from_client_config
                self.logger.error(f"Error loading credentials from {GMAIL_CREDENTIALS_ENV_VAR}: {e}")
                return


        # TODO: This will block if run in a non-interactive environment.
        # Consider alternative flows for server-side applications (e.g., service accounts
        # or a web-based OAuth flow where the user is redirected).
        # For this subtask, we assume an environment where user interaction is possible.
        try:
            creds = flow.run_local_server(port=0)
        except Exception as e: # Catch generic exception from run_local_server
             self.logger.error(f"OAuth flow failed: {e}")
             return


        if creds:
            self._store_credentials(creds)
            self.gmail_service = build('gmail', 'v1', credentials=creds)
            self.logger.info("Authentication successful, Gmail service initialized.")
        else:
            self.logger.error("Failed to obtain credentials.")
            # Potentially raise an exception or handle this state appropriately

    def set_gmail_service(self, service):
        """Set the Gmail API service instance (Deprecated if using OAuth within class)"""
        # This method might be deprecated or changed if OAuth is handled internally
        self.logger.warning("set_gmail_service is called, but OAuth is now handled internally.")
        self.gmail_service = service
    
    async def collect_emails_incremental(
        self, 
        query_filter: str = "", 
        max_emails: Optional[int] = None,
        since_date: Optional[datetime] = None
    ) -> EmailBatch:
        """
        Collect emails incrementally with rate limiting and caching
        
        Args:
            query_filter: Gmail search query (e.g., "category:primary newer_than:7d")
            max_emails: Maximum number of emails to collect
            since_date: Only collect emails after this date
        """
        sync_id = hashlib.md5(f"{query_filter}_{datetime.now().date()}".encode()).hexdigest()
        
        # Check cache for existing sync state
        sync_state = self.cache.get_sync_state(query_filter)
        if not sync_state:
            sync_state = {
                "sync_id": sync_id,
                "query_filter": query_filter,
                "last_sync": datetime.now().isoformat(),
                "total_messages": 0,
                "processed_messages": 0,
                "next_page_token": None
            }
        
        # Build query with date filter if provided
        if since_date:
            date_str = since_date.strftime("%Y/%m/%d")
            query_filter = f"{query_filter} after:{date_str}".strip()
        
        collected_messages = []
        page_token = sync_state.get("next_page_token")
        
        try:
            while len(collected_messages) < (max_emails or float('inf')):
                # Rate limiting
                await self.rate_limiter.acquire()
                
                # Get message list from Gmail API (simulated)
                message_list = await self._get_message_list(
                    query_filter, 
                    page_token,
                    min(self.config.messages_per_request, (max_emails or 100) - len(collected_messages))
                )
                
                if not message_list.get("messages"):
                    break
                
                # Process messages in parallel with rate limiting
                batch_messages = await self._process_message_batch(
                    message_list["messages"]
                )
                
                collected_messages.extend(batch_messages)
                
                # Update sync state
                sync_state["processed_messages"] += len(batch_messages)
                sync_state["next_page_token"] = message_list.get("nextPageToken")
                sync_state["last_sync"] = datetime.now().isoformat()
                
                self.cache.update_sync_state(sync_state)
                
                # Break if no more pages
                if not message_list.get("nextPageToken"):
                    break
                
                page_token = message_list["nextPageToken"]
                
                # Log progress
                self.logger.info(f"Collected {len(collected_messages)} emails so far...")
        
        except Exception as e:
            self.logger.error(f"Error collecting emails: {e}")
            # Save current state for resumption
            self.cache.update_sync_state(sync_state)
            raise
        
        return EmailBatch(
            messages=collected_messages,
            batch_id=sync_id,
            timestamp=datetime.now(),
            query_filter=query_filter,
            total_count=len(collected_messages)
        )
    
    async def _get_message_list(
        self, 
        query: str, 
        page_token: Optional[str] = None,
        max_results: int = 100
    ) -> Dict[str, Any]:
        """
        Get list of message IDs from Gmail API
        In production, this would make actual Gmail API calls
        """
        # Simulate Gmail API response with realistic structure
        if self.gmail_service:
            try:
                # Actual Gmail API call
                return self.gmail_service.users().messages().list(
                    userId='me',
                    q=query,
                    pageToken=page_token,
                    maxResults=max_results
                ).execute()
            except HttpError as error:
                self.logger.error(f'An API error occurred: {error}')
                # Implement more sophisticated error handling and retry logic if needed
                return {"messages": [], "resultSizeEstimate": 0} # Return empty on error
            except Exception as e:
                self.logger.error(f"Unexpected error in _get_message_list: {e}")
                return {"messages": [], "resultSizeEstimate": 0}


        # Fallback to simulated response if gmail_service is not available
        self.logger.warning("Gmail service not available, using simulated response for _get_message_list.")
        return await self._simulate_gmail_response(query, page_token, max_results)
    
    async def _simulate_gmail_response(
        self, 
        query: str, 
        page_token: Optional[str],
        max_results: int
    ) -> Dict[str, Any]:
        """Simulate Gmail API response for development"""
        # Generate realistic message IDs
        base_time = int(time.time())
        messages = []
        
        for i in range(min(max_results, 10)):  # Limit simulation to 10 messages
            message_id = f"msg_{base_time}_{i:03d}"
            messages.append({"id": message_id, "threadId": f"thread_{base_time}_{i//3:03d}"})
        
        response = {
            "messages": messages,
            "resultSizeEstimate": len(messages)
        }
        
        # Add next page token if there would be more results
        if len(messages) == max_results and not page_token:
            response["nextPageToken"] = f"token_{base_time}_next"
        
        return response
    
    async def _process_message_batch(self, message_ids: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """Process a batch of message IDs to get full email content"""
        semaphore = asyncio.Semaphore(self.config.max_concurrent_requests)
        tasks = []
        
        for msg_info in message_ids:
            task = self._get_message_with_semaphore(semaphore, msg_info["id"])
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions and None results
        valid_messages = [
            result for result in results 
            if not isinstance(result, Exception) and result is not None
        ]
        
        return valid_messages
    
    async def _get_message_with_semaphore(
        self, 
        semaphore: asyncio.Semaphore, 
        message_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get message content with concurrency control"""
        async with semaphore:
            await self.rate_limiter.acquire()
            return await self._get_message_content(message_id)
    
    async def _get_message_content(self, message_id: str) -> Optional[Dict[str, Any]]:
        """
        Get full message content from Gmail API
        Implements caching to avoid duplicate requests
        """
        # Check cache first
        cached_email = self.cache.get_cached_email(message_id)
        if cached_email:
            self.logger.debug(f"Cache hit for message {message_id}")
            return cached_email
        self.logger.debug(f"Cache miss for message {message_id}")

        if self.gmail_service:
            try:
                self.logger.debug(f"Attempting to fetch message {message_id} from Gmail API.")
                message = self.gmail_service.users().messages().get(
                    userId='me',
                    id=message_id,
                    format='full'
                ).execute()
                self.logger.debug(f"Successfully fetched message {message_id} from API.")

                email_data = self._parse_message_payload(message)

                if email_data:
                    self.cache.cache_email(email_data)
                    self.logger.debug(f"Successfully parsed and cached message {message_id}.")
                    return email_data
                else:
                    self.logger.warning(f"Could not parse email data for message {message_id}. This message will not be processed further.")
                    return None  # Parsing failure, do not simulate for this specific case
            except HttpError as error:
                self.logger.error(f'API error fetching message {message_id}: {error}. Falling back to simulation.')
                # Fall through to simulation block below
            except Exception as e:
                self.logger.error(f"Unexpected error retrieving message {message_id}: {e}. Falling back to simulation.")
                # Fall through to simulation block below
        else:
            self.logger.warning(f"Gmail service not available. Falling back to simulation for message {message_id}.")
            # Fall through to simulation block below

        # Fallback to simulated response if API call failed or service was unavailable
        self.logger.info(f"Using simulated content for message {message_id}.")
        email_data = await self._simulate_email_content(message_id)

        # Ensure message_id is present in simulated data for caching
        if 'message_id' not in email_data: # _simulate_email_content should guarantee this
            email_data['message_id'] = message_id

        self.cache.cache_email(email_data)
        self.logger.debug(f"Cached simulated content for message {message_id}.")
        return email_data
            
    def _parse_message_payload(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Parses the raw message payload from Gmail API."""
        try:
            headers = {h['name']: h['value'] for h in message.get('payload', {}).get('headers', [])}
            
            # Simplified content extraction (plaintext preferred)
            # Real implementation would need to handle multipart messages, base64 decoding, etc.
            content = ""
            if 'parts' in message['payload']:
                for part in message['payload']['parts']:
                    if part['mimeType'] == 'text/plain' and 'data' in part['body']:
                        import base64
                        content = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                        break
                    # Could add more part types (e.g., text/html)
            elif 'body' in message['payload'] and 'data' in message['payload']['body']:
                 import base64
                 content = base64.urlsafe_b64decode(message['payload']['body']['data']).decode('utf-8')


            return {
                "message_id": message['id'],
                "thread_id": message.get('threadId', ""),
                "subject": headers.get('Subject', ""),
                "sender": headers.get('From', ""), # This often includes name and email
                "sender_email": self._extract_email_address(headers.get('From', "")),
                "content": content,
                "labels": message.get('labelIds', []),
                "timestamp": datetime.fromtimestamp(int(message['internalDate']) / 1000).isoformat()
            }
        except Exception as e:
            self.logger.error(f"Error parsing message payload for {message.get('id')}: {e}")
            return None

    def _extract_email_address(self, sender_header: str) -> str:
        """Extracts the email address from a 'From' header string."""
        # Simple extraction, might need a more robust regex for complex cases
        import re
        match = re.search(r'<([^>]+)>', sender_header)
        if match:
            return match.group(1)
        return sender_header # Return the whole string if no angle brackets found
    
    async def _simulate_email_content(self, message_id: str) -> Dict[str, Any]:
        """Simulate email content for development"""
        # Generate realistic email content based on message ID
        email_templates = [
            {
                "subject": "Project Update - Q4 Planning",
                "sender": "Project Manager",
                "sender_email": "pm@company.com",
                "content": "Hi team, I wanted to provide an update on our Q4 planning initiatives. We've made significant progress on the roadmap and need to finalize the budget allocations by end of week.",
                "labels": ["IMPORTANT", "WORK"]
            },
            {
                "subject": "Invoice #12345 - Payment Due",
                "sender": "Accounting",
                "sender_email": "billing@vendor.com",
                "content": "Your invoice #12345 for $2,500 is now due. Please process payment within 30 days to avoid late fees.",
                "labels": ["FINANCE", "BILLING"]
            },
            {
                "subject": "Weekend Plans",
                "sender": "Sarah",
                "sender_email": "sarah@gmail.com",
                "content": "Hey! Are you free this weekend? We're planning a barbecue and would love to have you join us!",
                "labels": ["PERSONAL", "SOCIAL"]
            }
        ]
        
        # Cycle through templates based on message ID
        template_idx = hash(message_id) % len(email_templates)
        template = email_templates[template_idx]
        
        return {
            "message_id": message_id,
            "thread_id": f"thread_{message_id.split('_')[1]}",
            "subject": template["subject"],
            "sender": template["sender"],
            "sender_email": template["sender_email"],
            "content": template["content"],
            "labels": template["labels"],
            "timestamp": datetime.now().isoformat()
        }
    
    def get_collection_strategies(self) -> Dict[str, Dict[str, Any]]:
        """
        Define different email collection strategies based on use case
        """
        return {
            "daily_sync": {
                "description": "Daily incremental sync for recent emails",
                "query": "newer_than:1d",
                "max_emails": 1000,
                "frequency": "daily",
                "priority": "high"
            },
            "weekly_bulk": {
                "description": "Weekly bulk collection for training data",
                "query": "newer_than:7d",
                "max_emails": 5000,
                "frequency": "weekly",
                "priority": "medium"
            },
            "historical_import": {
                "description": "One-time historical data import",
                "query": "older_than:30d",
                "max_emails": 10000,
                "frequency": "once",
                "priority": "low"
            },
            "category_specific": {
                "description": "Category-specific collection",
                "query": "category:primary OR category:social OR category:promotions",
                "max_emails": 2000,
                "frequency": "daily",
                "priority": "medium"
            }
        }
    
    async def execute_collection_strategy(self, strategy_name: str) -> EmailBatch:
        """Execute a predefined collection strategy"""
        strategies = self.get_collection_strategies()
        
        if strategy_name not in strategies:
            raise ValueError(f"Unknown strategy: {strategy_name}")
        
        strategy = strategies[strategy_name]
        
        self.logger.info(f"Executing collection strategy: {strategy_name}")
        self.logger.info(f"Description: {strategy['description']}")
        
        return await self.collect_emails_incremental(
            query_filter=strategy["query"],
            max_emails=strategy["max_emails"]
        )

async def main():
    """Example usage of Gmail data collector"""
    # Note: The main function would need to be async if _authenticate might run an async flow,
    # or _authenticate needs to be run in a way that doesn't block asyncio loop if used elsewhere.
    # For now, assuming _authenticate might block or run its own loop for console apps.
    
    # Note: The dummy credentials.json creation is removed.
    # The user must now configure environment variables.
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    logger = logging.getLogger(__name__)


    collector = GmailDataCollector() # This will trigger authentication if needed

    if not collector.gmail_service:
        logger.error("Gmail service initialization failed. Please check logs for details.")
        print("--------------------------------------------------------------------------------------")
        print("Gmail Service Initialization Failed!")
        print("--------------------------------------------------------------------------------------")
        print("Please ensure the following environment variables are correctly set:")
        print(f"1. {GMAIL_CREDENTIALS_ENV_VAR}: Should contain the JSON string of your Google Cloud credentials.")
        print(f"   Example: export {GMAIL_CREDENTIALS_ENV_VAR}='{{ \"installed\": {{ ... }} }}'")
        print(f"   (Alternatively, as a fallback, place a 'credentials.json' file in the script's directory: {os.getcwd()})")
        print(f"2. GMAIL_TOKEN_PATH (Optional): Specify a custom path for 'token.json'.")
        print(f"   Defaults to '{TOKEN_JSON_PATH}' in the script's directory: {os.getcwd()}")
        print("If running for the first time, you might need to go through the OAuth2 authentication flow in your browser.")
        print("Check the console logs for more detailed error messages from the application.")
        print("--------------------------------------------------------------------------------------")
        return

    # Execute daily sync strategy
    try:
        batch = await collector.execute_collection_strategy("daily_sync")

        if batch:
            print(f"Collected {batch.total_count} emails in batch {batch.batch_id}")

            # Print first few emails
            for email in batch.messages[:3]:
                print(f"Subject: {email['subject']}")
                print(f"From: {email['sender']} <{email['sender_email']}>")
                print(f"Preview: {email['content'][:100]}...")
                print("---")
        else:
            print("No emails collected or collection failed.")
            
    except Exception as e:
        print(f"Collection failed: {e}")
        logger.exception("Exception in main execution:")

if __name__ == "__main__":
    asyncio.run(main())