"""
Strategy generator for EmailIntelligence CLI

Implements logic for generating resolution strategies.
"""

from typing import List, Dict, Any
from ..core.interfaces import IResolutionStrategy
from ..core.conflict_models import Conflict, ResolutionStrategy, RiskLevel
from ..utils.logger import get_logger


logger = get_logger(__name__)


class StrategyGenerator(IResolutionStrategy):
    """
    Generates resolution strategies for conflicts.
    """
    
    def __init__(self):
        self.strategies = {}
    
    async def generate_resolution_strategy(self, conflicts: List[Conflict]) -> ResolutionStrategy:
        """
        Generate a resolution strategy for the given conflicts.
        
        Args:
            conflicts: List of conflicts to resolve
            
        Returns:
            Resolution strategy
        """
        logger.info(f"Generating resolution strategy for {len(conflicts)} conflicts")
        
        # Determine the overall strategy type based on conflict types and severity
        strategy_type = self._determine_strategy_type(conflicts)
        
        # Generate specific steps for each conflict
        steps = self._generate_resolution_steps(conflicts)
        
        # Estimate time based on conflict count and severity
        estimated_time = self._estimate_resolution_time(conflicts)
        
        # Assess risks
        risk_assessment = self._assess_resolution_risks(conflicts)
        
        strategy = ResolutionStrategy(
            strategy_type=strategy_type,
            steps=steps,
            estimated_time=estimated_time,
            risk_assessment=risk_assessment
        )
        
        logger.info(f"Resolution strategy generated: {strategy_type} with {len(steps)} steps")
        return strategy
    
    def _determine_strategy_type(self, conflicts: List[Conflict]) -> str:
        """Determine the appropriate strategy type based on conflicts."""
        if not conflicts:
            return "no_conflicts"
        
        # Count conflict types and severities
        severity_counts = {}
        type_counts = {}
        
        for conflict in conflicts:
            severity_counts[conflict.severity] = severity_counts.get(conflict.severity, 0) + 1
            type_counts[conflict.conflict_type] = type_counts.get(conflict.conflict_type, 0) + 1
        
        # Determine strategy based on highest severity
        if severity_counts.get(RiskLevel.CRITICAL, 0) > 0:
            return "critical_resolution"
        elif severity_counts.get(RiskLevel.HIGH, 0) > 0:
            return "high_priority_resolution"
        elif severity_counts.get(RiskLevel.MEDIUM, 0) > 0:
            return "standard_resolution"
        else:
            return "low_priority_resolution"
    
    def _generate_resolution_steps(self, conflicts: List[Conflict]) -> List[Dict[str, Any]]:
        """Generate specific steps for resolving conflicts."""
        steps = []
        
        for i, conflict in enumerate(conflicts):
            step = {
                "id": f"step_{i+1}",
                "conflict_file": conflict.file_path,
                "conflict_type": conflict.conflict_type.value,
                "severity": conflict.severity.value,
                "action": self._determine_action_for_conflict(conflict),
                "description": f"Resolve conflict in {conflict.file_path}",
                "dependencies": [],
                "estimated_time": conflict.estimated_resolution_time
            }
            steps.append(step)
        
        return steps
    
    def _determine_action_for_conflict(self, conflict: Conflict) -> str:
        """Determine the appropriate action for a specific conflict."""
        if conflict.conflict_type.value in ["binary", "SEMANTIC"]:
            return "manual_resolution"
        elif conflict.conflict_type.value == "ARCHITECTURAL":
            return "architectural_review"
        elif conflict.severity == RiskLevel.CRITICAL:
            return "expert_review"
        else:
            return "standard_merge"
    
    def _estimate_resolution_time(self, conflicts: List[Conflict]) -> int:
        """Estimate total resolution time."""
        if not conflicts:
            return 0
        
        # Base time calculation
        base_time = sum(c.estimated_resolution_time for c in conflicts)
        
        # Add overhead based on conflict count and severity
        overhead = len(conflicts) * 5  # 5 minutes per conflict for coordination
        
        # Add severity multiplier
        severity_multiplier = 1.0
        for conflict in conflicts:
            if conflict.severity == RiskLevel.CRITICAL:
                severity_multiplier *= 2.0
            elif conflict.severity == RiskLevel.HIGH:
                severity_multiplier *= 1.5
        
        total_time = int((base_time + overhead) * severity_multiplier)
        return max(total_time, 10)  # Minimum 10 minutes
    
    def _assess_resolution_risks(self, conflicts: List[Conflict]) -> Dict[str, Any]:
        """Assess risks associated with the resolution."""
        risk_assessment = {
            "overall_risk_level": self._determine_overall_risk_level(conflicts),
            "breaking_changes_risk": self._assess_breaking_changes_risk(conflicts),
            "performance_impact_risk": self._assess_performance_risk(conflicts),
            "security_risk": self._assess_security_risk(conflicts),
            "recommendations": self._generate_risk_recommendations(conflicts)
        }
        
        return risk_assessment
    
    def _determine_overall_risk_level(self, conflicts: List[Conflict]) -> str:
        """Determine the overall risk level."""
        if not conflicts:
            return "none"
        
        critical_count = sum(1 for c in conflicts if c.severity == RiskLevel.CRITICAL)
        high_count = sum(1 for c in conflicts if c.severity == RiskLevel.HIGH)
        
        if critical_count > 0:
            return "critical"
        elif high_count > 0:
            return "high"
        elif len(conflicts) > 5:
            return "medium"
        else:
            return "low"
    
    def _assess_breaking_changes_risk(self, conflicts: List[Conflict]) -> str:
        """Assess risk of breaking changes."""
        for conflict in conflicts:
            if "api" in conflict.file_path.lower() or "interface" in conflict.file_path.lower():
                return "high"
        
        return "medium" if len(conflicts) > 3 else "low"
    
    def _assess_performance_risk(self, conflicts: List[Conflict]) -> str:
        """Assess performance impact risk."""
        for conflict in conflicts:
            if "performance" in conflict.file_path.lower() or "cache" in conflict.file_path.lower():
                return "high"
        
        return "low"
    
    def _assess_security_risk(self, conflicts: List[Conflict]) -> str:
        """Assess security risk."""
        for conflict in conflicts:
            if "auth" in conflict.file_path.lower() or "security" in conflict.file_path.lower():
                return "high"
        
        return "medium" if len(conflicts) > 5 else "low"
    
    def _generate_risk_recommendations(self, conflicts: List[Conflict]) -> List[str]:
        """Generate risk mitigation recommendations."""
        recommendations = []
        
        if self._determine_overall_risk_level(conflicts) in ["high", "critical"]:
            recommendations.append("Perform thorough testing before merging")
            recommendations.append("Get additional code review")
        
        if self._assess_breaking_changes_risk(conflicts) == "high":
            recommendations.append("Update API documentation")
            recommendations.append("Check backward compatibility")
        
        if self._assess_security_risk(conflicts) == "high":
            recommendations.append("Perform security review")
            recommendations.append("Run security scanning tools")
        
        return recommendations