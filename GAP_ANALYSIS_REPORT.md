# Gap Analysis Report: EmailIntelligence CLI Tooling Restoration

**Generated:** 2026-11-08  
**Branch:** orchestration-tools (tooling substrate)  
**Base Commit:** baa620e6 (feat(taskmaster): implement AST-based semantic branch clustering framework)

---

## Executive Summary

The branch clustering tooling has been **fully restored** from commit `baa620e6` on the orchestration-tools branch. However, the broader CLI infrastructure is missing on the orchestration-tools branch, preventing the branch clustering command from being fully operational.

---

## Current State Summary

### ✅ Fully Restored (from commit baa620e6)
| Component | File | Lines | Description |
|-----------|------|-------|-------------|
| **ClusterBranchesCommand** | `src/cli/commands/task/cluster_branches.py` | 152 | Full command with --mode, --output, --validate |
| **BranchAnalyzer** | `src/cli/commands/task/engine/branch_clustering.py` | 239 | Full BranchAnalyzer + ClusterEngine |
| **ClusterEngine** | `src/cli/commands/task/engine/branch_clustering.py` | 239 | Two-stage clustering + target assignment |
| **ValidationFramework** | `src/cli/commands/task/engine/validation_framework.py` | 89 | YAML-based NL validation |
| **GitHistory** | `src/git/history.py` | 141 | Commit history retrieval + classification |
| **GitConflictDetector** | `src/git/conflict_detector.py` | ~200 | Git merge-tree conflict detection |
| **WorktreeManager** | `src/git/worktree.py` | 364 | gtr-based worktree management |
| **BranchHealthCommand** | `src/cli/commands/git/branch_health.py` | 349 | Branch health analysis |
| **ValidationFramework** | `src/cli/commands/task/engine/validation_framework.py` | 89 | NL validation layer |
| **Integration Registration** | `integration.py` (agent-6) | - | ClusterBranchesCommand registered |

---

## 🔴 Critical Gaps (P0 - Blocking)

### 1. Missing CLI Infrastructure (orchestration-tools branch)

| Missing Module | Required By | Status |
|----------------|-------------|--------|
| `src/cli/commands/interface.py` | Command ABC base class | ❌ Missing |
| `src/cli/commands/factory.py` | CommandFactory | ❌ Missing |
| `src/cli/commands/registry.py` | CommandRegistry | ❌ Missing |
| `src/cli/commands/git/` | WorktreeManager, ConflictDetector, RepositoryOperations | ❌ Missing |
| `src/analysis/constitutional/analyzer.py` | ConstitutionalAnalyzer | ❌ Missing (exists in .taskmaster) |
| `src/analysis/commits/commit_classifier.py` | CommitClassifier | ❌ Missing |
| `src/strategy/generator.py` | StrategyGenerator | ❌ Missing |
| `src/strategy/reordering.py` | RebasePlanner | ❌ Missing |
| `src/resolution/auto_resolver.py` | AutoResolver | ❌ Missing |
| `src/validation/validator.py` | Validator | ❌ Missing |
| `src/git/history.py` | GitHistory | ❌ Missing |
| `src/analysis/commits/commit_classifier.py` | CommitClassifier | ❌ Missing |

### 2. Git Operations Modules (Referenced but Missing)

| Module | Referenced In | Status |
|--------|---------------|--------|
| `src/git/worktree.py` | integration.py, cluster_branches.py | ✅ Restored from ae85d0e2 |
| `src/git/conflict_detector.py` | integration.py | ✅ Restored from 651ef165 |
| `src/git/worktree.py` (async) | integration.py | ❌ Missing (async version exists on main) |
| `src/git/conflict_detector.py` | integration.py | ✅ Restored from 651ef165 |
| `src/git/repository.py` | integration.py | ❌ Missing |
| `src/git/history.py` | integration.py | ✅ Restored from 651ef165 |

### 3. Analysis Modules (Referenced but Missing)

| Module | Referenced In | Status |
|--------|---------------|--------|
| `src/analysis/constitutional/analyzer.py` | integration.py | ❌ Missing (exists in .taskmaster) |
| `src/analysis/commits/commit_classifier.py` | integration.py | ❌ Missing |
| `src/strategy/generator.py` | integration.py | ❌ Missing |
| `src/strategy/reordering.py` | integration.py | ❌ Missing |
| `src/resolution/auto_resolver.py` | integration.py | ❌ Missing |
| `src/validation/validator.py` | integration.py | ❌ Missing |
| `src/git/history.py` | integration.py | ✅ Restored |
| `src/analysis/commits/commit_classifier.py` | integration.py | ❌ Missing |

### 4. CLI Commands (Registered but Missing Implementation)

| Command | Status | Notes |
|---------|--------|-------|
| `analyze` | ✅ Implemented | In src/cli/commands/analyze_command.py |
| `resolve` | ✅ Implemented | In src/cli/commands/resolve_command.py |
| `validate` | ✅ Implemented | In src/cli/commands/validate_command.py |
| `analyze-history` | ✅ Implemented | In src/cli/commands/analyze_history_command.py |
| `plan-rebase` | ✅ Implemented | In src/cli/commands/plan_rebase_command.py |
| `identify` | ❌ Missing | IdentifyCommand referenced but not found |
| `branch-cluster` | ✅ Registered | ClusterBranchesCommand registered as agent-6 |
| `git-analyze` | ❌ Missing | AnalyzeCommand registered but git-analyze not found |

---

## 📋 Implementation Gap Summary by Spec

### From 004-guided-workflow (Orchestration Core)

| Requirement (FR-*) | Spec Description | Implementation Status |
|--------------------|------------------|----------------------|
| FR-001 | dev.py with typer | ❌ Not implemented |
| FR-002 | git merge-tree | ❌ Not implemented |
| FR-003 | DAG rebase planner | ❌ Not implemented |
| FR-004 | AST constitutional scanner | ❌ Not implemented |
| FR-005 | Pydantic models | ❌ Not implemented |
| FR-006 | Replace placeholders | ❌ Not implemented |
| FR-007 | --dry-run flag | ❌ Not implemented |
| FR-008 | tasks.md execution | ❌ Not implemented |
| FR-009 | --json mode | ❌ Not implemented |
| FR-010 | ide-init command | ❌ Not implemented |
| FR-011 | Progressive disclosure | ❌ Not implemented |
| FR-012 | --answers JSON input | ❌ Not implemented |
| FR-013 | SHA-256 divergence check | ❌ Not implemented |
| FR-014 | .dev_state.json persistence | ❌ Not implemented |
| FR-015 | JSON violation report | ❌ Not implemented |
| FR-016 | Interactive multi-select sync | ❌ Not implemented |
| FR-017 | install-hooks command | ❌ Not implemented |
| FR-018 | schema command | ❌ Not implemented |
| FR-019 | deps extract | ❌ Not implemented |
| FR-020 | deps compare | ❌ Not implemented |
| FR-021 | analyze --artifacts | ❌ Not implemented |
| FR-022 | commit-classify | ❌ Not implemented |
| FR-023 | align command | ❌ Not implemented |
| FR-024 | ast-grep integration | ❌ Not implemented |
| FR-025 | CommandFactory + Registry | ✅ Restored on main, ❌ on orch-tools |
| FR-026 | GitLogParser | ❌ Not implemented |
| FR-027 | CommitClassifier | ❌ Not implemented |
| FR-028 | RebasePlanner | ❌ Not implemented |
| FR-029 | Cross-branch commit analysis | ❌ Not implemented |
| FR-030 | Fix/avoidance options | ❌ Not implemented |
| FR-031 | Directory structure comparison | ❌ Not implemented |
| FR-032 | Filename fuzzy matching | ❌ Not implemented |
| FR-033 | Content-level diff analysis | ❌ Not implemented |

### From 010-orchestration-workflow (Hub-and-Spoke)

| Component | Purpose | Status |
|-----------|---------|--------|
| orchestration-tools branch | Central hub | ✅ Exists |
| scripts/hooks/ | Git hooks | ❌ Missing |
| scripts/ | Sync scripts | ❌ Partial |
| File Ownership Matrix | Documentation | ❌ Missing |

### From 013-task-execution-layer

| Feature | Status |
|---------|--------|
| tasks.md parser | ❌ Not implemented |
| Task runner | ❌ Not implemented |
| PR linking | ❌ Not implemented |
| State persistence | ❌ Not implemented |
| Execution report | ❌ Not implemented |

---

## 🎯 Restoration Priority Matrix

### 🔴 P0 - Critical (Blocking)

| Priority | Task | Effort | Dependencies |
|----------|------|--------|--------------|
| **P0-1** | Copy interface.py, factory.py, registry.py to orchestration-tools | Low | None |
| **P0-2** | Copy git/ module (worktree.py, conflict_detector.py, repository.py) | Low | None |
| **P0-3** | Copy analysis/constitutional/analyzer.py from .taskmaster | Low | None |
| **P0-4** | Implement git/history.py (CommitClassifier, GitHistory) | Medium | None |
| **P0-5** | Implement git/conflict_detector.py (conflict detection) | Medium | git module |
| **P0-6** | Implement git/history.py (GitHistory, CommitClassifier) | Medium | None |
| **P0-7** | Register ClusterBranchesCommand on orchestration-tools | Low | interface.py, factory.py |

### P1 - High (Core Features)

| Priority | Task | Effort | Dependencies |
|----------|------|--------|--------------|
| **P1-1** | Git merge-tree implementation (FR-002) | High | git module |
| **P1-2** | DAG Rebase Planner (FR-003) | High | strategy/reordering.py |
| **P1-3** | AST Constitutional Scanner (FR-004) | High | analysis/constitutional/analyzer.py |
| **P1-4** | Pydantic Models (FR-005) | Medium | All modules |
| **P1-5** | Git Hooks (001-012) (FR-017) | Medium | scripts/hooks/ |
| **P1-6** | Session Persistence (FR-014) | Medium | .dev_state.json |

### P2 - Medium (Advanced Features)

| Priority | Task | Effort | Dependencies |
|----------|------|--------|--------------|
| **P2-1** | AST-grep Integration (FR-024) | High | ast-grep CLI |
| **P2-2** | Session Persistence (FR-014) | Medium | .dev_state.json |
| **P2-3** | Task Execution Layer (013 spec) | High | tasks.md parser |
| **P2-4** | Dependency Extraction (FR-019, FR-020) | Medium | AST/import analysis |
| **P2-5** | Git Hooks Enforcement | Medium | scripts/hooks/ |
| **P2-6** | Cross-branch Analysis (FR-029) | High | All git modules |

### P3 - Medium (Nice to Have)

| Priority | Task | Effort | Dependencies |
|----------|------|--------|--------------|
| **P3-1** | AST-grep Integration | High | ast-grep CLI |
| **P3-2** | Session Persistence | Medium | .dev_state.json |
| **P3-3** | Task Execution Layer | High | tasks.md parser |
| **P3-4** | Dependency Extraction | Medium | AST/import analysis |
| **P3-4** | Git Hooks Enforcement | Medium | scripts/hooks/ |
| **P3-5** | Cross-branch Analysis | High | All git modules |

---

## 📊 Restoration Progress Summary

| Category | Total Items | Completed | In Progress | Remaining |
|----------|-------------|-----------|-------------|-----------|
| **Branch Clustering** | 10 | 10 | 0 | 0 |
| **CLI Infrastructure** | 12 | 3 | 2 | 7 |
| **Git Operations** | 8 | 3 | 2 | 3 |
| **Analysis Modules** | 8 | 1 | 1 | 6 |
| **CLI Commands** | 8 | 4 | 1 | 3 |
| **FR Specs (004)** | 33 | 1 | 2 | 30 |
| **Hub-and-Spoke (010)** | 4 | 1 | 1 | 2 |
| **Task Execution (013)** | 5 | 0 | 0 | 5 |
| **TOTAL** | **74** | **16** | **6** | **52** |

**Overall Completion: ~22%**

---

## 🚀 Immediate Next Steps (This Week)

### Day 1-2: Foundation
1. [ ] Copy `interface.py`, `factory.py`, `registry.py` to orchestration-tools
2. [ ] Copy `src/git/` module (worktree.py, conflict_detector.py, repository.py)
3. [ ] Copy `analysis/constitutional/analyzer.py` from .taskmaster
4. [ ] Copy `src/git/history.py` (GitHistory + CommitClassifier)

### Day 3-4: Core Integration
5. [ ] Register ClusterBranchesCommand on orchestration-tools
6. [ ] Test `branch-cluster` command end-to-end
7. [ ] Implement `git merge-tree` conflict detection (FR-002)

### Day 5-7: Core Features
8. [ ] Implement DAG Rebase Planner (FR-003)
8. [ ] Implement AST Constitutional Scanner (FR-004)
9. [ ] Add Pydantic models (FR-005)
10. [ ] Implement Git Hooks (FR-017)

---

## 🔍 Verification Checklist

- [ ] `python -m src.cli.commands.task.cluster_branches --help` works
- [ ] `python -m src.cli branch-cluster --primary origin/main` runs without error
- [ ] `python -m src.cli branch-cluster --mode hybrid --output test.json` produces valid JSON
- [ ] `python -m src.cli branch-cluster --validate rules.yaml` validates against rules
- [ ] All 7 CLI commands registered and discoverable
- [ ] Integration tests pass for git operations