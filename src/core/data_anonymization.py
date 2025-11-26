"""
Data anonymization utilities for the Email Intelligence Platform.
Used for creating anonymized datasets for testing and development.
"""

import re
import hashlib
from typing import Dict, Any, List
from faker import Faker


class DataAnonymizer:
    """
    Service for anonymizing sensitive data in datasets.
    """

    def __init__(self):
        self.fake = Faker()
        # Use consistent seed for reproducible anonymization in testing
        Faker.seed(42)

    def anonymize_email_content(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Anonymize sensitive content in an email record.
        
        Args:
            email_data: Email data dictionary to anonymize
            
        Returns:
            Dict[str, Any]: Anonymized email data
        """
        anonymized_email = email_data.copy()
        
        # Anonymize sender information
        if "sender_email" in anonymized_email:
            anonymized_email["sender_email"] = self._anonymize_email(anonymized_email["sender_email"])
        
        if "sender" in anonymized_email:
            anonymized_email["sender"] = self.fake.name()
        
        # Anonymize subject
        if "subject" in anonymized_email:
            anonymized_email["subject"] = self._anonymize_text(anonymized_email["subject"])
        
        # Anonymize content
        if "content" in anonymized_email:
            anonymized_email["content"] = self._anonymize_text(anonymized_email["content"])
        
        # Anonymize other content fields
        if "content_html" in anonymized_email:
            anonymized_email["content_html"] = self._anonymize_text(anonymized_email["content_html"])
        
        # Anonymize any analysis metadata that might contain sensitive info
        if "analysis_metadata" in anonymized_email:
            if isinstance(anonymized_email["analysis_metadata"], dict):
                anon_meta = anonymized_email["analysis_metadata"].copy()
                # Anonymize specific fields that might contain sensitive info
                for key, value in anon_meta.items():
                    if isinstance(value, str):
                        anon_meta[key] = self._anonymize_text(value)
                anonymized_email["analysis_metadata"] = anon_meta
        
        return anonymized_email

    def anonymize_user_data(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Anonymize sensitive information in user data.
        
        Args:
            user_data: User data dictionary to anonymize
            
        Returns:
            Dict[str, Any]: Anonymized user data
        """
        anonymized_user = user_data.copy()
        
        if "username" in anonymized_user:
            # Create a hashed version based on original username to maintain uniqueness
            hash_obj = hashlib.sha256(anonymized_user["username"].encode())
            anonymized_user["username"] = f"user_{hash_obj.hexdigest()[:12]}"
        
        if "email" in anonymized_user:
            anonymized_user["email"] = self._anonymize_email(anonymized_user["email"])
            
        return anonymized_user

    def anonymize_dataset(self, dataset: List[Dict[str, Any]], data_type: str = "email") -> List[Dict[str, Any]]:
        """
        Anonymize an entire dataset of emails, users, or other data types.
        
        Args:
            dataset: List of data records to anonymize
            data_type: Type of data ('email', 'user', etc.)
            
        Returns:
            List[Dict[str, Any]]: Anonymized dataset
        """
        anonymized_dataset = []
        
        for record in dataset:
            if data_type == "email":
                anonymized_record = self.anonymize_email_content(record)
            elif data_type == "user":
                anonymized_record = self.anonymize_user_data(record)
            else:
                # For other data types, apply general anonymization
                anonymized_record = self._anonymize_general_data(record)
                
            anonymized_dataset.append(anonymized_record)
            
        return anonymized_dataset

    def _anonymize_email(self, email: str) -> str:
        """
        Anonymize an email address while preserving its format.
        
        Args:
            email: Email address to anonymize
            
        Returns:
            str: Anonymized email address
        """
        # Extract the domain
        if "@" in email:
            local_part, domain = email.split("@", 1)
            # Hash the local part to preserve uniqueness but hide the actual value
            hash_obj = hashlib.sha256(local_part.encode())
            anonymous_local = hash_obj.hexdigest()[:8]  # Use first 8 chars of hash
            return f"{anonymous_local}@{domain}"
        else:
            # If it's not a valid email format, just return a fake one
            return self.fake.email()

    def _anonymize_text(self, text: str) -> str:
        """
        Anonymize text content by replacing sensitive information.
        
        Args:
            text: Text to anonymize
            
        Returns:
            str: Anonymized text
        """
        if not text:
            return text
            
        # Replace email addresses with fake ones
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        text = re.sub(email_pattern, lambda m: self.fake.email(), text)
        
        # Replace phone numbers with fake ones
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        text = re.sub(phone_pattern, lambda m: self.fake.phone_number(), text)
        
        # Replace names with fake ones
        # This is a basic implementation - in a real system, you'd want more sophisticated NER
        # For demo purposes, we'll look for common name patterns
        words = text.split()
        anonymized_words = []
        
        for word in words:
            # Basic heuristic: capitalized words might be names
            if word[0].isupper() and len(word) > 2 and word.lower() not in ['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'its', 'may', 'new', 'now', 'old', 'see', 'two', 'who', 'boy', 'did', 'man', 'men', 'run', 'too', 'any', 'big', 'end', 'far', 'got', 'hot', 'let', 'lot', 'put', 'say', 'she', 'try', 'use', 'way', 'win', 'boy', 'age', 'art', 'car', 'day', 'eye', 'fun', 'guy', 'ice', 'job', 'key', 'law', 'map', 'mom', 'net', 'oil', 'pay', 'sea', 'tax', 'tip', 'war', 'web', 'win', 'act', 'arm', 'bay', 'bus', 'cup', 'cut', 'dad', 'die', 'dog', 'dry', 'due', 'eat', 'fan', 'fat', 'fix', 'fly', 'gas', 'hit', 'job', 'leg', 'lie', 'low', 'map', 'mix', 'net', 'oil', 'pay', 'pen', 'pet', 'pie', 'pin', 'sea', 'set', 'sex', 'she', 'sky', 'tax', 'tip', 'top', 'try', 'use', 'war', 'wet', 'win', 'age', 'art', 'bay', 'bed', 'box', 'bus', 'day', 'die', 'dog', 'dry', 'due', 'ear', 'eat', 'end', 'eye', 'fan', 'fat', 'fix', 'fly', 'fun', 'guy', 'gym', 'hit', 'ice', 'job', 'key', 'law', 'leg', 'lie', 'lot', 'low', 'map', 'mix', 'net', 'new', 'oil', 'old', 'pay', 'pen', 'pet', 'pie', 'pin', 'put', 'sea', 'set', 'sex', 'she', 'sky', 'tax', 'tip', 'top', 'try', 'use', 'war', 'web', 'wet', 'win', 'win']:
                # Replace with a fake name
                anonymized_words.append(self.fake.first_name())
            else:
                anonymized_words.append(word)
        
        text = " ".join(anonymized_words)
        
        return text

    def _anonymize_general_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply general anonymization to any data dictionary.
        
        Args:
            data: Data dictionary to anonymize
            
        Returns:
            Dict[str, Any]: Anonymized data
        """
        anonymized_data = data.copy()
        
        for key, value in anonymized_data.items():
            if isinstance(value, str):
                anonymized_data[key] = self._anonymize_text(value)
            elif isinstance(value, dict):
                anonymized_data[key] = self._anonymize_general_data(value)
            elif isinstance(value, list):
                anonymized_data[key] = [
                    self._anonymize_text(item) if isinstance(item, str) 
                    else item for item in value
                ]
        
        return anonymized_data


# Global instance for easy access
# In a real application, you would manage this differently to avoid global state
_anonymizer = None


def get_anonymizer() -> DataAnonymizer:
    """
    Get the global anonymizer instance.
    
    Returns:
        DataAnonymizer: The anonymizer instance
    """
    global _anonymizer
    if _anonymizer is None:
        _anonymizer = DataAnonymizer()
    return _anonymizer


def anonymize_email_dataset(emails: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Convenience function to anonymize a list of email records.
    
    Args:
        emails: List of email records to anonymize
        
    Returns:
        List[Dict[str, Any]]: Anonymized email records
    """
    anonymizer = get_anonymizer()
    return anonymizer.anonymize_dataset(emails, "email")


def anonymize_user_dataset(users: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Convenience function to anonymize a list of user records.
    
    Args:
        users: List of user records to anonymize
        
    Returns:
        List[Dict[str, Any]]: Anonymized user records
    """
    anonymizer = get_anonymizer()
    return anonymizer.anonymize_dataset(users, "user")