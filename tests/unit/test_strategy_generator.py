"""
Unit tests for Strategy Generator

Tests multi-phase strategy generation, risk assessment, and preservation analysis.
"""

import pytest
import time

# Import the modules to test
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from src.strategy.multi_phase_generator import (  # noqa: E402
    MultiPhaseStrategyGenerator,
    StrategyType,
    RiskCategory,
    MultiPhaseStrategy,
    EnhancementPreservation,
    RiskFactor,
)


class TestMultiPhaseStrategyGenerator:
    """Test suite for MultiPhaseStrategyGenerator"""

    @pytest.fixture
    def generator(self):
        """Create a MultiPhaseStrategyGenerator instance for testing"""
        return MultiPhaseStrategyGenerator()

    @pytest.fixture
    def sample_conflict_data(self):
        """Create sample conflict data for testing"""
        return type(
            "MockConflict",
            (),
            {
                "conflict_type": "content",
                "file_paths": ["src/module1.py", "src/module2.py"],
                "similarity_score": 0.75,
                "affected_components": ["core_functionality"],
            },
        )()

    @pytest.fixture
    def sample_context(self):
        """Create sample resolution context for testing"""
        return {
            "complexity_score": 6,
            "urgency_level": "medium",
            "feature_preservation_required": True,
            "source_branch": "feature/new-implementation",
            "target_branch": "main",
            "affected_features": ["authentication", "user_management"],
            "team_experience_level": "medium",
            "estimated_resolution_time": 45,
        }

    async def test_generator_initialization(self, generator):
        """Test strategy generator initialization"""
        assert generator is not None
        assert len(generator.strategy_types) > 0
        assert StrategyType.CONSERVATIVE_MERGE in generator.strategy_types
        assert len(generator.preservation_patterns) > 0

    async def test_strategy_type_selection(self, generator, sample_conflict_data, sample_context):
        """Test strategy type selection based on context"""
        # Test with medium risk tolerance
        selected_types = generator._select_strategy_types(
            sample_conflict_data, sample_context, "medium"
        )

        assert StrategyType.CONSERVATIVE_MERGE in selected_types
        assert StrategyType.FEATURE_PRESERVATION in selected_types

        # Test with low risk tolerance (should include safe mode)
        selected_types_low = generator._select_strategy_types(
            sample_conflict_data, sample_context, "very_low"
        )

        assert StrategyType.SAFE_MODE in selected_types_low

    async def test_single_strategy_generation(
        self, generator, sample_conflict_data, sample_context
    ):
        """Test single strategy generation"""
        strategy = generator._generate_single_strategy(
            StrategyType.FEATURE_PRESERVATION,
            sample_conflict_data,
            sample_context,
            "medium",
            "normal",
        )

        assert strategy is not None
        assert isinstance(strategy, MultiPhaseStrategy)
        assert strategy.strategy_type == StrategyType.FEATURE_PRESERVATION
        assert len(strategy.steps) > 0
        assert len(strategy.enhancement_preservation) > 0

    async def test_enhancement_preservation_analysis(
        self, generator, sample_conflict_data, sample_context
    ):
        """Test enhancement preservation analysis"""
        preservation_list = generator._generate_enhancement_preservation(
            sample_conflict_data, sample_context, StrategyType.FEATURE_PRESERVATION
        )

        assert len(preservation_list) > 0

        for preservation in preservation_list:
            assert isinstance(preservation, EnhancementPreservation)
            assert preservation.feature_name is not None
            assert preservation.preservation_priority in ["high", "medium", "low"]

    async def test_risk_factor_generation(self, generator, sample_conflict_data, sample_context):
        """Test risk factor generation"""
        risk_factors = generator._generate_risk_factors(
            sample_conflict_data,
            sample_context,
            StrategyType.CONSERVATIVE_MERGE,
            "medium",
        )

        assert len(risk_factors) > 0

        for risk in risk_factors:
            assert isinstance(risk, RiskFactor)
            assert risk.category in list(RiskCategory)
            assert 0.0 <= risk.probability <= 1.0
            assert 0.0 <= risk.impact <= 1.0
            assert risk.mitigation_strategy is not None

    async def test_execution_phases_generation(
        self, generator, sample_conflict_data, sample_context
    ):
        """Test execution phases generation"""
        execution_phases = generator._generate_execution_phases(
            sample_conflict_data, sample_context, StrategyType.CONSERVATIVE_MERGE
        )

        assert len(execution_phases) > 0

        # Should include validation phase
        phase_types = [phase.phase for phase in execution_phases]
        assert "validation" in phase_types

    async def test_multi_strategy_generation(self, generator, sample_conflict_data, sample_context):
        """Test generation of multiple strategies"""
        strategies = generator.generate_multi_phase_strategies(
            sample_conflict_data, sample_context, "medium", "normal"
        )

        assert len(strategies) > 0

        # Strategies should be ranked by confidence
        for i in range(len(strategies) - 1):
            assert strategies[i].confidence >= strategies[i + 1].confidence

    async def test_hybrid_strategy_generation(
        self, generator, sample_conflict_data, sample_context
    ):
        """Test hybrid strategy generation"""
        # First generate individual strategies
        strategies = generator.generate_multi_phase_strategies(
            sample_conflict_data, sample_context, "medium", "normal"
        )

        if len(strategies) >= 2:
            hybrid = generator._generate_hybrid_strategy(
                strategies, sample_conflict_data, sample_context
            )

            if hybrid:
                assert hybrid.strategy_type == StrategyType.HYBRID_APPROACH
                assert hybrid.confidence > 0.0

    async def test_strategy_ranking(self, generator):
        """Test strategy ranking functionality"""
        # Create mock strategies with different confidence levels
        strategy1 = MultiPhaseStrategy(
            id="strategy1",
            name="High Confidence",
            strategy_type=StrategyType.CONSERVATIVE_MERGE,
            approach="Test approach",
            steps=[],
            pros=["Pro 1"],
            cons=["Con 1"],
            confidence=0.9,
            estimated_time=30,
            risk_level="low",
            resource_requirements={},
            requires_approval=False,
            success_criteria=[],
            rollback_strategy="",
            validation_approach="",
            enhancement_preservation=[],
            risk_factors=[],
            execution_phases=[],
        )

        strategy2 = MultiPhaseStrategy(
            id="strategy2",
            name="Low Confidence",
            strategy_type=StrategyType.FAST_TRACK,
            approach="Test approach",
            steps=[],
            pros=["Pro 2"],
            cons=["Con 2"],
            confidence=0.5,
            estimated_time=20,
            risk_level="high",
            resource_requirements={},
            requires_approval=False,
            success_criteria=[],
            rollback_strategy="",
            validation_approach="",
            enhancement_preservation=[],
            risk_factors=[],
            execution_phases=[],
        )

        strategies = [strategy2, strategy1]  # Unsorted
        ranked = generator._rank_strategies(strategies)

        # High confidence strategy should come first
        assert ranked[0].confidence >= ranked[1].confidence

    async def test_confidence_calculation(self, generator, sample_conflict_data, sample_context):
        """Test strategy confidence calculation"""
        confidence = generator._calculate_strategy_confidence(
            StrategyType.CONSERVATIVE_MERGE, [], sample_context
        )

        assert 0.0 <= confidence <= 1.0
        assert confidence > 0.0

    async def test_risk_level_calculation(self, generator):
        """Test risk level calculation from risk factors"""
        # Create mock risk factors with different risk levels
        low_risk = RiskFactor(
            id="low_risk",
            category=RiskCategory.TECHNICAL,
            description="Low risk factor",
            probability=0.1,
            impact=0.2,
            mitigation_strategy="Standard mitigation",
            residual_risk=0.05,
            owner="Tech Lead",
        )

        high_risk = RiskFactor(
            id="high_risk",
            category=RiskCategory.BUSINESS,
            description="High risk factor",
            probability=0.8,
            impact=0.9,
            mitigation_strategy="Comprehensive mitigation",
            residual_risk=0.6,
            owner="Product Manager",
        )

        risk_factors = [low_risk, high_risk]
        risk_level = generator._calculate_risk_level(risk_factors)

        # Should result in medium to high risk due to high risk factor
        assert risk_level in ["medium", "high"]

    async def test_performance_benchmarks(self, generator, sample_conflict_data, sample_context):
        """Test strategy generation performance"""
        # Measure strategy generation time
        start_time = time.time()

        strategies = generator.generate_multi_phase_strategies(
            sample_conflict_data, sample_context, "medium", "normal"
        )

        end_time = time.time()
        generation_time = end_time - start_time

        # Should complete within reasonable time
        assert generation_time < 10.0  # 10 seconds maximum
        assert len(strategies) > 0

    async def test_parallel_execution_detection(
        self, generator, sample_conflict_data, sample_context
    ):
        """Test parallel execution capability detection"""
        strategies = generator.generate_multi_phase_strategies(
            sample_conflict_data, sample_context, "medium", "normal"
        )

        for strategy in strategies:
            # Check if parallel execution is properly detected
            if strategy.parallel_executable:
                assert any(phase.parallel_executable for phase in strategy.execution_phases)

    async def test_resource_requirement_generation(
        self, generator, sample_conflict_data, sample_context
    ):
        """Test resource requirement calculation"""
        strategy = generator._generate_single_strategy(
            StrategyType.CONSERVATIVE_MERGE,
            sample_conflict_data,
            sample_context,
            "medium",
            "normal",
        )

        assert strategy is not None
        assert "execution_phases" in strategy.resource_requirements
        assert "estimated_phases_time" in strategy.resource_requirements
        assert strategy.resource_requirements["execution_phases"] > 0

    async def test_complexity_adaptation(self, generator, sample_conflict_data):
        """Test strategy adaptation based on complexity"""
        # Test with high complexity
        high_complexity_context = {
            "complexity_score": 9,
            "urgency_level": "low",
            "estimated_resolution_time": 60,
        }

        strategy = generator._generate_single_strategy(
            StrategyType.CONSERVATIVE_MERGE,
            sample_conflict_data,
            high_complexity_context,
            "medium",
            "normal",
        )

        assert strategy is not None
        assert strategy.estimated_time >= 60  # Should be adjusted for complexity

    async def test_time_constraint_handling(self, generator, sample_conflict_data, sample_context):
        """Test strategy time constraint handling"""
        # Test tight time constraints
        strategies_tight = generator.generate_multi_phase_strategies(
            sample_conflict_data, sample_context, "medium", "tight"
        )

        # Test relaxed time constraints
        strategies_relaxed = generator.generate_multi_phase_strategies(
            sample_conflict_data, sample_context, "medium", "relaxed"
        )

        # Should generate different strategies based on time constraints
        assert len(strategies_tight) > 0
        assert len(strategies_relaxed) > 0


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
