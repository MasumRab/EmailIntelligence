#!/usr/bin/env python3

"""
Speckit Checklist Command

Implements the /speckit.checkist command to generate checklists based on 
user feedback and system requirements for the Email Intelligence platform.
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Add project root to sys.path for imports
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.ai_engine import ModernAIEngine as AIEngine
from src.core.database import DatabaseManager
from backend.python_nlp.nlp_engine import NLPEngine

logger = logging.getLogger(__name__)

class SpeckitCheckist:
    """Speckit Checklist Command Implementation"""
    
    def __init__(self, db_manager: Optional[DatabaseManager] = None, 
                 ai_engine: Optional[AIEngine] = None):
        self.db_manager = db_manager or DatabaseManager()
        self.ai_engine = ai_engine or AIEngine()
        # Initialize NLP engine with error handling
        try:
            self.nlp_engine = NLPEngine()
        except Exception as e:
            logger.warning(f"Could not initialize NLP engine: {e}")
            self.nlp_engine = None
        
    def execute(self, user_feedback: Optional[str] = None, 
                checklist_type: str = "development",
                output_format: str = "json") -> Dict[str, Any]:
        """
        Execute the speckit checkist command.
        
        Args:
            user_feedback: Optional user feedback to generate checklist from
            checklist_type: Type of checklist to generate (development, review, deployment, feedback)
            output_format: Output format (json, text, markdown)
            
        Returns:
            Checklist in specified format
        """
        logger.info(f"Executing speckit.checkist with type: {checklist_type}")
        
        checklist_results = {
            "timestamp": datetime.now().isoformat(),
            "checklist_type": checklist_type,
            "generated_from_feedback": user_feedback is not None,
            "checklist": []
        }
        
        if checklist_type == "feedback":
            if user_feedback:
                checklist = self._generate_feedback_driven_checklist(user_feedback)
            else:
                checklist = self._generate_default_feedback_checklist()
        elif checklist_type == "development":
            checklist = self._generate_development_checklist()
        elif checklist_type == "review":
            checklist = self._generate_review_checklist()
        elif checklist_type == "deployment":
            checklist = self._generate_deployment_checklist()
        else:
            checklist = self._generate_default_checklist()
        
        checklist_results["checklist"] = checklist
        
        return self._format_output(checklist_results, output_format)
    
    def _generate_feedback_driven_checklist(self, feedback: str) -> List[Dict[str, Any]]:
        """Generate a checklist based on user feedback."""
        logger.info("Generating feedback-driven checklist...")
        
        # Analyze feedback to identify issues and improvement areas
        themes = self._extract_themes_from_feedback(feedback)
        sentiment = self._analyze_sentiment_from_feedback(feedback)
        
        checklist = []
        
        # Generate checklist items based on identified themes
        if "performance" in themes:
            checklist.extend([
                {"item": "Review application performance", "category": "performance", "priority": "high"},
                {"item": "Optimize database queries", "category": "performance", "priority": "medium"},
                {"item": "Check for memory leaks", "category": "performance", "priority": "medium"}
            ])
        
        if "usability" in themes:
            checklist.extend([
                {"item": "Review user interface design", "category": "usability", "priority": "high"},
                {"item": "Test user workflow efficiency", "category": "usability", "priority": "medium"},
                {"item": "Check accessibility features", "category": "usability", "priority": "low"}
            ])
        
        if "bugs" in themes:
            checklist.extend([
                {"item": "Identify and fix reported bugs", "category": "bug_fixes", "priority": "high"},
                {"item": "Add error handling for common issues", "category": "bug_fixes", "priority": "medium"},
                {"item": "Improve logging for debugging", "category": "bug_fixes", "priority": "low"}
            ])
        
        if "features" in themes:
            checklist.extend([
                {"item": "Review requested feature implementation", "category": "features", "priority": "high"},
                {"item": "Plan feature development timeline", "category": "features", "priority": "medium"},
                {"item": "Consider feature dependencies", "category": "features", "priority": "low"}
            ])
        
        # Add general items based on sentiment
        if sentiment == "negative":
            checklist.append({
                "item": "Conduct comprehensive user experience review", 
                "category": "ux", 
                "priority": "high"
            })
        elif sentiment == "positive":
            checklist.append({
                "item": "Document successful approaches for future reference", 
                "category": "documentation", 
                "priority": "medium"
            })
        
        # If no specific themes identified, add general checklist items
        if not checklist:
            checklist = self._generate_default_checklist()
        
        return checklist
    
    def _generate_default_feedback_checklist(self) -> List[Dict[str, Any]]:
        """Generate a default feedback checklist when no specific feedback is provided."""
        return [
            {"item": "Collect user feedback on current implementation", "category": "feedback", "priority": "high"},
            {"item": "Analyze user satisfaction metrics", "category": "feedback", "priority": "medium"},
            {"item": "Review feature usage statistics", "category": "feedback", "priority": "medium"},
            {"item": "Identify areas for improvement based on user behavior", "category": "feedback", "priority": "high"}
        ]
    
    def _generate_development_checklist(self) -> List[Dict[str, Any]]:
        """Generate a development checklist."""
        return [
            {"item": "Set up development environment", "category": "setup", "priority": "high"},
            {"item": "Install dependencies", "category": "setup", "priority": "high"},
            {"item": "Configure code editor", "category": "setup", "priority": "medium"},
            {"item": "Review project architecture", "category": "development", "priority": "high"},
            {"item": "Understand existing codebase", "category": "development", "priority": "high"},
            {"item": "Plan implementation approach", "category": "development", "priority": "medium"},
            {"item": "Write unit tests", "category": "testing", "priority": "high"},
            {"item": "Implement functionality", "category": "development", "priority": "high"},
            {"item": "Perform code review", "category": "review", "priority": "high"},
            {"item": "Run integration tests", "category": "testing", "priority": "high"},
            {"item": "Update documentation", "category": "documentation", "priority": "medium"}
        ]
    
    def _generate_review_checklist(self) -> List[Dict[str, Any]]:
        """Generate a code review checklist."""
        return [
            {"item": "Check for adherence to coding standards", "category": "code_quality", "priority": "high"},
            {"item": "Review security practices", "category": "security", "priority": "high"},
            {"item": "Verify error handling implementation", "category": "reliability", "priority": "high"},
            {"item": "Check for performance implications", "category": "performance", "priority": "medium"},
            {"item": "Validate input sanitization", "category": "security", "priority": "high"},
            {"item": "Review database queries", "category": "performance", "priority": "medium"},
            {"item": "Check for memory leaks", "category": "reliability", "priority": "medium"},
            {"item": "Verify proper logging", "category": "reliability", "priority": "medium"},
            {"item": "Test with edge cases", "category": "testing", "priority": "high"},
            {"item": "Confirm documentation is up to date", "category": "documentation", "priority": "low"}
        ]
    
    def _generate_deployment_checklist(self) -> List[Dict[str, Any]]:
        """Generate a deployment checklist."""
        return [
            {"item": "Verify environment variables are set", "category": "configuration", "priority": "high"},
            {"item": "Check database connection", "category": "configuration", "priority": "high"},
            {"item": "Validate API keys and credentials", "category": "security", "priority": "high"},
            {"item": "Run pre-deployment tests", "category": "testing", "priority": "high"},
            {"item": "Check system resource availability", "category": "infrastructure", "priority": "high"},
            {"item": "Verify backup procedures", "category": "safety", "priority": "medium"},
            {"item": "Test rollback procedures", "category": "safety", "priority": "medium"},
            {"item": "Monitor system performance after deployment", "category": "monitoring", "priority": "high"},
            {"item": "Validate user access and permissions", "category": "security", "priority": "high"},
            {"item": "Confirm monitoring and alerting systems are active", "category": "monitoring", "priority": "medium"}
        ]
    
    def _generate_default_checklist(self) -> List[Dict[str, Any]]:
        """Generate a default checklist."""
        return [
            {"item": "Define project requirements", "category": "planning", "priority": "high"},
            {"item": "Design system architecture", "category": "planning", "priority": "high"},
            {"item": "Set up development environment", "category": "setup", "priority": "high"},
            {"item": "Implement core functionality", "category": "development", "priority": "high"},
            {"item": "Write comprehensive tests", "category": "testing", "priority": "high"},
            {"item": "Perform security review", "category": "security", "priority": "high"},
            {"item": "Document the implementation", "category": "documentation", "priority": "medium"},
            {"item": "Deploy to staging environment", "category": "deployment", "priority": "medium"},
            {"item": "Conduct user acceptance testing", "category": "testing", "priority": "high"},
            {"item": "Deploy to production", "category": "deployment", "priority": "high"}
        ]
    
    def _extract_themes_from_feedback(self, feedback: str) -> List[str]:
        """Extract key themes from user feedback."""
        # Use NLP to extract themes
        try:
            # This would use the NLP engine to identify themes
            # For now, we'll simulate this with simple keyword matching
            themes = []
            theme_keywords = {
                "performance": ["slow", "fast", "speed", "performance", "efficiency"],
                "usability": ["interface", "easy", "difficult", "user-friendly", "hard"],
                "features": ["feature", "functionality", "capability", "ability"],
                "bugs": ["bug", "error", "issue", "problem", "crash", "break"]
            }
            
            feedback_lower = feedback.lower()
            for theme, keywords in theme_keywords.items():
                if any(keyword in feedback_lower for keyword in keywords):
                    themes.append(theme)
                    
            return themes
        except Exception as e:
            logger.error(f"Error extracting themes: {e}")
            return ["general"]
    
    def _analyze_sentiment_from_feedback(self, feedback: str) -> str:
        """Analyze sentiment from user feedback."""
        # Fallback sentiment analysis
        positive_words = ["good", "great", "excellent", "amazing", "love", "perfect", "fantastic"]
        negative_words = ["bad", "terrible", "awful", "hate", "worst", "horrible", "disappointing"]
        
        feedback_lower = feedback.lower()
        pos_count = sum(1 for word in positive_words if word in feedback_lower)
        neg_count = sum(1 for word in negative_words if word in feedback_lower)
        
        if pos_count > neg_count:
            return "positive"
        elif neg_count > pos_count:
            return "negative"
        else:
            return "neutral"
    
    def _format_output(self, checklist_results: Dict[str, Any], 
                      output_format: str) -> Dict[str, Any]:
        """Format the checklist results according to specified format."""
        if output_format == "json":
            return checklist_results
        elif output_format == "text":
            return {"text_output": self._to_text(checklist_results)}
        elif output_format == "markdown":
            return {"markdown_output": self._to_markdown(checklist_results)}
        else:
            return checklist_results
    
    def _to_text(self, checklist_results: Dict[str, Any]) -> str:
        """Convert checklist results to text format."""
        text = f"Speckit Checklist Report\n"
        text += f"Timestamp: {checklist_results['timestamp']}\n"
        text += f"Checklist Type: {checklist_results['checklist_type']}\n\n"
        
        text += "Checklist Items:\n"
        for i, item in enumerate(checklist_results['checklist'], 1):
            text += f"{i}. [{item.get('priority', 'medium')}] {item['item']} (Category: {item.get('category', 'general')})\n"
        
        return text
    
    def _to_markdown(self, checklist_results: Dict[str, Any]) -> str:
        """Convert checklist results to markdown format."""
        md = f"# Speckit Checklist Report\n\n"
        md += f"**Timestamp:** {checklist_results['timestamp']}\n"
        md += f"**Checklist Type:** {checklist_results['checklist_type']}\n\n"
        
        md += "## Checklist\n\n"
        for item in checklist_results['checklist']:
            priority = item.get('priority', 'medium')
            category = item.get('category', 'general')
            md += f"- [{priority.upper()}] {item['item']} *(Category: {category})*\n"
        
        return md


def speckit_checkist(user_feedback: Optional[str] = None, 
                    checklist_type: str = "development",
                    output_format: str = "json") -> Dict[str, Any]:
    """
    Execute the speckit checkist command.
    
    Args:
        user_feedback: Optional user feedback to generate checklist from
        checklist_type: Type of checklist to generate (development, review, deployment, feedback)
        output_format: Output format (json, text, markdown)
        
    Returns:
        Checklist in specified format
    """
    checkister = SpeckitCheckist()
    return checkister.execute(user_feedback, checklist_type, output_format)
