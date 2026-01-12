# Tasks: Guided CLI Workflows

**Input**: `specs/004-guided-workflow/spec.md`
**Prerequisites**: plan.md (required)

**Tests**: Test-Driven Development (TDD) is MANDATORY.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel
- **[Story]**: US1, US2

## Phase 1: Foundational

- [ ] T001 [P] [US1] Create `src/lib/workflow_context.py` and implement the basic `WorkflowContextManager` class structure.
- [ ] T002 [P] [US1] Create `docs/cli_workflow_map.md` to provide a static, human-readable overview of the workflows discovered.
- [ ] T003 [US1] Write unit tests for the initial `WorkflowContextManager` in `tests/unit/test_workflow_context.py` to verify state management.

## Phase 2: `guide-dev` Implementation (User Story 1)

- [ ] T004 [US1] Extend `launch.py` to include a new `guide-dev` command.
- [ ] T005 [US1] Implement the logic for the `guide-dev` command, using the `WorkflowContextManager` to guide the user based on their intent (app code vs. orchestration code).
- [ ] T006 [US1] Add logic to `guide-dev` to detect the current Git branch and provide appropriate warnings if the user is not on `orchestration-tools` when attempting to edit managed files.
- [ ] T007 [US1] Write integration tests in `tests/integration/test_cli_guides.py` to simulate a user interacting with the `guide-dev` workflow.

## Phase 3: `guide-pr` Implementation (User Story 2)

- [ ] T008 [US2] Extend `launch.py` to include the new `guide-pr` command.
- [ ] T009 [US2] Implement the logic for the `guide-pr` command, guiding the user on whether to use `reverse_sync` or `git merge`.
- [ ] T010 [US2] Write integration tests in `tests/integration/test_cli_guides.py` to simulate a user interacting with the `guide-pr` workflow.

## Phase 4: Documentation & Polish

- [ ] T011 [P] [US1] Update the main `README.md` to include instructions on how to use the new `guide-dev` and `guide-pr` commands.
- [ ] T012 [P] [US1] Review all user-facing text in the guides for clarity and conciseness.