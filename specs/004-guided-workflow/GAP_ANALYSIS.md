# Gap Analysis: 004-guided-workflow Spec vs. Existing Codebase

**Date:** 2026-03-15  
**Branch:** `004-guided-workflow`  
**Spec:** `specs/004-guided-workflow/spec.md` (FR-001 → FR-035, US1–US12)  
**Analyst:** Amp (automated)

---

## Table of Contents

1. [Conflict Analysis: Spec vs. Constraints](#1-conflict-analysis-spec-vs-constraints)
2. [Project Organisation Audit](#2-project-organisation-audit)
3. [Baseline Implementation Inventory](#3-baseline-implementation-inventory)
4. [Scope Evaluation](#4-scope-evaluation)
5. [Pitfall Prediction](#5-pitfall-prediction)
6. [Missed Features Analysis](#6-missed-features-analysis)
7. [Branch Categorisation Deep Dive](#7-branch-categorisation-deep-dive)
8. [Implementability Assessment (FR Summary Table)](#8-implementability-assessment)

---

## 1. Conflict Analysis: Spec vs. Constraints

### Sources Compared

| Document | Location | Role |
|----------|----------|------|
| `spec.md` | `specs/004-guided-workflow/spec.md` | Desired outcomes (FR-001–FR-035) |
| `constitution.md` | `.specify/memory/constitution.md` | Architectural governance |
| `PROJECT_IDENTITY.md` | `.taskmaster/PROJECT_IDENTITY.md` | Scope identity for .taskmaster |
| `AGENTS.md` | Project root | Multi-agent workspace rules |

### Contradictions Found

#### ⚠️ CRITICAL: Identity Collision — `dev.py` vs. PROJECT_IDENTITY.md

**Conflict:** PROJECT_IDENTITY.md states this project is "**Branch Alignment Tooling (NOT EmailIntelligence)**" and says alignment tasks (001–028) must be "focused on: git, branches, merges, rebases, clustering, validation." The spec's `dev.py` builds exactly this kind of tooling — but lives on the `004-guided-workflow` branch of the **EmailIntelligence** repository, not inside `.taskmaster/`.

**Resolution:** PROJECT_IDENTITY.md constrains `.taskmaster/tasks/` only — it defines the scope of taskmaster tasks 001–028. The 004-guided-workflow spec creates a **separate** tool (`dev.py`) at the repo root of the EmailIntelligence repository. These are compatible: `dev.py` IS a branch alignment tool, it just lives in the parent repo. However, care must be taken:
- `dev.py` MUST NOT be treated as a taskmaster task deliverable
- taskmaster tasks 001–028 describe the *problem domain*; dev.py is the *solution* on a different branch
- No cross-pollination of dev.py code INTO `.taskmaster/tasks/` files

**Risk Level:** MEDIUM — agents may confuse which scope governs `dev.py`

#### ⚠️ MODERATE: `dev.py` Uses `argparse` — Spec Requires `typer` (FR-001)

**Conflict:** The existing `dev.py` (38 lines) uses `argparse`. FR-001 mandates `typer`. Additionally, `src/cli/main.py` (309 lines) uses `argparse` as a separate "git-verifier" CLI.

**Resolution:** `dev.py` must be rewritten from `argparse` to `typer`. The existing `src/cli/main.py` is a different tool ("git-verifier") and should remain separate. This is a clean break.

**Risk Level:** LOW — straightforward framework swap

#### ⚠️ MODERATE: Hook Installation Strategy Conflicts with Existing Hooks

**Conflict:** FR-017 says `dev.py install-hooks` should "rename existing hooks to `.bak`". But the repo has 3 active hooks (pre-commit: bd sync; post-commit: roborev; post-merge: bd import). The spec's "Backup & Overwrite" approach would break these.

**Resolution:** The spec needs amendment. Instead of overwriting, hooks should be **chained** — the constitutional check should be added as a step within the existing pre-commit hook, or use a hook-manager pattern (e.g., `pre-commit.d/` directory). Alternatively, use the `husky` pattern of calling multiple scripts.

**Risk Level:** HIGH — overwriting hooks will break `bd sync` and `roborev`

#### ⚠️ LOW: Constitution File Ownership Matrix vs. FR-004 AST Scanner

**Conflict:** Constitution Section IX defines `scripts/` as "Orchestration-only" and the AST scanner in FR-004 enforces "no logic in scripts/". But `.taskmaster/scripts/` contains 95+ Python scripts with substantial logic (task parsers, PRD generators, validators). The AST scanner would flag ALL of them.

**Resolution:** The scanner's `scripts/` check must exclude `.taskmaster/scripts/` (which is on a different branch/worktree). The scanner should only target `scripts/` relative to the repo root on the current branch.

**Risk Level:** LOW — path scoping fix

#### ⚠️ LOW: FR-013 References `origin/orchestration-tools` Which May Not Exist

**Conflict:** FR-013 and FR-016 require syncing against `origin/orchestration-tools`. The existence and current state of this branch is assumed but not verified.

**Resolution:** The SyncService already handles this gracefully (returns empty if ref not found). But the spec should document what happens when the canonical branch is missing.

**Risk Level:** LOW

---

## 2. Project Organisation Audit

### Spec Directory Structure

| Expected File | Exists? | Status |
|---------------|---------|--------|
| `specs/004-guided-workflow/spec.md` | ✅ | 305 lines, FR-001–FR-035, US1–US12 |
| `specs/004-guided-workflow/tasks.md` | ✅ | T001–T055, 54/55 checked |
| `specs/004-guided-workflow/plan.md` | ✅ | Implementation plan with phases |
| `specs/004-guided-workflow/research.md` | ✅ | Present |
| `specs/004-guided-workflow/data-model.md` | ✅ | Pydantic schemas |
| `specs/004-guided-workflow/quickstart.md` | ✅ | Dev guide |
| `specs/004-guided-workflow/contracts/` | ✅ | Directory present |
| `specs/004-guided-workflow/checklists/` | ✅ | Directory present |
| `specs/004-guided-workflow/research/` | ✅ | Directory present |

**Verdict:** ✅ Complete — all expected specify artifacts are present.

### Source Code Structure vs. FR Requirements

| Expected Directory | Exists? | Contents | Gap |
|-------------------|---------|----------|-----|
| `dev.py` | ✅ | 38-line argparse stub | ❌ Needs typer rewrite |
| `src/core/git/` | ✅ | plumbing.py, history.py, detector.py, comparison.py | Partially implemented |
| `src/core/analysis/` | ✅ | scanner.py, sync.py | Functional but basic |
| `src/core/resolution/` | ✅ | engine.py (AutoResolver) | Mock logic |
| `src/core/execution/` | ✅ | session.py, executor.py, task_runner.py | Functional |
| `src/core/models/` | ✅ | git.py, history.py, orchestration.py, execution.py | Good Pydantic models |
| `src/core/utils/` | ✅ | answers.py, files.py, logger.py | Present |
| `src/core/templates/` | ✅ | vscode, antigravity, windsurf .j2 files | Complete |
| `src/core/base.py` | ✅ | LogicEngine, Action, ExecutionContext | Complete |
| `src/cli/commands/` | ✅ | 17 files including factory, registry, interface | Rich but unintegrated |
| `src/core/commands/` | ✅ | Unknown (additional) | Possible duplication |

### Missing Model File

The `src/core/analysis/scanner.py` imports from `src.core.models.analysis` (for `Violation`, `ConstitutionalRule`), but `src/core/models/analysis.py` does NOT exist in the `src/core/models/` directory. There is `src/models/analysis.py` (a different module). This is a **broken import** that will fail at runtime.

### Dependency Availability

| Dependency | Required By | In pyproject.toml? | Importable? | Status |
|------------|-------------|---------------------|-------------|--------|
| `typer` | FR-001 | ❌ No | ✅ `click` fixed | ✅ Installed |
| `pydantic` | FR-005 | ✅ Yes (≥2.11.5) | ✅ v2.11.10 | ✅ Installed |
| `rich` | FR-011 | ❌ No | ✅ Installed via typer | ✅ Installed |
| `InquirerPy` | US1/T013 | ❌ No | ❌ Not installed | ❌ Missing |
| `pyastsim` | FR-034 | ❌ No | ✅ v1.2.0 installed | ⚠️ Installed but NOT integrated |
| `ast-grep` (Python API) | FR-024 | ❌ No | ❌ Not installed | ❌ Missing |
| `gkg` | FR-035 | ❌ No | ✅ In PATH at ~/.local/bin/ | ⚠️ Available but NOT integrated |
| `jinja2` | IDE templates | ❌ Not checked | Unknown | Unknown |
| `rank-bm25` | FR-036 | ❌ No | ❌ Not installed | ❌ Missing (proposed) |
| `sentence-transformers` | FR-037 | ❌ No | ❌ Not installed | ❌ Missing (proposed) |

**Critical gap:** 5 of 7 key dependencies are missing from pyproject.toml and not installed.

---

## 3. Baseline Implementation Inventory

### What EXISTS in `src/core/` (the spec's target structure)

| Module | File | Lines | Status | Quality |
|--------|------|-------|--------|---------|
| GitPlumbing | `src/core/git/plumbing.py` | 52 | Functional | `merge_tree` uses `--write-tree` not `--real-merge` (spec says `--real-merge`) |
| ConflictDetector | `src/core/git/detector.py` | 13 | Skeleton | Just wires plumbing → parse |
| DAGBuilder + HistoryService | `src/core/git/history.py` | 95 | Functional | Kahn's algorithm implemented with comments showing self-correction |
| BranchComparator | `src/core/git/comparison.py` | 52 | Functional | Jaccard similarity + unique commits |
| ASTScanner | `src/core/analysis/scanner.py` | 46 | Partial | Hardcoded `scripts/` check, no dynamic rule parsing from constitution.md |
| SyncService | `src/core/analysis/sync.py` | 41 | Functional | SHA-256 hash comparison against remote ref |
| AutoResolver | `src/core/resolution/engine.py` | 24 | Mock | Returns strings, not actual resolution |
| SessionManager | `src/core/execution/session.py` | 28 | Functional | Atomic write via tmp+rename |
| ActionExecutor | `src/core/execution/executor.py` | 37 | Partial | Rollback is a no-op (`pass`) |
| TaskRunner | `src/core/execution/task_runner.py` | 27 | Partial | Basic checkbox toggle, no real execution |
| ConflictModel | `src/core/models/git.py` | 22 | Complete | Pydantic model with enums |
| CommitNode + HistoryPlan | `src/core/models/history.py` | 17 | Complete | Clean Pydantic models |
| Session + SyncReport | `src/core/models/orchestration.py` | 28 | Complete | UUID, workflow types |
| ExecutionPlan | `src/core/models/execution.py` | 8 | Complete | Uses Action from base |
| LogicEngine + Action | `src/core/base.py` | 21 | Complete | ABC + Pydantic |

### What EXISTS in `src/cli/commands/` (the command layer)

17 files present — this is the cherry-picked modular command system from `consolidate/cli-unification`. Key files:

| File | Purpose | Wired to dev.py? |
|------|---------|-------------------|
| `factory.py` | CommandFactory (identical to workspace/ copy) | ❌ No |
| `registry.py` | CommandRegistry (identical to workspace/ copy) | ❌ No |
| `interface.py` | Command ABC | ❌ No |
| `integration.py` | setup_modular_cli() | ❌ No |
| `analyze_command.py` | Analysis command | ❌ No |
| `analyze_history_command.py` | History analysis | ❌ No |
| `plan_rebase_command.py` | Rebase planning | ❌ No |
| `resolve.py` / `resolve_command.py` | Resolution | ❌ No |
| `validate_command.py` | Validation | ❌ No |
| `guide.py` | Interactive guide | ❌ No |
| `schema.py` | JSON schema output | ❌ No |
| `sync.py` | Sync command | ❌ No |
| `compare.py` | Comparison | ❌ No |
| `ide.py` | IDE init | ❌ No |
| `rebase.py` | Rebase | ❌ No |
| `task.py` | Task runner | ❌ No |
| `analyze.py` | Another analysis module | ❌ No |

**Critical finding:** The modular command layer is fully scaffolded but **NONE** of it is wired to `dev.py`. The current `dev.py` is a 38-line argparse stub that prints "Logic implementation in progress."

### What EXISTS in `src/` (legacy/parallel modules, NOT in src/core/)

| Module | Location | Relevance |
|--------|----------|-----------|
| `GitConflictDetector` | `src/git/conflict_detector.py` | Detects conflict markers in files (regex-based, NOT merge-tree) |
| `ConflictAnalyzer` | `src/analysis/conflict_analyzer.py` | Analyzes conflict severity |
| `ConstitutionalAnalyzer` | `src/analysis/constitutional/analyzer.py` | Constitution compliance |
| `AutoResolver` | `src/resolution/auto_resolver.py` | Conflict resolution logic |
| `SemanticMerger` | `src/resolution/semantic_merger.py` | Semantic merge |
| `StrategyGenerator` | `src/strategy/generator.py` | Generates resolution strategies |
| `RiskAssessor` | `src/strategy/risk_assessor.py` | Risk assessment |
| `RebasePlanner` | `src/strategy/reordering.py` | Priority-based rebase (identical to workspace/) |
| `MultiPhaseGenerator` | `src/strategy/multi_phase_generator.py` | Multi-phase strategy |
| `Validator` | `src/validation/validator.py` | Post-resolution validation |
| `AnalysisService` | `src/services/analysis_service.py` | Git history analysis service |
| `RebaseAnalyzer` | `src/services/rebase_analyzer.py` | Rebase analysis (mock data) |
| `RebaseDetector` | `src/services/rebase_detector.py` | Detects rebased branches |
| `MergeVerifier` | `src/services/merge_verifier.py` | Merge integrity verification |
| `git-verifier CLI` | `src/cli/main.py` | 309-line argparse CLI (separate tool) |

**Key insight:** There are TWO parallel module trees:
1. `src/core/` — Spec-compliant, Pydantic-first, clean architecture (the T001–T054 deliverables)
2. `src/` (top-level) — Legacy modules from emailintelligence_cli.py, richer but not spec-aligned

### What EXISTS in `workspace/` (cherry-picked reference implementations)

| File | Source Branch | Lines | In src/cli/commands/ too? |
|------|--------------|-------|---------------------------|
| `cli_architecture/factory.py` | consolidate/cli-unification | 108 | ✅ Identical copy |
| `cli_architecture/registry.py` | consolidate/cli-unification | 158 | ✅ Identical copy |
| `cli_architecture/interface.py` | consolidate/cli-unification | 88 | ✅ Identical copy |
| `git_analysis/history.py` | feat-emailintelligence-cli-v2.0 | 77 | ❌ Different from src/core/git/history.py |
| `git_analysis/reordering.py` | feat-emailintelligence-cli-v2.0 | 65 | ❌ Different from src/strategy/reordering.py |

**Duplication alert:** `workspace/cli_architecture/` is byte-identical to `src/cli/commands/{factory,registry,interface}.py`. The workspace copies are redundant reference copies — the real code is already in `src/cli/commands/`.

---

## 4. Scope Evaluation

### FRs That Are Too Large for a Single `specify implement` Step

| FR | Issue | Recommendation |
|----|-------|----------------|
| FR-023 | `dev.py align` is a composite of FR-020 (deps compare), FR-022 (commit classify), FR-029 (cross-branch), FR-031–33 (structural analysis), plus risk scoring and recommendations. | Split into sub-FRs; implement individual analyzers first, then compose. |
| FR-035 | `gkg` integration requires external tool (git knowledge graph), parquet output format, and dependency graph generation. `gkg` is not in pyproject.toml and may not be a stable library. | Defer or mark as optional extension. |
| FR-034 | `pyastsim` for AST structural similarity requires installing and integrating a relatively niche library. | Defer to a later phase — not core functionality. |
| FR-029 | Cross-branch commit analysis with deduplication across N branches is algorithmically non-trivial. | Implement for 2-branch case first; multi-branch is a stretch goal. |

### FRs That Are Underspecified (NOW ADDRESSED)

| FR | Missing Detail | Now Covered By |
|----|----------------|----------------|
| FR-004 | How to "dynamically parse rules from constitution.md"? | **FR-038** - Dynamic rule parsing from constitution.md |
| FR-008 | What does "execute tasks.md" mean exactly? | **FR-040** - Task execution engine |
| FR-010 | IDE template format is defined but what data populates them? | **FR-041** - IDE task file generation |
| FR-024 | ast-grep integration interface undefined | **FR-039** - ast-grep CLI subprocess integration |
| FR-030 | Fix options UX undefined | **FR-042** - Interactive resolution UX |

### FRs That Depend on Unbuilt Infrastructure

| FR | Dependency | Status |
|----|------------|--------|
| FR-016 | Interactive multi-select requires `InquirerPy` | ❌ Not installed |
| FR-015 | JSON violation report requires `src.core.models.analysis.Violation` | ❌ Module missing |
| FR-024 | ast-grep Python API | ❌ Not installed |
| FR-034 | pyastsim library | ❌ Not installed |
| FR-035 | gkg tool | ❌ Not installed, possibly doesn't exist as pip package |

---

## 5. Pitfall Prediction

Based on the contamination history (12 incidents, 5 root cause types) and the 5-CLI-version problem:

### Predicted Failure Mode 1: Module Import Spaghetti
**Probability:** HIGH  
**Pattern:** The codebase has TWO parallel module trees (`src/core/` and `src/`). `emailintelligence_cli.py` imports from `src/` (legacy). `dev.py` should import from `src/core/` (spec). Agents will confuse these, importing `src.resolution.auto_resolver.AutoResolver` (legacy) instead of `src.core.resolution.engine.AutoResolver` (spec).  
**Mitigation:** Add explicit import path documentation. Consider renaming `src/core/` to something more distinct, or add `__init__.py` guards.

### Predicted Failure Mode 2: Broken Import — `src.core.models.analysis`
**Probability:** CERTAIN (100%)  
**Evidence:** `src/core/analysis/scanner.py` line 4 imports `from src.core.models.analysis import Violation, ConstitutionalRule` — but `src/core/models/analysis.py` does not exist. This module was never created despite T035–T037 being marked done.  
**Mitigation:** Create `src/core/models/analysis.py` with `Violation` and `ConstitutionalRule` Pydantic models before any scanner work.

### Predicted Failure Mode 3: CLI Framework Mismatch
**Probability:** HIGH  
**Pattern:** `workspace/cli_architecture/` uses `argparse` + custom Command ABC. FR-001 requires `typer`. The CommandFactory/Registry pattern is argparse-based (takes `parser.Namespace`). Adapting this to typer requires rewriting the `add_arguments()` and `execute(args: Namespace)` signatures.  
**Mitigation:** Decide: use typer natively (discard factory/registry) OR keep factory/registry but adapt the interface to typer's callback pattern.

### Predicted Failure Mode 4: Hook Destruction
**Probability:** HIGH  
**Evidence:** FR-017 says "rename existing hooks to .bak and install new ones." Existing hooks (`bd sync`, `roborev`, `bd import`) are actively used. Overwriting them breaks the workflow.  
**Mitigation:** Amend FR-017 to chain hooks instead of replacing them.

### Predicted Failure Mode 5: Worktree Contamination (Repeat of Nov 2025)
**Probability:** MEDIUM  
**Pattern:** `.taskmaster/` is a worktree on the `taskmaster` branch. Agents writing to `src/core/` on `004-guided-workflow` might accidentally modify `.taskmaster/src/` (which has its own `src/` tree on a different branch).  
**Mitigation:** The `.gitignore` protection is in place. Add pre-commit validation to reject changes touching `.taskmaster/` from the `004-guided-workflow` branch.

### Predicted Failure Mode 6: "Done" Tasks That Aren't Done
**Probability:** HIGH  
**Evidence:** T001–T054 are all marked ✅ done, but:
- `dev.py` is still a 38-line argparse stub (T001 says "Initialize dev.py with typer")
- `src/core/models/analysis.py` doesn't exist (T035 says "Define ASTScanner and ConstitutionalRule")
- `ActionExecutor.rollback()` is `pass` (T047 says "Implement ActionExecutor subprocess runner")
- `AutoResolver.resolve()` returns mock strings (T048 says "Implement AutoResolver strategy logic")
- `TaskRunner.run()` just toggles checkboxes (T050 says "Implement dev.py task run")

**These tasks were marked done but contain stubs/mocks.** This is the most significant gap.

---

## 6. Missed Features Analysis

Capabilities in the codebase NOT mentioned in the spec:

### High Value — Should Be Added

| Capability | Location | Benefit |
|------------|----------|---------|
| **ConflictAnalyzer** (severity analysis) | `src/analysis/conflict_analyzer.py` | Adds severity grading to FR-002's conflict detection |
| **RiskAssessor** (quantified risk scoring) | `src/strategy/risk_assessor.py` | Directly supports FR-023's "risk_score" field |
| **StrategyGenerator** (multi-phase resolution) | `src/strategy/generator.py`, `multi_phase_generator.py` | FR-030's fix options need strategy generation |
| **MergeVerifier** (post-merge integrity) | `src/services/merge_verifier.py` | Could be wired as post-rebase verification |
| **SemanticMerger** (context-aware merging) | `src/resolution/semantic_merger.py` | Upgrades FR-048's AutoResolver from mock to real |
| **RebaseDetector** (detects rebased branches) | `src/services/rebase_detector.py` | Useful for FR-023's alignment report |
| **ComprehensiveValidator** | `src/validation/comprehensive_validator.py` | 7 validator modules exist; only 1 referenced in spec |
| **AnalysisService** (git-verifier) | `src/services/analysis_service.py` | Full commit narrative generation with LLM integration |

### Medium Value — Consider for Future

| Capability | Location | Benefit |
|------------|----------|---------|
| `src/context_control/` (12 modules) | Only in cli-consolidation branch | Agent context isolation — relevant to Extension A |
| `src/core/audit_logger.py` | Present on branch | Audit trail — relevant to constitution |
| `src/core/performance_monitor.py` | Present on branch | SC-002 performance benchmarking |
| `scripts/analyze_git_history.py` | `.taskmaster/scripts/` | Commit categorization that FR-022 reinvents |
| `scripts/partial_cherry_pick.py` | `.taskmaster/scripts/` | Selective cherry-pick that FR-030 needs |

### Low Value — Informational

| Capability | Location | Note |
|------------|----------|------|
| `src/core/caching.py`, `enhanced_caching.py` | Present | Could help SC-002 performance |
| `src/core/mfa.py`, `auth.py` | Present | Not relevant to dev.py scope |
| `src/backend/` | Present | Full web backend — out of scope |

---

## 7. Branch Categorisation Deep Dive

### What EXISTS for Branch Analysis

**Layer 1: Low-level Git Operations**
- `src/core/git/plumbing.py` → `merge_tree()`, `cat_file()` — plumbing wrappers
- `src/core/git/comparison.py` → `BranchComparator` with Jaccard similarity and unique commit listing
- `src/core/git/detector.py` → `ConflictDetector` — wires merge-tree to conflict models

**Layer 2: Conflict Detection & Analysis**
- `src/git/conflict_detector.py` → `GitConflictDetector` — regex-based conflict marker detection (scans files for `<<<<<<<`)
- `src/analysis/conflict_analyzer.py` → `ConflictAnalyzer` — severity analysis of detected conflicts
- `src/analysis/constitutional/analyzer.py` → `ConstitutionalAnalyzer` — constitution compliance checking

**Layer 3: History Analysis**
- `src/core/git/history.py` → `DAGBuilder` + `HistoryService` — Kahn's topological sort
- `workspace/git_analysis/history.py` → `GitHistory` — async git log parser with commit categorization
- `src/services/analysis_service.py` → `AnalysisService` — full narrative generation per commit
- `src/services/rebase_analyzer.py` → `RebaseAnalyzer` — mock/placeholder

**Layer 4: Strategy & Resolution**
- `src/strategy/reordering.py` / `workspace/git_analysis/reordering.py` → `RebasePlanner` — priority-based grouping
- `src/strategy/generator.py` → `StrategyGenerator` — resolution strategy
- `src/strategy/risk_assessor.py` → `RiskAssessor` — risk quantification
- `src/resolution/auto_resolver.py` → `AutoResolver` (legacy, richer than src/core/ version)
- `src/resolution/semantic_merger.py` → `SemanticMerger`

### What's PLANNED in the Spec

| FR | Capability | Maps To |
|----|-----------|---------|
| FR-022 | `dev.py commit-classify` — conventional commits + risk | Partially exists in workspace/git_analysis/history.py (has category + risk_level fields) |
| FR-023 | `dev.py align` — alignment report | No single implementation; requires composing comparison + classification + risk |
| FR-026 | GitLogParser | workspace/git_analysis/history.py has this |
| FR-027 | CommitClassifier | NOT implemented anywhere — classification logic is missing |
| FR-029 | Cross-branch shared commit detection | NOT implemented — BranchComparator has unique commits but not shared problematic commit detection |
| FR-031 | Directory structure comparison | NOT implemented |
| FR-032 | Filename similarity (fuzzy matching) | NOT implemented |
| FR-033 | Content-level diff analysis | BranchComparator has commit-level, not file-content-level |

### What's MISSING

1. **CommitClassifier** — The spec cherry-picks this from `feat-emailintelligence-cli-v2.0` but it doesn't exist in any checked-out branch. The `workspace/git_analysis/history.py` has `category` and `risk_level` fields on the `Commit` model but NO classification logic to populate them.

2. **Cross-branch analysis for shared problematic commits (FR-029)** — `BranchComparator` gives unique commits per branch but doesn't identify commits that appear in multiple branches or that have similar change patterns.

3. **Directory structure comparison (FR-031)** — No implementation exists. Would need tree-walking + structural diff.

4. **Fuzzy filename matching (FR-032)** — No implementation exists. Would need Levenshtein/Jaro-Winkler.

5. **Full alignment report (FR-023)** — This is a composite deliverable requiring FR-020 + FR-022 + FR-029 + FR-031–33 + risk scoring. None of the individual pieces are production-ready.

### .taskmaster Task 007: Feature Branch ID & Categorization

Task 007 in `.taskmaster/tasks/` focuses on branch categorization at the BRANCH level (classifying branches into clusters). This is complementary to but different from the spec's FR-022 which operates at the COMMIT level. Both are needed for a complete picture:
- **Branch-level:** "Is this a feature branch, maintenance branch, or dead branch?" → Task 007
- **Commit-level:** "Is this commit a feat, fix, refactor, or regression?" → FR-022

The spec adequately covers commit-level but doesn't explicitly address branch-level categorization. Consider adding this.

---

## 8. Implementability Assessment

| FR | Description | Rating | Evidence |
|----|-------------|--------|----------|
| **FR-001** | Unified CLI via typer | **(c) Needs new code, straightforward** | dev.py exists but uses argparse. Typer rewrite is clean. Missing dep: `typer`, `click`. |
| **FR-002** | In-memory conflict detection via merge-tree | **(b) Partially implemented** | `plumbing.py` has `merge_tree()` but uses `--write-tree` not `--real-merge`. Parser is basic (regex for CONFLICT lines only, no OID extraction). |
| **FR-003** | HistoryService with DAG + topo sort | **(b) Partially implemented** | `history.py` has Kahn's algorithm. Needs commit classification integration and priority sorting. |
| **FR-004** | ASTScanner from constitution.md | **(d) Needs new code, complex** | Scanner exists but rules are hardcoded. Dynamic rule parsing from constitution.md prose requires NLP or structured rule format. Constitution.md has no machine-parseable rules section. |
| **FR-005** | Pydantic models for all data exchange | **(a) Already implemented** | Models exist in `src/core/models/` for git, history, orchestration, execution. Missing: `analysis.py` (Violation, ConstitutionalRule). |
| **FR-006** | Replace placeholders in src/cli/commands/ | **(d) Needs new code, complex** | 17 command files exist but are unconnected. Need to wire each to src/core/ logic engines AND to typer. |
| **FR-007** | --dry-run flag | **(b) Partially implemented** | ActionExecutor has dry_run support. dev.py stub has no global options. |
| **FR-008** | Parse & execute tasks.md | **(b) Partially implemented** | TaskRunner exists but is checkbox-toggle only, no real task execution. |
| **FR-009** | --json headless mode | **(c) Needs new code, straightforward** | No implementation. Add typer callback + JSON output serializer. |
| **FR-010** | IDE init command | **(b) Partially implemented** | Jinja2 templates exist for 3 IDEs. Command scaffolded in `src/cli/commands/ide.py`. Not wired. |
| **FR-011** | Token-Saver mode | **(c) Needs new code, straightforward** | logger.py exists in utils. Need to add rich suppression logic. |
| **FR-012** | --answers JSON pre-answering | **(b) Partially implemented** | `src/core/utils/answers.py` exists. Not wired to dev.py. |
| **FR-013** | SHA-256 sync with orchestration-tools | **(a) Already implemented** | SyncService in `src/core/analysis/sync.py` is functional. |
| **FR-014** | Atomic session persistence | **(a) Already implemented** | SessionManager in `src/core/execution/session.py` uses tmp+rename. |
| **FR-015** | JSON violation report | **(e) Blocked** | Requires `src/core/models/analysis.py` which doesn't exist. |
| **FR-016** | Interactive multi-select sync | **(e) Blocked** | Requires `InquirerPy` (not installed). |
| **FR-017** | Hook installation | **(d) Needs new code, complex** | Must chain with existing hooks (bd sync, roborev, bd import). Simple overwrite will break things. |
| **FR-018** | Schema output command | **(c) Needs new code, straightforward** | Pydantic models have `.model_json_schema()`. Just needs CLI wiring. |
| **FR-019** | Dependency graph extraction (AST) | **(d) Needs new code, complex** | No implementation. Requires walking Python AST for imports + function calls. |
| **FR-020** | Dependency comparison between branches | **(d) Needs new code, complex** | Requires FR-019 first, then diff logic. |
| **FR-021** | Merge artifact detection | **(b) Partially implemented** | `src/git/conflict_detector.py` detects conflict markers. Missing: broken imports, duplicate defs, orphaned exports. |
| **FR-022** | Commit classification | **(c) Needs new code, straightforward** | Commit model has fields. Classification logic (conventional commit parsing + heuristics) is ~100 lines. |
| **FR-023** | Alignment report | **(d) Needs new code, complex** | Composite of FR-020, FR-022, FR-029, FR-031–33, plus risk scoring. |
| **FR-024** | ast-grep integration | **(e) Blocked** | `ast-grep-py` not installed, no pyproject.toml entry. |
| **FR-025** | CommandFactory + Registry | **(a) Already implemented** | Identical copies in workspace/ and src/cli/commands/. |
| **FR-026** | GitLogParser | **(b) Partially implemented** | workspace/git_analysis/history.py has it. Uses async. Needs adaptation to src/core/ sync style. |
| **FR-027** | CommitClassifier | **(c) Needs new code, straightforward** | No implementation exists. Conventional commit regex + keyword detection is ~150 lines. |
| **FR-028** | RebasePlanner with topo sort | **(b) Partially implemented** | workspace/git_analysis/reordering.py has priority grouping. src/core/git/history.py has topo sort. Need to merge both. |
| **FR-029** | Cross-branch commit analysis | **(d) Needs new code, complex** | BranchComparator gives unique commits but not shared problematic detection. |
| **FR-030** | Fix/avoidance options | **(c) Needs new code, straightforward** | UX undefined but code is ~200 lines of option mapping. |
| **FR-031** | Directory structure comparison | **(c) Needs new code, straightforward** | Tree walk + set comparison. ~100 lines. |
| **FR-032** | Filename fuzzy matching | **(c) Needs new code, straightforward** | difflib.SequenceMatcher or Levenshtein. ~80 lines. |
| **FR-033** | Content-level diff analysis | **(c) Needs new code, straightforward** | git diff-tree + parsing. ~120 lines. |
| **FR-034** | pyastsim AST similarity | **(c) Needs new code, straightforward** | Library installed (v1.2.0). Integration ~50 lines. |
| **FR-035** | gkg integration | **(c) Needs new code, straightforward** | CLI available in PATH. Integration ~80 lines. |
| **FR-036** | BM25 text similarity | **(c) Needs new code, straightforward** | Requires `rank-bm25` package. ~60 lines. |
| **FR-037** | Sentence embedding semantic search | **(d) Complex new code** | Requires `sentence-transformers`. Heavy dependency, defer to Phase 2. |

### Summary Counts

| Rating | Count | Percentage |
|--------|-------|------------|
| **(a) Already implemented** | 4 | 10% |
| **(b) Partially implemented** | 10 | 26% |
| **(c) Straightforward new code** | 12 | 31% |
| **(d) Complex new code** | 8 | 21% |
| **(e) Blocked by missing infra** | 3 | 8% |
| **(N/A) Future phase** | 2 | 5% |

---

## 9. Semantic Search Capabilities Gap (BM25/2.5)

### Current State

| Capability | Specified | Installed | Integrated |
|------------|-----------|-----------|------------|
| **BM25 / BM 2.5** | ❌ No | ❌ No | ❌ No |

---

## 10. Constitution Update (2026-03-15)

### Section XII: Agentic-First Tool Design

The constitution has been updated with Section XII - Agentic-First Tool Design (v1.4.0). This affects all FRs in this spec:

**New Requirements per Constitution Section XII:**

1. Every command MUST support `--json` output
2. Exit codes: 0=success, 1=error, 2=usage
3. Structured errors: `{code, message, details, hint}`
4. Commands must be idempotent
5. `--help` must be agent-usable

### Section XIII: Constitution Governance (v1.5.0)

**New Principles:**

1. **Constitution First Principle**: Commit Constitution BEFORE spec work
2. **The Cascade**: Constitution → Research → Spec → Plan → Tasks → Implementation
3. **Quality Rules**:
   - Use accurate terminology (only mention patterns your project uses)
   - Avoid external standards references
   - Avoid vague rules (be specific)
4. **Constitution Completeness Test**: Checklist before starting spec work

**Impact on FRs:**
- All existing FRs need JSON output compliance verification
- New FRs (FR-038 to FR-042) already include agentic requirements
- dev.py commands must be updated to include JSON output
| **pyastsim** (FR-034) | ✅ Yes | ✅ Yes (v1.2.0) | ❌ No |
| **gkg** (FR-035) | ✅ Yes | ✅ Yes (in PATH) | ❌ No |
| **Sentence embeddings** | ❌ No | ❌ No | ❌ No |
| **Vector similarity** | ❌ No | ❌ No | ❌ No |

### Analysis

**BM25/2.5 is NOT specified** in FR-001 to FR-035. The spec currently relies on:
- **FR-032**: Fuzzy string matching (difflib) for filename similarity
- **FR-034**: pyastsim for AST structural similarity (Python only)
- **FR-035**: gkg for code structure analysis

### Gap

For true semantic/BM25 search capabilities in branch comparison:
1. **FR-032** (fuzzy matching) is text-based, not semantic
2. **FR-034** requires pyastsim integration (not done)
3. **FR-035** requires gkg integration (not done)

### Recommendation

Add new functional requirement for semantic search:

- **FR-036**: System MUST implement BM25-based similarity scoring for text content comparison between branches (optional, can be deferred to Phase 2)
- **FR-037**: System MUST provide sentence embedding-based semantic search for code comment/docstring analysis between branches (optional, can be deferred to Phase 2)

### Priority Actions Before `specify implement`

1. **Fix broken import:** Create `src/core/models/analysis.py` with `Violation` and `ConstitutionalRule` models
2. **Add missing dependencies to pyproject.toml:** `typer[all]`, `click`, `rich`, `InquirerPy`, `jinja2`, `rank-bm25`
3. **Rewrite dev.py from argparse to typer** (FR-001) - ✅ DONE
4. **Wire src/cli/commands/ to dev.py** via the CommandFactory/Registry or via typer directly
5. **Fix plumbing.py:** Change `--write-tree` to `--real-merge` per spec
6. **Amend FR-017:** Change hook strategy from overwrite to chaining
7. **Implement FR-034 (pyastsim):** Library installed, integrate for AST similarity
8. **Implement FR-035 (gkg):** CLI available, integrate for code structure analysis
9. **Add FR-036 (BM25):** Install `rank-bm25` for text similarity
10. **Defer FR-037:** Sentence embeddings require heavy dependencies, move to Phase 2
11. **Decide FR-024:** ast-grep — use ast-grep CLI subprocess or drop in favor of Python `ast` module (already used in scanner.py)
12. **Acknowledge T001–T054 quality debt:** Many "done" tasks contain stubs/mocks that need real implementation

---

*Generated by comprehensive gap analysis across spec.md, constitution.md, PROJECT_IDENTITY.md, and full codebase inspection.*
