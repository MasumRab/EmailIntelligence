"""
Speckit Analyse Command

Implements the /speckit.analyse command to analyze user feedback and codebase.
This module provides functionality to analyze feedback, identify patterns, 
and generate insights for the Email Intelligence platform.
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


class SpeckitAnalyse:
    """Speckit Analyse Command Implementation"""
    
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
                analysis_type: str = "comprehensive",
                output_format: str = "json") -> Dict[str, Any]:
        """
        Execute the speckit analyse command.
        
        Args:
            user_feedback: Optional user feedback to analyze
            analysis_type: Type of analysis to perform (comprehensive, feedback, codebase)
            output_format: Output format (json, text, markdown)
            
        Returns:
            Analysis results
        """
        logger.info(f"Executing speckit.analyse with type: {analysis_type}")
        
        analysis_results = {
            "timestamp": datetime.now().isoformat(),
            "analysis_type": analysis_type,
            "results": {}
        }
        
        if analysis_type in ["comprehensive", "feedback"]:
            if user_feedback:
                feedback_analysis = self._analyze_user_feedback(user_feedback)
                analysis_results["results"]["feedback_analysis"] = feedback_analysis
            else:
                # Analyze stored feedback if no explicit feedback provided
                feedback_analysis = self._analyze_stored_feedback()
                analysis_results["results"]["feedback_analysis"] = feedback_analysis
        
        if analysis_type in ["comprehensive", "codebase"]:
            codebase_analysis = self._analyze_codebase()
            analysis_results["results"]["codebase_analysis"] = codebase_analysis
            
        return self._format_output(analysis_results, output_format)
    
    def _analyze_user_feedback(self, feedback: str) -> Dict[str, Any]:
        """Analyze provided user feedback."""
        logger.info("Analyzing user feedback...")
        
        # Use NLP engine to analyze feedback if available
        if self.nlp_engine is not None:
            try:
                feedback_analysis = self.nlp_engine.analyze_email_text(feedback, feedback)
            except Exception:
                feedback_analysis = {"error": "NLP engine not available"}
                logger.warning("NLP engine analysis failed, using fallback")
        else:
            feedback_analysis = {"error": "NLP engine not available"}
            logger.warning("NLP engine not initialized, using fallback")
        
        # Extract key themes, sentiments, and issues from feedback
        themes = self._extract_themes_from_feedback(feedback)
        sentiment = self._analyze_sentiment_from_feedback(feedback)
        
        return {
            "raw_feedback": feedback,
            "nlp_analysis": feedback_analysis,
            "themes": themes,
            "sentiment": sentiment,
            "actionable_insights": self._generate_actionable_insights(themes, sentiment)
        }
    
    def _analyze_stored_feedback(self) -> Dict[str, Any]:
        """Analyze stored user feedback from the database."""
        logger.info("Analyzing stored user feedback...")
        
        try:
            # Attempt to get feedback from database
            feedback_records = []
            # This is a placeholder - actual implementation would depend on your schema
            # For now, we'll return a default analysis
            return {
                "message": "No stored feedback analysis available - this would connect to your feedback database",
                "placeholder": True
            }
        except Exception as e:
            logger.error(f"Error analyzing stored feedback: {e}")
            return {"error": str(e)}
    
    def _analyze_codebase(self) -> Dict[str, Any]:
        """Analyze the current codebase."""
        logger.info("Analyzing codebase...")
        
        # Get project structure and key metrics
        project_path = Path(__file__).resolve().parent.parent.parent
        
        analysis = {
            "project_structure": self._get_project_structure(project_path),
            "file_count": self._count_files(project_path),
            "recent_changes": self._get_recent_changes(project_path),
            "potential_improvements": self._identify_potential_improvements()
        }
        
        return analysis
    
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
    
    def _generate_actionable_insights(self, themes: List[str], sentiment: str) -> List[str]:
        """Generate actionable insights from analysis."""
        insights = []
        
        if "performance" in themes:
            insights.append("Consider optimizing performance based on user feedback")
        
        if "usability" in themes:
            insights.append("Review user interface and experience based on feedback")
        
        if "bugs" in themes:
            insights.append("Address reported issues and bugs")
        
        if sentiment == "negative":
            insights.append("Prioritize addressing user concerns")
        elif sentiment == "positive":
            insights.append("Continue with current successful approaches")
        
        return insights
    
    def _get_project_structure(self, project_path: Path) -> Dict[str, Any]:
        """Get the project structure."""
        structure = {}
        for item in project_path.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                # Limit depth to avoid too much information
                if item.name in ['backend', 'client', 'src', 'modules']:
                    structure[item.name] = self._get_subdirs(item, depth=2)
                else:
                    structure[item.name] = "directory"
            elif item.is_file() and item.suffix in ['.py', '.md', '.json', '.yml', '.yaml']:
                structure[item.name] = "file"
        
        return structure
    
    def _get_subdirs(self, path: Path, depth: int = 2) -> Dict[str, Any]:
        """Get subdirectories recursively up to a certain depth."""
        if depth <= 0:
            return "directory"
        
        result = {}
        for item in path.iterdir():
            if item.is_dir():
                result[item.name] = self._get_subdirs(item, depth - 1)
            elif item.is_file():
                if item.suffix in ['.py', '.md', '.json', '.yml', '.yaml']:
                    result[item.name] = "file"
        return result
    
    def _count_files(self, project_path: Path) -> Dict[str, int]:
        """Count different types of files in the project."""
        counts = {
            "python": 0,
            "javascript": 0,
            "typescript": 0,
            "markdown": 0,
            "config": 0,
            "total": 0
        }
        
        for file_path in project_path.rglob('*'):
            if file_path.is_file():
                counts["total"] += 1
                if file_path.suffix == '.py':
                    counts["python"] += 1
                elif file_path.suffix in ['.js', '.jsx']:
                    counts["javascript"] += 1
                elif file_path.suffix in ['.ts', '.tsx']:
                    counts["typescript"] += 1
                elif file_path.suffix == '.md':
                    counts["markdown"] += 1
                elif file_path.suffix in ['.json', '.yml', '.yaml', '.toml']:
                    counts["config"] += 1
        
        return counts
    
    def _get_recent_changes(self, project_path: Path) -> List[str]:
        """Get recent changes (would typically interface with git)."""
        try:
            # This would interface with git to get recent changes
            # For now, we'll return a placeholder
            return ["Recent changes analysis would require git integration"]
        except Exception:
            return ["Unable to retrieve recent changes"]
    
    def _identify_potential_improvements(self) -> List[str]:
        """Identify potential improvements in the codebase."""
        # This would perform static analysis to identify potential improvements
        # For now, we'll return a placeholder list
        return [
            "Review error handling in critical components",
            "Consider adding more comprehensive logging",
            "Evaluate performance optimization opportunities",
            "Review security best practices implementation"
        ]
    
    def _format_output(self, analysis_results: Dict[str, Any], 
                      output_format: str) -> Dict[str, Any]:
        """Format the analysis results according to specified format."""
        if output_format == "json":
            return analysis_results
        elif output_format == "text":
            return {"text_output": json.dumps(analysis_results, indent=2)}
        elif output_format == "markdown":
            return {"markdown_output": self._to_markdown(analysis_results)}
        else:
            return analysis_results
    
    def _to_markdown(self, analysis_results: Dict[str, Any]) -> str:
        """Convert analysis results to markdown format."""
        md = f"# Speckit Analysis Report\n\n"
        md += f"**Timestamp:** {analysis_results['timestamp']}\n\n"
        md += f"## Analysis Type: {analysis_results['analysis_type']}\n\n"
        
        results = analysis_results.get("results", {})
        
        if "feedback_analysis" in results:
            feedback = results["feedback_analysis"]
            md += "## Feedback Analysis\n\n"
            md += f"- **Sentiment:** {feedback.get('sentiment', 'N/A')}\n"
            md += f"- **Themes:** {', '.join(feedback.get('themes', []))}\n"
            md += f"- **Actionable Insights:\n"
            for insight in feedback.get('actionable_insights', []):
                md += f"  - {insight}\n"
            md += "\n"
        
        if "codebase_analysis" in results:
            codebase = results["codebase_analysis"]
            md += "## Codebase Analysis\n\n"
            md += f"- **Total Files:** {codebase.get('file_count', {}).get('total', 'N/A')}\n"
            md += f"- **Python Files:** {codebase.get('file_count', {}).get('python', 'N/A')}\n"
            md += f"- **Potential Improvements:\n"
            for improvement in codebase.get('potential_improvements', []):
                md += f"  - {improvement}\n"
            md += "\n"
        
        return md


def speckit_analyse(user_feedback: Optional[str] = None, 
                   analysis_type: str = "comprehensive",
                   output_format: str = "json") -> Dict[str, Any]:
    """
    Execute the speckit analyse command.
    
    Args:
        user_feedback: Optional user feedback to analyze
        analysis_type: Type of analysis to perform (comprehensive, feedback, codebase)
        output_format: Output format (json, text, markdown)
        
    Returns:
        Analysis results
    """
    analyser = SpeckitAnalyse()
    return analyser.execute(user_feedback, analysis_type, output_format)
