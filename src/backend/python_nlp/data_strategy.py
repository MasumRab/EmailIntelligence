"""
Data Collection and Preprocessing for Email NLP Models.

This module provides a comprehensive pipeline for collecting, annotating, and
preprocessing email data to prepare it for training machine learning models.
It includes strategies for data cleaning, feature extraction, and dataset creation.
"""

import hashlib
import json
import logging
import re
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class EmailSample:
    """
    Represents a structured email sample for training and testing.

    Attributes:
        id: A unique identifier for the email sample.
        subject: The subject line of the email.
        content: The body content of the email.
        sender: The email address of the sender.
        timestamp: The timestamp when the email was sent or collected.
        labels: A dictionary of ground truth labels for the email.
        metadata: A dictionary for storing additional context or metadata.
    """

    id: str
    subject: str
    content: str
    sender: str
    timestamp: str
    labels: Dict[str, Any]
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """Converts the EmailSample object to a dictionary."""
        return asdict(self)


@dataclass
class AnnotationSchema:
    """
    Defines the schema for annotating an email.

    Attributes:
        topic: The primary topic or category of the email.
        sentiment: The sentiment of the email (e.g., 'positive', 'negative').
        intent: The perceived intent of the email (e.g., 'request', 'complaint').
        urgency: The urgency level of the email (e.g., 'low', 'high').
        entities: A list of named entities extracted from the email.
        keywords: A list of important keywords from the email.
        confidence: The confidence score of the annotation.
        annotator_id: The ID of the annotator for quality tracking.
    """

    topic: str
    sentiment: str
    intent: str
    urgency: str
    entities: List[str]
    keywords: List[str]
    confidence: float
    annotator_id: str


class DataCollectionStrategy:
    """
    Implements a pipeline for email data collection and preprocessing.

    This class handles the entire workflow from data ingestion and cleaning to
    annotation and feature engineering, preparing the data for NLP models.
    """

    def __init__(self):
        """Initializes the DataCollectionStrategy."""
        self.logger = logging.getLogger(__name__)
        self.annotation_guidelines = self._load_annotation_guidelines()
        self.preprocessing_rules = self._load_preprocessing_rules()

    def _load_annotation_guidelines(self) -> Dict[str, Any]:
        """Loads internal guidelines and standards for annotation."""
        return {
            "topics": {
                "work_business": ["meeting", "project", "deadline", "budget"],
                "personal_family": ["family", "friend", "birthday", "wedding"],
                "finance_banking": ["payment", "invoice", "statement", "transaction"],
                "healthcare": ["appointment", "medical", "doctor", "prescription"],
                "travel": ["flight", "hotel", "booking", "itinerary"],
                "promotions": ["offer", "discount", "sale", "newsletter"],
            },
            "sentiment_indicators": {
                "positive": ["thank", "great", "excellent", "pleased", "happy"],
                "negative": ["problem", "issue", "complaint", "disappointed"],
                "neutral": ["information", "update", "notice", "regarding"],
            },
            "intent_patterns": {
                "request": ["please", "could you", "need", "require"],
                "information": ["inform", "update", "notice", "fyi"],
                "complaint": ["problem", "issue", "wrong", "error"],
                "question": ["?", "how", "what", "when", "where"],
                "confirmation": ["confirm", "verify", "check", "ensure"],
            },
            "urgency_signals": {
                "critical": ["emergency", "urgent", "immediate", "asap"],
                "high": ["soon", "today", "tomorrow", "deadline"],
                "medium": ["week", "few days", "when possible"],
                "low": ["whenever", "no rush", "eventually"],
            },
        }

    def _load_preprocessing_rules(self) -> Dict[str, Any]:
        """Loads rules and patterns for text preprocessing."""
        return {
            "email_patterns": {
                "email_addresses": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
                "phone_numbers": r"\b\d{3}-\d{3}-\d{4}\b|\b\(\d{3}\)\s*\d{3}-\d{4}\b",
                "urls": r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
                "signatures": r"(Best regards|Sincerely|Thanks|Cheers|Best|Regards).*$",
                "forwarded_headers": r"(From:|To:|Subject:|Date:|Sent:).*$",
            },
            "cleanup_rules": {
                "remove_extra_whitespace": True,
                "normalize_case": False,
                "remove_punctuation": False,
                "expand_contractions": True,
                "remove_stopwords": False,
            },
        }

    def collect_email_samples(self, source: str, limit: Optional[int] = None) -> List[EmailSample]:
        """
        Collects email samples from a given source.

        In a production environment, this method would connect to real email APIs.
        Here, it uses a simulated list of diverse email samples for demonstration.

        Args:
            source: The source of the email data (e.g., 'gmail', 'outlook').
            limit: The maximum number of email samples to collect.

        Returns:
            A list of EmailSample objects.
        """
        samples = []
        sample_emails = [
            {
                "subject": "Q4 Budget Review Meeting - Urgent Action Required",
                "content": "Hi team, we need to finalize the Q4 budget by tomorrow. Please review the attached spreadsheet and provide your feedback ASAP. This is critical for our quarterly planning.",
                "sender": "manager@company.com",
                "labels": {
                    "topic": "work_business",
                    "sentiment": "neutral",
                    "intent": "request",
                    "urgency": "high",
                },
            },
            {
                "subject": "Happy Birthday! Family Gathering This Weekend",
                "content": "Hey everyone! Don't forget about Dad's birthday party this Saturday. We're meeting at the park at 2 PM. Bring your favorite dish to share!",
                "sender": "sister@gmail.com",
                "labels": {
                    "topic": "personal_family",
                    "sentiment": "positive",
                    "intent": "information",
                    "urgency": "medium",
                },
            },
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
                    "preprocessed": False,
                },
            )
            samples.append(sample)

        return samples

    def _generate_sample_id(self, subject: str, sender: str) -> str:
        """Generates a unique ID for an email sample using a hash."""
        content = f"{subject}_{sender}_{datetime.now().isoformat()}"
        return hashlib.sha256(content.encode()).hexdigest()[:12]

    def preprocess_email(self, email: EmailSample) -> EmailSample:
        """
        Performs comprehensive preprocessing on a single email sample.

        This involves cleaning the text, normalizing content, and extracting
        basic features.

        Args:
            email: The EmailSample object to preprocess.

        Returns:
            The preprocessed EmailSample object with updated content and metadata.
        """
        processed_content = self._clean_email_content(email.content)
        processed_subject = self._clean_email_content(email.subject)
        features = self._extract_basic_features(processed_content, processed_subject)

        email.metadata.update(
            {
                "preprocessed": True,
                "preprocessing_timestamp": datetime.now().isoformat(),
                "original_length": len(email.content),
                "processed_length": len(processed_content),
                "features": features,
            }
        )

        email.content = processed_content
        email.subject = processed_subject
        return email

    def _clean_email_content(self, text: str) -> str:
        """Cleans and normalizes the text content of an email."""
        text = re.sub(
            self.preprocessing_rules["email_patterns"]["signatures"],
            "",
            text,
            flags=re.MULTILINE | re.IGNORECASE,
        )
        text = re.sub(
            self.preprocessing_rules["email_patterns"]["forwarded_headers"],
            "",
            text,
            flags=re.MULTILINE | re.IGNORECASE,
        )
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"\n+", "\n", text)
        text = text.strip()
        return text

    def _extract_basic_features(self, content: str, subject: str) -> Dict[str, Any]:
        """Extracts a set of basic features from the email text."""
        combined_text = f"{subject} {content}".lower()
        features = {
            "word_count": len(content.split()),
            "sentence_count": len(re.split(r"[.!?]+", content)),
            "has_question": "?" in combined_text,
            "has_exclamation": "!" in combined_text,
            "has_numbers": bool(re.search(r"\d+", combined_text)),
            "has_email": bool(
                re.search(
                    self.preprocessing_rules["email_patterns"]["email_addresses"], combined_text
                )
            ),
            "has_phone": bool(
                re.search(
                    self.preprocessing_rules["email_patterns"]["phone_numbers"], combined_text
                )
            ),
            "has_url": bool(
                re.search(self.preprocessing_rules["email_patterns"]["urls"], combined_text)
            ),
            "urgency_keywords": self._count_pattern_matches(combined_text, "urgency_signals"),
            "sentiment_keywords": self._count_pattern_matches(
                combined_text, "sentiment_indicators"
            ),
            "intent_keywords": self._count_pattern_matches(combined_text, "intent_patterns"),
        }
        return features

    def _count_pattern_matches(self, text: str, pattern_category: str) -> Dict[str, int]:
        """Counts keyword matches for a specific pattern category."""
        counts = {}
        patterns = self.annotation_guidelines.get(pattern_category, {})
        for category, keywords in patterns.items():
            count = sum(1 for keyword in keywords if keyword.lower() in text.lower())
            counts[category] = count
        return counts

    def annotate_email(
        self,
        email: EmailSample,
        annotator_id: str = "auto",
        external_analysis_results: Optional[Dict[str, Any]] = None,
    ) -> AnnotationSchema:
        """
        Creates a structured annotation for an email sample.

        It prioritizes external analysis results (e.g., from a trained model)
        but can fall back to internal rule-based predictions.

        Args:
            email: The email sample to annotate.
            annotator_id: The identifier for the annotator (e.g., 'human', 'auto').
            external_analysis_results: Optional dictionary of analysis results
                from an external source.

        Returns:
            An AnnotationSchema object containing the structured annotations.
        """
        if external_analysis_results:
            self.logger.info(f"Using external analysis results for email ID: {email.id}")
            topic = external_analysis_results.get(
                "topic", self._predict_topic(email.content, is_fallback=True)
            )
            sentiment = external_analysis_results.get(
                "sentiment", self._predict_sentiment(email.content, is_fallback=True)
            )
            intent = external_analysis_results.get(
                "intent", self._predict_intent(email.content, is_fallback=True)
            )
            urgency = external_analysis_results.get(
                "urgency", self._predict_urgency(email.content, is_fallback=True)
            )
            keywords = external_analysis_results.get(
                "keywords", self._extract_keywords(email.content)
            )
            entities = external_analysis_results.get(
                "entities", self._extract_entities(email.content)
            )
            confidence = external_analysis_results.get("confidence", 0.9)
            annotator_id_suffix = "_external"
        else:
            self.logger.info(f"Using internal basic prediction for email ID: {email.id}")
            topic = self._predict_topic(email.content)
            sentiment = self._predict_sentiment(email.content)
            intent = self._predict_intent(email.content)
            urgency = self._predict_urgency(email.content)
            entities = self._extract_entities(email.content)
            keywords = self._extract_keywords(email.content)
            confidence = 0.65
            annotator_id_suffix = "_internal_basic"

        return AnnotationSchema(
            topic=topic,
            sentiment=sentiment,
            intent=intent,
            urgency=urgency,
            entities=entities,
            keywords=keywords,
            confidence=confidence,
            annotator_id=f"{annotator_id}{annotator_id_suffix}",
        )

    def _predict_topic(self, text: str, is_fallback: bool = False) -> str:
        """Predicts the topic of a text based on keyword matching."""
        prefix = "[Fallback] " if is_fallback else ""
        self.logger.debug(f"{prefix}Predicting topic for text: '{text[:50]}...'")
        text_lower = text.lower()
        topic_scores = {}
        for topic, keywords in self.annotation_guidelines["topics"].items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            topic_scores[topic] = score
        result = max(topic_scores, key=topic_scores.get) if any(topic_scores.values()) else "other"
        self.logger.debug(f"{prefix}Predicted topic: {result}")
        return result

    def _predict_sentiment(self, text: str, is_fallback: bool = False) -> str:
        """Predicts the sentiment of a text based on keyword matching."""
        prefix = "[Fallback] " if is_fallback else ""
        self.logger.debug(f"{prefix}Predicting sentiment for text: '{text[:50]}...'")
        text_lower = text.lower()
        sentiment_scores = {}
        for sentiment, keywords in self.annotation_guidelines["sentiment_indicators"].items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            sentiment_scores[sentiment] = score
        if sentiment_scores.get("positive", 0) > 0 and sentiment_scores[
            "positive"
        ] == sentiment_scores.get("negative", 0):
            result = "positive"
        elif sentiment_scores.get("negative", 0) > 0 and sentiment_scores[
            "negative"
        ] == sentiment_scores.get("positive", 0):
            result = "negative"
        else:
            result = (
                max(sentiment_scores, key=sentiment_scores.get)
                if any(sentiment_scores.values())
                else "neutral"
            )
        self.logger.debug(f"{prefix}Predicted sentiment: {result}")
        return result

    def _predict_intent(self, text: str, is_fallback: bool = False) -> str:
        """Predicts the intent of a text based on pattern matching."""
        prefix = "[Fallback] " if is_fallback else ""
        self.logger.debug(f"{prefix}Predicting intent for text: '{text[:50]}...'")
        text_lower = text.lower()
        intent_scores = {}
        for intent, patterns in self.annotation_guidelines["intent_patterns"].items():
            score = sum(1 for pattern in patterns if pattern in text_lower)
            intent_scores[intent] = score
        result = (
            max(intent_scores, key=intent_scores.get)
            if any(intent_scores.values())
            else "information"
        )
        self.logger.debug(f"{prefix}Predicted intent: {result}")
        return result

    def _predict_urgency(self, text: str, is_fallback: bool = False) -> str:
        """Predicts the urgency of a text based on signal matching."""
        prefix = "[Fallback] " if is_fallback else ""
        self.logger.debug(f"{prefix}Predicting urgency for text: '{text[:50]}...'")
        text_lower = text.lower()
        urgency_scores = {}
        for urgency, signals in self.annotation_guidelines["urgency_signals"].items():
            score = sum(1 for signal in signals if signal in text_lower)
            urgency_scores[urgency] = score
        result = (
            max(urgency_scores, key=urgency_scores.get) if any(urgency_scores.values()) else "low"
        )
        self.logger.debug(f"{prefix}Predicted urgency: {result}")
        return result

    def _extract_entities(self, text: str) -> List[str]:
        """Extracts named entities (email, phone, URL, date) from text."""
        entities = []
        emails = re.findall(self.preprocessing_rules["email_patterns"]["email_addresses"], text)
        entities.extend([f"EMAIL:{email}" for email in emails])
        phones = re.findall(self.preprocessing_rules["email_patterns"]["phone_numbers"], text)
        entities.extend([f"PHONE:{phone}" for phone in phones])
        urls = re.findall(self.preprocessing_rules["email_patterns"]["urls"], text)
        entities.extend([f"URL:{url}" for url in urls])
        dates = re.findall(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b", text)
        entities.extend([f"DATE:{date}" for date in dates])
        return entities

    def _extract_keywords(self, text: str) -> List[str]:
        """Extracts important keywords from text using frequency analysis."""
        words = re.findall(r"\b\w+\b", text.lower())
        stopwords = {
            "the",
            "a",
            "an",
            "and",
            "in",
            "on",
            "at",
            "to",
            "for",
            "of",
            "with",
            "is",
            "are",
            "was",
            "were",
            "this",
            "that",
            "i",
            "you",
            "we",
            "they",
        }
        keywords = [word for word in words if len(word) > 3 and word not in stopwords]
        from collections import Counter

        word_freq = Counter(keywords)
        return [word for word, _ in word_freq.most_common(10)]

    def create_training_dataset(self, samples: List[EmailSample]) -> Dict[str, Any]:
        """
        Creates a structured training dataset from a list of email samples.

        Args:
            samples: A list of EmailSample objects.

        Returns:
            A dictionary representing the complete training dataset.
        """
        if not samples:
            self.logger.warning("No email samples provided for dataset creation")
            return {
                "metadata": {"creation_date": datetime.now().isoformat(), "sample_count": 0},
                "samples": [],
                "statistics": {},
            }

        self.logger.info(f"Creating training dataset from {len(samples)} samples")
        dataset = {
            "metadata": {
                "creation_date": datetime.now().isoformat(),
                "sample_count": len(samples),
                "version": "1.0",
                "schema": "email_nlp_v1",
            },
            "samples": [],
            "statistics": self._calculate_dataset_statistics(samples),
        }

        for sample in samples:
            processed_sample = self.preprocess_email(sample)
            annotation = self.annotate_email(processed_sample)
            dataset["samples"].append(
                {"sample": processed_sample.to_dict(), "annotation": asdict(annotation)}
            )

        return dataset

    def _calculate_dataset_statistics(self, samples: List[EmailSample]) -> Dict[str, Any]:
        """Calculates and returns statistics for the dataset."""
        if not samples:
            return {}
        word_counts = [len(sample.content.split()) for sample in samples]
        return {
            "total_samples": len(samples),
            "avg_word_count": sum(word_counts) / len(word_counts),
            "min_word_count": min(word_counts),
            "max_word_count": max(word_counts),
            "unique_senders": len(set(sample.sender for sample in samples)),
        }

    def export_dataset(self, dataset: Dict[str, Any], filepath: str) -> None:
        """
        Exports the dataset to a JSON file.

        Args:
            dataset: The dataset dictionary to export.
            filepath: The path to the output JSON file.
        """
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(dataset, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Dataset exported successfully to {filepath}")
        except (IOError, json.JSONEncodeError) as e:
            self.logger.error(f"Failed to export dataset to {filepath}: {e}")
            raise

    def load_dataset(self, filepath: str) -> Dict[str, Any]:
        """
        Loads a dataset from a JSON file.

        Args:
            filepath: The path to the input JSON file.

        Returns:
            The loaded dataset as a dictionary.
        """
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                dataset = json.load(f)
            self.logger.info(f"Dataset loaded successfully from {filepath}")
            return dataset
        except (FileNotFoundError, IOError, json.JSONDecodeError) as e:
            self.logger.error(f"Failed to load dataset from {filepath}: {e}")
            raise


def main():
    """Demonstrates the usage of the DataCollectionStrategy."""
    strategy = DataCollectionStrategy()
    samples = strategy.collect_email_samples("demo_source", limit=10)
    print(f"Collected {len(samples)} email samples")
    dataset = strategy.create_training_dataset(samples)
    print(f"Created dataset with {len(dataset['samples'])} processed samples")
    strategy.export_dataset(dataset, "email_training_dataset.json")
    print("Dataset exported successfully")


if __name__ == "__main__":
    main()
