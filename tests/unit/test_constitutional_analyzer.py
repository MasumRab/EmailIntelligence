
import pytest
import asyncio
from src.analysis.constitutional.analyzer import ConstitutionalAnalyzer
from src.core.models import Conflict, ConflictBlock, ConflictTypeExtended, RiskLevel

@pytest.mark.asyncio
async def test_constitutional_analysis_violations():
    analyzer = ConstitutionalAnalyzer()
    
    # Code with violations: No docstring, no type hints, no error handling
    bad_code = """
def risky_function(x):
    return x * 2
    """
    
    conflict = Conflict(
        id="test-conflict",
        type=ConflictTypeExtended.MERGE_CONFLICT,
        severity=RiskLevel.MEDIUM,
        description="Test conflict",
        file_paths=["test.py"],
        blocks=[
            ConflictBlock(
                file_path="test.py",
                start_line=1,
                end_line=3,
                current_content="",
                incoming_content=bad_code,
                conflict_marker_type="git"
            )
        ]
    )
    
    result = await analyzer.analyze(conflict)
    
    assert result.risk_level in [RiskLevel.HIGH, RiskLevel.MEDIUM]
    assert len(result.constitutional_violations) > 0
    assert any("docstring" in v.lower() for v in result.constitutional_violations)
    assert any("type hints" in v.lower() for v in result.constitutional_violations)

@pytest.mark.asyncio
async def test_constitutional_analysis_clean():
    analyzer = ConstitutionalAnalyzer()
    
    # Clean code
    good_code = """
def safe_function(x: int) -> int:
    \"\"\"Safely doubles the input.\"\"\"
    try:
        return x * 2
    except Exception:
        return 0
    """
    
    conflict = Conflict(
        id="test-conflict-clean",
        type=ConflictTypeExtended.MERGE_CONFLICT,
        severity=RiskLevel.LOW,
        description="Test conflict",
        file_paths=["test.py"],
        blocks=[
            ConflictBlock(
                file_path="test.py",
                start_line=1,
                end_line=8,
                current_content="",
                incoming_content=good_code,
                conflict_marker_type="git"
            )
        ]
    )
    
    result = await analyzer.analyze(conflict)
    
    # Should have fewer violations (maybe none depending on strictness)
    # Note: ErrorHandlingChecker checks if *file* has error handling if it has functions
    # Our snippet has both.
    
    # We expect risk to be lower than the bad code
    assert result.risk_level in [RiskLevel.LOW, RiskLevel.MEDIUM]
