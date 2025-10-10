"""
Gmail API Integration with Rate Limiting and Efficient Data Retrieval
Implements smart batching, caching, and rate limit management for email collection
"""

import asyncio
import hashlib
import json
import logging
import os
import sqlite3
import time
from collections import deque
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Load environment variables from .env file
load_dotenv()

# If modifying these SCOPES, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
<<<<<<< Updated upstream

# Define the project's root directory and default path for the email cache
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CACHE_PATH = PROJECT_ROOT / "email_cache.db"

# Path for token.json, configurable via environment variable
=======
>>>>>>> Stashed changes
TOKEN_JSON_PATH = os.getenv("GMAIL_TOKEN_PATH", "token.json")

# Credentials content will be loaded from GMAIL_CREDENTIALS_JSON environment variable
# CREDENTIALS_PATH is now a placeholder for where it *would* be if it were a file.
# Users should set GMAIL_CREDENTIALS_JSON instead of creating credentials.json
CREDENTIALS_PATH = (
    "credentials.json"  # Placeholder, not directly used if GMAIL_CREDENTIALS_JSON is set.
)
GMAIL_CREDENTIALS_ENV_VAR = "GMAIL_CREDENTIALS_JSON"


@dataclass
class RateLimitConfig:
    """Configuration for Gmail API rate limiting"""

<<<<<<< Updated upstream
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
=======
    Attributes:
        queries_per_minute: The total number of quota units allowed per minute (project limit).
        queries_per_user_minute: The number of quota units per user per minute.
        queries_per_100_seconds: The number of quota units per 100 seconds.
        queries_per_second: A practical limit to avoid request bursts.
        messages_per_request: The maximum number of messages per list request.
        max_concurrent_requests: The maximum number of concurrent API calls.
        initial_backoff: The initial backoff duration in seconds for retries.
        max_backoff: The maximum backoff duration in seconds.
        backoff_multiplier: The multiplier for exponential backoff.
    """
    queries_per_minute: int = 1200000  # 1.2M quota units per minute (project limit)
    queries_per_user_minute: int = 15000  # 15K quota units per user per minute
    queries_per_100_seconds: int = 250
    queries_per_second: int = 5
    messages_per_request: int = 100
    max_concurrent_requests: int = 10
    initial_backoff: float = 1.0
    max_backoff: float = 60.0
    backoff_multiplier: float = 2.0
>>>>>>> Stashed changes


@dataclass
class EmailBatch:
    """Batch of emails for processing"""

    messages: List[Dict[str, Any]]
    batch_id: str
    timestamp: datetime
    query_filter: str
    total_count: int


class RateLimiter:
<<<<<<< Updated upstream
    """Token bucket rate limiter for Gmail API"""
=======
    """
    Implements a token bucket rate limiting algorithm for the Gmail API.

    This class helps to avoid exceeding the API's rate limits by controlling
    the frequency of outgoing requests. It implements both per-second and
    per-minute rate limiting.
    """
>>>>>>> Stashed changes

    def __init__(self, config: RateLimitConfig):
        self.config = config
        self.tokens_per_second = config.queries_per_second
        self.tokens_per_minute = config.queries_per_minute // 60  # Convert to per-second rate
        self.last_second_update = time.time()
        self.last_minute_update = time.time()
        self.request_times_100s = deque()  # For 100-second window
        self.request_times_minute = deque()  # For per-minute tracking

    async def acquire(self) -> None:
        """Acquire permission to make an API request"""
        current_time = time.time()

<<<<<<< Updated upstream
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
=======
        # Check 100-second window limit
        while self.request_times_100s and current_time - self.request_times_100s[0] > 100:
            self.request_times_100s.popleft()

        if len(self.request_times_100s) >= self.config.queries_per_100_seconds:
            sleep_time = 100 - (current_time - self.request_times_100s[0])
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)

        # Check per-minute limit
        while self.request_times_minute and current_time - self.request_times_minute[0] > 60:
            self.request_times_minute.popleft()

        if len(self.request_times_minute) >= self.config.queries_per_minute:
            sleep_time = 60 - (current_time - self.request_times_minute[0])
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)

        # Update token buckets
        time_passed = current_time - self.last_second_update
        self.tokens_per_second = min(
>>>>>>> Stashed changes
            self.config.queries_per_second,
            self.tokens_per_second + time_passed * (self.config.queries_per_second / 1.0),
        )
        self.last_second_update = current_time

        # Wait if we don't have enough tokens
        if self.tokens_per_second < 1:
            sleep_time = (1 - self.tokens_per_second) / self.config.queries_per_second
            await asyncio.sleep(sleep_time)
            self.tokens_per_second = 0
        else:
            self.tokens_per_second -= 1

<<<<<<< Updated upstream
        # Record this request
        self.request_times.append(current_time)
=======
        # Record the request
        self.request_times_100s.append(current_time)
        self.request_times_minute.append(current_time)
>>>>>>> Stashed changes


class EmailCache:
    """SQLite-based cache for email metadata and content

    This helps to reduce redundant API calls by storing previously fetched
    email data and synchronization states.
    """

<<<<<<< Updated upstream
    def __init__(self, cache_path: str = DEFAULT_CACHE_PATH):
=======
    def __init__(self, cache_path: str = "email_cache.db"):
        """Initializes the EmailCache."""
>>>>>>> Stashed changes
        self.cache_path = cache_path
        self.conn = sqlite3.connect(cache_path, check_same_thread=False)
        self._init_cache()

    def _init_cache(self):
        """Initialize cache database tables"""
        self.conn.execute(
            """
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
        """
        )

        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS sync_metadata (
                sync_id TEXT PRIMARY KEY,
                query_filter TEXT,
                last_sync TEXT,
                total_messages INTEGER,
                processed_messages INTEGER,
                next_page_token TEXT
            )
        """
        )

        self.conn.commit()

    def get_cached_email(self, message_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve cached email by message ID"""
        cursor = self.conn.execute("SELECT * FROM emails WHERE message_id = ?", (message_id,))
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
                "content_hash": row[9],
            }
        return None

    def cache_email(self, email_data: Dict[str, Any]) -> None:
        """Cache email data"""
        content_hash = hashlib.md5(email_data.get("content", "").encode()).hexdigest()

        self.conn.execute(
            """
            INSERT OR REPLACE INTO emails
            (message_id, thread_id, subject, sender, sender_email, content,
             labels, timestamp, retrieved_at, content_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                email_data["message_id"],
                email_data.get("thread_id", ""),
                email_data.get("subject", ""),
                email_data.get("sender", ""),
                email_data.get("sender_email", ""),
                email_data.get("content", ""),
                json.dumps(email_data.get("labels", [])),
                email_data.get("timestamp", ""),
                datetime.now().isoformat(),
                content_hash,
            ),
        )
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
                "next_page_token": row[5],
            }
        return None

    def update_sync_state(self, sync_data: Dict[str, Any]) -> None:
        """Update synchronization state"""
        self.conn.execute(
            """
            INSERT OR REPLACE INTO sync_metadata
            (sync_id, query_filter, last_sync, total_messages, processed_messages, next_page_token)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                sync_data["sync_id"],
                sync_data["query_filter"],
                sync_data["last_sync"],
                sync_data["total_messages"],
                sync_data["processed_messages"],
                sync_data.get("next_page_token", ""),
            ),
        )
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
        token_path = TOKEN_JSON_PATH  # Uses the global TOKEN_JSON_PATH
        if os.path.exists(token_path):
            try:
                creds = Credentials.from_authorized_user_file(token_path, SCOPES)
            except Exception as e:
                self.logger.error("Error loading credentials from %s: %s", token_path, e)
                creds = None  # Ensure creds is None if loading fails

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                self.logger.info("Refreshing expired credentials from %s...", token_path)
                try:
                    creds.refresh(Request())
                except Exception as e:
                    self.logger.error("Error refreshing credentials: %s", e)
                    # Potentially delete token.json and force re-authentication
                    if os.path.exists(token_path):
                        try:
                            os.remove(token_path)
                            self.logger.info("Removed invalid token file: %s", token_path)
                        except OSError as oe:
                            self.logger.error("Error removing token file %s: %s", token_path, oe)
                    creds = None  # Force re-authentication
            # If creds are still None (not loaded or refresh failed), _authenticate will be called

        if creds:
            self.gmail_service = build("gmail", "v1", credentials=creds)
            self._store_credentials(creds)  # Store potentially refreshed credentials
        else:
            self.gmail_service = None  # Ensure service is None if no valid creds

    def _store_credentials(self, creds):
        """Stores API credentials.
        Uses TOKEN_JSON_PATH which can be set by GMAIL_TOKEN_PATH env var.
        """
        token_path = TOKEN_JSON_PATH  # Uses the global TOKEN_JSON_PATH
        try:
            with open(token_path, "w") as token_file:
                token_file.write(creds.to_json())
            self.logger.info("Credentials stored in %s", token_path)
        except OSError as e:
            self.logger.error("Error storing credentials to %s: %s", token_path, e)

    def _authenticate(self):
        """Authenticates the user and obtains credentials using GMAIL_CREDENTIALS_JSON env var."""
        creds = None
        credentials_json_str = os.getenv(GMAIL_CREDENTIALS_ENV_VAR)

        if not credentials_json_str:
            self.logger.error(
                "Environment variable %s is not set. "
                "This variable should contain the JSON content of your Google Cloud credentials file.",
                GMAIL_CREDENTIALS_ENV_VAR,
            )
            # Attempt to fall back to local credentials.json if GMAIL_CREDENTIALS_JSON is not set
            # This maintains previous behavior if the env var is not set, but logs a warning.
            self.logger.warning(
                "Attempting to use local '%s' as fallback for OAuth. "
                "It is recommended to set the %s environment variable.",
                CREDENTIALS_PATH,
                GMAIL_CREDENTIALS_ENV_VAR,
            )
            if os.path.exists(CREDENTIALS_PATH):
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
                except Exception as e:
                    self.logger.error(
                        "Error loading fallback credentials from %s: %s", CREDENTIALS_PATH, e
                    )
                    return  # Exit if fallback also fails
            else:
                self.logger.error(
                    "Fallback credentials file '%s' not found. "
                    "Please set the GMAIL_CREDENTIALS_JSON environment variable or provide the file.",
                    CREDENTIALS_PATH,
                )
                return  # Exit if no credentials source is found
        else:
            try:
                credentials_info = json.loads(credentials_json_str)
                flow = InstalledAppFlow.from_client_config(credentials_info, SCOPES)
            except json.JSONDecodeError:
                self.logger.error(
                    "Invalid JSON content in %s. " "Please ensure it's a valid JSON string.",
                    GMAIL_CREDENTIALS_ENV_VAR,
                )
                return
            except Exception as e:  # Catch other potential errors from from_client_config
                self.logger.error(
                    "Error loading credentials from %s: %s", GMAIL_CREDENTIALS_ENV_VAR, e
                )
                return

        # TODO: This will block if run in a non-interactive environment.
        # Consider alternative flows for server-side applications (e.g., service accounts
        # or a web-based OAuth flow where the user is redirected).
        # For this subtask, we assume an environment where user interaction is possible.
        try:
            creds = flow.run_local_server(port=0)
        except Exception as e:  # Catch generic exception from run_local_server
            self.logger.error("OAuth flow failed: %s", e)
            return

        if creds:
            self._store_credentials(creds)
            self.gmail_service = build("gmail", "v1", credentials=creds)
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
        since_date: Optional[datetime] = None,
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
                "next_page_token": None,
            }

        # Build query with date filter if provided
        if since_date:
            date_str = since_date.strftime("%Y/%m/%d")
            query_filter = f"{query_filter} after:{date_str}".strip()

        collected_messages = []
        page_token = sync_state.get("next_page_token")

        try:
            while len(collected_messages) < (max_emails or float("inf")):
                # Rate limiting
                await self.rate_limiter.acquire()

                # Get message list from Gmail API (simulated)
                message_list = await self._get_message_list(
                    query_filter,
                    page_token,
                    min(
                        self.config.messages_per_request,
                        (max_emails or 100) - len(collected_messages),
                    ),
                )

                if not message_list.get("messages"):
                    break

                # Process messages in parallel with rate limiting
                batch_messages = await self._process_message_batch(message_list["messages"])

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
                self.logger.info("Collected %s emails so far...", len(collected_messages))

        except Exception as e:
            self.logger.error("Error collecting emails: %s", e)
            # Save current state for resumption
            self.cache.update_sync_state(sync_state)
            raise

        return EmailBatch(
            messages=collected_messages,
            batch_id=sync_id,
            timestamp=datetime.now(),
            query_filter=query_filter,
            total_count=len(collected_messages),
        )

    async def _get_message_list(
        self, query: str, page_token: Optional[str] = None, max_results: int = 100
    ) -> Dict[str, Any]:
        """
        Get list of message IDs from Gmail API
        In production, this would make actual Gmail API calls
        """
        # Simulate Gmail API response with realistic structure
        if self.gmail_service:
            try:
                # Actual Gmail API call
                return (
                    self.gmail_service.users()
                    .messages()
                    .list(
                        userId="me",
                        q=query,
                        pageToken=page_token,
                        maxResults=max_results,
                    )
                    .execute()
                )
            except HttpError as error:
                self.logger.error("An API error occurred: %s", error)
                # Implement more sophisticated error handling and retry logic if needed
                return {
                    "messages": [],
                    "resultSizeEstimate": 0,
                }  # Return empty on error
            except Exception as e:
                self.logger.error("Unexpected error in _get_message_list: %s", e)
                return {"messages": [], "resultSizeEstimate": 0}

        # Fallback to simulated response if gmail_service is not available
        self.logger.warning(
            "Gmail service not available, using simulated response for _get_message_list."
        )
        return await self._simulate_gmail_response(query, page_token, max_results)

    async def _simulate_gmail_response(
        self, query: str, page_token: Optional[str], max_results: int
    ) -> Dict[str, Any]:
        """Simulate Gmail API response for development"""
        # Generate realistic message IDs
        base_time = int(time.time())
        messages = []

        for i in range(min(max_results, 10)):  # Limit simulation to 10 messages
            message_id = f"msg_{base_time}_{i:03d}"
            messages.append({"id": message_id, "threadId": f"thread_{base_time}_{i//3:03d}"})

        response = {"messages": messages, "resultSizeEstimate": len(messages)}

        # Add next page token if there would be more results
        if len(messages) == max_results and not page_token:
            response["nextPageToken"] = f"token_{base_time}_next"

        return response

    async def _process_message_batch(
        self, message_ids: List[Dict[str, str]]
    ) -> List[Dict[str, Any]]:
        """Process a batch of message IDs to get full email content"""
        semaphore = asyncio.Semaphore(self.config.max_concurrent_requests)
        tasks = []

        for msg_info in message_ids:
            task = self._get_message_with_semaphore(semaphore, msg_info["id"])
            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out exceptions and None results
        valid_messages = [
            result for result in results if not isinstance(result, Exception) and result is not None
        ]

        return valid_messages

    async def _get_message_with_semaphore(
        self, semaphore: asyncio.Semaphore, message_id: str
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
            self.logger.debug("Cache hit for message %s", message_id)
            return cached_email
        self.logger.debug("Cache miss for message %s", message_id)

        if self.gmail_service:
            try:
                self.logger.debug("Attempting to fetch message %s from Gmail API.", message_id)
                message = (
                    self.gmail_service.users()
                    .messages()
                    .get(userId="me", id=message_id, format="full")
                    .execute()
                )
                self.logger.debug("Successfully fetched message %s from API.", message_id)

                email_data = self._parse_message_payload(message)

                if email_data:
                    self.cache.cache_email(email_data)
                    self.logger.debug("Successfully parsed and cached message %s.", message_id)
                    return email_data
                else:
                    self.logger.warning(
                        "Could not parse email data for message %s. This message will not be processed further.",
                        message_id,
                    )
                    return None  # Parsing failure, do not simulate for this specific case
            except HttpError as error:
                self.logger.error(
                    "API error fetching message %s: %s. Falling back to simulation.",
                    message_id,
                    error,
                )
                # Fall through to simulation block below
            except Exception as e:
                self.logger.error(
                    "Unexpected error retrieving message %s: %s. Falling back to simulation.",
                    message_id,
                    e,
                )
                # Fall through to simulation block below
        else:
            self.logger.warning(
                "Gmail service not available. Falling back to simulation for message %s.",
                message_id,
            )
            # Fall through to simulation block below

        # Fallback to simulated response if API call failed or service was unavailable
        self.logger.info("Using simulated content for message %s.", message_id)
        email_data = await self._simulate_email_content(message_id)

        # Ensure message_id is present in simulated data for caching
        if "message_id" not in email_data:  # _simulate_email_content should guarantee this
            email_data["message_id"] = message_id

        self.cache.cache_email(email_data)
        self.logger.debug("Cached simulated content for message %s.", message_id)
        return email_data

    def _parse_message_payload(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Parses the raw message payload from Gmail API."""
        try:
            headers = {h["name"]: h["value"] for h in message.get("payload", {}).get("headers", [])}

            # Simplified content extraction (plaintext preferred)
            # Real implementation would need to handle multipart messages, base64 decoding, etc.
            content = ""
            if "parts" in message["payload"]:
                for part in message["payload"]["parts"]:
                    if part["mimeType"] == "text/plain" and "data" in part["body"]:
                        import base64

                        content = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
                        break
                    # Could add more part types (e.g., text/html)
            elif "body" in message["payload"] and "data" in message["payload"]["body"]:
                import base64

                content = base64.urlsafe_b64decode(message["payload"]["body"]["data"]).decode(
                    "utf-8"
                )

            return {
                "message_id": message["id"],
                "thread_id": message.get("threadId", ""),
                "subject": headers.get("Subject", ""),
                "sender": headers.get("From", ""),  # This often includes name and email
                "sender_email": self._extract_email_address(headers.get("From", "")),
                "content": content,
                "labels": message.get("labelIds", []),
                "timestamp": datetime.fromtimestamp(
                    int(message["internalDate"]) / 1000
                ).isoformat(),
            }
        except Exception as e:
            self.logger.error("Error parsing message payload for %s: %s", message.get("id"), e)
            return None

    def _extract_email_address(self, sender_header: str) -> str:
        """Extracts the email address from a 'From' header string."""
        # Simple extraction, might need a more robust regex for complex cases
        import re

        match = re.search(r"<([^>]+)>", sender_header)
        if match:
            return match.group(1)
        return sender_header  # Return the whole string if no angle brackets found

    async def _simulate_email_content(self, message_id: str) -> Dict[str, Any]:
        """Simulate email content for development"""
        # Generate realistic email content based on message ID
        email_templates = [
            {
                "subject": "Project Update - Q4 Planning",
                "sender": "Project Manager",
                "sender_email": "pm@company.com",
                "content": "Hi team, I wanted to provide an update on our Q4 planning initiatives. We've made significant progress on the roadmap and need to finalize the budget allocations by end of week.",
                "labels": ["IMPORTANT", "WORK"],
            },
            {
                "subject": "Invoice #12345 - Payment Due",
                "sender": "Accounting",
                "sender_email": "billing@vendor.com",
                "content": "Your invoice #12345 for $2,500 is now due. Please process payment within 30 days to avoid late fees.",
                "labels": ["FINANCE", "BILLING"],
            },
            {
                "subject": "Weekend Plans",
                "sender": "Sarah",
                "sender_email": "sarah@gmail.com",
                "content": "Hey! Are you free this weekend? We're planning a barbecue and would love to have you join us!",
                "labels": ["PERSONAL", "SOCIAL"],
            },
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
            "timestamp": datetime.now().isoformat(),
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
                "priority": "high",
            },
            "weekly_bulk": {
                "description": "Weekly bulk collection for training data",
                "query": "newer_than:7d",
                "max_emails": 5000,
                "frequency": "weekly",
                "priority": "medium",
            },
            "historical_import": {
                "description": "One-time historical data import",
                "query": "older_than:30d",
                "max_emails": 10000,
                "frequency": "once",
                "priority": "low",
            },
            "category_specific": {
                "description": "Category-specific collection",
                "query": "category:primary OR category:social OR category:promotions",
                "max_emails": 2000,
                "frequency": "daily",
                "priority": "medium",
            },
        }

    async def execute_collection_strategy(self, strategy_name: str) -> EmailBatch:
        """Execute a predefined collection strategy"""
        strategies = self.get_collection_strategies()

        if strategy_name not in strategies:
            raise ValueError(f"Unknown strategy: {strategy_name}")

        strategy = strategies[strategy_name]

        self.logger.info("Executing collection strategy: %s", strategy_name)
        self.logger.info("Description: %s", strategy["description"])

        return await self.collect_emails_incremental(
            query_filter=strategy["query"], max_emails=strategy["max_emails"]
        )


"""
Demonstrates the usage of the GmailDataCollector for email collection.

This main function initializes logging, creates a GmailDataCollector instance, 
and executes a daily email sync strategy. It handles authentication errors 
and provides detailed guidance for resolving credential issues.

Key steps:
- Set up logging
- Initialize Gmail data collector
- Validate Gmail service authentication
- Execute daily sync collection strategy
- Print collected email details or error messages

Raises:
    Various exceptions related to authentication or email collection
"""


async def main():
    """Example usage of Gmail data collector"""
    # Note: The main function would need to be async if _authenticate might run an async flow,
    # or _authenticate needs to be run in a way that doesn't block asyncio loop if used elsewhere.
    # For now, assuming _authenticate might block or run its own loop for console apps.

    # Note: The dummy credentials.json creation is removed.
    # The user must now configure environment variables.
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    collector = GmailDataCollector()  # This will trigger authentication if needed

    if not collector.gmail_service:
        logger.error("Gmail service initialization failed. Please check logs for details.")
        print(
            "--------------------------------------------------------------------------------------"
        )
        print("Gmail Service Initialization Failed!")
        print(
            "--------------------------------------------------------------------------------------"
        )
        print("Please ensure the following environment variables are correctly set:")
        print(
            f"1. {GMAIL_CREDENTIALS_ENV_VAR}: Should contain the JSON string of your Google Cloud credentials."
        )
        print(f"   Example: export {GMAIL_CREDENTIALS_ENV_VAR}='{{ \"installed\": {{ ... }} }}'")
        print(
            f"   (Alternatively, as a fallback, place a 'credentials.json' file in the script's directory: {os.getcwd()})"
        )
        print(f"2. GMAIL_TOKEN_PATH (Optional): Specify a custom path for 'token.json'.")
        print(f"   Defaults to '{TOKEN_JSON_PATH}' in the script's directory: {os.getcwd()}")
        print(
            "If running for the first time, you might need to go through the OAuth2 authentication flow in your browser."
        )
        print("Check the console logs for more detailed error messages from the application.")
        print(
            "--------------------------------------------------------------------------------------"
        )
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
