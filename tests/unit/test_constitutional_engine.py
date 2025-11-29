"""
Unit tests for Constitutional Engine

Tests constitutional compliance validation, rule scoring, and violation handling.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch
from datetime import datetime

# Import the modules to test
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from resolution.constitutional_engine import ConstitutionalEngine, ConstitutionalRule, ViolationType


class TestConstitutionalEngine:
    """Test suite for ConstitutionalEngine"""
    
    @pytest.fixture
    def engine(self):
        """Create a ConstitutionalEngine instance for testing"""
        return ConstitutionalEngine()
    
    @pytest.fixture
    def sample_rules(self):
        """Create sample constitutional rules for testing"""
        return [
            ConstitutionalRule(
                id="test_rule_1",
                name="Test Rule 1",
                description="A test rule for validation",
                category="quality",
                violation_type=ViolationType.MAJOR,
                rule_pattern=r"quality_score\":\s*0\.[0-6]",  # Matches low scores
                severity_score=0.7,
                auto_fixable=False,
                remediation_guide="Improve quality score",
                examples=[],
                dependencies=[],
                phase_applications=["all"]
            ),
            ConstitutionalRule(
                id="test_rule_2", 
                name="Test Rule 2",
                description="Another test rule",
                category="security",
                violation_type=ViolationType.CRITICAL,
                rule_pattern=r"security_compliant\":\s*false",
                severity_score=0.9,
                auto_fixable=True,
                remediation_guide="Address security issues",
                examples=[],
                dependencies=[],
                phase_applications=["all"]
            )
        ]
    
    @pytest.fixture
    def sample_template_data(self):
        """Create sample template data for validation"""
        return {
            "template_content": {
                "overview": {
                    "description": "Test specification template",
                    "quality_score": 0.8
                },
                "constitutional_compliance": {
                    "compliance_score": 0.9,
                    "security_compliant": True
                },
                "implementation_strategy": {
                    "approach": "multi_phase",
                    "risk_assessment": "comprehensive"
                }
            },
            "template_metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "template_type": "enhanced"
            }
        }

    async def test_engine_initialization(self, engine):
        """Test constitutional engine initialization"""
        assert engine is not None
        assert engine.rule_cache == {}
        assert engine.validation_stats == {
            "total_validations": 0,
            "successful_validations": 0,
            "violation_count": 0,
            "average_processing_time": 0.0
        }

    async def test_rule_registration(self, engine, sample_rules):
        """Test constitutional rule registration"""
        result = await engine.register_constitutional_rules(sample_rules)
        
        assert result.success
        assert len(result.registered_rules) == 2
        assert "test_rule_1" in engine.rule_cache
        assert "test_rule_2" in engine.rule_cache

    async def test_template_validation_basic(self, engine, sample_rules, sample_template_data):
        """Test basic template validation"""
        # Register sample rules
        await engine.register_constitutional_rules(sample_rules)
        
        # Validate template
        result = await engine.validate_template(sample_template_data)
        
        assert isinstance(result, ValidationResult)
        assert result.overall_score >= 0.0
        assert isinstance(result.violations, list)
        assert isinstance(result.compliance_score, float)

    async def test_violation_detection(self, engine, sample_rules):
        """Test violation detection and classification"""
        # Create template with intentional violations
        violation_template = {
            "template_content": {
                "overview": {
                    "description": "Poor quality template",
                    "quality_score": 0.3  # Below threshold
                },
                "constitutional_compliance": {
                    "compliance_score": 0.9,
                    "security_compliant": False  # Security violation
                }
            }
        }
        
        await engine.register_constitutional_rules(sample_rules)
        result = await engine.validate_template(violation_template)
        
        # Should detect violations
        assert len(result.violations) > 0
        
        # Check violation types
        violation_types = [v.violation_type for v in result.violations]
        assert ViolationType.MAJOR in violation_types or ViolationType.CRITICAL in violation_types

    async def test_real_time_validation(self, engine, sample_rules):
        """Test real-time validation functionality"""
        await engine.register_constitutional_rules(sample_rules)
        
        # Test real-time validation with continuous updates
        initial_template = {
            "template_content": {
                "overview": {"description": "Initial template", "quality_score": 0.5},
                "constitutional_compliance": {"security_compliant": False}
            }
        }
        
        # Validate initial state
        result = await engine.validate_template(initial_template)
        initial_violations = len(result.violations)
        
        # Update template with improvements
        improved_template = {
            "template_content": {
                "overview": {"description": "Improved template", "quality_score": 0.8},
                "constitutional_compliance": {"security_compliant": True}
            }
        }
        
        # Validate improved state
        result = await engine.validate_template(improved_template)
        improved_violations = len(result.violations)
        
        # Should have fewer violations after improvement
        assert improved_violations <= initial_violations

    async def test_constitutional_scoring(self, engine, sample_rules):
        """Test constitutional compliance scoring"""
        await engine.register_constitutional_rules(sample_rules)
        
        # Test high-scoring template
        high_score_template = {
            "template_content": {
                "overview": {"description": "High quality", "quality_score": 0.95},
                "constitutional_compliance": {"security_compliant": True}
            }
        }
        
        result = await engine.validate_template(high_score_template)
        assert result.overall_score >= 0.8
        assert result.compliance_score >= 0.8
        
        # Test low-scoring template
        low_score_template = {
            "template_content": {
                "overview": {"description": "Low quality", "quality_score": 0.2},
                "constitutional_compliance": {"security_compliant": False}
            }
        }
        
        result = await engine.validate_template(low_score_template)
        assert result.overall_score <= 0.5

    async def test_performance_benchmarks(self, engine, sample_rules):
        """Test constitutional validation performance"""
        await engine.register_constitutional_rules(sample_rules)
        
        # Create larger template for performance testing
        large_template = {
            "template_content": {
                f"section_{i}": {
                    f"content_{j}": f"Test content {i}-{j}" 
                    for j in range(10)
                }
                for i in range(50)
            }
        }
        
        # Measure validation time
        import time
        start_time = time.time()
        
        result = await engine.validate_template(large_template)
        
        end_time = time.time()
        validation_time = end_time - start_time
        
        # Should complete within reasonable time (adjust threshold as needed)
        assert validation_time < 5.0  # 5 seconds maximum
        assert result.validation_time >= 0.0

    async def test_rule_caching(self, engine, sample_rules):
        """Test rule caching functionality"""
        await engine.register_constitutional_rules(sample_rules)
        
        template_data = {
            "template_content": {"overview": {"quality_score": 0.8}}
        }
        
        # First validation (cache miss)
        start_time = time.time()
        result1 = await engine.validate_template(template_data)
        first_validation_time = time.time() - start_time
        
        # Second validation (should use cache)
        start_time = time.time()
        result2 = await engine.validate_template(template_data)
        second_validation_time = time.time() - start_time
        
        # Second validation should be faster due to caching
        assert second_validation_time <= first_validation_time
        assert result1.overall_score == result2.overall_score

    async def test_error_handling(self, engine):
        """Test error handling for invalid inputs"""
        # Test invalid template data
        with pytest.raises((ValueError, TypeError)):
            await engine.validate_template(None)
        
        # Test missing required fields
        invalid_template = {
            "invalid_field": "This doesn't match expected structure"
        }
        
        result = await engine.validate_template(invalid_template)
        # Should handle gracefully, possibly with warnings or default values
        assert isinstance(result, ValidationResult)

    async def test_validation_statistics(self, engine, sample_rules):
        """Test validation statistics tracking"""
        await engine.register_constitutional_rules(sample_rules)
        
        # Perform multiple validations
        templates = [
            {"template_content": {"overview": {"quality_score": 0.9}}},
            {"template_content": {"overview": {"quality_score": 0.3}}},
            {"template_content": {"overview": {"quality_score": 0.7}}}
        ]
        
        for template in templates:
            await engine.validate_template(template)
        
        # Check statistics
        stats = engine.get_validation_statistics()
        assert stats["total_validations"] == 3
        assert stats["successful_validations"] == 3
        assert stats["average_processing_time"] > 0

    async def test_batch_validation(self, engine, sample_rules):
        """Test batch template validation"""
        await engine.register_constitutional_rules(sample_rules)
        
        templates = [
            {"template_content": {"overview": {"quality_score": 0.9}}},
            {"template_content": {"overview": {"quality_score": 0.5}}},
            {"template_content": {"overview": {"quality_score": 0.3}}}
        ]
        
        # Batch validation should process all templates
        results = await engine.batch_validate_templates(templates)
        
        assert len(results) == 3
        for result in results:
            assert isinstance(result, ValidationResult)
            assert result.overall_score >= 0.0

    async def test_constitutional_framework_integration(self, engine, sample_rules):
        """Test integration with constitutional framework rules"""
        # Test with actual constitutional rules from templates
        await engine.load_constitutional_rules_from_directory("constitutions/pr-resolution-templates")
        
        template = {
            "template_content": {
                "overview": {"description": "Test template"},
                "constitutional_compliance": {"compliance_score": 0.8}
            }
        }
        
        result = await engine.validate_template(template)
        
        # Should have loaded rules and performed validation
        assert len(engine.rule_cache) > 0
        assert isinstance(result, ValidationResult)

    async def test_custom_rule_function(self, engine):
        """Test custom rule function validation"""
        # Create custom rule with specific validation logic
        custom_rule = ConstitutionalRule(
            id="custom_rule",
            name="Custom Validation Rule",
            description="Custom rule for testing",
            category="custom",
            violation_type=ViolationType.MAJOR,
            rule_pattern=r"section[0-9]+",  # Dummy pattern for testing
            severity_score=0.7,
            auto_fixable=False,
            remediation_guide="Add more template sections",
            examples=[],
            dependencies=[],
            phase_applications=["all"]
        )
        
        await engine.register_constitutional_rules([custom_rule])
        
        # Test with valid template
        valid_template = {
            "template_content": {
                "section1": {"content": "data"},
                "section2": {"content": "data"},
                "section3": {"content": "data"}
            }
        }
        
        result = await engine.validate_template(valid_template)
        # Should pass custom rule
        custom_violations = [v for v in result.violations if "custom_rule" in v.rule_id]
        assert len(custom_violations) == 0
        
        # Test with invalid template
        invalid_template = {
            "template_content": {
                "section1": {"content": "data"}
            }
        }
        
        result = await engine.validate_template(invalid_template)
        # Should fail custom rule
        custom_violations = [v for v in result.violations if "custom_rule" in v.rule_id]
        assert len(custom_violations) > 0


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])