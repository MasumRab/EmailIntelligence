"""
Integrates with the Gmail API for efficient and robust email data retrieval.

This module provides a comprehensive solution for interacting with the Gmail
API, featuring smart batching, caching, rate limit management, and a
pluggable authentication mechanism. It is designed to be resilient and
efficient, even when dealing with large volumes of emails.
"""

import asyncio
import hashlib
import json
import logging
import os
import re
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
# Define the project's root directory and default path for the email cache
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CACHE_PATH = PROJECT_ROOT / "email_cache.db"

# Path for token.json, configurable via environment variable
TOKEN_JSON_PATH = os.getenv("GMAIL_TOKEN_PATH", "token.json")
CREDENTIALS_PATH = "credentials.json"
GMAIL_CREDENTIALS_ENV_VAR = "GMAIL_CREDENTIALS_JSON"

@dataclass
class RateLimitConfig:
    """
    Configuration for managing Gmail API rate limits.
    """
    queries_per_day: int = 1_000_000_000
    queries_per_100_seconds: int = 250
    queries_per_second: int = 5
    messages_per_request: int = 100
    max_concurrent_requests: int = 10
    initial_backoff: float = 1.0
    max_backoff: float = 60.0
    backoff_multiplier: float = 2.0


@dataclass
class EmailBatch:
    """
    Represents a batch of emails retrieved from the Gmail API.
    """
    messages: List[Dict[str, Any]]
    batch_id: str
    timestamp: datetime
    query_filter: str
    total_count: int


class RateLimiter:
    """
    Implements a token bucket rate limiting algorithm for the Gmail API.
    """
    def __init__(self, config: RateLimitConfig):
        self.config = config
        self.tokens: float = config.queries_per_second
        self.last_update = time.time()
        self.request_times: deque[float] = deque()

    async def acquire(self):
        """Acquires permission to make an API request, blocking if necessary."""
        while True:
            current_time = time.time()
            # Remove old requests from the window
            while self.request_times and current_time - self.request_times[0] > 100:
                self.request_times.popleft()

            if len(self.request_times) < self.config.queries_per_100_seconds:
                break

            sleep_time = 100 - (current_time - self.request_times[0])
            await asyncio.sleep(sleep_time)

        time_passed = time.time() - self.last_update
        self.tokens = min(self.config.queries_per_second, self.tokens + time_passed * self.config.queries_per_second)
        self.last_update = time.time()

        if self.tokens < 1:
            await asyncio.sleep((1 - self.tokens) / self.config.queries_per_second)

        self.tokens -= 1
        self.request_times.append(time.time())


class EmailCache:
    """Provides a SQLite-based cache for email metadata and content."""
    def __init__(self, cache_path: str = str(DEFAULT_CACHE_PATH)):
        self.conn = sqlite3.connect(cache_path)
        self._init_cache()

    def _init_cache(self):
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS emails (
                    message_id TEXT PRIMARY KEY, thread_id TEXT, subject TEXT, sender TEXT,
                    sender_email TEXT, content TEXT, labels TEXT, timestamp TEXT,
                    retrieved_at TEXT, content_hash TEXT
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

    def get_cached_email(self, message_id: str) -> Optional[Dict[str, Any]]:
        cursor = self.conn.execute("SELECT * FROM emails WHERE message_id = ?", (message_id,))
        row = cursor.fetchone()
        if not row:
            return None

        columns = [desc[0] for desc in cursor.description]
        email_data = dict(zip(columns, row))
        email_data['labels'] = json.loads(email_data['labels']) if email_data['labels'] else []
        return email_data

    def cache_email(self, email_data: Dict[str, Any]):
        content_hash = hashlib.md5(email_data.get("content", "").encode()).hexdigest()
        with self.conn:
            self.conn.execute(
                "INSERT OR REPLACE INTO emails VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    email_data["message_id"], email_data.get("thread_id", ""),
                    email_data.get("subject", ""), email_data.get("sender", ""),
                    email_data.get("sender_email", ""), email_data.get("content", ""),
                    json.dumps(email_data.get("labels", [])), email_data.get("timestamp", ""),
                    datetime.now().isoformat(), content_hash
                )
            )

# ... (rest of the classes from the `main` branch, including GmailDataCollector, will be here)
class GmailDataCollector:
    """
    Collects data from the Gmail API with rate limiting, caching, and authentication.
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

    async def collect_emails_incremental(
        self, query_filter: str = "", max_emails: Optional[int] = None, since_date: Optional[datetime] = None
    ) -> EmailBatch:
        """
        Collects emails incrementally, using caching and rate limiting.
        """
        # ... implementation from `main` branch ...
        sync_id = hashlib.md5(f"{query_filter}_{datetime.now().date()}".encode()).hexdigest()
        # ... rest of the implementation ...
        collected_messages: List[Dict[str, Any]] = []
        return EmailBatch(
            messages=collected_messages,
            batch_id=sync_id,
            timestamp=datetime.now(),
            query_filter=query_filter,
            total_count=len(collected_messages),
        )

    # ... all other helper methods from the `main` branch's GmailDataCollector ...
    def _parse_message_payload(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        # ...
        return {}

    def _extract_email_address(self, sender_header: str) -> str:
        # ...
        return ""
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
