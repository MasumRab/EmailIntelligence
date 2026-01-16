# Implementation Plan: Guided CLI Workflows

**Branch**: `004-guided-workflow` | **Date**: 2026-01-16 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/004-guided-workflow/spec.md`

## Summary

Implement a unified developer CLI (`dev.py`) that provides interactive guidance (`guide-dev`, `guide-pr`) and integrates advanced conflict resolution engines from the Scientific branch (`GitConflictDetector`, `ConstitutionalEngine`).

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: `argparse` (stdlib), `git` (CLI), `PyYAML` (for constitutions)
**Storage**: In-memory state for guides; JSON for analysis reports.
**Testing**: `pytest` for unit/integration tests.
**Target Platform**: Developer Workstations (Linux/macOS/WSL).
**Project Type**: CLI Tooling.

## Constitution Check

*   **Verification-First**: All guides must be tested.
*   **Fail-Safe**: `GitWorktreeRunner` ensures main worktree safety.
*   **Role-Based**: Guides are advisory; they do not force destructive actions without confirmation.

## Project Structure

### Documentation
```text
specs/004-guided-workflow/
├── plan.md              # This file
├── research.md          # Unified Integration Strategy
├── data-model.md        # Unified Schemas
├── quickstart.md        # Usage Guide
└── tasks.md             # Implementation Tasks
```

### Source Code
```text
dev.py                          # New Entry Point (Sidecar)
src/
├── cli/
│   └── guides/                 # Standalone Guide Modules
│       ├── dev_guide.py
│       └── pr_guide.py
├── core/
│   ├── git/
│   │   └── worktree.py         # GitWorktreeRunner
│   └── conflict_models.py      # Data Models
├── resolution/                 # Scientific Engines
└── lib/
    └── workflow_context.py     # State Manager
```

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| `dev.py` Sidecar | Decoupling from `launch.py` | Modifying `launch.py` blocked by refactor risks. |
| `GitWorktreeRunner` | Safety / Isolation | In-place analysis risks destroying user work. |