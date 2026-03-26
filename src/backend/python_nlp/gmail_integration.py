"""
Integrates with the Gmail API for efficient and robust email data retrieval.

This module provides a comprehensive solution for interacting with the Gmail
API, featuring smart batching, caching, rate limit management, and a
pluggable authentication mechanism. It is designed to be resilient and
efficient, even when dealing with large volumes of emails.
"""

import asyncio
import dataclasses
import hashlib
import json
import logging
import os
import re
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

from src.core.security import PathValidator

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
# Define the project's root directory and default path for the email cache
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CACHE_PATH = PROJECT_ROOT / "email_cache.db"

# Path for token.json, configurable via environment variable
TOKEN_JSON_PATH = os.getenv("GMAIL_TOKEN_PATH", "jsons/token.json")
CREDENTIALS_PATH = "jsons/credentials.json"
GMAIL_CREDENTIALS_ENV_VAR = "GMAIL_CREDENTIALS_JSON"


@dataclasses.dataclass
class RateLimitConfig:
    """
    Configuration for managing Gmail API rate limits.

    Attributes:
        queries_per_day: The total number of quota units allowed per day.
        queries_per_100_seconds: The number of quota units per 100 seconds.
        queries_per_second: A practical limit to avoid request bursts.
        messages_per_request: The maximum number of messages per list request.
        max_concurrent_requests: The maximum number of concurrent API calls.
        initial_backoff: The initial backoff duration in seconds for retries.
        max_backoff: The maximum backoff duration in seconds.
        backoff_multiplier: The multiplier for exponential backoff.
    """

    queries_per_day: int = 1000000000
    queries_per_100_seconds: int = 250
    queries_per_second: int = 5
    messages_per_request: int = 100
    max_concurrent_requests: int = 10
    initial_backoff: float = 1.0
    max_backoff: float = 60.0
    backoff_multiplier: float = 2.0


@dataclasses.dataclass
@dataclasses.dataclass
class EmailBatch:
    """
    Represents a batch of emails retrieved from the Gmail API.

    Attributes:
        messages: A list of email data dictionaries.
        batch_id: A unique identifier for this batch.
        timestamp: The timestamp when the batch was created.
        query_filter: The filter query used to retrieve this batch.
        total_count: The total number of emails in the batch.
    """

    messages: List[Dict[str, Any]]
    batch_id: str
    timestamp: datetime
    query_filter: str
    total_count: int


class RateLimiter:
    """
    Implements a token bucket rate limiting algorithm for the Gmail API.

    This class helps to avoid exceeding the API's rate limits by controlling
    the frequency of outgoing requests.
    """

    def __init__(self, config: RateLimitConfig):
        """Initializes the RateLimiter."""
        self.config = config
        self.tokens: float = config.queries_per_second
        self.last_update = time.time()
        self.request_times: deque[float] = deque()

    async def acquire(self) -> None:
        """
        Acquires permission to make an API request, blocking if necessary.
        """
        current_time = time.time()

        while self.request_times and current_time - self.request_times[0] > 100:
            self.request_times.popleft()

        if len(self.request_times) >= self.config.queries_per_100_seconds:
            sleep_time = 100 - (current_time - self.request_times[0])
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)

        time_passed = current_time - self.last_update
        self.tokens = min(
            self.config.queries_per_second,
            self.tokens + time_passed * (self.config.queries_per_second / 1.0),
        )
        self.last_update = current_time

        if self.tokens < 1:
            sleep_time = (1 - self.tokens) / self.config.queries_per_second
            await asyncio.sleep(sleep_time)
            self.tokens = 0
        else:
            self.tokens -= 1

        self.request_times.append(current_time)


class EmailCache:
    """
    Provides a SQLite-based cache for email metadata and content.

    This helps to reduce redundant API calls by storing previously fetched
    email data and synchronization states.
    """

    def __init__(self, cache_path: str = str(DEFAULT_CACHE_PATH)):
        """Initializes the EmailCache."""
        # Secure path validation
        self.cache_path = str(
            PathValidator.validate_database_path(cache_path, Path(cache_path).parent)
        )
        self.conn = sqlite3.connect(self.cache_path, check_same_thread=False)
        self._init_cache()

    def _init_cache(self):
        """Initializes the cache database tables if they don't exist."""
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS emails (
                message_id TEXT PRIMARY KEY, thread_id TEXT, subject TEXT,
                sender TEXT, sender_email TEXT, content TEXT, labels TEXT,
                timestamp TEXT, retrieved_at TEXT, content_hash TEXT
            )
            """
        )
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS sync_metadata (
                sync_id TEXT PRIMARY KEY, query_filter TEXT, last_sync TEXT,
                total_messages INTEGER, processed_messages INTEGER, next_page_token TEXT
            )
            """
        )
        self.conn.commit()

    def get_cached_email(self, message_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a cached email by its message ID."""
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
        """Caches a single email's data."""
        content_hash = hashlib.md5(email_data.get("content", "").encode()).hexdigest()
        self.conn.execute(
            "INSERT OR REPLACE INTO emails VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
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
        """Retrieves the synchronization state for a given query filter."""
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
        """Updates the synchronization state in the cache."""
        self.conn.execute(
            "INSERT OR REPLACE INTO sync_metadata VALUES (?, ?, ?, ?, ?, ?)",
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
    Collects data from the Gmail API with rate limiting, caching, and authentication.

    This class orchestrates the entire process of fetching emails, handling
    API credentials, managing rate limits, and caching results to ensure
    efficient and reliable data collection.
    """

    def __init__(self, config: Optional[RateLimitConfig] = None):
        """Initializes the GmailDataCollector."""
        self.config = config or RateLimitConfig()
        self.rate_limiter = RateLimiter(self.config)
        self.cache = EmailCache()
        self.logger = logging.getLogger(__name__)
        self.gmail_service = None
        self._load_credentials()
        if not self.gmail_service:
            self._authenticate()

    def _load_credentials(self):
        """Loads API credentials from a token file if it exists."""
        creds = None
        if os.path.exists(TOKEN_JSON_PATH):
            try:
                creds = Credentials.from_authorized_user_file(TOKEN_JSON_PATH, SCOPES)
            except Exception as e:
                self.logger.error(f"Error loading credentials from {TOKEN_JSON_PATH}: {e}")
        if creds and creds.valid:
            self.gmail_service = build("gmail", "v1", credentials=creds)
        elif creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                self.gmail_service = build("gmail", "v1", credentials=creds)
                self._store_credentials(creds)
            except Exception as e:
                self.logger.error(f"Error refreshing credentials: {e}")

    def _store_credentials(self, creds):
        """Stores the API credentials to a token file."""
        try:
            with open(TOKEN_JSON_PATH, "w") as token_file:
                token_file.write(creds.to_json())
            self.logger.info(f"Credentials stored in {TOKEN_JSON_PATH}")
        except OSError as e:
            self.logger.error(f"Error storing credentials to {TOKEN_JSON_PATH}: {e}")

    def _authenticate(self):
        """
        Authenticates the user via the OAuth 2.0 flow.

        It first tries to load credentials from the GMAIL_CREDENTIALS_JSON
        environment variable. If that fails, it falls back to a local
        'credentials.json' file.
        """
        creds = None
        credentials_json_str = os.getenv(GMAIL_CREDENTIALS_ENV_VAR)
        if credentials_json_str:
            try:
                credentials_info = json.loads(credentials_json_str)
                flow = InstalledAppFlow.from_client_config(credentials_info, SCOPES)
            except (json.JSONDecodeError, Exception) as e:
                self.logger.error(f"Error loading credentials from env var: {e}")
                return
        elif os.path.exists(CREDENTIALS_PATH):
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
        else:
            self.logger.error("No valid credentials source found.")
            return

        try:
            creds = flow.run_local_server(port=0)
            self._store_credentials(creds)
            self.gmail_service = build("gmail", "v1", credentials=creds)
            self.logger.info("Authentication successful.")
        except Exception as e:
            self.logger.error(f"OAuth flow failed: {e}")

    def set_gmail_service(self, service):
        """Sets the Gmail API service instance."""
        self.logger.warning("set_gmail_service is deprecated as auth is handled internally.")
        self.gmail_service = service

    async def collect_emails_incremental(
        self,
        query_filter: str = "",
        max_emails: Optional[int] = None,
        since_date: Optional[datetime] = None,
    ) -> EmailBatch:
        """
        Collects emails incrementally, using caching and rate limiting.

        Args:
            query_filter: The Gmail search query to filter emails.
            max_emails: The maximum number of emails to collect.
            since_date: The date from which to start collecting emails.

        Returns:
            An EmailBatch object containing the collected emails.
        """
        sync_id = hashlib.md5(f"{query_filter}_{datetime.now().date()}".encode()).hexdigest()
        sync_state = self.cache.get_sync_state(query_filter) or {
            "sync_id": sync_id,
            "query_filter": query_filter,
            "last_sync": datetime.now().isoformat(),
            "total_messages": 0,
            "processed_messages": 0,
            "next_page_token": None,
        }
        if since_date:
            query_filter = f"{query_filter} after:{since_date.strftime('%Y/%m/%d')}".strip()

        collected_messages: List[Dict[str, Any]] = []
        page_token = sync_state.get("next_page_token")
        try:
            while len(collected_messages) < (max_emails or float("inf")):
                await self.rate_limiter.acquire()
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
                batch_messages = await self._process_message_batch(message_list["messages"])
                collected_messages.extend(batch_messages)
                sync_state.update(
                    {
                        "processed_messages": sync_state["processed_messages"]
                        + len(batch_messages),
                        "next_page_token": message_list.get("nextPageToken"),
                        "last_sync": datetime.now().isoformat(),
                    }
                )
                self.cache.update_sync_state(sync_state)
                if not message_list.get("nextPageToken"):
                    break
                page_token = message_list["nextPageToken"]
                self.logger.info(f"Collected {len(collected_messages)} emails so far...")
        except Exception as e:
            self.logger.error(f"Error collecting emails: {e}")
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
        """Retrieves a list of message IDs from the Gmail API."""
        if self.gmail_service:
            try:
                return (
                    self.gmail_service.users()
                    .messages()
                    .list(userId="me", q=query, pageToken=page_token, maxResults=max_results)
                    .execute()
                )
            except HttpError as error:
                self.logger.error(f"An API error occurred: {error}")
                return {"messages": [], "resultSizeEstimate": 0}
            except Exception as e:
                self.logger.error(f"Unexpected error in _get_message_list: {e}")
                return {"messages": [], "resultSizeEstimate": 0}
        self.logger.warning("Gmail service not available, using simulated response.")
        return await self._simulate_gmail_response(query, page_token, max_results)

    async def _simulate_gmail_response(
        self, query: str, page_token: Optional[str], max_results: int
    ) -> Dict[str, Any]:
        """Simulates a Gmail API response for development purposes."""
        base_time = int(time.time())
        messages = [
            {"id": f"msg_{base_time}_{i:03d}", "threadId": f"thread_{base_time}_{i // 3:03d}"}
            for i in range(min(max_results, 10))
        ]
        response = {"messages": messages, "resultSizeEstimate": len(messages)}
        if len(messages) == max_results and not page_token:
            response["nextPageToken"] = f"token_{base_time}_next"
        return response

    async def _process_message_batch(
        self, message_ids: List[Dict[str, str]]
    ) -> List[Dict[str, Any]]:
        """Processes a batch of message IDs to retrieve their full content."""
        semaphore = asyncio.Semaphore(self.config.max_concurrent_requests)
        tasks = [
            self._get_message_with_semaphore(semaphore, msg_info["id"]) for msg_info in message_ids
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return [
            res for res in results if res and not isinstance(res, Exception)
        ]  # type: ignore [misc]

    async def _get_message_with_semaphore(
        self, semaphore: asyncio.Semaphore, message_id: str
    ) -> Optional[Dict[str, Any]]:
        """Retrieves message content under the control of a semaphore."""
        async with semaphore:
            await self.rate_limiter.acquire()
            return await self._get_message_content(message_id)

    async def _get_message_content(self, message_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves the full content of a message, using a cache to avoid
        redundant API calls.
        """
        if cached_email := self.cache.get_cached_email(message_id):
            self.logger.debug(f"Cache hit for message {message_id}")
            return cached_email
        self.logger.debug(f"Cache miss for message {message_id}")
        if self.gmail_service:
            try:
                self.logger.debug(f"Fetching message {message_id} from Gmail API.")
                message = (
                    self.gmail_service.users()
                    .messages()
                    .get(userId="me", id=message_id, format="full")
                    .execute()
                )
                if email_data := self._parse_message_payload(message):
                    self.cache.cache_email(email_data)
                    return email_data
            except (HttpError, Exception) as e:
                self.logger.error(f"Error fetching message {message_id}: {e}")
        self.logger.info(f"Using simulated content for message {message_id}.")
        email_data = await self._simulate_email_content(message_id)
        self.cache.cache_email(email_data)
        return email_data

    def _parse_message_payload(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Parses the raw payload of a message from the Gmail API."""
        try:
            headers = {h["name"]: h["value"] for h in message.get("payload", {}).get("headers", [])}
            content = ""
            if "parts" in message["payload"]:
                for part in message["payload"]["parts"]:
                    if part["mimeType"] == "text/plain" and "data" in part["body"]:
                        import base64

                        content = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
                        break
            elif "body" in message["payload"] and "data" in message["payload"]["body"]:
                import base64

                content = base64.urlsafe_b64decode(message["payload"]["body"]["data"]).decode(
                    "utf-8"
                )
            return {
                "message_id": message["id"],
                "thread_id": message.get("threadId", ""),
                "subject": headers.get("Subject", ""),
                "sender": headers.get("From", ""),
                "sender_email": self._extract_email_address(headers.get("From", "")),
                "content": content,
                "labels": message.get("labelIds", []),
                "timestamp": datetime.fromtimestamp(
                    int(message["internalDate"]) / 1000
                ).isoformat(),
            }
        except Exception as e:
            self.logger.error(f"Error parsing message payload for {message.get('id')}: {e}")
            return None

    def _extract_email_address(self, sender_header: str) -> str:
        """Extracts the email address from a 'From' header string."""
        from email.utils import parseaddr
        # Use parseaddr to robustly extract the email address from the header
        name, email_addr = parseaddr(sender_header)
        return email_addr if email_addr else sender_header

    async def _simulate_email_content(self, message_id: str) -> Dict[str, Any]:
        """Simulates email content for development and testing."""
        templates = [
            {
                "subject": "Project Update",
                "sender": "pm@company.com",
                "content": "Update on Q4 planning...",
                "labels": ["WORK"],
            },
            {
                "subject": "Invoice #12345",
                "sender": "billing@vendor.com",
                "content": "Your invoice is due.",
                "labels": ["FINANCE"],
            },
            {
                "subject": "Weekend Plans",
                "sender": "sarah@gmail.com",
                "content": "Barbecue this weekend?",
                "labels": ["PERSONAL"],
            },
        ]
        template = templates[hash(message_id) % len(templates)]
        return {
            "message_id": message_id,
            "thread_id": f"thread_{message_id.split('_')[1]}",
            "subject": template["subject"],
            "sender": template["sender"],
            "sender_email": template["sender"],
            "content": template["content"],
            "labels": template["labels"],
            "timestamp": datetime.now().isoformat(),
        }

    def get_collection_strategies(self) -> Dict[str, Dict[str, Any]]:
        """Defines a set of named strategies for collecting emails."""
        return {
            "daily_sync": {
                "description": "Daily sync for recent emails",
                "query": "newer_than:1d",
                "max_emails": 1000,
            },
            "weekly_bulk": {
                "description": "Weekly bulk collection",
                "query": "newer_than:7d",
                "max_emails": 5000,
            },
            "historical_import": {
                "description": "One-time historical import",
                "query": "older_than:30d",
                "max_emails": 10000,
            },
        }

    async def execute_collection_strategy(self, strategy_name: str) -> EmailBatch:
        """Executes a predefined email collection strategy."""
        strategies = self.get_collection_strategies()
        if strategy_name not in strategies:
            raise ValueError(f"Unknown strategy: {strategy_name}")
        strategy = strategies[strategy_name]
        self.logger.info(f"Executing strategy: {strategy_name} - {strategy['description']}")
        return await self.collect_emails_incremental(
            query_filter=strategy["query"], max_emails=strategy["max_emails"]
        )


async def main():
    """Demonstrates the usage of the GmailDataCollector."""
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    logger = logging.getLogger(__name__)
    collector = GmailDataCollector()
    if not collector.gmail_service:
        logger.error("Gmail service initialization failed. Please check credentials.")
        return
    try:
        if batch := await collector.execute_collection_strategy("daily_sync"):
            print(f"Collected {batch.total_count} emails.")
            for email in batch.messages[:3]:
                print(f"  - Subject: {email['subject']}")
    except Exception as e:
        logger.exception(f"Collection failed: {e}")


if __name__ == "__main__":
    asyncio.run(main())
