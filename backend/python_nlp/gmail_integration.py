"""Gmail API Integration with Rate Limiting and Efficient Data Retrieval
Implements smart batching, caching, and rate limit management for email collection
"""

import dataclasses
from typing import List, Optional

@dataclasses.dataclass
import asyncio
import hashlib
import json
import logging
import os
import sqlite3
import time
from collections import deque
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
TOKEN_JSON_PATH = os.getenv("GMAIL_TOKEN_PATH", "token.json")
CREDENTIALS_PATH = "credentials.json"
GMAIL_CREDENTIALS_ENV_VAR = "GMAIL_CREDENTIALS_JSON"


@dataclass
class RateLimitConfig:
    """Configuration for rate limiting."""
    max_calls: int = 5
    period_seconds: int = 60

@dataclasses.dataclass
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


@dataclass
class EmailBatch:
    """Represents a batch of emails."""
    emails: List[dict]

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
    the frequency of outgoing requests. It implements both per-second and
    per-minute rate limiting.
    """

    def __init__(self, config: RateLimitConfig):
        """Initializes the RateLimiter."""
        self.config = config
        self.tokens_per_second = config.queries_per_second
        self.tokens_per_minute = config.queries_per_minute // 60  # Convert to per-second rate
        self.last_second_update = time.time()
        self.last_minute_update = time.time()
        self.request_times_100s = deque()  # For 100-second window
        self.request_times_minute = deque()  # For per-minute tracking

    async def acquire(self) -> None:
        """
        Acquires permission to make an API request, blocking if necessary.
        """
        current_time = time.time()

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

        # Record the request
        self.request_times_100s.append(current_time)
        self.request_times_minute.append(current_time)


class EmailCache:
    """
    Provides a SQLite-based cache for email metadata and content.

    This helps to reduce redundant API calls by storing previously fetched
    email data and synchronization states.
    """

    def __init__(self, cache_path: str = "email_cache.db"):
        """Initializes the EmailCache."""
        self.cache_path = cache_path
        self.conn = sqlite3.connect(cache_path, check_same_thread=False)
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
                "message_id": row[0], "thread_id": row[1], "subject": row[2],
                "sender": row[3], "sender_email": row[4], "content": row[5],
                "labels": json.loads(row[6]) if row[6] else [], "timestamp": row[7],
                "retrieved_at": row[8], "content_hash": row[9],
            }
        return None

    def cache_email(self, email_data: Dict[str, Any]) -> None:
        """Caches a single email's data."""
        content_hash = hashlib.md5(email_data.get("content", "").encode()).hexdigest()
        self.conn.execute(
            "INSERT OR REPLACE INTO emails VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                email_data["message_id"], email_data.get("thread_id", ""),
                email_data.get("subject", ""), email_data.get("sender", ""),
                email_data.get("sender_email", ""), email_data.get("content", ""),
                json.dumps(email_data.get("labels", [])), email_data.get("timestamp", ""),
                datetime.now().isoformat(), content_hash,
            ),
        )
        self.conn.commit()

    def get_sync_state(self, query_filter: str) -> Optional[Dict[str, Any]]:
        """Retrieves the synchronization state for a given query filter."""
        cursor = self.conn.execute("SELECT * FROM sync_metadata WHERE query_filter = ?", (query_filter,))
        row = cursor.fetchone()
        if row:
            return {
                "sync_id": row[0], "query_filter": row[1], "last_sync": row[2],
                "total_messages": row[3], "processed_messages": row[4], "next_page_token": row[5],
            }
        return None

    def update_sync_state(self, sync_data: Dict[str, Any]) -> None:
        """Updates the synchronization state in the cache."""
        self.conn.execute(
            "INSERT OR REPLACE INTO sync_metadata VALUES (?, ?, ?, ?, ?, ?)",
            (
                sync_data["sync_id"], sync_data["query_filter"], sync_data["last_sync"],
                sync_data["total_messages"], sync_data["processed_messages"],
                sync_data.get("next_page_token", ""),
            ),
        )
        self.conn.commit()


class GmailDataCollector:
    """Collects data from Gmail with rate limiting."""

    def __init__(self, rate_config: Optional[RateLimitConfig] = None):
        """Initializes the data collector."""
        self.rate_config = rate_config or RateLimitConfig()

    def fetch_emails(self, query: str, max_count: int) -> EmailBatch:
        """Fetches emails from Gmail."""
        # This is a mock implementation.
        # In a real implementation, this would connect to the Gmail API.
        print(f"Fetching emails with query: {query}, max_count: {max_count}")
        return EmailBatch(emails=[])
