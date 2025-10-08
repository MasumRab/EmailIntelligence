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
    strategy_name: str
    last_sync_date: datetime
    last_history_id: str
    processed_count: int
    next_page_token: Optional[str]
    errors_count: int

class SmartGmailRetriever:

    def __init__(self, checkpoint_db_path: str = DEFAULT_CHECKPOINT_DB_PATH):
        """Initializes the SmartGmailRetriever."""
        self.logger = logging.getLogger(__name__)
        self.checkpoint_db_path = checkpoint_db_path
        self.gmail_service = None
        self._init_checkpoint_db()
        creds = self._load_credentials() or self._authenticate()
        if creds and creds.valid:
            self.gmail_service = build('gmail', 'v1', credentials=creds)

    def _init_checkpoint_db(self):
        with sqlite3.connect(self.checkpoint_db_path) as conn:
            conn.execute('CREATE TABLE IF NOT EXISTS sync_checkpoints (strategy_name TEXT PRIMARY KEY, last_sync_date TEXT, last_history_id TEXT)')
            conn.execute('CREATE TABLE IF NOT EXISTS retrieval_stats (date TEXT PRIMARY KEY, total_retrieved INTEGER, api_calls_used INTEGER)')

    def _load_credentials(self) -> Optional[Credentials]:
        if os.path.exists(TOKEN_JSON_PATH):
            return Credentials.from_authorized_user_file(TOKEN_JSON_PATH, SCOPES)
        return None

    def _store_credentials(self, creds: Credentials):
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
        base_query = strategy.query_filter
        if checkpoint and checkpoint.last_sync_date:
            base_query += f' after:{int(checkpoint.last_sync_date.timestamp())}'
        return base_query

    async def execute_smart_retrieval(self, strategies: Optional[List[RetrievalStrategy]]=None, max_api_calls: int=100, time_budget_minutes: int=30) -> Dict[str, Any]:
        """
        Executes a series of retrieval strategies within given constraints.

        Args:
            strategies: A list of strategies to execute. If None, uses default optimized strategies.
            max_api_calls: The maximum number of API calls to make.
            time_budget_minutes: The time limit in minutes for the retrieval process.

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