"""
Rule-based model provider for Email Intelligence Platform
"""

import asyncio
import logging
import time
from typing import Any, Dict, List, Optional

from .model_provider import BaseModelProvider

logger = logging.getLogger(__name__)


class RuleBasedModelProvider(BaseModelProvider):
    """
    Rule-based model provider that uses simple heuristics for analysis.
    
    This provider serves as a fallback when more sophisticated models
    are not available or as a baseline for comparison.
    """
    
    def __init__(self):
        self._initialized = True
        self._model_info = {
            "name": "Rule-Based Model Provider",
            "version": "1.0.0",
            "type": "rule-based",
            "description": "Simple rule-based analysis using heuristics"
        }
        logger.info("RuleBasedModelProvider initialized")
    
    async def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment using rule-based heuristics.
        """
        start_time = time.time()
        
        # Convert to lowercase for analysis
        text_lower = text.lower()
        
        # Define sentiment keywords
        positive_keywords = [
            "good", "great", "excellent", "amazing", "wonderful", "fantastic", 
            "awesome", "brilliant", "perfect", "love", "like", "enjoy", 
            "happy", "pleased", "satisfied", "thank", "appreciate", "grateful"
        ]
        
        negative_keywords = [
            "bad", "terrible", "awful", "horrible", "disgusting", "hate", 
            "dislike", "hated", "disliked", "angry", "sad", "upset", 
            "frustrated", "disappointed", "annoyed", "problem", "issue", 
            "complaint", "sorry", "concern"
        ]
        
        # Count positive and negative words
        positive_count = sum(1 for word in positive_keywords if word in text_lower)
        negative_count = sum(1 for word in negative_keywords if word in text_lower)
        
        # Determine sentiment based on counts
        if positive_count > negative_count:
            sentiment = "positive"
            confidence = min(0.5 + (positive_count - negative_count) * 0.1, 1.0)
        elif negative_count > positive_count:
            sentiment = "negative"
            confidence = min(0.5 + (negative_count - positive_count) * 0.1, 1.0)
        else:
            sentiment = "neutral"
            confidence = 0.5
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        return {
            "sentiment": sentiment,
            "confidence": confidence,
            "positive_words_found": positive_count,
            "negative_words_found": negative_count,
            "processing_time": processing_time,
            "method_used": "rule-based"
        }
    
    async def analyze_topics(self, text: str) -> Dict[str, Any]:
        """
        Analyze topics using rule-based heuristics.
        """
        start_time = time.time()
        
        text_lower = text.lower()
        
        # Define topic keywords
        topic_keywords = {
            "work": ["meeting", "project", "deadline", "office", "work", "business", 
                    "task", "colleague", "boss", "employee", "company", "job"],
            "finance": ["payment", "invoice", "bill", "account", "money", "bank", 
                       "finance", "transaction", "budget", "expense", "salary", "loan"],
            "healthcare": ["doctor", "medical", "appointment", "health", "clinic", 
                          "hospital", "medicine", "patient", "treatment", "symptom"],
            "personal": ["family", "friend", "home", "relationship", "personal", 
                        "private", "vacation", "holiday", "party", "celebration"],
            "technical": ["software", "code", "bug", "server", "database", "api", 
                         "system", "computer", "technology", "programming", "network"],
            "legal": ["contract", "agreement", "law", "legal", "court", "attorney", 
                     "document", "terms", "policy", "compliance", "regulation"],
            "education": ["school", "university", "student", "teacher", "class", 
                         "course", "education", "learning", "study", "assignment"]
        }
        
        # Find topics based on keyword matches
        topics_found = []
        topic_confidences = {}
        
        for topic, keywords in topic_keywords.items():
            matches = sum(1 for word in keywords if word in text_lower)
            if matches > 0:
                topics_found.append(topic)
                # Calculate confidence based on number of matches
                topic_confidences[topic] = min(matches * 0.2, 1.0)
        
        # If no topics found, default to general
        if not topics_found:
            topics_found = ["general"]
            topic_confidences["general"] = 0.3
        
        # Sort topics by confidence
        sorted_topics = sorted(topics_found, key=lambda x: topic_confidences[x], reverse=True)
        
        processing_time = time.time() - start_time
        
        return {
            "topics": sorted_topics[:3],  # Return top 3 topics
            "topic_confidences": {topic: topic_confidences[topic] for topic in sorted_topics[:3]},
            "processing_time": processing_time,
            "method_used": "rule-based"
        }
    
    async def analyze_intent(self, text: str) -> Dict[str, Any]:
        """
        Analyze intent using rule-based heuristics.
        """
        start_time = time.time()
        
        text_lower = text.lower()
        
        # Define intent patterns
        intent_patterns = {
            "question": ["?", "what", "how", "when", "where", "why", "which", "who", "whom", "whose"],
            "request": ["please", "can you", "would you", "could you", "help", "assist", "support"],
            "confirmation": ["yes", "ok", "okay", "alright", "sure", "indeed", "agreed"],
            "negation": ["no", "not", "never", "nothing", "nowhere", "nobody", "none"],
            "apology": ["sorry", "apologize", "apology", "excuse", "forgive", "pardon"],
            "gratitude": ["thank", "thanks", "appreciate", "grateful", "appreciative", "gratitude"],
            "complaint": ["problem", "issue", "error", "mistake", "wrong", "incorrect", "defect"],
            "information": ["information", "details", "data", "facts", "knowledge", "learn"]
        }
        
        # Count intent pattern matches
        intent_counts = {}
        for intent, patterns in intent_patterns.items():
            matches = sum(1 for pattern in patterns if pattern in text_lower)
            if matches > 0:
                intent_counts[intent] = matches
        
        # Determine primary intent
        if intent_counts:
            primary_intent = max(intent_counts, key=intent_counts.get)
            confidence = min(intent_counts[primary_intent] * 0.3, 1.0)
        else:
            primary_intent = "information"
            confidence = 0.3
        
        processing_time = time.time() - start_time
        
        return {
            "intent": primary_intent,
            "confidence": confidence,
            "intent_counts": intent_counts,
            "processing_time": processing_time,
            "method_used": "rule-based"
        }
    
    async def analyze_urgency(self, text: str) -> Dict[str, Any]:
        """
        Analyze urgency using rule-based heuristics.
        """
        start_time = time.time()
        
        text_lower = text.lower()
        
        # Define urgency indicators
        urgency_indicators = [
            "urgent", "asap", "immediately", "right now", "today", "within 24 hours",
            "deadline", "due", "expedited", "rush", "emergency", "critical", "vital",
            "important", "priority", "top priority", "high priority", "expedite",
            "at your earliest convenience", "please respond immediately"
        ]
        
        # Count urgency indicators
        urgency_count = sum(1 for indicator in urgency_indicators if indicator in text_lower)
        
        # Determine urgency level
        if urgency_count >= 3:
            urgency_level = "high"
            confidence = min(0.6 + urgency_count * 0.1, 1.0)
        elif urgency_count >= 1:
            urgency_level = "medium"
            confidence = min(0.4 + urgency_count * 0.1, 1.0)
        else:
            urgency_level = "low"
            confidence = 0.4
        
        processing_time = time.time() - start_time
        
        return {
            "urgency": urgency_level,
            "confidence": confidence,
            "urgency_indicators_found": urgency_count,
            "processing_time": processing_time,
            "method_used": "rule-based"
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Perform a health check of the rule-based provider.
        """
        start_time = time.time()
        
        # Perform a simple test
        test_text = "This is a test message for health check"
        try:
            sentiment_result = await self.analyze_sentiment(test_text)
            topic_result = await self.analyze_topics(test_text)
            intent_result = await self.analyze_intent(test_text)
            urgency_result = await self.analyze_urgency(test_text)
            
            processing_time = time.time() - start_time
            
            return {
                "status": "healthy",
                "provider_info": self._model_info,
                "test_results": {
                    "sentiment_test": sentiment_result["sentiment"],
                    "topic_test": topic_result["topics"][:1],
                    "intent_test": intent_result["intent"],
                    "urgency_test": urgency_result["urgency"]
                },
                "processing_time": processing_time,
                "timestamp": time.time()
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "provider_info": self._model_info,
                "error": str(e),
                "timestamp": time.time()
            }
    
    def get_provider_info(self) -> Dict[str, Any]:
        """
        Get information about the provider.
        """
        return self._model_info