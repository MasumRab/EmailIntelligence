# Decomposition & Testability Checklist: Orchestration Core

**Purpose**: Validate that requirements and tasks are sufficiently granular to ensure low-complexity implementation and easy verification.
**Created**: 2026-01-14
**Feature**: [004-guided-workflow](../spec.md)

## Requirement Granularity (Spec)

- [x] CHK001 Are functional requirements atomic (one verb/outcome per FR)? [Clarity, Spec Requirements]
- [x] CHK002 Is the "canonical source" for Sync explicitly defined to prevent implementation ambiguity? [Clarity, FR-013]
- [x] CHK003 Are the specific AST rules for "Constitution Enforcement" defined or delegated to a specific config format? [Completeness, FR-004]
- [x] CHK004 Is the output format of the "Violation Report" specified (JSON schema vs free text)? [Measurability, FR-015]
- [x] CHK005 Are "interactive" behaviors (e.g., multi-select) separated from "headless" behaviors in requirements? [Consistency, US5 vs US6]

## Task Atomicity (Tasks)

- [x] CHK006 Does every task in Phase 4 (Conflict Analysis) result in a verifiable state change or output? [Measurability, Tasks Phase 4]
- [x] CHK007 Are "Research" tasks separated from "Implementation" tasks to prevent scope creep? [Granularity]
- [x] CHK008 Are the Pydantic model tasks (T006-T009) broken down by domain (Git, History, Orchestration) to allow parallel work? [Decomposition, Tasks Phase 2]
- [x] CHK009 Is the `SessionManager` implementation (T010) isolated from its consumer integration (T038) to reduce coupling? [Decomposition, Tasks Phase 2 vs 7]
- [x] CHK010 Are unit tests for "Git Plumbing" (T020) scheduled *before* the logic implementation (T023)? [Ordering, Tasks Phase 4]

## Logic & Testability

- [x] CHK011 Can the `ConflictDetector` be tested with *pure data* (OIDs) without requiring a full git repo on disk? [Testability, Plan Data Model]
- [x] CHK012 Is the `DAGBuilder` logic (T028) decoupled from the `git rev-list` command execution for easier unit testing? [Testability, Tasks Phase 5]
- [x] CHK013 Are error scenarios (e.g., "Binary File Conflict") explicitly accounted for in the task list? [Completeness, Edge Cases]
- [x] CHK014 Is the "Atomic Write" mechanism (FR-014) verified by a specific crash-recovery test task? [Coverage, T041]
- [x] CHK015 Are the "Token-Saver" UI requirements testable via a captured stdout check? [Measurability, T018]

## Dependencies & Flow

- [x] CHK016 Are the "Foundational" data models (Phase 2) confirmed as blockers for all subsequent Logic phases? [Dependency, Tasks Dependencies]
- [x] CHK017 Is the `dev.py` CLI skeleton (Phase 3) required before implementing specific subcommands to ensure a consistent interface? [Dependency]
- [x] CHK018 Are parallelization opportunities marked `[P]` valid (i.e., truly no shared state dependencies)? [Efficiency, Tasks]

## Notes
- Use this checklist to verify that the implementation plan remains low-complexity.
- If a task feels "too big" during implementation, refer back to CHK001-005 to see if the requirement itself was too broad.
