"""
Integration tests for complete resolution workflows

Tests end-to-end resolution processes including specification creation,
strategy generation, and validation.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch

# Import the modules to test
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from specification.template_generator import SpecificationTemplateGenerator, SpecificationPhase
from specification.interactive_creator import GuidedPromptSystem
from strategy.multi_phase_generator import MultiPhaseStrategyGenerator
from resolution.constitutional_engine import ConstitutionalEngine


class TestResolutionWorkflow:
    """Integration test suite for resolution workflows"""
    
    @pytest.fixture
    async def workflow_components(self):
        """Create all workflow components for testing"""
        template_generator = SpecificationTemplateGenerator()
        prompt_system = GuidedPromptSystem(template_generator)
        strategy_generator = MultiPhaseStrategyGenerator()
        constitutional_engine = ConstitutionalEngine()
        
        # Initialize components
        await template_generator.initialize()
        await prompt_system.initialize()
        await constitutional_engine.initialize()
        
        return {
            "template_generator": template_generator,
            "prompt_system": prompt_system,
            "strategy_generator": strategy_generator,
            "constitutional_engine": constitutional_engine
        }
    
    @pytest.fixture
    def sample_conflict_data(self):
        """Create sample conflict data for integration testing"""
        return type('MockConflict', (), {
            'conflict_type': 'content',
            'file_paths': ['src/user_service.py', 'src/auth_service.py'],
            'pr_numbers': [123],
            'branches': ['feature/user-auth', 'main'],
            'complexity_score': 7,
            'affected_components': ['authentication', 'user_management'],
            'estimated_resolution_time': 45,
            'risk_level': 'MEDIUM',
            'stakeholder_impact': 'high'
        })()
    
    @pytest.fixture
    def sample_project_context(self):
        """Create sample project context"""
        return {
            "organization": {"name": "EmailIntelligence Team"},
            "technology_stack": {"language": "Python", "framework": "FastAPI"},
            "deployment_environment": {"type": "Development"},
            "testing_phase": "improved",
            "user_profile": {
                "level": "intermediate",
                "team_size": "medium",
                "experience": "some"
            }
        }
    
    @pytest.fixture
    def sample_team_context(self):
        """Create sample team context"""
        return {
            "roles": ["Developer", "Technical Lead", "QA Engineer"],
            "skills": ["Git", "Constitutional Framework", "Quality Assurance"],
            "experience_level": "intermediate",
            "constraints": "Must maintain constitutional compliance",
            "preferences": {
                "risk_tolerance": "moderate",
                "execution_approach": "sequential",
                "rollback_strategy": "semi-automated"
            }
        }

    async def test_complete_specification_workflow(self, workflow_components, sample_conflict_data, sample_project_context, sample_team_context):
        """Test complete specification creation workflow"""
        template_generator = workflow_components["template_generator"]
        
        # Generate specification
        specification = await template_generator.generate_specification_template(
            sample_conflict_data,
            sample_project_context,
            sample_team_context,
            SpecificationPhase.IMPROVED
        )
        
        # Verify specification structure
        assert "template_metadata" in specification
        assert "template_content" in specification
        assert "constitutional_validation" in specification
        assert "quality_recommendations" in specification
        
        # Verify quality score
        quality_score = specification["template_metadata"]["quality_score"]
        assert 0.0 <= quality_score <= 1.0

    async def test_constitutional_compliance_integration(self, workflow_components, sample_conflict_data, sample_project_context, sample_team_context):
        """Test constitutional compliance throughout workflow"""
        template_generator = workflow_components["template_generator"]
        constitutional_engine = workflow_components["constitutional_engine"]
        
        # Generate specification
        specification = await template_generator.generate_specification_template(
            sample_conflict_data,
            sample_project_context,
            sample_team_context,
            SpecificationPhase.IMPROVED
        )
        
        # Validate with constitutional engine
        validation_result = await constitutional_engine.validate_template(specification)
        
        # Should have constitutional validation
        assert validation_result is not None
        assert validation_result.overall_score >= 0.0

    async def test_strategy_generation_integration(self, workflow_components, sample_conflict_data, sample_project_context):
        """Test strategy generation integration"""
        strategy_generator = workflow_components["strategy_generator"]
        
        # Generate strategies
        strategies = strategy_generator.generate_multi_phase_strategies(
            sample_conflict_data,
            sample_project_context,
            "medium",
            "normal"
        )
        
        # Verify strategies
        assert len(strategies) > 0
        
        for strategy in strategies:
            assert strategy.id is not None
            assert strategy.strategy_type is not None
            assert len(strategy.steps) > 0
            assert len(strategy.execution_phases) > 0

    async def test_workflow_coordination(self, workflow_components, sample_conflict_data, sample_project_context, sample_team_context):
        """Test coordination between workflow components"""
        template_generator = workflow_components["template_generator"]
        strategy_generator = workflow_components["strategy_generator"]
        
        # Step 1: Generate specification
        specification = await template_generator.generate_specification_template(
            sample_conflict_data,
            sample_project_context,
            sample_team_context,
            SpecificationPhase.IMPROVED
        )
        
        # Step 2: Generate strategy using specification context
        strategy_context = {
            "complexity_score": specification["template_metadata"].get("complexity_score", 5),
            "urgency_level": "medium",
            "feature_preservation_required": True,
            "estimated_resolution_time": specification["template_metadata"].get("estimated_time", 30)
        }
        
        strategies = strategy_generator.generate_multi_phase_strategies(
            sample_conflict_data,
            strategy_context,
            "medium",
            "normal"
        )
        
        # Verify integration
        assert len(strategies) > 0
        best_strategy = strategies[0]  # Highest ranked
        
        # Strategy should incorporate specification insights
        assert best_strategy.estimated_time > 0
        assert len(best_strategy.enhancement_preservation) > 0

    async def test_performance_integration(self, workflow_components, sample_conflict_data, sample_project_context, sample_team_context):
        """Test performance across integrated workflow"""
        import time
        
        template_generator = workflow_components["template_generator"]
        strategy_generator = workflow_components["strategy_generator"]
        
        # Measure complete workflow time
        start_time = time.time()
        
        # Generate specification
        specification = await template_generator.generate_specification_template(
            sample_conflict_data,
            sample_project_context,
            sample_team_context,
            SpecificationPhase.IMPROVED
        )
        
        # Generate strategies
        strategies = strategy_generator.generate_multi_phase_strategies(
            sample_conflict_data,
            sample_project_context,
            "medium",
            "normal"
        )
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Should complete within acceptable time
        assert total_time < 15.0  # 15 seconds maximum for complete workflow
        assert len(strategies) > 0

    async def test_error_propagation_integration(self, workflow_components):
        """Test error handling and propagation in integrated workflow"""
        template_generator = workflow_components["template_generator"]
        
        # Test with invalid data
        invalid_conflict_data = None
        invalid_context = {}
        
        try:
            specification = await template_generator.generate_specification_template(
                invalid_conflict_data,
                invalid_context,
                {},
                SpecificationPhase.IMPROVED
            )
            
            # Should handle gracefully or raise appropriate exception
            # Either way, should not crash
            assert specification is not None
            
        except (ValueError, TypeError, AttributeError):
            # Expected exceptions for invalid input
            pass

    async def test_quality_gate_integration(self, workflow_components, sample_conflict_data, sample_project_context, sample_team_context):
        """Test quality gates throughout the workflow"""
        template_generator = workflow_components["template_generator"]
        constitutional_engine = workflow_components["constitutional_engine"]
        
        # Generate specification
        specification = await template_generator.generate_specification_template(
            sample_conflict_data,
            sample_project_context,
            sample_team_context,
            SpecificationPhase.IMPROVED
        )
        
        # Check quality gates
        quality_score = specification["template_metadata"]["quality_score"]
        constitutional_score = specification["constitutional_validation"]["overall_score"]
        
        # Quality gates
        assert quality_score >= 0.5  # Minimum quality threshold
        assert constitutional_score >= 0.7  # Minimum constitutional compliance
        
        # Validate with constitutional engine
        validation_result = await constitutional_engine.validate_template(specification)
        assert validation_result.overall_score >= 0.5

    async def test_workflow_with_constitutional_violations(self, workflow_components, sample_conflict_data, sample_project_context, sample_team_context):
        """Test workflow handling of constitutional violations"""
        template_generator = workflow_components["template_generator"]
        constitutional_engine = workflow_components["constitutional_engine"]
        
        # Create template with potential violations
        problematic_context = {
            "organization": {"name": "EmailIntelligence Team"},
            "technology_stack": {"language": "Python", "framework": "FastAPI"},
            "deployment_environment": {"type": "Development"},
            "testing_phase": "baseline",  # Lower quality expectations
            "user_profile": {
                "level": "beginner",  # Lower expertise
                "team_size": "large",  # More coordination overhead
                "experience": "none"
            }
        }
        
        # Generate specification
        specification = await template_generator.generate_specification_template(
            sample_conflict_data,
            problematic_context,
            sample_team_context,
            SpecificationPhase.BASELINE
        )
        
        # Validate with constitutional engine
        validation_result = await constitutional_engine.validate_template(specification)
        
        # Should detect and report violations
        if len(validation_result.violations) > 0:
            # Verify violation reporting
            violation_types = [v.violation_type for v in validation_result.violations]
            assert len(violation_types) > 0
            
            # Should provide remediation suggestions
            for violation in validation_result.violations:
                assert violation.remediation_suggestion is not None

    async def test_parallel_workflow_capabilities(self, workflow_components, sample_conflict_data, sample_project_context):
        """Test parallel workflow execution capabilities"""
        strategy_generator = workflow_components["strategy_generator"]
        
        # Generate multiple strategies
        strategies = strategy_generator.generate_multi_phase_strategies(
            sample_conflict_data,
            sample_project_context,
            "medium",
            "normal"
        )
        
        # Check parallel execution support
        parallel_strategies = [s for s in strategies if s.parallel_executable]
        
        if parallel_strategies:
            # Verify parallel strategy characteristics
            for strategy in parallel_strategies:
                assert any(phase.parallel_executable for phase in strategy.execution_phases)
                assert len(strategy.execution_phases) > 0

    async def test_workflow_scalability(self, workflow_components):
        """Test workflow scalability with larger inputs"""
        template_generator = workflow_components["template_generator"]
        
        # Create larger conflict data
        large_conflict_data = type('MockConflict', (), {
            'conflict_type': 'content',
            'file_paths': [f'src/module_{i}.py' for i in range(20)],  # 20 files
            'pr_numbers': list(range(100, 110)),  # 10 PRs
            'branches': ['feature/major-refactor', 'main'],
            'complexity_score': 8,
            'affected_components': [f'component_{i}' for i in range(10)],
            'estimated_resolution_time': 120,
            'risk_level': 'HIGH',
            'stakeholder_impact': 'critical'
        })()
        
        large_project_context = {
            "organization": {"name": "Large Team Org"},
            "technology_stack": {"language": "Python", "framework": "FastAPI"},
            "deployment_environment": {"type": "Production"},
            "testing_phase": "improved",
            "user_profile": {
                "level": "expert",
                "team_size": "large",
                "experience": "extensive"
            }
        }
        
        # Should handle larger inputs without significant performance degradation
        import time
        start_time = time.time()
        
        specification = await template_generator.generate_specification_template(
            large_conflict_data,
            large_project_context,
            {},
            SpecificationPhase.IMPROVED
        )
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Should complete within reasonable time even for large inputs
        assert processing_time < 30.0  # 30 seconds maximum
        assert specification is not None

    async def test_constitutional_framework_compliance(self, workflow_components, sample_conflict_data, sample_project_context, sample_team_context):
        """Test overall constitutional framework compliance"""
        template_generator = workflow_components["template_generator"]
        constitutional_engine = workflow_components["constitutional_engine"]
        
        # Load constitutional rules
        await constitutional_engine.load_constitutional_rules_from_directory("constitutions/pr-resolution-templates")
        
        # Generate specification
        specification = await template_generator.generate_specification_template(
            sample_conflict_data,
            sample_project_context,
            sample_team_context,
            SpecificationPhase.IMPROVED
        )
        
        # Validate against constitutional framework
        validation_result = await constitutional_engine.validate_template(specification)
        
        # Should meet constitutional standards
        assert len(constitutional_engine.rule_cache) > 0  # Rules loaded
        assert validation_result.overall_score >= 0.0
        assert validation_result.constitutional_score >= 0.0


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])