# Tasks: Task Execution Layer

**Input**: `specs/013-task-execution-layer/plan.md`, `specs/013-task-execution-layer/spec.md`
**Prerequisites**: 004-guided-workflow execution modules (task_runner.py, executor.py, session.py, models/execution.py)

**Tests**: Functional execution tests using ephemeral task files and crash-recovery tests are MANDATORY.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel
- **[Story]**: US1 (Execution), US2 (PR Tracking), US3 (Configuration)

## Phase 1: Task Parser Enhancement

- [ ] T001 [US1] Define `Task` Pydantic model with fields (id, description, command, status, dependencies, metadata) in `src/core/models/execution.py`
- [ ] T002 [US1] Implement structured `tasks.md` parser in `src/core/execution/task_runner.py` — extract task ID, checkbox status, description, and inline metadata
- [ ] T003 [US1] Add dependency declaration parsing (e.g., `depends: T001, T002`) to task parser
- [ ] T004 [P] [US1] Implement DAG validation for task dependencies — detect circular dependencies and report in `src/core/execution/task_runner.py`
- [ ] T005 [P] [US1] Write unit tests for parser: valid tasks.md, empty file, malformed entries, circular deps in `tests/unit/test_task_parser.py`

## Phase 2: Execution Engine

- [ ] T006 [US1] Upgrade `ActionExecutor.execute_action()` to capture stdout/stderr via `subprocess.run(capture_output=True)` in `src/core/execution/executor.py`
- [ ] T007 [US1] Add per-task timeout support using `subprocess.run(timeout=)` with configurable default (300s) in `src/core/execution/executor.py`
- [ ] T008 [US1] Implement execution state tracking (Pending → In Progress → Done → Failed) in `ActionExecutor` with state updates to `ExecutionLog` model
- [ ] T009 [US3] Add `stop_on_fail` and `continue_on_fail` configuration options to `ExecutionPlan` model in `src/core/models/execution.py`
- [ ] T010 [P] [US1] Write functional test: execute 3 tasks in sequence, verify ordering and state transitions in `tests/functional/test_execution.py`

## Phase 3: Crash Recovery

- [ ] T011 [US1] Enhance `SessionManager.save()` to include per-task execution index in session state in `src/core/execution/session.py`
- [ ] T012 [US1] Implement `SessionManager.get_resume_index()` to return the last successfully completed task index
- [ ] T013 [US1] Add resume prompt logic to `dev.py task run` — detect stale session, ask user to resume or restart
- [ ] T014 [P] [US1] Write crash-recovery test: simulate process kill mid-execution, verify resume from correct task in `tests/functional/test_recovery.py`

## Phase 4: Reporting & PR Integration

- [ ] T015 [US1] Define `ExecutionReport` Pydantic model (total, passed, failed, skipped, duration, per-task details) in `src/core/models/execution.py`
- [ ] T016 [US1] Implement report generation in `ActionExecutor` after execution completes in `src/core/execution/executor.py`
- [ ] T017 [US1] Add `--json` output mode for execution report in `dev.py task run` command
- [ ] T018 [P] [US2] Add PR issue linking: parse `resolves: #123` metadata from tasks and include in report
- [ ] T019 [P] [US1] Write test: verify report contains correct pass/fail counts and per-task durations in `tests/unit/test_execution_report.py`

## Phase 5: Edge Cases & Polish

- [ ] T020 [US3] Implement configurable parallel vs serial execution mode in `ExecutionPlan`
- [ ] T021 [US1] Add SIGTERM → SIGKILL escalation for timed-out tasks in `ActionExecutor`
- [ ] T022 [P] [US1] Implement environment snapshot at execution start (capture PATH, key env vars) in `ExecutionLog`
- [ ] T023 [US1] Update `dev.py task run --help` with usage examples and document in `docs/orchestration_core.md`
- [ ] T024 [US1] Perform "No Stubs" audit of `src/core/execution/` — replace all placeholder logic with real implementations

## Dependencies

1. Phase 1 (Parser) must complete before Phase 2 (Engine) — engine needs parsed Task objects.
2. Phase 2 (Engine) must complete before Phase 3 (Recovery) — recovery needs execution state.
3. Phase 4 (Reporting) depends on Phase 2 completion.
4. Phase 5 tasks are independent once Phase 2 is done.
5. External: 004-guided-workflow execution modules must exist (✅ confirmed).

## Implementation Strategy

1. **Parser First**: Upgrade the stub TaskRunner to a real parser — this unblocks everything.
2. **Engine Core**: Add stdout capture, timeout, state tracking to ActionExecutor.
3. **Resilience**: Enhance SessionManager for per-task checkpointing.
4. **Ship Report**: Generate structured reports for human and agent consumption.
5. **Harden**: Edge cases, parallel mode, environment tracking.
