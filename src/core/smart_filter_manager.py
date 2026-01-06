"""
Advanced Smart Filter Manager for the Email Intelligence Platform.

This module provides intelligent email filtering capabilities with persistence,
performance monitoring, and integration with the advanced workflow engine.
It follows the same patterns as other core modules in the src/core directory.
"""

import asyncio
import json
import logging
import os
import re
import sqlite3
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set, Union
from pathlib import Path

from .database import DATA_DIR
from .performance_monitor import log_performance
from .enhanced_caching import EnhancedCachingManager
from .enhanced_error_reporting import (
    log_error,
    ErrorSeverity,
    ErrorCategory,
    create_error_context
)

logger = logging.getLogger(__name__)

# Define paths for data storage
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
        created_at: The datetime when the filter was created.
        last_used: The datetime of the last time the filter was used.
        usage_count: The total number of times the filter has been used.
        false_positive_rate: The calculated false positive rate for the filter.
        performance_metrics: A dictionary of detailed performance metrics.
        is_active: Whether the filter is currently active.
    """

    filter_id: str
    name: str
    description: str
    criteria: Dict[str, Any]
    actions: Dict[str, Any]
    priority: int
    effectiveness_score: float
    created_at: datetime
    last_used: datetime
    usage_count: int
    false_positive_rate: float
    performance_metrics: Dict[str, float]
    is_active: bool = True


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


@dataclass
class _EmailContext:
    """
    Internal context helper to avoid redundant processing of email fields
    during filter application loop.
    """
    email: Dict[str, Any]
    sender_domain: str
    subject_lower: str
    content_lower: str
    sender_lower: str


class SmartFilterManager:
    """
    Advanced manager for the lifecycle of smart email filters.

    This class handles the creation, storage, application, and optimization
    of email filters with enhanced features like async operations, caching,
    and error reporting following the patterns used in other core modules.
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
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self.conn = None
        if self.db_path == ":memory:":
            self.conn = sqlite3.connect(":memory:")
            self.conn.row_factory = sqlite3.Row
        self._init_filter_db()
        self.filter_templates = self._load_filter_templates()
        self.pruning_criteria = self._load_pruning_criteria()

        # Enhanced caching system
        self.caching_manager = EnhancedCachingManager()

        # State
        self._dirty_data: set[str] = set()
        self._initialized = False

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
                    error_context = create_error_context(
                        component="SmartFilterManager",
                        operation="_db_execute",
                        additional_context={"query": query[:100], "attempt": attempt}
                    )
                    error_id = log_error(
                        e,
                        severity=ErrorSeverity.ERROR,
                        category=ErrorCategory.INTEGRATION,
                        context=error_context
                    )
                    self.logger.error(
                        f"Database error after {retries} attempts: {e} with query: {query[:100]}. Error ID: {error_id}"
                    )
                    raise
            except sqlite3.Error as e:
                error_context = create_error_context(
                    component="SmartFilterManager",
                    operation="_db_execute",
                    additional_context={"query": query[:100]}
                )
                error_id = log_error(
                    e,
                    severity=ErrorSeverity.ERROR,
                    category=ErrorCategory.INTEGRATION,
                    context=error_context
                )
                self.logger.error(f"Database error: {e} with query: {query[:100]}. Error ID: {error_id}")
                raise
            finally:
                self._close_db_connection(conn)

    def _db_fetchone(self, query: str, params: tuple = ()) -> Optional[sqlite3.Row]:
        """Executes a read query and fetches a single row."""
        conn = self._get_db_connection()
        try:
            return conn.execute(query, params).fetchone()
        except sqlite3.Error as e:
            error_context = create_error_context(
                component="SmartFilterManager",
                operation="_db_fetchone",
                additional_context={"query": query[:100]}
            )
            error_id = log_error(
                e,
                severity=ErrorSeverity.ERROR,
                category=ErrorCategory.INTEGRATION,
                context=error_context
            )
            self.logger.error(f"Database error on fetchone: {e}. Error ID: {error_id}")
            return None
        finally:
            self._close_db_connection(conn)

    def _db_fetchall(self, query: str, params: tuple = ()) -> List[sqlite3.Row]:
        """Executes a read query and fetches all rows."""
        conn = self._get_db_connection()
        try:
            return conn.execute(query, params).fetchall()
        except sqlite3.Error as e:
            error_context = create_error_context(
                component="SmartFilterManager",
                operation="_db_fetchall",
                additional_context={"query": query[:100]}
            )
            error_id = log_error(
                e,
                severity=ErrorSeverity.ERROR,
                category=ErrorCategory.INTEGRATION,
                context=error_context
            )
            self.logger.error(f"Database error on fetchall: {e}. Error ID: {error_id}")
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
                effectiveness_score REAL DEFAULT 0.0, created_at TEXT, last_used TEXT,
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

    async def _ensure_initialized(self):
        """Ensure all components are properly initialized."""
        if self._initialized:
            return

        # Initialize caching manager
        await self.caching_manager._ensure_initialized()

        self._initialized = True
        logger.info("SmartFilterManager fully initialized")

    async def close(self):
        """Closes the persistent database connection."""
        if self.conn:
            self.conn.close()

    def _load_filter_templates(self) -> Dict[str, Dict[str, Any]]:
        """Loads a set of predefined filter templates."""
        return {
            "high_priority_work": {
                "criteria": {"subject_keywords": ["urgent", "important", "asap"]},
                "actions": {"mark_important": True, "add_label": "Priority"},
                "priority": 9,
                "description": "High priority work",
            },
            "financial_documents": {
                "criteria": {"subject_keywords": ["invoice", "statement", "payment", "bill"]},
                "actions": {"add_label": "Finance", "move_to_folder": "Finance"},
                "priority": 7,
                "description": "Financial documents",
            },
            "meeting_invitations": {
                "criteria": {"subject_keywords": ["meeting", "calendar", "invite"]},
                "actions": {"add_label": "Meetings", "add_to_calendar": True},
                "priority": 6,
                "description": "Meeting invitations",
            },
        }

    def _load_pruning_criteria(self) -> Dict[str, Any]:
        """Loads the criteria used for pruning ineffective filters."""
        return {"effectiveness_threshold": 0.3, "usage_threshold": 10, "age_threshold_days": 90}

    @log_performance(operation="create_intelligent_filters")
    async def create_intelligent_filters(self, email_samples: List[Dict[str, Any]]) -> List[EmailFilter]:
        """
        Analyzes email samples to intelligently generate and store new filters.

        Args:
            email_samples: A list of email data dictionaries to analyze.

        Returns:
            A list of the newly created `EmailFilter` objects.
        """
        await self._ensure_initialized()

        created_filters = []
        patterns = self._analyze_email_patterns(email_samples)
        template_filters = await self._create_filters_from_templates(patterns)
        created_filters.extend(template_filters)
        custom_filters = await self._create_custom_filters(patterns)
        created_filters.extend(custom_filters)
        self.logger.info(f"Created {len(created_filters)} intelligent filters")
        return created_filters

    async def _create_filters_from_templates(self, patterns: Dict[str, Any]) -> List[EmailFilter]:
        """Creates filters from templates that match the analyzed patterns."""
        filters = []
        for name, template in self.filter_templates.items():
            if await self._should_create_filter_async(template, patterns):
                filter_obj = self._create_filter_from_template(name, template)
                await self._save_filter_async(filter_obj)
                filters.append(filter_obj)
        return filters

    def _extract_patterns_from_single_email(self, email: Dict[str, Any]) -> Dict[str, Any]:
        """Extracts key patterns from a single email."""
        patterns = {}
        if domain := self._extract_domain(email.get("sender_email", email.get("sender", ""))):
            patterns["sender_domain"] = domain
        if keywords := self._extract_keywords(email.get("subject", "")):
            patterns["subject_keywords"] = keywords
        if keywords := self._extract_keywords(email.get("content", email.get("body", ""))):
            patterns["content_keywords"] = keywords
        return patterns

    def _analyze_email_patterns(self, email_samples: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregates patterns found across a list of email samples."""
        aggregated = {"sender_domains": Counter(), "subject_keywords": Counter(), "content_keywords": Counter()}
        for email in email_samples:
            patterns = self._extract_patterns_from_single_email(email)
            if "sender_domain" in patterns:
                aggregated["sender_domains"][patterns["sender_domain"]] += 1
            if "subject_keywords" in patterns:
                aggregated["subject_keywords"].update(patterns["subject_keywords"])
            if "content_keywords" in patterns:
                aggregated["content_keywords"].update(patterns["content_keywords"])
        return aggregated

    def _extract_domain(self, email_address: str) -> str:
        """Extracts the domain from an email address."""
        return email_address.split("@")[1].lower() if "@" in email_address else ""

    def _extract_keywords(self, text: str) -> List[str]:
        """Extracts meaningful keywords from a string of text."""
        if not text:
            return []
        return [word for word in re.findall(r"\b[a-zA-Z]{3,}\b", text.lower()) if len(word) > 3]

    def _is_automated_email(self, email: Dict[str, Any]) -> bool:
        """Determines if an email is likely automated."""
        sender = email.get("sender_email", email.get("sender", "")).lower()
        return any(ind in sender for ind in ["noreply", "automated", "notification", "admin"])

    async def _should_create_filter_async(self, template: Dict[str, Any], patterns: Dict[str, Any]) -> bool:
        """Determines if a filter should be created based on a template and discovered patterns."""
        # Check if patterns match the template criteria
        template_keywords = template["criteria"].get("subject_keywords", [])
        for keyword in template_keywords:
            if any(keyword.lower() in pattern_kw.lower() for pattern_kw in patterns.get("subject_keywords", [])):
                return True
        return False

    def _create_filter_from_template(self, name: str, template: Dict[str, Any]) -> EmailFilter:
        """Creates an EmailFilter object from a template."""
        filter_id = f"template_{name}_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')[:17]}"
        return EmailFilter(
            filter_id=filter_id,
            name=name,
            description=template["description"],
            criteria=template["criteria"],
            actions=template["actions"],
            priority=template["priority"],
            effectiveness_score=0.0,
            created_at=datetime.now(timezone.utc),
            last_used=datetime.now(timezone.utc),
            usage_count=0,
            false_positive_rate=0.0,
            performance_metrics={},
        )

    async def _create_custom_filters(self, patterns: Dict[str, Any]) -> List[EmailFilter]:
        """Creates custom filters based on frequently observed patterns."""
        filters = []

        # Create filter based on frequent sender domains
        for domain, count in patterns["sender_domains"].most_common(3):
            if count >= 3:  # Only create if domain appears in 3+ emails
                filter_obj = self._create_domain_filter(domain)
                await self._save_filter_async(filter_obj)
                filters.append(filter_obj)

        # Create filter based on frequent subject keywords
        for keyword, count in patterns["subject_keywords"].most_common(5):
            if count >= 2:  # Only create if keyword appears in 2+ emails
                filter_obj = self._create_keyword_filter(keyword)
                await self._save_filter_async(filter_obj)
                filters.append(filter_obj)

        return filters

    def _create_domain_filter(self, domain: str) -> EmailFilter:
        """Creates a filter for a specific domain."""
        name = f"From {domain}"
        filter_id = f"domain_{domain.replace('.', '_')}_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')[:17]}"
        return EmailFilter(
            filter_id=filter_id,
            name=name,
            description=f"Filter for emails from {domain}",
            criteria={"sender_domain": domain},
            actions={"add_label": domain.replace(".", "_")},
            priority=5,
            effectiveness_score=0.0,
            created_at=datetime.now(timezone.utc),
            last_used=datetime.now(timezone.utc),
            usage_count=0,
            false_positive_rate=0.0,
            performance_metrics={},
        )

    def _create_keyword_filter(self, keyword: str) -> EmailFilter:
        """Creates a filter for a specific keyword."""
        name = f"Contains {keyword}"
        filter_id = f"keyword_{keyword}_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')[:17]}"
        return EmailFilter(
            filter_id=filter_id,
            name=name,
            description=f"Filter for emails containing {keyword}",
            criteria={"subject_keywords": [keyword], "content_keywords": [keyword]},
            actions={"add_label": keyword},
            priority=4,
            effectiveness_score=0.0,
            created_at=datetime.now(timezone.utc),
            last_used=datetime.now(timezone.utc),
            usage_count=0,
            false_positive_rate=0.0,
            performance_metrics={},
        )

    @log_performance(operation="add_custom_filter")
    async def add_custom_filter(
        self,
        name: str,
        description: str,
        criteria: Dict[str, Any],
        actions: Dict[str, Any],
        priority: int = 5,
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
        await self._ensure_initialized()

        filter_id = f"custom_{name.replace(' ', '_')}_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')[:17]}"
        new_filter = EmailFilter(
            filter_id=filter_id,
            name=name,
            description=description,
            criteria=criteria,
            actions=actions,
            priority=priority,
            effectiveness_score=0.0,
            created_at=datetime.now(timezone.utc),
            last_used=datetime.now(timezone.utc),
            usage_count=0,
            false_positive_rate=0.0,
            performance_metrics={},
        )
        await self._save_filter_async(new_filter)
        self.logger.info(f"Custom filter '{name}' added with ID: {filter_id}")
        return new_filter

    @log_performance(operation="prune_ineffective_filters")
    async def prune_ineffective_filters(self) -> Dict[str, Any]:
        """
        Removes or disables filters that are no longer effective.

        Returns:
            A dictionary summarizing the results of the pruning process.
        """
        await self._ensure_initialized()

        pruned_filters = []
        disabled_filters = []

        active_filters = await self.get_active_filters_sorted()
        for filter_obj in active_filters:
            decision = await self._evaluate_filter_for_pruning(filter_obj)
            if decision == "prune":
                await self.delete_filter(filter_obj.filter_id)
                pruned_filters.append(filter_obj.filter_id)
            elif decision == "disable":
                await self.update_filter_status(filter_obj.filter_id, False)
                disabled_filters.append(filter_obj.filter_id)

        return {"pruned_filters": pruned_filters, "disabled_filters": disabled_filters}

    async def _evaluate_filter_for_pruning(self, filter_obj: EmailFilter) -> str:
        """Evaluates a single filter to decide if it should be kept, pruned, or disabled."""
        # Check effectiveness score
        if filter_obj.effectiveness_score < self.pruning_criteria["effectiveness_threshold"]:
            return "disable"

        # Check usage count
        if filter_obj.usage_count < self.pruning_criteria["usage_threshold"]:
            # Check age - if filter is old and not used much, consider for pruning
            age_days = (datetime.now(timezone.utc) - filter_obj.created_at).days
            if age_days > self.pruning_criteria["age_threshold_days"]:
                return "prune"

        return "keep"

    async def _apply_filter_to_email(self, filter_obj: EmailFilter, context: Union[Dict[str, Any], '_EmailContext']) -> bool:
        """
        Applies a single filter's criteria to an email.

        Args:
            filter_obj: The filter to apply.
            context: Either the raw email dict (for backward compatibility) or an _EmailContext object.
        """
        criteria = filter_obj.criteria

        # Handle backward compatibility or raw usage
        if not isinstance(context, _EmailContext):
            sender_email = context.get("sender_email", context.get("sender", ""))
            ctx = _EmailContext(
                email=context,
                sender_domain=self._extract_domain(sender_email),
                subject_lower=context.get("subject", "").lower(),
                content_lower=context.get("content", context.get("body", "")).lower(),
                sender_lower=sender_email.lower()
            )
        else:
            ctx = context

        # Check sender domain criteria
        if "sender_domain" in criteria:
            if ctx.sender_domain != criteria["sender_domain"]:
                return False

        # Check subject keywords
        if "subject_keywords" in criteria:
            # Optimization: check if any keyword matches
            if not any(keyword.lower() in ctx.subject_lower for keyword in criteria["subject_keywords"]):
                return False

        # Check content keywords
        if "content_keywords" in criteria:
            if not any(keyword.lower() in ctx.content_lower for keyword in criteria["content_keywords"]):
                return False

        # Check from patterns
        if "from_patterns" in criteria:
            if not any(re.search(p, ctx.sender_lower, re.IGNORECASE) for p in criteria["from_patterns"]):
                return False

        return True

    async def _save_filter_async(self, filter_obj: EmailFilter):
        """Saves a filter to the database asynchronously."""
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
            filter_obj.created_at.isoformat(),
            filter_obj.last_used.isoformat(),
            filter_obj.usage_count,
            filter_obj.false_positive_rate,
            json.dumps(filter_obj.performance_metrics),
            filter_obj.is_active,
        )
        self._db_execute(query, params)

        # Update cache
        cache_key = f"filter_{filter_obj.filter_id}"
        await self.caching_manager.set(cache_key, filter_obj)

    @log_performance(operation="get_active_filters_sorted")
    async def get_active_filters_sorted(self) -> List[EmailFilter]:
        """Loads all active filters from the database, sorted by priority."""
        await self._ensure_initialized()

        # Check cache first
        cache_key = "active_filters_sorted"
        cached_result = await self.caching_manager.get(cache_key)
        if cached_result is not None:
            return cached_result

        rows = self._db_fetchall(
            "SELECT * FROM email_filters WHERE is_active = 1 ORDER BY priority DESC"
        )
        filters = [
            EmailFilter(
                filter_id=row["filter_id"],
                name=row["name"],
                description=row["description"],
                criteria=json.loads(row["criteria"]),
                actions=json.loads(row["actions"]),
                priority=row["priority"],
                effectiveness_score=row["effectiveness_score"],
                created_at=datetime.fromisoformat(row["created_at"]),
                last_used=datetime.fromisoformat(row["last_used"]),
                usage_count=row["usage_count"],
                false_positive_rate=row["false_positive_rate"],
                performance_metrics=json.loads(row["performance_metrics"]),
                is_active=bool(row["is_active"]),
            )
            for row in rows
        ]

        # Cache the result
        await self.caching_manager.set(cache_key, filters)

        return filters

    @log_performance(operation="apply_filters_to_email")
    async def apply_filters_to_email(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Applies all active filters to an email and returns a summary of actions.

        Args:
            email_data: A dictionary representing the email data.

        Returns:
            A dictionary summarizing the matched filters and actions taken.
        """
        await self._ensure_initialized()

        summary = {"filters_matched": [], "actions_taken": [], "categories": []}

        # Pre-calculate email properties once to avoid repeated processing in the loop
        # This reduces complexity from O(N_filters * Length) to O(1 * Length + N_filters)
        sender_email = email_data.get("sender_email", email_data.get("sender", ""))
        email_context = _EmailContext(
            email=email_data,
            sender_domain=self._extract_domain(sender_email),
            subject_lower=email_data.get("subject", "").lower(),
            content_lower=email_data.get("content", email_data.get("body", "")).lower(),
            sender_lower=sender_email.lower()
        )

        # Get active filters sorted by priority
        active_filters = await self.get_active_filters_sorted()

        for filter_obj in active_filters:
            try:
                if await self._apply_filter_to_email(filter_obj, email_context):
                    # Record that this filter matched
                    summary["filters_matched"].append({
                        "filter_id": filter_obj.filter_id,
                        "name": filter_obj.name,
                        "priority": filter_obj.priority
                    })

                    # Execute actions
                    for action_key, action_value in filter_obj.actions.items():
                        if action_key == "add_label":
                            if isinstance(action_value, str):
                                summary["categories"].append(action_value)
                        elif action_key == "mark_important":
                            if action_value:
                                summary["actions_taken"].append("marked_important")
                        elif action_key == "move_to_folder":
                            if isinstance(action_value, str):
                                summary["actions_taken"].append(f"moved_to_{action_value}")

                    # Update filter usage stats
                    await self._update_filter_usage(filter_obj.filter_id)

            except Exception as e:
                error_context = create_error_context(
                    component="SmartFilterManager",
                    operation="apply_filters_to_email",
                    additional_context={"filter_id": filter_obj.filter_id, "email_id": email_data.get("id")}
                )
                error_id = log_error(
                    e,
                    severity=ErrorSeverity.WARNING,
                    category=ErrorCategory.INTEGRATION,
                    context=error_context
                )
                self.logger.warning(f"Error applying filter {filter_obj.filter_id} to email {email_data.get('id')}: {e}. Error ID: {error_id}")

        # Update the last_used timestamp for the email
        email_data["last_filtered_at"] = datetime.now(timezone.utc).isoformat()

        return summary

    async def _update_filter_usage(self, filter_id: str):
        """Updates the usage statistics for a filter."""
        # Update usage count and last used time
        update_query = """
            UPDATE email_filters
            SET usage_count = usage_count + 1, last_used = ?
            WHERE filter_id = ?
        """
        current_time = datetime.now(timezone.utc).isoformat()
        self._db_execute(update_query, (current_time, filter_id))

        # OPTIMIZATION: Removed redundant cache invalidation for "active_filters_sorted".
        # Why: Invalidating this cache on every filter match causes a "thundering herd"
        # effect where the entire filter list is re-fetched from DB for every matched email.
        # Impact: Turns O(N) DB reads into O(1) cache hits during batch processing.
        # Trade-off: Usage counts in the cached list will be slightly stale until TTL expires,
        # which is acceptable as they are not used for filter logic (priority/criteria).
        # await self.caching_manager.delete("active_filters_sorted")

    @log_performance(operation="get_filter_by_id")
    async def get_filter_by_id(self, filter_id: str) -> Optional[EmailFilter]:
        """Retrieves a specific filter by its ID."""
        await self._ensure_initialized()

        # Check cache first
        cache_key = f"filter_{filter_id}"
        cached_result = await self.caching_manager.get(cache_key)
        if cached_result is not None:
            return cached_result

        row = self._db_fetchone(
            "SELECT * FROM email_filters WHERE filter_id = ?", (filter_id,)
        )

        if not row:
            return None

        filter_obj = EmailFilter(
            filter_id=row["filter_id"],
            name=row["name"],
            description=row["description"],
            criteria=json.loads(row["criteria"]),
            actions=json.loads(row["actions"]),
            priority=row["priority"],
            effectiveness_score=row["effectiveness_score"],
            created_at=datetime.fromisoformat(row["created_at"]),
            last_used=datetime.fromisoformat(row["last_used"]),
            usage_count=row["usage_count"],
            false_positive_rate=row["false_positive_rate"],
            performance_metrics=json.loads(row["performance_metrics"]),
            is_active=bool(row["is_active"]),
        )

        # Cache the result
        await self.caching_manager.set(cache_key, filter_obj)

        return filter_obj

    @log_performance(operation="update_filter")
    async def update_filter(self, filter_id: str, **kwargs) -> bool:
        """Updates a filter's properties."""
        await self._ensure_initialized()

        # Get the existing filter
        existing_filter = await self.get_filter_by_id(filter_id)
        if not existing_filter:
            return False

        # Update the filter object with new values
        for key, value in kwargs.items():
            if hasattr(existing_filter, key):
                setattr(existing_filter, key, value)

        # Save the updated filter
        await self._save_filter_async(existing_filter)

        # Invalidate cache
        await self.caching_manager.delete(f"filter_{filter_id}")
        await self.caching_manager.delete("active_filters_sorted")

        return True

    @log_performance(operation="update_filter_status")
    async def update_filter_status(self, filter_id: str, is_active: bool) -> bool:
        """Updates a filter's active status."""
        await self._ensure_initialized()

        update_query = "UPDATE email_filters SET is_active = ? WHERE filter_id = ?"
        self._db_execute(update_query, (is_active, filter_id))

        # Invalidate cache
        await self.caching_manager.delete(f"filter_{filter_id}")
        await self.caching_manager.delete("active_filters_sorted")

        return True

    @log_performance(operation="delete_filter")
    async def delete_filter(self, filter_id: str) -> bool:
        """Deletes a filter from the system."""
        await self._ensure_initialized()

        delete_query = "DELETE FROM email_filters WHERE filter_id = ?"
        self._db_execute(delete_query, (filter_id,))

        # Also delete associated performance data
        delete_perf_query = "DELETE FROM filter_performance WHERE filter_id = ?"
        self._db_execute(delete_perf_query, (filter_id,))

        # Invalidate cache
        await self.caching_manager.delete(f"filter_{filter_id}")
        await self.caching_manager.delete("active_filters_sorted")

        return True

    @log_performance(operation="get_filters_by_category")
    async def get_filters_by_category(self, category: str) -> List[EmailFilter]:
        """Retrieves filters that are associated with a specific category."""
        await self._ensure_initialized()

        # This looks for filters that have actions related to the category
        rows = self._db_fetchall(
            "SELECT * FROM email_filters WHERE actions LIKE ? AND is_active = 1",
            (f'%{category}%',)
        )

        filters = [
            EmailFilter(
                filter_id=row["filter_id"],
                name=row["name"],
                description=row["description"],
                criteria=json.loads(row["criteria"]),
                actions=json.loads(row["actions"]),
                priority=row["priority"],
                effectiveness_score=row["effectiveness_score"],
                created_at=datetime.fromisoformat(row["created_at"]),
                last_used=datetime.fromisoformat(row["last_used"]),
                usage_count=row["usage_count"],
                false_positive_rate=row["false_positive_rate"],
                performance_metrics=json.loads(row["performance_metrics"]),
                is_active=bool(row["is_active"]),
            )
            for row in rows
        ]

        return filters

    async def cleanup(self):
        """Performs cleanup operations."""
        await self.close()
        await self.caching_manager.close()
