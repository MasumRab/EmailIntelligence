"""
Tests for resolution module - Constitutional Engine

Note: Using local imports to work around forward reference issue in source code.
"""

import pytest


# Import individual classes that don't have forward reference issues
class TestComplianceLevel:
    """Tests for ComplianceLevel enum"""

    def test_compliance_levels(self):
        """Test all compliance levels exist"""
        from src.resolution import ComplianceLevel
        
        assert ComplianceLevel.NON_COMPLIANT.value == "non_compliant"
        assert ComplianceLevel.PARTIALLY_COMPLIANT.value == "partially_compliant"
        assert ComplianceLevel.COMPLIANT.value == "compliant"
        assert ComplianceLevel.EXCELLENT.value == "excellent"


class TestConstitutionalRequirement:
    """Tests for ConstitutionalRequirement dataclass"""

    def test_create_requirement(self):
        """Test creating a constitutional requirement"""
        from src.resolution import ConstitutionalRequirement
        
        req = ConstitutionalRequirement(
            id="test-001",
            name="Test Requirement",
            description="A test requirement",
            category="testing",
            severity="should",
            compliance_threshold=0.8,
        )
        assert req.id == "test-001"
        assert req.name == "Test Requirement"
        assert req.category == "testing"
        assert req.severity == "should"
        assert req.compliance_threshold == 0.8


class TestComplianceResult:
    """Tests for ComplianceResult dataclass"""

    def test_create_compliance_result(self):
        """Test creating a compliance result"""
        from src.resolution import ComplianceResult
        
        result = ComplianceResult(
            requirement_id="test-001",
            is_compliant=True,
            score=0.95,
            details="Test passed",
            suggestions=["Keep up the good work"],
        )
        assert result.requirement_id == "test-001"
        assert result.is_compliant is True
        assert result.score == 0.95


class TestConstitutionalEngine:
    """Tests for ConstitutionalEngine"""

    def test_engine_initialization_default(self):
        """Test engine initializes with default constitution"""
        from src.resolution import ConstitutionalEngine
        
        engine = ConstitutionalEngine()
        assert len(engine.requirements) > 0
        # Should have loaded default requirements
        assert any(req.id == "security-001" for req in engine.requirements)

    def test_engine_initialization_with_file(self, tmp_path):
        """Test engine loads constitution from file"""
        from src.resolution import ConstitutionalEngine
        
        # Create a temporary constitution file
        constitution_file = tmp_path / "constitution.yaml"
        constitution_file.write_text("""
requirements:
  - id: custom-001
    name: Custom Requirement
    description: A custom requirement
    category: testing
    severity: may
    compliance_threshold: 0.5
""")
        engine = ConstitutionalEngine(str(constitution_file))
        assert len(engine.requirements) == 1
        assert engine.requirements[0].id == "custom-001"

    def test_engine_initialization_nonexistent_file(self):
        """Test engine falls back to default when file doesn't exist"""
        from src.resolution import ConstitutionalEngine
        
        engine = ConstitutionalEngine("/nonexistent/path.yaml")
        assert len(engine.requirements) > 0

    def test_analyze_compliance_returns_results(self):
        from src.resolution import ConstitutionalEngine, ComplianceResult
        
        engine = ConstitutionalEngine()
        code = "def validate_input(data): pass"
        results = engine.analyze_compliance(code)
        assert len(results) == len(engine.requirements)
        assert all(isinstance(r, ComplianceResult) for r in results)

    def test_analyze_compliance_with_validation(self):
        from src.resolution import ConstitutionalEngine
        
        engine = ConstitutionalEngine()
        # Code with 'validate' should pass security-001
        code = "def validate_input(data): pass"
        results = engine.analyze_compliance(code)
        security_result = next(r for r in results if r.requirement_id == "security-001")
        assert security_result.is_compliant is True
        assert security_result.score > 0.5

    def test_analyze_compliance_without_validation(self):
        from src.resolution import ConstitutionalEngine
        
        engine = ConstitutionalEngine()
        # Code without 'validate' should fail security-001
        code = "def process(data): return data"
        results = engine.analyze_compliance(code)
        security_result = next(r for r in results if r.requirement_id == "security-001")
        assert security_result.is_compliant is False

    def test_generate_compliance_report(self):
        from src.resolution import ConstitutionalEngine
        
        engine = ConstitutionalEngine()
        results = engine.analyze_compliance("def validate(x): pass")
        report = engine.generate_compliance_report(results)
        assert "Constitutional Compliance Report" in report
        assert "Total Requirements:" in report
        assert "Compliant:" in report

    def test_get_non_compliant_requirements(self):
        from src.resolution import ConstitutionalEngine
        
        engine = ConstitutionalEngine()
        # Code without validation should have non-compliant results
        results = engine.analyze_compliance("def process(x): return x")
        non_compliant = engine.get_non_compliant_requirements(results)
        assert len(non_compliant) > 0
        assert all(not r.is_compliant for r in non_compliant)

    @pytest.mark.asyncio
    async def test_initialize_async(self):
        from src.resolution import ConstitutionalEngine
        
        engine = ConstitutionalEngine()
        await engine.initialize()
        # Just verify it completes without error