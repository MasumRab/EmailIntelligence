"""
Constitutional Engine for EmailIntelligence PR Resolution

This module provides constitutional validation and compliance checking
for specification templates, resolution strategies, and execution phases
following the Spec Kit methodology.

Key Features:
- Constitutional rule loading and validation
- Specification template compliance checking
- Resolution strategy phase validation
- Constitutional scoring integration
- Rule violation detection and classification
- Compliance reporting and recommendations
"""

import json
import os
import re
from typing import Dict, List, Any, Optional, Union, Set, Tuple
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum
import structlog

from .types import (
    MergeConflict,
    DependencyConflict,
    ArchitectureViolation,
    ResolutionStrategy,
)

logger = structlog.get_logger()


class ViolationType(Enum):
    """Types of constitutional violations"""

    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"
    WARNING = "warning"
    INFO = "info"


class ComplianceLevel(Enum):
    """Constitutional compliance levels"""

    FULL_COMPLIANCE = "full_compliance"
    MINOR_VIOLATIONS = "minor_violations"
    MAJOR_VIOLATIONS = "major_violations"
    CRITICAL_VIOLATIONS = "critical_violations"
    NON_COMPLIANT = "non_compliant"


@dataclass
class ConstitutionalRule:
    """Constitutional rule definition"""

    id: str
    name: str
    description: str
    category: str
    violation_type: ViolationType
    rule_pattern: str
    severity_score: float  # 0.0-1.0
    auto_fixable: bool
    remediation_guide: str
    examples: List[str]
    dependencies: List[str]  # Rule dependencies
    phase_applications: List[str]  # Which phases this rule applies to


@dataclass
class ViolationResult:
    """Constitutional violation result"""

    rule_id: str
    rule_name: str
    violation_type: ViolationType
    severity_score: float
    description: str
    location: str
    context: str
    remediation: str
    auto_fixable: bool
    confidence: float  # 0.0-1.0


@dataclass
class ComplianceResult:
    """Constitutional compliance analysis result"""

    overall_score: float  # 0.0-1.0
    compliance_level: ComplianceLevel
    violations: List[ViolationResult]
    recommendations: List[str]
    passed_rules: List[str]
    failed_rules: List[str]
    analysis_timestamp: datetime
    analysis_context: Dict[str, Any]


@dataclass
class RegistrationResult:
    """Result of constitutional rule registration"""

    success: bool
    registered_rules: List[str]
    failed_rules: List[str]


class ConstitutionalEngine:
    """
    Constitutional validation engine for EmailIntelligence

    Provides constitutional compliance checking for:
    - Specification templates and plans
    - Resolution strategy generation and execution
    - Multi-phase workflow compliance
    - Rule violation detection and classification
    """

    def __init__(self, constitutions_dir: str = "constitutions"):
        """
        Initialize the constitutional engine

        Args:
            constitutions_dir: Directory containing constitutional rules
        """
        self.constitutions_dir = constitutions_dir
        self.rules: Dict[str, ConstitutionalRule] = {}
        self.rule_categories: Set[str] = set()
        self.compliance_history: List[ComplianceResult] = []
        self.violation_patterns: Dict[str, re.Pattern] = {}

        logger.info("Constitutional engine initialized", constitutions_dir=constitutions_dir)

    async def initialize(self) -> bool:
        """Initialize the constitutional engine and load rules"""
        try:
            await self._load_constitutional_rules()
            await self._compile_rule_patterns()
            logger.info(
                "Constitutional engine loaded successfully",
                rule_count=len(self.rules),
                categories=list(self.rule_categories),
            )
            return True
        except Exception as e:
            logger.error("Failed to initialize constitutional engine", error=str(e))
            return False

    def register_constitutional_rules(self, rules: List[ConstitutionalRule]) -> RegistrationResult:
        """Register new constitutional rules"""
        registered_ids = []
        failed_ids = []

        for rule in rules:
            self.rules[rule.id] = rule
            self.rule_categories.add(rule.category)
            try:
                self.violation_patterns[rule.id] = re.compile(
                    rule.rule_pattern, re.MULTILINE | re.IGNORECASE
                )
                registered_ids.append(rule.id)
            except re.error as e:
                logger.error("Failed to compile rule pattern", rule_id=rule.id, error=str(e))
                failed_ids.append(rule.id)

        return RegistrationResult(
            success=len(failed_ids) == 0,
            registered_rules=registered_ids,
            failed_rules=failed_ids,
        )

    async def validate_template(self, template_data: Dict[str, Any]) -> ComplianceResult:
        """Generic template validation for tests"""
        if template_data is None:
            raise ValueError("Template data cannot be None")

        # Convert dict to string for pattern matching if needed
        content_str = json.dumps(template_data, indent=2)

        # Determine template type from data or default
        template_type = template_data.get("template_metadata", {}).get("template_type", "unknown")

        return await self.validate_specification_template(
            template_content=content_str,
            template_type=template_type,
            context={"source": "test"},
        )

    async def batch_validate_templates(
        self, templates: List[Dict[str, Any]]
    ) -> List[ComplianceResult]:
        """Batch validate multiple templates"""
        import asyncio

        tasks = [self.validate_template(template) for template in templates]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        final_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error("Template validation failed in batch", index=i, error=str(result))
                # Create a failure result
                failure_result = ComplianceResult(
                    overall_score=0.0,
                    compliance_level=ComplianceLevel.NON_COMPLIANT,
                    violations=[
                        ViolationResult(
                            rule_id="validation_error",
                            rule_name="Validation Error",
                            violation_type=ViolationType.CRITICAL,
                            severity_score=1.0,
                            description=f"Validation failed with error: {str(result)}",
                            location="batch_validation",
                            context=f"Template index: {i}",
                            remediation="Check template format and engine logs",
                            auto_fixable=False,
                            confidence=1.0,
                        )
                    ],
                    recommendations=["Fix template format errors"],
                    passed_rules=[],
                    failed_rules=[],
                    analysis_timestamp=datetime.utcnow(),
                    analysis_context={"error": str(result)},
                )
                final_results.append(failure_result)
            else:
                final_results.append(result)

        return final_results

    async def load_constitutional_rules_from_directory(self, directory: str) -> None:
        """Load rules from a specific directory"""
        self.constitutions_dir = directory
        await self.initialize()

    def get_validation_statistics(self) -> Dict[str, Any]:
        """Get validation statistics"""
        stats = {
            "total_validations": len(self.compliance_history),
            "successful_validations": len([r for r in self.compliance_history if not r.violations]),
            "violation_count": sum(len(r.violations) for r in self.compliance_history),
            "average_processing_time": 0.0,  # Placeholder
        }
        return stats

    async def validate_specification_template(
        self, template_content: str, template_type: str, context: Dict[str, Any]
    ) -> ComplianceResult:
        """
        Validate a specification template against constitutional rules

        Args:
            template_content: Content of the specification template
            template_type: Type of template (spec.md, plan.md, etc.)
            context: Additional context for validation

        Returns:
            ComplianceResult with detailed analysis
        """
        logger.info("Validating specification template", template_type=template_type)

        violations = []
        passed_rules = []
        failed_rules = []

        # Load applicable rules for specification templates
        applicable_rules = self._get_applicable_rules("specification_template", template_type)

        for rule in applicable_rules:
            try:
                violation = await self._check_rule_compliance(
                    rule, template_content, "specification_template", context
                )

                if violation:
                    violations.append(violation)
                    failed_rules.append(rule.id)
                else:
                    passed_rules.append(rule.id)

            except Exception as e:
                logger.error("Rule validation failed", rule_id=rule.id, error=str(e))
                failed_rules.append(rule.id)

        # Generate compliance score
        overall_score = self._calculate_compliance_score(violations, len(applicable_rules))
        compliance_level = self._determine_compliance_level(violations)

        # Generate recommendations
        recommendations = self._generate_recommendations(violations, "specification_template")

        result = ComplianceResult(
            overall_score=overall_score,
            compliance_level=compliance_level,
            violations=violations,
            recommendations=recommendations,
            passed_rules=passed_rules,
            failed_rules=failed_rules,
            analysis_timestamp=datetime.utcnow(),
            analysis_context={
                "template_type": template_type,
                "template_length": len(template_content),
                "rule_count": len(applicable_rules),
            },
        )

        self.compliance_history.append(result)
        logger.info(
            "Specification template validation completed",
            overall_score=overall_score,
            violation_count=len(violations),
        )

        return result

    async def validate_resolution_strategy(
        self,
        strategy: ResolutionStrategy,
        conflict_data: Union[MergeConflict, DependencyConflict, ArchitectureViolation],
        execution_phase: str,
        context: Dict[str, Any],
    ) -> ComplianceResult:
        """
        Validate a resolution strategy against constitutional rules

        Args:
            strategy: Resolution strategy to validate
            conflict_data: Original conflict data
            execution_phase: Current execution phase
            context: Additional context for validation

        Returns:
            ComplianceResult with detailed analysis
        """
        logger.info(
            "Validating resolution strategy",
            strategy_id=strategy.id,
            execution_phase=execution_phase,
        )

        violations = []
        passed_rules = []
        failed_rules = []

        # Convert strategy to dict for pattern matching
        strategy_dict = asdict(strategy)
        strategy_json = json.dumps(strategy_dict, indent=2)

        # Load applicable rules for resolution strategies
        applicable_rules = self._get_applicable_rules("resolution_strategy", execution_phase)

        for rule in applicable_rules:
            try:
                violation = await self._check_rule_compliance(
                    rule, strategy_json, "resolution_strategy", context
                )

                if violation:
                    violations.append(violation)
                    failed_rules.append(rule.id)
                else:
                    passed_rules.append(rule.id)

            except Exception as e:
                logger.error("Rule validation failed", rule_id=rule.id, error=str(e))
                failed_rules.append(rule.id)

        # Validate strategy-specific requirements
        strategy_violations = await self._validate_strategy_requirements(
            strategy, conflict_data, context
        )
        violations.extend(strategy_violations)

        # Generate compliance score
        total_rules = len(applicable_rules) + 3  # +3 for strategy-specific checks
        overall_score = self._calculate_compliance_score(violations, total_rules)
        compliance_level = self._determine_compliance_level(violations)

        # Generate recommendations
        recommendations = self._generate_recommendations(violations, "resolution_strategy")

        result = ComplianceResult(
            overall_score=overall_score,
            compliance_level=compliance_level,
            violations=violations,
            recommendations=recommendations,
            passed_rules=passed_rules,
            failed_rules=failed_rules,
            analysis_timestamp=datetime.utcnow(),
            analysis_context={
                "strategy_id": strategy.id,
                "execution_phase": execution_phase,
                "conflict_type": type(conflict_data).__name__,
                "strategy_confidence": strategy.confidence,
            },
        )

        self.compliance_history.append(result)
        logger.info(
            "Resolution strategy validation completed",
            overall_score=overall_score,
            violation_count=len(violations),
        )

        return result

    async def validate_execution_phase(
        self, phase_name: str, phase_data: Dict[str, Any], context: Dict[str, Any]
    ) -> ComplianceResult:
        """
        Validate an execution phase against constitutional rules

        Args:
            phase_name: Name of the execution phase
            phase_data: Data for the execution phase
            context: Additional context for validation

        Returns:
            ComplianceResult with detailed analysis
        """
        logger.info("Validating execution phase", phase_name=phase_name)

        violations = []
        passed_rules = []
        failed_rules = []

        # Convert phase data to string for pattern matching
        phase_json = json.dumps(phase_data, indent=2)

        # Load applicable rules for execution phases
        applicable_rules = self._get_applicable_rules("execution_phase", phase_name)

        for rule in applicable_rules:
            try:
                violation = await self._check_rule_compliance(
                    rule, phase_json, "execution_phase", context
                )

                if violation:
                    violations.append(violation)
                    failed_rules.append(rule.id)
                else:
                    passed_rules.append(rule.id)

            except Exception as e:
                logger.error("Rule validation failed", rule_id=rule.id, error=str(e))
                failed_rules.append(rule.id)

        # Generate compliance score
        overall_score = self._calculate_compliance_score(violations, len(applicable_rules))
        compliance_level = self._determine_compliance_level(violations)

        # Generate recommendations
        recommendations = self._generate_recommendations(violations, "execution_phase")

        result = ComplianceResult(
            overall_score=overall_score,
            compliance_level=compliance_level,
            violations=violations,
            recommendations=recommendations,
            passed_rules=passed_rules,
            failed_rules=failed_rules,
            analysis_timestamp=datetime.utcnow(),
            analysis_context={
                "phase_name": phase_name,
                "phase_data_keys": list(phase_data.keys()),
            },
        )

        self.compliance_history.append(result)
        logger.info(
            "Execution phase validation completed",
            overall_score=overall_score,
            violation_count=len(violations),
        )

        return result

    async def get_constitutional_scoring(
        self, analysis_results: List[ComplianceResult], weights: Dict[str, float] = None
    ) -> Dict[str, Any]:
        """
        Generate constitutional scoring for spec-kit workflows

        Args:
            analysis_results: List of compliance analysis results
            weights: Optional weights for different analysis types

        Returns:
            Constitutional scoring analysis
        """
        if weights is None:
            weights = {
                "specification_template": 0.25,
                "resolution_strategy": 0.50,
                "execution_phase": 0.25,
            }

        # Group results by type
        template_scores = []
        strategy_scores = []
        phase_scores = []

        for result in analysis_results:
            context = result.analysis_context
            if "template_type" in context:
                template_scores.append(result.overall_score)
            elif "strategy_id" in context:
                strategy_scores.append(result.overall_score)
            elif "phase_name" in context:
                phase_scores.append(result.overall_score)

        # Calculate weighted averages
        avg_template_score = sum(template_scores) / len(template_scores) if template_scores else 1.0
        avg_strategy_score = sum(strategy_scores) / len(strategy_scores) if strategy_scores else 1.0
        avg_phase_score = sum(phase_scores) / len(phase_scores) if phase_scores else 1.0

        # Calculate overall constitutional score
        constitutional_score = (
            avg_template_score * weights["specification_template"]
            + avg_strategy_score * weights["resolution_strategy"]
            + avg_phase_score * weights["execution_phase"]
        )

        # Calculate improvement potential
        violations_by_type = self._analyze_violations_by_type(analysis_results)
        improvement_potential = self._calculate_improvement_potential(violations_by_type)

        scoring_result = {
            "constitutional_score": constitutional_score,
            "component_scores": {
                "specification_template": avg_template_score,
                "resolution_strategy": avg_strategy_score,
                "execution_phase": avg_phase_score,
            },
            "weights_used": weights,
            "violation_analysis": violations_by_type,
            "improvement_potential": improvement_potential,
            "compliance_level": self._score_to_compliance_level(constitutional_score),
            "recommendations": self._generate_scoring_recommendations(
                constitutional_score, violations_by_type
            ),
            "analysis_timestamp": datetime.utcnow().isoformat(),
        }

        logger.info(
            "Constitutional scoring completed",
            constitutional_score=constitutional_score,
            violation_count=sum(len(r.violations) for r in analysis_results),
        )

        return scoring_result

    async def _load_constitutional_rules(self) -> None:
        """Load constitutional rules from the constitutions directory"""
        rules_dir = os.path.join(self.constitutions_dir, "pr-resolution-templates")

        if not os.path.exists(rules_dir):
            logger.warning("Constitutional rules directory not found", rules_dir=rules_dir)
            return

        # Load default rule sets
        rule_files = [
            "specification-rules.json",
            "strategy-rules.json",
            "execution-rules.json",
            "general-rules.json",
        ]

        for rule_file in rule_files:
            rule_path = os.path.join(rules_dir, rule_file)
            if os.path.exists(rule_path):
                try:
                    with open(rule_path, "r") as f:
                        rules_data = json.load(f)

                    for rule_data in rules_data.get("rules", []):
                        rule = ConstitutionalRule(**rule_data)
                        self.rules[rule.id] = rule
                        self.rule_categories.add(rule.category)

                    logger.debug(
                        "Loaded constitutional rules",
                        file=rule_file,
                        rule_count=len(rules_data.get("rules", [])),
                    )

                except Exception as e:
                    logger.error(
                        "Failed to load constitutional rules",
                        file=rule_file,
                        error=str(e),
                    )

    async def _compile_rule_patterns(self) -> None:
        """Compile regex patterns for rule validation"""
        for rule_id, rule in self.rules.items():
            try:
                self.violation_patterns[rule_id] = re.compile(
                    rule.rule_pattern, re.MULTILINE | re.IGNORECASE
                )
            except re.error as e:
                logger.error("Failed to compile rule pattern", rule_id=rule_id, error=str(e))

    def _get_applicable_rules(self, validation_type: str, context: str) -> List[ConstitutionalRule]:
        """Get rules applicable to a specific validation type and context"""
        applicable = []

        for rule in self.rules.values():
            # Check if rule applies to this validation type
            if validation_type in rule.phase_applications or "all" in rule.phase_applications:
                applicable.append(rule)

        return applicable

    async def _check_rule_compliance(
        self,
        rule: ConstitutionalRule,
        content: str,
        validation_type: str,
        context: Dict[str, Any],
    ) -> Optional[ViolationResult]:
        """Check compliance against a specific rule"""

        pattern = self.violation_patterns.get(rule.id)
        if not pattern:
            return None

        matches = pattern.findall(content)

        if matches:
            # Calculate violation confidence based on pattern matching
            confidence = min(1.0, len(matches) / 5.0)  # More matches = higher confidence

            # Determine location of violation
            location = self._find_violation_location(content, pattern)

            return ViolationResult(
                rule_id=rule.id,
                rule_name=rule.name,
                violation_type=rule.violation_type,
                severity_score=rule.severity_score,
                description=f"Constitutional rule violation: {rule.description}",
                location=location,
                context=self._extract_violation_context(content, pattern, location),
                remediation=rule.remediation_guide,
                auto_fixable=rule.auto_fixable,
                confidence=confidence,
            )

        return None

    async def _validate_strategy_requirements(
        self,
        strategy: ResolutionStrategy,
        conflict_data: Union[MergeConflict, DependencyConflict, ArchitectureViolation],
        context: Dict[str, Any],
    ) -> List[ViolationResult]:
        """Validate strategy-specific constitutional requirements"""
        violations = []

        # Check for minimum confidence requirement
        if strategy.confidence < 0.6:
            violations.append(
                ViolationResult(
                    rule_id="strategy_confidence_minimum",
                    rule_name="Strategy Confidence Minimum",
                    violation_type=ViolationType.MAJOR,
                    severity_score=0.7,
                    description="Strategy confidence is below minimum threshold",
                    location="strategy.confidence",
                    context=f"Current confidence: {strategy.confidence}, required: >= 0.6",
                    remediation="Enhance strategy with more detailed analysis and validation steps",
                    auto_fixable=False,
                    confidence=1.0,
                )
            )

        # Check for rollback strategy requirement
        if not strategy.rollback_strategy:
            violations.append(
                ViolationResult(
                    rule_id="strategy_rollback_required",
                    rule_name="Strategy Rollback Required",
                    violation_type=ViolationType.CRITICAL,
                    severity_score=0.9,
                    description="Strategy lacks rollback strategy",
                    location="strategy.rollback_strategy",
                    context="No rollback strategy defined",
                    remediation="Add comprehensive rollback strategy to mitigate risks",
                    auto_fixable=True,
                    confidence=1.0,
                )
            )

        # Check for validation approach requirement
        if not strategy.validation_approach:
            violations.append(
                ViolationResult(
                    rule_id="strategy_validation_required",
                    rule_name="Strategy Validation Required",
                    violation_type=ViolationType.MAJOR,
                    severity_score=0.6,
                    description="Strategy lacks validation approach",
                    location="strategy.validation_approach",
                    context="No validation approach defined",
                    remediation=(
                        "Add comprehensive validation approach including testing and verification"
                    ),
                    auto_fixable=True,
                    confidence=1.0,
                )
            )

        return violations

    def _calculate_compliance_score(
        self, violations: List[ViolationResult], total_rules: int
    ) -> float:
        """Calculate overall compliance score"""
        if total_rules == 0:
            return 1.0

        # Start with full score and subtract violation penalties
        total_penalty = 0.0

        for violation in violations:
            penalty = violation.severity_score * violation.confidence
            total_penalty += penalty

        # Normalize penalty to prevent negative scores
        max_penalty = total_rules * 1.0
        normalized_penalty = min(total_penalty / max_penalty, 1.0)

        return max(0.0, 1.0 - normalized_penalty)

    def _determine_compliance_level(self, violations: List[ViolationResult]) -> ComplianceLevel:
        """Determine compliance level based on violations"""

        critical_violations = [v for v in violations if v.violation_type == ViolationType.CRITICAL]
        major_violations = [v for v in violations if v.violation_type == ViolationType.MAJOR]
        minor_violations = [v for v in violations if v.violation_type == ViolationType.MINOR]

        if critical_violations:
            return ComplianceLevel.CRITICAL_VIOLATIONS
        elif major_violations:
            return ComplianceLevel.MAJOR_VIOLATIONS
        elif minor_violations:
            return ComplianceLevel.MINOR_VIOLATIONS
        else:
            return ComplianceLevel.FULL_COMPLIANCE

    def _generate_recommendations(
        self, violations: List[ViolationResult], validation_type: str
    ) -> List[str]:
        """Generate recommendations based on violations"""
        recommendations = []

        # Group violations by type
        by_type = {}
        for violation in violations:
            if violation.violation_type not in by_type:
                by_type[violation.violation_type] = []
            by_type[violation.violation_type].append(violation)

        # Generate recommendations for each violation type
        if ViolationType.CRITICAL in by_type:
            recommendations.append(
                "🚨 CRITICAL: Address critical constitutional violations before proceeding"
            )

        if ViolationType.MAJOR in by_type:
            recommendations.append(
                "⚠️ MAJOR: Resolve major violations to ensure constitutional compliance"
            )

        if ViolationType.MINOR in by_type:
            recommendations.append(
                "ℹ️ MINOR: Consider addressing minor violations for improved compliance"
            )

        # Specific recommendations based on validation type
        if validation_type == "specification_template":
            recommendations.append("📋 Ensure specification templates follow Spec Kit methodology")
            recommendations.append("📋 Include all required sections and validation criteria")

        elif validation_type == "resolution_strategy":
            recommendations.append("🔧 Ensure resolution strategies include rollback procedures")
            recommendations.append("🔧 Validate strategy effectiveness against conflict complexity")

        elif validation_type == "execution_phase":
            recommendations.append(
                "⚡ Ensure execution phases include proper validation checkpoints"
            )
            recommendations.append("⚡ Include error handling and recovery mechanisms")

        return recommendations

    def _find_violation_location(self, content: str, pattern: re.Pattern) -> str:
        """Find the location of a violation in content"""
        match = pattern.search(content)
        if match:
            lines = content[: match.start()].count("\n") + 1
            return f"Line {lines}"
        return "Unknown location"

    def _extract_violation_context(self, content: str, pattern: re.Pattern, location: str) -> str:
        """Extract context around a violation"""
        match = pattern.search(content)
        if match:
            start = max(0, match.start() - 100)
            end = min(len(content), match.end() + 100)
            context = content[start:end].strip()
            return f"...{context}..."
        return "Context not available"

    def _analyze_violations_by_type(self, results: List[ComplianceResult]) -> Dict[str, int]:
        """Analyze violations by type across multiple results"""
        by_type = {
            ViolationType.CRITICAL.value: 0,
            ViolationType.MAJOR.value: 0,
            ViolationType.MINOR.value: 0,
            ViolationType.WARNING.value: 0,
            ViolationType.INFO.value: 0,
        }

        for result in results:
            for violation in result.violations:
                by_type[violation.violation_type.value] += 1

        return by_type

    def _calculate_improvement_potential(self, violations_by_type: Dict[str, int]) -> float:
        """Calculate potential for improvement based on violations"""
        total_violations = sum(violations_by_type.values())
        if total_violations == 0:
            return 0.0

        # Weight violations by severity
        weighted_violations = (
            violations_by_type[ViolationType.CRITICAL.value] * 1.0
            + violations_by_type[ViolationType.MAJOR.value] * 0.8
            + violations_by_type[ViolationType.MINOR.value] * 0.6
            + violations_by_type[ViolationType.WARNING.value] * 0.4
            + violations_by_type[ViolationType.INFO.value] * 0.2
        )

        # Normalize to 0-1 scale (assuming max 20 weighted violations)
        return min(1.0, weighted_violations / 20.0)

    def _score_to_compliance_level(self, score: float) -> str:
        """Convert score to compliance level string"""
        if score >= 0.9:
            return "EXCELLENT"
        elif score >= 0.8:
            return "GOOD"
        elif score >= 0.7:
            return "ACCEPTABLE"
        elif score >= 0.6:
            return "NEEDS_IMPROVEMENT"
        else:
            return "NON_COMPLIANT"

    def _generate_scoring_recommendations(
        self, constitutional_score: float, violations_by_type: Dict[str, int]
    ) -> List[str]:
        """Generate recommendations based on constitutional scoring"""
        recommendations = []

        if constitutional_score < 0.7:
            recommendations.append(
                "🎯 FOCUS: Constitutional compliance requires immediate attention"
            )
            recommendations.append("🔧 PRIORITIZE: Address critical and major violations first")

        if violations_by_type[ViolationType.CRITICAL.value] > 0:
            recommendations.append(
                "🚨 URGENT: Critical violations must be resolved before proceeding"
            )

        if constitutional_score >= 0.9:
            recommendations.append(
                "✅ EXCELLENT: Constitutional compliance is at an excellent level"
            )

        return recommendations

    def get_compliance_history(self, limit: int = 10) -> List[ComplianceResult]:
        """Get recent compliance history"""
        return self.compliance_history[-limit:]

    def get_violation_statistics(self) -> Dict[str, Any]:
        """Get violation statistics across all analyses"""
        total_analyses = len(self.compliance_history)
        if total_analyses == 0:
            return {"total_analyses": 0}

        total_violations = sum(len(result.violations) for result in self.compliance_history)
        avg_score = sum(result.overall_score for result in self.compliance_history) / total_analyses

        # Count violations by type
        violations_by_type = {vt.value: 0 for vt in ViolationType}
        for result in self.compliance_history:
            for violation in result.violations:
                violations_by_type[violation.violation_type.value] += 1

        return {
            "total_analyses": total_analyses,
            "total_violations": total_violations,
            "average_score": avg_score,
            "violations_by_type": violations_by_type,
            "most_common_violations": self._get_most_common_violations(),
        }

    def _get_most_common_violations(self) -> List[Tuple[str, int]]:
        """Get most common violations across all analyses"""
        violation_counts = {}

        for result in self.compliance_history:
            for violation in result.violations:
                rule_id = violation.rule_id
                if rule_id not in violation_counts:
                    violation_counts[rule_id] = 0
                violation_counts[rule_id] += 1

        # Sort by count and return top 10
        sorted_violations = sorted(violation_counts.items(), key=lambda x: x[1], reverse=True)
        return sorted_violations[:10]
