# Tasks: Task Execution Layer

**Input**: `specs/007-task-execution-layer/spec.md`
**Prerequisites**: plan.md (required)

**Tests**: Test-Driven Development (TDD) is MANDATORY.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel
- **[Story]**: US1, US2, US3

## Phase 1: Models & Parsing (Foundational)

- [ ] T001 [P] [US1] Define `Task` and `TaskPhase` data models in `src/models/task.py` including attributes for ID, dependencies, and command.
- [ ] T002 [P] [US1] Implement `TaskParser` in `src/services/task_parser.py` to parse standard `tasks.md` format.
- [ ] T003 [US1] Write unit tests for `TaskParser` to verify it correctly extracts tasks from a sample markdown string in `tests/unit/test_task_parser.py`.
- [ ] T004 [US1] Implement dependency graph validation (circular dependency detection) in `src/services/dependency_validator.py`.

## Phase 2: Execution Engine (User Story 1)

- [ ] T005 [US1] Create `TaskExecutor` class in `src/services/task_executor.py` with methods to execute shell commands.
- [ ] T006 [US1] Implement topological sort logic to determine execution order based on dependencies.
- [ ] T007 [US1] Write integration tests for `TaskExecutor` mocking subprocess calls in `tests/integration/test_executor.py`.
- [ ] T008 [US1] Implement `tm run-tasks` CLI command in `src/cli/tasks.py`.

## Phase 3: Status & Reporting (User Story 2)

- [ ] T009 [US2] Implement `ExecutionStatus` tracking (pending, running, success, failed).
- [ ] T010 [US2] Create `ConsoleReporter` to output real-time status to stdout with colors/spinners.
- [ ] T011 [US2] Write tests for the reporter output format.

## Phase 4: Configuration (User Story 3)

- [ ] T012 [US3] Add configuration options for "dry-run" and "parallel" execution in `TaskExecutor`.
- [ ] T013 [US3] Implement parallel execution logic using `asyncio` or `concurrent.futures`.
