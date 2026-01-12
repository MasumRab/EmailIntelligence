# Tasks: Agent Context Control

**Input**: `specs/009-agent-context-control/spec.md`
**Prerequisites**: plan.md (required)

**Tests**: Test-Driven Development (TDD) is MANDATORY.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel
- **[Story]**: US1, US2

## Phase 1: Core Models (User Story 1)

- [ ] T001 [P] [US1] Define `ContextProfile` model in `src/models/context.py` (id, matching_rules, active_rules).
- [ ] T002 [P] [US1] Implement `ContextDetector` in `src/services/context_detector.py` to identify current branch type.
- [ ] T003 [US1] Write unit tests for `ContextDetector` with various branch name patterns in `tests/unit/test_context_detector.py`.

## Phase 2: Context Manager (User Story 1)

- [ ] T004 [US1] Create `ContextManager` class in `src/services/context_manager.py`.
- [ ] T005 [US1] Implement logic to load profiles from `.context-control/profiles/`.
- [ ] T006 [US1] Implement `get_active_context()` method that returns the correct profile for current state.
- [ ] T007 [US1] Write integration tests simulating branch switches in `tests/integration/test_context_manager.py`.

## Phase 3: CLI Integration (User Story 2)

- [ ] T008 [US2] Implement `tm context show` CLI command to display current active context.
- [ ] T009 [US2] Implement `tm context validate` to check if current environment matches expected context.
