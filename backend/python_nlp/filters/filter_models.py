"""
Data models for email filters.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class EmailFilter:
    """
    Represents a structured definition of an email filter.

    Attributes:
        filter_id: A unique identifier for the filter.
        name: A human-readable name for the filter.
        description: A brief description of what the filter does.
        criteria: A dictionary defining the conditions for the filter to match.
        actions: A dictionary defining the actions to take when the filter matches.
        priority: The priority level of the filter (higher numbers run first).
        effectiveness_score: A score representing the filter's performance.
        created_date: The date when the filter was created.
        last_used: The timestamp of the last time the filter was used.
        usage_count: The total number of times the filter has been used.
        false_positive_rate: The calculated false positive rate for the filter.
        performance_metrics: A dictionary of detailed performance metrics.
    """

    filter_id: str
    name: str
    description: str
    criteria: Dict[str, Any]
    actions: Dict[str, Any]
    priority: int = 1
    effectiveness_score: float = 0.0
    created_date: Optional[datetime] = None
    last_used: Optional[datetime] = None
    usage_count: int = 0
    false_positive_rate: float = 0.0
    performance_metrics: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if self.created_date is None:
            self.created_date = datetime.now()
        if self.performance_metrics is None:
            self.performance_metrics = {}
        if self.criteria is None:
            self.criteria = {}
        if self.actions is None:
            self.actions = {}