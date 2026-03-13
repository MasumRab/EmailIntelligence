# CLI Tools Inventory — EmailIntelligence Repository

**Date:** 2026-03-13
**Scope:** All CLI tools, entry points, and script utilities across branches and worktrees
**Repo:** https://github.com/MasumRab/EmailIntelligence.git
**Working Branch:** `taskmaster`

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Primary CLI Tools](#primary-cli-tools)
3. [emailintelligence_cli.py — Version Matrix](#emailintelligence_clipy--version-matrix)
4. [Remote-Only CLI Branches](#remote-only-cli-branches)
5. [cli-consolidation Worktree — Divergence Analysis](#cli-consolidation-worktree--divergence-analysis)
6. [Supporting Scripts & Utilities](#supporting-scripts--utilities)
7. [src/ Module Structure Comparison](#src-module-structure-comparison)
8. [Relevance to Branch Alignment Workflow](#relevance-to-branch-alignment-workflow)
9. [Recommendations](#recommendations)

---

## Executive Summary

The EmailIntelligence repo contains **3 primary CLI tools** and **100+ supporting scripts** spread across multiple branches and worktrees. The most significant finding is that `emailintelligence_cli.py` exists in **5 different versions** across 4 branches plus the current worktree — ranging from 1,698 to 2,116 lines — with meaningful architectural differences between them. The CLI's conflict detection and resolution capabilities are directly relevant to the branch alignment workflow (Tasks 009, 010, 014).

| CLI Tool | Location | Lines | Purpose |
|----------|----------|-------|---------|
| `emailintelligence_cli.py` | Multiple branches/worktrees | 1,698–2,116 | AI-powered git conflict resolution |
| `taskmaster_cli.py` | `.taskmaster/` | 300 | Task management (markdown → JSON) |
| `src/main.py` | `.taskmaster/src/` | ~170 | FastAPI service wrapping the CLI |

---

## Primary CLI Tools

### 1. `emailintelligence_cli.py` — Conflict Resolution CLI

**Class:** `EmailIntelligenceCLI`
**Lines:** 1,745 (taskmaster branch)
**Language:** Python 3.8+
**Dependencies:** PyYAML (optional), src/ module tree

#### CLI Subcommands

| Command | Description |
|---------|-------------|
| `setup-resolution` | Create git worktree-based resolution workspace for a PR |
| `analyze-constitutional` | Analyze conflicts against constitution/spec documents |
| `develop-spec-kit-strategy` | Generate conflict resolution strategy using spec-kit approach |
| `align-content` | Execute content alignment across worktrees |
| `validate-resolution` | Validate completed resolution for correctness |
| `auto-resolve` | Automatically resolve conflicts using constitutional engine |
| `version` | Show version information |

#### Key Methods (50+)

| Category | Methods |
|----------|---------|
| **Setup** | `setup_resolution()`, `_dry_run_setup()`, `_ensure_directories()` |
| **Detection** | `_detect_conflicts()`, `_detect_conflicts_interface_based()` |
| **Analysis** | `analyze_constitutional()`, `_analyze_constitutional_async()`, `_perform_constitutional_analysis()`, `_assess_constitutional_compliance()` |
| **Strategy** | `develop_spec_kit_strategy()`, `_generate_spec_kit_strategy()`, `_interactive_strategy_development()` |
| **Resolution** | `align_content()`, `auto_resolve_conflicts()`, `_execute_phase()`, `_execute_phase_interactive()` |
| **Validation** | `validate_resolution()`, `_perform_validation()`, `_validate_constitutional_compliance()` |
| **Reporting** | `_generate_analysis_report()`, `_generate_strategy_report()`, `_display_*()` methods |

#### Module Dependencies (src/)

```
emailintelligence_cli.py
├── src.core.config          → ConfigurationManager
├── src.core.security        → SecurityValidator
├── src.core.git_operations  → GitOperations
├── src.core.conflict_models → Conflict, ConflictBlock, ConflictTypeExtended, RiskLevel
├── src.resolution           → ConstitutionalEngine
├── src.resolution.auto_resolver    → AutoResolver
├── src.resolution.semantic_merger  → SemanticMerger
├── src.git.conflict_detector       → GitConflictDetector
├── src.analysis.conflict_analyzer  → ConflictAnalyzer
├── src.analysis.constitutional.analyzer → ConstitutionalAnalyzer
├── src.strategy.generator   → StrategyGenerator
├── src.strategy.risk_assessor → RiskAssessor
└── src.validation.validator → Validator
```

---

### 2. `taskmaster_cli.py` — Task Management CLI

**Lines:** 300
**Purpose:** Parse task markdown files into `tasks.json` for Task Master AI consumption

#### Interface

```bash
python taskmaster_cli.py parse-prd --input tasks/ [--output tasks.json] [--dry-run]
```

| Argument | Description |
|----------|-------------|
| `--input` | Input directory containing task markdown files or PRD file |
| `--output` | Output path for tasks.json (default: `.taskmaster/tasks/tasks.json`) |
| `--dry-run` | Preview without writing |
| `--verbose` | Detailed output |

#### Capabilities
- Extracts task ID, title, status, priority, effort, complexity from markdown headers
- Parses dependencies from `**Dependencies:**` field
- Extracts Overview/Purpose section as description
- Handles parent/subtask hierarchy (`task_NNN.md` → `task_NNN.M.md`)

---

### 3. `src/main.py` — FastAPI Service Wrapper

**Lines:** ~170
**Purpose:** Wraps `emailintelligence_cli.py` as a FastAPI HTTP service

#### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check with CLI availability status |
| GET | `/cli/status` | CLI capabilities and status |

#### Architecture
- Factory pattern: `create_app()` function
- `CLIMiddleware` for request tracking
- Imports `EmailIntelligenceCLI` with graceful fallback if unavailable
- CORS enabled, request ID tracking, timing headers

---

## emailintelligence_cli.py — Version Matrix

**Critical Finding:** The CLI exists in **5 distinct versions** across branches. The copies on `taskmaster` and `consolidate/cli-unification` are **byte-identical** (1,745 lines), but other branches have different versions.

| Branch | Lines | Key Differences |
|--------|-------|----------------|
| `taskmaster` (current) | 1,745 | Has `ConfigurationManager`, `SecurityValidator`, `GitOperations` imports. No CLI command system. |
| `consolidate/cli-unification` (worktree) | 1,745 | **Identical** to taskmaster copy |
| `feat-emailintelligence-cli-v2.0` | **2,116** | **Largest version.** Has dual-mode parser (legacy + modular). Imports `src.cli.commands.integration` with `setup_modular_cli`, `handle_modular_command`. |
| `feat/emailintelligence-cli-v2.0-with-pr-framework` | 1,754 | Lacks `ConfigurationManager`/`SecurityValidator`/`GitOperations`. No modular CLI. Simpler import set. |
| `orchestration-tools-changes-emailintelligence-cli-*` | 1,698 | **Oldest/smallest.** No interface-based architecture imports (no `AutoResolver`, `SemanticMerger`, `StrategyGenerator`, `RiskAssessor`). |

### Evolution Timeline

```
orchestration-tools (1,698 lines)
  └─ Basic CLI: ConstitutionalEngine + GitConflictDetector + ConflictAnalyzer only

feat/emailintelligence-cli-v2.0-with-pr-framework (1,754 lines)
  └─ +Interface-based architecture (AutoResolver, SemanticMerger, StrategyGenerator, RiskAssessor, Validator)

taskmaster / consolidate/cli-unification (1,745 lines)
  └─ +ConfigurationManager, SecurityValidator, GitOperations (modular core)
  └─ -CLI command system (no src.cli.commands)

feat-emailintelligence-cli-v2.0 (2,116 lines) ← MOST COMPLETE
  └─ +Modular CLI command system (src.cli.commands.integration)
  └─ +Dual-mode parser (legacy + modular)
  └─ +5 phases of development (Phase 1-5 documented in commit history)
  └─ Has interface-based imports but NOT the ConfigurationManager/SecurityValidator
```

### Missing from All Versions
- None have the **combined** feature set (modular CLI commands + ConfigurationManager + SecurityValidator)
- A true v3.0 would merge `feat-emailintelligence-cli-v2.0`'s command system with `taskmaster`'s modular core

---

## Remote-Only CLI Branches

### `feat-emailintelligence-cli-v2.0`

**Status:** Remote-only (not checked out locally)
**Commits:** 15 (most recent: `docs: update README with modular CLI architecture section`)

| Phase | Commit | Description |
|-------|--------|-------------|
| Phase 1 | `63c1e9b9` | SOLID foundation for CLI modularization |
| Phase 3 | `78c44423` | CLI integration |
| Phase 4 | `2184c094` | Testing framework |
| Phase 5 | `1c244f0e` | Documentation and cleanup |
| Final | `f588955e` | README update with modular CLI architecture |

**Unique features:** Modular command system in `src/cli/commands/` with:
- `analyze_command.py` — Analysis subcommand
- `analyze_history_command.py` — History analysis
- `plan_rebase_command.py` — Rebase planning
- `resolve_command.py` — Conflict resolution
- `validate_command.py` — Validation
- `factory.py`, `registry.py`, `interface.py` — Command registration framework

**Assessment:** Most architecturally advanced version. Should be the merge target for CLI unification.

---

### `feat/emailintelligence-cli-v2.0-with-pr-framework`

**Status:** Remote-only
**Relationship:** Ancestor/sibling of `feat-emailintelligence-cli-v2.0` (shares common history, diverged before Phases 1-5)

**Key commits:**
- `e5843d7e` — Phase 1-3 refactoring (core, git, storage, analysis)
- `fdfd2965` — Cherry-pick launch.py and setup files from orchestration-tools
- `830ce29e` — Merge from `feat-emailintelligence-cli-v2.0`

**Assessment:** Intermediate version. Superseded by `feat-emailintelligence-cli-v2.0`. Can be archived.

---

### `orchestration-tools-changes-emailintelligence-cli-20251112`

**Status:** Remote-only
**Key commit:** `a66b3cc6` — Merge latest CLI features from `feat-emailintelligence-cli-v2.0`

**Assessment:** Integration branch that pulled CLI features into orchestration-tools context. Oldest CLI version (1,698 lines). Historical artifact — can be archived.

---

## cli-consolidation Worktree — Divergence Analysis

### Worktree Details

| Property | Value |
|----------|-------|
| Path | `/home/masum/github/PR/cli-consolidation` |
| Branch | `consolidate/cli-unification` |
| emailintelligence_cli.py | Identical to taskmaster (1,745 lines) |

### Divergence Stats

| Metric | Count |
|--------|-------|
| Commits in **taskmaster** not in cli-unification | **141** |
| Commits in **cli-unification** not in taskmaster | **1,409** |
| Total diverged commits | **1,550** |

**This is massive divergence.** The branches share a common ancestor but have evolved independently with very different commit histories.

### cli-unification Unique Content

**Commits ahead (sample):**
- `d7474a89` — Integrate taskmaster CLI and src/ structure
- `acd42151` — Add SecurityValidator integration
- `0ee0b574` — Resolve merge conflicts for PR #176 integration
- `823d7a14` — Distribute .github/instructions to main branch
- Multiple PR merges (#198, #194, #189) and refactoring commits

**Unique directories in cli-consolidation:**
- `src/backend/` — Full Python backend (node engine, plugins, python_backend with routes, auth, database, AI engine, workflow engine)
- `src/cli/` — Modular command system
- `src/context_control/` — Context isolation/validation (12 modules: agent, config, core, environment, isolation, logging, models, project, storage, validation, exceptions)
- `src/__init__.py`

**Additional src/core/ modules only in cli-consolidation:**
- `advanced_workflow_engine.py`, `ai_engine.py`, `audit_logger.py`, `auth.py`, `caching.py`
- `database.py`, `factory.py`, `job_queue.py`, `mfa.py`, `middleware.py`
- `model_registry.py`, `performance_monitor.py`, `plugin_manager.py`, `rate_limiter.py`
- `security_validator.py`, `smart_filter_manager.py`, `workflow_engine.py`
- `data/` subpackage (database_source, data_source, factory, notmuch_data_source, repository)

**Additional scripts in cli-consolidation:**
- `scripts/agents/` — Agent scripts directory
- `scripts/context-control/` — Context control scripts
- `scripts/install-hooks.sh` — Hook installation
- `scripts/cleanup_orchestration.sh`, `scripts/orchestration_status.sh`
- 30+ additional Python scripts (conflict_predictor, bottleneck_detector, completion_predictor, concurrent_review, distributed_translation, etc.)

---

## Supporting Scripts & Utilities

### scripts/ Directory (taskmaster branch)

**Total:** ~95 Python scripts + 5 shell scripts

#### Git Management Tools (documented in `scripts/GIT_MANAGEMENT_TOOLS.md`)

| Script | Purpose |
|--------|---------|
| `analyze_git_history.py` | Categorize commit history, filter orchestration noise |
| `partial_cherry_pick.py` | Selective cherry-pick with safe change filtering |
| `inject_markers.py` | Inject 3-way merge conflict markers |

#### PRD / Round-Trip Fidelity

| Script | Purpose |
|--------|---------|
| `perfect_fidelity_reverse_engineer_prd.py` | Production-quality PRD from tasks |
| `ultra_enhanced_reverse_engineer_prd.py` | Advanced PRD reverse engineering |
| `ralph_loop_controller.py` | Iterative distance minimization (Tasks → PRD → Tasks) |
| `test_round_trip_enhanced.py` | Round-trip fidelity validation |
| `perfect_fidelity_validator.py` | Strict fidelity validation |
| `taskmaster_runner.py` | Unified task-master parse-prd with simulation fallback |

#### Task Enhancement

| Script | Purpose |
|--------|---------|
| `enhance_task_specifications_for_prd_accuracy.py` | Enhance task specs for PRD output |
| `validate_task_specifications.py` | Validate against enhanced template |
| `restructure_tasks_to_14_section_format.py` | Migrate tasks to 14-section standard |
| `add_missing_sections.py` | Add missing sections to task files |
| `standardize_tasks.py` | Standardize task formatting |

#### Task Analysis & Management

| Script | Purpose |
|--------|---------|
| `list_tasks.py` | List tasks with filtering |
| `show_task.py` | Display task details |
| `next_task.py` | Find next available task |
| `search_tasks.py` | Search tasks by keyword |
| `compare_task_files.py` | Compare task file versions |
| `task_summary.py` | Generate task summary |
| `audit_dependencies.py` | Audit task dependencies |
| `task_complexity_analyzer.py` | Analyze task complexity |

#### Shell Scripts

| Script | Purpose |
|--------|---------|
| `disable-hooks.sh` | Disable orchestration hooks for independent development |
| `sync_setup_worktrees.sh` | Sync setup files between worktrees |
| `reverse_sync_orchestration.sh` | Reverse sync approved changes to orchestration-tools |
| `format_code.sh` | Code formatting |
| `compress_progress.sh` | Compress progress logs |

### task_scripts/ Directory

| Script | Purpose |
|--------|---------|
| `secure_merge_task_manager.py` | Production-ready merge process management with security |
| `merge_task_manager.py` | Task-aware merge management |
| `taskmaster_common.py` | Shared utilities for task scripts |
| `task_validator_fixer.py` | Task validation and auto-fix |
| `consolidate_completed_tasks.py` | Move completed tasks to archive |

---

## src/ Module Structure Comparison

### Modules Present in Both Branches

| Module | Path |
|--------|------|
| Conflict Analyzer | `src/analysis/conflict_analyzer.py` |
| Constitutional Analyzer | `src/analysis/constitutional/analyzer.py` |
| Requirement Checker | `src/analysis/constitutional/requirement_checker.py` |
| API Main | `src/api/main.py` |
| Conflict Resolution App | `src/application/conflict_resolution_app.py` |
| Config | `src/core/config.py` |
| Conflict Models | `src/core/conflict_models.py` |
| Exceptions | `src/core/exceptions.py` |
| Git Operations | `src/core/git_operations.py` |
| Interfaces | `src/core/interfaces.py` |
| Security | `src/core/security.py` |
| Conflict Detector | `src/git/conflict_detector.py` |
| Repository | `src/git/repository.py` |
| Auto Resolver | `src/resolution/auto_resolver.py` |
| Semantic Merger | `src/resolution/semantic_merger.py` |
| Strategy Generator | `src/strategy/generator.py` |
| Risk Assessor | `src/strategy/risk_assessor.py` |
| Logger | `src/utils/logger.py` |
| Validator | `src/validation/validator.py` |

### Modules Only in cli-consolidation

| Category | Modules |
|----------|---------|
| **CLI Commands** (10) | `analyze_command`, `analyze_history_command`, `plan_rebase_command`, `resolve_command`, `validate_command`, `factory`, `registry`, `interface`, `integration`, `__init__` |
| **Context Control** (12) | `agent`, `config`, `core`, `environment`, `exceptions`, `isolation`, `logging`, `models`, `project`, `storage`, `validation`, `__init__` |
| **Backend** (40+) | Full Python backend, node engine, plugins, routes, auth, database, AI engine |
| **Core Extensions** (20+) | `advanced_workflow_engine`, `ai_engine`, `audit_logger`, `auth`, `caching`, `database`, `factory`, `job_queue`, `mfa`, `middleware`, `model_registry`, `performance_monitor`, `plugin_manager`, `rate_limiter`, etc. |
| **Strategy** (2) | `multi_phase_generator`, `reordering`, `selector` |

---

## Relevance to Branch Alignment Workflow

### Direct Relevance — High

| Alignment Task | CLI Capability | Mapping |
|---------------|----------------|---------|
| **Task 009** — Core rebase alignment | `auto_resolve_conflicts()`, `align_content()` | CLI can detect, analyze, and auto-resolve conflicts during rebase |
| **Task 010** — Complex alignment | `develop_spec_kit_strategy()`, `_interactive_strategy_development()` | CLI generates multi-phase resolution strategies for complex merges |
| **Task 013** — Conflict detection/resolution | `GitConflictDetector`, `ConflictAnalyzer`, `AutoResolver` | Direct implementation of conflict detection pipeline |
| **Task 014** — Validation | `validate_resolution()`, `Validator` | Post-resolution validation framework |
| **Task 005** — Error detection | `_detect_conflicts()`, `_detect_conflicts_interface_based()` | Detect merge artifacts and errors |

### Indirect Relevance

| Alignment Task | Script | Mapping |
|---------------|--------|---------|
| **Task 007** — Branch categorization | `analyze_git_history.py` | Git history categorization filters |
| **Task 004** — Branch protection | `scripts/disable-hooks.sh` | Hook management patterns |
| **Task 006** — Backup/restore | `secure_merge_task_manager.py` | Backup-before-merge pattern |
| **Task 012** — Orchestration | `ralph_loop_controller.py` | Iterative loop + state management pattern |

### The Self-Reference Problem

The CLI (`emailintelligence_cli.py`) is **itself a branch alignment challenge**:
- 5 versions across 4+ branches
- 1,550 diverged commits between the two main variants
- The tool meant to help with branch alignment needs to be aligned first

**Resolution path:** Merge `feat-emailintelligence-cli-v2.0` (modular CLI commands, 2,116 lines) with `taskmaster`'s `ConfigurationManager`/`SecurityValidator` additions to produce a unified v3.0.

---

## Recommendations

### Immediate Actions

1. **Archive stale CLI branches:**
   - `feat/emailintelligence-cli-v2.0-with-pr-framework` → superseded
   - `orchestration-tools-changes-emailintelligence-cli-20251112` → superseded

2. **Designate canonical CLI version:**
   - Base: `feat-emailintelligence-cli-v2.0` (most complete, has modular command system)
   - Merge in: `taskmaster`'s `ConfigurationManager`, `SecurityValidator`, `GitOperations` from `src/core/`

3. **Document the CLI for Task 004 hook integration:**
   - The CLI's `auto-resolve` and `validate-resolution` commands could be wired as pre-push hook validators

### Before Task 009

4. **Unify the CLI** as a prerequisite (or parallel to Task 004):
   - Checkout `feat-emailintelligence-cli-v2.0` into a worktree
   - Cherry-pick `ConfigurationManager`/`SecurityValidator` additions
   - Test the combined version
   - Merge back to `taskmaster`

5. **Evaluate cli-consolidation divergence:**
   - 1,409 commits ahead is too many to merge blindly
   - Use `analyze_git_history.py` to categorize those commits
   - Selective cherry-pick valuable additions (context_control, strategy extensions)

### Long-Term

6. **Single entry point:** Make `emailintelligence_cli.py` the unified CLI for both task management and conflict resolution (or keep them separate with clear separation)

7. **CI integration:** Wire the CLI's `validate-resolution` into Task 008's merge validation framework

---

*Generated by Amp CLI tools inventory analysis. Source: git branch analysis, file comparison, and module inspection across taskmaster, consolidate/cli-unification, and 3 remote-only branches.*
