
import pytest
from unittest.mock import MagicMock
from src.strategy.reordering import RebasePlanner
from src.git.history import Commit
from src.resolution.types import RiskLevel

from datetime import datetime

@pytest.fixture
def planner():
    return RebasePlanner()

def test_generate_plan_grouping(planner):
    now = datetime.now()
    commits = [
        Commit(hash="1", message="Critical fix", risk_level=RiskLevel.CRITICAL.value, category="fix", author="Test", date=now),
        Commit(hash="2", message="Chore update", risk_level=RiskLevel.LOW.value, category="chore", author="Test", date=now),
        Commit(hash="3", message="New feature", risk_level=RiskLevel.MEDIUM.value, category="feat", author="Test", date=now),
        Commit(hash="4", message="Bug fix", risk_level=RiskLevel.LOW.value, category="fix", author="Test", date=now),
        Commit(hash="5", message="Docs update", risk_level=RiskLevel.LOW.value, category="docs", author="Test", date=now),
    ]
    
    plan = planner.generate_plan(commits)
    
    # Check Phase 1: Critical & Infra
    assert "## Phase 1: Critical & Infrastructure" in plan
    assert "pick 1 Critical fix" in plan
    assert "pick 2 Chore update" in plan
    
    # Check Phase 2: Features
    assert "## Phase 2: Features" in plan
    assert "pick 3 New feature" in plan
    
    # Check Phase 3: Fixes
    assert "## Phase 3: Fixes" in plan
    assert "pick 4 Bug fix" in plan
    
    # Check Phase 4: Docs
    assert "## Phase 4: Documentation & Cleanup" in plan
    assert "pick 5 Docs update" in plan

def test_generate_plan_ordering(planner):
    """Test that critical items come before others."""
    now = datetime.now()
    commits = [
        Commit(hash="1", message="Feature", risk_level=RiskLevel.MEDIUM.value, category="feat", author="Test", date=now),
        Commit(hash="2", message="Critical", risk_level=RiskLevel.CRITICAL.value, category="fix", author="Test", date=now),
    ]
    
    plan = planner.generate_plan(commits)
    
    # Critical should be in Phase 1, Feature in Phase 2
    phase1_idx = plan.find("## Phase 1")
    phase2_idx = plan.find("## Phase 2")
    
    crit_idx = plan.find("pick 2")
    feat_idx = plan.find("pick 1")
    
    assert phase1_idx < crit_idx < phase2_idx < feat_idx
