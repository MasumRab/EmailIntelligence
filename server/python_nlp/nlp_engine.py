#!/usr/bin/env python3
"""
Enhanced NLP Engine for Gmail AI Email Management
Advanced natural language processing with multiple AI models and validation
"""

import sys
import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import re
import os
try:
    import nltk
    from textblob import TextBlob
    import joblib # For loading scikit-learn models
    HAS_NLTK = True
    HAS_SKLEARN_AND_JOBLIB = True
except ImportError:
    HAS_NLTK = False
    HAS_SKLEARN_AND_JOBLIB = False # Assume if one is missing, model loading won't work
    print("Warning: NLTK, scikit-learn or joblib not available. Model loading and/or advanced NLP features will be disabled.", file=sys.stderr)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)

# Define paths for pre-trained models (assuming they are in the same directory or a specified model directory)
MODEL_DIR = os.getenv("NLP_MODEL_DIR", os.path.dirname(__file__)) # Default to script's directory
SENTIMENT_MODEL_PATH = os.path.join(MODEL_DIR, "sentiment_model.pkl")
TOPIC_MODEL_PATH = os.path.join(MODEL_DIR, "topic_model.pkl")
INTENT_MODEL_PATH = os.path.join(MODEL_DIR, "intent_model.pkl")
URGENCY_MODEL_PATH = os.path.join(MODEL_DIR, "urgency_model.pkl")


class NLPEngine:
    def __init__(self):
        self.stop_words = set(nltk.corpus.stopwords.words('english')) if HAS_NLTK else set()

        self.sentiment_model = None
        self.topic_model = None
        self.intent_model = None
        self.urgency_model = None

        if HAS_SKLEARN_AND_JOBLIB:
            logger.info("Attempting to load NLP models...")
            self.sentiment_model = self._load_model(SENTIMENT_MODEL_PATH)
            self.topic_model = self._load_model(TOPIC_MODEL_PATH)
            self.intent_model = self._load_model(INTENT_MODEL_PATH)
            self.urgency_model = self._load_model(URGENCY_MODEL_PATH)
        else:
            logger.warning("Scikit-learn or joblib not available. NLP models will not be loaded. Using fallback logic.")

    def _load_model(self, model_path: str) -> Any:
        """Helper function to load a pickled model file."""
        try:
            if os.path.exists(model_path):
                model = joblib.load(model_path)
                logger.info(f"Successfully loaded model from {model_path}")
                return model
            else:
                logger.warning(f"Model file not found at {model_path}. This model will be unavailable.")
                return None
        except Exception as e:
            logger.error(f"Error loading model from {model_path}: {e}")
            return None

    def _preprocess_text(self, text: str) -> str:
        """Basic text cleaning and normalization"""
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        return text

    def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Enhanced sentiment analysis with confidence scoring using a loaded model or TextBlob."""
        if self.sentiment_model:
            try:
                # Assuming the model is a scikit-learn pipeline that handles preprocessing (e.g., vectorization)
                # And it has methods predict() and predict_proba()
                # The classes_ attribute should tell us the order of probabilities
                prediction = self.sentiment_model.predict([text])[0]
                probabilities = self.sentiment_model.predict_proba([text])[0]

                # Assuming classes are ordered e.g. ['negative', 'neutral', 'positive']
                # Or the model has a classes_ attribute
                class_labels = self.sentiment_model.classes_
                confidence = max(probabilities)

                # Polarity and subjectivity are harder to get directly from a generic classifier.
                # We'll set polarity based on prediction and default subjectivity.
                # This part might need refinement based on how the sentiment model is trained.
                polarity = 0.0
                if prediction == 'positive':
                    polarity = confidence # Use confidence as a proxy for polarity strength
                elif prediction == 'negative':
                    polarity = -confidence

                return {
                    'sentiment': str(prediction), # Ensure it's a string
                    'polarity': polarity,
                    'subjectivity': 0.5,  # Default subjectivity, TextBlob is better for this
                    'confidence': float(confidence),
                    'method_used': 'model_sentiment'
                }
            except Exception as e:
                logger.error(f"Error using sentiment model: {e}. Falling back to TextBlob/simple analysis.")
                # Fall through to TextBlob/simple analysis

        # Fallback to TextBlob if NLTK is available
        if HAS_NLTK:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity

            if polarity > 0.1:
                sentiment_label = 'positive'
                confidence = min(polarity + 0.5, 1.0)
            elif polarity < -0.1:
                sentiment_label = 'negative'
                confidence = min(abs(polarity) + 0.5, 1.0)
            else:
                sentiment_label = 'neutral'
                confidence = 0.7 # Default confidence for TextBlob neutral

            return {
                'sentiment': sentiment_label,
                'polarity': polarity,
                'subjectivity': subjectivity,
                'confidence': confidence,
                'method_used': 'fallback_textblob_sentiment'
            }

        # Absolute fallback (simple keyword-based if NLTK/TextBlob also failed or unavailable)
        text_lower = text.lower()
        positive_words = ['good', 'great', 'excellent', 'thank', 'please', 'welcome', 'happy', 'love']
        negative_words = ['bad', 'terrible', 'problem', 'issue', 'error', 'failed', 'hate', 'angry']
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)

        if positive_count > negative_count: sentiment_label, pol, conf = 'positive', 0.5, 0.6
        elif negative_count > positive_count: sentiment_label, pol, conf = 'negative', -0.5, 0.6
        else: sentiment_label, pol, conf = 'neutral', 0.0, 0.5

        return {
            'sentiment': sentiment_label,
            'polarity': pol,
            'subjectivity': 0.5,
            'confidence': conf,
            'method_used': 'fallback_keyword_sentiment'
        }


    def _analyze_topic(self, text: str) -> Dict[str, Any]:
        """Identify main topic of the email using a loaded model or keyword-based fallback."""
        if self.topic_model:
            try:
                prediction = self.topic_model.predict([text])[0]
                probabilities = self.topic_model.predict_proba([text])[0]
                confidence = float(max(probabilities))
                return {'topic': str(prediction), 'confidence': confidence, 'method_used': 'model_topic'}
            except Exception as e:
                logger.error(f"Error using topic model: {e}. Falling back to keyword-based analysis.")
                # Fall through to keyword-based

        # Fallback keyword-based logic
        topics = {
            'Work & Business': ['meeting', 'conference', 'project', 'deadline', 'client', 'presentation', 'report', 'proposal'],
            'Finance & Banking': ['payment', 'invoice', 'bill', 'statement', 'account', 'credit', 'debit', 'transfer', 'money', 'financial'],
            'Personal & Family': ['family', 'personal', 'friend', 'birthday', 'anniversary', 'vacation', 'holiday', 'weekend', 'dinner', 'lunch'],
            'Health & Wellness': ['doctor', 'medical', 'health', 'hospital', 'clinic', 'appointment', 'prescription', 'medicine', 'treatment', 'therapy'],
            'Travel & Leisure': ['travel', 'flight', 'hotel', 'booking', 'reservation', 'trip', 'vacation', 'destination', 'airport', 'airline']
        }
        topic_scores = {}
        text_lower = text.lower()
        for topic, keywords in topics.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            topic_scores[topic] = score

        if any(score > 0 for score in topic_scores.values()): # Check if any keyword matched
            best_topic = max(topic_scores, key=topic_scores.get)
            confidence = min(topic_scores[best_topic] / 5.0, 0.9)
            return {'topic': best_topic, 'confidence': max(0.1, confidence), 'method_used': 'fallback_keyword_topic'}
        else:
            return {'topic': 'General', 'confidence': 0.5, 'method_used': 'fallback_keyword_topic'}


    def _analyze_intent(self, text: str) -> Dict[str, Any]:
        """Determine the intent of the email using a loaded model or regex-based fallback."""
        if self.intent_model:
            try:
                prediction = self.intent_model.predict([text])[0]
                probabilities = self.intent_model.predict_proba([text])[0]
                confidence = float(max(probabilities))
                return {'intent': str(prediction), 'confidence': confidence, 'method_used': 'model_intent'}
            except Exception as e:
                logger.error(f"Error using intent model: {e}. Falling back to regex-based analysis.")
                # Fall through to regex-based

        # Fallback regex-based logic
        intent_patterns = {
            'request': r'\b(please|could you|would you|can you|need|require|request)\b',
            'inquiry': r'\b(question|ask|wonder|curious|information|details|clarification)\b',
            'scheduling': r'\b(schedule|calendar|meeting|appointment|time|date|available)\b',
            'urgent_action': r'\b(urgent|asap|immediately|emergency|critical|priority)\b', # This might overlap with urgency
            'gratitude': r'\b(thank|thanks|grateful|appreciate)\b',
            'complaint': r'\b(complaint|complain|issue|problem|dissatisfied|unhappy)\b',
            'follow_up': r'\b(follow up|follow-up|checking in|status|update|progress)\b',
            'confirmation': r'\b(confirm|confirmation|verify|check|acknowledge)\b'
        }
        intent_scores = {}
        text_lower = text.lower()
        for intent, pattern in intent_patterns.items():
            matches = re.findall(pattern, text_lower)
            intent_scores[intent] = len(matches)

        if any(score > 0 for score in intent_scores.values()):
            best_intent = max(intent_scores, key=intent_scores.get)
            confidence = min(intent_scores[best_intent] / 3.0, 0.9)
            return {'intent': best_intent, 'confidence': max(0.1, confidence), 'method_used': 'fallback_regex_intent'}
        else:
            return {'intent': 'informational', 'confidence': 0.6, 'method_used': 'fallback_regex_intent'}


    def _analyze_urgency(self, text: str) -> Dict[str, Any]:
        """Assess the urgency level of the email"""
        if self.urgency_model:
            try:
                prediction = self.urgency_model.predict([text])[0]
                probabilities = self.urgency_model.predict_proba([text])[0]
                confidence = float(max(probabilities))
                return {'urgency': str(prediction), 'confidence': confidence, 'method_used': 'model_urgency'}
            except Exception as e:
                logger.error(f"Error using urgency model: {e}. Falling back to regex-based analysis.")
                # Fall through to regex based

        text_lower = text.lower()
        if re.search(r'\b(emergency|urgent|asap|immediately|critical|crisis|disaster)\b', text_lower):
            urgency_label, conf = 'critical', 0.9
        elif re.search(r'\b(soon|quickly|priority|important|deadline|time-sensitive)\b', text_lower):
            urgency_label, conf = 'high', 0.8
        elif re.search(r'\b(when you can|next week|upcoming|planned|scheduled)\b', text_lower):
            urgency_label, conf = 'medium', 0.6
        else:
            urgency_label, conf = 'low', 0.5
        return {'urgency': urgency_label, 'confidence': conf, 'method_used': 'fallback_regex_urgency'}

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text"""
        if not HAS_NLTK:
            # Simple keyword extraction without NLTK
            words = text.lower().split()
            keywords = []
            important_words = ['meeting', 'project', 'deadline', 'urgent', 'important', 
                             'work', 'business', 'personal', 'family', 'email']
            for word in words:
                if len(word) > 3 and word in important_words:
                    keywords.append(word)
            return keywords[:10]

        # Remove stopwords and extract important terms
        blob = TextBlob(text)

        # Get noun phrases as potential keywords
        keywords = []
        for phrase in blob.noun_phrases:
            if len(phrase.split()) <= 3:  # Keep short phrases
                keywords.append(phrase)

        # Add important single words
        words = blob.words
        important_words = [word for word in words 
                          if len(word) > 3 and word.lower() not in self.stop_words]

        keywords.extend(important_words[:10])  # Limit to top 10

        return list(set(keywords))[:15]  # Remove duplicates and limit

    def _categorize_content(self, text: str) -> List[str]:
        """Categorize email content based on keywords"""
        categories = []
        text_lower = text.lower()

        category_patterns = {
            'Work & Business': [
                r'\b(meeting|conference|project|deadline|client|presentation|report|proposal|budget|team|colleague|office|work|business|professional|corporate|company|organization)\b',
                r'\b(employee|staff|manager|supervisor|director|executive|department|division|quarterly|annual|monthly|weekly|daily)\b'
            ],
            'Finance & Banking': [
                r'\b(bank|payment|transaction|invoice|bill|statement|account|credit|debit|transfer|money|financial|insurance|investment|loan|mortgage)\b',
                r'\$[\d,]+|\b\d+\s?(dollars?|USD|EUR|GBP)\b',
                r'\b(tax|taxes|irs|refund|audit|accountant|bookkeeping|overdraft|bankruptcy)\b'
            ],
            'Healthcare': [
                r'\b(doctor|medical|health|hospital|clinic|appointment|prescription|medicine|treatment|therapy|checkup|surgery|dental|pharmacy)\b',
                r'\b(symptoms|diagnosis|patient|specialist|emergency|ambulance|insurance|medicare|medicaid|covid|coronavirus|vaccine)\b'
            ],
            'Personal & Family': [
                r'\b(family|personal|friend|birthday|anniversary|vacation|holiday|weekend|dinner|lunch|home|house|kids|children)\b',
                r'\b(mom|dad|mother|father|sister|brother|grandma|grandpa|wedding|graduation|baby|party|celebration)\b'
            ],
            'Travel': [
                r'\b(travel|flight|hotel|booking|reservation|trip|vacation|destination|airport|airline|passport|visa|itinerary)\b',
                r'\b(departure|arrival|check-in|luggage|baggage|cruise|resort|tour|tickets|confirmation)\b'
            ],
            'Technology': [
                r'\b(software|hardware|computer|laptop|mobile|app|application|website|internet|email|password|account|login)\b',
                r'\b(server|database|API|code|programming|development|tech|technical|IT|support|troubleshoot|install)\b'
            ]
        }

        for category, patterns in category_patterns.items():
            score = 0
            for pattern in patterns:
                matches = re.findall(pattern, text_lower)
                score += len(matches)
            if score > 0:
                categories.append(category)

        return categories[:3] if categories else ['General']

    def _calculate_confidence(self, analysis_results: List[Dict[str, Any]]) -> float:
        """Calculate overall confidence score"""
        total_confidence = sum(result['confidence'] for result in analysis_results)
        return min(total_confidence / len(analysis_results), 0.95)

    def _generate_reasoning(self, sentiment: Dict[str, Any], topic: Dict[str, Any], intent: Dict[str, Any], urgency: Dict[str, Any]) -> str:
        """Generate human-readable reasoning for the analysis, indicating if fallbacks were used."""
        parts = []

        def get_method_suffix(analysis_result: Optional[Dict[str, Any]]) -> str:
            if analysis_result and 'method_used' in analysis_result and 'fallback' in analysis_result['method_used']:
                return f" (using fallback: {analysis_result['method_used'].replace('fallback_', '')})"
            elif analysis_result and 'method_used' in analysis_result and 'model' in analysis_result['method_used']:
                return " (using AI model)"
            return " (method unknown)"


        if sentiment and sentiment.get('sentiment') != 'neutral':
            parts.append(f"Sentiment analysis detected {sentiment['sentiment']} sentiment{get_method_suffix(sentiment)}")

        if topic and topic.get('topic') != 'General':
            parts.append(f"Identified topic: {topic['topic']}{get_method_suffix(topic)}")

        if intent and intent.get('intent') != 'informational':
            parts.append(f"Detected intent: {intent['intent']}{get_method_suffix(intent)}")

        if urgency and urgency.get('urgency') != 'low':
            parts.append(f"Assessed urgency level: {urgency['urgency']}{get_method_suffix(urgency)}")

        if not parts:
            return "No significant insights detected from the email content through automated analysis."

        return ". ".join(parts) + "."

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
            }
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
            }
        }

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
            cleaned_text = self._preprocess_text(full_text)

            # Multi-model analysis
            # These methods will internally use models if available, or fall back.
            sentiment_analysis = self._analyze_sentiment(cleaned_text)
            topic_analysis = self._analyze_topic(cleaned_text) # Will be updated in next step
            intent_analysis = self._analyze_intent(cleaned_text) # Will be updated in next step
            urgency_analysis = self._analyze_urgency(cleaned_text) # Already updated

            # This method is regex-based, no model to load for it currently per its implementation
            risk_analysis_flags = self._detect_risk_factors(cleaned_text)


            # Extract keywords and entities
            keywords = self._extract_keywords(cleaned_text) # Uses TextBlob if available
            categories = self._categorize_content(cleaned_text) # Regex-based

            # Consolidate results
            # Confidence calculation might need to be revisited if models are very different
            # For now, let's assume each analysis function returns a 'confidence' field.
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
            # Filter out None results before passing to _validate_analysis
            validation_input_filtered = {k: v for k, v in validation_input.items() if v is not None}
            validation = self._validate_analysis(validation_input_filtered)


            return {
                'topic': topic_analysis.get('topic', 'General') if topic_analysis else 'General',
                'sentiment': sentiment_analysis.get('sentiment', 'neutral') if sentiment_analysis else 'neutral',
                'intent': intent_analysis.get('intent', 'informational') if intent_analysis else 'informational',
                'urgency': urgency_analysis.get('urgency', 'low') if urgency_analysis else 'low',
                'confidence': overall_confidence,
                'categories': categories,
                'keywords': keywords,
                'reasoning': reasoning,
                'suggested_labels': self._suggest_labels(categories, urgency_analysis.get('urgency', 'low') if urgency_analysis else 'low'),
                'risk_flags': risk_analysis_flags, # Use the direct output from _detect_risk_factors
                'validation': validation,
                # Include individual model confidences for transparency if needed
                'details': {
                    'sentiment_analysis': sentiment_analysis,
                    'topic_analysis': topic_analysis,
                    'intent_analysis': intent_analysis,
                    'urgency_analysis': urgency_analysis,
                }
            }

        except Exception as e:
            error_msg = f"NLP analysis failed: {str(e)}"
            logger.exception("Exception in analyze_email:") # Log full traceback
            return self._get_fallback_analysis(error_msg)

def main():
    # Basic logging for CLI usage, can be overridden by Gunicorn's logger in production
    logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

    if len(sys.argv) < 3: # Allow content to be empty
        print(json.dumps({'error': 'Invalid arguments. Usage: python nlp_engine.py "<subject>" "<content>"'}))
        sys.exit(1)

    subject = sys.argv[1]
    # Content can be empty, handle that case
    content = sys.argv[2] if len(sys.argv) > 2 else ""


    engine = NLPEngine()
    result = engine.analyze_email(subject, content)

    print(json.dumps(result, indent=2)) # Pretty print for readability

if __name__ == "__main__":
    main()