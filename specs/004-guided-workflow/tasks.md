# Tasks: Guided CLI Workflows

**Input**: `specs/004-guided-workflow/spec.md`
**Prerequisites**: plan.md (required)

**Tests**: Test-Driven Development (TDD) is MANDATORY.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel
- **[Story]**: US1, US2

## Phase 1: Foundational

- [x] T001 [P] [US1] Create `src/lib/workflow_context.py` and implement the basic `WorkflowContextManager` class structure.
- [x] T002 [P] [US1] Create `docs/cli_workflow_map.md` to provide a static, human-readable overview of the workflows discovered.
- [x] T003 [US1] Write unit tests for the initial `WorkflowContextManager` in `tests/unit/test_workflow_context.py` to verify state management.

## Phase 2: `guide-dev` Implementation (User Story 1)

- [x] T020 [P] [US1] Create `dev.py` in the repository root as the primary developer entry point.
- [ ] T004 [US1] Create standalone module `src/cli/guides/dev_guide.py` with a `main()` entry point, called by `dev.py`.
- [ ] T005 [US1] Implement the logic for the `guide-dev` command within the standalone module.
- [ ] T006 [US1] Add Git branch detection and safety warnings to `guide-dev`.
- [ ] T019 [P] [US1] Integrate `scripts/stash_manager_optimized.sh` into `WorkflowContextManager`.
- [ ] T007 [US1] Write integration tests for `python dev.py guide-dev`.

## Phase 3: Scientific Integration (Unified Logic)

- [x] T013 [P] [US3] Port `GitConflictDetector` and `ConstitutionalEngine` logic from `scientific` branch (Completed via Merge).
- [ ] T021 [P] [US3] Implement `GitWorktreeRunner` in `src/core/git/worktree.py` as a Python Context Manager (inspired by `git-worktree-runner`) to safely manage ephemeral worktrees.
- [ ] T014 [P] [US3] Wire up the migrated engines to `dev.py` commands (`analyze`, `resolve`).
- [ ] T015 [P] [US3] Create `requirements-guides.txt` for specific dependencies needed by the guides (e.g., PyYAML).
- [ ] T016 [US3] Add unit tests for the migrated engines ensuring they work in isolation.

## Phase 4: `guide-pr` Implementation (User Story 2, 3, 4)

- [ ] T008 [US2] Create standalone module `src/cli/guides/pr_guide.py`, called by `dev.py`.
- [ ] T009 [US2] Implement the logic for the `guide-pr` command routing.
- [ ] T017 [US3] Integrate `Analyze` and `Resolve` logic into `guide-pr`.
- [ ] T018 [US4] Implement `RebasePlanner` logic within `guide-pr`.
- [ ] T010 [US2] Write integration tests for `python dev.py guide-pr`.

## Phase 5: Documentation & Polish

- [ ] T011 [P] [US1] Update the main `README.md` to include instructions on how to use the new `guide-dev` and `guide-pr` commands.
- [ ] T012 [P] [US1] Review all user-facing text in the guides for clarity and conciseness.