
import pytest
import asyncio
from src.strategy.generator import StrategyGenerator
from src.core.models import (
    Conflict, 
    ConflictBlock, 
    ConflictTypeExtended, 
    RiskLevel, 
    AnalysisResult
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
        file_paths=["src/core/auth.py"], # Core/Auth = High Risk
        blocks=[
            ConflictBlock(
                file_path="src/core/auth.py",
                start_line=1,
                end_line=100,
                current_content="def login(): pass",
                incoming_content="def authenticate(): pass", # Renamed function
                conflict_marker_type="git"
            )
        ]
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
        confidence_score=0.9
    )
    
    strategies = await generator.generate_strategies(conflict, analysis)
    
    assert len(strategies) >= 1
    primary = strategies[0]
    assert primary.type == "manual"
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
        blocks=[]
    )
    
    analysis = AnalysisResult(
        conflict_id=conflict.id,
        complexity_score=10.0,
        risk_level=RiskLevel.LOW,
        estimated_resolution_time_minutes=5,
        is_auto_resolvable=True,
        recommended_strategy_type="accept_incoming",
        root_cause="Documentation update",
        confidence_score=0.95
    )
    
    strategies = await generator.generate_strategies(conflict, analysis)
    
    assert len(strategies) >= 1
    primary = strategies[0]
    assert primary.type == "accept_incoming"
    assert primary.requires_approval is False
