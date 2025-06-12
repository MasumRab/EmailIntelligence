#!/usr/bin/env python3
"""
Advanced NLP Engine for Email Analysis
Provides sophisticated email categorization, sentiment analysis, and intent detection
"""

import re
import json
import sys
import logging
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from collections import Counter
import math

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class EmailAnalysis:
    """Complete email analysis result"""
    topic: str
    sentiment: str  # positive, negative, neutral
    intent: str
    urgency: str  # low, medium, high, critical
    confidence: float
    categories: List[str]
    keywords: List[str]
    reasoning: str
    suggested_labels: List[str]
    risk_flags: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class AccuracyValidation:
    """Accuracy validation metrics"""
    validation_method: str
    score: float
    reliable: bool
    feedback: str

class AdvancedNLPEngine:
    """
    Advanced NLP engine using pattern matching, linguistic rules, and statistical analysis
    Designed to work without external dependencies for maximum reliability
    """
    
    def __init__(self):
        self.accuracy_threshold = 0.7
        self.sentiment_lexicon = self._build_sentiment_lexicon()
        self.category_patterns = self._build_category_patterns()
        self.intent_patterns = self._build_intent_patterns()
        self.urgency_patterns = self._build_urgency_patterns()
        self.stopwords = self._get_stopwords()
        
    def _build_sentiment_lexicon(self) -> Dict[str, Dict[str, float]]:
        """Build comprehensive sentiment lexicon with weights"""
        return {
            'positive': {
                'excellent': 0.9, 'amazing': 0.9, 'fantastic': 0.9, 'wonderful': 0.8,
                'great': 0.8, 'good': 0.7, 'nice': 0.6, 'pleased': 0.7, 'happy': 0.8,
                'satisfied': 0.7, 'thank': 0.6, 'thanks': 0.6, 'grateful': 0.7,
                'appreciate': 0.7, 'love': 0.8, 'perfect': 0.9, 'success': 0.8,
                'achievement': 0.7, 'congratulations': 0.8, 'well done': 0.8,
                'approve': 0.6, 'accept': 0.6, 'agree': 0.6, 'brilliant': 0.9,
                'outstanding': 0.9, 'impressive': 0.8, 'recommend': 0.7
            },
            'negative': {
                'terrible': 0.9, 'awful': 0.9, 'horrible': 0.9, 'disaster': 0.9,
                'bad': 0.7, 'poor': 0.7, 'disappointed': 0.8, 'frustrated': 0.8,
                'angry': 0.8, 'upset': 0.7, 'problem': 0.7, 'issue': 0.6,
                'error': 0.7, 'mistake': 0.7, 'wrong': 0.6, 'failed': 0.8,
                'failure': 0.8, 'broken': 0.7, 'difficult': 0.6, 'trouble': 0.7,
                'concern': 0.6, 'worry': 0.7, 'urgent': 0.8, 'emergency': 0.9,
                'critical': 0.8, 'serious': 0.7, 'reject': 0.7, 'deny': 0.7,
                'refuse': 0.7, 'cancel': 0.6, 'complaint': 0.8, 'complain': 0.7
            }
        }
    
    def _build_category_patterns(self) -> Dict[str, List[Dict[str, Any]]]:
        """Build comprehensive category classification patterns"""
        return {
            'Work & Business': [
                {
                    'patterns': [
                        r'\b(meeting|conference|project|deadline|client|presentation|report|proposal|budget)\b',
                        r'\b(team|colleague|office|work|business|professional|corporate|company|organization)\b',
                        r'\b(schedule|calendar|appointment|discussion|review|analysis|strategy|planning)\b',
                        r'\b(employee|staff|manager|supervisor|director|executive|department|division)\b'
                    ],
                    'weight': 1.0
                },
                {
                    'patterns': [r'\b(quarterly|annual|monthly|weekly|daily)\s+(report|meeting|review)\b'],
                    'weight': 1.2
                }
            ],
            'Finance & Banking': [
                {
                    'patterns': [
                        r'\b(bank|payment|transaction|invoice|bill|statement|account|credit|debit)\b',
                        r'\b(transfer|money|financial|insurance|investment|loan|mortgage|interest)\b',
                        r'\$[\d,]+|\b\d+\s?(dollars?|USD|EUR|GBP|cents?)\b',
                        r'\b(tax|taxes|irs|refund|audit|accountant|bookkeeping)\b'
                    ],
                    'weight': 1.0
                },
                {
                    'patterns': [r'\b(overdraft|bankruptcy|foreclosure|collections?)\b'],
                    'weight': 1.3
                }
            ],
            'Personal & Family': [
                {
                    'patterns': [
                        r'\b(family|personal|friend|birthday|anniversary|vacation|holiday|weekend)\b',
                        r'\b(dinner|lunch|home|house|kids|children|spouse|partner|relative)\b',
                        r'\b(mom|dad|mother|father|sister|brother|grandma|grandpa|aunt|uncle|cousin)\b',
                        r'\b(wedding|graduation|baby|shower|party|celebration|reunion)\b'
                    ],
                    'weight': 1.0
                }
            ],
            'Healthcare': [
                {
                    'patterns': [
                        r'\b(doctor|medical|health|hospital|clinic|appointment|prescription|medicine)\b',
                        r'\b(treatment|therapy|checkup|surgery|dental|pharmacy|nurse|physician)\b',
                        r'\b(symptoms|diagnosis|patient|specialist|emergency|ambulance|urgent care)\b',
                        r'\b(insurance|medicare|medicaid|copay|deductible|benefits)\b'
                    ],
                    'weight': 1.0
                },
                {
                    'patterns': [r'\b(covid|coronavirus|pandemic|vaccine|vaccination)\b'],
                    'weight': 1.2
                }
            ],
            'Travel': [
                {
                    'patterns': [
                        r'\b(travel|flight|hotel|booking|reservation|trip|vacation|destination)\b',
                        r'\b(airport|airline|passport|visa|itinerary|accommodation|boarding)\b',
                        r'\b(departure|arrival|check-in|luggage|baggage|rental car)\b',
                        r'\b(cruise|resort|tour|guide|tickets?|confirmation)\b'
                    ],
                    'weight': 1.0
                }
            ],
            'Promotions & Marketing': [
                {
                    'patterns': [
                        r'\b(sale|discount|offer|promotion|deal|coupon|newsletter|marketing)\b',
                        r'\b(advertisement|special|limited|exclusive|free|save|percent off)\b',
                        r'%\s*off|free shipping|limited time|act now|don\'t miss|buy now',
                        r'\b(unsubscribe|opt-out|mailing list|promotional)\b'
                    ],
                    'weight': 1.0
                }
            ],
            'Education': [
                {
                    'patterns': [
                        r'\b(school|university|college|student|teacher|professor|course|class)\b',
                        r'\b(lecture|assignment|homework|exam|grade|study|education|academic)\b',
                        r'\b(semester|tuition|scholarship|graduation|degree|diploma|transcript)\b',
                        r'\b(enrollment|registration|admissions?|application)\b'
                    ],
                    'weight': 1.0
                }
            ],
            'Technology': [
                {
                    'patterns': [
                        r'\b(software|hardware|computer|laptop|mobile|app|application|website)\b',
                        r'\b(internet|email|password|account|login|update|upgrade|bug|feature)\b',
                        r'\b(server|database|API|code|programming|development|tech|technical|IT)\b',
                        r'\b(support|troubleshoot|install|configure|backup|security)\b'
                    ],
                    'weight': 1.0
                }
            ],
            'Legal': [
                {
                    'patterns': [
                        r'\b(legal|law|lawyer|attorney|court|lawsuit|litigation|contract)\b',
                        r'\b(agreement|terms|conditions|policy|compliance|regulation|statute)\b',
                        r'\b(copyright|trademark|patent|intellectual property|license)\b',
                        r'\b(defendant|plaintiff|judge|jury|verdict|settlement)\b'
                    ],
                    'weight': 1.0
                }
            ]
        }
    
    def _build_intent_patterns(self) -> Dict[str, List[str]]:
        """Build intent detection patterns"""
        return {
            'request': [
                r'\b(please|could you|would you|can you|need|require|request|ask for)\b',
                r'\b(help|assist|support|provide|send|give|share)\b',
                r'\b(want|would like|looking for|in need of)\b'
            ],
            'inquiry': [
                r'\b(question|ask|wonder|curious|information|details|clarification)\b',
                r'\b(explain|how|what|when|where|why|which|who)\b',
                r'\?|inquire|query|wondering'
            ],
            'scheduling': [
                r'\b(schedule|calendar|meeting|appointment|time|date|available|busy|free)\b',
                r'\b(reschedule|postpone|cancel|confirm|book|reserve)\b',
                r'\b(today|tomorrow|next week|this week|monday|tuesday|wednesday|thursday|friday)\b'
            ],
            'confirmation': [
                r'\b(confirm|confirmation|verify|check|ensure|validate|acknowledge)\b',
                r'\b(received|got|understand|clear|correct|right)\b'
            ],
            'complaint': [
                r'\b(complaint|complain|issue|problem|dissatisfied|unhappy|wrong|error)\b',
                r'\b(not working|broken|failed|disappointed|frustrated)\b'
            ],
            'gratitude': [
                r'\b(thank|thanks|grateful|appreciate|acknowledgment|recognition)\b',
                r'\b(thankful|blessed|indebted)\b'
            ],
            'urgent_action': [
                r'\b(urgent|asap|immediately|emergency|critical|priority|deadline|rush)\b',
                r'\b(time sensitive|right away|as soon as possible|expedite)\b'
            ],
            'follow_up': [
                r'\b(follow up|follow-up|checking in|status|update|progress|reminder)\b',
                r'\b(following up|circling back|touching base)\b'
            ],
            'notification': [
                r'\b(notify|notification|alert|inform|update|announcement|notice)\b',
                r'\b(fyi|for your information|heads up|letting you know)\b'
            ],
            'approval': [
                r'\b(approve|approval|authorize|permission|consent|agree|accept)\b',
                r'\b(sign off|green light|go ahead|proceed)\b'
            ]
        }
    
    def _build_urgency_patterns(self) -> Dict[str, List[str]]:
        """Build urgency detection patterns"""
        return {
            'critical': [
                r'\b(emergency|urgent|asap|immediately|critical|crisis|disaster)\b',
                r'\b(failure|down|broken|not working|system failure)\b',
                r'\b(deadline today|due today|overdue|expired|final notice)\b'
            ],
            'high': [
                r'\b(soon|quickly|priority|important|deadline|due date|time-sensitive)\b',
                r'\b(prompt|expedite|rush|this week|tomorrow|by end of day|eod)\b',
                r'\b(before|until|by)\s+\d{1,2}[:/]\d{2}'
            ],
            'medium': [
                r'\b(when you can|at your convenience|next week|upcoming|planned)\b',
                r'\b(scheduled|reminder|follow up|checking in|status update)\b',
                r'\b(within.*days?|by.*week)\b'
            ]
        }
    
    def _get_stopwords(self) -> set:
        """Get comprehensive stopwords list"""
        return {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
            'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did',
            'will', 'would', 'could', 'should', 'can', 'may', 'might', 'must', 'shall', 'this', 'that',
            'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'
        }
    
    def analyze_email(self, subject: str, content: str) -> Dict[str, Any]:
        """
        Perform comprehensive email analysis
        
        Args:
            subject: Email subject line
            content: Email body content
            
        Returns:
            Complete analysis results with validation
        """
        try:
            full_text = f"{subject}\n\n{content}"
            
            # Core analysis components
            sentiment = self._analyze_sentiment(full_text)
            categories = self._categorize_email(full_text)
            intent = self._detect_intent(full_text)
            urgency = self._assess_urgency(full_text)
            keywords = self._extract_keywords(full_text)
            confidence = self._calculate_confidence(full_text, categories, sentiment, intent)
            
            # Advanced features
            topic = self._extract_topic(categories, keywords)
            suggested_labels = self._generate_labels(categories, intent, urgency, keywords)
            risk_flags = self._detect_risk_flags(full_text, confidence, urgency)
            reasoning = self._generate_reasoning(categories, sentiment, intent, urgency, confidence)
            
            # Create analysis result
            analysis = EmailAnalysis(
                topic=topic,
                sentiment=sentiment,
                intent=intent,
                urgency=urgency,
                confidence=confidence,
                categories=categories,
                keywords=keywords,
                reasoning=reasoning,
                suggested_labels=suggested_labels,
                risk_flags=risk_flags
            )
            
            # Validate accuracy
            validation = self._validate_accuracy(analysis, full_text)
            
            return {
                **analysis.to_dict(),
                'validation': {
                    'validation_method': validation.validation_method,
                    'score': validation.score,
                    'reliable': validation.reliable,
                    'feedback': validation.feedback
                }
            }
            
        except Exception as e:
            logger.error(f"Error in email analysis: {str(e)}")
            return self._get_fallback_analysis(str(e))
    
    def _analyze_sentiment(self, text: str) -> str:
        """Analyze sentiment using lexicon-based approach with context"""
        text_lower = text.lower()
        positive_score = 0.0
        negative_score = 0.0
        
        # Count weighted sentiment words
        for word, weight in self.sentiment_lexicon['positive'].items():
            count = len(re.findall(r'\b' + re.escape(word) + r'\b', text_lower))
            positive_score += count * weight
        
        for word, weight in self.sentiment_lexicon['negative'].items():
            count = len(re.findall(r'\b' + re.escape(word) + r'\b', text_lower))
            negative_score += count * weight
        
        # Consider negation patterns
        negation_patterns = [r'not\s+\w+', r'no\s+\w+', r'never\s+\w+', r"don't\s+\w+", r"won't\s+\w+"]
        negation_count = sum(len(re.findall(pattern, text_lower)) for pattern in negation_patterns)
        
        # Adjust scores based on negation
        if negation_count > 0:
            positive_score *= (1 - min(negation_count * 0.2, 0.8))
            negative_score *= (1 + min(negation_count * 0.1, 0.5))
        
        # Determine sentiment
        if positive_score > negative_score + 0.5:
            return 'positive'
        elif negative_score > positive_score + 0.5:
            return 'negative'
        else:
            return 'neutral'
    
    def _categorize_email(self, text: str) -> List[str]:
        """Categorize email using weighted pattern matching"""
        text_lower = text.lower()
        category_scores = {}
        
        for category, pattern_groups in self.category_patterns.items():
            total_score = 0.0
            
            for group in pattern_groups:
                group_score = 0.0
                weight = group.get('weight', 1.0)
                
                for pattern in group['patterns']:
                    matches = re.findall(pattern, text_lower)
                    group_score += len(matches)
                
                total_score += group_score * weight
            
            if total_score > 0:
                category_scores[category] = total_score
        
        # Return top categories (maximum 3)
        if not category_scores:
            return ['General']
        
        sorted_categories = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)
        return [cat for cat, score in sorted_categories[:3]]
    
    def _detect_intent(self, text: str) -> str:
        """Detect email intent using pattern matching"""
        text_lower = text.lower()
        intent_scores = {}
        
        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                matches = re.findall(pattern, text_lower)
                score += len(matches)
            
            if score > 0:
                intent_scores[intent] = score
        
        if not intent_scores:
            return 'informational'
        
        return max(intent_scores.items(), key=lambda x: x[1])[0]
    
    def _assess_urgency(self, text: str) -> str:
        """Assess email urgency level"""
        text_lower = text.lower()
        
        for urgency_level in ['critical', 'high', 'medium']:
            patterns = self.urgency_patterns[urgency_level]
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return urgency_level
        
        return 'low'
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords using TF-IDF-like scoring"""
        # Clean and tokenize
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        
        # Filter stopwords and count frequencies
        word_freq = Counter([word for word in words if word not in self.stopwords])
        
        # Extract named entities (simple approach)
        entities = []
        entity_patterns = [
            r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',  # Names
            r'\b[A-Z]{2,}\b',  # Acronyms
            r'\b\w+@\w+\.\w+\b',  # Emails
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',  # Dates
            r'\$[\d,]+(?:\.\d{2})?'  # Money
        ]
        
        for pattern in entity_patterns:
            entities.extend(re.findall(pattern, text))
        
        # Combine frequency-based keywords with entities
        top_words = [word for word, freq in word_freq.most_common(8)]
        
        # Remove duplicates and limit
        all_keywords = []
        seen = set()
        for item in entities[:3] + top_words:
            if item not in seen:
                all_keywords.append(item)
                seen.add(item)
        
        return all_keywords[:10]
    
    def _calculate_confidence(self, text: str, categories: List[str], sentiment: str, intent: str) -> float:
        """Calculate confidence score based on multiple factors"""
        base_confidence = 0.6
        
        # Text length factor
        text_length = len(text)
        if text_length > 500:
            length_factor = 0.2
        elif text_length > 200:
            length_factor = 0.1
        else:
            length_factor = 0.0
        
        # Category specificity factor
        if len(categories) == 1 and categories[0] != 'General':
            category_factor = 0.15
        elif len(categories) > 1 and 'General' not in categories:
            category_factor = 0.1
        else:
            category_factor = 0.0
        
        # Sentiment certainty factor
        sentiment_factor = 0.1 if sentiment != 'neutral' else 0.0
        
        # Intent specificity factor
        intent_factor = 0.1 if intent != 'informational' else 0.0
        
        confidence = base_confidence + length_factor + category_factor + sentiment_factor + intent_factor
        return min(confidence, 0.95)
    
    def _extract_topic(self, categories: List[str], keywords: List[str]) -> str:
        """Extract main topic from categories and keywords"""
        if categories and categories[0] != 'General':
            return categories[0]
        elif keywords:
            return f"Discussion about {keywords[0]}"
        else:
            return "General Communication"
    
    def _generate_labels(self, categories: List[str], intent: str, urgency: str, keywords: List[str]) -> List[str]:
        """Generate suggested labels for the email"""
        labels = []
        
        # Add category labels
        labels.extend(categories)
        
        # Add intent-based labels
        if intent != 'informational':
            intent_label = intent.replace('_', ' ').title()
            labels.append(intent_label)
        
        # Add urgency labels
        if urgency in ['high', 'critical']:
            labels.append(f"{urgency.title()} Priority")
        
        # Add content-based labels
        text_indicators = {
            'attachment': 'Has Attachment',
            'meeting': 'Meeting Request',
            'deadline': 'Time Sensitive',
            'follow up': 'Follow Up',
            'question': 'Requires Response'
        }
        
        for keyword in keywords:
            keyword_lower = keyword.lower()
            for indicator, label in text_indicators.items():
                if indicator in keyword_lower and label not in labels:
                    labels.append(label)
        
        # Remove duplicates and limit
        result = []
        seen = set()
        for label in labels:
            if label not in seen:
                result.append(label)
                seen.add(label)
        
        return result[:6]
    
    def _detect_risk_flags(self, text: str, confidence: float, urgency: str) -> List[str]:
        """Detect potential risk flags in the email"""
        flags = []
        
        # Low confidence flag
        if confidence < 0.5:
            flags.append('low_confidence')
        
        # Urgent content flag
        if urgency in ['high', 'critical']:
            flags.append('urgent_content')
        
        # Potential spam indicators
        spam_patterns = [
            r'\b(free|winner|congratulations|claim|prize|lottery)\b',
            r'\b(click here|act now|limited time|exclusive offer)\b',
            r'\b(nigerian prince|inheritance|lottery|sweepstakes)\b'
        ]
        
        text_lower = text.lower()
        spam_score = sum(len(re.findall(pattern, text_lower)) for pattern in spam_patterns)
        if spam_score > 2:
            flags.append('potential_spam')
        
        # Sensitive content indicators
        sensitive_patterns = [
            r'\b(confidential|classified|proprietary|secret)\b',
            r'\b(password|ssn|social security|credit card)\b',
            r'\b(legal|lawsuit|court|attorney|lawyer)\b'
        ]
        
        sensitive_score = sum(len(re.findall(pattern, text_lower)) for pattern in sensitive_patterns)
        if sensitive_score > 0:
            flags.append('sensitive_content')
        
        return flags
    
    def _generate_reasoning(self, categories: List[str], sentiment: str, intent: str, urgency: str, confidence: float) -> str:
        """Generate human-readable reasoning for the analysis"""
        parts = []
        
        if categories and categories[0] != 'General':
            parts.append(f"Categorized as {', '.join(categories)} based on content analysis")
        
        if sentiment != 'neutral':
            parts.append(f"Detected {sentiment} sentiment")
        
        if intent != 'informational':
            parts.append(f"Identified as {intent.replace('_', ' ')} intent")
        
        if urgency != 'low':
            parts.append(f"Marked as {urgency} urgency")
        
        confidence_desc = "high" if confidence > 0.8 else "medium" if confidence > 0.6 else "low"
        parts.append(f"Analysis confidence: {confidence_desc} ({confidence:.2f})")
        
        return ". ".join(parts) + "."
    
    def _validate_accuracy(self, analysis: EmailAnalysis, text: str) -> AccuracyValidation:
        """Validate the accuracy of the analysis"""
        validation_score = analysis.confidence
        
        # Additional validation checks
        consistency_score = self._check_internal_consistency(analysis, text)
        validation_score = (validation_score * 0.7) + (consistency_score * 0.3)
        
        reliable = validation_score >= self.accuracy_threshold
        
        feedback = (
            f"Analysis reliability: {'High' if reliable else 'Low'}. "
            f"Validation score: {validation_score:.2f}. "
            f"{'Meets' if reliable else 'Below'} accuracy threshold of {self.accuracy_threshold}."
        )
        
        return AccuracyValidation(
            validation_method='pattern_based_validation',
            score=validation_score,
            reliable=reliable,
            feedback=feedback
        )
    
    def _check_internal_consistency(self, analysis: EmailAnalysis, text: str) -> float:
        """Check internal consistency of the analysis"""
        consistency_score = 0.8  # Base score
        
        # Check if urgency matches intent
        if analysis.urgency in ['high', 'critical'] and analysis.intent == 'urgent_action':
            consistency_score += 0.1
        
        # Check if sentiment matches content tone
        negative_indicators = ['problem', 'issue', 'error', 'complaint', 'urgent']
        text_lower = text.lower()
        
        has_negative_content = any(indicator in text_lower for indicator in negative_indicators)
        if has_negative_content and analysis.sentiment == 'negative':
            consistency_score += 0.1
        elif not has_negative_content and analysis.sentiment == 'positive':
            consistency_score += 0.05
        
        return min(consistency_score, 1.0)
    
    def _get_fallback_analysis(self, error_msg: str) -> Dict[str, Any]:
        """Return fallback analysis in case of errors"""
        return {
            'topic': 'General',
            'sentiment': 'neutral',
            'intent': 'informational',
            'urgency': 'low',
            'confidence': 0.3,
            'categories': ['General'],
            'keywords': [],
            'reasoning': f'Fallback analysis due to error: {error_msg}',
            'suggested_labels': ['Needs Review'],
            'risk_flags': ['processing_error', 'low_confidence'],
            'validation': {
                'validation_method': 'fallback',
                'score': 0.3,
                'reliable': False,
                'feedback': 'Analysis failed, manual review required'
            }
        }

def main():
    """Main function for standalone execution"""
    if len(sys.argv) != 3:
        print(json.dumps({'error': 'Usage: python nlp_engine.py <subject> <content>'}))
        sys.exit(1)
    
    subject = sys.argv[1]
    content = sys.argv[2]
    
    engine = AdvancedNLPEngine()
    result = engine.analyze_email(subject, content)
    
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()