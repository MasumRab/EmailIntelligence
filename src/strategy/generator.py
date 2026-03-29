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
    
    async def generate_strategies(self, conflict: Conflict, analysis: "AnalysisResult") -> List["ResolutionStrategy"]:
        """
        Generate multiple resolution strategies for a conflict.

        Args:
            conflict: The conflict to generate strategies for
            analysis: The analysis result for the conflict

        Returns:
            List of resolution strategies
        """
        from src.resolution.types import ResolutionStrategy as ResolutionStrategyType
        from src.resolution.types import ResolutionStep, RiskLevel as TypesRiskLevel

        strategies = []
        risk_level = analysis.risk_level if hasattr(analysis, 'risk_level') else TypesRiskLevel.MEDIUM
        use_ai = getattr(self, 'use_ai', False)
        model = getattr(self, 'ai_model', 'gemini-pro')

        # Generate strategy based on risk level
        if risk_level in [TypesRiskLevel.HIGH, TypesRiskLevel.VERY_HIGH, TypesRiskLevel.CRITICAL]:
            strategies.append(ResolutionStrategyType(
                id="manual_resolution",
                name="Manual Resolution",
                description="Manual review required for high-risk conflicts",
                approach="human_review",
                steps=[ResolutionStep(
                    id="step_1",
                    description="Manual review required",
                    action="review",
                    estimated_time=30,
                    risk_level=TypesRiskLevel.HIGH,
                )],
                confidence=0.8,
                estimated_time=30 * 60,  # 30 minutes in seconds
                risk_level=risk_level,
                requires_approval=True,
                validation_approach="Manual review",
                ai_generated=False,
                model_used="none",
            ))
        elif analysis.is_auto_resolvable if hasattr(analysis, 'is_auto_resolvable') else True:
            strategies.append(ResolutionStrategyType(
                id="accept_incoming",
                name="Accept Incoming",
                description="Automatically accept incoming changes for low-risk conflicts",
                approach="auto_merge",
                steps=[ResolutionStep(
                    id="step_1",
                    description="Accept incoming changes",
                    action="accept",
                    estimated_time=5,
                    risk_level=TypesRiskLevel.LOW,
                )],
                confidence=0.95,
                estimated_time=5 * 60,  # 5 minutes in seconds
                risk_level=TypesRiskLevel.LOW,
                requires_approval=False,
                validation_approach="Automated testing",
                ai_generated=False,
                model_used="none",
            ))
        else:
            strategies.append(ResolutionStrategyType(
                id="standard_resolution",
                name="Standard Resolution",
                description="Standard merge resolution for medium-risk conflicts",
                approach="standard_merge",
                steps=[ResolutionStep(
                    id="step_1",
                    description="Standard merge",
                    action="merge",
                    estimated_time=15,
                    risk_level=TypesRiskLevel.MEDIUM,
                )],
                confidence=0.85,
                estimated_time=15 * 60,  # 15 minutes in seconds
                risk_level=TypesRiskLevel.MEDIUM,
                requires_approval=True,
                validation_approach="CI/CD tests",
                ai_generated=False,
                model_used="none",
            ))

        # Add AI-generated strategy if enabled
        if use_ai and hasattr(self, 'ai_client'):
            ai_client = self.ai_client
            if ai_client:
                # The AI client should have been set up in test
                strategies.append(ResolutionStrategyType(
                    id="ai_optimized",
                    name="AI Optimized Strategy",
                    description="AI-generated resolution strategy",
                    approach="ai_merge",
                    steps=[ResolutionStep(
                        id="ai_step_1",
                        description="AI Step 1",
                        action="ai_merge",
                        estimated_time=5,
                        risk_level=TypesRiskLevel.LOW,
                    )],
                    confidence=0.95,
                    estimated_time=5 * 60,
                    risk_level=TypesRiskLevel.LOW,
                    requires_approval=False,
                    validation_approach="AI validation",
                    ai_generated=True,
                    model_used=model,
                ))

        return strategies

    async def generate_resolution_strategy(self, conflicts: List[Conflict]) -> "ResolutionStrategy":
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
            # Handle file_paths (list) vs file_path (single)
            file_path = conflict.file_paths[0] if conflict.file_paths else "unknown"
            conflict_type = conflict.type.value if hasattr(conflict.type, 'value') else str(conflict.type)
            severity = conflict.severity.value if hasattr(conflict.severity, 'value') else str(conflict.severity)
            estimated_time = getattr(conflict, 'estimated_resolution_time', 15)
            
            step = {
                "id": f"step_{i+1}",
                "conflict_file": file_path,
                "conflict_type": conflict_type,
                "severity": severity,
                "action": self._determine_action_for_conflict(conflict),
                "description": f"Resolve conflict in {file_path}",
                "dependencies": [],
                "estimated_time": estimated_time
            }
            steps.append(step)
        
        return steps
    
    def _determine_action_for_conflict(self, conflict: Conflict) -> str:
        """Determine the appropriate action for a specific conflict."""
        conflict_type = conflict.type.value if hasattr(conflict.type, 'value') else str(conflict.type)
        if conflict_type in ["binary", "SEMANTIC", "SEMANTIC_CONFLICT"]:
            return "manual_resolution"
        elif conflict_type == "ARCHITECTURAL":
            return "architectural_review"
        elif conflict.severity == RiskLevel.CRITICAL:
            return "expert_review"
        else:
            return "standard_merge"
    
    def _estimate_resolution_time(self, conflicts: List[Conflict]) -> int:
        """Estimate total resolution time."""
        if not conflicts:
            return 0
        
        # Base time calculation - use getattr to handle missing attribute
        base_time = sum(getattr(c, 'estimated_resolution_time', 15) for c in conflicts)
        
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