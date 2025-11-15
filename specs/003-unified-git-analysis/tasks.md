# Tasks for Feature: Unified Git Analysis and Verification

This document outlines the implementation tasks for the unified `git-verifier` tool, consolidating the goals of features 001 and 002.

## Implementation Strategy

The implementation will follow a logical progression, starting with foundational elements, then building up the core analysis and verification capabilities as defined in the user stories. The project will strictly adhere to a Test-Driven Development (TDD) workflow. Tasks from previous plans are merged and de-duplicated here.

## Phase 1: Setup (Consolidated)

- [ ] T001 Create project structure in `src/` with `models/`, `services/`, `cli/`, `lib/` directories, and `tests/` with `unit/`, `integration/`, `contract/` subdirectories.
- [ ] T002 Create a `requirements.txt` file and add `GitPython` and `pytest`.
- [ ] T003 Create a virtual environment and install dependencies from `requirements.txt`.

## Phase 2: Foundational (Consolidated)

- [ ] T004 Implement a robust Git repository wrapper in `src/lib/git_wrapper.py` to handle repository initialization, commit iteration, and reflog access.
- [ ] T005 [P] Write unit tests for the `git_wrapper` in `tests/unit/test_git_wrapper.py`.

## Phase 3: User Story 4 - Unified Tool Access (Priority: P1)

**Goal**: Ensure the tool is easy to adopt and integrate into any developer's workflow.
**Independent Test Criteria**: The tool is installed and the `git-verifier` command is available and executes successfully from any branch.

- [ ] T006 [US4] Implement the main CLI entry point for `git-verifier` in `src/cli/main.py`.
- [ ] T007 [P] [US4] Define contract tests in `tests/contract/test_cli_contracts.py` to validate the CLI's behavior against `contracts/cli-contracts.md`.
- [ ] T008 [P] [US4] Write integration tests for the `git-verifier` CLI and its sub-commands in `tests/integration/test_cli.py`.

## Phase 4: User Story 1 - Generate Action Narrative (Priority: P1)

**Goal**: Analyze any branch or commit range to generate a clear, synthesized narrative of the actions taken.
**Independent Test Criteria**: The `git-verifier analyze` command generates an accurate and descriptive synthesized narrative for a given commit range.

- [ ] T009 [US1] Implement the data models (`ActionNarrative`, `IntentReport`, `VerificationResult`) in `src/models/unified_analysis.py`.
- [ ] T010 [US1] Implement the core narrative synthesis logic within `src/services/analysis_service.py`.
- [ ] T011 [US1] Implement the `analyze` sub-command in `src/cli/main.py`.
- [ ] T012 [P] [US1] Write unit tests for the unified `analysis_service` covering narrative synthesis logic in `tests/unit/test_analysis_service.py`.

## Phase 5: User Story 2 - Identify Rebased Branches & Generate Intent Report (Priority: P2)

**Goal**: Automatically identify rebased branches and generate a pre-merge "Intent Report" for them.
**Independent Test Criteria**: The `git-verifier detect-rebased` command correctly identifies rebased branches and the `analyze --report` command generates a comprehensive Intent Report.

- [ ] T013 [US2] Implement the rebase detection logic in `src/services/analysis_service.py`, using the reflog access provided by the `git_wrapper`.
- [ ] T014 [US2] Implement the `detect-rebased` sub-command in `src/cli/main.py`.
- [ ] T015 [P] [US2] Write unit tests for the unified `analysis_service` covering rebase detection logic in `tests/unit/test_analysis_service.py`.

## Phase 6: User Story 3 - Verify Post-Merge Integrity (Priority: P2)

**Goal**: Compare the final merged state against the pre-merge "Intent Report" to ensure no changes were lost or altered.
**Independent Test Criteria**: The `git-verifier verify` command correctly compares a merged branch against a pre-generated Intent Report and highlights discrepancies.

- [ ] T016 [US3] Implement the verification logic in `src/services/analysis_service.py` to compare an `IntentReport` with the state of a merged branch.
- [ ] T017 [US3] Implement the `verify` sub-command in `src/cli/main.py`.
- [ ] T018 [P] [US3] Write unit tests for the unified `analysis_service` covering verification logic in `tests/unit/test_analysis_service.py`.

## Final Phase: Polish & Cross-Cutting Concerns

- [ ] T019 [P] Implement robust error handling and user-friendly messages across all `git-verifier` sub-commands in `src/cli/main.py`.
- [ ] T020 [P] Add user-friendly progress indicators for long-running operations like analysis and verification.
- [ ] T021 [P] Refine all output formats (`text`, `json`, `md`) for clarity and correctness.
- [ ] T022 [P] Implement and configure code coverage reporting to ensure minimum 90% overall coverage and 100% for critical paths.
- [ ] T023 [P] Implement and verify secure coding practices, including input validation, secure data handling, and vulnerability prevention.
- [ ] T024 [P] Integrate automated security scanning into the CI/CD pipeline for this feature.
- [ ] T025 [P] Integrate automated performance validation into the CI/CD pipeline for this feature.
- [ ] T026 [P] Implement anonymization logic for secrets and PII before sending data to external LLMs.
- [ ] T027 [P] Implement file input/output for IntentReport in `analyze` and `verify` commands.

## Dependencies

*   Phase 2 (Foundational) must be completed before any User Story Phase.
*   Phase 3 (US4) is foundational for all other CLI commands.
*   Phase 4 (US1) is foundational for IntentReport generation, which is used by US2 and US3.
*   Phase 5 (US2) depends on Phase 4.
*   Phase 6 (US3) depends on Phase 4.

## Parallel Execution Examples

*   Within Phase 2, T004 and T005 can be done in parallel.
*   Within Phase 3, T007 and T008 can be done in parallel.
*   Within Phase 4, T010 and T012 can be done in parallel.
*   Within Phase 5, T013 and T015 can be done in parallel.
*   Within Phase 6, T016 and T018 can be done in parallel.
*   Within the Final Phase, T019-T027 can be done in parallel.