# Tasks: Guided CLI Workflows

**Input**: `specs/004-guided-workflow/spec.md`

## Phase 1: Foundational

- [ ] T001 Create `src/lib/workflow_context.py` and implement the basic `WorkflowContextManager` class structure.
- [ ] T002 Create `docs/cli_workflow_map.md` to provide a static, human-readable overview of the workflows discovered.
- [ ] T003 Write unit tests for the initial `WorkflowContextManager` in `tests/unit/test_workflow_context.py` to verify state management.

## Phase 2: `guide-dev` Implementation (User Story 1)

- [ ] T003b Write unit tests for the guide logic in `tests/unit/test_cli_guides.py` (TDD).
- [ ] T004 Create a root `launch.py` wrapper and extend `setup/launch.py` to include the new `guide-dev` command.
- [ ] T005 Implement the `guide-dev` logic in `src/cli/guides.py`, using the `WorkflowContextManager` to guide the user based on their intent (app code vs. orchestration/CLI tools).
- [ ] T006 Add logic to `guide-dev` to detect the current Git branch and provide appropriate warnings if the user is not on `orchestration-tools` when attempting to edit orchestration tools or configs.
- [ ] T007 Write integration tests in `tests/integration/test_cli_guides.py` to simulate a user interacting with the `guide-dev` workflow.

## Phase 3: `guide-pr` Implementation (User Story 2)

- [ ] T008 Extend `setup/launch.py` to include the new `guide-pr` command.
- [ ] T009 Implement the `guide-pr` logic in `src/cli/guides.py`, guiding the user on whether to use `reverse_sync` or `git merge`.
- [ ] T010 Write integration tests in `tests/integration/test_cli_guides.py` to simulate a user interacting with the `guide-pr` workflow.

## Phase 4: Documentation & Polish

- [ ] T011 Update the main `README.md` to include instructions on how to use the new `guide-dev` and `guide-pr` commands.
- [ ] T012 Review all user-facing text in the guides for clarity and conciseness.
