"""
Risk assessor for EmailIntelligence CLI

Implements logic for assessing risks in conflict resolution.
"""

from typing import List, Dict, Any
from ..core.conflict_models import Conflict, RiskLevel
from ..utils.logger import get_logger


logger = get_logger(__name__)


class RiskAssessor:
    """
    Assesses risks associated with conflicts and their resolution.
    """
    
    def __init__(self):
        self.risk_factors = {
            "file_type": {
                "critical": ["auth", "security", "config", "database", "api"],
                "high": ["model", "core", "engine", "service"],
                "medium": ["util", "helper", "test"],
                "low": ["docs", "readme", "example"]
            },
            "change_type": {
                "critical": ["delete", "rename"],
                "high": ["modify", "refactor"],
                "medium": ["add", "update"],
                "low": ["comment", "format"]
            }
        }
    
    def assess_conflict_risks(self, conflicts: List[Conflict]) -> Dict[str, Any]:
        """
        Assess risks for a list of conflicts.
        
        Args:
            conflicts: List of conflicts to assess
            
        Returns:
            Risk assessment results
        """
        logger.info(f"Assessing risks for {len(conflicts)} conflicts")
        
        risk_summary = {
            "total_conflicts": len(conflicts),
            "by_severity": self._categorize_by_severity(conflicts),
            "by_type": self._categorize_by_type(conflicts),
            "critical_files": self._identify_critical_files(conflicts),
            "risk_score": self._calculate_overall_risk_score(conflicts),
            "risk_level": self._determine_overall_risk_level(conflicts),
            "mitigation_strategies": self._generate_mitigation_strategies(conflicts),
            "recommendations": self._generate_recommendations(conflicts)
        }
        
        logger.info(f"Risk assessment completed. Overall risk level: {risk_summary['risk_level']}")
        return risk_summary
    
    def _categorize_by_severity(self, conflicts: List[Conflict]) -> Dict[str, int]:
        """Categorize conflicts by severity."""
        severity_counts = {}
        for conflict in conflicts:
            severity = conflict.severity.value
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        return severity_counts
    
    def _categorize_by_type(self, conflicts: List[Conflict]) -> Dict[str, int]:
        """Categorize conflicts by type."""
        type_counts = {}
        for conflict in conflicts:
            conflict_type = conflict.conflict_type.value
            type_counts[conflict_type] = type_counts.get(conflict_type, 0) + 1
        return type_counts
    
    def _identify_critical_files(self, conflicts: List[Conflict]) -> List[str]:
        """Identify critical files that appear in conflicts."""
        critical_files = []
        
        for conflict in conflicts:
            file_path = conflict.file_path.lower()
            
            # Check if file is critical based on name
            for critical_indicator in self.risk_factors["file_type"]["critical"]:
                if critical_indicator in file_path:
                    critical_files.append(conflict.file_path)
                    break
        
        return list(set(critical_files))  # Remove duplicates
    
    def _calculate_overall_risk_score(self, conflicts: List[Conflict]) -> float:
        """Calculate an overall risk score (0.0 to 1.0)."""
        if not conflicts:
            return 0.0
        
        total_score = 0.0
        for conflict in conflicts:
            # Assign scores based on severity
            if conflict.severity == RiskLevel.CRITICAL:
                total_score += 1.0
            elif conflict.severity == RiskLevel.HIGH:
                total_score += 0.7
            elif conflict.severity == RiskLevel.MEDIUM:
                total_score += 0.4
            else:  # LOW
                total_score += 0.1
        
        # Normalize to 0-1 range
        return min(1.0, total_score / len(conflicts))
    
    def _determine_overall_risk_level(self, conflicts: List[Conflict]) -> str:
        """Determine the overall risk level."""
        if not conflicts:
            return "none"
        
        risk_score = self._calculate_overall_risk_score(conflicts)
        
        if risk_score >= 0.8:
            return "critical"
        elif risk_score >= 0.6:
            return "high"
        elif risk_score >= 0.4:
            return "medium"
        else:
            return "low"
    
    def _generate_mitigation_strategies(self, conflicts: List[Conflict]) -> List[Dict[str, str]]:
        """Generate mitigation strategies for the conflicts."""
        strategies = []
        
        # Add general strategies based on overall risk
        overall_risk = self._determine_overall_risk_level(conflicts)
        
        if overall_risk in ["critical", "high"]:
            strategies.append({
                "strategy": "thorough_testing",
                "description": "Perform comprehensive testing including unit, integration, and end-to-end tests"
            })
            strategies.append({
                "strategy": "peer_review",
                "description": "Require additional peer review before merging"
            })
        
        if "critical" in [c.severity.value for c in conflicts]:
            strategies.append({
                "strategy": "staged_rollout",
                "description": "Consider staged rollout to minimize impact"
            })
        
        # Add file-specific strategies
        critical_files = self._identify_critical_files(conflicts)
        if critical_files:
            strategies.append({
                "strategy": "security_review",
                "description": f"Perform security review for critical files: {', '.join(critical_files)}"
            })
        
        return strategies
    
    def _generate_recommendations(self, conflicts: List[Conflict]) -> List[str]:
        """Generate recommendations based on the conflicts."""
        recommendations = []
        
        # Add recommendations based on conflict types
        conflict_types = [c.conflict_type.value for c in conflicts]
        if "SEMANTIC" in conflict_types:
            recommendations.append("Ensure semantic compatibility between changes")
        if "ARCHITECTURAL" in conflict_types:
            recommendations.append("Review architectural implications of changes")
        if "BINARY" in conflict_types:
            recommendations.append("Manually resolve binary file conflicts")
        
        # Add recommendations based on severity
        if any(c.severity == RiskLevel.CRITICAL for c in conflicts):
            recommendations.append("Prioritize resolution of critical conflicts")
        if any(c.severity == RiskLevel.HIGH for c in conflicts):
            recommendations.append("Address high severity conflicts before merging")
        
        # Add general recommendations
        if len(conflicts) > 5:
            recommendations.append("Consider breaking changes into smaller, more manageable PRs")
        
        if not recommendations:
            recommendations.append("Standard conflict resolution process applies")
        
        return recommendations
    
    def assess_resolution_risk(self, strategy: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess risks associated with a particular resolution strategy.
        
        Args:
            strategy: The resolution strategy to assess
            
        Returns:
            Risk assessment for the strategy
        """
        logger.info("Assessing risks for resolution strategy")
        
        strategy_risks = {
            "complexity_risk": self._assess_complexity_risk(strategy),
            "time_risk": self._assess_time_risk(strategy),
            "quality_risk": self._assess_quality_risk(strategy),
            "overall_strategy_risk": self._calculate_strategy_risk_score(strategy)
        }
        
        return strategy_risks
    
    def _assess_complexity_risk(self, strategy: Dict[str, Any]) -> str:
        """Assess complexity risk of the strategy."""
        steps = strategy.get("steps", [])
        if len(steps) > 10:
            return "high"
        elif len(steps) > 5:
            return "medium"
        else:
            return "low"
    
    def _assess_time_risk(self, strategy: Dict[str, Any]) -> str:
        """Assess time-related risks of the strategy."""
        estimated_time = strategy.get("estimated_time", 0)
        if estimated_time > 240:  # More than 4 hours
            return "high"
        elif estimated_time > 120:  # More than 2 hours
            return "medium"
        else:
            return "low"
    
    def _assess_quality_risk(self, strategy: Dict[str, Any]) -> str:
        """Assess quality risks of the strategy."""
        strategy_type = strategy.get("strategy_type", "")
        if strategy_type in ["critical_resolution", "high_priority_resolution"]:
            return "high"
        elif strategy_type in ["standard_resolution"]:
            return "medium"
        else:
            return "low"
    
    def _calculate_strategy_risk_score(self, strategy: Dict[str, Any]) -> float:
        """Calculate an overall risk score for the strategy."""
        # This is a simplified calculation - in a real system, this would be more sophisticated
        complexity_risk = {"low": 0.2, "medium": 0.5, "high": 0.8}[self._assess_complexity_risk(strategy)]
        time_risk = {"low": 0.1, "medium": 0.4, "high": 0.7}[self._assess_time_risk(strategy)]
        quality_risk = {"low": 0.1, "medium": 0.4, "high": 0.8}[self._assess_quality_risk(strategy)]
        
        # Weighted average
        return (complexity_risk * 0.5 + time_risk * 0.3 + quality_risk * 0.2)