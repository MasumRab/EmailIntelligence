"""
Smart Email Filter Management System
Implements intelligent filter creation, pruning, and Google Apps Script integration
"""

import json
import re
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import logging
from collections import defaultdict, Counter
import sqlite3

@dataclass
class EmailFilter:
    """Structured email filter definition"""
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
    """Filter performance analytics"""
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
    """Intelligent email filter management with performance optimization"""
    
    def __init__(self, db_path: str = "smart_filters.db"):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self.conn = None  # For persistent in-memory connection

        if self.db_path == ":memory:":
            self.conn = sqlite3.connect(":memory:")
            self.conn.row_factory = sqlite3.Row

        self._init_filter_db()
        
        # Filter categories and templates
        self.filter_templates = self._load_filter_templates()
        self.pruning_criteria = self._load_pruning_criteria()
        
    def _get_db_connection(self) -> sqlite3.Connection:
        """Get a database connection."""
        if self.conn: # Use persistent in-memory connection if it exists
            return self.conn
        # For file-based DBs, create a new connection each time (or manage a pool)
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _close_db_connection(self, conn: sqlite3.Connection):
        """Close connection if it's not the persistent in-memory one."""
        if conn is not self.conn:
            conn.close()

    def _db_execute(self, query: str, params: tuple = ()):
        """Execute a query (INSERT, UPDATE, DELETE)."""
        conn = self._get_db_connection()
        try:
            conn.execute(query, params)
            conn.commit()
        except sqlite3.Error as e:
            self.logger.error(f"Database error: {e} with query: {query[:100]}")
            # Optionally re-raise or handle
        finally:
            self._close_db_connection(conn)

    def _db_fetchone(self, query: str, params: tuple = ()) -> Optional[sqlite3.Row]:
        """Execute a query and fetch one row."""
        conn = self._get_db_connection()
        try:
            cursor = conn.execute(query, params)
            return cursor.fetchone()
        except sqlite3.Error as e:
            self.logger.error(f"Database error: {e} with query: {query[:100]}")
            return None
        finally:
            self._close_db_connection(conn)

    def _db_fetchall(self, query: str, params: tuple = ()) -> List[sqlite3.Row]:
        """Execute a query and fetch all rows."""
        conn = self._get_db_connection()
        try:
            cursor = conn.execute(query, params)
            return cursor.fetchall()
        except sqlite3.Error as e:
            self.logger.error(f"Database error: {e} with query: {query[:100]}")
            return []
        finally:
            self._close_db_connection(conn)

    def _init_filter_db(self):
        """Initialize filter database"""
        queries = [
            """
            CREATE TABLE IF NOT EXISTS email_filters (
                filter_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                criteria TEXT NOT NULL,
                actions TEXT NOT NULL,
                priority INTEGER DEFAULT 5,
                effectiveness_score REAL DEFAULT 0.0,
                created_date TEXT,
                last_used TEXT,
                usage_count INTEGER DEFAULT 0,
                false_positive_rate REAL DEFAULT 0.0,
                performance_metrics TEXT,
                is_active BOOLEAN DEFAULT 1
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS filter_performance (
                performance_id TEXT PRIMARY KEY,
                filter_id TEXT,
                measurement_date TEXT,
                accuracy REAL,
                precision_score REAL,
                recall_score REAL,
                f1_score REAL,
                processing_time_ms REAL,
                emails_processed INTEGER,
                true_positives INTEGER,
                false_positives INTEGER,
                false_negatives INTEGER,
                FOREIGN KEY (filter_id) REFERENCES email_filters (filter_id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS google_scripts (
                script_id TEXT PRIMARY KEY,
                script_name TEXT NOT NULL,
                script_type TEXT,
                script_content TEXT,
                version TEXT,
                created_date TEXT,
                last_modified TEXT,
                is_deployed BOOLEAN DEFAULT 0,
                performance_score REAL DEFAULT 0.0,
                error_count INTEGER DEFAULT 0
            )
            """
        ]
        conn = self._get_db_connection()
        try:
            for query in queries:
                conn.execute(query) # Uses the connection from _get_db_connection
            conn.commit() # Commit on the same connection
        except sqlite3.Error as e:
            self.logger.error(f"Database initialization error: {e}")
        finally:
            # Do not close if it's the persistent self.conn
            self._close_db_connection(conn)


    def close(self):
        """Close the persistent database connection if it exists."""
        if self.conn:
            self.conn.close()
            self.conn = None

    def _load_filter_templates(self) -> Dict[str, Dict[str, Any]]:
        """Load intelligent filter templates"""
        return {
            "high_priority_work": {
                "criteria": {
                    "from_patterns": [
                        r".*@(company\.com|organization\.org)",
                        r".*(manager|director|ceo|president).*@.*"
                    ],
                    "subject_keywords": ["urgent", "important", "asap", "deadline", "meeting"], # Already lowercase
                    "content_keywords": ["project", "budget", "proposal", "contract"], # Already lowercase
                    "time_sensitivity": "high",
                    "exclude_patterns": ["newsletter", "unsubscribe", "automated"] # Already lowercase
                },
                "actions": {
                    "add_label": "Work/High Priority",
                    "mark_important": True,
                    "forward_to": None,
                    "auto_reply": False
                },
                "priority": 9,
                "description": "High priority work emails requiring immediate attention"
            },
            
            "financial_documents": {
                "criteria": {
                    "from_patterns": [
                        r".*@(bank|credit|finance|accounting).*",
                        r".*(invoice|billing|payment).*@.*"
                    ],
                    "subject_keywords": ["invoice", "statement", "payment", "receipt", "bill"], # Already lowercase
                    "attachment_types": ["pdf", "xlsx", "csv"], # Case-insensitive usually, but good to be consistent
                    "content_keywords": ["amount", "due", "balance", "transaction"] # Already lowercase
                },
                "actions": {
                    "add_label": "Finance/Documents",
                    "mark_important": False,
                    "archive": False,
                    "extract_data": True
                },
                "priority": 7,
                "description": "Financial documents and billing information"
            },
            
            "automated_notifications": {
                "criteria": {
                    "from_patterns": [
                        r".*noreply.*",
                        r".*no-reply.*",
                        r".*automated.*",
                        r".*notification.*@.*"
                    ],
                    "subject_keywords": ["notification", "alert", "update", "reminder"], # Already lowercase
                    "content_keywords": ["automated", "do not reply", "unsubscribe"], # Already lowercase
                    "exclude_keywords": ["urgent", "important", "action required"] # Already lowercase
                },
                "actions": {
                    "add_label": "Automated/Notifications",
                    "mark_important": False,
                    "archive": True,
                    "mark_read": True
                },
                "priority": 3,
                "description": "Automated notifications and system messages"
            },
            
            "promotional_emails": {
                "criteria": {
                    "subject_keywords": ["sale", "discount", "offer", "deal", "promotion", "%", "save"], # Already lowercase
                    "content_keywords": ["unsubscribe", "promotional", "marketing", "advertisement"], # Already lowercase
                    "from_patterns": [r".*@(marketing|promo|deals|offers).*"],
                    "list_unsubscribe_header": True
                },
                "actions": {
                    "add_label": "Promotions",
                    "mark_important": False,
                    "archive": True,
                    "bulk_process": True
                },
                "priority": 2,
                "description": "Marketing and promotional emails"
            },
            
            "personal_communications": {
                "criteria": {
                    "from_patterns": [r".*@(gmail\.com|yahoo\.com|hotmail\.com|outlook\.com)"],
                    "exclude_patterns": [r".*noreply.*", r".*automated.*"], # These are regex, not keywords for keyword list
                    "subject_exclude": ["newsletter", "promotion", "unsubscribe"], # Already lowercase
                    "content_personal_indicators": ["how are you", "hope you", "let me know", "talk soon"] # Already lowercase
                },
                "actions": {
                    "add_label": "Personal",
                    "mark_important": False,
                    "notify": True
                },
                "priority": 6,
                "description": "Personal communications from individuals"
            },
            
            "security_alerts": {
                "criteria": {
                    "subject_keywords": ["security", "login", "password", "suspicious", "breach", "alert"], # Already lowercase
                    "from_patterns": [r".*security.*@.*", r".*@.*(google|microsoft|apple)\.com"],
                    "content_keywords": ["unauthorized", "verify", "suspicious activity", "security alert"], # Already lowercase
                    "urgency_indicators": ["immediate", "verify now", "action required"] # Already lowercase
                },
                "actions": {
                    "add_label": "Security/Alerts",
                    "mark_important": True,
                    "notify_immediately": True,
                    "never_archive": True
                },
                "priority": 10,
                "description": "Security alerts and authentication notifications"
            }
        }
    
    def _load_pruning_criteria(self) -> Dict[str, Any]:
        """Load filter pruning criteria"""
        return {
            "effectiveness_threshold": 0.3,  # Minimum effectiveness score
            "false_positive_threshold": 0.15,  # Maximum false positive rate
            "usage_threshold": 10,  # Minimum usage count
            "age_threshold_days": 90,  # Maximum age without use
            "accuracy_threshold": 0.7,  # Minimum accuracy
            "f1_threshold": 0.6,  # Minimum F1 score
            "redundancy_threshold": 0.8  # Similarity threshold for redundant filters
        }
    
    def create_intelligent_filters(self, email_samples: List[Dict[str, Any]]) -> List[EmailFilter]:
        """Create intelligent filters based on email patterns"""
        created_filters = []
        
        # Analyze email patterns
        patterns = self._analyze_email_patterns(email_samples)
        
        # Create filters from templates
        template_filters = self._create_filters_from_templates(patterns)
        created_filters.extend(template_filters)
        
        # Create custom filters based on discovered patterns
        custom_filters = self._create_custom_filters(patterns) # This method already saves the filters
        created_filters.extend(custom_filters)
        
        self.logger.info(f"Created {len(created_filters)} intelligent filters")
        return created_filters

    def _create_filters_from_templates(self, patterns: Dict[str, Any]) -> List[EmailFilter]:
        """Creates filters based on predefined templates and analyzed patterns."""
        template_filters = []
        for template_name, template_data in self.filter_templates.items():
            if self._should_create_filter(template_data, patterns):
                filter_obj = self._create_filter_from_template(template_name, template_data)
                self._save_filter(filter_obj) # Save the filter
                template_filters.append(filter_obj)
        return template_filters

    def _extract_patterns_from_single_email(self, email: Dict[str, Any]) -> Dict[str, Any]:
        """Extracts various pattern elements from a single email."""
        email_patterns = {}

        sender_domain = self._extract_domain(email.get('senderEmail', ''))
        if sender_domain:
            email_patterns["sender_domain"] = sender_domain # Store single domain

        subject_words = self._extract_keywords(email.get('subject', ''))
        if subject_words:
            email_patterns["subject_keywords"] = subject_words # Store list of words

        content_words = self._extract_keywords(email.get('content', ''))
        if content_words:
            email_patterns["content_keywords"] = content_words # Store list of words

        category = email.get('category') or email.get('ai_analysis', {}).get('topic', 'unknown')
        email_patterns["category"] = category # Store single category

        if email.get('isImportant') or email.get('isStarred'):
            # Combine subject and content words for importance, ensure no duplicates if that's desired
            # For now, simple concatenation is fine as Counter will handle frequency.
            email_patterns["importance_keywords"] = list(set(subject_words + content_words))


        # For automation indicators, we want to associate them with the email's characteristics
        if self._is_automated_email(email):
            # Collect words and domain that indicated automation for this email
            automation_flags = set(subject_words)
            if sender_domain:
                automation_flags.add(sender_domain)
            email_patterns["automation_flags"] = list(automation_flags)

        return email_patterns

    def _analyze_email_patterns(self, email_samples: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze email samples to discover patterns by aggregating findings from each email."""
        # Initialize aggregated patterns structure
        aggregated_patterns = {
            "sender_domains": Counter(),
            "subject_keywords": Counter(),
            "content_keywords": Counter(),
            "time_patterns": defaultdict(list), # time_patterns not currently populated by _extract_patterns_from_single_email
            "category_distributions": Counter(),
            "importance_indicators": Counter(), # Changed to Counter for frequency
            "automation_indicators": Counter()  # Changed to Counter for frequency
        }

        for email in email_samples:
            individual_email_patterns = self._extract_patterns_from_single_email(email)

            if "sender_domain" in individual_email_patterns:
                aggregated_patterns["sender_domains"][individual_email_patterns["sender_domain"]] += 1
            
            if "subject_keywords" in individual_email_patterns:
                aggregated_patterns["subject_keywords"].update(individual_email_patterns["subject_keywords"])
            
            if "content_keywords" in individual_email_patterns:
                aggregated_patterns["content_keywords"].update(individual_email_patterns["content_keywords"])
            
            if "category" in individual_email_patterns:
                aggregated_patterns["category_distributions"][individual_email_patterns["category"]] += 1
            
            if "importance_keywords" in individual_email_patterns:
                aggregated_patterns["importance_indicators"].update(individual_email_patterns["importance_keywords"])
            
            if "automation_flags" in individual_email_patterns:
                aggregated_patterns["automation_indicators"].update(individual_email_patterns["automation_flags"])

        return aggregated_patterns
    
    def _extract_domain(self, email_address: str) -> str:
        """Extract domain from email address"""
        if '@' in email_address:
            return email_address.split('@')[1].lower()
        return ""
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract meaningful keywords from text"""
        if not text:
            return []
        
        # Clean and tokenize
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        
        # Filter stopwords
        stopwords = {
            'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
            'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before',
            'after', 'above', 'below', 'between', 'among', 'this', 'that', 'these',
            'those', 'you', 'your', 'his', 'her', 'its', 'our', 'their'
        }
        
        return [word for word in words if word not in stopwords and len(word) > 2]
    
    def _is_automated_email(self, email: Dict[str, Any]) -> bool:
        """Detect if email is automated"""
        automated_indicators = [
            'noreply', 'no-reply', 'automated', 'donotreply', 'notification',
            'system', 'admin', 'support', 'bot', 'mailer'
        ]
        
        sender = email.get('senderEmail', '').lower()
        subject = email.get('subject', '').lower()
        
        return any(indicator in sender or indicator in subject for indicator in automated_indicators)
    
    def _should_create_filter(self, template: Dict[str, Any], patterns: Dict[str, Any]) -> bool:
        """Determine if a filter should be created based on patterns"""
        criteria = template["criteria"]
        
        # Check if we have enough matching patterns
        relevance_score = 0
        
        # Check sender patterns
        if "from_patterns" in criteria:
            for pattern in criteria["from_patterns"]:
                matching_domains = [domain for domain in patterns["sender_domains"] 
                                 if re.match(pattern, domain)]
                if matching_domains:
                    relevance_score += 1
        
        # Check keyword presence
        if "subject_keywords" in criteria:
            keyword_matches = sum(patterns["subject_keywords"][keyword] 
                                for keyword in criteria["subject_keywords"] 
                                if keyword in patterns["subject_keywords"])
            if keyword_matches > 5:  # Threshold for keyword relevance
                relevance_score += 1
        
        return relevance_score >= 1  # Minimum relevance threshold
    
    def _create_filter_from_template(self, template_name: str, template: Dict[str, Any]) -> EmailFilter:
        """Create filter object from template"""
        filter_id = f"template_{template_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        return EmailFilter(
            filter_id=filter_id,
            name=template_name.replace('_', ' ').title(),
            description=template["description"],
            criteria=template["criteria"],
            actions=template["actions"],
            priority=template["priority"],
            effectiveness_score=0.0,
            created_date=datetime.now(),
            last_used=datetime.now(),
            usage_count=0,
            false_positive_rate=0.0,
            performance_metrics={}
        )
    
    def _create_custom_filters(self, patterns: Dict[str, Any]) -> List[EmailFilter]:
        """Create custom filters based on discovered patterns"""
        custom_filters = []
        
        # Create filters for frequent sender domains
        for domain, count in patterns["sender_domains"].most_common(10):
            if count >= 5 and domain not in ['gmail.com', 'yahoo.com', 'hotmail.com']:
                filter_obj = self._create_domain_filter(domain, count)
                custom_filters.append(filter_obj)
                self._save_filter(filter_obj)
        
        # Create filters for frequent keyword combinations
        keyword_combinations = self._find_keyword_combinations(patterns["subject_keywords"])
        for combo, score in keyword_combinations:
            if score >= 3:
                filter_obj = self._create_keyword_filter(combo, score)
                custom_filters.append(filter_obj)
                self._save_filter(filter_obj)
        
        return custom_filters
    
    def _create_domain_filter(self, domain: str, frequency: int) -> EmailFilter:
        """Create filter for specific domain"""
        filter_id = f"domain_{domain.replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        return EmailFilter(
            filter_id=filter_id,
            name=f"Domain: {domain}",
            description=f"Auto-generated filter for {domain} (frequency: {frequency})",
            criteria={
                "from_patterns": [f".*@{re.escape(domain)}"],
                "min_frequency": frequency
            },
            actions={
                "add_label": f"Domain/{domain}",
                "mark_important": False
            },
            priority=4,
            effectiveness_score=min(1.0, frequency / 20),
            created_date=datetime.now(),
            last_used=datetime.now(),
            usage_count=0,
            false_positive_rate=0.0,
            performance_metrics={"domain_frequency": frequency}
        )
    
    def _create_keyword_filter(self, keywords: List[str], score: float) -> EmailFilter:
        """Create filter for keyword combination"""
        keyword_str = "_".join(keywords[:3])
        filter_id = f"keywords_{keyword_str}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        return EmailFilter(
            filter_id=filter_id,
            name=f"Keywords: {', '.join(keywords[:3])}",
            description=f"Auto-generated filter for keyword combination (score: {score})",
            criteria={
                "subject_keywords": keywords,
                "operator": "AND",
                "min_score": score
            },
            actions={
                "add_label": f"Keywords/{keyword_str}",
                "mark_important": False
            },
            priority=3,
            effectiveness_score=min(1.0, score / 10),
            created_date=datetime.now(),
            last_used=datetime.now(),
            usage_count=0,
            false_positive_rate=0.0,
            performance_metrics={"keyword_score": score}
        )
    
    def _find_keyword_combinations(self, keyword_counter: Counter) -> List[tuple[List[str], float]]:
        """Find meaningful keyword combinations"""
        combinations = []
        frequent_keywords = [word for word, count in keyword_counter.most_common(50) if count >= 3]
        
        # Generate 2-word combinations
        for i, word1 in enumerate(frequent_keywords):
            for word2 in frequent_keywords[i+1:]:
                # Calculate combination score based on co-occurrence
                score = min(keyword_counter[word1], keyword_counter[word2]) / 2
                if score >= 2:
                    combinations.append(([word1, word2], score))
        
        return sorted(combinations, key=lambda x: x[1], reverse=True)[:10]
    
    def prune_ineffective_filters(self) -> Dict[str, Any]:
        """Remove or disable ineffective filters"""
        pruning_results = {
            "pruned_filters": [],
            "disabled_filters": [],
            "updated_filters": [],
            "total_analyzed": 0,
            "performance_improvements": {}
        }
        
        # Load all filters
        all_filters = self._load_all_filters() # Load all, including inactive ones for this evaluation
        pruning_results["total_analyzed"] = len(all_filters)

        active_filters_map = {f.filter_id: f for f in all_filters if self._is_filter_active_in_db(f.filter_id)} # Check DB for active status
        
        actions_to_take = defaultdict(list)
        filters_to_keep_for_redundancy_check = []

        for filter_obj in all_filters:
            # Only evaluate active filters for pruning actions like disable/optimize.
            # Potentially, an inactive filter could be pruned if it's very old and meets pruning criteria.
            # For now, let's focus evaluation on active ones, or those that should be active.
            # The _evaluate_filter_for_pruning can also consider if a filter is currently inactive.
            
            evaluation_action = self._evaluate_filter_for_pruning(filter_obj) # This method might need adjustment
            
            if evaluation_action == "prune":
                actions_to_take["prune"].append(filter_obj)
            elif evaluation_action == "disable":
                # Only disable if it was active
                if filter_obj.filter_id in active_filters_map:
                    actions_to_take["disable"].append(filter_obj)
                else: # If already inactive, it might be kept or pruned based on other rules (e.g. age)
                    filters_to_keep_for_redundancy_check.append(filter_obj) # Or it's just ignored
            elif evaluation_action == "optimize":
                # Only optimize if it was active
                if filter_obj.filter_id in active_filters_map:
                    actions_to_take["optimize"].append(filter_obj)
                else: # If inactive, but could be optimized, what to do? For now, ignore.
                    filters_to_keep_for_redundancy_check.append(filter_obj)
            else: # "keep"
                if filter_obj.filter_id in active_filters_map: # Only active filters are kept for redundancy
                    filters_to_keep_for_redundancy_check.append(filter_obj)
                # If inactive and "keep", it remains inactive and not part of active redundancy checks.

        # Execute actions
        for filter_obj in actions_to_take["prune"]:
            self._delete_filter(filter_obj.filter_id)
            pruning_results["pruned_filters"].append({"filter_id": filter_obj.filter_id, "name": filter_obj.name, "reason": "Pruned by evaluation"})
            if filter_obj.filter_id in active_filters_map: del active_filters_map[filter_obj.filter_id]

        for filter_obj in actions_to_take["disable"]:
            self._disable_filter(filter_obj.filter_id)
            pruning_results["disabled_filters"].append({"filter_id": filter_obj.filter_id, "name": filter_obj.name, "reason": "Disabled by evaluation"})
            if filter_obj.filter_id in active_filters_map: del active_filters_map[filter_obj.filter_id]

        for filter_obj in actions_to_take["optimize"]:
            optimized_filter = self._optimize_filter(filter_obj) # Assume _optimize_filter returns the modified object
            self._update_filter(optimized_filter)
            pruning_results["updated_filters"].append({"filter_id": optimized_filter.filter_id, "name": optimized_filter.name, "changes": "Criteria optimized"})
            # No change to active_filters_map key, but its value (filter_obj) is now stale if map holds objects.
            # If map holds IDs, then it's fine. Let's assume filters_to_keep_for_redundancy_check holds latest objects if needed.
            # For simplicity, we'll use the remaining filters in active_filters_map for redundancy check.
            # Update: filters_to_keep_for_redundancy_check should be used instead.
            # The optimized filter remains active.
            active_filters_map[filter_obj.filter_id] = optimized_filter # Update with optimized version

        # Update filters_to_keep_for_redundancy_check to reflect optimizations
        final_filters_for_redundancy_check = []
        for f_obj in filters_to_keep_for_redundancy_check:
            if f_obj.filter_id in active_filters_map: # If it was kept and active
                 final_filters_for_redundancy_check.append(active_filters_map[f_obj.filter_id])

        # Remove redundant filters from the set of currently active and kept filters
        # This should operate on filters that are currently considered active after the above pruning/disabling.
        self._prune_redundant_filters(final_filters_for_redundancy_check, pruning_results)
        
        self.logger.info(f"Pruning completed: {len(pruning_results['pruned_filters'])} pruned, "
                        f"{len(pruning_results['disabled_filters'])} disabled, "
                        f"{len(pruning_results['updated_filters'])} optimized")
        
        return pruning_results

    def _is_filter_active_in_db(self, filter_id: str) -> bool:
        """Check if a filter is currently marked as active in the database."""
        # This is a helper, assumes _load_filter or similar would respect is_active,
        # but _load_all_filters was changed to load all for full eval.
        # So we need a direct check.
        row = self._db_fetchone("SELECT is_active FROM email_filters WHERE filter_id = ?", (filter_id,))
        return row['is_active'] == 1 if row else False

    def _prune_redundant_filters(self, active_kept_filters: List[EmailFilter], pruning_results: Dict[str, Any]):
        """Finds and prunes redundant filters from the provided list."""
        # Sort filters by effectiveness (desc) to prefer keeping more effective ones
        sorted_filters = sorted(active_kept_filters, key=lambda f: f.effectiveness_score, reverse=True)

        deleted_ids_due_to_redundancy: Set[str] = set()

        for i, filter1 in enumerate(sorted_filters):
            if filter1.filter_id in deleted_ids_due_to_redundancy:
                continue # Skip if already marked for deletion

            for j in range(i + 1, len(sorted_filters)):
                filter2 = sorted_filters[j]
                if filter2.filter_id in deleted_ids_due_to_redundancy:
                    continue

                similarity = self._calculate_filter_similarity(filter1, filter2)
                if similarity > self.pruning_criteria["redundancy_threshold"]:
                    # filter1 is more effective or earlier in list, so prune filter2
                    self._delete_filter(filter2.filter_id) # Actual deletion
                    pruning_results["pruned_filters"].append({
                        "filter_id": filter2.filter_id,
                        "name": filter2.name,
                        "reason": f"Redundant with {filter1.name} (similarity: {similarity:.2f})"
                    })
                    deleted_ids_due_to_redundancy.add(filter2.filter_id)

    def _evaluate_filter_for_pruning(self, filter_obj: EmailFilter) -> str:
        """Evaluate if filter should be pruned, disabled, or optimized"""
        # This evaluation should ideally know if the filter is currently active from DB.
        # For now, let's assume filter_obj reflects its current DB state accurately enough for evaluation.
        # Or, add a parameter is_currently_active.
        # For simplicity, we assume filter_obj.effectiveness_score etc. are up-to-date.

        criteria = self.pruning_criteria
        
        # Rule 1: Very low effectiveness = prune
        if filter_obj.effectiveness_score < criteria["effectiveness_threshold"] * 0.5: # Stricter for direct prune
             return "prune"

        # Rule 2: High false positive rate = prune
        if filter_obj.false_positive_rate > criteria["false_positive_threshold"]:
            return "prune"
        
        # Rule 3: Old and unused (if it were active, this implies it should be disabled)
        # If it's already inactive, this rule might mean prune if it's very old.
        # Let's assume this rule is primarily for active filters to become disabled.
        days_since_last_used = (datetime.now() - filter_obj.last_used).days # More relevant than created_date
        # This rule is tricky if the filter was already inactive.
        # Let's assume we are evaluating an "active" filter for this condition.
        # If _is_filter_active_in_db(filter_obj.filter_id) : (check added to caller)
        if (filter_obj.usage_count < criteria["usage_threshold"] and
                days_since_last_used > criteria["age_threshold_days"]):
            return "disable" # Candidate for disabling if it was active

        # Rule 4: Performance suggests optimization (for active filters)
        # if _is_filter_active_in_db(filter_obj.filter_id): (check added to caller)
        performance = self._get_filter_performance(filter_obj.filter_id) # This fetches latest performance
        if performance and (performance.accuracy < criteria["accuracy_threshold"] or
                              performance.f1_score < criteria["f1_threshold"]):
            # Check if effectiveness is not too low for optimization
            if filter_obj.effectiveness_score > criteria["effectiveness_threshold"] * 0.7: # Avoid optimizing hopeless filters
                return "optimize"
            else: # Low effectiveness and poor perf might mean prune or disable
                return "disable" # Or prune if it also meets other prune criteria

        # Rule 5: Low effectiveness but not terrible, and not high FP = disable rather than prune
        if filter_obj.effectiveness_score < criteria["effectiveness_threshold"]:
            return "disable"

        return "keep"
    
    def _optimize_filter(self, filter_obj: EmailFilter) -> EmailFilter:
        """Optimize filter criteria for better performance"""
        # Analyze recent performance to identify improvements
        performance_history = self._get_filter_performance_history(filter_obj.filter_id)
        
        if not performance_history:
            return filter_obj
        
        # Adjust criteria based on false positives/negatives
        optimized_criteria = filter_obj.criteria.copy()
        
        # If high false positive rate, make criteria more restrictive
        if filter_obj.false_positive_rate > 0.1:
            optimized_criteria = self._make_criteria_more_restrictive(optimized_criteria)
        
        # If low recall, make criteria more inclusive
        avg_recall = sum(p.recall for p in performance_history) / len(performance_history)
        if avg_recall < 0.6:
            optimized_criteria = self._make_criteria_more_inclusive(optimized_criteria)
        
        filter_obj.criteria = optimized_criteria
        return filter_obj
    
    def _make_criteria_more_restrictive(self, criteria: Dict[str, Any]) -> Dict[str, Any]:
        """Make filter criteria more restrictive to reduce false positives"""
        # Add more specific keywords or patterns
        if "subject_keywords" in criteria:
            # Require multiple keyword matches
            criteria["keyword_operator"] = "AND"
            criteria["min_keyword_matches"] = max(2, len(criteria["subject_keywords"]) // 2)
        
        if "from_patterns" in criteria:
            # Make email patterns more specific
            criteria["from_patterns"] = [pattern + "$" for pattern in criteria["from_patterns"]]
        
        return criteria
    
    def _make_criteria_more_inclusive(self, criteria: Dict[str, Any]) -> Dict[str, Any]:
        """Make filter criteria more inclusive to increase recall"""
        # Add related keywords
        if "subject_keywords" in criteria:
            criteria["keyword_operator"] = "OR"
            criteria["min_keyword_matches"] = 1
        
        return criteria
    
    def _find_redundant_filters(self, filters: List[EmailFilter]) -> List[tuple[str, str]]:
        """Find pairs of redundant filters"""
        redundant_pairs = []
        
        for i, filter1 in enumerate(filters):
            for filter2 in filters[i+1:]:
                similarity = self._calculate_filter_similarity(filter1, filter2)
                if similarity > self.pruning_criteria["redundancy_threshold"]:
                    redundant_pairs.append((filter1.filter_id, filter2.filter_id))
        
        return redundant_pairs
    
    def _calculate_filter_similarity(self, filter1: EmailFilter, filter2: EmailFilter) -> float:
        """Calculate similarity between two filters"""
        # Compare criteria
        criteria_similarity = self._compare_criteria(filter1.criteria, filter2.criteria)
        
        # Compare actions
        action_similarity = self._compare_actions(filter1.actions, filter2.actions)
        
        # Overall similarity
        return (criteria_similarity + action_similarity) / 2
    
    def _compare_criteria(self, criteria1: Dict[str, Any], criteria2: Dict[str, Any]) -> float:
        """Compare filter criteria similarity"""
        common_keys = set(criteria1.keys()) & set(criteria2.keys())
        if not common_keys:
            return 0.0
        
        similarity_scores = []
        
        for key in common_keys:
            val1, val2 = criteria1[key], criteria2[key]
            
            if isinstance(val1, list) and isinstance(val2, list):
                # Compare lists (e.g., keywords, patterns)
                common_items = set(val1) & set(val2)
                total_items = set(val1) | set(val2)
                similarity = len(common_items) / len(total_items) if total_items else 0
            elif val1 == val2:
                similarity = 1.0
            else:
                similarity = 0.0
            
            similarity_scores.append(similarity)
        
        return sum(similarity_scores) / len(similarity_scores) if similarity_scores else 0.0
    
    def _compare_actions(self, actions1: Dict[str, Any], actions2: Dict[str, Any]) -> float:
        """Compare filter actions similarity"""
        common_keys = set(actions1.keys()) & set(actions2.keys())
        if not common_keys:
            return 0.0
        
        matches = sum(1 for key in common_keys if actions1[key] == actions2[key])
        return matches / len(common_keys)
    
    def evaluate_filter_performance(self, filter_id: str, test_emails: List[Dict[str, Any]]) -> FilterPerformance:
        """Evaluate filter performance on test emails"""
        filter_obj = self._load_filter(filter_id)
        if not filter_obj:
            raise ValueError(f"Filter {filter_id} not found")
        
        start_time = datetime.now()
        
        # Get results of applying filter to emails
        application_results, processing_time_ms = self._get_filter_application_results(filter_obj, test_emails, start_time)
        
        # Calculate performance metrics
        metrics_dict = self._calculate_performance_metrics_from_results(application_results, len(test_emails))
        
        performance = FilterPerformance(
            filter_id=filter_id,
            accuracy=metrics_dict["accuracy"],
            precision=metrics_dict["precision"],
            recall=metrics_dict["recall"],
            f1_score=metrics_dict["f1_score"],
            processing_time_ms=processing_time_ms,
            emails_processed=len(test_emails),
            true_positives=metrics_dict["true_positives"],
            false_positives=metrics_dict["false_positives"],
            false_negatives=metrics_dict["false_negatives"]
        )
        
        # Save performance metrics
        self._save_filter_performance(performance)
        
        # Update filter effectiveness
        filter_obj.effectiveness_score = performance.f1_score # Use the F1 from FilterPerformance object
        filter_obj.false_positive_rate = metrics_dict["false_positive_rate"]
        self._update_filter(filter_obj)
        
        return performance

    def _get_filter_application_results(self, filter_obj: EmailFilter, test_emails: List[Dict[str, Any]], start_time: datetime) -> tuple[List[tuple[bool, bool]], float]:
        """Applies a filter to test emails and returns predicted vs actual results, and processing time."""
        results = []
        for email in test_emails:
            predicted = self._apply_filter_to_email(filter_obj, email)
            actual = email.get('expected_filter_match', False) # Assuming 'expected_filter_match' key exists
            results.append((predicted, actual))

        processing_time_ms = (datetime.now() - start_time).total_seconds() * 1000
        return results, processing_time_ms

    def _calculate_performance_metrics_from_results(self, results: List[tuple[bool, bool]], total_emails: int) -> Dict[str, float]:
        """Calculates various performance metrics from (predicted, actual) results."""
        true_positives = sum(1 for pred, actual in results if pred and actual)
        false_positives = sum(1 for pred, actual in results if pred and not actual)
        false_negatives = sum(1 for pred, actual in results if not pred and actual)
        true_negatives = sum(1 for pred, actual in results if not pred and not actual)

        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0.0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0.0
        accuracy = (true_positives + true_negatives) / total_emails if total_emails > 0 else 0.0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        false_positive_rate = false_positives / total_emails if total_emails > 0 else 0.0

        return {
            "true_positives": true_positives,
            "false_positives": false_positives,
            "false_negatives": false_negatives,
            "true_negatives": true_negatives,
            "precision": precision,
            "recall": recall,
            "accuracy": accuracy,
            "f1_score": f1_score,
            "false_positive_rate": false_positive_rate
        }
    
    def _check_sender_patterns(self, criteria_block: Dict[str, Any], email: Dict[str, Any]) -> bool:
        """Check sender patterns against email."""
        sender = email.get('senderEmail', '')
        # Uses re.search for regex matching, re.IGNORECASE for case-insensitivity.
        return any(re.search(pattern, sender, re.IGNORECASE) for pattern in criteria_block)

    def _check_subject_keywords(self, criteria_block: List[str], email: Dict[str, Any], operator: str, min_matches: int) -> bool:
        """Check subject keywords against email subject."""
        subject = email.get('subject', '').lower()
        keyword_matches = sum(1 for keyword in criteria_block if keyword.lower() in subject)

        if operator == "AND":
            return keyword_matches == len(criteria_block) # All keywords must match
        elif operator == "OR":
            return keyword_matches >= min_matches
        return False # Should not happen if operator is valid

    def _check_content_keywords(self, criteria_block: List[str], email: Dict[str, Any]) -> bool:
        """Check content keywords against email content."""
        content = email.get('content', '').lower()
        # Assumes OR logic for content keywords: any keyword match is sufficient.
        return any(keyword.lower() in content for keyword in criteria_block)

    def _check_exclusion_patterns(self, criteria_block: List[str], email: Dict[str, Any]) -> bool:
        """Check exclusion patterns (regex) against email subject and content. Returns True if no exclusions match."""
        text_to_check = f"{email.get('subject', '')} {email.get('content', '')}" # No .lower() here, regex handles case if needed via IGNORECASE
        # If any exclusion pattern matches, the check fails (returns False).
        # Assuming criteria_block contains regex patterns.
        if any(re.search(pattern, text_to_check, re.IGNORECASE) for pattern in criteria_block):
            return False # Exclusion found (pattern matched)
        return True # No exclusions matched

    def _apply_filter_to_email(self, filter_obj: EmailFilter, email: Dict[str, Any]) -> bool:
        """Apply filter to email and return match result by evaluating various criteria checks."""
        criteria = filter_obj.criteria

        if "from_patterns" in criteria:
            if not self._check_sender_patterns(criteria["from_patterns"], email):
                return False
        
        if "subject_keywords" in criteria:
            operator = criteria.get("keyword_operator", "OR") # Default OR
            min_matches = criteria.get("min_keyword_matches", 1) # Default 1 for OR
            if operator == "AND": # For AND, all keywords must match
                min_matches = len(criteria["subject_keywords"])
            if not self._check_subject_keywords(criteria["subject_keywords"], email, operator, min_matches):
                return False
        
        if "content_keywords" in criteria:
            # Assuming OR logic for content keywords by default (any match is enough)
            # If specific AND/min_matches logic is needed, it should be structured like subject_keywords
            if not self._check_content_keywords(criteria["content_keywords"], email):
                return False
        
        if "exclude_patterns" in criteria: # Renamed from exclude_keywords for clarity
            if not self._check_exclusion_patterns(criteria["exclude_patterns"], email):
                return False
        
        # Add other criteria checks here following the same pattern, e.g.:
        # if "attachment_types" in criteria:
        #     if not self._check_attachment_types(criteria["attachment_types"], email):
        #         return False

        return True
    
    # Database operations
    def _save_filter(self, filter_obj: EmailFilter):
        """Save filter to database"""
        query = """
            INSERT OR REPLACE INTO email_filters 
            (filter_id, name, description, criteria, actions, priority, effectiveness_score,
             created_date, last_used, usage_count, false_positive_rate, performance_metrics, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
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
            True # Assuming save means it's active
        )
        self._db_execute(query, params)

    def _load_filter(self, filter_id: str) -> Optional[EmailFilter]:
        """Load a specific filter from database, regardless of active status."""
        query = "SELECT * FROM email_filters WHERE filter_id = ?"
        row = self._db_fetchone(query, (filter_id,))
        
        if not row:
            return None
        
        return EmailFilter(
            filter_id=row[0],
            name=row[1],
            description=row[2],
            criteria=json.loads(row[3]),
            actions=json.loads(row[4]),
            priority=row[5],
            effectiveness_score=row[6],
            created_date=datetime.fromisoformat(row[7]),
            last_used=datetime.fromisoformat(row[8]),
            usage_count=row[9],
            false_positive_rate=row[10],
            performance_metrics=json.loads(row["performance_metrics"]),
            # is_active=row["is_active"] == 1 # Assuming EmailFilter dataclass gets an is_active field
            # For now, EmailFilter dataclass does not have is_active. Callers can use _is_filter_active_in_db if needed.
        )

    def _load_all_filters(self) -> List[EmailFilter]:
        """Load all filters from the database, regardless of active status."""
        query = "SELECT * FROM email_filters" # Changed to load all
        rows = self._db_fetchall(query)
        
        filters = []
        for row in rows:
            filters.append(EmailFilter(
                filter_id=row["filter_id"],
                name=row["name"],
                description=row["description"],
                criteria=json.loads(row["criteria"]),
                actions=json.loads(row["actions"]),
                priority=row["priority"],
                effectiveness_score=row["effectiveness_score"],
                created_date=datetime.fromisoformat(row["created_date"]),
                last_used=datetime.fromisoformat(row["last_used"]),
                usage_count=row["usage_count"],
                false_positive_rate=row["false_positive_rate"],
                performance_metrics=json.loads(row["performance_metrics"]),
                # is_active=row["is_active"] == 1 # As above, EmailFilter dataclass would need this
            ))
        return filters

    def _update_filter(self, filter_obj: EmailFilter):
        """Update filter in database. This will also set it to active."""
        # _save_filter handles INSERT OR REPLACE, and currently always sets is_active = True.
        # This might need refinement if updating a filter should not automatically re-activate it.
        # For pruning/optimization, typically an updated filter remains/becomes active.
        self._save_filter(filter_obj)

    def _delete_filter(self, filter_id: str):
        """Permanently delete filter and its performance metrics from database."""
        self._db_execute("DELETE FROM email_filters WHERE filter_id = ?", (filter_id,))
        self._db_execute("DELETE FROM filter_performance WHERE filter_id = ?", (filter_id,))

    def _disable_filter(self, filter_id: str):
        """Disable filter without deleting"""
        query = "UPDATE email_filters SET is_active = 0 WHERE filter_id = ?"
        self._db_execute(query, (filter_id,))

    def _save_filter_performance(self, performance: FilterPerformance):
        """Save filter performance metrics"""
        query = """
            INSERT INTO filter_performance 
            (performance_id, filter_id, measurement_date, accuracy, precision_score, recall_score,
             f1_score, processing_time_ms, emails_processed, true_positives, false_positives, false_negatives)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        # Added microseconds for more unique ID
        performance_id = f"{performance.filter_id}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        params = (
            performance_id,
            performance.filter_id,
            datetime.now().isoformat(),
            performance.accuracy,
            performance.precision,
            performance.recall,
            performance.f1_score,
            performance.processing_time_ms,
            performance.emails_processed,
            performance.true_positives,
            performance.false_positives,
            performance.false_negatives
        )
        self._db_execute(query, params)

    def _get_filter_performance(self, filter_id: str) -> Optional[FilterPerformance]:
        """Get latest performance metrics for filter"""
        query = """
            SELECT * FROM filter_performance 
            WHERE filter_id = ? 
            ORDER BY measurement_date DESC 
            LIMIT 1
        """
        row = self._db_fetchone(query, (filter_id,))
        
        if not row:
            return None
        
        return FilterPerformance(
            filter_id=row[1],
            accuracy=row[3],
            precision=row[4],
            recall=row[5],
            f1_score=row[6],
            processing_time_ms=row[7],
            emails_processed=row[8],
            true_positives=row[9],
            false_positives=row["false_positives"],
            false_negatives=row["false_negatives"]
        )

    def _get_filter_performance_history(self, filter_id: str, days: int = 30) -> List[FilterPerformance]:
        """Get performance history for filter"""
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        query = """
            SELECT * FROM filter_performance 
            WHERE filter_id = ? AND measurement_date >= ?
            ORDER BY measurement_date DESC
        """
        rows = self._db_fetchall(query, (filter_id, cutoff_date))
        
        return [FilterPerformance(
            filter_id=row["filter_id"],
            accuracy=row["accuracy"],
            precision=row["precision_score"], # Note: column name precision_score in DB
            recall=row["recall_score"],       # Note: column name recall_score in DB
            f1_score=row["f1_score"],
            processing_time_ms=row["processing_time_ms"],
            emails_processed=row["emails_processed"],
            true_positives=row["true_positives"],
            false_positives=row["false_positives"],
            false_negatives=row["false_negatives"]
        ) for row in rows]

    def get_active_filters_sorted(self) -> List[EmailFilter]:
        """Loads all active filters from the database, sorted by priority."""
        query = "SELECT * FROM email_filters WHERE is_active = 1 ORDER BY priority DESC"
        rows = self._db_fetchall(query)
        filters = []
        for row in rows:
            filters.append(EmailFilter(
                filter_id=row["filter_id"],
                name=row["name"],
                description=row["description"],
                criteria=json.loads(row["criteria"]),
                actions=json.loads(row["actions"]),
                priority=row["priority"],
                effectiveness_score=row["effectiveness_score"],
                created_date=datetime.fromisoformat(row["created_date"]),
                last_used=datetime.fromisoformat(row["last_used"]),
                usage_count=row["usage_count"],
                false_positive_rate=row["false_positive_rate"],
                performance_metrics=json.loads(row["performance_metrics"]),
            ))
        return filters

    def _execute_filter_actions(self, email_data: Dict[str, Any], actions: Dict[str, Any]) -> List[str]:
        """
        Executes the defined actions on the email_data dictionary.
        Returns a list of descriptions of actions taken.
        """
        actions_taken_summary = []

        if actions.get("add_label"):
            label = actions["add_label"]
            if "labels" not in email_data:
                email_data["labels"] = []
            if label not in email_data["labels"]:
                email_data["labels"].append(label)
            actions_taken_summary.append(f"Added label: {label}")

        if actions.get("mark_important"):
            email_data["is_important_override"] = True # Use an override field
            actions_taken_summary.append("Marked as important")

        if actions.get("archive"):
            email_data["should_archive_override"] = True
            actions_taken_summary.append("Marked for archive")

        if actions.get("mark_read"):
            email_data["is_read_override"] = True
            actions_taken_summary.append("Marked as read")

        if actions.get("set_priority_high"): # Specific action from BSFM
            email_data["priority_override"] = "high"
            actions_taken_summary.append("Set priority to high")

        if actions.get("set_low_priority"): # Specific action from BSFM
            email_data["priority_override"] = "low"
            actions_taken_summary.append("Set priority to low")

        if actions.get("mark_as_spam"): # Specific action from BSFM
            email_data["is_spam_override"] = True
            email_data["priority_override"] = "low" # Typically spam is low priority
            actions_taken_summary.append("Marked as spam")

        # For category overrides, BSFM used specific action names
        # We can map them or use a generic "set_category" in NSFM's action definition
        # Example: action "set_category_finance" from BSFM
        if actions.get("action_name") == "set_category_finance": # Hypothetical action name in NSFM
             email_data["category_name_override"] = "Finance & Banking"
             actions_taken_summary.append("Categorized as Finance & Banking")
        elif actions.get("category_override"): # More generic way
             email_data["category_name_override"] = actions["category_override"]
             actions_taken_summary.append(f"Categorized as {actions['category_override']}")


        # This part needs to be adapted based on how NSFM actions are structured.
        # The above are examples based on BSFM's direct manipulations.
        # NSFM actions are like: "actions": {"add_label": "Work/High Priority", "mark_important": True}

        return actions_taken_summary

    def apply_filters_to_email_data(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply all active, sorted filters to an email data dictionary.
        Modifies email_data in place and returns a summary of actions.
        """
        applied_filter_results = []
        sorted_filters = self.get_active_filters_sorted()

        email_actions_summary = {
            "filters_matched": [],
            "actions_taken": [],
            "modified_fields": {} # To track what changed in email_data
        }

        for filter_obj in sorted_filters:
            match_result = self._apply_filter_to_email(filter_obj, email_data)

            if match_result:
                self.logger.info(f"Email matched filter: {filter_obj.name}")
                # Update usage stats for the matched filter
                filter_obj.usage_count += 1
                filter_obj.last_used = datetime.now()
                self._update_filter(filter_obj) # Save updated stats to DB

                # Execute actions defined in the filter
                action_descriptions = self._execute_filter_actions(email_data, filter_obj.actions)

                email_actions_summary["filters_matched"].append(filter_obj.name)
                email_actions_summary["actions_taken"].extend(action_descriptions)

                # For simplicity, we'll assume BSFM's "stop at first match for certain high-priority actions"
                # This can be configured in the filter's actions dict if needed e.g. "stop_processing": True
                if filter_obj.actions.get("mark_as_spam") or filter_obj.actions.get("set_priority_high"):
                    self.logger.info(f"Stopping further filter processing due to action in {filter_obj.name}")
                    break

        # To report modified fields, we'd need to compare original email_data to current.
        # For now, this is a conceptual placeholder.
        # email_actions_summary["modified_fields"] = ...

        return email_actions_summary

def main():
    """Example usage of smart filter manager"""
    manager = SmartFilterManager()
    
    # Sample email data for testing
    sample_emails = [
        {
            'senderEmail': 'manager@company.com',
            'subject': 'Urgent: Budget Review Meeting',
            'content': 'We need to discuss the quarterly budget immediately.',
            'isImportant': True,
            'category': 'work_business'
        },
        {
            'senderEmail': 'noreply@bank.com',
            'subject': 'Your Monthly Statement',
            'content': 'Your account statement is ready for download.',
            'category': 'finance_banking'
        }
    ]
    
    # Create intelligent filters
    filters = manager.create_intelligent_filters(sample_emails)
    print(f"Created {len(filters)} intelligent filters")
    
    # Evaluate filter performance
    for filter_obj in filters[:1]:  # Test first filter
        performance = manager.evaluate_filter_performance(filter_obj.filter_id, sample_emails)
        print(f"Filter {filter_obj.name}: Accuracy={performance.accuracy:.2f}, F1={performance.f1_score:.2f}")
    
    # Prune ineffective filters
    pruning_results = manager.prune_ineffective_filters()
    print(f"Pruning results: {len(pruning_results['pruned_filters'])} pruned, "
          f"{len(pruning_results['disabled_filters'])} disabled")

if __name__ == "__main__":
    main()