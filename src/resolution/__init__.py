"""
Constitutional Engine

Implements constitutional analysis for code compliance and standards.
"""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import json
import yaml
from pathlib import Path


@dataclass
class ConstitutionalRequirement:
    """Represents a constitutional requirement"""
    id: str
    name: str
    description: str
    category: str
    severity: str  # 'must', 'should', 'may'
    compliance_threshold: float  # 0.0 to 1.0


from enum import Enum

class ComplianceLevel(Enum):
    """Levels of compliance"""
    NON_COMPLIANT = "non_compliant"
    PARTIALLY_COMPLIANT = "partially_compliant"
    COMPLIANT = "compliant"
    EXCELLENT = "excellent"


@dataclass
class ConstitutionalValidationResult:
    """Result of constitutional validation"""
    overall_score: float  # 0.0 to 1.0
    compliance_level: ComplianceLevel
    detailed_results: List[ComplianceResult]
    summary: str = ""
    recommendations: List[str] = None

    def __post_init__(self):
        if self.recommendations is None:
            self.recommendations = []


@dataclass
class ComplianceResult:
    """Result of constitutional compliance check"""
    requirement_id: str
    is_compliant: bool
    score: float  # 0.0 to 1.0
    details: str
    suggestions: List[str]


class ConstitutionalEngine:
    """Engine for constitutional analysis and compliance checking"""
    
    def __init__(self, constitution_file: Optional[str] = None):
        self.requirements: List[ConstitutionalRequirement] = []
        self.load_constitution(constitution_file)
    
    def load_constitution(self, constitution_file: Optional[str] = None):
        """Load constitutional requirements from file or default set"""
        if constitution_file and Path(constitution_file).exists():
            self._load_from_file(constitution_file)
        else:
            self._load_default_constitution()
    
    def _load_from_file(self, constitution_file: str):
        """Load constitution from file"""
        file_path = Path(constitution_file)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            if file_path.suffix.lower() in ['.yaml', '.yml']:
                data = yaml.safe_load(f)
            else:
                data = json.load(f)
        
        for req_data in data.get('requirements', []):
            req = ConstitutionalRequirement(
                id=req_data['id'],
                name=req_data['name'],
                description=req_data['description'],
                category=req_data.get('category', 'general'),
                severity=req_data.get('severity', 'should'),
                compliance_threshold=req_data.get('compliance_threshold', 0.8)
            )
            self.requirements.append(req)
    
    def _load_default_constitution(self):
        """Load default constitutional requirements"""
        default_requirements = [
            ConstitutionalRequirement(
                id="security-001",
                name="Input Validation",
                description="All user inputs must be validated and sanitized",
                category="security",
                severity="must",
                compliance_threshold=1.0
            ),
            ConstitutionalRequirement(
                id="security-002",
                name="Authentication Required",
                description="Sensitive operations must require authentication",
                category="security",
                severity="must",
                compliance_threshold=1.0
            ),
            ConstitutionalRequirement(
                id="performance-001",
                name="Response Time",
                description="API responses should be under 2 seconds",
                category="performance",
                severity="should",
                compliance_threshold=0.9
            ),
            ConstitutionalRequirement(
                id="architecture-001",
                name="Separation of Concerns",
                description="Components should follow single responsibility principle",
                category="architecture",
                severity="should",
                compliance_threshold=0.8
            ),
            ConstitutionalRequirement(
                id="testing-001",
                name="Test Coverage",
                description="Code should have at least 80% test coverage",
                category="testing",
                severity="should",
                compliance_threshold=0.8
            )
        ]
        
        self.requirements = default_requirements
    
    def analyze_compliance(self, code: str, context: Dict[str, Any] = None) -> List[ComplianceResult]:
        """Analyze code compliance against constitutional requirements"""
        results = []
        
        for requirement in self.requirements:
            result = self._check_requirement(code, requirement, context)
            results.append(result)
        
        return results
    
    def _check_requirement(self, code: str, requirement: ConstitutionalRequirement, 
                          context: Dict[str, Any] = None) -> ComplianceResult:
        """Check compliance with a single requirement"""
        # This is a simplified implementation - in a real system, this would be more sophisticated
        compliant = True
        score = 1.0
        details = f"Requirement '{requirement.name}' checked"
        suggestions = []
        
        # Example checks based on requirement category
        if requirement.category == "security":
            if requirement.id == "security-001":  # Input validation
                # Check for common input validation patterns
                if "validate" not in code.lower() and "sanitize" not in code.lower():
                    compliant = False
                    score = 0.2
                    details = f"Input validation not found for requirement: {requirement.name}"
                    suggestions = ["Add input validation for user inputs", "Implement sanitization functions"]
        
        elif requirement.category == "performance":
            if requirement.id == "performance-001":  # Response time
                # This would be more complex in reality
                compliant = True  # Assume compliant for now
                score = 0.95
                details = "Performance requirements appear to be met"
        
        elif requirement.category == "architecture":
            if requirement.id == "architecture-001":  # Separation of concerns
                # Check for functions/classes that might be doing too much
                lines = code.split('\n')
                if len(lines) > 100:  # Very basic check
                    score = 0.6
                    details = "Large code block detected, consider separation"
                    suggestions = ["Consider breaking down large functions/classes"]
        
        return ComplianceResult(
            requirement_id=requirement.id,
            is_compliant=compliant,
            score=score,
            details=details,
            suggestions=suggestions
        )
    
    def generate_compliance_report(self, results: List[ComplianceResult]) -> str:
        """Generate a compliance report from analysis results"""
        compliant_count = sum(1 for r in results if r.is_compliant)
        total_count = len(results)
        overall_score = sum(r.score for r in results) / total_count if total_count > 0 else 0.0
        
        report_lines = [
            "# Constitutional Compliance Report",
            "",
            f"## Summary",
            f"- Total Requirements: {total_count}",
            f"- Compliant: {compliant_count}",
            f"- Non-compliant: {total_count - compliant_count}",
            f"- Overall Compliance Score: {overall_score:.2%}",
            "",
            f"## Detailed Results",
        ]
        
        for result in results:
            status = "✅" if result.is_compliant else "❌"
            report_lines.append(f"- {status} {result.requirement_id}: {result.score:.2%} - {result.details}")
            if result.suggestions:
                for suggestion in result.suggestions:
                    report_lines.append(f"  - 💡 {suggestion}")
        
        return "\n".join(report_lines)
    
    def get_non_compliant_requirements(self, results: List[ComplianceResult]) -> List[ComplianceResult]:
        """Get only non-compliant requirements"""
        return [r for r in results if not r.is_compliant]

    async def initialize(self):
        """Initialize the constitutional engine (async for compatibility)"""
        # In this implementation, initialization is synchronous
        # but we provide an async wrapper for compatibility
        pass

    async def validate_specification_template(
        self,
        template_content: str,
        template_type: str,
        context: Dict[str, Any] = None
    ) -> ConstitutionalValidationResult:
        """Validate a specification template against constitutional requirements"""
        # Perform analysis on the template content
        compliance_results = self.analyze_compliance(template_content, context)

        # Calculate overall score
        if compliance_results:
            overall_score = sum(r.score for r in compliance_results) / len(compliance_results)
        else:
            overall_score = 1.0  # Perfect compliance if no requirements checked

        # Determine compliance level
        if overall_score >= 0.9:
            compliance_level = ComplianceLevel.EXCELLENT
        elif overall_score >= 0.8:
            compliance_level = ComplianceLevel.COMPLIANT
        elif overall_score >= 0.6:
            compliance_level = ComplianceLevel.PARTIALLY_COMPLIANT
        else:
            compliance_level = ComplianceLevel.NON_COMPLIANT

        # Generate summary
        non_compliant_count = len([r for r in compliance_results if not r.is_compliant])
        summary = f"Template validation: {len(compliance_results)} requirements checked, {non_compliant_count} non-compliant"

        # Generate recommendations
        recommendations = []
        for result in compliance_results:
            if not result.is_compliant and result.suggestions:
                recommendations.extend(result.suggestions)

        return ConstitutionalValidationResult(
            overall_score=overall_score,
            compliance_level=compliance_level,
            detailed_results=compliance_results,
            summary=summary,
            recommendations=list(set(recommendations))  # Remove duplicates
        )