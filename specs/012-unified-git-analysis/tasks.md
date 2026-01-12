# Tasks: Unified Git Analysis

**Input**: `specs/012-unified-git-analysis/spec.md`
**Prerequisites**: plan.md (required)

**Tests**: Test-Driven Development (TDD) is MANDATORY.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel
- **[Story]**: US1, US2, US3, US4, FND (Foundational)

## Phase 1: Setup (Consolidated)

- [ ] T001 [P] [FND] Create project structure in `src/` with `models/`, `services/`, `cli/`, `lib/` directories.
- [ ] T002 [P] [FND] Create a `requirements.txt` file and add `GitPython` and `pytest`.
- [ ] T003 [FND] Create a virtual environment and install dependencies from `requirements.txt`.

## Phase 2: Foundational (Consolidated)

- [ ] T004 [FND] Implement a robust Git repository wrapper in `src/lib/git_wrapper.py`.
- [ ] T005 [P] [FND] Write unit tests for the `git_wrapper` in `tests/unit/test_git_wrapper.py`.

## Phase 3: User Story 4 - Unified Tool Access (Priority: P1)

- [ ] T006 [US4] Implement the main CLI entry point for `git-verifier` in `src/cli/main.py`.
- [ ] T007 [P] [US4] Define contract tests in `tests/contract/test_cli_contracts.py`.
- [ ] T008 [P] [US4] Write integration tests for the `git-verifier` CLI in `tests/integration/test_cli.py`.

## Phase 4: User Story 1 - Generate Action Narrative (Priority: P1)

- [ ] T009 [US1] Implement the data models (`ActionNarrative`, `IntentReport`, `VerificationResult`) in `src/models/unified_analysis.py`.
- [ ] T010 [US1] Implement the core narrative synthesis logic within `src/services/analysis_service.py`.
- [ ] T011 [US1] Implement the `analyze` sub-command in `src/cli/main.py`.
- [ ] T012 [P] [US1] Write unit tests for the unified `analysis_service` in `tests/unit/test_analysis_service.py`.

## Phase 5: User Story 2 - Identify Rebased Branches (Priority: P2)

- [ ] T013 [US2] Implement the rebase detection logic in `src/services/analysis_service.py`.
- [ ] T014 [US2] Implement the `detect-rebased` sub-command in `src/cli/main.py`.
- [ ] T015 [P] [US2] Write unit tests for the unified `analysis_service` covering rebase detection.

## Phase 6: User Story 3 - Verify Post-Merge Integrity (Priority: P2)

- [ ] T016 [US3] Implement the verification logic in `src/services/analysis_service.py`.
- [ ] T017 [US3] Implement the `verify` sub-command in `src/cli/main.py`.
- [ ] T018 [P] [US3] Write unit tests for the unified `analysis_service` covering verification.

## Phase 7: Polish & Cross-Cutting Concerns

- [ ] T019 [P] [FND] Implement robust error handling and user-friendly messages.
- [ ] T020 [P] [FND] Add user-friendly progress indicators.
- [ ] T021 [P] [FND] Refine all output formats (`text`, `json`, `md`).
- [ ] T022 [P] [FND] Implement and configure code coverage reporting.
- [ ] T023 [P] [FND] Implement and verify secure coding practices.
- [ ] T024 [P] [FND] Integrate automated security scanning.
- [ ] T025 [P] [FND] Integrate automated performance validation.
- [ ] T026 [P] [FND] Implement anonymization logic for secrets.
- [ ] T027 [P] [FND] Implement file input/output for IntentReport.
