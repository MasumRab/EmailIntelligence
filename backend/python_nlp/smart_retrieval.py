<<<<<<< HEAD
=======
"""
Smart Gmail Retrieval with Advanced Filtering and Batching Strategies
Implements intelligent filtering, date-based incremental sync, and optimized batch processing
"""

>>>>>>> origin/feat/modular-ai-platform
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
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
TOKEN_JSON_PATH = os.getenv('GMAIL_TOKEN_PATH', 'token.json')
CREDENTIALS_PATH = 'credentials.json'
GMAIL_CREDENTIALS_ENV_VAR = 'GMAIL_CREDENTIALS_JSON'

# Define constants for authentication
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
TOKEN_JSON_PATH = os.getenv("GMAIL_TOKEN_PATH", "token.json")
CREDENTIALS_PATH = "credentials.json"  # Fallback
GMAIL_CREDENTIALS_ENV_VAR = "GMAIL_CREDENTIALS_JSON"

# Define the project's root directory and default path for the checkpoint database
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_CHECKPOINT_DB_PATH = os.path.join(PROJECT_ROOT, "sync_checkpoints.db")


@dataclass
class RetrievalStrategy:
<<<<<<< HEAD
=======
    """Configuration for smart retrieval strategy"""

>>>>>>> origin/feat/modular-ai-platform
    name: str
    query_filter: str
    priority: int  # 1-10, higher is more priority
    batch_size: int
    frequency: str  # hourly, daily, weekly
    max_emails_per_run: int
    include_folders: List[str]
    exclude_folders: List[str]
    date_range_days: int

@dataclass
class SyncCheckpoint:
<<<<<<< HEAD
=======
    """Checkpoint for incremental synchronization"""

>>>>>>> origin/feat/modular-ai-platform
    strategy_name: str
    last_sync_date: datetime
    last_history_id: str
    processed_count: int
    next_page_token: Optional[str]
    errors_count: int

class SmartGmailRetriever:
<<<<<<< HEAD

<<<<<<< HEAD
    def __init__(self, checkpoint_db_path: str = DEFAULT_CHECKPOINT_DB_PATH):
=======
    def __init__(self, checkpoint_db_path: str = "sync_checkpoints.db"):
        """Initializes the SmartGmailRetriever."""
>>>>>>> origin/feature/git-history-analysis-report
=======
    """Advanced Gmail retrieval with intelligent filtering and batching"""

    def __init__(self, checkpoint_db_path: str = DEFAULT_CHECKPOINT_DB_PATH):
>>>>>>> origin/feat/modular-ai-platform
        self.logger = logging.getLogger(__name__)
        self.checkpoint_db_path = checkpoint_db_path
        self.logger.info(f"Using checkpoint database: {self.checkpoint_db_path}")
        self.gmail_service = None
        self._init_checkpoint_db()

        creds = self._load_credentials()
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    self._store_credentials(creds)
                except Exception as e:
                    self.logger.error(f"Failed to refresh token: {e}")
                    creds = self._authenticate()  # Try to re-authenticate
            else:
                creds = self._authenticate()

        if creds and creds.valid:
<<<<<<< HEAD
            self.gmail_service = build('gmail', 'v1', credentials=creds)

    def _init_checkpoint_db(self):
        with sqlite3.connect(self.checkpoint_db_path) as conn:
            conn.execute('CREATE TABLE IF NOT EXISTS sync_checkpoints (strategy_name TEXT PRIMARY KEY, last_sync_date TEXT, last_history_id TEXT)')
            conn.execute('CREATE TABLE IF NOT EXISTS retrieval_stats (date TEXT PRIMARY KEY, total_retrieved INTEGER, api_calls_used INTEGER)')

    def _load_credentials(self) -> Optional[Credentials]:
=======
            try:
                self.gmail_service = build("gmail", "v1", credentials=creds)
                self._store_credentials(creds)  # Save refreshed or new credentials
                self.logger.info("Gmail service initialized successfully.")
            except Exception as e:
                self.logger.error(f"Failed to build Gmail service: {e}")
                self.gmail_service = None  # Ensure service is None if build fails
                self.logger.error("Gmail service initialization failed.")
        else:
            self.logger.error("Failed to obtain valid credentials. Gmail service not initialized.")

        # Gmail API quotas and limits
        self.api_limits = {
            "daily_quota": 1000000000,  # 1 billion units per day
            "per_user_per_100_seconds": 250,  # 250 units per 100 seconds
            "batch_size_limit": 100,  # Max emails per batch request
            "concurrent_requests": 10,  # Max concurrent API calls
        }

        # Smart filtering categories
        self.folder_mappings = {
            "INBOX": {"priority": 10, "frequency": "hourly"},
            "SENT": {"priority": 5, "frequency": "daily"},
            "IMPORTANT": {"priority": 9, "frequency": "hourly"},
            "STARRED": {"priority": 8, "frequency": "hourly"},
            "CATEGORY_PERSONAL": {"priority": 7, "frequency": "daily"},
            "CATEGORY_SOCIAL": {"priority": 4, "frequency": "daily"},
            "CATEGORY_PROMOTIONS": {"priority": 2, "frequency": "weekly"},
            "CATEGORY_UPDATES": {"priority": 3, "frequency": "daily"},
            "CATEGORY_FORUMS": {"priority": 2, "frequency": "weekly"},
            "SPAM": {"priority": 1, "frequency": "weekly"},
            "TRASH": {"priority": 1, "frequency": "never"},
        }

    def _init_checkpoint_db(self):
        """Initialize checkpoint database for sync state management"""
        conn = sqlite3.connect(self.checkpoint_db_path)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS sync_checkpoints (
                strategy_name TEXT PRIMARY KEY,
                last_sync_date TEXT,
                last_history_id TEXT,
                processed_count INTEGER DEFAULT 0,
                next_page_token TEXT,
                errors_count INTEGER DEFAULT 0,
                created_at TEXT,
                updated_at TEXT
            )
        """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS retrieval_stats (
                date TEXT PRIMARY KEY,
                total_retrieved INTEGER DEFAULT 0,
                api_calls_used INTEGER DEFAULT 0,
                quota_remaining INTEGER DEFAULT 0,
                strategies_executed TEXT,
                performance_metrics TEXT
            )
        """
        )

        conn.commit()
        conn.close()

    def _load_credentials(self) -> Credentials | None:
        """Loads credentials from TOKEN_JSON_PATH if it exists."""
        creds = None
>>>>>>> origin/feat/modular-ai-platform
        if os.path.exists(TOKEN_JSON_PATH):
            try:
                creds = Credentials.from_authorized_user_file(TOKEN_JSON_PATH, SCOPES)
                self.logger.info(f"Loaded credentials from {TOKEN_JSON_PATH}")
            except Exception as e:
                self.logger.error(f"Error loading credentials from {TOKEN_JSON_PATH}: {e}")
        return creds

    def _store_credentials(self, creds: Credentials):
<<<<<<< HEAD
        with open(TOKEN_JSON_PATH, 'w') as token_file:
            token_file.write(creds.to_json())

    def _authenticate(self) -> Optional[Credentials]:
        flow = None
        gmail_creds_json = os.getenv(GMAIL_CREDENTIALS_ENV_VAR)
        if gmail_creds_json:
            try:
                self.logger.info('Attempting authentication using GMAIL_CREDENTIALS_JSON environment variable.')
                creds_info = json.loads(gmail_creds_json)
                flow = InstalledAppFlow.from_client_config(creds_info, SCOPES)
            except json.JSONDecodeError:
                self.logger.error('Failed to parse GMAIL_CREDENTIALS_JSON. Ensure it is valid JSON.')
                return None
        elif os.path.exists(CREDENTIALS_PATH):
            self.logger.info(f'Attempting authentication using {CREDENTIALS_PATH} file.')
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
        else:
            self.logger.error(f"Authentication failed: Neither GMAIL_CREDENTIALS_JSON environment variable is set nor the '{CREDENTIALS_PATH}' file was found.")
            return None
        try:
            creds = flow.run_local_server(port=0)
            if creds:
                self._store_credentials(creds)
            return creds
        except Exception as e:
            self.logger.error(f'An unexpected error occurred during the OAuth flow: {e}', exc_info=True)
            return None

    def get_optimized_retrieval_strategies(self) -> List[RetrievalStrategy]:
        return [RetrievalStrategy('critical_inbox', 'is:important', 10, 50, 'hourly', 200, ['INBOX'], [], 1)]

    def get_incremental_query(self, strategy: RetrievalStrategy, checkpoint: Optional[SyncCheckpoint]=None) -> str:
=======
        """Stores credentials to TOKEN_JSON_PATH."""
        try:
            with open(TOKEN_JSON_PATH, "w") as token_file:
                token_file.write(creds.to_json())
            self.logger.info(f"Stored credentials to {TOKEN_JSON_PATH}")
        except Exception as e:
            self.logger.error(f"Error storing credentials to {TOKEN_JSON_PATH}: {e}")

    def _authenticate(self) -> Credentials | None:
        """Authenticates the user via OAuth flow and returns credentials."""
        creds = None
        credentials_json_str = os.getenv(GMAIL_CREDENTIALS_ENV_VAR)

        flow = None
        if credentials_json_str:
            try:
                creds_info = json.loads(credentials_json_str)
                flow = InstalledAppFlow.from_client_config(creds_info, SCOPES)
                self.logger.info(
                    "Loaded credentials from GMAIL_CREDENTIALS_JSON environment variable."
                )
            except json.JSONDecodeError as e:
                self.logger.error(
                    f"Error decoding GMAIL_CREDENTIALS_JSON: {e}. Trying {CREDENTIALS_PATH} next."
                )
            except Exception as e:
                self.logger.error(
                    f"Error loading credentials from GMAIL_CREDENTIALS_JSON: {e}. Trying {CREDENTIALS_PATH} next."
                )

        if not flow and os.path.exists(CREDENTIALS_PATH):
            try:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
                self.logger.info(f"Loaded credentials from {CREDENTIALS_PATH}.")
            except Exception as e:
                self.logger.error(f"Error loading credentials from {CREDENTIALS_PATH}: {e}")
                return None  # Cannot proceed without client secrets

        if not flow:
            self.logger.error(
                f"Authentication failed: No credentials found in GMAIL_CREDENTIALS_JSON or at {CREDENTIALS_PATH}"
            )
            return None

        try:
            creds = flow.run_local_server(port=0)
            self.logger.info("Authentication successful via local server flow.")
        except Exception as e:
            self.logger.error(f"Authentication flow failed: {e}")
            return None

        if creds:
            self._store_credentials(creds)
        return creds

    def get_optimized_retrieval_strategies(self) -> List[RetrievalStrategy]:
        """Generate optimized retrieval strategies based on folder types and priorities"""
        strategies = []

        # High-priority real-time strategies
        strategies.extend(
            [
                # Critical inbox monitoring
                RetrievalStrategy(
                    name="critical_inbox",
                    query_filter="in:inbox is:important newer_than:1h",
                    priority=10,
                    batch_size=50,
                    frequency="hourly",
                    max_emails_per_run=200,
                    include_folders=["INBOX", "IMPORTANT"],
                    exclude_folders=["SPAM", "TRASH"],
                    date_range_days=1,
                ),
                # Starred items
                RetrievalStrategy(
                    name="starred_recent",
                    query_filter="is:starred newer_than:6h",
                    priority=9,
                    batch_size=30,
                    frequency="hourly",
                    max_emails_per_run=100,
                    include_folders=["STARRED"],
                    exclude_folders=["SPAM", "TRASH"],
                    date_range_days=7,
                ),
                # Unread priority emails
                RetrievalStrategy(
                    name="unread_priority",
                    query_filter="is:unread (is:important OR from:manager OR from:ceo OR subject:urgent OR subject:asap) newer_than:2h",
                    priority=9,
                    batch_size=40,
                    frequency="hourly",
                    max_emails_per_run=150,
                    include_folders=["INBOX", "IMPORTANT"],
                    exclude_folders=["SPAM", "TRASH", "CATEGORY_PROMOTIONS"],
                    date_range_days=1,
                ),
            ]
        )

        # Medium-priority daily strategies
        strategies.extend(
            [
                # Personal category
                RetrievalStrategy(
                    name="personal_daily",
                    query_filter="category:primary newer_than:1d",
                    priority=7,
                    batch_size=100,
                    frequency="daily",
                    max_emails_per_run=500,
                    include_folders=["CATEGORY_PERSONAL", "INBOX"],
                    exclude_folders=["SPAM", "TRASH"],
                    date_range_days=3,
                ),
                # Social updates
                RetrievalStrategy(
                    name="social_daily",
                    query_filter="category:social newer_than:1d",
                    priority=5,
                    batch_size=75,
                    frequency="daily",
                    max_emails_per_run=300,
                    include_folders=["CATEGORY_SOCIAL"],
                    exclude_folders=["SPAM", "TRASH"],
                    date_range_days=2,
                ),
                # Updates and notifications
                RetrievalStrategy(
                    name="updates_daily",
                    query_filter="category:updates newer_than:1d",
                    priority=4,
                    batch_size=80,
                    frequency="daily",
                    max_emails_per_run=400,
                    include_folders=["CATEGORY_UPDATES"],
                    exclude_folders=["SPAM", "TRASH"],
                    date_range_days=2,
                ),
                # Work-related emails
                RetrievalStrategy(
                    name="work_comprehensive",
                    query_filter="(from:company.com OR subject:meeting OR subject:project OR subject:deadline) newer_than:1d",
                    priority=8,
                    batch_size=60,
                    frequency="daily",
                    max_emails_per_run=300,
                    include_folders=["INBOX", "SENT"],
                    exclude_folders=["SPAM", "TRASH", "CATEGORY_PROMOTIONS"],
                    date_range_days=2,
                ),
            ]
        )

        # Low-priority weekly strategies
        strategies.extend(
            [
                # Promotional emails
                RetrievalStrategy(
                    name="promotions_weekly",
                    query_filter="category:promotions newer_than:7d",
                    priority=2,
                    batch_size=100,
                    frequency="weekly",
                    max_emails_per_run=1000,
                    include_folders=["CATEGORY_PROMOTIONS"],
                    exclude_folders=["SPAM", "TRASH"],
                    date_range_days=7,
                ),
                # Forums and communities
                RetrievalStrategy(
                    name="forums_weekly",
                    query_filter="category:forums newer_than:7d",
                    priority=2,
                    batch_size=50,
                    frequency="weekly",
                    max_emails_per_run=200,
                    include_folders=["CATEGORY_FORUMS"],
                    exclude_folders=["SPAM", "TRASH"],
                    date_range_days=7,
                ),
                # Sent items analysis
                RetrievalStrategy(
                    name="sent_analysis",
                    query_filter="in:sent newer_than:7d",
                    priority=3,
                    batch_size=75,
                    frequency="weekly",
                    max_emails_per_run=500,
                    include_folders=["SENT"],
                    exclude_folders=["SPAM", "TRASH"],
                    date_range_days=7,
                ),
            ]
        )

        # Special strategies for training and analysis
        strategies.extend(
            [
                # Comprehensive training data
                RetrievalStrategy(
                    name="training_data_comprehensive",
                    query_filter="newer_than:30d",
                    priority=1,
                    batch_size=200,
                    frequency="monthly",
                    max_emails_per_run=5000,
                    include_folders=[
                        "INBOX",
                        "SENT",
                        "CATEGORY_PERSONAL",
                        "CATEGORY_SOCIAL",
                    ],
                    exclude_folders=["SPAM", "TRASH"],
                    date_range_days=30,
                ),
                # Historical important emails
                RetrievalStrategy(
                    name="historical_important",
                    query_filter="is:important OR is:starred older_than:30d newer_than:365d",
                    priority=2,
                    batch_size=50,
                    frequency="monthly",
                    max_emails_per_run=1000,
                    include_folders=["IMPORTANT", "STARRED"],
                    exclude_folders=["SPAM", "TRASH"],
                    date_range_days=365,
                ),
            ]
        )

        return sorted(strategies, key=lambda x: x.priority, reverse=True)

    def get_incremental_query(
        self, strategy: RetrievalStrategy, checkpoint: Optional[SyncCheckpoint] = None
    ) -> str:
        """Build incremental query based on checkpoint and strategy"""
>>>>>>> origin/feat/modular-ai-platform
        base_query = strategy.query_filter
        self.logger.debug(f"Base query for strategy '{strategy.name}': {base_query}")

        if checkpoint and checkpoint.last_sync_date:
<<<<<<< HEAD
            base_query += f' after:{int(checkpoint.last_sync_date.timestamp())}'
        return base_query

    async def execute_smart_retrieval(self, strategies: Optional[List[RetrievalStrategy]]=None, max_api_calls: int=100, time_budget_minutes: int=30) -> Dict[str, Any]:
        """
        Executes a series of retrieval strategies within given constraints.
=======
            self.logger.info(
                f"Found checkpoint for strategy '{strategy.name}' with last_sync_date: {checkpoint.last_sync_date}"
            )
            # Use checkpoint date for incremental sync
            last_sync = checkpoint.last_sync_date
            if isinstance(last_sync, str):
                last_sync = datetime.fromisoformat(last_sync.replace("Z", "+00:00"))

            # Calculate time since last sync
            time_diff = datetime.now() - last_sync

            if time_diff.days > 0:
                date_filter = f"newer_than:{time_diff.days}d"
            elif time_diff.seconds > 3600:
                hours = int(time_diff.seconds / 3600)
                date_filter = f"newer_than:{hours}h"
            else:
                date_filter = "newer_than:1h"

            # Replace or add date filter to base query
            if "newer_than:" in base_query:
                # Replace existing date filter
                import re

                base_query = re.sub(r"newer_than:\d+[hdw]", date_filter, base_query)
            else:
                # Add date filter
                base_query = f"{base_query} {date_filter}"

        # Add folder-specific filters
        if strategy.include_folders:
            folder_filters = " OR ".join(
                [f"in:{folder.lower()}" for folder in strategy.include_folders]
            )
            base_query = f"({base_query}) AND ({folder_filters})"

        if strategy.exclude_folders:
            exclude_filters = " AND ".join(
                [f"-in:{folder.lower()}" for folder in strategy.exclude_folders]
            )
            base_query = f"{base_query} {exclude_filters}"

        self.logger.info(
            f"Generated incremental query for strategy '{strategy.name}': {base_query}"
        )
        return base_query

    async def execute_smart_retrieval(
        self,
        strategies: Optional[List[RetrievalStrategy]] = None,
        max_api_calls: int = 100,
        time_budget_minutes: int = 30,
    ) -> Dict[str, Any]:
        """Execute smart retrieval with multiple strategies and rate limiting"""
        self.logger.info(
            f"Starting smart retrieval. Max API calls: {max_api_calls}, Time budget: {time_budget_minutes} mins."
        )
>>>>>>> origin/feat/modular-ai-platform

        if strategies is None:
            strategies = self.get_optimized_retrieval_strategies()
            self.logger.info(
                f"No specific strategies provided, using {len(strategies)} optimized strategies."
            )
        else:
            self.logger.info(f"Executing {len(strategies)} provided strategies.")

<<<<<<< HEAD
        Returns:
            A dictionary summarizing the results of the retrieval.
        """
        if not self.gmail_service:
            return {'success': False, 'error': 'Gmail service not initialized.'}
        strategies = strategies or self.get_optimized_retrieval_strategies()
        results = {'strategies_executed': [], 'total_emails_retrieved': 0, 'api_calls_used': 0}
        start_time = datetime.now()
        for strategy in strategies:
            if (datetime.now() - start_time).total_seconds() / 60 > time_budget_minutes:
                break
            checkpoint = self._load_checkpoint(strategy.name)
            query = self.get_incremental_query(strategy, checkpoint)
            results['strategies_executed'].append(strategy.name)
        return results

    async def _fetch_email_batch(self, query: str, batch_size: int, page_token: Optional[str]=None) -> Dict[str, Any]:
        """Fetches a single batch of emails from the Gmail API."""
        response = self.gmail_service.users().messages().list(userId='me', q=query, maxResults=batch_size, pageToken=page_token).execute()
        return {'messages': response.get('messages', []), 'nextPageToken': response.get('nextPageToken')}

    def _load_checkpoint(self, strategy_name: str) -> Optional[SyncCheckpoint]:
        with sqlite3.connect(self.checkpoint_db_path) as conn:
            cursor = conn.execute('SELECT last_sync_date, last_history_id FROM sync_checkpoints WHERE strategy_name = ?', (strategy_name,))
            row = cursor.fetchone()
            if row:
                return SyncCheckpoint(strategy_name, datetime.fromisoformat(row[0]), row[1], 0, None, 0)
        return None

    def _save_checkpoint(self, checkpoint: SyncCheckpoint):
        with sqlite3.connect(self.checkpoint_db_path) as conn:
            conn.execute('INSERT OR REPLACE INTO sync_checkpoints (strategy_name, last_sync_date, last_history_id) VALUES (?, ?, ?)', (checkpoint.strategy_name, checkpoint.last_sync_date.isoformat(), checkpoint.last_history_id))

async def main_cli():
    """Provides a command-line interface for the SmartGmailRetriever."""
    parser = argparse.ArgumentParser(description='Smart Gmail Retriever CLI')
    parser.add_argument('command', choices=['list-strategies', 'execute-strategies'])
    args = parser.parse_args()
    retriever = SmartGmailRetriever()
    if args.command == 'list-strategies':
        strategies = retriever.get_optimized_retrieval_strategies()
        print(json.dumps([asdict(s) for s in strategies], indent=2))
    elif args.command == 'execute-strategies':
        results = await retriever.execute_smart_retrieval()
        print(json.dumps(results, indent=2))
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    asyncio.run(main_cli())
=======
        results = {
            "strategies_executed": [],
            "total_emails_retrieved": 0,
            "api_calls_used": 0,
            "errors": [],
            "performance_metrics": {},
            "quota_status": {},
        }

        start_time = datetime.now()
        api_calls_used = 0

        # Execute strategies in priority order
        for i, strategy in enumerate(strategies):
            self.logger.info(
                f"Executing strategy {i+1}/{len(strategies)}: '{strategy.name}' (Priority: {strategy.priority})"
            )
            # Check time and API budget
            elapsed_time_seconds = (datetime.now() - start_time).total_seconds()
            elapsed_time_minutes = elapsed_time_seconds / 60

            if elapsed_time_minutes >= time_budget_minutes:
                self.logger.warning(
                    f"Time budget of {time_budget_minutes} minutes reached. "
                    f"Elapsed: {elapsed_time_minutes:.2f} mins. Stopping retrieval."
                )
                break
            if api_calls_used >= max_api_calls:
                self.logger.warning(
                    f"API call limit of {max_api_calls} reached. Used: {api_calls_used}. Stopping retrieval."
                )
                break

            self.logger.info(
                f"Current budget status - Time elapsed: {elapsed_time_minutes:.2f}/{time_budget_minutes} mins. "
                f"API calls used: {api_calls_used}/{max_api_calls}."
            )

            try:
                # Load checkpoint for this strategy
                checkpoint = self._load_checkpoint(strategy.name)

                # Build incremental query
                query = self.get_incremental_query(strategy, checkpoint)

                # Execute retrieval for this strategy
                self.logger.debug(f"Calling _execute_strategy_retrieval for '{strategy.name}'")
                strategy_result = await self._execute_strategy_retrieval(
                    strategy,
                    query,
                    checkpoint,
                    remaining_api_calls=max_api_calls - api_calls_used,
                )
                self.logger.debug(f"Strategy '{strategy.name}' result: {strategy_result}")

                # Update results
                results["strategies_executed"].append(
                    {
                        "strategy_name": strategy.name,
                        "emails_retrieved": strategy_result["emails_count"],
                        "api_calls": strategy_result["api_calls"],
                        "success": strategy_result["success"],
                    }
                )

                results["total_emails_retrieved"] += strategy_result["emails_count"]
                api_calls_used += strategy_result["api_calls"]

                if not strategy_result["success"]:
                    results["errors"].append(
                        {
                            "strategy": strategy.name,
                            "error": strategy_result.get("error", "Unknown error"),
                        }
                    )

                # Update checkpoint
                if strategy_result["success"]:
                    self._save_checkpoint(
                        SyncCheckpoint(
                            strategy_name=strategy.name,
                            last_sync_date=datetime.now(),
                            last_history_id=strategy_result.get("last_history_id", ""),
                            processed_count=(
                                checkpoint.processed_count + strategy_result["emails_count"]
                                if checkpoint
                                else strategy_result["emails_count"]
                            ),
                            next_page_token=strategy_result.get("next_page_token"),
                            errors_count=checkpoint.errors_count if checkpoint else 0,
                        )
                    )

                # Rate limiting between strategies
                await asyncio.sleep(1)

            except Exception as e:
                self.logger.error(f"Strategy {strategy.name} failed: {e}")
                results["errors"].append({"strategy": strategy.name, "error": str(e)})

        # Calculate performance metrics
        total_execution_time = (datetime.now() - start_time).total_seconds()
        results["performance_metrics"] = {
            "total_time_seconds": total_execution_time,
            "emails_per_second": (
                results["total_emails_retrieved"] / total_execution_time
                if total_execution_time > 0
                else 0
            ),
            "api_efficiency": (
                results["total_emails_retrieved"] / api_calls_used if api_calls_used > 0 else 0
            ),
        }

        results["api_calls_used"] = api_calls_used
        results["quota_status"] = {
            "daily_quota_used_percent": (
                (api_calls_used / self.api_limits["daily_quota"]) * 100
                if self.api_limits["daily_quota"] > 0
                else "N/A"
            ),
            "remaining_calls_in_budget": max_api_calls - api_calls_used,
        }

        self.logger.info(
            f"Smart retrieval finished. Total emails retrieved: {results['total_emails_retrieved']}. Total API calls: {api_calls_used}."
        )
        # Store daily statistics
        self._store_daily_stats(results)

        return results

    async def _execute_strategy_retrieval(
        self,
        strategy: RetrievalStrategy,
        query: str,
        checkpoint: Optional[SyncCheckpoint],
        remaining_api_calls: int,
    ) -> Dict[str, Any]:
        """Execute retrieval for a specific strategy"""
        self.logger.info(
            f"Executing strategy '{strategy.name}'. Query: '{query}'. Max emails for this run: {strategy.max_emails_per_run}."
        )
        self.logger.debug(f"Checkpoint for '{strategy.name}': {checkpoint}")

        try:
            emails_retrieved_for_strategy = []
            api_calls_for_strategy = 0
            current_page_token = checkpoint.next_page_token if checkpoint else None

            # Calculate max emails for this strategy based on its own limit and remaining global API calls
            # Each batch uses 1 API call for list() and N for get() if we fetch full messages,
            # but current _fetch_email_batch uses 1 for list and N for metadata get.
            # Let's assume batch_size is the dominant factor for now for max_emails calculation.
            effective_max_emails = min(
                strategy.max_emails_per_run,
                (
                    remaining_api_calls * strategy.batch_size
                    if strategy.batch_size > 0
                    else remaining_api_calls
                ),
            )
            self.logger.debug(
                f"Effective max emails for '{strategy.name}': {effective_max_emails} (strategy.max_emails_per_run: {strategy.max_emails_per_run}, remaining_api_calls: {remaining_api_calls})"
            )

            while (
                len(emails_retrieved_for_strategy) < effective_max_emails
                and api_calls_for_strategy < remaining_api_calls
            ):
                batch_size_for_call = min(
                    strategy.batch_size,
                    effective_max_emails - len(emails_retrieved_for_strategy),
                )
                if (
                    batch_size_for_call <= 0
                ):  # Should not happen if effective_max_emails is correctly calculated
                    break

                self.logger.debug(
                    f"Fetching batch for '{strategy.name}'. Batch size: {batch_size_for_call}, Page token: {current_page_token}"
                )
                batch_result = await self._fetch_email_batch(
                    query=query,
                    batch_size=batch_size_for_call,
                    page_token=current_page_token,
                )

                # Count actual API calls: 1 for list + N for individual message gets
                messages_in_batch = batch_result.get("messages", [])
                batch_api_calls = 1 + len(messages_in_batch)  # 1 list call + N get calls
                api_calls_for_strategy += batch_api_calls

                if batch_result.get("error"):
                    self.logger.error(
                        f"Error in _fetch_email_batch for strategy '{strategy.name}': {batch_result['error']}"
                    )
                    return {
                        "success": False,
                        "emails_count": len(emails_retrieved_for_strategy),
                        "api_calls": api_calls_for_strategy,
                        "error": batch_result["error"],
                        "last_history_id": (checkpoint.last_history_id if checkpoint else None),
                        "next_page_token": current_page_token,
                    }

                if not messages_in_batch:
                    self.logger.info(
                        f"No more messages found for strategy '{strategy.name}' in this batch."
                    )
                    break

                emails_retrieved_for_strategy.extend(messages_in_batch)
                current_page_token = batch_result.get("nextPageToken")

                self.logger.info(
                    f"Retrieved {len(messages_in_batch)} messages in this batch for '{strategy.name}'. Total for strategy: {len(emails_retrieved_for_strategy)}. API calls for batch: {batch_api_calls}"
                )

                if not current_page_token:
                    self.logger.info(
                        f"No next page token for strategy '{strategy.name}'. End of results for this query."
                    )
                    break

                # Rate limiting between batches
                await asyncio.sleep(0.5)

            self.logger.info(
                f"Strategy '{strategy.name}' finished. Retrieved {len(emails_retrieved_for_strategy)} emails using {api_calls_for_strategy} API calls."
            )
            return {
                "success": True,
                "emails_count": len(emails_retrieved_for_strategy),
                "api_calls": api_calls_for_strategy,
                "emails": emails_retrieved_for_strategy,
                "next_page_token": current_page_token,
                "last_history_id": batch_result.get(
                    "historyId", checkpoint.last_history_id if checkpoint else None
                ),
            }

        except Exception as e:
            self.logger.exception(
                f"Exception in _execute_strategy_retrieval for '{strategy.name}': {e}"
            )
            return {
                "success": False,
                "emails_count": (
                    len(emails_retrieved_for_strategy)
                    if "emails_retrieved_for_strategy" in locals()
                    else 0
                ),
                "api_calls": (
                    api_calls_for_strategy if "api_calls_for_strategy" in locals() else 0
                ),
                "error": str(e),
            }

    async def _fetch_email_batch(
        self, query: str, batch_size: int, page_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """Fetch a batch of emails using Gmail API or simulated for development if service is unavailable."""

        if not self.gmail_service:
            self.logger.warning(
                "Gmail service not available. Using simulated email fetching for query: %s",
                query,
            )
            return await self._simulate_gmail_response(query, batch_size, page_token)

        fetched_messages = []
        next_page_token_from_list = None
        history_id_from_list = None
        list_response_messages = 0  # For logging

        try:
            self.logger.debug(
                f"Fetching email list with query: '{query}', batch_size: {batch_size}, page_token: {page_token}"
            )
            list_response = (
                self.gmail_service.users()
                .messages()
                .list(userId="me", q=query, maxResults=batch_size, pageToken=page_token)
                .execute()
            )
            list_response_messages = len(list_response.get("messages", []))
            self.logger.info(
                f"Gmail API list call successful for query '{query}'. Messages in list: {list_response_messages}. Batch size: {batch_size}"
            )

            next_page_token_from_list = list_response.get("nextPageToken")
            history_id_from_list = list_response.get("historyId")

            if "messages" in list_response:
                for i, message_ref in enumerate(list_response["messages"]):
                    try:
                        self.logger.debug(
                            f"Fetching message detail {i+1}/{list_response_messages} for ID {message_ref['id']} (query: '{query}')"
                        )
                        msg_detail = (
                            self.gmail_service.users()
                            .messages()
                            .get(userId="me", id=message_ref["id"], format="metadata")
                            .execute()
                        )

                        transformed_message = {
                            "id": msg_detail["id"],
                            "threadId": msg_detail["threadId"],
                            "snippet": msg_detail.get("snippet", ""),
                            "payload": {
                                "headers": msg_detail.get("payload", {}).get("headers", [])
                            },
                        }
                        fetched_messages.append(transformed_message)
                        if msg_detail.get("historyId"):
                            current_msg_hist_id = str(msg_detail.get("historyId"))
                            if history_id_from_list is None or current_msg_hist_id > str(
                                history_id_from_list
                            ):
                                history_id_from_list = current_msg_hist_id
                                self.logger.debug(
                                    f"Updated historyId to {history_id_from_list} from message {msg_detail['id']}"
                                )

                    except HttpError as e_get:
                        self.logger.error(
                            f"HttpError fetching message detail for ID {message_ref['id']} (query: '{query}'): {e_get}. Skipping."
                        )
                        continue
                    except Exception as e_generic_get:
                        self.logger.error(
                            f"Generic error fetching message detail for ID {message_ref['id']} (query: '{query}'): {e_generic_get}. Skipping."
                        )
                        continue
            self.logger.debug(
                f"Finished processing batch for query: '{query}'. Fetched details for {len(fetched_messages)} messages."
            )

        except HttpError as e_list:
            self.logger.error(
                f"HttpError fetching email list from Gmail API for query '{query}': {e_list}"
            )
            return {
                "messages": [],
                "nextPageToken": None,
                "error": str(e_list),
                "historyId": None,
            }
        except Exception as e_generic_list:
            self.logger.error(
                f"Generic error during email list fetching for query '{query}': {e_generic_list}"
            )
            return {
                "messages": [],
                "nextPageToken": None,
                "error": str(e_generic_list),
                "historyId": None,
            }

        return {
            "messages": fetched_messages,
            "nextPageToken": next_page_token_from_list,
            "resultSizeEstimate": list_response.get("resultSizeEstimate", len(fetched_messages)),
            "historyId": history_id_from_list,
        }

    async def _simulate_gmail_response(
        self, query: str, batch_size: int, page_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """Simulates a Gmail API response for development when the service is unavailable."""
        self.logger.info(
            f"Simulating Gmail response for query: '{query}', batch_size: {batch_size}, page_token: {page_token}"
        )
        messages = []
        for i in range(min(batch_size, 10)):  # Limit simulation
            message_id = f"msg_{datetime.now().timestamp()}_{i:03d}"
            messages.append(
                {
                    "id": message_id,
                    "threadId": f"thread_{message_id.split('_')[1]}_{i//3:03d}",
                    "snippet": f"Sample email content for query '{query}'...",
                    "payload": {
                        "headers": [
                            {
                                "name": "Subject",
                                "value": f"Simulated Email {i+1} for {query}",
                            },
                            {
                                "name": "From",
                                "value": f"sender.simulated{i}@example.com",
                            },
                            {
                                "name": "Date",
                                "value": datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z"),
                            },
                        ]
                    },
                }
            )

        response = {
            "messages": messages,
            "resultSizeEstimate": len(messages),
            "historyId": f"history_simulated_{datetime.now().timestamp()}",
        }

        if batch_size >= 10 and not page_token:  # Simplified simulation of next page token
            response["nextPageToken"] = f"token_simulated_{datetime.now().timestamp()}"

        self.logger.debug(f"Simulated response: {response}")
        return response

    def _load_checkpoint(self, strategy_name: str) -> Optional[SyncCheckpoint]:
        """Load sync checkpoint for strategy"""
        self.logger.debug(f"Loading checkpoint for strategy: {strategy_name}")
        conn = sqlite3.connect(self.checkpoint_db_path)
        cursor = conn.execute(
            "SELECT * FROM sync_checkpoints WHERE strategy_name = ?", (strategy_name,)
        )
        row = cursor.fetchone()
        conn.close()

        if row:
            loaded_checkpoint = SyncCheckpoint(
                strategy_name=row[0],
                last_sync_date=(
                    datetime.fromisoformat(row[1]) if row[1] else datetime.now()
                ),  # Consider default if None
                last_history_id=row[2] or "",
                processed_count=row[3] or 0,
                next_page_token=row[4],
                errors_count=row[5] or 0,
            )
            self.logger.info(
                f"Checkpoint loaded for '{strategy_name}': Last sync {loaded_checkpoint.last_sync_date}, Processed {loaded_checkpoint.processed_count}"
            )
            return loaded_checkpoint
        self.logger.info(f"No checkpoint found for strategy: {strategy_name}")
        return None

    def _save_checkpoint(self, checkpoint: SyncCheckpoint):
        """Save sync checkpoint"""
        self.logger.info(
            f"Saving checkpoint for strategy '{checkpoint.strategy_name}': Last sync {checkpoint.last_sync_date}, Processed {checkpoint.processed_count}, HistoryID {checkpoint.last_history_id}"
        )
        conn = sqlite3.connect(self.checkpoint_db_path)
        conn.execute(
            """
            INSERT OR REPLACE INTO sync_checkpoints
            (strategy_name, last_sync_date, last_history_id, processed_count,
             next_page_token, errors_count, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                checkpoint.strategy_name,
                checkpoint.last_sync_date.isoformat(),
                checkpoint.last_history_id,
                checkpoint.processed_count,
                checkpoint.next_page_token,
                checkpoint.errors_count,
                datetime.now().isoformat(),
            ),
        )
        conn.commit()
        conn.close()

    def _store_daily_stats(self, results: Dict[str, Any]):
        """Store daily retrieval statistics"""
        today = datetime.now().date().isoformat()
        self.logger.info(
            f"Storing daily stats for {today}. Total retrieved: {results['total_emails_retrieved']}, API calls: {results['api_calls_used']}"
        )

        conn = sqlite3.connect(self.checkpoint_db_path)
        conn.execute(
            """
            INSERT OR REPLACE INTO retrieval_stats
            (date, total_retrieved, api_calls_used, strategies_executed, performance_metrics)
            VALUES (?, ?, ?, ?, ?)
        """,
            (
                today,
                results["total_emails_retrieved"],
                results["api_calls_used"],
                json.dumps([s["strategy_name"] for s in results["strategies_executed"]]),
                json.dumps(results["performance_metrics"]),
            ),
        )
        conn.commit()
        conn.close()

    def get_retrieval_analytics(self, days: int = 30) -> Dict[str, Any]:
        """Get retrieval analytics for the past N days"""
        self.logger.info(f"Fetching retrieval analytics for the last {days} days.")
        conn = sqlite3.connect(self.checkpoint_db_path)

        # Get daily stats
        cursor = conn.execute(
            """
            SELECT date, total_retrieved, api_calls_used, strategies_executed, performance_metrics
            FROM retrieval_stats
            WHERE date >= date('now', '-{} days')
            ORDER BY date DESC
        """.format(
                days
            )
        )

        daily_stats = []
        for row in cursor.fetchall():
            daily_stats.append(
                {
                    "date": row[0],
                    "total_retrieved": row[1],
                    "api_calls_used": row[2],
                    "strategies_executed": json.loads(row[3]) if row[3] else [],
                    "performance_metrics": json.loads(row[4]) if row[4] else {},
                }
            )

        # Get strategy performance
        cursor = conn.execute(
            """
            SELECT strategy_name,
                   COUNT(*) as sync_count,
                   SUM(processed_count) as total_processed,
                   AVG(processed_count) as avg_per_sync,
                   SUM(errors_count) as total_errors
            FROM sync_checkpoints
            GROUP BY strategy_name
        """
        )

        # Create a map of strategy name to its category (frequency) for aggregation
        strategy_map = {
            s.name: s.frequency for s in self.get_optimized_retrieval_strategies()
        }

        # Aggregate performance by category (frequency)
        aggregated_performance = {}

        for row in cursor.fetchall():
            strategy_name = row[0]
            sync_count = row[1]
            total_processed = row[2]
            # avg_per_sync is per-strategy, so we'll recalculate it for the category
            total_errors = row[4]

            category = strategy_map.get(strategy_name, "uncategorized")

            if category not in aggregated_performance:
                aggregated_performance[category] = {
                    "sync_count": 0, "total_processed": 0, "total_errors": 0, "strategy_count": 0
                }

            aggregated_performance[category]["sync_count"] += sync_count
            aggregated_performance[category]["total_processed"] += total_processed
            aggregated_performance[category]["total_errors"] += total_errors
            aggregated_performance[category]["strategy_count"] += 1

        # Format the aggregated data for the final output
        strategy_category_performance = []
        for category, data in aggregated_performance.items():
            strategy_category_performance.append({
                "category": category,
                "sync_count": data["sync_count"],
                "total_processed": data["total_processed"],
                "avg_per_sync": data["total_processed"] / data["sync_count"] if data["sync_count"] > 0 else 0,
                "total_errors": data["total_errors"],
                "error_rate": (data["total_errors"] / data["sync_count"]) * 100 if data["sync_count"] > 0 else 0,
                "strategy_count": data["strategy_count"],
            })

        conn.close()

        # Calculate summary metrics
        total_retrieved = sum(day["total_retrieved"] for day in daily_stats)
        total_api_calls = sum(day["api_calls_used"] for day in daily_stats)

        return {
            "summary": {
                "total_emails_retrieved": total_retrieved,
                "total_api_calls_used": total_api_calls,
                "average_daily_retrieval": (
                    total_retrieved / len(daily_stats) if daily_stats else 0
                ),
                "api_efficiency": (total_retrieved / total_api_calls if total_api_calls > 0 else 0),
                "days_analyzed": len(daily_stats),
            },
            "daily_stats": daily_stats,
            "strategy_performance": strategy_category_performance,
        }

    def optimize_strategies_based_on_performance(self) -> List[RetrievalStrategy]:
        """Optimize retrieval strategies based on historical performance"""
        self.logger.info("Attempting to optimize strategies based on performance (last 7 days).")
        analytics = self.get_retrieval_analytics(days=7)

        # Get current strategies
        strategies = self.get_optimized_retrieval_strategies()

        # Adjust strategies based on performance
        strategy_performance_map = {
            s["strategy_name"]: s for s in analytics.get("strategy_performance", [])
        }

        optimized_strategies = []
        for strategy in strategies:
            original_batch_size = strategy.batch_size
            original_frequency = strategy.frequency

            perf = strategy_performance_map.get(strategy.name)
            if perf:
                self.logger.debug(f"Performance data for strategy '{strategy.name}': {perf}")
                error_rate = perf.get("error_rate", 0)
                avg_per_sync = perf.get("avg_per_sync", 0)

                if error_rate > 10:  # High error rate
                    strategy.batch_size = max(10, strategy.batch_size // 2)
                    self.logger.info(
                        f"Strategy '{strategy.name}': High error rate ({error_rate:.2f}%). Reducing batch size from {original_batch_size} to {strategy.batch_size}."
                    )
                elif (
                    error_rate < 2 and perf.get("sync_count", 0) > 5
                ):  # Low error rate and sufficient data
                    strategy.batch_size = min(
                        self.api_limits.get("batch_size_limit", 100),
                        int(strategy.batch_size * 1.2),
                    )  # Ensure not over API limit
                    if strategy.batch_size != original_batch_size:
                        self.logger.info(
                            f"Strategy '{strategy.name}': Low error rate ({error_rate:.2f}%). Increasing batch size from {original_batch_size} to {strategy.batch_size}."
                        )

                if (
                    avg_per_sync < 10
                    and strategy.frequency == "hourly"
                    and perf.get("sync_count", 0) > 10
                ):  # Low volume and sufficient data
                    strategy.frequency = "daily"
                    self.logger.info(
                        f"Strategy '{strategy.name}': Low avg emails per sync ({avg_per_sync:.2f}). Changing frequency from {original_frequency} to {strategy.frequency}."
                    )
                elif (
                    avg_per_sync > (strategy.max_emails_per_run * 0.8)
                    and strategy.frequency == "daily"
                    and perf.get("sync_count", 0) > 5
                ):  # High volume, nearing max_emails_per_run
                    strategy.frequency = "hourly"
                    self.logger.info(
                        f"Strategy '{strategy.name}': High avg emails per sync ({avg_per_sync:.2f}). Changing frequency from {original_frequency} to {strategy.frequency}."
                    )
            else:
                self.logger.debug(
                    f"No performance data found for strategy '{strategy.name}'. Using default parameters."
                )

            optimized_strategies.append(strategy)

        self.logger.info(
            f"Strategy optimization complete. {len(optimized_strategies)} strategies processed."
        )
        return optimized_strategies


async def run_example_usage():
    """Example usage of smart Gmail retriever"""
    retriever = SmartGmailRetriever()

    # Get optimized strategies
    strategies = retriever.get_optimized_retrieval_strategies()
    print(f"Generated {len(strategies)} retrieval strategies")

    # Execute smart retrieval
    results = await retriever.execute_smart_retrieval(
        strategies=strategies[:5],  # Execute top 5 priority strategies
        max_api_calls=50,
        time_budget_minutes=10,
    )

    print(f"Retrieval completed:")
    print(f"- Total emails: {results['total_emails_retrieved']}")
    print(f"- API calls used: {results['api_calls_used']}")
    print(f"- Strategies executed: {len(results['strategies_executed'])}")

    # Get analytics
    analytics = retriever.get_retrieval_analytics(days=7)
    print(f"Analytics summary: {analytics['summary']}")


async def main_cli():
    """Command-line interface for Smart Gmail Retriever"""
    parser = argparse.ArgumentParser(description="Smart Gmail Retriever CLI")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # list-strategies subparser
    list_parser = subparsers.add_parser(
        "list-strategies", help="List available retrieval strategies"
    )
    list_parser.add_argument(
        "--checkpoint-db-path",
        type=str,
        default="sync_checkpoints.db",
        help="Path to the checkpoint database",
    )

    # execute-strategies subparser
    execute_parser = subparsers.add_parser(
        "execute-strategies", help="Execute retrieval strategies"
    )
    execute_parser.add_argument(
        "--strategies",
        "--strategy-names",
        dest="strategies",
        nargs="+",
        help="Names of specific strategies to execute (optional)",
    )
    execute_parser.add_argument(
        "--max-api-calls", type=int, default=100, help="Maximum API calls allowed"
    )
    execute_parser.add_argument(
        "--time-budget-minutes",
        type=int,
        default=30,
        help="Time budget for retrieval in minutes",
    )
    execute_parser.add_argument(
        "--checkpoint-db-path",
        type=str,
        default="sync_checkpoints.db",
        help="Path to the checkpoint database",
    )

    # get-retrieval-analytics subparser
    analytics_parser = subparsers.add_parser(
        "get-retrieval-analytics", help="Get retrieval analytics"
    )
    analytics_parser.add_argument(
        "--days",
        type=int,
        default=30,
        help="Number of past days to include in analytics",
    )
    analytics_parser.add_argument(
        "--checkpoint-db-path",
        type=str,
        default="sync_checkpoints.db",
        help="Path to the checkpoint database",
    )

    args = parser.parse_args()

    retriever = SmartGmailRetriever(checkpoint_db_path=args.checkpoint_db_path)

    try:
        if args.command == "list-strategies":
            strategies = retriever.get_optimized_retrieval_strategies()
            print(
                json.dumps(
                    {"success": True, "strategies": [asdict(s) for s in strategies]},
                    indent=2,
                )
            )

        elif args.command == "execute-strategies":
            if not retriever.gmail_service:
                print(
                    json.dumps(
                        {
                            "success": False,
                            "error": "Gmail authentication failed. Cannot execute strategies.",
                        },
                        indent=2,
                    )
                )
                sys.exit(1)

            selected_strategies = None
            if args.strategies:
                all_strategies = retriever.get_optimized_retrieval_strategies()
                selected_strategies = [s for s in all_strategies if s.name in args.strategies]
                if not selected_strategies:
                    print(
                        json.dumps(
                            {
                                "success": False,
                                "error": f"Specified strategy names not found: {args.strategies}",
                            },
                            indent=2,
                        )
                    )
                    sys.exit(1)

            results = await retriever.execute_smart_retrieval(
                strategies=selected_strategies,
                max_api_calls=args.max_api_calls,
                time_budget_minutes=args.time_budget_minutes,
            )
            print(json.dumps({"success": True, "results": results}, indent=2))

        elif args.command == "get-retrieval-analytics":
            analytics = retriever.get_retrieval_analytics(days=args.days)
            print(json.dumps({"success": True, "analytics": analytics}, indent=2))

    except Exception as e:
        logging.exception("An critical error occurred during CLI command execution:")
        print(
            json.dumps(
                {"success": False, "error": f"An unexpected error occurred: {str(e)}"},
                indent=2,
            )
        )
        sys.exit(1)


if __name__ == "__main__":
    # Configure logging. Default to INFO, but allow override via environment variable for debugging.
    log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(levelname)s - %(name)s - %(module)s.%(funcName)s:%(lineno)d - %(message)s",
    )

    # Reduce verbosity of Google API client libraries unless LOG_LEVEL is DEBUG
    if log_level > logging.DEBUG:
        logging.getLogger("googleapiclient.discovery").setLevel(logging.WARNING)
        logging.getLogger("google.auth.transport.requests").setLevel(logging.WARNING)
        logging.getLogger("oauth2client.client").setLevel(
            logging.WARNING
        )  # For older versions if present

    asyncio.run(main_cli())
>>>>>>> origin/feat/modular-ai-platform
