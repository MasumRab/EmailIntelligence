"""
Module for evaluating filter criteria against email content.
"""

import re
from typing import Any, Dict
from .filter_models import EmailFilter


def evaluate_filter_criteria(email: Dict[str, Any], filter_obj: EmailFilter) -> bool:
    """
    Evaluates whether an email matches the criteria specified in a filter.

    Args:
        email: A dictionary containing email data.
        filter_obj: An EmailFilter object containing the criteria to match.

    Returns:
        True if the email matches the filter criteria, False otherwise.
    """
    criteria = filter_obj.criteria

    # Check for required keywords in subject or content
    if "required_keywords" in criteria:
        required_keywords = criteria["required_keywords"]
        email_text = f"{email.get('subject', '')} {email.get('content', '')}".lower()
        for keyword in required_keywords:
            if keyword.lower() not in email_text:
                return False

    # Check for excluded keywords in subject or content
    if "excluded_keywords" in criteria:
        excluded_keywords = criteria["excluded_keywords"]
        email_text = f"{email.get('subject', '')} {email.get('content', '')}".lower()
        for keyword in excluded_keywords:
            if keyword.lower() in email_text:
                return False

    # Check sender criteria
    if "required_senders" in criteria:
        required_senders = set(criteria["required_senders"])
        sender = email.get("sender_email", "").lower()
        if sender not in required_senders:
            return False

    if "excluded_senders" in criteria:
        excluded_senders = set(criteria["excluded_senders"])
        sender = email.get("sender_email", "").lower()
        if sender in excluded_senders:
            return False

    # Check recipient criteria
    if "required_recipients" in criteria:
        required_recipients = set(criteria["required_recipients"])
        recipients = [r.lower() for r in email.get("recipients", [])]
        if not any(recipient in required_recipients for recipient in recipients):
            return False

    if "excluded_recipients" in criteria:
        excluded_recipients = set(criteria["excluded_recipients"])
        recipients = [r.lower() for r in email.get("recipients", [])]
        if any(recipient in excluded_recipients for recipient in recipients):
            return False

    # Check category criteria
    if "required_categories" in criteria:
        required_categories = set(criteria["required_categories"])
        category = email.get("category", "")
        if category not in required_categories:
            return False

    if "excluded_categories" in criteria:
        excluded_categories = set(criteria["excluded_categories"])
        category = email.get("category", "")
        if category in excluded_categories:
            return False

    # Check date/time criteria
    if "date_range" in criteria:
        date_range = criteria["date_range"]
        email_time_str = email.get("time", "")
        if email_time_str:
            try:
                from datetime import datetime
                email_time = datetime.fromisoformat(email_time_str.replace('Z', '+00:00'))
                if "start_date" in date_range:
                    start_date = datetime.fromisoformat(date_range["start_date"])
                    if email_time < start_date:
                        return False
                if "end_date" in date_range:
                    end_date = datetime.fromisoformat(date_range["end_date"])
                    if email_time > end_date:
                        return False
            except ValueError:
                # If date parsing fails, log and continue
                pass

    # Check email size
    if "size_range" in criteria:
        size_range = criteria["size_range"]
        email_size = email.get("size", 0)
        if "min_size" in size_range and email_size < size_range["min_size"]:
            return False
        if "max_size" in size_range and email_size > size_range["max_size"]:
            return False

    # Check priority level
    if "priority_levels" in criteria:
        priority_levels = set(criteria["priority_levels"])
        priority = email.get("priority", "")
        if priority not in priority_levels:
            return False

    return True