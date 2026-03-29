# Tasks: Orchestration Core & Guided Workflows

**Input**: `specs/004-guided-workflow/plan.md`, `specs/004-guided-workflow/spec.md`
**Prerequisites**: `data-model.md`, `research.md`, `constitution.md`, `contracts/cli-schema.json`

**Tests**: Functional parity tests in ephemeral Git repositories and crash-recovery tests are MANDATORY (Constitution Section VIII).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel
- **[Story]**: US1, US2, US3, US4, US5, US6, US7, US8, US9, US10, US11, US12, US13, US14, US15

## Phase 1: Setup & Scaffolding (RE-EVALUATED)

- [ ] T001 Initialize `dev.py` with `typer` app shell and global flags. [RE-OPENED: Shell exists but global flag logic is stubbed]
- [x] T002 [P] Create core directory structure and `.dev_state/logs/`. [Verified]
- [x] T003 Define `src/core/base.py` with abstract base classes for logic engines, enforcing Agentic-First (Section XII) patterns. [Implemented]
- [x] T004 [P] Create `tests/conftest.py` with `git_repo` fixture for side-effect testing. [Verified]
- [ ] T005 [P] Setup crash-simulation test in `tests/functional/test_recovery.py`. [RE-OPENED: Test file exists but implementation is marked as TODO]
- [ ] T006 [P] Implement `SecurityValidator` in `src/core/security/validator.py` to verify environment safety for worktree operations. [Consolidation: `SecurityValidator` class]

## Phase 2: Foundational Logic & Data Models

- [x] T007 [P] Implement Pydantic models for Git data in `src/core/models/git.py` (ConflictModel, HunkModel). [Implemented]
- [x] T008 [P] Implement Pydantic models for History in `src/core/models/history.py` (CommitNode, HistoryPlan). [Implemented]
- [x] T009 [P] Implement Pydantic models for Orchestration in `src/core/models/orchestration.py` (Session, SyncReport). [Implemented]
- [x] T010 [P] Implement `ExecutionPlan` and `Action` models in `src/core/models/execution.py`. [Implemented]
- [ ] T011 [RE-OPEN] Update `SessionManager` in `src/core/execution/session.py` for auto-cleanup on success logic (Mandate: Section XII). [Guide: `.taskmaster/tasks/task_019.md`]
- [ ] T012 [P] Implement `AnswerService` in `src/core/utils/answers.py` for --answers injection logic.
- [ ] T013 [P] Implement `StructuredLogger` in `src/core/utils/logger.py` to sink JSONL logs to `.dev_state/logs/`.

## Phase 3: US1 & US6 - Headless Cockpit & CI (STUBBED)

**Goal**: Establish `dev.py` as the primary entry point for human and machine workflows.
**Test**: `dev.py analyze --json` returns valid JSON matching `contracts/cli-schema.json`.

- [ ] T014 [US1] Implement interactive `guide` command using `InquirerPy` in `dev.py`.
- [ ] T015 [US6] Implement `dev.py schema` command to output JSON schemas for all Pydantic models.
- [ ] T016 [US6] Integrate `AnswerService` and `StructuredLogger` into the Typer global callback in `dev.py`.
- [ ] T017 [US1] Create template for `.vscode/tasks.json` in `src/core/templates/vscode_tasks.json.j2`.
- [ ] T018 [US1] Create template for Antigravity config in `src/core/templates/antigravity.json.j2`.
- [ ] T019 [US1] Create template for Windsurf config in `src/core/templates/windsurf.json.j2`.
- [ ] T020 [US1] Implement `dev.py ide-init` command with `--target` option.
- [ ] T021 [US6] Write functional tests verifying `--json` mode returns valid payloads for all commands.

## Phase 4: US2 & US15 - High-Rigor Git Plumbing (CORE LOGIC)

**Goal**: Conflict detection and safe isolated resolution.
**Test**: `dev.py resolve --worktree` creates a clean isolated environment.

- [x] T022 [US2] Implement `GitPlumbing.merge_tree()` wrapper for `git merge-tree --real-merge` in `src/core/git/plumbing.py`. [Implemented]
- [ ] T023 [US15] Implement `GitPlumbing.setup_worktree()` and `GitPlumbing.cleanup_worktree()` in `src/core/git/plumbing.py`. [Guide: `.taskmaster/tasks/task_006.md`]
- [x] T024 [US2] Create test fixture in `tests/functional/test_git_plumbing.py` that generates real conflicting blob OIDs. [Verified]
- [ ] T025 [US2] Implement regex-based parser for `git merge-tree` output to extract paths and OIDs in `src/core/git/plumbing.py`.
- [ ] T026 [US2] Implement `ConflictDetector` logic to map parsed results into `ConflictModel` Pydantic objects.
- [ ] T027 [US2] Connect `dev.py analyze` to the `ConflictDetector`.

## Phase 5: US3 - Algorithmic Rebase Planning (CORE LOGIC)

- [x] T028 [US3] Define `HistoryService` class skeleton and `DAGBuilder` signatures in `src/core/git/history.py`. [Implemented]
- [x] T029 [US3] Create test data containing complex non-linear Git commit histories. [Verified]
- [x] T030 [US3] Implement `DAGBuilder` to parse `git rev-list --parents` into a directed adjacency list in `src/core/git/history.py`. [Implemented]
- [x] T031 [US3] Implement Kahn's Algorithm for topological sorting in `src/core/git/history.py`. [Implemented]
- [x] T032 [US3] Implement cycle detection and error handling for history graphs in `src/core/git/history.py`. [Implemented]
- [ ] T033 [US3] Implement `dev.py plan-rebase` command to generate and output sorted `HistoryPlan` objects.
- [ ] T034 [US3] Implement `dev.py rebase --apply` command to execute the plan interactively.

## Phase 6: US4 & US5 - Governance & Tool Sync

- [x] T035 [US4] Define `ASTScanner` and `ConstitutionalRule` logic in `src/core/analysis/scanner.py`. [Implemented]
- [x] T036 [US4] Create test file suite containing intentional architectural violations. [Verified]
- [x] T037 [US4] Implement `ast.NodeVisitor` logic to identify function/class definitions in forbidden paths in `src/core/analysis/scanner.py`. [Implemented]
- [ ] T038 [US5] Implement `SyncService` in `src/core/analysis/sync.py` using SHA-256 file hash comparisons against `origin/orchestration-tools`.
- [ ] T039 [US5] Implement `dev.py sync` command to report and apply updates from `orchestration-tools`.
- [ ] T040 [US4] Add `--const` flag logic to `dev.py analyze` to trigger the AST scanner.
- [ ] T041 [US1] Implement "Backup & Overwrite" logic in `src/core/utils/files.py` (rename to .bak).
- [ ] T042 [US1] Implement `dev.py install-hooks` using the backup logic.

## Phase 7: US7 - Resilient Session Recovery

- [x] T043 [US7] Implement atomic write logic for `Session` state update in `src/core/execution/session.py`. [Implemented]
- [ ] T044 [US7] Implement progress checkpointing in `ActionExecutor` to update `Session` index.
- [ ] T045 [US7] Implement resume-logic in `dev.py` to prompt user when a stale session is found.
- [ ] T046 [US7] Write integration tests for process interruption and state recovery in `tests/integration/test_recovery.py`.

## Phase 8: Polish & Safety Checks

- [ ] T047 Implement `ActionExecutor` subprocess runner with mandatory Dry-Run safety in `src/core/execution/executor.py`.
- [ ] T048 Implement `AutoResolver` strategy logic (Take Ours, Take Theirs, Simple Union) in `src/core/resolution/engine.py`.
- [ ] T049 Refactor `src/cli/commands/resolve_command.py` to use `AutoResolver`.
- [ ] T050 [US1] Implement `dev.py task run` command to parse and execute `tasks.md` checkbox lists in `dev.py`.
- [ ] T051 [US1] Add logic to `TaskRunner` to write commit hashes and log paths back to the input markdown file in `src/core/execution/task_runner.py`.
- [ ] T052 Perform final "No Stubs" audit across `src/core/` and remove obsolete placeholders.
- [ ] T053 Update `README.md` with high-fidelity usage, agentic protocol, and architecture diagrams.
- [ ] T054 Create `docs/orchestration_core.md` with detailed API and schema documentation.
- [ ] T055 [SC-002] Implement performance benchmarks for 100-commit history analysis (<5s).

## Phase 9: Dependency & Structural Analysis (US8, US12)

- [ ] T056 [P] [US8] Implement `DependencyExtractor` logic using `ast` and `ast-grep` CLI subprocess in `src/core/analysis/dependency.py`. [Guide: `.taskmaster/tasks/task_002.2.md`]
- [ ] T057 [US8] Implement `dev.py deps extract` and `dev.py deps compare` commands with JSON output in `dev.py`. [Protocol: JSON-First per Section XII]
- [ ] T058 [P] [US12] Implement structural similarity metrics (directory structure, filename fuzzy matching). [Guide: `.taskmaster/tasks/task_002.2.md`]
- [ ] T059 [US12] Integrate **`code-diff`** (GumTree algorithm) for high-accuracy function move and rename detection between branches.
- [ ] T060 [US12] Integrate `gkg` CLI to generate parquet-based dependency graphs in `src/core/git/knowledge_graph.py`.
- [ ] T061 [US12] Implement BM25 scoring for documentation and commit message similarity in `src/core/analysis/text.py`. [Protocol: Logic Chain 4 - Doc Sync]

## Phase 10: Advanced Alignment & Risk (US9, US10, US11, US12 - Micro)

**Goal**: Analyze individual branches to classify change types and assess risk (Layer 1: Micro Analysis).

- [ ] T062 [US10] Implement `ArtifactScanner` to detect conflict markers and broken imports in `src/core/analysis/artifacts.py`.
- [ ] T063 [P] [US9/US11] Implement `GitLogParser` and `CommitClassifier` logic for intent vs change analysis in `src/core/git/classifier.py`. [Guide: `.taskmaster/tasks/task_002.1.md`]
- [ ] T064 [US12] Implement `AlignmentService` to unify divergence, deps, and risk into a report in `src/core/analysis/align.py`. [Protocol: Logic chain 3 - Chess]
- [ ] T065 [US12] Implement `dev.py align <branch-a> <branch-b>` command.
- [ ] T066 [US12] Integrate `pydriller` for advanced commit topology analysis in `src/core/git/topology.py`.
- [ ] T067 [US9] Implement problematic commit detection and fix/avoidance selection UX. [Guide: `.taskmaster/tasks/task_002.5.md`]
- [ ] T068 [US12] Implement coarse-level alignment and atomic decomposition logic. [Protocol: FR-050]
- [ ] T069 [US12] Implement justification tracking for deletions and path changes. [Protocol: FR-051]
- [ ] T070 [US12] Integrate `git-graphable` for repository hygiene analysis in `src/core/git/hygiene.py`.

## Phase 11: Machine Intelligence & Performance (FR-048, FR-058, FR-059, US13 - Macro)

**Goal**: Group multiple branches by similarity and optimize merge sequencing (Layer 2: Macro Analysis).

- [ ] T071 [US12] Implement analysis cache with SHA-based validation in `src/core/execution/cache.py`. [Guide: `.taskmaster/tasks/task_002.6.md`]
- [ ] T072 [FR-048] Implement ML-based branch clustering using `AgglomerativeClustering` in `src/core/analysis/clustering.py`. [Guide: `.taskmaster/tasks/task_002.4.md`] [Modes: Targeted vs. Untargeted (US16)]
- [ ] T073 [US6] Implement time estimation and timeout awareness for long-running commands in `src/core/utils/performance.py`. [Protocol: FR-057]
- [ ] T074 [US12] Integrate semantic search using lightweight embeddings for documentation in `src/core/analysis/semantic.py`. [Protocol: FR-037]
- [ ] T075 [FR-058] Implement **Optimal Merge Sequencer** logic using **`networkx`** in `src/core/resolution/sequencer.py`. [Protocol: Logic Chain 3 - Chess]
- [ ] T076 [FR-059] Implement **Intent Overlap Detector** using BM25/AST similarity in `src/core/analysis/overlap.py`. [Protocol: Logic Chain 1 - Overlap]
- [ ] T077 [US1] Implement `dev.py align --batch` command to trigger the sequencer and overlap detector.
- [ ] T078 [US3] Migrate `HistoryService` logic to use **`networkx.DiGraph`** in `src/core/git/history.py`.

## Phase 12: Developer Experience & Shell (US1, US6)

- [ ] T079 [US1] Implement shell completion scripts for zsh, bash, and powershell using Typer in `src/cli/main.py`.
- [ ] T080 [US1] Implement interactive wizard patterns for complex src/setup/sync workflows in `src/cli/ui/wizard.py`.
- [ ] T081 [US1] Implement command aliases (br, an, etc.) and registration validation in `src/cli/main.py`.
- [ ] T082 [US6] Implement environment variable overrides for output modes (DEV_JSON, etc.) in `src/cli/main.py`.
- [ ] T083 [US1] Implement `git push` logic gated by the `--enable-remote` flag with lease safety in `src/core/git/plumbing.py`.

## Phase 13: History Pattern Analysis & Fix Memory (US14)

**Goal**: Detect change loops and suggest "Clean Simple Fixes" based on historical resolution templates.

- [ ] T084 [US14] Implement **History Loop Detector** to identify "Undo/Redo" commit patterns in `src/core/git/loop_detector.py`.
- [ ] T085 [US14] Implement **Resolution Template Engine** using **`rerereric`** logic to match and apply fuzzy conflict resolutions in `src/core/resolution/templates.py`.
- [ ] T086 [US14] Implement `dev.py analyze --patterns` command to report detected loops and suggest templates.
- [ ] T087 [US14] Implement `dev.py resolve --template` command to execute an automated cleanup fix.
- [ ] T088 [US14] Implement logic to ingest successful resolutions into the template store in `src/core/resolution/ingestor.py`.

## Phase 14: Final Audit & Delivery

**Goal**: Fulfill the "NO STUBS" mandate and finalize documentation.

- [ ] T089 Perform a project-wide audit to remove all `Logic in progress` markers and yellow-echo stubs in `dev.py` and `src/cli/commands/`.
- [ ] T090 Finalize `docs/orchestration_core.md` with 100% accurate API and JSON examples.
- [ ] T091 Run the full integration test suite against 50 divergent branch scenarios to verify SC-009 success.

## Phase 15: Logical Unification (Salvage Pass)

**Goal**: Restore 40+ functions and patterns discovered in the "Shadow" tools into the high-rigor architecture.

- [ ] T092 [US1] Move `setup_resolution` and worktree logic from `.taskmaster/emailintelligence_cli.py` to `src/core/git/plumbing.py`.
- [ ] T093 [US11] Move `CommitClassifier` and intent analysis logic from shadow tools to `src/core/git/classifier.py`.
- [ ] T094 [US14] Re-implement the `self_healing` pattern from root `emailintelligence_cli.py` into `src/core/base.py`.
- [ ] T095 [US6] Integrate `_generate_strategy_report` and `AlignmentReport` logic into `src/core/analysis/align.py`.

## Agentic Execution Protocol

1. **Consult Guide**: If a task has a `[Guide: ...]` reference, the agent MUST read that file in `.taskmaster/tasks/` before writing code. It contains the exact mathematical formulas and library parameters.
2. **Follow Logic Chains**: Ensure implementations support the defined research goals (e.g., T059 must support "Move vs Delete" detection).
3. **Agentic-First (Section XII)**: All command outputs must be machine-parseable JSON via Pydantic models.
4. **Resilience**: Every command must implement the **Circuit Breaker** pattern for remote or heavy processing calls.
5. **Validation**: Use `tests/conftest.py` to verify logic against ephemeral Git repositories for every task completion.

## Dependencies

1. Foundational Models (Phase 2) must precede Logic implementation (Phases 4-6).
2. US7 SessionManager (Phase 1/7) is foundational for all long-running commands.
3. US1 & US6 (Phase 3) establish the interface protocol for all subsequent logic.
4. All logic engines (Phases 4-6) depend on Phase 2 data models.
5. Similarity engines (Phase 9) are prerequisites for complex alignment reports (Phase 10).
6. NetworkX migration (T078) is a prerequisite for advanced Merge Sequencing (T075).

## Implementation Strategy

1. **Safety & Scaffolding First**: Deliver Phase 1 & 2 to establish the "Law" (Constitution) and the "Language" (Data Models).
2. **Interface Mastery**: Finalize Phase 3 to enable the machine-first protocol for subsequent work.
3. **Atomic Intelligence**: Deliver Phase 4 (Conflicts) and Phase 5 (Rebase) step-by-step, ensuring each algorithm is fully tested.
4. **Resilience & Sync**: Deliver Phase 6 and 7 to lock down the codebase architecture and ensure crash-safety.
5. **Advanced Alignment**: Build out dependency analysis and similarity scoring before finalizing the comprehensive alignment report.
