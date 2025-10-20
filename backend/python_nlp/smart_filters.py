"""
A system for managing and applying intelligent email filters.

This module provides functionalities for creating, storing, evaluating, and
pruning smart email filters. It uses a SQLite database for persistence and
includes logic for generating filters based on email patterns.
"""

import json
import logging
import os
import re
import sqlite3
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

# Define the project's root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_DB_PATH = os.path.join(PROJECT_ROOT, "smart_filters.db")


@dataclass
class EmailFilter:
    """Represents a structured definition of an email filter."""
    filter_id: str
    name: str
    description: str
    criteria: Dict[str, Any]
    actions: Dict[str, Any]
    priority: int
    effectiveness_score: float
    created_date: datetime
    last_used: datetime
    usage_count: int
    false_positive_rate: float
    performance_metrics: Dict[str, float]


class SmartFilterManager:
    """Manages the lifecycle of smart email filters."""

    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        """Initializes the SmartFilterManager."""
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_filter_db()
        self.filter_templates = self._load_filter_templates()

    def _init_filter_db(self):
        """Initializes the filter database schema."""
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS email_filters (
                    filter_id TEXT PRIMARY KEY, name TEXT NOT NULL, description TEXT,
                    criteria TEXT NOT NULL, actions TEXT NOT NULL, priority INTEGER DEFAULT 5,
                    effectiveness_score REAL DEFAULT 0.0, created_date TEXT, last_used TEXT,
                    usage_count INTEGER DEFAULT 0, false_positive_rate REAL DEFAULT 0.0,
                    performance_metrics TEXT, is_active BOOLEAN DEFAULT 1
                )
                """
            )

    def _load_filter_templates(self) -> Dict[str, Dict[str, Any]]:
        """Loads a set of predefined filter templates."""
        return {
            "high_priority_work": {"criteria": {"subject_keywords": ["urgent", "important"]}, "actions": {"mark_important": True}, "priority": 9, "description": "High priority work"},
            "financial_documents": {"criteria": {"subject_keywords": ["invoice", "statement"]}, "actions": {"add_label": "Finance"}, "priority": 7, "description": "Financial documents"},
        }

    def add_custom_filter(self, name: str, description: str, criteria: Dict[str, Any], actions: Dict[str, Any], priority: int) -> EmailFilter:
        """Adds a new user-defined filter to the system."""
        filter_id = f"custom_{name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        new_filter = EmailFilter(filter_id, name, description, criteria, actions, priority, 0.0, datetime.now(), datetime.now(), 0, 0.0, {})
        self._save_filter(new_filter)
        self.logger.info(f"Custom filter '{name}' added with ID: {filter_id}")
        return new_filter

    def _save_filter(self, filter_obj: EmailFilter):
        """Saves a filter to the database."""
        with self.conn:
            self.conn.execute(
                "INSERT OR REPLACE INTO email_filters VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    filter_obj.filter_id, filter_obj.name, filter_obj.description,
                    json.dumps(filter_obj.criteria), json.dumps(filter_obj.actions),
                    filter_obj.priority, filter_obj.effectiveness_score,
                    filter_obj.created_date.isoformat(), filter_obj.last_used.isoformat(),
                    filter_obj.usage_count, filter_obj.false_positive_rate,
                    json.dumps(filter_obj.performance_metrics), True
                )
            )

    def get_active_filters_sorted(self) -> List[EmailFilter]:
        """Loads all active filters from the database, sorted by priority."""
        cursor = self.conn.execute("SELECT * FROM email_filters WHERE is_active = 1 ORDER BY priority DESC")
        rows = cursor.fetchall()
        return [self._row_to_email_filter(row) for row in rows]

    def _row_to_email_filter(self, row: sqlite3.Row) -> EmailFilter:
        """Converts a database row to an EmailFilter object."""
        return EmailFilter(
            row["filter_id"], row["name"], row["description"],
            json.loads(row["criteria"]), json.loads(row["actions"]),
            row["priority"], row["effectiveness_score"],
            datetime.fromisoformat(row["created_date"]), datetime.fromisoformat(row["last_used"]),
            row["usage_count"], row["false_positive_rate"], json.loads(row["performance_metrics"])
        )

    def apply_filters_to_email_data(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """Applies all active filters to an email and returns a summary of actions."""
        summary = {"filters_matched": [], "actions_taken": []}
        for filter_obj in self.get_active_filters_sorted():
            if self._apply_filter_to_email(filter_obj, email_data):
                summary["filters_matched"].append(filter_obj.name)
                # In a real implementation, you would also apply the actions
        return summary

    def _apply_filter_to_email(self, filter_obj: EmailFilter, email: Dict[str, Any]) -> bool:
        """Applies a single filter's criteria to an email."""
        criteria = filter_obj.criteria
        # Simplified logic, can be expanded to be more robust
        if "from_patterns" in criteria and not any(re.search(p, email.get("senderEmail", ""), re.IGNORECASE) for p in criteria["from_patterns"]):
            return False
        if "subject_keywords" in criteria and not any(k.lower() in email.get("subject", "").lower() for k in criteria["subject_keywords"]):
            return False
        return True

    def create_intelligent_filters(self, email_samples: List[Dict[str, Any]]) -> List[EmailFilter]:
        """Analyzes email samples to intelligently generate and store new filters."""
        # Simplified logic for demonstration
        created_filters = []
        if not email_samples:
            return created_filters

        # Example: Create a filter for a common sender domain
        domain_counts = Counter(self._extract_domain(email.get("senderEmail", "")) for email in email_samples)
        common_domain, count = domain_counts.most_common(1)[0]
        if count > 1: # If a domain appears more than once
            filter_name = f"Auto: From {common_domain}"
            new_filter = self.add_custom_filter(
                name=filter_name,
                description=f"Automatically generated filter for emails from {common_domain}",
                criteria={"from_patterns": [re.escape(common_domain)]},
                actions={"add_label": "Auto-Filtered"},
                priority=3
            )
            created_filters.append(new_filter)
        return created_filters

    def _extract_domain(self, email_address: str) -> str:
        """Extracts the domain from an email address."""
        return email_address.split("@")[1].lower() if "@" in email_address else ""

    def prune_ineffective_filters(self) -> Dict[str, Any]:
        """Removes or disables filters that are no longer effective."""
        # Simplified logic for demonstration
        return {"pruned_filters": [], "disabled_filters": []}

def main():
    """Demonstrates the usage of the SmartFilterManager."""
    manager = SmartFilterManager(db_path=":memory:")
    sample_emails = [{"senderEmail": "test@example.com", "subject": "Urgent Meeting"}, {"senderEmail": "another@example.com", "subject": "Project Update"}]
    filters = manager.create_intelligent_filters(sample_emails)
    print(f"Created {len(filters)} filters.")
    if filters:
        print(f"Applied filters to sample email: {manager.apply_filters_to_email_data(sample_emails[0])}")

if __name__ == "__main__":
    main()
