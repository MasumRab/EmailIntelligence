import pytest
from unittest.mock import MagicMock
from src.analysis.dependency import DependencyAnalyzer, DependencyNode
from src.core.conflict_models import Conflict, ConflictTypeExtended, RiskLevel

@pytest.fixture
def analyzer():
    return DependencyAnalyzer()

def test_detect_cycles_no_cycle(analyzer):
    """Test that no cycles are detected in a linear graph."""
    analyzer.graph = {
        "A": DependencyNode(name="A", dependencies={"B"}),
        "B": DependencyNode(name="B", dependencies={"C"}),
        "C": DependencyNode(name="C", dependencies=set()),
    }
    cycles = analyzer._detect_cycles()
    assert len(cycles) == 0

def test_detect_cycles_simple_cycle(analyzer):
    """Test detection of a simple A -> B -> A cycle."""
    analyzer.graph = {
        "A": DependencyNode(name="A", dependencies={"B"}),
        "B": DependencyNode(name="B", dependencies={"A"}),
    }
    cycles = analyzer._detect_cycles()
    assert len(cycles) > 0
    # Check if the detected cycle matches expected structure
    # The cycle could be reported starting from A or B
    valid_cycles = [["A", "B", "A"], ["B", "A", "B"]]
    assert any(cycle in valid_cycles for cycle in cycles)

def test_detect_cycles_self_cycle(analyzer):
    """Test detection of a self-reference cycle A -> A."""
    analyzer.graph = {
        "A": DependencyNode(name="A", dependencies={"A"}),
    }
    cycles = analyzer._detect_cycles()
    assert len(cycles) > 0
    assert ["A", "A"] in cycles

def test_detect_cycles_complex(analyzer):
    """Test detection in a more complex graph."""
    # A -> B -> C -> A (cycle)
    # D -> E (no cycle)
    analyzer.graph = {
        "A": DependencyNode(name="A", dependencies={"B"}),
        "B": DependencyNode(name="B", dependencies={"C"}),
        "C": DependencyNode(name="C", dependencies={"A"}),
        "D": DependencyNode(name="D", dependencies={"E"}),
        "E": DependencyNode(name="E", dependencies=set()),
    }
    cycles = analyzer._detect_cycles()
    assert len(cycles) > 0
    
    # Verify A-B-C-A cycle is found
    cycle_found = False
    for cycle in cycles:
        if set(cycle) == {"A", "B", "C"}:
            cycle_found = True
            break
    assert cycle_found

@pytest.mark.asyncio
async def test_analyze_dependency_conflict(analyzer):
    """Test analyze method returns conflicts when cycles exist."""
    analyzer.graph = {
        "A": DependencyNode(name="A", dependencies={"B"}),
        "B": DependencyNode(name="B", dependencies={"A"}),
    }
    
    conflict = MagicMock(spec=Conflict)
    conflict.type = ConflictTypeExtended.DEPENDENCY_CONFLICT
    
    results = await analyzer.analyze(conflict)
    
    assert len(results) > 0
    assert results[0].conflict_type == "circular_dependency"
    assert results[0].severity == RiskLevel.HIGH
    assert "Refactor to break cycle" in results[0].resolution_suggestions

@pytest.mark.asyncio
async def test_analyze_ignores_non_dependency_conflict(analyzer):
    """Test analyze returns empty list for non-dependency conflicts."""
    conflict = MagicMock(spec=Conflict)
    # Use a different conflict type
    conflict.type = "some_other_type" 
    
    results = await analyzer.analyze(conflict)
    assert len(results) == 0
