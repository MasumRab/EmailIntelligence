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
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Set

from src.core.security import PathValidator

# Define paths for data storage
# Use the project's data directory for database files to avoid cluttering the root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
DEFAULT_DB_PATH = os.path.join(DATA_DIR, "smart_filters.db")


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
    priority: int
    effectiveness_score: float
    created_date: datetime
    last_used: datetime
    usage_count: int
    false_positive_rate: float
    performance_metrics: Dict[str, float]


@dataclass
class FilterPerformance:
    """
    Holds performance analytics for a single email filter.

    Attributes:
        filter_id: The ID of the filter being measured.
        accuracy: The accuracy score of the filter.
        precision: The precision score of the filter.
        recall: The recall score of the filter.
        f1_score: The F1 score of the filter.
        processing_time_ms: The average processing time in milliseconds.
        emails_processed: The number of emails processed during evaluation.
        true_positives: The count of true positive matches.
        false_positives: The count of false positive matches.
        false_negatives: The count of false negative matches.
    """

    filter_id: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    processing_time_ms: float
    emails_processed: int
    true_positives: int
    false_positives: int
    false_negatives: int


class SmartFilterManager:
    """
    Manages the lifecycle of smart email filters.

    This class handles the creation, storage, application, and optimization
    of email filters, using a SQLite database for persistence.
    """

    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        """
        Initializes the SmartFilterManager.

        Args:
            db_path: Path to the SQLite database file. If None, uses the default
                    path in the project's data directory. Relative paths are
                    resolved relative to the project's data directory to prevent
                    path traversal attacks and ensure consistent behavior.
        """
<<<<<<< HEAD
        self.db_path = db_path
=======
        if db_path is None:
            db_path = DEFAULT_DB_PATH
        elif not os.path.isabs(db_path):
            # Secure path validation to prevent directory traversal
            filename = PathValidator.sanitize_filename(os.path.basename(db_path))
            db_path = os.path.join(DATA_DIR, filename)

        # Validate the final path
        self.db_path = str(PathValidator.validate_database_path(db_path, DATA_DIR))
>>>>>>> scientific
        self.logger = logging.getLogger(__name__)
        self.conn = None
        if self.db_path == ":memory:":
            self.conn = sqlite3.connect(":memory:")
            self.conn.row_factory = sqlite3.Row
        self._init_filter_db()
        self.filter_templates = self._load_filter_templates()
        self.pruning_criteria = self._load_pruning_criteria()

    def _get_db_connection(self) -> sqlite3.Connection:
        """Establishes and returns a database connection."""
        if self.conn:
            return self.conn
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _close_db_connection(self, conn: sqlite3.Connection):
        """Closes the database connection if it's not a persistent one."""
        if conn is not self.conn:
            conn.close()

    def _db_execute(self, query: str, params: tuple = (), retries: int = 3):
        """Execute a query (INSERT, UPDATE, DELETE) with retry logic for robustness."""
        for attempt in range(retries):
            conn = self._get_db_connection()
            try:
                conn.execute(query, params)
                conn.commit()
                return
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e) and attempt < retries - 1:
                    self.logger.warning(f"Database locked, retrying ({attempt + 1}/{retries}): {e}")
                    import time

                    time.sleep(0.1 * (attempt + 1))  # Exponential backoff
                    continue
                else:
                    self.logger.error(
                        f"Database error after {retries} attempts: {e} with query: {query[:100]}"
                    )
                    raise
            except sqlite3.Error as e:
                self.logger.error(f"Database error: {e} with query: {query[:100]}")
                raise
            finally:
                self._close_db_connection(conn)

    def _db_fetchone(self, query: str, params: tuple = ()) -> Optional[sqlite3.Row]:
        """Executes a read query and fetches a single row."""
        conn = self._get_db_connection()
        try:
            return conn.execute(query, params).fetchone()
        except sqlite3.Error as e:
            self.logger.error(f"Database error on fetchone: {e}")
            return None
        finally:
            self._close_db_connection(conn)

    def _db_fetchall(self, query: str, params: tuple = ()) -> List[sqlite3.Row]:
        """Executes a read query and fetches all rows."""
        conn = self._get_db_connection()
        try:
            return conn.execute(query, params).fetchall()
        except sqlite3.Error as e:
            self.logger.error(f"Database error on fetchall: {e}")
            return []
        finally:
            self._close_db_connection(conn)

    def _init_filter_db(self):
        """Initializes the filter database schema if it doesn't exist."""
        queries = [
            """
            CREATE TABLE IF NOT EXISTS email_filters (
                filter_id TEXT PRIMARY KEY, name TEXT NOT NULL, description TEXT,
                criteria TEXT NOT NULL, actions TEXT NOT NULL, priority INTEGER DEFAULT 5,
                effectiveness_score REAL DEFAULT 0.0, created_date TEXT, last_used TEXT,
                usage_count INTEGER DEFAULT 0, false_positive_rate REAL DEFAULT 0.0,
                performance_metrics TEXT, is_active BOOLEAN DEFAULT 1
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS filter_performance (
                performance_id TEXT PRIMARY KEY, filter_id TEXT, measurement_date TEXT,
                accuracy REAL, precision_score REAL, recall_score REAL, f1_score REAL,
                processing_time_ms REAL, emails_processed INTEGER, true_positives INTEGER,
                false_positives INTEGER, false_negatives INTEGER,
                FOREIGN KEY (filter_id) REFERENCES email_filters (filter_id)
            )
            """,
        ]
        for query in queries:
            self._db_execute(query)

    def close(self):
        """Closes the persistent database connection."""
        if self.conn:
            self.conn.close()

    def _load_filter_templates(self) -> Dict[str, Dict[str, Any]]:
        """Loads a set of predefined filter templates."""
        return {
            "high_priority_work": {
                "criteria": {"subject_keywords": ["urgent", "important"]},
                "actions": {"mark_important": True},
                "priority": 9,
                "description": "High priority work",
            },
            "financial_documents": {
                "criteria": {"subject_keywords": ["invoice", "statement"]},
                "actions": {"add_label": "Finance"},
                "priority": 7,
                "description": "Financial documents",
            },
        }

    def _load_pruning_criteria(self) -> Dict[str, Any]:
        """Loads the criteria used for pruning ineffective filters."""
        return {"effectiveness_threshold": 0.3, "usage_threshold": 10, "age_threshold_days": 90}

    def create_intelligent_filters(self, email_samples: List[Dict[str, Any]]) -> List[EmailFilter]:
        """
        Analyzes email samples to intelligently generate and store new filters.

        Args:
            email_samples: A list of email data dictionaries to analyze.

        Returns:
            A list of the newly created `EmailFilter` objects.
        """
        created_filters = []
        patterns = self._analyze_email_patterns(email_samples)
        template_filters = self._create_filters_from_templates(patterns)
        created_filters.extend(template_filters)
        custom_filters = self._create_custom_filters(patterns)
        created_filters.extend(custom_filters)
        self.logger.info(f"Created {len(created_filters)} intelligent filters")
        return created_filters

    def _create_filters_from_templates(self, patterns: Dict[str, Any]) -> List[EmailFilter]:
        """Creates filters from templates that match the analyzed patterns."""
        filters = []
        for name, template in self.filter_templates.items():
            if self._should_create_filter(template, patterns):
                filter_obj = self._create_filter_from_template(name, template)
                self._save_filter(filter_obj)
                filters.append(filter_obj)
        return filters

    def _extract_patterns_from_single_email(self, email: Dict[str, Any]) -> Dict[str, Any]:
        """Extracts key patterns from a single email."""
        patterns = {}
        if domain := self._extract_domain(email.get("senderEmail", "")):
            patterns["sender_domain"] = domain
        if keywords := self._extract_keywords(email.get("subject", "")):
            patterns["subject_keywords"] = keywords
        return patterns

    def _analyze_email_patterns(self, email_samples: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregates patterns found across a list of email samples."""
        aggregated = {"sender_domains": Counter(), "subject_keywords": Counter()}
        for email in email_samples:
            patterns = self._extract_patterns_from_single_email(email)
            if "sender_domain" in patterns:
                aggregated["sender_domains"][patterns["sender_domain"]] += 1
            if "subject_keywords" in patterns:
                aggregated["subject_keywords"].update(patterns["subject_keywords"])
        return aggregated

    def _extract_domain(self, email_address: str) -> str:
        """Extracts the domain from an email address."""
        return email_address.split("@")[1].lower() if "@" in email_address else ""

    def _extract_keywords(self, text: str) -> List[str]:
        """Extracts meaningful keywords from a string of text."""
        return [word for word in re.findall(r"\b[a-zA-Z]{3,}\b", text.lower()) if len(word) > 3]

    def _is_automated_email(self, email: Dict[str, Any]) -> bool:
        """Determines if an email is likely automated."""
        return any(ind in email.get("senderEmail", "").lower() for ind in ["noreply", "automated"])

    def _should_create_filter(self, template: Dict[str, Any], patterns: Dict[str, Any]) -> bool:
        """Determines if a filter should be created based on a template and discovered patterns."""
        return True  # Simplified logic

    def _create_filter_from_template(self, name: str, template: Dict[str, Any]) -> EmailFilter:
        """Creates an EmailFilter object from a template."""
        return EmailFilter(
            f"template_{name}",
            name,
            template["description"],
            template["criteria"],
            template["actions"],
            template["priority"],
            0.0,
            datetime.now(),
            datetime.now(),
            0,
            0.0,
            {},
        )

    def _create_custom_filters(self, patterns: Dict[str, Any]) -> List[EmailFilter]:
        """Creates custom filters based on frequently observed patterns."""
        return []  # Simplified

    def add_custom_filter(
        self,
        name: str,
        description: str,
        criteria: Dict[str, Any],
        actions: Dict[str, Any],
        priority: int,
    ) -> EmailFilter:
        """
        Adds a new user-defined filter to the system.

        Args:
            name: The name of the filter.
            description: A description of the filter.
            criteria: The matching criteria for the filter.
            actions: The actions to take on match.
            priority: The priority of the filter.

        Returns:
            The newly created `EmailFilter` object.
        """
        filter_id = f"custom_{name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        new_filter = EmailFilter(
            filter_id,
            name,
            description,
            criteria,
            actions,
            priority,
            0.0,
            datetime.now(),
            datetime.now(),
            0,
            0.0,
            {},
        )
        self._save_filter(new_filter)
        self.logger.info(f"Custom filter '{name}' added with ID: {filter_id}")
        return new_filter

    def prune_ineffective_filters(self) -> Dict[str, Any]:
        """
        Removes or disables filters that are no longer effective.

        Returns:
            A dictionary summarizing the results of the pruning process.
        """
        return {"pruned_filters": [], "disabled_filters": []}  # Simplified

    def _evaluate_filter_for_pruning(self, filter_obj: EmailFilter) -> str:
        """Evaluates a single filter to decide if it should be kept, pruned, or disabled."""
        return "keep"  # Simplified

    def _apply_filter_to_email(self, filter_obj: EmailFilter, email: Dict[str, Any]) -> bool:
        """Applies a single filter's criteria to an email."""
        criteria = filter_obj.criteria
        if "from_patterns" in criteria and not any(
            re.search(p, email.get("senderEmail", ""), re.IGNORECASE)
            for p in criteria["from_patterns"]
        ):
            return False
        if "subject_keywords" in criteria and not any(
            k.lower() in email.get("subject", "").lower() for k in criteria["subject_keywords"]
        ):
            return False
        return True

    def _save_filter(self, filter_obj: EmailFilter):
        """Saves a filter to the database."""
        query = (
            "INSERT OR REPLACE INTO email_filters VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        )
        params = (
            filter_obj.filter_id,
            filter_obj.name,
            filter_obj.description,
            json.dumps(filter_obj.criteria),
            json.dumps(filter_obj.actions),
            filter_obj.priority,
            filter_obj.effectiveness_score,
            filter_obj.created_date.isoformat(),
            filter_obj.last_used.isoformat(),
            filter_obj.usage_count,
            filter_obj.false_positive_rate,
            json.dumps(filter_obj.performance_metrics),
            True,
        )
        self._db_execute(query, params)

    def get_active_filters_sorted(self) -> List[EmailFilter]:
        """Loads all active filters from the database, sorted by priority."""
        rows = self._db_fetchall(
            "SELECT * FROM email_filters WHERE is_active = 1 ORDER BY priority DESC"
        )
        return [
            EmailFilter(
                row["filter_id"],
                row["name"],
                row["description"],
                json.loads(row["criteria"]),
                json.loads(row["actions"]),
                row["priority"],
                row["effectiveness_score"],
                datetime.fromisoformat(row["created_date"]),
                datetime.fromisoformat(row["last_used"]),
                row["usage_count"],
                row["false_positive_rate"],
                json.loads(row["performance_metrics"]),
            )
            for row in rows
        ]

    def apply_filters_to_email_data(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Applies all active filters to an email and returns a summary of actions.

        Args:
            email_data: A dictionary representing the email data.

        Returns:
            A dictionary summarizing the matched filters and actions taken.
        """
        summary = {"filters_matched": [], "actions_taken": []}
        for filter_obj in self.get_active_filters_sorted():
            if self._apply_filter_to_email(filter_obj, email_data):
                summary["filters_matched"].append(filter_obj.name)
        return summary


def main():
    """Demonstrates the usage of the SmartFilterManager."""
    manager = SmartFilterManager()
    sample_emails = [{"senderEmail": "urgent@company.com", "subject": "Urgent: Action Required"}]
    filters = manager.create_intelligent_filters(sample_emails)
    print(f"Created {len(filters)} filters.")
    if filters:
        print(
            f"Applied filters to sample email: {manager.apply_filters_to_email_data(sample_emails[0])}"
        )


if __name__ == "__main__":
    main()
