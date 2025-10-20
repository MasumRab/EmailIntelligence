"""
Smart Gmail Retrieval with Advanced Filtering and Batching Strategies
Implements intelligent filtering, date-based incremental sync, and optimized batch processing
"""

import argparse
import asyncio
import json
import logging
import os
import sqlite3
import sys
from dataclasses import asdict, dataclass
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

# Define the project's root directory and default path for the checkpoint database
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_CHECKPOINT_DB_PATH = os.path.join(PROJECT_ROOT, "sync_checkpoints.db")


@dataclass
class RetrievalStrategy:
    """Configuration for smart retrieval strategy"""
    name: str
    query_filter: str
    priority: int
    batch_size: int
    frequency: str
    max_emails_per_run: int
    include_folders: List[str]
    exclude_folders: List[str]
    date_range_days: int


@dataclass
class SyncCheckpoint:
    """Checkpoint for incremental synchronization"""
    strategy_name: str
    last_sync_date: datetime
    last_history_id: str
    processed_count: int
    next_page_token: Optional[str]
    errors_count: int


class SmartGmailRetriever:
    """Advanced Gmail retrieval with intelligent filtering and batching"""

    def __init__(self, checkpoint_db_path: str = DEFAULT_CHECKPOINT_DB_PATH):
        self.logger = logging.getLogger(__name__)
        self.checkpoint_db_path = checkpoint_db_path
        self.gmail_service = None
        self._init_checkpoint_db()
        creds = self._load_credentials() or self._authenticate()
        if creds and creds.valid:
            try:
                self.gmail_service = build("gmail", "v1", credentials=creds)
                self._store_credentials(creds)
                self.logger.info("Gmail service initialized successfully.")
            except Exception as e:
                self.logger.error(f"Failed to build Gmail service: {e}")
                self.gmail_service = None
        else:
            self.logger.error("Failed to obtain valid credentials.")

        self.api_limits = {"daily_quota": 1_000_000_000, "per_user_per_100_seconds": 250}

    def _init_checkpoint_db(self):
        """Initialize checkpoint database for sync state management"""
        with sqlite3.connect(self.checkpoint_db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS sync_checkpoints (
                    strategy_name TEXT PRIMARY KEY, last_sync_date TEXT, last_history_id TEXT,
                    processed_count INTEGER DEFAULT 0, next_page_token TEXT, errors_count INTEGER DEFAULT 0,
                    created_at TEXT, updated_at TEXT
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS retrieval_stats (
                    date TEXT PRIMARY KEY, total_retrieved INTEGER DEFAULT 0, api_calls_used INTEGER DEFAULT 0,
                    quota_remaining INTEGER DEFAULT 0, strategies_executed TEXT, performance_metrics TEXT
                )
                """
            )

    def _load_credentials(self) -> Optional[Credentials]:
        """Loads credentials from TOKEN_JSON_PATH if it exists."""
        if os.path.exists(TOKEN_JSON_PATH):
            return Credentials.from_authorized_user_file(TOKEN_JSON_PATH, SCOPES)
        return None

    def _store_credentials(self, creds: Credentials):
        """Stores credentials to TOKEN_JSON_PATH."""
        with open(TOKEN_JSON_PATH, "w") as token_file:
            token_file.write(creds.to_json())

    def _authenticate(self) -> Optional[Credentials]:
        """Authenticates the user via OAuth flow and returns credentials."""
        flow = None
        creds_json_str = os.getenv(GMAIL_CREDENTIALS_ENV_VAR)
        if creds_json_str:
            try:
                creds_info = json.loads(creds_json_str)
                flow = InstalledAppFlow.from_client_config(creds_info, SCOPES)
            except (json.JSONDecodeError, Exception) as e:
                self.logger.error(f"Error loading credentials from env var: {e}")

        if not flow and os.path.exists(CREDENTIALS_PATH):
            try:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            except Exception as e:
                self.logger.error(f"Error loading credentials from file: {e}")
                return None

        if not flow:
            self.logger.error("Could not configure authentication flow.")
            return None

        try:
            creds = flow.run_local_server(port=0)
            if creds:
                self._store_credentials(creds)
            return creds
        except Exception as e:
            self.logger.error(f"OAuth flow failed: {e}", exc_info=True)
            return None

    def get_optimized_retrieval_strategies(self) -> List[RetrievalStrategy]:
        """Generate optimized retrieval strategies based on folder types and priorities"""
        # A simplified but effective list of strategies
        return [
            RetrievalStrategy("critical_inbox", "in:inbox is:important newer_than:1h", 10, 50, "hourly", 200, ["INBOX", "IMPORTANT"], ["SPAM"], 1),
            RetrievalStrategy("personal_daily", "category:primary newer_than:1d", 7, 100, "daily", 500, ["CATEGORY_PERSONAL", "INBOX"], ["SPAM"], 3),
            RetrievalStrategy("promotions_weekly", "category:promotions newer_than:7d", 2, 100, "weekly", 1000, ["CATEGORY_PROMOTIONS"], ["SPAM"], 7),
        ]

    def get_incremental_query(self, strategy: RetrievalStrategy, checkpoint: Optional[SyncCheckpoint] = None) -> str:
        """Build incremental query based on checkpoint and strategy"""
        query = strategy.query_filter
        if checkpoint and checkpoint.last_sync_date:
            query += f" after:{int(checkpoint.last_sync_date.timestamp())}"
        return query

    async def execute_smart_retrieval(
        self, strategies: Optional[List[RetrievalStrategy]] = None, max_api_calls: int = 100, time_budget_minutes: int = 30
    ) -> Dict[str, Any]:
        """Execute smart retrieval with multiple strategies and rate limiting"""
        if not self.gmail_service:
            return {"success": False, "error": "Gmail service not initialized."}

        strategies_to_run = strategies or self.get_optimized_retrieval_strategies()
        results = {"strategies_executed": [], "total_emails_retrieved": 0, "api_calls_used": 0, "errors": []}
        start_time = datetime.now()

        for strategy in strategies_to_run:
            if (datetime.now() - start_time).total_seconds() / 60 > time_budget_minutes or results["api_calls_used"] >= max_api_calls:
                break

            checkpoint = self._load_checkpoint(strategy.name)
            query = self.get_incremental_query(strategy, checkpoint)

            try:
                strategy_result = await self._execute_strategy_retrieval(strategy, query, checkpoint, max_api_calls - results["api_calls_used"])
                results["strategies_executed"].append(strategy_result)
                results["total_emails_retrieved"] += strategy_result.get("emails_count", 0)
                results["api_calls_used"] += strategy_result.get("api_calls", 0)
                if not strategy_result.get("success"):
                    results["errors"].append({"strategy": strategy.name, "error": strategy_result.get("error")})
            except Exception as e:
                self.logger.error(f"Strategy {strategy.name} failed unexpectedly: {e}")
                results["errors"].append({"strategy": strategy.name, "error": str(e)})

        return results

    async def _execute_strategy_retrieval(self, strategy, query, checkpoint, remaining_api_calls) -> Dict:
        """Execute retrieval for a single strategy."""
        emails, api_calls, page_token = [], 0, (checkpoint.next_page_token if checkpoint else None)

        while len(emails) < strategy.max_emails_per_run and api_calls < remaining_api_calls:
            batch_result = await self._fetch_email_batch(query, strategy.batch_size, page_token)
            api_calls += 1 + len(batch_result.get("messages", [])) # list + get for each message

            if batch_result.get("error"):
                return {"success": False, "error": batch_result["error"], "api_calls": api_calls, "emails_count": len(emails)}

            emails.extend(batch_result.get("messages", []))
            page_token = batch_result.get("nextPageToken")
            if not page_token:
                break

        if emails:
            self._save_checkpoint(SyncCheckpoint(strategy.name, datetime.now(), emails[-1]['id'], len(emails), page_token, 0))

        return {"success": True, "strategy_name": strategy.name, "emails_count": len(emails), "api_calls": api_calls}

    async def _fetch_email_batch(self, query: str, batch_size: int, page_token: Optional[str] = None) -> Dict[str, Any]:
        """Fetch a batch of emails using Gmail API."""
        try:
            list_response = self.gmail_service.users().messages().list(userId="me", q=query, maxResults=batch_size, pageToken=page_token).execute()
            messages = []
            if "messages" in list_response:
                for msg_ref in list_response["messages"]:
                    msg = self.gmail_service.users().messages().get(userId="me", id=msg_ref["id"], format="metadata").execute()
                    messages.append(msg)
            return {"messages": messages, "nextPageToken": list_response.get("nextPageToken")}
        except HttpError as e:
            return {"error": str(e)}

    def _load_checkpoint(self, strategy_name: str) -> Optional[SyncCheckpoint]:
        """Load sync checkpoint for strategy"""
        with sqlite3.connect(self.checkpoint_db_path) as conn:
            cursor = conn.execute("SELECT last_sync_date, last_history_id, processed_count, next_page_token, errors_count FROM sync_checkpoints WHERE strategy_name = ?", (strategy_name,))
            row = cursor.fetchone()
            if row:
                return SyncCheckpoint(strategy_name, datetime.fromisoformat(row[0]), row[1], row[2], row[3], row[4])
        return None

    def _save_checkpoint(self, checkpoint: SyncCheckpoint):
        """Save sync checkpoint"""
        with sqlite3.connect(self.checkpoint_db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO sync_checkpoints (strategy_name, last_sync_date, last_history_id, processed_count, next_page_token, errors_count, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (checkpoint.strategy_name, checkpoint.last_sync_date.isoformat(), checkpoint.last_history_id, checkpoint.processed_count, checkpoint.next_page_token, checkpoint.errors_count, datetime.now().isoformat())
            )

async def main_cli():
    """Provides a command-line interface for the SmartGmailRetriever."""
    parser = argparse.ArgumentParser(description="Smart Gmail Retriever CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list-strategies", help="List available retrieval strategies")
    execute_parser = subparsers.add_parser("execute-strategies", help="Execute retrieval strategies")
    execute_parser.add_argument("--strategies", nargs="+", help="Names of specific strategies to execute")
    execute_parser.add_argument("--max-api-calls", type=int, default=100)
    execute_parser.add_argument("--time-budget-minutes", type=int, default=30)

    args = parser.parse_args()
    retriever = SmartGmailRetriever()

    if args.command == "list-strategies":
        strategies = retriever.get_optimized_retrieval_strategies()
        print(json.dumps([asdict(s) for s in strategies], indent=2))
    elif args.command == "execute-strategies":
        strategies_to_run = retriever.get_optimized_retrieval_strategies()
        if args.strategies:
            strategies_to_run = [s for s in strategies_to_run if s.name in args.strategies]

        results = await retriever.execute_smart_retrieval(strategies_to_run, args.max_api_calls, args.time_budget_minutes)
        print(json.dumps(results, indent=2))

if __name__ == "__main__":
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper(), format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    asyncio.run(main_cli())
