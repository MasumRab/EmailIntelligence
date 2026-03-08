"""
Manager for intelligent email filters.
"""

import logging
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from .filter_criteria_evaluator import evaluate_filter_criteria
from .filter_database import FilterDatabase
from .filter_models import EmailFilter


class SmartFilterManager:
    """
    Manager for creating, storing, evaluating, and pruning smart email filters.
    """

    def __init__(self, db_path: str = None):
        self.filter_db = FilterDatabase(db_path)
        self.logger = logging.getLogger(__name__)

    def apply_filters(self, email: Dict[str, any], filters: List[EmailFilter] = None) -> List[EmailFilter]:
        """
        Apply filters to an email and return matching filters.

        Args:
            email: A dictionary containing email data.
            filters: Optional list of filters to apply. If None, all saved filters are used.

        Returns:
            A list of filters that matched the email.
        """
        if filters is None:
            filters = self.filter_db.get_all_filters()

        matching_filters = []
        for filter_obj in filters:
            if evaluate_filter_criteria(email, filter_obj):
                matching_filters.append(filter_obj)
                # Update filter usage statistics
                self.filter_db.update_filter_usage(filter_obj.filter_id)

        # Sort by priority
        matching_filters.sort(key=lambda f: f.priority, reverse=True)
        return matching_filters

    def generate_filter_from_email_set(self, emails: List[Dict], name: str = "Generated Filter") -> Optional[EmailFilter]:
        """
        Generate a filter based on patterns in a set of emails.

        Args:
            emails: A list of email dictionaries to analyze.
            name: A name for the generated filter.

        Returns:
            An EmailFilter object, or None if generation failed.
        """
        if not emails:
            return None

        # Analyze patterns in the email set
        subject_keywords = self._extract_common_keywords([e.get("subject", "") for e in emails])
        content_keywords = self._extract_common_keywords([e.get("content", "") for e in emails])
        senders = [e.get("sender_email", "") for e in emails if e.get("sender_email")]
        categories = [e.get("category", "") for e in emails if e.get("category")]

        # Create criteria based on patterns
        criteria = {}
        if subject_keywords:
            criteria["required_keywords"] = subject_keywords
        elif content_keywords:
            criteria["required_keywords"] = content_keywords[:5]  # Use top 5 content keywords

        if senders:
            # Use most common senders as required, unless there are too many distinct ones
            sender_counts = Counter(senders)
            if len(sender_counts) <= 5:  # If few distinct senders, make them required
                criteria["required_senders"] = [sender for sender, count in sender_counts.most_common(5)]
            else:  # If many distinct senders, maybe identify unusual ones to exclude
                common_senders = set(sender for sender, count in sender_counts.most_common(5))
                all_senders = set(senders)
                rare_senders = list(all_senders - common_senders)
                if rare_senders:
                    criteria["excluded_senders"] = rare_senders

        if categories:
            category_counts = Counter(categories)
            # Use most common categories
            criteria["required_categories"] = [cat for cat, count in category_counts.most_common(3)]

        # Create default actions
        actions = {
            "categorize": "auto-generated",
            "move_to_folder": "filtered",
            "notify_user": False
        }

        # Create the filter
        filter_id = f"gen_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(emails)}"
        description = f"Auto-generated filter based on {len(emails)} emails"
        new_filter = EmailFilter(
            filter_id=filter_id,
            name=name,
            description=description,
            criteria=criteria,
            actions=actions
        )

        # Save the new filter
        if self.filter_db.save_filter(new_filter):
            return new_filter
        else:
            return None

    def _extract_common_keywords(self, texts: List[str], min_frequency: int = 2) -> List[str]:
        """
        Extract common keywords from a list of texts.

        Args:
            texts: A list of text strings to analyze.
            min_frequency: Minimum number of times a word must appear across texts to be included.

        Returns:
            A list of common keywords.
        """
        # Combine all texts into one
        combined_text = " ".join(texts).lower()
        # Remove special characters and split into words
        import re
        words = re.findall(r'\b\w+\b', combined_text)

        # Filter out common stop words and very short words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should', 'may', 'might', 'must', 'can', 'could', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
        filtered_words = [word for word in words if len(word) > 3 and word not in stop_words]

        # Count occurrences
        word_counts = Counter(filtered_words)
        # Return words that appear in at least min_frequency texts
        return [word for word, count in word_counts.items() if count >= min_frequency]

    def prune_filters(self, min_effectiveness: float = 0.3, max_age_days: int = 365) -> int:
        """
        Remove filters that are no longer effective or too old.

        Args:
            min_effectiveness: Minimum effectiveness score for a filter to be kept.
            max_age_days: Maximum age of filters in days.

        Returns:
            Number of filters removed.
        """
        all_filters = self.filter_db.get_all_filters()
        current_time = datetime.now()
        cutoff_date = current_time - timedelta(days=max_age_days)
        filters_to_remove = []

        for filter_obj in all_filters:
            # Check if filter is too old
            if filter_obj.created_date and filter_obj.created_date < cutoff_date:
                filters_to_remove.append(filter_obj.filter_id)
                continue

            # Check if filter is ineffective
            if filter_obj.effectiveness_score < min_effectiveness:
                filters_to_remove.append(filter_obj.filter_id)

        # Remove the filters
        removed_count = 0
        for filter_id in filters_to_remove:
            if self.filter_db.delete_filter(filter_id):
                removed_count += 1
                self.logger.info(f"Removed filter {filter_id} during pruning")

        return removed_count

    def get_filter_statistics(self) -> Dict[str, any]:
        """
        Get statistics about the filter collection.

        Returns:
            A dictionary with filter statistics.
        """
        all_filters = self.filter_db.get_all_filters()
        if not all_filters:
            return {
                "total_filters": 0,
                "average_effectiveness": 0.0,
                "most_common_category": None,
                "filters_by_priority": {}
            }

        effectiveness_scores = [f.effectiveness_score for f in all_filters if f.effectiveness_score is not None]
        categories = [f.actions.get("categorize") for f in all_filters if f.actions.get("categorize")]

        # Calculate stats
        total_filters = len(all_filters)
        avg_effectiveness = sum(effectiveness_scores) / len(effectiveness_scores) if effectiveness_scores else 0.0
        most_common_category = Counter(categories).most_common(1)[0][0] if categories else None

        # Count filters by priority
        priority_counts = defaultdict(int)
        for f in all_filters:
            priority_counts[f.priority] += 1

        return {
            "total_filters": total_filters,
            "average_effectiveness": avg_effectiveness,
            "most_common_category": most_common_category,
            "filters_by_priority": dict(priority_counts)
        }