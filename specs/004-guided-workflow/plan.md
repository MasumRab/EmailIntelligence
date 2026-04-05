# Implementation Plan: Orchestration Core & Guided Workflows

**Branch**: `004-guided-workflow` | **Date**: 2026-03-17 | **Spec**: ./spec.md
**Input**: Feature specification for `dev.py` (Orchestration Core) - Updated with Constitution v1.6.0 (Agentic-First)

## Summary

Implement `dev.py` as the unified developer cockpit, replacing scattered stubs with a high-rigor, API-first Python application. This system integrates Git plumbing (`merge-tree`), constitutional enforcement (AST scanning), and atomic, ephemeral session persistence to enable safe, guided development workflows. The design prioritizes AI agent consumption (JSON-first) while providing a polished interactive experience for humans.

## Technical Context

**Language/Version**: Python 3.11+ (Required for `typer` and `pydantic` v2 compatibility)  
**Primary Dependencies**: 
- `typer[all]` (CLI Framework with shell completion)
- `pydantic` (Data Models & JSON Serialization)
- `rich` (Terminal Styling for Human UX)
- `InquirerPy` (Interactive Wizard Patterns)
- `networkx` (Graph Engine for Multi-Branch Chess strategy)
- `code-diff` (AST-based move and rename detection)
- `rerereric` (Fuzzy conflict resolution pattern matching)
- `pyastsim` (AST Similarity Detection)
- `rank-bm25` (BM25 Text Similarity)
- `scikit-learn` (ML Branch Clustering)
- `pydriller` (Commit Topology Analysis)
- `ast-grep` (Structural Pattern Matching)
- `gkg` (Git Knowledge Graph)
**Storage**: Ephemeral JSON (`.dev_state.json`) for session persistence; Structured JSONL logs in `.dev_state/logs/`.  
**Testing**: `pytest` with functional Git side-effect verification using Ephemeral (temporary) Git repositories.  
**Target Platform**: Developer Workstation (Linux/macOS).
**Project Type**: CLI Tool / Orchestration Engine.  
**Performance Goals**: <5s analysis for 100 commits; <200ms CLI startup; BM25 similarity <2s for 1000 pairs.  
**Constraints**: 
- 🔴 **Zero working-tree modification** during analysis (US2).
- 🔴 **No logic in `scripts/`** (Constitution Section I).
- 🔴 **Agentic-First**: Every command MUST support `--json` (Constitution Section XII).
- 🔴 **Safety Flag**: Remote operations require `--enable-remote`.  
**Scale/Scope**: Supports repositories with 10k+ files and 1k+ commit histories.  
**IDE Integration**: Templates for VSCode, Antigravity, and Windsurf (FR-041).

## Constitution Check (v1.6.0)

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

1. **Principle 0 (Agentic-First)**:
   - ✅ Every command implemented in `src/cli/commands/` MUST inherit from a base that enforces `--json`, exit codes, and structured error reporting.
   - ✅ JSON schemas MUST be defined for all outputs (FR-018).

2. **Section XII (Agentic-First Tool Design)**:
   - ✅ **Machine-Parseable**: Default to Rich-styled text, but strict JSON on `--json`.
   - ✅ **Exit Codes**: 0=Success, 1=General, 2=Usage, 3=Conflict, 4=Violation.
   - ✅ **Structured Errors**: JSON `{code, message, details, hint}`.

3. **Section VII (API-First)**:
   - ✅ Core logic isolated in `src/core/`. CLI is a thin wrapper.

4. **Section II (TDD)**:
   - ✅ Logic engines (HistoryService, ASTScanner) MUST have unit tests before CLI integration.

## Project Structure

### Documentation (this feature)

```text
specs/004-guided-workflow/
├── plan.md              # This file
├── research.md          # Technology decisions and algorithm research
├── data-model.md        # Pydantic entity definitions
├── quickstart.md        # Usage guide for humans and agents
├── contracts/           # CLI command schemas and JSON output contracts
└── tasks.md             # Implementation tasks (generated separately)
```

### Source Code (repository root)

```text
src/
├── core/                    # Pure Logic (API-First)
│   ├── git/                 # Plumbing wrappers (merge-tree, rev-list, pydriller)
│   ├── analysis/            # AST Scanner, Sync Service, ML Clustering
│   ├── resolution/          # Conflict Engine, Rebase Planner
│   ├── execution/           # Session Manager, Action Executor, Task Engine
│   └── models/              # Pydantic Definitions (Entities)
├── cli/                     # Interface Layer
│   ├── commands/            # Typer subcommands (analyze, sync, align, etc.)
│   ├── ui/                  # Rich/InquirerPy components
│   └── main.py              # dev.py entry point
└── utils/                   # Shared utilities (logging, hashing, answers)

dev.py                       # Unified CLI entry point (thin wrapper)
.dev_state/                  # Ephemeral state and logs (gitignored)
    ├── .dev_state.json      # Atomic session state
    └── logs/                # Structured JSONL logs
```

**Structure Decision**: Single project layout with strict separation between `src/core` (Domain Logic) and `src/cli` (Delivery). This ensures the "Orchestration Core" is a reusable library that the CLI happens to consume.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| In-Memory Git Analysis | "Plumbing over Porcelain" requirement (US2) | `git checkout` disrupts user workflow and triggers hooks unnecessarily. |
| AST Scanning | "Constitution Enforcement" (US4) | Regex is too fragile for detecting complex logical violations. |
| ML Clustering | "Intelligent Branch Grouping" (FR-048) | Manual tagging is unscalable for large feature sets. |
| Atomic Decomp | "Safe History Rewriting" (FR-050) | Single large commits make history-revert impossible for complex alignments. |

## Phase Priorities

### Phase 1: Agentic-First Infrastructure (MANDATORY)
1. Implement `BaseCommand` with `--json`, `--quiet`, `--verbose` support.
2. Implement `StructuredLogger` (JSONL to `.dev_state/logs/`).
3. Implement `SessionManager` (Ephemeral state with auto-cleanup on success).
4. Implement `ErrorRegistry` for consistent `{code, message, details, hint}` reporting.
5. Implement `SecurityValidator` (Pre-flight check for worktree operations).

### Phase 2: High-Rigor Git & AST Plumbing
1. Implement `GitPlumbing` (merge-tree, rev-list, worktree setup) in `src/core/git/`.
2. Implement `ASTScanner` with dynamic rule parsing from `constitution.md`.
3. Implement `HistoryService` (DAG, topological sort).

### Phase 3: Alignment & Similarity (FR-019 - FR-037)
1. Implement `DependencyExtractor` (ast-grep + Python AST).
2. Implement `SimilarityEngine` (pyastsim, BM25).
3. Implement `BranchAligner` (coarse-level alignment, atomic decomposition).

### Phase 4: Intelligence & Tasks (FR-040 - FR-059)
**Strategy**: Implement Micro-level classification (intent/risk) followed by Macro-level clustering (thematic overlap) to enable the "Multi-Branch Chess" merge engine.

1. Implement `TaskEngine` (markdown checkbox execution).
2. Implement **Micro-Intelligence**: `CommitClassifier` and `ArtifactScanner` (US9, US10, US11).
3. Implement **Macro-Intelligence: BranchClustering** (Targeted vs. Untargeted modes) (FR-048, US16).
4. Implement **Macro-Intelligence: MergeSequencer** (FR-058, US12, US13).
5. Implement **Macro-Intelligence: OverlapDetector** (FR-059).
6. Implement `TimeEstimator` and `TimeoutManager`.
7. Implement `WizardPatterns` (InquirerPy).

### Phase 5: History Pattern Analysis & Fix Memory (US14)
**Strategy**: Implement automated detection of developmental "loops" (undo/redo) and problematic commit patterns, mapping them to pre-validated resolution templates.

1. Implement `HistoryLoopDetector` (detecting redundant changes).
2. Implement `ResolutionTemplateEngine` (using `rerereric` logic for fuzzy fix matching).
3. Implement `PatternReport` integration into the `align` command.
