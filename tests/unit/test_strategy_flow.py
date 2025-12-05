import pytest
from src.strategy.generator import StrategyGenerator
from src.core.conflict_models import (
    Conflict,
    ConflictBlock,
    ConflictTypeExtended,
    RiskLevel,
    AnalysisResult,
)


@pytest.mark.asyncio
async def test_strategy_generation_manual_high_risk():
    generator = StrategyGenerator()

    # High risk conflict (breaking change + high complexity)
    conflict = Conflict(
        id="conflict-high-risk",
        type=ConflictTypeExtended.MERGE_CONFLICT,
        severity=RiskLevel.HIGH,
        description="Complex conflict",
        file_paths=["src/core/auth.py"],  # Core/Auth = High Risk
        blocks=[
            ConflictBlock(
                file_path="src/core/auth.py",
                start_line=1,
                end_line=100,
                current_content="def login(): pass",
                incoming_content="def authenticate(): pass",  # Renamed function
                conflict_marker_type="git",
            )
        ],
    )

    # Mock analysis result
    analysis = AnalysisResult(
        conflict_id=conflict.id,
        complexity_score=85.0,
        risk_level=RiskLevel.HIGH,
        estimated_resolution_time_minutes=30,
        is_auto_resolvable=False,
        recommended_strategy_type="manual",
        root_cause="Breaking API change",
        confidence_score=0.9,
    )

    strategies = await generator.generate_strategies(conflict, analysis)

    assert len(strategies) >= 1
    primary = strategies[0]
    assert primary.name == "Manual Resolution"
    assert primary.requires_approval is True
    assert len(primary.steps) > 0


@pytest.mark.asyncio
async def test_strategy_generation_auto_low_risk():
    generator = StrategyGenerator()

    # Low risk conflict
    conflict = Conflict(
        id="conflict-low-risk",
        type=ConflictTypeExtended.MERGE_CONFLICT,
        severity=RiskLevel.LOW,
        description="Simple conflict",
        file_paths=["README.md"],
        blocks=[],
    )

    analysis = AnalysisResult(
        conflict_id=conflict.id,
        complexity_score=10.0,
        risk_level=RiskLevel.LOW,
        estimated_resolution_time_minutes=5,
        is_auto_resolvable=True,
        recommended_strategy_type="accept_incoming",
        root_cause="Documentation update",
        confidence_score=0.95,
    )

    strategies = await generator.generate_strategies(conflict, analysis)

    assert len(strategies) >= 1
    primary = strategies[0]
    assert primary.name == "Accept Incoming"
    assert primary.requires_approval is False


@pytest.mark.asyncio
async def test_strategy_generation_ai():
    """Test AI strategy generation when enabled."""
    from unittest.mock import patch, MagicMock
    import json
    
    # Mock settings to enable AI
    with patch("src.strategy.generator.settings") as mock_settings:
        mock_settings.use_ai_strategies = True
        mock_settings.gemini_model = "gemini-pro"
        
        # Create generator with mocked AI client
        generator = StrategyGenerator()
        generator.ai_client = MagicMock()
        
        # Mock AI response
        ai_response_json = {
            "strategy": {
                "name": "AI Optimized Strategy",
                "approach": "Smart merge",
                "steps": [
                    {
                        "id": "step1",
                        "description": "AI Step 1",
                        "risk_level": "LOW",
                        "estimated_time": 5
                    }
                ],
                "confidence": 0.95,
                "risk_level": "LOW",
                "requires_approval": False
            }
        }
        
        # Mock generate_content to return JSON string
        async def mock_generate(*args, **kwargs):
            return json.dumps(ai_response_json)
            
        generator.ai_client.generate_content.side_effect = mock_generate
        
        # Create conflict and analysis
        conflict = Conflict(
            id="conflict-ai",
            type=ConflictTypeExtended.MERGE_CONFLICT,
            severity=RiskLevel.MEDIUM,
            description="AI test conflict",
            file_paths=["src/test.py"],
            blocks=[
                ConflictBlock(
                    file_path="src/test.py",
                    start_line=1,
                    end_line=10,
                    current_content="A",
                    incoming_content="B",
                    base_content="C",
                    conflict_marker_type="git"
                )
            ]
        )
        
        analysis = AnalysisResult(
            conflict_id=conflict.id,
            complexity_score=50.0,
            risk_level=RiskLevel.MEDIUM,
            estimated_resolution_time_minutes=15,
            is_auto_resolvable=False,
            recommended_strategy_type="manual", # Default to manual so AI kicks in
            root_cause="Logic change",
            confidence_score=0.7
        )
        
        strategies = await generator.generate_strategies(conflict, analysis)
        
        # Should have manual strategy AND AI strategy
        assert len(strategies) >= 2
        
        # Find AI strategy
        ai_strategy = next((s for s in strategies if getattr(s, "ai_generated", False)), None)
        assert ai_strategy is not None
        assert ai_strategy.name == "AI Optimized Strategy"
        assert ai_strategy.model_used == "gemini-pro"
        assert len(ai_strategy.steps) == 1
        assert ai_strategy.steps[0].description == "AI Step 1"
