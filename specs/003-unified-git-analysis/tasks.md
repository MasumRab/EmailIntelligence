# Tasks for Feature: Unified Git Analysis and Verification

This document outlines the implementation tasks for the unified `git-verifier` tool, consolidating the goals of features 001 and 002.

## Implementation Strategy

The implementation will follow a logical progression, starting with foundational elements, then building up the core analysis and verification capabilities as defined in the user stories. The project will strictly adhere to a Test-Driven Development (TDD) workflow. Tasks from previous plans are merged and de-duplicated here.

## Phase 1: Setup (Consolidated)

- [x] T001 Create project structure in `src/` with `models/`, `services/`, `cli/`, `lib/` directories, and `tests/` with `unit/`, `integration/`, `contract/` subdirectories.
- [x] T002 Create a `requirements.txt` file and add `GitPython` and `pytest`.
- [x] T003 Create a virtual environment and install dependencies from `requirements.txt`.

## Phase 2: Foundational (Consolidated)

- [x] T004 Implement a robust Git repository wrapper in `src/lib/git_wrapper.py` to handle repository initialization, commit iteration, and reflog access.

## Phase 3: Testing (TDD)

**Goal**: Write a comprehensive test suite before implementation.
**Independent Test Criteria**: All tests should fail initially and pass only after their corresponding features are implemented.

- [x] T005 [P] Write unit tests for the `git_wrapper` in `tests/unit/test_git_wrapper.py`.
- [x] T006 [P] Write unit tests for the unified `analysis_service` in `tests/unit/test_analysis_service.py`, covering narrative synthesis, rebase detection, and verification logic.
- [x] T007 [P] Write integration tests for the `git-verifier` CLI and its sub-commands (`analyze`, `detect-rebased`, `verify`) in `tests/integration/test_cli.py`.
- [x] T008 [P] Define contract tests in `tests/contract/test_cli_contracts.py` to validate the CLI's behavior against `contracts/cli-contracts.md`.

## Phase 4: Core Implementation (US1, US4)

**Goal**: Implement the core analysis engine and the unified CLI tool.
**Independent Test Criteria**: The `git-verifier analyze` command should generate a synthesized narrative for a given commit range.

- [x] T009 [US1] Implement the data models (`ActionNarrative`, `IntentReport`, `VerificationResult`) in `src/models/unified_analysis.py`.
- [x] T010 [US1] Implement the core narrative synthesis logic within a new `src/services/analysis_service.py`.
- [x] T011 [US4] Implement the main CLI entry point for `git-verifier` and the `analyze` sub-command in `src/cli/main.py`.

## Phase 5: Rebase Detection (US2)

**Goal**: Add the capability to detect rebased branches.
**Independent Test Criteria**: The `git-verifier detect-rebased` command should correctly identify branches that have been rebased.

- [x] T012 [US2] Implement the rebase detection logic in `src/services/analysis_service.py`, using the reflog access provided by the `git_wrapper`.
- [ ] T013 [US2] Implement the `detect-rebased` sub-command in `src/cli/main.py`.

## Phase 6: Verification (US3)

**Goal**: Implement the post-merge verification functionality.
**Independent Test Criteria**: The `git-verifier verify` command should correctly compare a merged branch against a pre-generated Intent Report.

- [ ] T014 [US3] Implement the verification logic in `src/services/analysis_service.py` to compare an `IntentReport` with the state of a merged branch.
- [ ] T015 [US3] Implement the `verify` sub-command in `src/cli/main.py`.

## Final Phase: Polish & Cross-Cutting Concerns (Consolidated)

- [ ] T016 [P] Implement robust error handling and user-friendly messages across all `git-verifier` sub-commands in `src/cli/main.py`.
- [ ] T017 [P] Add user-friendly progress indicators for long-running operations like analysis and verification.
- [ ] T018 [P] Refine all output formats (`text`, `json`, `md`) for clarity and correctness.

## Dependencies

- All implementation phases (**4, 5, 6**) depend on **Phase 2 (Foundational)** and **Phase 3 (Testing)**.
- **Phase 6 (Verification)** depends on the `IntentReport` generated in **Phase 4 (Core Implementation)**.

## Parallel Execution Examples

- Within **Phase 3**, all testing tasks (T005-T008) can be performed in parallel.
- In the **Final Phase**, all polishing tasks (T016-T018) can be done in parallel.
