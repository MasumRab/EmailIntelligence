"""
Smart Email Filter Management System
Implements intelligent filter creation, pruning, and Google Apps Script integration
"""

import json
import re
from typing import Dict, List, Optional, Any, Tuple, Set
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
        self._init_filter_db()
        
        # Filter categories and templates
        self.filter_templates = self._load_filter_templates()
        self.pruning_criteria = self._load_pruning_criteria()
        
    def _init_filter_db(self):
        """Initialize filter database"""
        conn = sqlite3.connect(self.db_path)
        
        conn.execute("""
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
        """)
        
        conn.execute("""
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
        """)
        
        conn.execute("""
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
        """)
        
        conn.commit()
        conn.close()
    
    def _load_filter_templates(self) -> Dict[str, Dict[str, Any]]:
        """Load intelligent filter templates"""
        return {
            "high_priority_work": {
                "criteria": {
                    "from_patterns": [
                        r".*@(company\.com|organization\.org)",
                        r".*(manager|director|ceo|president).*@.*"
                    ],
                    "subject_keywords": ["urgent", "important", "asap", "deadline", "meeting"],
                    "content_keywords": ["project", "budget", "proposal", "contract"],
                    "time_sensitivity": "high",
                    "exclude_patterns": ["newsletter", "unsubscribe", "automated"]
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
                    "subject_keywords": ["invoice", "statement", "payment", "receipt", "bill"],
                    "attachment_types": ["pdf", "xlsx", "csv"],
                    "content_keywords": ["amount", "due", "balance", "transaction"]
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
                    "subject_keywords": ["notification", "alert", "update", "reminder"],
                    "content_keywords": ["automated", "do not reply", "unsubscribe"],
                    "exclude_keywords": ["urgent", "important", "action required"]
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
                    "subject_keywords": ["sale", "discount", "offer", "deal", "promotion", "%", "save"],
                    "content_keywords": ["unsubscribe", "promotional", "marketing", "advertisement"],
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
                    "exclude_patterns": [r".*noreply.*", r".*automated.*"],
                    "subject_exclude": ["newsletter", "promotion", "unsubscribe"],
                    "content_personal_indicators": ["how are you", "hope you", "let me know", "talk soon"]
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
                    "subject_keywords": ["security", "login", "password", "suspicious", "breach", "alert"],
                    "from_patterns": [r".*security.*@.*", r".*@.*(google|microsoft|apple)\.com"],
                    "content_keywords": ["unauthorized", "verify", "suspicious activity", "security alert"],
                    "urgency_indicators": ["immediate", "verify now", "action required"]
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
        
        # Generate filters from templates
        for template_name, template in self.filter_templates.items():
            if self._should_create_filter(template, patterns):
                filter_obj = self._create_filter_from_template(template_name, template)
                created_filters.append(filter_obj)
                self._save_filter(filter_obj)
        
        # Create custom filters based on discovered patterns
        custom_filters = self._create_custom_filters(patterns)
        created_filters.extend(custom_filters)
        
        self.logger.info(f"Created {len(created_filters)} intelligent filters")
        return created_filters
    
    def _analyze_email_patterns(self, email_samples: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze email samples to discover patterns"""
        patterns = {
            "sender_domains": Counter(),
            "subject_keywords": Counter(),
            "content_keywords": Counter(),
            "time_patterns": defaultdict(list),
            "category_distributions": Counter(),
            "importance_indicators": set(),
            "automation_indicators": set()
        }
        
        for email in email_samples:
            # Analyze sender domains
            sender_domain = self._extract_domain(email.get('senderEmail', ''))
            if sender_domain:
                patterns["sender_domains"][sender_domain] += 1
            
            # Analyze subject keywords
            subject_words = self._extract_keywords(email.get('subject', ''))
            patterns["subject_keywords"].update(subject_words)
            
            # Analyze content keywords
            content_words = self._extract_keywords(email.get('content', ''))
            patterns["content_keywords"].update(content_words)
            
            # Analyze categories
            category = email.get('category') or email.get('ai_analysis', {}).get('topic', 'unknown')
            patterns["category_distributions"][category] += 1
            
            # Detect importance indicators
            if email.get('isImportant') or email.get('isStarred'):
                patterns["importance_indicators"].update(subject_words + content_words)
            
            # Detect automation indicators
            if self._is_automated_email(email):
                patterns["automation_indicators"].update(subject_words + [sender_domain])
        
        return patterns
    
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
    
    def _find_keyword_combinations(self, keyword_counter: Counter) -> List[Tuple[List[str], float]]:
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
        filters = self._load_all_filters()
        pruning_results["total_analyzed"] = len(filters)
        
        for filter_obj in filters:
            action = self._evaluate_filter_for_pruning(filter_obj)
            
            if action == "prune":
                self._delete_filter(filter_obj.filter_id)
                pruning_results["pruned_filters"].append({
                    "filter_id": filter_obj.filter_id,
                    "name": filter_obj.name,
                    "reason": "Low effectiveness or high false positive rate"
                })
            
            elif action == "disable":
                self._disable_filter(filter_obj.filter_id)
                pruning_results["disabled_filters"].append({
                    "filter_id": filter_obj.filter_id,
                    "name": filter_obj.name,
                    "reason": "Underutilized but potentially useful"
                })
            
            elif action == "optimize":
                optimized_filter = self._optimize_filter(filter_obj)
                self._update_filter(optimized_filter)
                pruning_results["updated_filters"].append({
                    "filter_id": filter_obj.filter_id,
                    "name": filter_obj.name,
                    "changes": "Criteria optimized for better performance"
                })
        
        # Remove redundant filters
        redundant_pairs = self._find_redundant_filters(filters)
        for filter1_id, filter2_id in redundant_pairs:
            # Keep the more effective one
            filter1 = next(f for f in filters if f.filter_id == filter1_id)
            filter2 = next(f for f in filters if f.filter_id == filter2_id)
            
            if filter1.effectiveness_score < filter2.effectiveness_score:
                self._delete_filter(filter1_id)
                pruning_results["pruned_filters"].append({
                    "filter_id": filter1_id,
                    "name": filter1.name,
                    "reason": f"Redundant with {filter2.name}"
                })
            else:
                self._delete_filter(filter2_id)
                pruning_results["pruned_filters"].append({
                    "filter_id": filter2_id,
                    "name": filter2.name,
                    "reason": f"Redundant with {filter1.name}"
                })
        
        self.logger.info(f"Pruning completed: {len(pruning_results['pruned_filters'])} pruned, "
                        f"{len(pruning_results['disabled_filters'])} disabled, "
                        f"{len(pruning_results['updated_filters'])} optimized")
        
        return pruning_results
    
    def _evaluate_filter_for_pruning(self, filter_obj: EmailFilter) -> str:
        """Evaluate if filter should be pruned, disabled, or optimized"""
        criteria = self.pruning_criteria
        
        # Check effectiveness
        if filter_obj.effectiveness_score < criteria["effectiveness_threshold"]:
            return "prune"
        
        # Check false positive rate
        if filter_obj.false_positive_rate > criteria["false_positive_threshold"]:
            return "prune"
        
        # Check usage
        days_since_creation = (datetime.now() - filter_obj.created_date).days
        if (filter_obj.usage_count < criteria["usage_threshold"] and 
            days_since_creation > criteria["age_threshold_days"]):
            return "disable"
        
        # Check if filter needs optimization
        performance = self._get_filter_performance(filter_obj.filter_id)
        if performance and (performance.accuracy < criteria["accuracy_threshold"] or 
                          performance.f1_score < criteria["f1_threshold"]):
            return "optimize"
        
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
    
    def _find_redundant_filters(self, filters: List[EmailFilter]) -> List[Tuple[str, str]]:
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
        
        # Apply filter to test emails
        results = []
        for email in test_emails:
            predicted = self._apply_filter_to_email(filter_obj, email)
            actual = email.get('expected_filter_match', False)
            results.append((predicted, actual))
        
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        # Calculate metrics
        true_positives = sum(1 for pred, actual in results if pred and actual)
        false_positives = sum(1 for pred, actual in results if pred and not actual)
        false_negatives = sum(1 for pred, actual in results if not pred and actual)
        true_negatives = sum(1 for pred, actual in results if not pred and not actual)
        
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
        accuracy = (true_positives + true_negatives) / len(results) if results else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        performance = FilterPerformance(
            filter_id=filter_id,
            accuracy=accuracy,
            precision=precision,
            recall=recall,
            f1_score=f1_score,
            processing_time_ms=processing_time,
            emails_processed=len(test_emails),
            true_positives=true_positives,
            false_positives=false_positives,
            false_negatives=false_negatives
        )
        
        # Save performance metrics
        self._save_filter_performance(performance)
        
        # Update filter effectiveness
        filter_obj.effectiveness_score = f1_score
        filter_obj.false_positive_rate = false_positives / len(results) if results else 0
        self._update_filter(filter_obj)
        
        return performance
    
    def _apply_filter_to_email(self, filter_obj: EmailFilter, email: Dict[str, Any]) -> bool:
        """Apply filter to email and return match result"""
        criteria = filter_obj.criteria
        
        # Check sender patterns
        if "from_patterns" in criteria:
            sender = email.get('senderEmail', '')
            if not any(re.search(pattern, sender, re.IGNORECASE) for pattern in criteria["from_patterns"]):
                return False
        
        # Check subject keywords
        if "subject_keywords" in criteria:
            subject = email.get('subject', '').lower()
            keyword_matches = sum(1 for keyword in criteria["subject_keywords"] if keyword.lower() in subject)
            
            operator = criteria.get("keyword_operator", "OR")
            min_matches = criteria.get("min_keyword_matches", 1)
            
            if operator == "AND" and keyword_matches < len(criteria["subject_keywords"]):
                return False
            elif operator == "OR" and keyword_matches < min_matches:
                return False
        
        # Check content keywords
        if "content_keywords" in criteria:
            content = email.get('content', '').lower()
            if not any(keyword.lower() in content for keyword in criteria["content_keywords"]):
                return False
        
        # Check exclusion patterns
        if "exclude_patterns" in criteria:
            text = f"{email.get('subject', '')} {email.get('content', '')}".lower()
            if any(pattern.lower() in text for pattern in criteria["exclude_patterns"]):
                return False
        
        return True
    
    # Database operations
    def _save_filter(self, filter_obj: EmailFilter):
        """Save filter to database"""
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            INSERT OR REPLACE INTO email_filters 
            (filter_id, name, description, criteria, actions, priority, effectiveness_score,
             created_date, last_used, usage_count, false_positive_rate, performance_metrics)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
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
            json.dumps(filter_obj.performance_metrics)
        ))
        conn.commit()
        conn.close()
    
    def _load_filter(self, filter_id: str) -> Optional[EmailFilter]:
        """Load filter from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("SELECT * FROM email_filters WHERE filter_id = ?", (filter_id,))
        row = cursor.fetchone()
        conn.close()
        
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
            performance_metrics=json.loads(row[11])
        )
    
    def _load_all_filters(self) -> List[EmailFilter]:
        """Load all active filters"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("SELECT * FROM email_filters WHERE is_active = 1")
        rows = cursor.fetchall()
        conn.close()
        
        filters = []
        for row in rows:
            filters.append(EmailFilter(
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
                performance_metrics=json.loads(row[11])
            ))
        
        return filters
    
    def _update_filter(self, filter_obj: EmailFilter):
        """Update filter in database"""
        self._save_filter(filter_obj)
    
    def _delete_filter(self, filter_id: str):
        """Delete filter from database"""
        conn = sqlite3.connect(self.db_path)
        conn.execute("DELETE FROM email_filters WHERE filter_id = ?", (filter_id,))
        conn.commit()
        conn.close()
    
    def _disable_filter(self, filter_id: str):
        """Disable filter without deleting"""
        conn = sqlite3.connect(self.db_path)
        conn.execute("UPDATE email_filters SET is_active = 0 WHERE filter_id = ?", (filter_id,))
        conn.commit()
        conn.close()
    
    def _save_filter_performance(self, performance: FilterPerformance):
        """Save filter performance metrics"""
        conn = sqlite3.connect(self.db_path)
        performance_id = f"{performance.filter_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        conn.execute("""
            INSERT INTO filter_performance 
            (performance_id, filter_id, measurement_date, accuracy, precision_score, recall_score,
             f1_score, processing_time_ms, emails_processed, true_positives, false_positives, false_negatives)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
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
        ))
        conn.commit()
        conn.close()
    
    def _get_filter_performance(self, filter_id: str) -> Optional[FilterPerformance]:
        """Get latest performance metrics for filter"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("""
            SELECT * FROM filter_performance 
            WHERE filter_id = ? 
            ORDER BY measurement_date DESC 
            LIMIT 1
        """, (filter_id,))
        row = cursor.fetchone()
        conn.close()
        
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
            false_positives=row[10],
            false_negatives=row[11]
        )
    
    def _get_filter_performance_history(self, filter_id: str, days: int = 30) -> List[FilterPerformance]:
        """Get performance history for filter"""
        conn = sqlite3.connect(self.db_path)
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        cursor = conn.execute("""
            SELECT * FROM filter_performance 
            WHERE filter_id = ? AND measurement_date >= ?
            ORDER BY measurement_date DESC
        """, (filter_id, cutoff_date))
        rows = cursor.fetchall()
        conn.close()
        
        return [FilterPerformance(
            filter_id=row[1],
            accuracy=row[3],
            precision=row[4],
            recall=row[5],
            f1_score=row[6],
            processing_time_ms=row[7],
            emails_processed=row[8],
            true_positives=row[9],
            false_positives=row[10],
            false_negatives=row[11]
        ) for row in rows]

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