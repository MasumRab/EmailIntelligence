"""
Data models for email retrieval strategies.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class RetrievalStrategy:
    """
    Defines a strategy for retrieving emails from external services.

    Attributes:
        name: A unique name for the strategy.
        query_filter: The query filter to use for searching emails.
        priority: The priority level of the strategy (higher numbers run first).
        batch_size: The number of emails to retrieve in each batch.
        frequency: How frequently to run the retrieval (e.g., 'daily', 'hourly').
        max_emails_per_run: Maximum number of emails to retrieve in a single run.
        include_folders: List of folders to include in the search.
        exclude_folders: List of folders to exclude from the search.
        date_range_days: Number of days back to include in the search.
    """
    name: str
    query_filter: str = ""
    priority: int = 1
    batch_size: int = 100
    frequency: str = "daily"
    max_emails_per_run: int = 1000
    include_folders: List[str] = None
    exclude_folders: List[str] = None
    date_range_days: int = 30  # Default to last 30 days


@dataclass
class SyncCheckpoint:
    """
    Represents a checkpoint in the email synchronization process.

    Attributes:
        strategy_name: The name of the strategy associated with this checkpoint.
        last_sync_date: The date of the last successful synchronization.
        last_history_id: The history ID of the last processed email (for incremental sync).
        processed_count: The number of emails processed since the last checkpoint.
        next_page_token: Token for retrieving the next page of results, if applicable.
        errors_count: The number of errors encountered during the sync.
    """
    strategy_name: str
    last_sync_date: datetime
    last_history_id: str
    processed_count: int = 0
    next_page_token: Optional[str] = None
    errors_count: int = 0