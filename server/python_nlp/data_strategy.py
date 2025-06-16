"""
Data Collection, Annotation, and Preprocessing Strategy for Email NLP
Comprehensive pipeline for preparing email data for machine learning models
"""

import re
import json
import hashlib
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

@dataclass
class EmailSample:
    """Structured email sample for training and testing"""
    id: str
    subject: str
    content: str
    sender: str
    timestamp: str
    labels: Dict[str, Any]  # Ground truth labels
    metadata: Dict[str, Any]  # Additional context
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class AnnotationSchema:
    """Schema for email annotation"""
    topic: str  # Primary topic/category
    sentiment: str  # positive, negative, neutral
    intent: str  # request, information, complaint, etc.
    urgency: str  # low, medium, high, critical
    entities: List[str]  # Named entities
    keywords: List[str]  # Important keywords
    confidence: float  # Annotator confidence
    annotator_id: str  # For quality tracking

class DataCollectionStrategy:
    """
    Data collection and preprocessing pipeline for email NLP
    Handles data ingestion, cleaning, annotation, and feature engineering
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.annotation_guidelines = self._load_annotation_guidelines()
        self.preprocessing_rules = self._load_preprocessing_rules()
        
    def _load_annotation_guidelines(self) -> Dict[str, Any]:
        """Load annotation guidelines and standards"""
        return {
            "topics": {
                "work_business": ["meeting", "project", "deadline", "budget", "presentation"],
                "personal_family": ["family", "friend", "birthday", "wedding", "vacation"],
                "finance_banking": ["payment", "invoice", "statement", "transaction", "account"],
                "healthcare": ["appointment", "medical", "doctor", "prescription", "health"],
                "travel": ["flight", "hotel", "booking", "itinerary", "trip"],
                "promotions": ["offer", "discount", "sale", "newsletter", "marketing"]
            },
            "sentiment_indicators": {
                "positive": ["thank", "great", "excellent", "pleased", "happy", "wonderful"],
                "negative": ["problem", "issue", "complaint", "disappointed", "frustrated", "urgent"],
                "neutral": ["information", "update", "notice", "regarding", "confirm"]
            },
            "intent_patterns": {
                "request": ["please", "could you", "would you", "can you", "need", "require"],
                "information": ["inform", "update", "notice", "regarding", "fyi", "announce"],
                "complaint": ["problem", "issue", "wrong", "error", "disappointed", "unsatisfied"],
                "question": ["?", "how", "what", "when", "where", "why", "which"],
                "confirmation": ["confirm", "verify", "check", "ensure", "validate"]
            },
            "urgency_signals": {
                "critical": ["emergency", "urgent", "immediate", "asap", "critical", "now"],
                "high": ["soon", "today", "tomorrow", "deadline", "important", "priority"],
                "medium": ["week", "few days", "when possible", "convenient", "schedule"],
                "low": ["whenever", "no rush", "eventually", "future", "later"]
            }
        }
    
    def _load_preprocessing_rules(self) -> Dict[str, Any]:
        """Load text preprocessing rules and patterns"""
        return {
            "email_patterns": {
                "email_addresses": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                "phone_numbers": r'\b\d{3}-\d{3}-\d{4}\b|\b\(\d{3}\)\s*\d{3}-\d{4}\b',
                "urls": r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                "signatures": r'(Best regards|Sincerely|Thanks|Cheers|Best|Regards).*$',
                "forwarded_headers": r'(From:|To:|Subject:|Date:|Sent:).*$'
            },
            "cleanup_rules": {
                "remove_extra_whitespace": True,
                "normalize_case": False,
                "remove_punctuation": False,
                "expand_contractions": True,
                "remove_stopwords": False  # Keep for context
            }
        }
    
    def collect_email_samples(self, source: str, limit: Optional[int] = None) -> List[EmailSample]:
        """
        Collect email samples from various sources
        In production, this would connect to real email APIs
        """
        samples = []
        
        # Simulated diverse email samples for training
        sample_emails = [
            {
                "subject": "Q4 Budget Review Meeting - Urgent Action Required",
                "content": "Hi team, we need to finalize the Q4 budget by tomorrow. Please review the attached spreadsheet and provide your feedback ASAP. This is critical for our quarterly planning.",
                "sender": "manager@company.com",
                "labels": {
                    "topic": "work_business",
                    "sentiment": "neutral",
                    "intent": "request",
                    "urgency": "high"
                }
            },
            {
                "subject": "Happy Birthday! Family Gathering This Weekend",
                "content": "Hey everyone! Don't forget about Dad's birthday party this Saturday. We're meeting at the park at 2 PM. Bring your favorite dish to share!",
                "sender": "sister@gmail.com",
                "labels": {
                    "topic": "personal_family",
                    "sentiment": "positive",
                    "intent": "information",
                    "urgency": "medium"
                }
            },
            {
                "subject": "Account Statement - March 2024",
                "content": "Your monthly account statement is now available. You can view and download it from your online banking portal. Contact us if you have any questions.",
                "sender": "bank@americanbank.com",
                "labels": {
                    "topic": "finance_banking",
                    "sentiment": "neutral",
                    "intent": "information",
                    "urgency": "low"
                }
            },
            {
                "subject": "Appointment Reminder - Dr. Smith Tomorrow",
                "content": "This is a reminder for your appointment with Dr. Smith tomorrow at 3:00 PM. Please arrive 15 minutes early and bring your insurance card.",
                "sender": "clinic@healthcare.com",
                "labels": {
                    "topic": "healthcare",
                    "sentiment": "neutral",
                    "intent": "information",
                    "urgency": "medium"
                }
            },
            {
                "subject": "Flight Booking Confirmation - Trip to Paris",
                "content": "Your flight booking has been confirmed! Flight AA123 departing March 15th at 8:00 AM. Check-in opens 24 hours before departure. Have a great trip!",
                "sender": "bookings@airline.com",
                "labels": {
                    "topic": "travel",
                    "sentiment": "positive",
                    "intent": "confirmation",
                    "urgency": "medium"
                }
            },
            {
                "subject": "Exclusive 50% Off Sale - Limited Time Only!",
                "content": "Don't miss our biggest sale of the year! Get 50% off on all items. Use code SAVE50 at checkout. Offer valid until midnight tonight!",
                "sender": "sales@retailer.com",
                "labels": {
                    "topic": "promotions",
                    "sentiment": "positive",
                    "intent": "request",
                    "urgency": "high"
                }
            }
        ]
        
        for i, email_data in enumerate(sample_emails):
            if limit and i >= limit:
                break
                
            sample = EmailSample(
                id=self._generate_sample_id(email_data["subject"], email_data["sender"]),
                subject=email_data["subject"],
                content=email_data["content"],
                sender=email_data["sender"],
                timestamp=datetime.now().isoformat(),
                labels=email_data["labels"],
                metadata={
                    "source": source,
                    "collection_date": datetime.now().isoformat(),
                    "preprocessed": False
                }
            )
            samples.append(sample)
        
        return samples
    
    def _generate_sample_id(self, subject: str, sender: str) -> str:
        """Generate unique ID for email sample"""
        content = f"{subject}_{sender}_{datetime.now().isoformat()}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def preprocess_email(self, email: EmailSample) -> EmailSample:
        """
        Comprehensive email preprocessing
        Cleans and normalizes email content for NLP processing
        """
        processed_content = self._clean_email_content(email.content)
        processed_subject = self._clean_email_content(email.subject)
        
        # Extract features during preprocessing
        features = self._extract_basic_features(processed_content, processed_subject)
        
        # Update metadata
        email.metadata.update({
            "preprocessed": True,
            "preprocessing_timestamp": datetime.now().isoformat(),
            "original_length": len(email.content),
            "processed_length": len(processed_content),
            "features": features
        })
        
        # Update content
        email.content = processed_content
        email.subject = processed_subject
        
        return email
    
    def _clean_email_content(self, text: str) -> str:
        """Clean and normalize email text"""
        # Remove email signatures
        text = re.sub(self.preprocessing_rules["email_patterns"]["signatures"], "", text, flags=re.MULTILINE | re.IGNORECASE)
        
        # Remove forwarded headers
        text = re.sub(self.preprocessing_rules["email_patterns"]["forwarded_headers"], "", text, flags=re.MULTILINE | re.IGNORECASE)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove extra newlines
        text = re.sub(r'\n+', '\n', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def _extract_basic_features(self, content: str, subject: str) -> Dict[str, Any]:
        """Extract basic features from email text"""
        combined_text = f"{subject} {content}".lower()
        
        features = {
            "word_count": len(content.split()),
            "sentence_count": len(re.split(r'[.!?]+', content)),
            "has_question": '?' in combined_text,
            "has_exclamation": '!' in combined_text,
            "has_numbers": bool(re.search(r'\d+', combined_text)),
            "has_email": bool(re.search(self.preprocessing_rules["email_patterns"]["email_addresses"], combined_text)),
            "has_phone": bool(re.search(self.preprocessing_rules["email_patterns"]["phone_numbers"], combined_text)),
            "has_url": bool(re.search(self.preprocessing_rules["email_patterns"]["urls"], combined_text)),
            "urgency_keywords": self._count_pattern_matches(combined_text, "urgency_signals"),
            "sentiment_keywords": self._count_pattern_matches(combined_text, "sentiment_indicators"),
            "intent_keywords": self._count_pattern_matches(combined_text, "intent_patterns")
        }
        
        return features
    
    def _count_pattern_matches(self, text: str, pattern_category: str) -> Dict[str, int]:
        """Count matches for specific pattern categories"""
        counts = {}
        patterns = self.annotation_guidelines.get(pattern_category, {})
        
        for category, keywords in patterns.items():
            count = sum(1 for keyword in keywords if keyword.lower() in text.lower())
            counts[category] = count
            
        return counts
    
    def annotate_email(self, email: EmailSample, annotator_id: str = "auto", external_analysis_results: Optional[Dict[str, Any]] = None) -> AnnotationSchema:
        """
        Create structured annotation for email sample.
        If `external_analysis_results` (e.g., from NLPEngine) are provided,
        they will be prioritized over internal basic prediction methods.
        Internal predictions serve as a basic fallback for data generation scenarios.
        """
        if external_analysis_results:
            self.logger.info(f"Using external analysis results for email ID: {email.id}")
            # Ensure keys from external_analysis_results match AnnotationSchema fields
            # and provide defaults if some keys are missing.
            topic = external_analysis_results.get('topic', self._predict_topic(email.content + " " + email.subject, is_fallback=True))
            sentiment = external_analysis_results.get('sentiment', self._predict_sentiment(email.content + " " + email.subject, is_fallback=True))
            intent = external_analysis_results.get('intent', self._predict_intent(email.content + " " + email.subject, is_fallback=True))
            urgency = external_analysis_results.get('urgency', self._predict_urgency(email.content + " " + email.subject, is_fallback=True))
            # Keywords and entities might also come from external_analysis_results
            keywords = external_analysis_results.get('keywords', self._extract_keywords(email.content + " " + email.subject))
            entities = external_analysis_results.get('entities', self._extract_entities(email.content)) # Assuming entities are not part of NLPEngine's typical output or need separate extraction.
            confidence = external_analysis_results.get('confidence', 0.9) # Higher confidence if from advanced engine
            annotator_id_suffix = "_external"
        else:
            self.logger.info(f"Using internal basic prediction for email ID: {email.id}")
            topic = self._predict_topic(email.content + " " + email.subject)
            sentiment = self._predict_sentiment(email.content + " " + email.subject)
            intent = self._predict_intent(email.content + " " + email.subject)
            urgency = self._predict_urgency(email.content + " " + email.subject)
            entities = self._extract_entities(email.content)
            keywords = self._extract_keywords(email.content + " " + email.subject)
            confidence = 0.65  # Lower confidence for basic internal prediction
            annotator_id_suffix = "_internal_basic"

        annotation = AnnotationSchema(
            topic=topic,
            sentiment=sentiment,
            intent=intent,
            urgency=urgency,
            entities=entities,
            keywords=keywords,
            confidence=confidence,
            annotator_id=f"{annotator_id}{annotator_id_suffix}"
        )
        
        return annotation
    
    def _predict_topic(self, text: str, is_fallback: bool = False) -> str:
        """Predict topic based on keyword matching. Optionally marked as fallback."""
        prefix = "[Fallback] " if is_fallback else ""
        self.logger.debug(f"{prefix}Predicting topic for text: '{text[:50]}...'")
        text_lower = text.lower()
        topic_scores = {}
        
        for topic, keywords in self.annotation_guidelines["topics"].items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            topic_scores[topic] = score
            
        result = max(topic_scores, key=topic_scores.get) if any(s > 0 for s in topic_scores.values()) else "other"
        self.logger.debug(f"{prefix}Predicted topic: {result}")
        return result
    
    def _predict_sentiment(self, text: str, is_fallback: bool = False) -> str:
        """Predict sentiment based on keyword matching. Optionally marked as fallback."""
        prefix = "[Fallback] " if is_fallback else ""
        self.logger.debug(f"{prefix}Predicting sentiment for text: '{text[:50]}...'")
        text_lower = text.lower()
        sentiment_scores = {}
        
        for sentiment, keywords in self.annotation_guidelines["sentiment_indicators"].items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            sentiment_scores[sentiment] = score

        # Basic tie-breaking: prefer non-neutral if scores are equal
        if sentiment_scores.get("positive", 0) > 0 and sentiment_scores["positive"] == sentiment_scores.get("negative", 0):
            result = "positive" # Or some other logic
        elif sentiment_scores.get("negative", 0) > 0 and sentiment_scores["negative"] == sentiment_scores.get("positive", 0):
            result = "negative"
        else:
            result = max(sentiment_scores, key=sentiment_scores.get) if any(s > 0 for s in sentiment_scores.values()) else "neutral"

        self.logger.debug(f"{prefix}Predicted sentiment: {result}")
        return result
    
    def _predict_intent(self, text: str, is_fallback: bool = False) -> str:
        """Predict intent based on pattern matching. Optionally marked as fallback."""
        prefix = "[Fallback] " if is_fallback else ""
        self.logger.debug(f"{prefix}Predicting intent for text: '{text[:50]}...'")
        text_lower = text.lower()
        intent_scores = {}
        
        for intent, patterns in self.annotation_guidelines["intent_patterns"].items():
            score = sum(1 for pattern in patterns if pattern in text_lower)
            intent_scores[intent] = score
            
        result = max(intent_scores, key=intent_scores.get) if any(s > 0 for s in intent_scores.values()) else "information"
        self.logger.debug(f"{prefix}Predicted intent: {result}")
        return result
    
    def _predict_urgency(self, text: str, is_fallback: bool = False) -> str:
        """Predict urgency based on signal matching. Optionally marked as fallback."""
        prefix = "[Fallback] " if is_fallback else ""
        self.logger.debug(f"{prefix}Predicting urgency for text: '{text[:50]}...'")
        text_lower = text.lower()
        urgency_scores = {}
        
        for urgency, signals in self.annotation_guidelines["urgency_signals"].items():
            score = sum(1 for signal in signals if signal in text_lower)
            urgency_scores[urgency] = score
            
        result = max(urgency_scores, key=urgency_scores.get) if any(s > 0 for s in urgency_scores.values()) else "low"
        self.logger.debug(f"{prefix}Predicted urgency: {result}")
        return result
    
    def _extract_entities(self, text: str) -> List[str]:
        """Extract named entities from text"""
        entities = []
        
        # Extract email addresses
        emails = re.findall(self.preprocessing_rules["email_patterns"]["email_addresses"], text)
        entities.extend([f"EMAIL:{email}" for email in emails])
        
        # Extract phone numbers
        phones = re.findall(self.preprocessing_rules["email_patterns"]["phone_numbers"], text)
        entities.extend([f"PHONE:{phone}" for phone in phones])
        
        # Extract URLs
        urls = re.findall(self.preprocessing_rules["email_patterns"]["urls"], text)
        entities.extend([f"URL:{url}" for url in urls])
        
        # Extract dates (simple pattern)
        dates = re.findall(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', text)
        entities.extend([f"DATE:{date}" for date in dates])
        
        return entities
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text"""
        # Simple keyword extraction based on frequency and importance
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Filter out common words and short words
        stopwords = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "is", "are", "was", "were", "be", "been", "have", "has", "had", "do", "does", "did", "will", "would", "could", "should", "may", "might", "can", "this", "that", "these", "those", "i", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us", "them"}
        
        keywords = [word for word in words if len(word) > 3 and word not in stopwords]
        
        # Return top 10 most frequent keywords
        from collections import Counter
        word_freq = Counter(keywords)
        return [word for word, _ in word_freq.most_common(10)]
    
    def create_training_dataset(self, samples: List[EmailSample]) -> Dict[str, Any]:
        """Create structured training dataset from email samples"""
        if not samples:
            self.logger.warning("No email samples provided for dataset creation")
            return {
                "metadata": {
                    "creation_date": datetime.now().isoformat(),
                    "sample_count": 0,
                    "version": "1.0",
                    "schema": "email_nlp_v1"
                },
                "samples": [],
                "statistics": {}
            }
        
        self.logger.info(f"Creating training dataset from {len(samples)} samples")
        dataset = {
            "metadata": {
                "creation_date": datetime.now().isoformat(),
                "sample_count": len(samples),
                "version": "1.0",
                "schema": "email_nlp_v1"
            },
            "samples": [],
            "statistics": self._calculate_dataset_statistics(samples)
        }
        
        for sample in samples:
            # Preprocess sample
            processed_sample = self.preprocess_email(sample)
            
            # Create annotation
            annotation = self.annotate_email(processed_sample)
            
            dataset["samples"].append({
                "sample": processed_sample.to_dict(),
                "annotation": asdict(annotation)
            })
        
        return dataset
    
    def _calculate_dataset_statistics(self, samples: List[EmailSample]) -> Dict[str, Any]:
        """Calculate statistics for the dataset"""
        if not samples:
            return {}
        
        word_counts = [len(sample.content.split()) for sample in samples]
        
        return {
            "total_samples": len(samples),
            "avg_word_count": sum(word_counts) / len(word_counts),
            "min_word_count": min(word_counts),
            "max_word_count": max(word_counts),
            "unique_senders": len(set(sample.sender for sample in samples))
        }
    
    def export_dataset(self, dataset: Dict[str, Any], filepath: str) -> None:
        """Export dataset to JSON file"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(dataset, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Dataset exported successfully to {filepath}")
        except IOError as e:
            self.logger.error(f"Failed to export dataset to {filepath}: {e}")
            raise
        except json.JSONEncodeError as e:
            self.logger.error(f"Failed to encode dataset to JSON: {e}")
            raise
    
    def load_dataset(self, filepath: str) -> Dict[str, Any]:
        """Load dataset from JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                dataset = json.load(f)
            self.logger.info(f"Dataset loaded successfully from {filepath}")
            return dataset
        except FileNotFoundError:
            self.logger.error(f"Dataset file not found: {filepath}")
            raise
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to decode JSON from {filepath}: {e}")
            raise
        except IOError as e:
            self.logger.error(f"Failed to read dataset from {filepath}: {e}")
            raise

def main():
    """Example usage of data collection strategy"""
    strategy = DataCollectionStrategy()
    
    # Collect email samples
    samples = strategy.collect_email_samples("demo_source", limit=10)
    print(f"Collected {len(samples)} email samples")
    
    # Create training dataset
    dataset = strategy.create_training_dataset(samples)
    print(f"Created dataset with {len(dataset['samples'])} processed samples")
    
    # Export dataset
    strategy.export_dataset(dataset, "email_training_dataset.json")
    print("Dataset exported successfully")

if __name__ == "__main__":
    main()