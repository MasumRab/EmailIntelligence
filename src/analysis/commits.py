
"""
Commit analysis and classification module.
"""

import re
from typing import List, Dict
from ..git.history import Commit
from ..resolution.types import RiskLevel

class CommitClassifier:
    """
    Classifies commits based on conventional commits and risk keywords.
    """
    
    PATTERNS = {
        "feat": r"^feat(\(.*\))?:",
        "fix": r"^fix(\(.*\))?:",
        "docs": r"^docs(\(.*\))?:",
        "style": r"^style(\(.*\))?:",
        "refactor": r"^refactor(\(.*\))?:",
        "perf": r"^perf(\(.*\))?:",
        "test": r"^test(\(.*\))?:",
        "chore": r"^chore(\(.*\))?:",
        "build": r"^build(\(.*\))?:",
        "ci": r"^ci(\(.*\))?:",
        "revert": r"^revert:",
    }
    
    RISK_KEYWORDS = {
        "security": RiskLevel.CRITICAL,
        "auth": RiskLevel.HIGH,
        "login": RiskLevel.HIGH,
        "database": RiskLevel.HIGH,
        "migration": RiskLevel.HIGH,
        "api": RiskLevel.MEDIUM,
        "config": RiskLevel.MEDIUM,
    }
    
    def classify(self, commit: Commit) -> Commit:
        """
        Classify a single commit.
        """
        # 1. Determine Category
        commit.category = "other"
        for cat, pattern in self.PATTERNS.items():
            if re.match(pattern, commit.message):
                commit.category = cat
                break
        
        if commit.is_merge:
            commit.category = "merge"
            
        # 2. Assess Risk
        commit.risk_level = RiskLevel.LOW.value
        
        # Check keywords
        msg_lower = commit.message.lower()
        for keyword, level in self.RISK_KEYWORDS.items():
            if keyword in msg_lower:
                # Upgrade risk if higher
                current_risk = RiskLevel(commit.risk_level)
                if self._risk_value(level) > self._risk_value(current_risk):
                    commit.risk_level = level.value
                    
        # Category based risk adjustments
        if commit.category == "feat":
            if commit.risk_level == RiskLevel.LOW.value:
                commit.risk_level = RiskLevel.MEDIUM.value
        elif commit.category in ["docs", "style", "test"]:
             commit.risk_level = RiskLevel.VERY_LOW.value
             
        return commit
        
    def _risk_value(self, level: RiskLevel) -> int:
        """Helper to compare risk levels"""
        levels = [
            RiskLevel.VERY_LOW, 
            RiskLevel.LOW, 
            RiskLevel.MEDIUM, 
            RiskLevel.HIGH, 
            RiskLevel.VERY_HIGH, 
            RiskLevel.CRITICAL
        ]
        return levels.index(level)

    def analyze_history(self, commits: List[Commit]) -> Dict[str, int]:
        """
        Analyze a list of commits and return statistics.
        """
        stats = {
            "total": len(commits),
            "by_category": {},
            "by_risk": {}
        }
        
        for commit in commits:
            self.classify(commit)
            
            # Count category
            stats["by_category"][commit.category] = stats["by_category"].get(commit.category, 0) + 1
            
            # Count risk
            stats["by_risk"][commit.risk_level] = stats["by_risk"].get(commit.risk_level, 0) + 1
            
        return stats
