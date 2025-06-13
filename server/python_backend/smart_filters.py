
"""
Smart filtering system for email management
Advanced filtering with AI-powered categorization
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass
import re

logger = logging.getLogger(__name__)

@dataclass
class EmailFilter:
    """Email filter configuration"""
    name: str
    description: str
    criteria: Dict[str, Any]
    action: str
    priority: int
    enabled: bool = True
    
@dataclass
class FilterResult:
    """Filter application result"""
    matched: bool
    filter_name: str
    action_taken: str
    confidence: float
    metadata: Dict[str, Any]

class SmartFilterManager:
    """Smart email filtering with AI integration"""
    
    def __init__(self):
        self.filters = []
        self.filter_stats = {}
        self.load_default_filters()
    
    def load_default_filters(self):
        """Load default smart filters"""
        self.filters = [
            EmailFilter(
                name="High Priority Work",
                description="Important work emails requiring immediate attention",
                criteria={
                    "urgency": ["high", "critical"],
                    "categories": ["Work & Business"],
                    "keywords": ["urgent", "asap", "deadline", "meeting", "project"],
                    "sender_patterns": ["@company.com", "@work.org"]
                },
                action="set_priority_high",
                priority=10
            ),
            EmailFilter(
                name="Financial Alerts",
                description="Banking and financial notifications",
                criteria={
                    "categories": ["Finance & Banking"],
                    "keywords": ["payment", "transaction", "invoice", "statement", "alert"],
                    "urgency": ["medium", "high", "critical"]
                },
                action="set_category_finance",
                priority=9
            ),
            EmailFilter(
                name="Healthcare Appointments",
                description="Medical appointments and health reminders",
                criteria={
                    "categories": ["Healthcare"],
                    "keywords": ["appointment", "reminder", "medical", "doctor", "clinic"],
                    "intent": ["scheduling", "confirmation"]
                },
                action="set_category_health",
                priority=8
            ),
            EmailFilter(
                name="Travel Confirmations",
                description="Travel bookings and confirmations",
                criteria={
                    "categories": ["Travel"],
                    "keywords": ["confirmation", "booking", "flight", "hotel", "itinerary"],
                    "sender_patterns": ["@airline.", "@hotel.", "@booking."]
                },
                action="set_category_travel",
                priority=7
            ),
            EmailFilter(
                name="Promotional Content",
                description="Marketing and promotional emails",
                criteria={
                    "categories": ["Promotions"],
                    "keywords": ["sale", "discount", "offer", "promotion", "deal"],
                    "sentiment": ["positive"],
                    "confidence_threshold": 0.7
                },
                action="set_low_priority",
                priority=3
            ),
            EmailFilter(
                name="Personal Communications",
                description="Personal emails from friends and family",
                criteria={
                    "categories": ["Personal & Family"],
                    "sentiment": ["positive", "neutral"],
                    "not_keywords": ["unsubscribe", "promotion", "marketing"]
                },
                action="set_category_personal",
                priority=6
            ),
            EmailFilter(
                name="Spam Detection",
                description="Potential spam and unwanted emails",
                criteria={
                    "risk_flags": ["potential_spam"],
                    "keywords": ["winner", "claim", "lottery", "prize", "congratulations"],
                    "confidence_threshold": 0.5
                },
                action="mark_as_spam",
                priority=1
            ),
            EmailFilter(
                name="Newsletter Management",
                description="Newsletter and subscription emails",
                criteria={
                    "keywords": ["newsletter", "unsubscribe", "subscription", "weekly"],
                    "sender_patterns": ["@newsletter.", "@mail.", "noreply@"],
                    "categories": ["Promotions", "General"]
                },
                action="set_category_newsletter",
                priority=4
            )
        ]
    
    async def apply_filters_to_email(self, email_data: Dict[str, Any]) -> List[FilterResult]:
        """Apply all filters to an email"""
        results = []
        
        # Sort filters by priority (highest first)
        sorted_filters = sorted(self.filters, key=lambda f: f.priority, reverse=True)
        
        for filter_config in sorted_filters:
            if not filter_config.enabled:
                continue
            
            result = await self.apply_single_filter(email_data, filter_config)
            if result.matched:
                results.append(result)
                
                # Update filter statistics
                self._update_filter_stats(filter_config.name, True)
                
                # Stop at first match for certain high-priority actions
                if filter_config.action in ["mark_as_spam", "set_priority_high"]:
                    break
            else:
                self._update_filter_stats(filter_config.name, False)
        
        return results
    
    async def apply_single_filter(self, email_data: Dict[str, Any], 
                                filter_config: EmailFilter) -> FilterResult:
        """Apply a single filter to an email"""
        criteria = filter_config.criteria
        matched = True
        confidence = 1.0
        metadata = {}
        
        # Check urgency criteria
        if "urgency" in criteria:
            email_urgency = email_data.get("urgency", "low")
            if email_urgency not in criteria["urgency"]:
                matched = False
        
        # Check category criteria
        if "categories" in criteria and matched:
            email_categories = email_data.get("categories", [])
            if not any(cat in criteria["categories"] for cat in email_categories):
                matched = False
        
        # Check keyword criteria
        if "keywords" in criteria and matched:
            email_text = f"{email_data.get('subject', '')} {email_data.get('content', '')}"
            keyword_matches = self._check_keywords(email_text, criteria["keywords"])
            if not keyword_matches["found"]:
                matched = False
            else:
                confidence *= keyword_matches["confidence"]
                metadata["keyword_matches"] = keyword_matches["matches"]
        
        # Check negative keywords
        if "not_keywords" in criteria and matched:
            email_text = f"{email_data.get('subject', '')} {email_data.get('content', '')}"
            negative_matches = self._check_keywords(email_text, criteria["not_keywords"])
            if negative_matches["found"]:
                matched = False
                metadata["negative_matches"] = negative_matches["matches"]
        
        # Check sender patterns
        if "sender_patterns" in criteria and matched:
            sender_email = email_data.get("sender_email", "")
            sender_matches = self._check_sender_patterns(sender_email, criteria["sender_patterns"])
            if not sender_matches["found"]:
                matched = False
            else:
                metadata["sender_matches"] = sender_matches["patterns"]
        
        # Check sentiment criteria
        if "sentiment" in criteria and matched:
            email_sentiment = email_data.get("sentiment", "neutral")
            if email_sentiment not in criteria["sentiment"]:
                matched = False
        
        # Check intent criteria
        if "intent" in criteria and matched:
            email_intent = email_data.get("intent", "informational")
            if email_intent not in criteria["intent"]:
                matched = False
        
        # Check risk flags
        if "risk_flags" in criteria and matched:
            email_risk_flags = email_data.get("risk_flags", [])
            if not any(flag in criteria["risk_flags"] for flag in email_risk_flags):
                matched = False
        
        # Check confidence threshold
        if "confidence_threshold" in criteria and matched:
            email_confidence = email_data.get("confidence", 0.0)
            if email_confidence < criteria["confidence_threshold"]:
                confidence *= 0.5  # Reduce confidence but don't exclude
        
        action_taken = ""
        if matched:
            action_taken = await self._execute_filter_action(email_data, filter_config.action)
        
        return FilterResult(
            matched=matched,
            filter_name=filter_config.name,
            action_taken=action_taken,
            confidence=confidence,
            metadata=metadata
        )
    
    def _check_keywords(self, text: str, keywords: List[str]) -> Dict[str, Any]:
        """Check for keyword matches in text"""
        text_lower = text.lower()
        matches = []
        
        for keyword in keywords:
            if keyword.lower() in text_lower:
                matches.append(keyword)
        
        confidence = len(matches) / len(keywords) if keywords else 0.0
        
        return {
            "found": len(matches) > 0,
            "matches": matches,
            "confidence": min(confidence + 0.3, 1.0)  # Boost confidence
        }
    
    def _check_sender_patterns(self, sender_email: str, patterns: List[str]) -> Dict[str, Any]:
        """Check sender email against patterns"""
        matches = []
        
        for pattern in patterns:
            if pattern in sender_email.lower():
                matches.append(pattern)
        
        return {
            "found": len(matches) > 0,
            "patterns": matches
        }
    
    async def _execute_filter_action(self, email_data: Dict[str, Any], action: str) -> str:
        """Execute filter action"""
        actions_taken = []
        
        if action == "set_priority_high":
            email_data["priority"] = "high"
            actions_taken.append("Set priority to high")
        
        elif action == "set_category_finance":
            email_data["category_name_override"] = "Finance & Banking"
            actions_taken.append("Categorized as Finance & Banking")
        
        elif action == "set_category_health":
            email_data["category_name_override"] = "Healthcare"
            actions_taken.append("Categorized as Healthcare")
        
        elif action == "set_category_travel":
            email_data["category_name_override"] = "Travel"
            actions_taken.append("Categorized as Travel")
        
        elif action == "set_category_personal":
            email_data["category_name_override"] = "Personal & Family"
            actions_taken.append("Categorized as Personal & Family")
        
        elif action == "set_low_priority":
            email_data["priority"] = "low"
            actions_taken.append("Set priority to low")
        
        elif action == "mark_as_spam":
            email_data["is_spam"] = True
            email_data["priority"] = "low"
            actions_taken.append("Marked as spam")
        
        elif action == "set_category_newsletter":
            # Assuming "Newsletter" is a sub-category or a label, and "Promotions" is the general category.
            # If "Newsletter" should be a main category, this would be: email_data["category_name_override"] = "Newsletter"
            # For now, let's assume "Promotions" is the target main category for newsletters if not overridden by AI.
            email_data["category_name_override"] = "Promotions"
            email_data["labels"] = email_data.get("labels", []) + ["Newsletter"]
            actions_taken.append("Categorized as Promotions (Newsletter)")
        
        return "; ".join(actions_taken)
    
    def _update_filter_stats(self, filter_name: str, matched: bool):
        """Update filter statistics"""
        if filter_name not in self.filter_stats:
            self.filter_stats[filter_name] = {
                "total_applied": 0,
                "total_matched": 0,
                "last_used": None
            }
        
        self.filter_stats[filter_name]["total_applied"] += 1
        if matched:
            self.filter_stats[filter_name]["total_matched"] += 1
        self.filter_stats[filter_name]["last_used"] = datetime.now().isoformat()
    
    def get_filter_stats(self) -> Dict[str, Any]:
        """Get filter performance statistics"""
        stats = {}
        
        for filter_name, data in self.filter_stats.items():
            match_rate = 0.0
            if data["total_applied"] > 0:
                match_rate = data["total_matched"] / data["total_applied"]
            
            stats[filter_name] = {
                "total_applied": data["total_applied"],
                "total_matched": data["total_matched"],
                "match_rate": match_rate,
                "last_used": data["last_used"]
            }
        
        return stats
    
    def add_custom_filter(self, filter_config: EmailFilter):
        """Add a custom filter"""
        self.filters.append(filter_config)
        logger.info(f"Added custom filter: {filter_config.name}")
    
    def remove_filter(self, filter_name: str) -> bool:
        """Remove a filter by name"""
        for i, filter_config in enumerate(self.filters):
            if filter_config.name == filter_name:
                del self.filters[i]
                logger.info(f"Removed filter: {filter_name}")
                return True
        return False
    
    def enable_filter(self, filter_name: str) -> bool:
        """Enable a filter"""
        for filter_config in self.filters:
            if filter_config.name == filter_name:
                filter_config.enabled = True
                logger.info(f"Enabled filter: {filter_name}")
                return True
        return False
    
    def disable_filter(self, filter_name: str) -> bool:
        """Disable a filter"""
        for filter_config in self.filters:
            if filter_config.name == filter_name:
                filter_config.enabled = False
                logger.info(f"Disabled filter: {filter_name}")
                return True
        return False
    
    def get_filters(self) -> List[Dict[str, Any]]:
        """Get all filters"""
        return [
            {
                "name": f.name,
                "description": f.description,
                "criteria": f.criteria,
                "action": f.action,
                "priority": f.priority,
                "enabled": f.enabled
            }
            for f in self.filters
        ]
    
    async def optimize_filters(self) -> Dict[str, Any]:
        """Optimize filter performance based on usage statistics"""
        optimization_results = {
            "filters_analyzed": len(self.filters),
            "optimizations_applied": [],
            "recommendations": []
        }
        
        for filter_config in self.filters:
            stats = self.filter_stats.get(filter_config.name, {})
            
            # Disable filters with very low match rates
            if stats.get("total_applied", 0) > 100:
                match_rate = stats.get("total_matched", 0) / stats["total_applied"]
                if match_rate < 0.05:  # Less than 5% match rate
                    filter_config.enabled = False
                    optimization_results["optimizations_applied"].append(
                        f"Disabled {filter_config.name} due to low match rate ({match_rate:.2%})"
                    )
            
            # Suggest priority adjustments
            if stats.get("total_matched", 0) > 1000:
                optimization_results["recommendations"].append(
                    f"Consider increasing priority for {filter_config.name} (high usage)"
                )
        
        return optimization_results

async def main():
    """Example usage of smart filter manager"""
    filter_manager = SmartFilterManager()
    
    # Sample email data
    sample_email = {
        "subject": "Urgent: Project deadline approaching",
        "content": "Please review the project deliverables ASAP. The client meeting is tomorrow.",
        "sender_email": "manager@company.com",
        "urgency": "high",
        "categories": ["Work & Business"],
        "sentiment": "neutral",
        "intent": "urgent_action",
        "confidence": 0.85,
        "risk_flags": []
    }
    
    # Apply filters
    results = await filter_manager.apply_filters_to_email(sample_email)
    
    print(f"Applied {len(results)} filters:")
    for result in results:
        print(f"- {result.filter_name}: {result.action_taken} (confidence: {result.confidence:.2f})")
    
    # Get filter stats
    stats = filter_manager.get_filter_stats()
    print(f"\nFilter statistics: {len(stats)} filters tracked")

if __name__ == "__main__":
    asyncio.run(main())
