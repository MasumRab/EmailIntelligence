# Prioritized Implementation Roadmap

**Based on:** GAP_ANALYSIS_REPORT.md  
**Target Branch:** orchestration-tools (tooling substrate)  
**Base Commit:** baa620e6 (fully restored branch clustering)

---

## 🎯 Priority Matrix

| Priority | Task | Effort | Blocking | Week |
|----------|------|--------|----------|------|
| **P0-1** | Copy interface.py, factory.py, registry.py to orchestration-tools | 30 min | None | Week 1 |
| **P0-2** | Copy src/git/ module (worktree.py, conflict_detector.py, repository.py) | 30 min | None | Week 1 |
| **P0-3** | Copy analysis/constitutional/analyzer.py from .taskmaster | 30 min | None | Week 1 |
| **P0-4** | Copy src/git/history.py (GitHistory + CommitClassifier) | 30 min | None | Week 1 |
| **P0-5** | Register ClusterBranchesCommand on orchestration-tools | 15 min | P0-1, P0-2 | Week 1 |
| **P0-6** | Test `branch-cluster --help` and basic execution | 30 min | P0-5 | Week 1 |
| **P0-7** | Test `branch-cluster --mode hybrid --output test.json` | 30 min | P0-6 | Week 1 |

---

## Week 1: Foundation (Days 1-2) ✅ **START HERE**

### Day 1: Copy Core Infrastructure
```bash
# 1. Copy CLI infrastructure to orchestration-tools
cd /home/masum/github/remote/EmailIntelligence
git checkout orchestration-tools

# Copy from main (these exist on main)
cp src/cli/commands/interface.py src/cli/commands/
cp src/cli/commands/factory.py src/cli/commands/
cp src/cli/commands/registry.py src/cli/commands/

# Copy git module from main
cp -r src/git src/git

# Copy analysis module from .taskmaster
mkdir -p src/analysis/constitutional
cp .taskmaster/src/analysis/constitutional/analyzer.py src/analysis/constitutional/
cp .taskmaster/src/analysis/constitutional/requirement_checker.py src/analysis/constitutional/

# Copy git/history.py from main (651ef165 commit)
git show 651ef165:src/git/history.py > src/git/history.py
git show 651ef165:src/git/conflict_detector.py > src/git/conflict_detector.py
```

### Day 2: Register & Test
```bash
# Register ClusterBranchesCommand in integration.py
# (already done in integration.py - verify)

# Test the command
cd /home/masum/github/remote/EmailIntelligence
git checkout orchestration-tools
python3 -c "
import sys
sys.path.insert(0, 'src')
from cli.commands.task.cluster_branches import ClusterBranchesCommand
cmd = ClusterBranchesCommand()
print('Name:', cmd.name)
print('Description:', cmd.description)
"
# Expected: Name: branch-cluster, Description: Cluster and categorize Git branches by semantic and structural similarity

# Test CLI
python3 -c "
import sys
sys.path.insert(0, 'src')
import argparse
from cli.commands.task.cluster_branches import ClusterBranchesCommand
parser = argparse.ArgumentParser()
cmd = ClusterBranchesCommand()
cmd.add_arguments(parser)
args = parser.parse_args(['--primary', 'origin/main', '--mode', 'hybrid', '--output', 'test.json'])
print('All args parsed:', args)
"

# Run actual clustering
python -m src.cli.commands.task.cluster_branches --primary origin/main --mode hybrid --output test_results.json
```

---

## Week 2: Core Features (Days 3-7)

### P1-1: Git merge-tree Implementation (FR-002) - 2 days
```python
# In src/git/conflict_detector.py
async def detect_conflicts_between_branches(self, source_branch: str, target_branch: str) -> List[Conflict]:
    """Use git merge-tree --real-merge for zero working-tree side effects."""
    # Implementation using git merge-tree --real-merge
    # Parse output for conflict hunks
    # Return structured Conflict objects
```

### P1-2: DAG Rebase Planner (FR-003) - 2 days
```python
# In src/strategy/reordering.py
class RebasePlanner:
    def build_commit_dag(self, commits: List[Commit]) -> nx.DiGraph:
        """Build dependency graph from commits"""
    
    def topological_sort(self, dag: nx.DiGraph) -> List[str]:
        """Return topologically sorted commit SHAs"""
    
    def plan_rebase(self, branch: str, base: str) -> RebasePlan:
        """Generate rebase plan with dependencies"""
```

### P1-3: AST Constitutional Scanner (FR-004) - 2 days
```python
# In src/analysis/constitutional/analyzer.py
class ConstitutionalAnalyzer:
    def __init__(self, constitution_path: str = "constitution.md"):
        self.rules = self._parse_constitution(constitution_path)
    
    async def scan(self, files: List[str]) -> List[Violation]:
        """Scan files for constitutional violations using AST"""
        # Parse constitution.md rules
        # Walk AST of each file
        # Return violations with rule, file, line, snippet
```

### P1-4: Pydantic Models (FR-005) - 1 day
```python
# In src/core/models.py or shared models
from pydantic import BaseModel

class ConflictModel(BaseModel):
    file: str
    type: str
    hunks: List[HunkModel]

class CommitNode(BaseModel):
    sha: str
    message: str
    category: str
    risk_level: str

class ExecutionPlan(BaseModel):
    steps: List[PlanStep]
```

---

## Week 3: Integration & Testing

### P1-5: Git Hooks (FR-017) - 2 days
```bash
# In scripts/hooks/
# pre-commit: AST constitutional scan
# pre-push: Branch clustering analysis
# commit-msg: Conventional commit validation
```

### P1-6: Session Persistence (FR-014) - 1 day
```python
# In src/core/session.py
class SessionManager:
    def save_state(self, session_id: str, step: int, data: dict):
        """Atomic write to .dev_state.json"""
    
    def load_state(self, session_id: str) -> SessionState:
        """Load session state for recovery"""
```

---

## Week 4: Advanced Features

### P2-1: AST-grep Integration (FR-024) - 2 days
```python
# In src/analysis/structural.py
import subprocess
import json

class StructuralAnalyzer:
    def extract_dependencies(self, code: str) -> StructuralDeps:
        """Use ast-grep for structural pattern matching"""
        # Run ast-grep with patterns for imports, calls, classes
```

### P2-2: Dependency Extraction (FR-019, FR-020) - 2 days
```python
# In src/analysis/dependencies.py
class DependencyAnalyzer:
    def extract(self, path: str) -> DependencyGraph:
        """Extract imports, calls, classes using AST"""
    
    def compare(self, branch_a: str, branch_b: str) -> DiffReport:
        """Return {added, removed, moved, refactored}"""
```

### P2-3: Session Persistence (FR-014) - 1 day
```python
# In src/core/session.py
class SessionManager:
    def save_atomic(self, state: SessionState):
        """Atomic write with temp file + rename"""
    
    def load(self) -> SessionState:
        """Load and validate session state"""
```

---

## 📅 4-Week Sprint Plan

| Week | Focus | Deliverables |
|------|-------|--------------|
| **Week 1** | Foundation | ✅ CLI infra, git module, branch-cluster working |
| **Week 2** | Core Features | merge-tree, DAG rebase, AST scanner, Pydantic models |
| **Week 3** | Integration | Git hooks, session persistence, dry-run |
| **Week 4** | Advanced | AST-grep, deps compare, session persistence |

---

## 🎯 Success Criteria (Definition of Done)

| Milestone | Criteria |
|-----------|----------|
| **Foundation** | `branch-cluster --help` works, all 7 CLI commands registered |
| **Core** | `branch-cluster --mode hybrid --output test.json` produces valid JSON |
| **Core Features** | `git merge-tree` detects conflicts, rebase plan generates valid DAG |
| **Integration** | All 7 commands work with `--json` and `--dry-run` |
| **Advanced** | AST-grep extracts structural deps, session persists across crashes |

---

## 🚨 Risk Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Missing gtr binary | Medium | High | Fallback to native git worktree |
| Missing libcst | Low | Medium | Graceful fallback to AST only |
| Missing ast-grep | Medium | Medium | Optional feature, graceful degradation |
| Missing Pydantic | Low | High | Add to requirements.txt |
| Git merge-tree failures | Medium | High | Graceful fallback with clear errors |

---

## 📦 Dependencies to Add

```txt
# requirements.txt additions
typer>=0.9.0
rich>=13.0.0
InquirerPy>=0.3.4
pydantic>=2.0.0
libcst>=1.0.0
ast-grep>=0.30.0  # optional
networkx>=3.0  # for DAG
GitPython>=3.1.0
```

---

## ✅ Quick Validation Checklist

Run after each phase:
- [ ] `python -m src.cli.commands.task.cluster_branches --help` works
- [ ] `python -m src.cli branch-cluster --primary origin/main --mode hybrid --output test.json` produces valid JSON
- [ ] All 7 commands appear in `registry.get_available_commands()`
- [ ] `git merge-tree` detection works on conflicting branches
- [ ] Rebase plan generates valid topological order
- [ ] AST scanner finds violations in test files
- [ ] Session state persists across restarts
- [ ] Git hooks install and run on commit/push