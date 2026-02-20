# Tasks: Orchestration Core & Guided Workflows

**Input**: `specs/004-guided-workflow/plan.md`, `specs/004-guided-workflow/spec.md`
**Prerequisites**: `data-model.md` (v1.1.0), `research.md`, `constitution.md`

**Tests**: Functional parity tests in ephemeral Git repositories and crash-recovery tests are MANDATORY (Constitution Section VIII).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel
- **[Story]**: US1, US2, US3, US4, US5, US6, US7

## Phase 1: Setup & Scaffolding

- [x] T001 Initialize `dev.py` with `typer` application and global options (--dry-run, --json, --quiet, --answers) in `dev.py`
- [x] T002 [P] Create core directory structure: `src/core/{git,analysis,resolution,execution,models,utils}`
- [x] T003 Define `src/core/base.py` with abstract base classes for logic engines
- [x] T004 [P] Create `tests/conftest.py` with `git_repo` fixture for side-effect testing
- [x] T005 [P] Setup crash-simulation test in `tests/functional/test_recovery.py` to verify Session foundation

## Phase 2: Foundational logic & Data Models (v1.1.0)

- [x] T006 [P] Implement Pydantic models for Git data in `src/core/models/git.py` (ConflictModel, HunkModel) with Stable IDs
- [x] T007 [P] Implement Pydantic models for History in `src/core/models/history.py` (CommitNode, HistoryPlan) with Stable IDs
- [x] T008 [P] Implement Pydantic models for Orchestration in `src/core/models/orchestration.py` (Session, SyncReport)
- [x] T009 [P] Implement `ExecutionPlan` and `Action` models in `src/core/models/execution.py` with schema version 1.1.0 logic
- [x] T010 Implement `SessionManager` in `src/core/execution/session.py` for atomic `.dev_state.json` persistence (US7 foundation)
- [x] T011 [P] Implement `AnswerService` in `src/core/utils/answers.py` for --answers injection logic
- [x] T012 [P] Implement `TokenSaver` utility in `src/core/utils/logger.py` to suppress Rich output in headless mode

## Phase 3: US1 & US6 - Headless Cockpit & CI (Priority: P1)

**Goal**: Establish `dev.py` as the primary entry point for human and machine workflows.
**Test**: `dev.py analyze --json` returns valid JSON with zero ANSI noise.

- [x] T013 [US1] Implement interactive `guide` command using `InquirerPy` in `dev.py`
- [x] T014 [US6] Implement `dev.py schema` command to output JSON schemas for all Pydantic models
- [x] T015 [US6] Integrate `AnswerService` and `TokenSaver` into the Typer global callback in `dev.py`
- [x] T016 [US1] Create template for `.vscode/tasks.json` in `src/core/templates/vscode_tasks.json.j2`
- [x] T017 [US1] Create template for Antigravity config in `src/core/templates/antigravity.json.j2`
- [x] T018 [US1] Create template for Windsurf config in `src/core/templates/windsurf.json.j2`
- [x] T019 [US1] Implement `dev.py ide-init` command with `--target` option to generate configs from templates
- [x] T020 [US6] Write functional tests verifying `--json` mode returns valid payloads for all commands

## Phase 4: US2 - In-Memory Conflict Analysis (Priority: P1)

**Goal**: High-rigor conflict detection using Git plumbing without worktree modification.
**Test**: `dev.py analyze` output matches `git merge` results while worktree remains clean.

- [x] T021 [US2] Define `ConflictDetector` class skeleton and `GitPlumbing` interface in `src/core/git/plumbing.py`
- [x] T022 [US2] Create test fixture in `tests/functional/test_git_plumbing.py` that generates real conflicting blob OIDs
- [x] T023 [US2] Implement `GitPlumbing.merge_tree()` wrapper for `git merge-tree --real-merge` in `src/core/git/plumbing.py`
- [x] T024 [US2] Implement regex-based parser for `git merge-tree` output to extract paths and OIDs in `src/core/git/plumbing.py`
- [x] T025 [US2] Implement `ConflictDetector` logic to map parsed results into `ConflictModel` Pydantic objects in `src/core/git/detector.py`
- [x] T026 [US2] Refactor existing `src/cli/commands/analyze_command.py` to use `ConflictDetector` via logic core
- [x] T027 [US2] Implement `dev.py analyze` command to trigger and display the Conflict Report in `dev.py`

## Phase 5: US3 - Algorithmic Rebase Planning (Priority: P2)

**Goal**: Topologically sort commits for clean rebase plans.
**Test**: Verify linear commit sequence respects parent-child dependencies in multi-branch DAGs.

- [x] T028 [US3] Define `HistoryService` class skeleton and `DAGBuilder` signatures in `src/core/git/history.py`
- [x] T029 [US3] Create test data containing complex non-linear Git commit histories in `tests/fixtures/git_history.py`
- [x] T030 [US3] Implement `DAGBuilder` to parse `git rev-list --parents` into a directed adjacency list in `src/core/git/history.py`
- [x] T031 [US3] Implement Kahn's Algorithm for topological sorting in `src/core/git/history.py`
- [x] T032 [US3] Implement cycle detection and error handling for malformed history graphs in `src/core/git/history.py`
- [x] T033 [US3] Implement `dev.py plan-rebase` command to generate and output sorted `HistoryPlan` objects in `dev.py`
- [x] T034 [US3] Implement `dev.py rebase --apply` command to execute the plan interactively

## Phase 6: US4 & US5 - Governance & Tool Sync (Priority: P2)

**Goal**: Enforce constitution and synchronize environment scripts.
**Test**: divergence from `orchestration-tools` detected; logic leaks in `scripts/` flagged.

- [x] T035 [US4] Define `ASTScanner` and `ConstitutionalRule` logic in `src/core/analysis/scanner.py`
- [x] T036 [US4] Create test file suite containing intentional architectural violations in `tests/fixtures/bad_code.py`
- [x] T037 [US4] Implement `ast.NodeVisitor` logic to identify function/class definitions in forbidden paths in `src/core/analysis/scanner.py`
- [x] T038 [US5] Implement `SyncService` in `src/core/analysis/sync.py` using SHA-256 file hash comparisons against `origin/orchestration-tools`
- [x] T039 [US5] Implement `dev.py sync` command to report and apply updates from `orchestration-tools` in `dev.py`
- [x] T040 [US4] Add `--const` flag logic to `dev.py analyze` to trigger the AST scanner in `dev.py`
- [x] T041 [US1] Implement "Backup & Overwrite" logic in `src/core/utils/files.py` (rename to .bak)
- [x] T042 [US1] Implement `dev.py install-hooks` using the backup logic to safely install constitutional hooks

## Phase 7: US7 - Resilient Session Recovery (Priority: P3)

**Goal**: Persist and resume long-running orchestration operations.
**Test**: Kill process during merge; verify `dev.py` resumes from correct index.

- [x] T043 [US7] Implement atomic write logic for `Session` state update in `src/core/execution/session.py`
- [x] T044 [US7] Implement progress checkpointing in `ActionExecutor` to update `Session` index in `src/core/execution/executor.py`
- [x] T045 [US7] Implement resume-logic in `dev.py` to prompt user when a stale session is found in `dev.py`
- [x] T046 [US7] Write integration tests for process interruption and state recovery in `tests/integration/test_recovery.py`

## Phase 8: Polish & Advanced Logic

- [x] T047 Implement `ActionExecutor` subprocess runner with mandatory Dry-Run safety in `src/core/execution/executor.py`
- [x] T048 Implement `AutoResolver` strategy logic (Take Ours, Take Theirs, Simple Union) in `src/core/resolution/engine.py`
- [x] T049 Refactor `src/cli/commands/resolve_command.py` to use `AutoResolver` and accept Stable IDs
- [x] T050 [US1] Implement `dev.py task run` command to parse and execute `tasks.md` checkbox lists in `dev.py`
- [x] T051 [US1] Add logic to `TaskRunner` to write commit hashes and log paths back to the input markdown file in `src/core/execution/task_runner.py`
- [x] T052 Perform final "No Stubs" audit across `src/core/` and remove obsolete placeholders
- [x] T053 Update `README.md` with high-fidelity usage, agentic protocol, and architecture diagrams
- [x] T054 Create `docs/orchestration_core.md` with detailed API and schema documentation

## Dependencies

1. Foundational Models (Phase 2) must precede Logic implementation (Phases 4-6).
2. US7 SessionManager (Phase 1/7) is foundational for all long-running commands.
3. US1 & US6 (Phase 3) establish the interface protocol for all subsequent logic.
4. All logic engines (Phases 4-6) depend on Phase 2 data models.

## Implementation Strategy

1. **Safety & Scaffolding First**: Deliver Phase 1 & 2 to establish the "Law" (Constitution) and the "Language" (Data Models).
2. **Interface Mastery**: Finalize Phase 3 to enable the machine-first protocol for subsequent work.
3. **Atomic Intelligence**: Deliver Phase 4 (Conflicts) and Phase 5 (Rebase) step-by-step, ensuring each algorithm is fully tested.
4. **Resilience & Sync**: Deliver Phase 6 and 7 to lock down the codebase architecture and ensure crash-safety.