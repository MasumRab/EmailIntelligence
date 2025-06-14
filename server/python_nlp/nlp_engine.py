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
try:
    import nltk
    from textblob import TextBlob
    HAS_NLTK = True
except ImportError:
    HAS_NLTK = False
    print("Warning: NLTK not available, using fallback analysis", file=sys.stderr)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NLPEngine:
    def __init__(self):
        self.stop_words = set(nltk.corpus.stopwords.words('english')) if HAS_NLTK else set()

    def _preprocess_text(self, text: str) -> str:
        """Basic text cleaning and normalization"""
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        return text

    def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Enhanced sentiment analysis with confidence scoring"""
        if not HAS_NLTK:
            # Simple sentiment analysis without TextBlob
            text_lower = text.lower()
            positive_words = ['good', 'great', 'excellent', 'thank', 'please', 'welcome', 'happy', 'love']
            negative_words = ['bad', 'terrible', 'problem', 'issue', 'error', 'failed', 'hate', 'angry']

            positive_count = sum(1 for word in positive_words if word in text_lower)
            negative_count = sum(1 for word in negative_words if word in text_lower)

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

            return {
                'sentiment': sentiment,
                'polarity': polarity,
                'subjectivity': 0.5,
                'confidence': confidence
            }

        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity

        # Convert polarity to categorical sentiment
        if polarity > 0.1:
            sentiment = 'positive'
            confidence = min(polarity + 0.5, 1.0)
        elif polarity < -0.1:
            sentiment = 'negative'
            confidence = min(abs(polarity) + 0.5, 1.0)
        else:
            sentiment = 'neutral'
            confidence = 0.7

        return {
            'sentiment': sentiment,
            'polarity': polarity,
            'subjectivity': subjectivity,
            'confidence': confidence
        }

    def _analyze_topic(self, text: str) -> Dict[str, Any]:
        """Identify main topic of the email"""
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

        if topic_scores:
            best_topic = max(topic_scores, key=topic_scores.get)
            confidence = min(topic_scores[best_topic] / 10.0, 0.9)
            return {'topic': best_topic, 'confidence': confidence}
        else:
            return {'topic': 'General', 'confidence': 0.5}

    def _analyze_intent(self, text: str) -> Dict[str, Any]:
        """Determine the intent of the email"""
        intent_patterns = {
            'request': r'\b(please|could you|would you|can you|need|require|request)\b',
            'inquiry': r'\b(question|ask|wonder|curious|information|details|clarification)\b',
            'scheduling': r'\b(schedule|calendar|meeting|appointment|time|date|available)\b',
            'urgent_action': r'\b(urgent|asap|immediately|emergency|critical|priority)\b',
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

        if intent_scores:
            best_intent = max(intent_scores, key=intent_scores.get)
            confidence = min(intent_scores[best_intent] / 5.0, 0.9)
            return {'intent': best_intent, 'confidence': confidence}
        else:
            return {'intent': 'informational', 'confidence': 0.6}

    def _analyze_urgency(self, text: str) -> Dict[str, Any]:
        """Assess the urgency level of the email"""
        text_lower = text.lower()

        if re.search(r'\b(emergency|urgent|asap|immediately|critical|crisis|disaster)\b', text_lower):
            urgency = 'critical'
            confidence = 0.9
        elif re.search(r'\b(soon|quickly|priority|important|deadline|time-sensitive)\b', text_lower):
            urgency = 'high'
            confidence = 0.8
        elif re.search(r'\b(when you can|next week|upcoming|planned|scheduled)\b', text_lower):
            urgency = 'medium'
            confidence = 0.6
        else:
            urgency = 'low'
            confidence = 0.5

        return {'urgency': urgency, 'confidence': confidence}

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
        """Generate human-readable reasoning for the analysis"""
        parts = []

        if sentiment['sentiment'] != 'neutral':
            parts.append(f"Sentiment analysis detected {sentiment['sentiment']} sentiment")

        if topic['topic'] != 'General':
            parts.append(f"Identified topic: {topic['topic']}")

        if intent['intent'] != 'informational':
            parts.append(f"Detected intent: {intent['intent']}")

        if urgency['urgency'] != 'low':
            parts.append(f"Assessed urgency level: {urgency['urgency']}")

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
            'risk_flags': ['analysis_failed'],
            'validation': {
                'method': 'fallback',
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
                'validation_method': 'basic_fallback',
                'score': 0.6,
                'reliable': False,
                'feedback': 'Basic analysis - install NLTK for enhanced features'
            }
        }

    def analyze_email(self, subject: str, content: str) -> Dict[str, Any]:
        """
        Comprehensive email analysis using multiple NLP techniques
        """
        try:
            # If NLTK is not available, use fallback analysis
            if not HAS_NLTK:
                return self._get_simple_fallback_analysis(subject, content)

            # Combine subject and content for analysis
            full_text = f"{subject} {content}"

            # Basic preprocessing
            cleaned_text = self._preprocess_text(full_text)

            # Multi-model analysis
            sentiment_analysis = self._analyze_sentiment(cleaned_text)
            topic_analysis = self._analyze_topic(cleaned_text)
            intent_analysis = self._analyze_intent(cleaned_text)
            urgency_analysis = self._analyze_urgency(cleaned_text)
            risk_analysis = self._analyze_risk_factors(cleaned_text)

            # Extract keywords and entities
            keywords = self._extract_keywords(cleaned_text)
            categories = self._categorize_content(cleaned_text)

            # Calculate overall confidence
            confidence = self._calculate_confidence([
                sentiment_analysis, topic_analysis, 
                intent_analysis, urgency_analysis
            ])

            # Generate reasoning
            reasoning = self._generate_reasoning(
                sentiment_analysis, topic_analysis, 
                intent_analysis, urgency_analysis
            )

            # Validation
            validation = self._validate_analysis({
                'sentiment': sentiment_analysis,
                'topic': topic_analysis,
                'intent': intent_analysis,
                'urgency': urgency_analysis
            })

            return {
                'topic': topic_analysis['topic'],
                'sentiment': sentiment_analysis['sentiment'],
                'intent': intent_analysis['intent'],
                'urgency': urgency_analysis['urgency'],
                'confidence': confidence,
                'categories': categories,
                'keywords': keywords,
                'reasoning': reasoning,
                'suggested_labels': self._suggest_labels(categories, urgency_analysis['urgency']),
                'risk_flags': risk_analysis,
                'validation': validation
            }

        except Exception as e:
            error_msg = f"NLP analysis failed: {str(e)}"
            logging.error(error_msg)
            return self._get_fallback_analysis(error_msg)

def main():
    if len(sys.argv) != 3:
        print(json.dumps({'error': 'Invalid arguments. Usage: python nlp_engine.py <subject> <content>'}))
        sys.exit(1)

    subject = sys.argv[1]
    content = sys.argv[2]

    engine = NLPEngine()
    result = engine.analyze_email(subject, content)

    print(json.dumps(result))

if __name__ == "__main__":
    main()