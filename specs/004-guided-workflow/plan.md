# Implementation Plan: Orchestration Core & Guided Workflows

**Branch**: `004-guided-workflow` | **Date**: 2026-01-14 | **Spec**: ./spec.md
**Input**: Feature specification for `dev.py` (Orchestration Core).

## Summary
Implement `dev.py` as the unified developer cockpit, replacing scattered scripts with a high-rigor, API-first Python application. This system integrates Git plumbing (merge-tree), constitutional enforcement (AST scanning), and atomic session persistence to enable safe, guided development workflows.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: `typer` (CLI), `pydantic` (Data Models), `GitPython` (Plumbing), `rich` (UI), `InquirerPy` (Interactive prompts).
**Storage**: Atomic JSON (`.dev_state.json`) for session persistence (Gitignored).
**Testing**: `pytest` with functional Git side-effect verification (Ephemeral Repos).
**Target Platform**: Developer Workstation (Linux/macOS).
**Project Type**: Single Project (CLI Tool).
**Performance Goals**: <5s analysis for 100 commits; <200ms CLI startup.
**Constraints**: Zero working-tree modification during analysis; No logic in `scripts/`.
**Scale/Scope**: ~20 core modules, supporting 1000+ commits history analysis.
**IDE Integration**: Templates for VSCode, Antigravity, and Windsurf (US1/FR-010).

## Constitution Check

*GATE: Must pass before Phase 0 research.*

- **Principle VII (API-First)**: Core logic (git, analysis, resolution) isolated in `src/core/` and exposed via Pydantic APIs. `dev.py` is a thin CLI wrapper. (PASS)
- **Principle IX (Orchestration)**: `dev.py` respects the "File Ownership Matrix", managing only orchestration files. (PASS)
- **Principle II (TDD)**: All logic engines (merge-tree parser, AST scanner) testable via unit tests before integration. (PASS)
- **Extension B (Verification)**: "Context-Aware Verification" implemented via AST Scanner and Sync Service. (PASS)

## Project Structure

### Documentation (this feature)

```text
specs/004-guided-workflow/
├── plan.md              # This file
├── research.md          # Git plumbing nuances
├── data-model.md        # Pydantic schemas (Session, Conflict, etc.)
├── quickstart.md        # Developer guide for dev.py
├── contracts/           # CLI Interface definitions
└── tasks.md             # Implementation tasks
```

### Source Code (repository root)

```text
src/
├── core/                    # Pure Logic (API-First)
│   ├── git/                 # Plumbing wrappers (merge-tree, rev-list)
│   ├── analysis/            # AST Scanner, Sync Service
│   ├── resolution/          # Conflict Logic, Rebase Planner
│   ├── execution/           # Session Manager, Action Executor
│   └── models/              # Pydantic Definitions (v1.1.0)
├── cli/                     # Interface Layer
│   ├── commands/            # Typer subcommands (analyze, plan, etc.)
│   └── main.py              # dev.py entry point
└── utils/                   # Shared utilities (logging, hashing)

tests/
├── unit/                    # Logic tests (AST, Parsing)
├── integration/             # Git side-effect tests (Ephemeral)
└── fixtures/                # Complex git history generators
```

**Structure Decision**: Standard "Single Project" layout, strictly separating `core` (Logic) from `cli` (Presentation) to satisfy Principle VII.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| In-Memory Git Analysis | "Plumbing over Porcelain" requirement (US2) | `git checkout` (Porcelain) disrupts user workflow and triggers hooks. |
| AST Scanning | "Constitution Enforcement" (US4) | Regex matching is too fragile for detecting logical violations (e.g. class structure). |
| Multi-IDE Support | "Unified Cockpit" (US1) | Restricting to VSCode alienates users of Windsurf/Antigravity; Template complexity is low. |
| Atomic Hook Backup | "Fail-Safe" (Design Principle 1) | Interactive prompts for every hook install create friction; Backup is safer. |