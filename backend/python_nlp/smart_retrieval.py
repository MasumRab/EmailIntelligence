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
DEFAULT_CHECKPOINT_DB_PATH = os.path.join(PROJECT_ROOT, "data", "sync_checkpoints.db")


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


class GmailRetrievalService:
    """
    Service for retrieving emails from Gmail using the Gmail API.
    """

    def __init__(
        self,
        credentials_path: str = CREDENTIALS_PATH,
        token_path: str = TOKEN_JSON_PATH,
        checkpoint_db_path: str = DEFAULT_CHECKPOINT_DB_PATH,
    ):
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.checkpoint_db_path = checkpoint_db_path
        self.creds = None
        self.service = None
        self._db_conn = None
        self.logger = logging.getLogger(__name__)

    def authenticate(self):
        """Authenticate with Gmail API using OAuth2."""
        # Load existing token if available
        if os.path.exists(self.token_path):
            self.creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)

        # If no valid credentials, request authorization
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                # Use credentials from environment variable if available
                creds_json = os.getenv(GMAIL_CREDENTIALS_ENV_VAR)
                if creds_json:
                    import json as json_std
                    import tempfile

                    # Write credentials to a temporary file
                    with tempfile.NamedTemporaryFile(
                        mode="w", delete=False, suffix=".json"
                    ) as temp_file:
                        temp_file.write(creds_json)
                        temp_creds_path = temp_file.name

                    flow = InstalledAppFlow.from_client_secrets_file(temp_creds_path, SCOPES)
                    self.creds = flow.run_local_server(port=0)

                    # Clean up temporary file
                    os.unlink(temp_creds_path)
                else:
                    # Use credentials file from disk
                    flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, SCOPES)
                    self.creds = flow.run_local_server(port=0)

            # Save credentials for next run
            with open(self.token_path, "w") as token:
                token.write(self.creds.to_json())

        self.service = build("gmail", "v1", credentials=self.creds)

    def _init_checkpoint_db(self):
        """Initialize the checkpoint database if it doesn't exist."""
        self._db_conn = sqlite3.connect(self.checkpoint_db_path)
        cursor = self._db_conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sync_checkpoints (
                strategy_name TEXT PRIMARY KEY,
                last_sync_date TEXT,
                last_history_id TEXT,
                processed_count INTEGER,
                next_page_token TEXT,
                errors_count INTEGER
            )
        """
        )
        self._db_conn.commit()

    def get_checkpoint(self, strategy_name: str) -> Optional[SyncCheckpoint]:
        """Retrieve a sync checkpoint for a given strategy."""
        if not self._db_conn:
            self._init_checkpoint_db()

        cursor = self._db_conn.cursor()
        cursor.execute("SELECT * FROM sync_checkpoints WHERE strategy_name = ?", (strategy_name,))
        row = cursor.fetchone()

        if row:
            return SyncCheckpoint(
                strategy_name=row[0],
                last_sync_date=datetime.fromisoformat(row[1]) if row[1] else None,
                last_history_id=row[2],
                processed_count=row[3] or 0,
                next_page_token=row[4],
                errors_count=row[5] or 0,
            )
        return None

    def save_checkpoint(self, checkpoint: SyncCheckpoint):
        """Save a sync checkpoint."""
        if not self._db_conn:
            self._init_checkpoint_db()

        cursor = self._db_conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO sync_checkpoints 
            (strategy_name, last_sync_date, last_history_id, processed_count, next_page_token, errors_count)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                checkpoint.strategy_name,
                checkpoint.last_sync_date.isoformat() if checkpoint.last_sync_date else None,
                checkpoint.last_history_id,
                checkpoint.processed_count,
                checkpoint.next_page_token,
                checkpoint.errors_count,
            ),
        )
        self._db_conn.commit()

    def retrieve_emails(
        self, strategy: RetrievalStrategy, max_emails: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve emails based on the provided strategy.

        Args:
            strategy: The retrieval strategy to use
            max_emails: Maximum number of emails to retrieve (overrides strategy setting)

        Returns:
            A list of email objects retrieved from Gmail
        """
        if not self.service:
            self.authenticate()

        # Use strategy's max_emails_per_run unless overridden
        max_to_retrieve = max_emails or strategy.max_emails_per_run

        # Get any existing checkpoint for this strategy
        checkpoint = self.get_checkpoint(strategy.name)

        emails = []
        page_token = None
        total_retrieved = 0

        # Determine query based on strategy and checkpoint
        query_parts = [strategy.query_filter] if strategy.query_filter else []

        # Add date range if specified
        if strategy.date_range_days:
            from datetime import datetime, timedelta

            start_date = datetime.now() - timedelta(days=strategy.date_range_days)
            query_parts.append(f"after:{start_date.strftime('%Y/%m/%d')}")

        query = " ".join(query_parts)

        try:
            while total_retrieved < max_to_retrieve:
                # Construct the API call
                api_call = (
                    self.service.users()
                    .messages()
                    .list(
                        userId="me",
                        q=query,
                        maxResults=min(strategy.batch_size, max_to_retrieve - total_retrieved),
                        pageToken=page_token,
                    )
                )

                response = api_call.execute()

                # Process messages in this batch
                messages = response.get("messages", [])
                if not messages:
                    # No more messages available
                    break

                # Get detailed information for each message
                for msg in messages:
                    try:
                        # Get full message details
                        full_msg = (
                            self.service.users().messages().get(userId="me", id=msg["id"]).execute()
                        )

                        # Convert to our internal format
                        email_data = self._parse_gmail_message(full_msg)
                        emails.append(email_data)
                        total_retrieved += 1

                        # Update checkpoint with the latest history ID
                        if "historyId" in full_msg:
                            if checkpoint:
                                checkpoint.last_history_id = full_msg["historyId"]
                                checkpoint.processed_count += 1
                                self.save_checkpoint(checkpoint)
                            else:
                                new_checkpoint = SyncCheckpoint(
                                    strategy_name=strategy.name,
                                    last_sync_date=datetime.now(),
                                    last_history_id=full_msg["historyId"],
                                    processed_count=1,
                                )
                                self.save_checkpoint(new_checkpoint)

                        if total_retrieved >= max_to_retrieve:
                            break

                    except HttpError as e:
                        self.logger.error(f"Error retrieving message {msg['id']}: {e}")
                        if checkpoint:
                            checkpoint.errors_count += 1
                            self.save_checkpoint(checkpoint)

                # Check for next page
                page_token = response.get("nextPageToken")
                if not page_token:
                    # No more pages
                    break

        except HttpError as e:
            self.logger.error(f"Error during email retrieval: {e}")
            raise

        return emails

    def _parse_gmail_message(self, gmail_msg: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse a Gmail API message object into our internal format.

        Args:
            gmail_msg: The raw Gmail API message object

        Returns:
            A dictionary with our internal email format
        """
        # Extract headers
        headers = {
            h["name"].lower(): h["value"] for h in gmail_msg.get("payload", {}).get("headers", [])
        }

        # Extract body
        body = ""
        payload = gmail_msg.get("payload", {})
        parts = payload.get("parts", [])

        # Look for the text/plain part
        for part in parts:
            if part.get("mimeType") == "text/plain":
                import base64

                data = part.get("body", {}).get("data")
                if data:
                    # Decode base64 encoded body
                    body = base64.urlsafe_b64decode(data).decode("utf-8")
                break
        else:
            # If no text/plain part found, look for body in the payload itself
            if payload.get("mimeType") == "text/plain":
                import base64

                data = payload.get("body", {}).get("data")
                if data:
                    body = base64.urlsafe_b64decode(data).decode("utf-8")

        # Construct our email format
        email_data = {
            "id": gmail_msg.get("id"),
            "thread_id": gmail_msg.get("threadId"),
            "label_ids": gmail_msg.get("labelIds", []),
            "subject": headers.get("subject", ""),
            "sender": headers.get("from", ""),
            "sender_email": self._extract_email(headers.get("from", "")),
            "recipients": headers.get("to", ""),
            "cc": headers.get("cc", ""),
            "bcc": headers.get("bcc", ""),
            "date": headers.get("date", ""),
            "content": body,
            "size_estimate": gmail_msg.get("sizeEstimate", 0),
            "history_id": gmail_msg.get("historyId"),
            "internal_date": gmail_msg.get("internalDate"),
        }

        return email_data

    def _extract_email(self, from_header: str) -> str:
        """
        Extract email address from a 'From' header that might be in format 'Name <email@domain.com>'.

        Args:
            from_header: The raw 'From' header value

        Returns:
            The extracted email address
        """
        import re

        # Pattern to match email addresses in the form 'Name <email>' or just 'email'
        pattern = r"<([^>]+)>|([^<>\s]+@[^<>\s]+)"
        match = re.search(pattern, from_header)
        if match:
            # Group 1 is for <email> format, group 2 is for plain email format
            return match.group(1) or match.group(2)
        return from_header


async def main():
    """Main function demonstrating usage of the Gmail retrieval service."""
    parser = argparse.ArgumentParser(description="Gmail Retrieval Service")
    parser.add_argument(
        "--credentials-path", default=CREDENTIALS_PATH, help="Path to credentials.json file"
    )
    parser.add_argument("--token-path", default=TOKEN_JSON_PATH, help="Path to token.json file")
    parser.add_argument("--query", default="from:me after:2023-01-01", help="Gmail search query")
    parser.add_argument(
        "--max-emails", type=int, default=10, help="Maximum number of emails to retrieve"
    )
    parser.add_argument("--batch-size", type=int, default=10, help="Batch size for API requests")

    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Create a retrieval strategy
    strategy = RetrievalStrategy(
        name="default_strategy",
        query_filter=args.query,
        priority=1,
        batch_size=args.batch_size,
        frequency="manual",
        max_emails_per_run=args.max_emails,
        include_folders=[],
        exclude_folders=[],
        date_range_days=30,
    )

    # Create and use the retrieval service
    service = GmailRetrievalService(
        credentials_path=args.credentials_path, token_path=args.token_path
    )

    try:
        emails = service.retrieve_emails(strategy, max_emails=args.max_emails)
        print(f"Retrieved {len(emails)} emails")

        # Print first email as example
        if emails:
            print("\nFirst email:")
            print(json.dumps(emails[0], indent=2, default=str))

    except Exception as e:
        print(f"Error retrieving emails: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())


# Work-in-progress implementation: SmartRetrievalManager as an extension
class SmartRetrievalManager(GmailRetrievalService):
    """
    Extended retrieval system with optimized strategies and smart features.
    This class extends GmailRetrievalService to add advanced functionality
    while maintaining all original capabilities.
    """

    def __init__(
        self,
        checkpoint_db_path: str = DEFAULT_CHECKPOINT_DB_PATH,
        credentials_path: str = CREDENTIALS_PATH,
        token_path: str = TOKEN_JSON_PATH,
    ):
        # Initialize the parent class
        super().__init__(credentials_path, token_path, checkpoint_db_path)

        # Additional attributes for advanced functionality
        self.retrieval_strategies = []

        # Initialize checkpoint database for advanced features if not already done by parent
        if not hasattr(self, "_db_conn") or self._db_conn is None:
            self._init_checkpoint_db()

    def _store_credentials(self, creds: Credentials):
        """
        Store credentials to file (this is already handled by parent class).
        """
        # Using the credential management from parent class
        # This method is preserved as a placeholder for potential custom logic
        super()._store_credentials(creds)  # assuming parent has a method

    def get_optimized_retrieval_strategies(self) -> List[RetrievalStrategy]:
        """
        Retrieve optimized strategies for email retrieval (WIP).
        """
        # TODO: Implement logic to determine optimized strategies
        # For now, return a default strategy
        default_strategy = RetrievalStrategy(
            name="default_optimized",
            query_filter="from:me after:2023-01-01",
            priority=1,
            batch_size=50,
            frequency="daily",
            max_emails_per_run=100,
            include_folders=["INBOX"],
            exclude_folders=["TRASH", "SPAM"],
            date_range_days=30,
        )
        self.retrieval_strategies = [default_strategy]
        return self.retrieval_strategies

    def get_incremental_query(
        self, strategy: RetrievalStrategy, checkpoint: Optional[SyncCheckpoint] = None
    ) -> str:
        """
        Construct an incremental query based on checkpoint (WIP).
        """
        base_query = strategy.query_filter
        if checkpoint and checkpoint.last_sync_date:
            # Add date filter based on last sync to make query incremental
            base_query += f" after:{checkpoint.last_sync_date.strftime('%Y/%m/%d')}"
        return base_query

    async def execute_smart_retrieval(
        self,
        strategies: Optional[List[RetrievalStrategy]] = None,
        max_api_calls: int = 100,
        time_budget_minutes: int = 30,
    ) -> Dict[str, Any]:
        """
        Execute smart retrieval with provided strategies, API call limits, and time budget.

        Args:
            strategies: A list of strategies to execute. If None, uses default optimized strategies.
            max_api_calls: The maximum number of API calls to make.
            time_budget_minutes: The time limit in minutes for the retrieval process.
        """
        # Use the strategies if provided, otherwise get optimized strategies
        if not strategies:
            strategies = self.get_optimized_retrieval_strategies()

        # Track API calls to respect the limit
        api_call_count = 0
        start_time = datetime.now()
        all_retrieved_emails = []

        self.logger.info(
            f"Starting smart retrieval with {len(strategies)} strategies, "
            f"max {max_api_calls} API calls and {time_budget_minutes} min budget"
        )

        for strategy in strategies:
            if api_call_count >= max_api_calls:
                self.logger.info("Reached maximum API call limit")
                break

            elapsed_time = (datetime.now() - start_time).total_seconds() / 60
            if elapsed_time >= time_budget_minutes:
                self.logger.info("Reached time budget limit")
                break

            # Get any existing checkpoint for this strategy
            checkpoint = self.get_checkpoint(strategy.name)

            # Get incremental query based on checkpoint
            query = self.get_incremental_query(strategy, checkpoint)

            # Temporarily modify strategy to use incremental query
            original_query = strategy.query_filter
            strategy.query_filter = query

            # Use the parent's retrieval method with current strategy
            self.logger.info(f"Executing retrieval with strategy: {strategy.name}, query: {query}")
            emails = self.retrieve_emails(strategy)
            all_retrieved_emails.extend(emails)

            # Restore original query
            strategy.query_filter = original_query

            # Update checkpoint
            if emails:
                new_checkpoint = SyncCheckpoint(
                    strategy_name=strategy.name,
                    last_sync_date=datetime.now(),
                    last_history_id=emails[-1].get("history_id", ""),
                    processed_count=len(emails),
                    next_page_token=None,
                    errors_count=0,
                )
                self.save_checkpoint(new_checkpoint)

            # Increment API call count (estimate)
            api_call_count += min(
                strategy.max_emails_per_run // strategy.batch_size + 1, 10
            )  # Rough estimate

        total_time = (datetime.now() - start_time).total_seconds() / 60
        self.logger.info(
            f"Smart retrieval completed in {total_time:.2f} minutes, "
            f"made {api_call_count} API calls, retrieved {len(all_retrieved_emails)} emails"
        )

        return {
            "emails": all_retrieved_emails,
            "api_calls_made": api_call_count,
            "time_elapsed_minutes": total_time,
            "strategies_used": [s.name for s in strategies],
            "total_retrieved": len(all_retrieved_emails),
        }

    def _save_checkpoint(self, checkpoint: SyncCheckpoint):
        """
        Save a sync checkpoint.
        Using the checkpoint functionality from parent class.
        """
        # Delegate to the parent class's save_checkpoint method
        self.save_checkpoint(checkpoint)  # Call the instance method directly, not super()


async def main_cli():
    """Provides a command-line interface for the SmartGmailRetriever."""
    parser = argparse.ArgumentParser(description="Smart Gmail Retriever CLI")

    # TODO: Implement CLI logic
    # Pseudo code for CLI implementation:
    # parser.add_argument("--strategies", nargs="+", help="Retrieval strategies to use")
    # parser.add_argument("--max-api-calls", type=int, default=100, help="Maximum API calls")
    # parser.add_argument("--time-budget", type=int, default=30, help="Time budget in minutes")
    # parser.add_argument("--output", help="Output file path")
    # parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    # args = parser.parse_args()

    # try:
    #     # Initialize SmartGmailRetriever
    #     # retriever = SmartGmailRetriever()
    #
    #     # Execute smart retrieval
    #     # result = await retriever.execute_smart_retrieval(
    #     #     strategies=args.strategies,
    #     #     max_api_calls=args.max_api_calls,
    #     #     time_budget_minutes=args.time_budget
    #     # )
    #
    #     # Handle output (JSON, CSV, etc.)
    #     # if args.output:
    #     #     # Save to file
    #     # else:
    #     #     # Print to console
    #
    # except Exception as e:
    #     # Handle errors
    #     # print(f"Error: {e}", file=sys.stderr)
    #     # sys.exit(1)

    # Placeholder implementation
    print("CLI not yet implemented. Use the API instead.")
    pass


if __name__ == "__main__":
    asyncio.run(main_cli())
