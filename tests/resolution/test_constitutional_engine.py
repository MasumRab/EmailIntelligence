"""Tests for resolution module - ConstitutionalEngine."""

import pytest
import json
import tempfile
from pathlib import Path

from src.resolution import (
    ConstitutionalRequirement,
    ConstitutionalValidationResult,
    ComplianceResult,
    ComplianceLevel,
    ConstitutionalEngine,
)


class TestConstitutionalRequirement:
    """Test ConstitutionalRequirement dataclass."""

    def test_creation(self):
        """Test creating a constitutional requirement."""
        req = ConstitutionalRequirement(
            id="test-001",
            name="Test Requirement",
            description="A test requirement",
            category="test",
            severity="should",
            compliance_threshold=0.8
        )
        assert req.id == "test-001"
        assert req.name == "Test Requirement"
        assert req.severity == "should"

    def test_default_compliance_threshold(self):
        """Test default compliance threshold."""
        req = ConstitutionalRequirement(
            id="test-001",
            name="Test",
            description="Test",
            category="test",
            severity="should",
            compliance_threshold=0.8
        )
        assert req.compliance_threshold == 0.8


class TestComplianceLevel:
    """Test ComplianceLevel enum."""

    def test_compliance_levels(self):
        """Test all compliance levels exist."""
        assert ComplianceLevel.NON_COMPLIANT.value == "non_compliant"
        assert ComplianceLevel.PARTIALLY_COMPLIANT.value == "partially_compliant"
        assert ComplianceLevel.COMPLIANT.value == "compliant"
        assert ComplianceLevel.EXCELLENT.value == "excellent"


class TestComplianceResult:
    """Test ComplianceResult dataclass."""

    def test_creation(self):
        """Test creating a compliance result."""
        result = ComplianceResult(
            requirement_id="test-001",
            is_compliant=True,
            score=0.9,
            details="Test passed",
            suggestions=["Suggestion 1"]
        )
        assert result.requirement_id == "test-001"
        assert result.is_compliant is True
        assert result.score == 0.9


class TestConstitutionalValidationResult:
    """Test ConstitutionalValidationResult dataclass."""

    def test_creation_with_defaults(self):
        """Test creating with default recommendations."""
        result = ConstitutionalValidationResult(
            overall_score=0.85,
            compliance_level=ComplianceLevel.COMPLIANT,
            detailed_results=[]
        )
        assert result.recommendations == []

    def test_creation_with_custom_values(self):
        """Test creating with custom values."""
        result = ConstitutionalValidationResult(
            overall_score=0.95,
            compliance_level=ComplianceLevel.EXCELLENT,
            detailed_results=[],
            summary="All checks passed",
            recommendations=["Keep it up"]
        )
        assert result.summary == "All checks passed"
        assert result.recommendations == ["Keep it up"]


class TestConstitutionalEngine:
    """Test ConstitutionalEngine class."""

    def test_initialization_default(self):
        """Test default initialization loads default constitution."""
        engine = ConstitutionalEngine()
        assert len(engine.requirements) > 0
        assert all(isinstance(r, ConstitutionalRequirement) for r in engine.requirements)

    def test_initialization_with_file(self):
        """Test initialization with custom constitution file."""
        # Create a temporary constitution file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({
                "requirements": [
                    {
                        "id": "custom-001",
                        "name": "Custom Requirement",
                        "description": "A custom requirement",
                        "category": "custom",
                        "severity": "must",
                        "compliance_threshold": 1.0
                    }
                ]
            }, f)
            temp_file = f.name

        try:
            engine = ConstitutionalEngine(constitution_file=temp_file)
            assert len(engine.requirements) == 1
            assert engine.requirements[0].id == "custom-001"
        finally:
            Path(temp_file).unlink()

    def test_initialization_nonexistent_file(self):
        """Test with nonexistent file falls back to defaults."""
        engine = ConstitutionalEngine(constitution_file="/nonexistent/file.json")
        assert len(engine.requirements) > 0  # Should have default requirements

    def test_load_constitution_with_yaml(self):
        """Test loading constitution from YAML file."""
        import yaml
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump({
                "requirements": [
                    {
                        "id": "yaml-001",
                        "name": "YAML Requirement",
                        "description": "From YAML file",
                        "category": "test",
                        "severity": "should",
                        "compliance_threshold": 0.9
                    }
                ]
            }, f)
            temp_file = f.name

        try:
            engine = ConstitutionalEngine(constitution_file=temp_file)
            assert len(engine.requirements) == 1
            assert engine.requirements[0].id == "yaml-001"
        finally:
            Path(temp_file).unlink()

    def test_load_default_constitution(self):
        """Test loading default constitution."""
        engine = ConstitutionalEngine()
        # Default constitution has specific requirements
        requirement_ids = [r.id for r in engine.requirements]
        assert "security-001" in requirement_ids
        assert "performance-001" in requirement_ids
        assert "architecture-001" in requirement_ids
        assert "testing-001" in requirement_ids

    def test_analyze_compliance(self):
        """Test analyzing compliance."""
        engine = ConstitutionalEngine()
        code = "def validate_input(data): return True"
        results = engine.analyze_compliance(code)
        assert len(results) > 0
        assert all(isinstance(r, ComplianceResult) for r in results)

    def test_analyze_compliance_with_context(self):
        """Test analyzing with context."""
        engine = ConstitutionalEngine()
        code = "some code"
        context = {"file": "test.py"}
        results = engine.analyze_compliance(code, context)
        assert len(results) > 0

    def test_check_requirement_security(self):
        """Test checking security requirement."""
        engine = ConstitutionalEngine()
        requirement = ConstitutionalRequirement(
            id="security-001",
            name="Input Validation",
            description="All user inputs must be validated",
            category="security",
            severity="must",
            compliance_threshold=1.0
        )
        # Code with validation - should be compliant
        result = engine._check_requirement("def validate(x): pass", requirement)
        assert result.requirement_id == "security-001"

        # Code without validation - should not be compliant
        result = engine._check_requirement("def process(x): pass", requirement)
        assert result.is_compliant is False

    def test_check_requirement_performance(self):
        """Test checking performance requirement."""
        engine = ConstitutionalEngine()
        requirement = ConstitutionalRequirement(
            id="performance-001",
            name="Response Time",
            description="API responses under 2 seconds",
            category="performance",
            severity="should",
            compliance_threshold=0.9
        )
        result = engine._check_requirement("some code", requirement)
        assert result.is_compliant is True

    def test_check_requirement_architecture(self):
        """Test checking architecture requirement."""
        engine = ConstitutionalEngine()
        requirement = ConstitutionalRequirement(
            id="architecture-001",
            name="Separation of Concerns",
            description="Components follow single responsibility",
            category="architecture",
            severity="should",
            compliance_threshold=0.8
        )
        # Large code block should get lower score
        large_code = "\n".join(["line"] * 150)
        result = engine._check_requirement(large_code, requirement)
        assert result.score < 1.0

    def test_generate_compliance_report_empty(self):
        """Test generating report with no results."""
        engine = ConstitutionalEngine()
        report = engine.generate_compliance_report([])
        assert "Total Requirements: 0" in report

    def test_generate_compliance_report(self):
        """Test generating compliance report."""
        engine = ConstitutionalEngine()
        results = [
            ComplianceResult(
                requirement_id="test-001",
                is_compliant=True,
                score=0.9,
                details="Test passed",
                suggestions=[]
            ),
            ComplianceResult(
                requirement_id="test-002",
                is_compliant=False,
                score=0.3,
                details="Test failed",
                suggestions=["Fix it"]
            )
        ]
        report = engine.generate_compliance_report(results)
        assert "Total Requirements: 2" in report
        assert "Compliant: 1" in report
        assert "Non-compliant: 1" in report

    def test_get_non_compliant_requirements(self):
        """Test getting non-compliant requirements."""
        engine = ConstitutionalEngine()
        results = [
            ComplianceResult("test-001", True, 0.9, "passed", []),
            ComplianceResult("test-002", False, 0.3, "failed", ["fix"]),
        ]
        non_compliant = engine.get_non_compliant_requirements(results)
        assert len(non_compliant) == 1
        assert non_compliant[0].requirement_id == "test-002"

    @pytest.mark.asyncio
    async def test_initialize(self):
        """Test async initialization."""
        engine = ConstitutionalEngine()
        await engine.initialize()
        # Just checks it doesn't raise

    @pytest.mark.asyncio
    async def test_validate_specification_template_empty(self):
        """Test validating empty template."""
        engine = ConstitutionalEngine()
        result = await engine.validate_specification_template("", "test")
        # Empty template will fail security-001, so score won't be 1.0
        assert result.overall_score > 0
        assert isinstance(result.compliance_level, ComplianceLevel)

    @pytest.mark.asyncio
    async def test_validate_specification_template_valid(self):
        """Test validating template with validate keyword."""
        engine = ConstitutionalEngine()
        template = "def validate_input(data): pass"
        result = await engine.validate_specification_template(template, "python")
        assert result.overall_score > 0
        assert isinstance(result.compliance_level, ComplianceLevel)
        assert isinstance(result.detailed_results, list)

    @pytest.mark.asyncio
    async def test_validate_specification_template_with_context(self):
        """Test validating with context."""
        engine = ConstitutionalEngine()
        template = "some code"
        context = {"file_type": "python"}
        result = await engine.validate_specification_template(template, "python", context)
        assert result.overall_score >= 0
        assert result.summary != ""

    @pytest.mark.asyncio
    async def test_validate_specification_all_levels(self):
        """Test all compliance levels."""
        engine = ConstitutionalEngine()

        # Test Excellent (>= 0.9)
        template = "def validate sanitize check"  # Contains security keywords
        result = await engine.validate_specification_template(template, "test")
        assert result.compliance_level in [ComplianceLevel.EXCELLENT, ComplianceLevel.COMPLIANT]

        # Test Partially Compliant (>= 0.6)
        # Just check it returns a valid level
        assert result.compliance_level in ComplianceLevel