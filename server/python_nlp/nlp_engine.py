#!/usr/bin/env python3
"""
Enhanced NLP Engine for Gmail AI Email Management.

This module provides advanced natural language processing capabilities with multiple AI models
and validation for analyzing email content.
"""

import argparse
import json
import logging
import os
import re
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

from server.python_nlp.text_utils import clean_text
from server.python_nlp.action_item_extractor import ActionItemExtractor # Import ActionItemExtractor
from .analysis_components.sentiment_model import SentimentModel
from .analysis_components.topic_model import TopicModel
from .analysis_components.intent_model import IntentModel
from .analysis_components.urgency_model import UrgencyModel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Try to import optional dependencies
try:
    import nltk
    from textblob import TextBlob
    import joblib
    HAS_NLTK = True
    HAS_SKLEARN_AND_JOBLIB = True
except ImportError:
    HAS_NLTK = False
    HAS_SKLEARN_AND_JOBLIB = False
    print(
        "Warning: NLTK, scikit-learn or joblib not available. "
        "Model loading and/or advanced NLP features will be disabled.",
        file=sys.stderr
    )

# Define paths for pre-trained models
# MODEL_DIR = os.getenv("NLP_MODEL_DIR", os.path.dirname(__file__)) # Moved to __init__
# SENTIMENT_MODEL_PATH = os.path.join(MODEL_DIR, "sentiment_model.pkl")
# TOPIC_MODEL_PATH = os.path.join(MODEL_DIR, "topic_model.pkl")
# INTENT_MODEL_PATH = os.path.join(MODEL_DIR, "intent_model.pkl")
# URGENCY_MODEL_PATH = os.path.join(MODEL_DIR, "urgency_model.pkl")


class NLPEngine:
    """
    Natural Language Processing engine for email analysis.
    
    This class provides methods for analyzing email content using various NLP techniques,
    including sentiment analysis, topic identification, intent detection, and urgency assessment.
    """
    
    def __init__(self):
        """Initialize the NLP engine and load required models."""

        # Define model paths dynamically using env var at instantiation time
        model_dir = os.getenv("NLP_MODEL_DIR", os.path.dirname(__file__))
        self.sentiment_model_path = os.path.join(model_dir, "sentiment_model.pkl")
        self.topic_model_path = os.path.join(model_dir, "topic_model.pkl")
        self.intent_model_path = os.path.join(model_dir, "intent_model.pkl")
        self.urgency_model_path = os.path.join(model_dir, "urgency_model.pkl")

        # Initialize stop words if NLTK is available
        if HAS_NLTK:
            try:
                nltk.data.find('corpora/stopwords')
            except LookupError:
                logger.info("NLTK 'stopwords' resource not found. Downloading...")
                nltk.download('stopwords', quiet=True)
            self.stop_words = set(nltk.corpus.stopwords.words('english'))
        else:
            self.stop_words = set()

        # Initialize model attributes
        self.sentiment_model = None
        self.topic_model = None
        self.intent_model = None
        self.urgency_model = None

        # Initialize ActionItemExtractor
        self.action_item_extractor = ActionItemExtractor()

        # Load models if dependencies are available
        # These attributes self.sentiment_model, self.topic_model etc. are the actual model objects (e.g. from joblib)
        _sentiment_model_obj = None
        _topic_model_obj = None
        _intent_model_obj = None
        _urgency_model_obj = None

        if HAS_SKLEARN_AND_JOBLIB:
            logger.info("Attempting to load NLP models...")
            _sentiment_model_obj = self._load_model(self.sentiment_model_path)
            _topic_model_obj = self._load_model(self.topic_model_path)
            _intent_model_obj = self._load_model(self.intent_model_path)
            _urgency_model_obj = self._load_model(self.urgency_model_path)
        else:
            logger.warning(
                "Scikit-learn or joblib not available. "
                "NLP models will not be loaded. Using fallback logic."
            )

        # Initialize SentimentModel (previously SentimentAnalyzer)
        # These attributes self.sentiment_analyzer, self.topic_analyzer etc. are instances of our analyzer/model classes
        self.sentiment_analyzer = SentimentModel(
            sentiment_model=_sentiment_model_obj,
            has_nltk_installed=HAS_NLTK
        )

        # Initialize TopicModel (previously TopicAnalyzer)
        self.topic_analyzer = TopicModel(topic_model=_topic_model_obj)

        # Initialize IntentModel (previously IntentAnalyzer)
        self.intent_analyzer = IntentModel(intent_model=_intent_model_obj)

        # Initialize UrgencyModel (previously UrgencyAnalyzer)
        self.urgency_analyzer = UrgencyModel(urgency_model=_urgency_model_obj)

    def _load_model(self, model_path: str) -> Optional[Any]:
        """
        Load a pickled model file from the specified path.
        
        Args:
            model_path: Path to the model file
            
        Returns:
            Loaded model object or None if loading fails
        """
        try:
            if os.path.exists(model_path):
                model = joblib.load(model_path)
                logger.info(f"Successfully loaded model from {model_path}")
                return model
            
            logger.warning(f"Model file not found at {model_path}. This model will be unavailable.")
            return None
        except Exception as e:
            logger.error(f"Error loading model from {model_path}: {e}")
            return None

    def _preprocess_text(self, text: str) -> str:
        """
        Perform basic text cleaning and normalization using the shared utility.
        
        Args:
            text: Raw text to preprocess
            
        Returns:
            Preprocessed text
        """
        return clean_text(text)

    def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Perform sentiment analysis using the SentimentAnalyzer component.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary containing sentiment analysis results
        """
        # Try model-based analysis first
        analysis_result = self._analyze_sentiment_model(text)
        if analysis_result:
            return analysis_result

        # Try TextBlob analysis if model fails
        analysis_result = self._analyze_sentiment_textblob(text)
        if analysis_result:
            return analysis_result

        # Use keyword matching as final fallback
        return self._analyze_sentiment_keyword(text)

    def _analyze_topic_model(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Analyze topic using the loaded sklearn model.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary containing topic analysis results or None if analysis fails
        """
        if not self.topic_model:
            return None
            
        try:
            prediction = self.topic_model.predict([text])[0]
            probabilities = self.topic_model.predict_proba([text])[0]
            confidence = float(max(probabilities))
            
            return {
                'topic': str(prediction), 
                'confidence': confidence, 
                'method_used': 'model_topic'
            }
        except Exception as e:
            logger.error(f"Error using topic model: {e}. Trying fallback.")
            return None

    def _analyze_topic_keyword(self, text: str) -> Dict[str, Any]:
        """
        Analyze topic using keyword matching as a fallback method.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary containing topic analysis results
        """
        # Define topic categories and their associated keywords
        topics = {
            'Work & Business': [
                'meeting', 'conference', 'project', 'deadline', 'client', 
                'presentation', 'report', 'proposal'
            ],
            'Finance & Banking': [
                'payment', 'invoice', 'bill', 'statement', 'account', 
                'credit', 'debit', 'transfer', 'money', 'financial'
            ],
            'Personal & Family': [
                'family', 'personal', 'friend', 'birthday', 'anniversary', 
                'vacation', 'holiday', 'weekend', 'dinner', 'lunch'
            ],
            'Health & Wellness': [
                'doctor', 'medical', 'health', 'hospital', 'clinic', 
                'appointment', 'prescription', 'medicine', 'treatment', 'therapy'
            ],
            'Travel & Leisure': [
                'travel', 'flight', 'hotel', 'booking', 'reservation', 
                'trip', 'vacation', 'destination', 'airport', 'airline'
            ]
        }
        
        # Calculate scores for each topic
        topic_scores = {}
        text_lower = text.lower()
        for topic, keywords in topics.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            topic_scores[topic] = score

        # Determine the best matching topic
        if any(score > 0 for score in topic_scores.values()):
            best_topic = max(topic_scores, key=topic_scores.get)
            
            # Calculate confidence score
            # Using a simple heuristic: matched_keywords / 5.0 (capped at 0.9)
            confidence = min(topic_scores[best_topic] / 5.0, 0.9)
            normalized_topic = best_topic.lower().replace(" & ", "_").replace(" ", "_")
            
            return {
                'topic': normalized_topic, # Normalized topic
                'confidence': max(0.1, confidence), 
                'method_used': 'fallback_keyword_topic'
            }
        else:
            return {
                'topic': 'general_communication', # Consistent fallback topic name
                'confidence': 0.5, 
                'method_used': 'fallback_keyword_topic'
            }

    def _analyze_topic(self, text: str) -> Dict[str, Any]:
        """
        Identify the main topic of the email using the TopicAnalyzer component.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary containing topic analysis results
        """
        return self.topic_analyzer.analyze(text)

    def _analyze_intent(self, text: str) -> Dict[str, Any]:
        """
        Determine the intent of the email using the IntentAnalyzer component.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary containing intent analysis results
        """
        return self.intent_analyzer.analyze(text)

    def _analyze_urgency(self, text: str) -> Dict[str, Any]:
        """
        Assess the urgency level of the email using the UrgencyAnalyzer component.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary containing urgency analysis results
        """
        return self.urgency_analyzer.analyze(text)

    def _extract_keywords(self, text: str) -> List[str]:
        """
        Extract important keywords from text.
        
        This method uses TextBlob and NLTK if available, otherwise falls back to
        a simple word matching approach.
        
        Args:
            text: Text to extract keywords from
            
        Returns:
            List of extracted keywords
        """
        # Simple keyword extraction if NLTK is not available
        if not HAS_NLTK:
            words = text.lower().split()
            keywords = []
            important_words = [
                'meeting', 'project', 'deadline', 'urgent', 'important',
                'work', 'business', 'personal', 'family', 'email'
            ]
            
            for word in words:
                if len(word) > 3 and word in important_words:
                    keywords.append(word)
                    
            return keywords[:10]  # Limit to top 10 keywords

        # Advanced keyword extraction with TextBlob and NLTK
        blob = TextBlob(text)
        keywords = []

        # Extract noun phrases as potential keywords
        for phrase in blob.noun_phrases:
            if len(phrase.split()) <= 3:  # Keep only short phrases (up to 3 words)
                keywords.append(phrase)

        # Extract important single words (not in stopwords and longer than 3 chars)
        words = blob.words
        important_words = [
            word for word in words 
            if len(word) > 3 and word.lower() not in self.stop_words
        ]

        # Add top 10 important words
        keywords.extend(important_words[:10])
        
        # Remove duplicates and limit to 15 keywords
        return list(set(keywords))[:15]

    def _categorize_content(self, text: str) -> List[str]:
        """
        Categorize email content based on keyword patterns.
        
        This method uses regex pattern matching to identify the categories
        that best match the email content.
        
        Args:
            text: Text to categorize
            
        Returns:
            List of matched categories (up to 3)
        """
        categories = []
        text_lower = text.lower()

        # Define category patterns for content categorization
        category_patterns = {
            'Work & Business': [
                r'\b(meeting|conference|project|deadline|client|presentation|report|proposal|budget|team|'
                r'colleague|office|work|business|professional|corporate|company|organization)\b',
                
                r'\b(employee|staff|manager|supervisor|director|executive|department|division|'
                r'quarterly|annual|monthly|weekly|daily)\b'
            ],
            'Finance & Banking': [
                r'\b(bank|payment|transaction|invoice|bill|statement|account|credit|debit|transfer|'
                r'money|financial|insurance|investment|loan|mortgage)\b',
                
                r'\$[\d,]+|\b\d+\s?(dollars?|USD|EUR|GBP)\b',
                
                r'\b(tax|taxes|irs|refund|audit|accountant|bookkeeping|overdraft|bankruptcy)\b'
            ],
            'Healthcare': [
                r'\b(doctor|medical|health|hospital|clinic|appointment|prescription|medicine|'
                r'treatment|therapy|checkup|surgery|dental|pharmacy)\b',
                
                r'\b(symptoms|diagnosis|patient|specialist|emergency|ambulance|insurance|'
                r'medicare|medicaid|covid|coronavirus|vaccine)\b'
            ],
            'Personal & Family': [
                r'\b(family|personal|friend|birthday|anniversary|vacation|holiday|weekend|'
                r'dinner|lunch|home|house|kids|children)\b',
                
                r'\b(mom|dad|mother|father|sister|brother|grandma|grandpa|wedding|'
                r'graduation|baby|party|celebration)\b'
            ],
            'Travel': [
                r'\b(travel|flight|hotel|booking|reservation|trip|vacation|destination|'
                r'airport|airline|passport|visa|itinerary)\b',
                
                r'\b(departure|arrival|check-in|luggage|baggage|cruise|resort|tour|'
                r'tickets|confirmation)\b'
            ],
            'Technology': [
                r'\b(software|hardware|computer|laptop|mobile|app|application|website|'
                r'internet|email|password|account|login)\b',
                
                r'\b(server|database|API|code|programming|development|tech|technical|'
                r'IT|support|troubleshoot|install)\b'
            ]
        }

        # Calculate scores for each category
        category_scores = {}
        for category, patterns in category_patterns.items():
            score = 0
            for pattern in patterns:
                matches = re.findall(pattern, text_lower)
                score += len(matches)
                
            if score > 0:
                category_scores[category] = score
                categories.append(category)

        # Sort categories by score (descending)
        if categories:
            categories.sort(key=lambda cat: category_scores[cat], reverse=True)
            return categories[:3]  # Return top 3 matched categories
            
        # Default category if no matches found
        return ['General']

    def _calculate_confidence(self, analysis_results: List[Dict[str, Any]]) -> float:
        """
        Calculate overall confidence score based on individual analysis results.
        
        Args:
            analysis_results: List of analysis result dictionaries
            
        Returns:
            Overall confidence score (0.0-0.95)
        """
        if not analysis_results:
            return 0.5  # Default confidence if no results
            
        # Sum confidence scores from all analysis results
        total_confidence = sum(result['confidence'] for result in analysis_results)
        
        # Calculate average and cap at 0.95
        return min(total_confidence / len(analysis_results), 0.95)

    def _generate_reasoning(self,
                           sentiment: Optional[Dict[str, Any]],
                           topic: Optional[Dict[str, Any]],
                           intent: Optional[Dict[str, Any]],
                           urgency: Optional[Dict[str, Any]]) -> str:
        """
        Generate human-readable reasoning for the analysis results.
        
        This method creates a natural language explanation of the analysis results,
        indicating which methods were used (AI model or fallback).
        
        Args:
            sentiment: Sentiment analysis results
            topic: Topic analysis results
            intent: Intent analysis results
            urgency: Urgency analysis results
            
        Returns:
            Human-readable explanation of the analysis
        """
        parts = []

        def get_method_suffix(analysis_result: Optional[Dict[str, Any]]) -> str:
            """Generate a suffix indicating which method was used for analysis."""
            if not analysis_result or 'method_used' not in analysis_result:
                return " (method unknown)"
                
            method = analysis_result['method_used']
            if 'fallback' in method:
                return f" (using fallback: {method.replace('fallback_', '')})"
            elif 'model' in method:
                return " (using AI model)"
                
            return " (method unknown)"

        # Add sentiment reasoning if significant
        if sentiment and sentiment.get('sentiment') != 'neutral':
            parts.append(
                f"Sentiment analysis detected {sentiment['sentiment']} sentiment"
                f"{get_method_suffix(sentiment)}"
            )

        # Add topic reasoning if significant
        if topic and topic.get('topic') != 'General':
            parts.append(
                f"Identified topic: {topic['topic']}"
                f"{get_method_suffix(topic)}"
            )

        # Add intent reasoning if significant
        if intent and intent.get('intent') != 'informational':
            parts.append(
                f"Detected intent: {intent['intent']}"
                f"{get_method_suffix(intent)}"
            )

        # Add urgency reasoning if significant
        if urgency and urgency.get('urgency') != 'low':
            parts.append(
                f"Assessed urgency level: {urgency['urgency']}"
                f"{get_method_suffix(urgency)}"
            )

        # Return default message if no significant insights
        if not parts:
            return "No significant insights detected from the email content through automated analysis."

        # Join all parts with periods
        return f"{'. '.join(parts)}."

    def _suggest_labels(self, categories: List[str], urgency: str) -> List[str]:
        """Suggest labels for the email"""
        labels = categories.copy()

        if urgency in ['high', 'critical']:
            labels.append(f'{urgency.title()} Priority')

        return list(set(labels))[:6]

    def _detect_risk_factors(self, text: str) -> List[str]:
        """Detect potential risk factors in the email"""
        risk_flags = []
        text_lower = text.lower()

        # Spam indicators
        spam_patterns = [
            r'\b(free|winner|congratulations|claim|prize|lottery)\b',
            r'\b(click here|act now|limited time|exclusive offer)\b'
        ]
        spam_score = sum(len(re.findall(pattern, text_lower)) for pattern in spam_patterns)
        if spam_score > 2:
            risk_flags.append('potential_spam')

        # Suspicious patterns
        suspicious_patterns = [
            r'\b(confidential|private|secret|password|ssn|social security)\b'
        ]
        suspicious_score = sum(len(re.findall(pattern, text_lower)) for pattern in suspicious_patterns)
        if suspicious_score > 0:
            risk_flags.append('sensitive_data')

        return risk_flags

    def _validate_analysis(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the analysis results"""
        # Simple validation based on confidence levels
        confidence = self._calculate_confidence([analysis_results[key] for key in analysis_results])
        is_reliable = confidence > 0.7

        if is_reliable:
            feedback = "Analysis completed with high confidence."
        else:
            feedback = "Analysis completed with moderate confidence. Please review the results."

        return {
            'method': 'confidence_threshold',
            'score': confidence,
            'reliable': is_reliable,
            'feedback': feedback
        }

    def _get_fallback_analysis(self, error_msg: str) -> Dict[str, Any]:
        """Return a fallback analysis in case of errors"""
        return {
            'topic': 'General',
            'sentiment': 'neutral',
            'intent': 'informational',
            'urgency': 'low',
            'confidence': 0.5,
            'categories': ['General'],
            'keywords': [],
            'reasoning': f"Fallback analysis due to error: {error_msg}",
            'suggested_labels': ['General'],
            'risk_flags': ['analysis_failed'], # Ensure this key exists
            'validation': {
                'method': 'fallback', # Ensure this key exists
                'score': 0.5,
                'reliable': False,
                'feedback': 'Analysis failed, using fallback method'
            },
            'action_items': [] # Include empty list for action items
        }

    def _get_simple_fallback_analysis(self, subject: str, content: str) -> Dict[str, Any]:
        """Simple fallback analysis when NLTK is not available"""
        text = f"{subject} {content}".lower()

        # Basic sentiment analysis
        positive_words = ['good', 'great', 'excellent', 'thank', 'please', 'welcome', 'happy']
        negative_words = ['bad', 'terrible', 'problem', 'issue', 'error', 'failed', 'urgent']

        positive_count = sum(1 for word in positive_words if word in text)
        negative_count = sum(1 for word in negative_words if word in text)

        if positive_count > negative_count:
            sentiment = 'positive'
            polarity = 0.5
            confidence = 0.6
        elif negative_count > positive_count:
            sentiment = 'negative'
            polarity = -0.5
            confidence = 0.6
        else:
            sentiment = 'neutral'
            polarity = 0.0
            confidence = 0.5

        # Basic urgency detection
        urgent_words = ['urgent', 'asap', 'immediately', 'critical', 'emergency', 'deadline']
        urgency = 'high' if any(word in text for word in urgent_words) else 'low'

        # Basic categorization
        work_words = ['meeting', 'project', 'deadline', 'work', 'office', 'business']
        personal_words = ['family', 'friend', 'personal', 'home', 'birthday']

        if any(word in text for word in work_words):
            categories = ['Work & Business']
            topic = 'work_business'
        elif any(word in text for word in personal_words):
            categories = ['Personal & Family']
            topic = 'personal_family'
        else:
            categories = ['General']
            topic = 'general_communication'

        return {
            'topic': topic,
            'sentiment': sentiment,
            'intent': 'informational',
            'urgency': urgency,
            'confidence': 0.6,  # Medium confidence for fallback
            'categories': categories,
            'keywords': [],
            'reasoning': 'Basic analysis using keyword matching (NLTK not available)',
            'suggested_labels': categories,
            'risk_flags': [],
            'validation': {
                'method': 'basic_fallback', # Changed key for consistency
                'score': 0.6,
                'reliable': False,
                'feedback': 'Basic analysis - NLTK/models not available or failed'
            },
            'action_items': [] # Include empty list for action items
        }

    def _analyze_action_items(self, text: str) -> List[Dict[str, Any]]:
        """
        Analyze text for action items using ActionItemExtractor.
        """
        logger.info("Analyzing for action items...")
        try:
            actions = self.action_item_extractor.extract_actions(text)
            logger.info(f"Action item analysis completed. Found {len(actions)} potential actions.")
            return actions
        except Exception as e:
            logger.error(f"Error during action item analysis: {e}", exc_info=True)
            return []

    def analyze_email(self, subject: str, content: str) -> Dict[str, Any]:
        """
        Comprehensive email analysis using multiple NLP techniques
        """
        try:
            # If NLTK and models are not available, use simple fallback
            if not HAS_NLTK and not HAS_SKLEARN_AND_JOBLIB: # or specific model checks
                 logger.warning("NLTK and scikit-learn/joblib are unavailable. Using simple fallback analysis.")
                 return self._get_simple_fallback_analysis(subject, content)

            # Combine subject and content for analysis
            full_text = f"{subject} {content}"

            # Basic preprocessing (primarily for non-model based methods or as initial step)
            # Model pipelines should ideally handle their own specific preprocessing.
            logger.info("Preprocessing email text...")
            cleaned_text = self._preprocess_text(full_text)
            logger.info("Email text preprocessed successfully.")

            # Multi-model analysis
            # These methods will internally use models if available, or fall back.
            logger.info("Analyzing sentiment...")
            sentiment_analysis = self._analyze_sentiment(cleaned_text)
            logger.info(f"Sentiment analysis completed. Method: {sentiment_analysis.get('method_used', 'unknown')}")

            logger.info("Analyzing topic...")
            topic_analysis = self._analyze_topic(cleaned_text)
            logger.info(f"Topic analysis completed. Method: {topic_analysis.get('method_used', 'unknown')}")

            logger.info("Analyzing intent...")
            intent_analysis = self._analyze_intent(cleaned_text)
            logger.info(f"Intent analysis completed. Method: {intent_analysis.get('method_used', 'unknown')}")

            logger.info("Analyzing urgency...")
            urgency_analysis = self._analyze_urgency(cleaned_text)
            logger.info(f"Urgency analysis completed. Method: {urgency_analysis.get('method_used', 'unknown')}")

            # This method is regex-based, no model to load for it currently per its implementation
            logger.info("Detecting risk factors...")
            risk_analysis_flags = self._detect_risk_factors(cleaned_text)
            logger.info(f"Risk factor detection completed. Flags: {risk_analysis_flags}")


            # Extract keywords and entities
            logger.info("Extracting keywords...")
            keywords = self._extract_keywords(cleaned_text) # Uses TextBlob if available
            logger.info(f"Keyword extraction completed. Keywords: {keywords}")

            logger.info("Categorizing content...")
            categories = self._categorize_content(cleaned_text) # Regex-based
            logger.info(f"Content categorization completed. Categories: {categories}")

            logger.info("Analyzing action items...")
            action_items = self._analyze_action_items(full_text) # Use full_text for action items for broader context before cleaning for other models
            logger.info(f"Action item analysis completed. Found {len(action_items)} potential actions.")

            logger.info("Building final analysis response...")
            response = self._build_final_analysis_response(
                sentiment_analysis, topic_analysis, intent_analysis, urgency_analysis,
                categories, keywords, risk_analysis_flags, action_items
            )
            logger.info("Final analysis response built successfully.")
            return response

        except Exception as e:
            error_msg = f"NLP analysis failed: {str(e)}"
            logger.exception("Exception in analyze_email:") # Log full traceback
            return self._get_fallback_analysis(error_msg)

    def _build_final_analysis_response(self, sentiment_analysis, topic_analysis, intent_analysis, urgency_analysis,
                                     categories, keywords, risk_analysis_flags, action_items) -> Dict[str, Any]:
        """Helper function to consolidate analysis results and build the final response dictionary."""

        analysis_results_for_confidence = [
            r for r in [sentiment_analysis, topic_analysis, intent_analysis, urgency_analysis] if r and 'confidence' in r
        ]
        overall_confidence = self._calculate_confidence(analysis_results_for_confidence) if analysis_results_for_confidence else 0.5

        reasoning = self._generate_reasoning(
            sentiment_analysis, topic_analysis,
            intent_analysis, urgency_analysis
        )

        validation_input = {
            'sentiment': sentiment_analysis, 'topic': topic_analysis,
            'intent': intent_analysis, 'urgency': urgency_analysis
        }
        validation_input_filtered = {k: v for k, v in validation_input.items() if v is not None}
        validation = self._validate_analysis(validation_input_filtered)

        # Determine default values for primary analysis fields
        final_topic = topic_analysis.get('topic', 'General') if topic_analysis else 'General'
        final_sentiment = sentiment_analysis.get('sentiment', 'neutral') if sentiment_analysis else 'neutral'
        final_intent = intent_analysis.get('intent', 'informational') if intent_analysis else 'informational'
        final_urgency = urgency_analysis.get('urgency', 'low') if urgency_analysis else 'low'

        suggested_labels = self._suggest_labels(categories, final_urgency)

        return {
            'topic': final_topic,
            'sentiment': final_sentiment,
            'intent': final_intent,
            'urgency': final_urgency,
            'confidence': overall_confidence,
            'categories': categories,
            'keywords': keywords,
            'reasoning': reasoning,
            'suggested_labels': suggested_labels,
            'risk_flags': risk_analysis_flags,
            'validation': validation,
            'details': {
                'sentiment_analysis': sentiment_analysis,
                'topic_analysis': topic_analysis,
                'intent_analysis': intent_analysis,
                'urgency_analysis': urgency_analysis,
            },
            'action_items': action_items
        }

# This is the main function to be kept (argparse based)
def main():
    # Basic logging for CLI usage, can be overridden by Gunicorn's logger in production
    logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

    parser = argparse.ArgumentParser(description="Enhanced NLP Engine for Gmail AI Email Management")
    parser.add_argument('--analyze-email', action='store_true', help="Perform email analysis.")
    parser.add_argument('--subject', type=str, default="", help="Subject of the email.")
    parser.add_argument('--content', type=str, default="", help="Content of the email.")
    parser.add_argument('--health-check', action='store_true', help="Perform a health check.")
    parser.add_argument('--output-format', type=str, default="text", choices=['json', 'text'],
                        help="Output format (json or text).")

    args = parser.parse_args()
    engine = NLPEngine()

    if args.health_check:
        _perform_health_check(engine, args.output_format)
        sys.exit(0)

    if args.analyze_email:
        _perform_email_analysis_cli(engine, args.subject, args.content, args.output_format)
        sys.exit(0)

    # Backward compatibility / Default behavior
    # This part handles the old way of calling: python nlp_engine.py "subject" "content"
    # It also serves as a default if no specific action like --health-check or --analyze-email is given.
    # Check if any of the new flags were used. If so, and they weren't handled above, it's an invalid combo or missing action.

    # If no new flags are present, and we have enough sys.argv, assume old style.

    # Prioritize new flags. If specific flags like --analyze-email or --health-check are used,
    # they should handle execution and exit.
    # If script reaches here, it means no specific action flag was triggered.
    # We can check for positional arguments for backward compatibility.

    if _handle_backward_compatible_cli_invocation(engine, args, sys.argv): # type: ignore
        sys.exit(0)

    # If no action flag and no old-style arguments, print help.
    # This condition might be tricky if --subject and --content are passed without --analyze-email.
    # The current argparse setup makes --subject/--content default to "" if not provided,
    # so they don't inherently trigger analysis without --analyze-email.

    # If --analyze-email was not specified, and --health-check was not specified,
    # and we didn't fall into backward compatibility, then print usage.
    # This handles cases like `python nlp_engine.py --subject "test"` (no action)
    if not args.analyze_email and not args.health_check:
        parser.print_help()
        sys.exit(1)

def _perform_health_check(engine: NLPEngine, output_format: str):
    """Performs a health check and prints the status."""
    models_available = []
    if engine.sentiment_model: models_available.append("sentiment")
    if engine.topic_model: models_available.append("topic")
    if engine.intent_model: models_available.append("intent")
    if engine.urgency_model: models_available.append("urgency")

    all_models_loaded = all(model is not None for model in [
        engine.sentiment_model, engine.topic_model,
        engine.intent_model, engine.urgency_model
    ])

    health_status = {
        "status": "ok" if all_models_loaded else "degraded",
        "models_available": models_available,
        "nltk_available": HAS_NLTK,
        "sklearn_available": HAS_SKLEARN_AND_JOBLIB,
        "timestamp": datetime.now().isoformat()
    }
    if output_format == 'json':
        print(json.dumps(health_status))
    else:
        # Pretty print for text output, even if it's JSON structure
        print(json.dumps(health_status, indent=2))

def _perform_email_analysis_cli(engine: NLPEngine, subject: str, content: str, output_format: str):
    """Performs email analysis based on CLI arguments and prints the result."""
    if not subject and not content:
        # If called with --analyze-email but no subject/content, could be an error or expect empty analysis
        logger.warning("Analysis requested with empty subject and content.")

    result = engine.analyze_email(subject, content)
    if output_format == 'json':
        print(json.dumps(result))  # Compact JSON for machine readability
    else:
        print(json.dumps(result, indent=2))  # Pretty print for text output

def _handle_backward_compatible_cli_invocation(engine: NLPEngine, args: argparse.Namespace, argv: List[str]) -> bool:
    """
    Handles backward compatible CLI invocation using positional arguments.
    Returns True if invocation was handled, False otherwise.
    """
    # Check if any known flags are present. If so, it's not an old-style invocation.
    known_flags = ['--analyze-email', '--health-check', '--subject', '--content', '--output-format']
    if any(flag in argv for flag in known_flags):
        return False

    # Old style: python nlp_engine.py "subject" "content"
    # len(argv) will be at least 1 (script name)
    if len(argv) > 1: # Script name + at least one arg
        if len(argv) < 3: # Script name, subject, (optional) content
             # Allow content to be empty for old style, but subject must be there if any arg is given
            err_msg = {'error': 'Invalid arguments for old-style invocation. Subject is required. Usage: python nlp_engine.py "<subject>" "[content]"'}
            if args.output_format == 'json': print(json.dumps(err_msg))
            else: print(json.dumps(err_msg, indent=2))
            sys.exit(1) # Exit here as it's an error in argument usage for this mode

        subject_old = argv[1]
        content_old = argv[2] if len(argv) > 2 else ""

        logger.info("Processing with backward compatibility mode (positional arguments).")
        # Use the already defined _perform_email_analysis_cli for consistency in output
        _perform_email_analysis_cli(engine, subject_old, content_old, args.output_format)
        return True
    return False

if __name__ == "__main__":
    main()
