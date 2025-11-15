# Tasks: Toolset Additive Analysis

**Input**: Design documents from `/specs/001-toolset-additive-analysis/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Test-Driven Development (TDD) is MANDATORY for all new feature development and bug fixes. Comprehensive testing standards, including unit, integration, and end-to-end tests (using pytest), MUST be applied. Tests MUST be written and approved before implementation, following the Red-Green-Refactor cycle, and are critical for validating smart agent outputs. All tests must pass in CI/CD pipeline before code can be merged. Test naming must be descriptive and clearly indicate what behavior is being tested and expected outcomes.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup

**Purpose**: Establish the foundational environment, branching adherence, and agent integration points, strictly following Principle IX (Branching and Orchestration Strategy).

- [ ] T001 Create project directory structure for `src/models`, `src/services`, `src/cli`, `src/lib`, `tests/unit`, `tests/integration`, `tests/contract`.
- [ ] T002 Initialize Git repository (if not already done) and create `001-toolset-additive-analysis` branch.
- [ ] T003 Set up Python 3.12+ virtual environment and install `GitPython` and `pytest`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented, adhering to Principle V (Critical Thinking and Simplicity).

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [ ] T004 Implement `GitWrapper` utility for Git repository interaction in `src/lib/git_wrapper.py`.
- [ ] T005 Implement `ToolsetComponent` data model in `src/models/toolset_component.py`.
- [ ] T006 Implement `Dependency` data model in `src/models/dependency.py`.
- [ ] T007 Implement `IntegrationPoint` data model in `src/models/integration_point.py`.
- [ ] T008 Implement `AnalysisReport` data model in `src/models/analysis_report.py`.
- [ ] T009 Implement base `FileParser` interface/abstract class in `src/lib/file_parser.py`.

#### Security and Privacy (NFR-SEC-001) - Foundational
- [ ] T010 Implement sensitive data anonymization before processing/reporting in `src/services/analysis_service.py`.
- [ ] T011 Implement secure storage and transmission of analysis data (if applicable, e.g., for output files) in `src/lib/report_generator.py`.
- [ ] T012 Write unit tests for security and privacy measures, including secure file handling, in `tests/unit/test_security_privacy.py`.

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel.

---

## Phase 3: User Story 1 - Analyze Toolset for Additive Integration (Priority: P1) 🎯 MVP

**Goal**: As a developer, I want to analyze the existing toolset within a Git repository and its local branches to understand its components, dependencies, and functionalities, so that I can identify optimal points for additive feature integration without breaking existing functionality.

**Independent Test**: Can be tested by providing a repository with a known toolset and verifying that the analysis output accurately describes the toolset's structure and potential integration points.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T013 [P] [US1] Write unit tests for `PythonScriptParser` in `tests/unit/test_python_script_parser.py`.
- [ ] T014 [P] [US1] Write unit tests for `ShellScriptParser` in `tests/unit/test_shell_script_parser.py`.
- [ ] T015 [P] [US1] Write unit tests for `ConfigParser` in `tests/unit/test_config_parser.py`.
- [ ] T016 [P] [US1] Write unit tests for `DependencyManifestParser` in `tests/unit/test_dependency_manifest_parser.py`.
- [ ] T017 [P] [US1] Write unit tests for `BranchFileFinder` in `tests/unit/test_branch_file_finder.py`.
- [ ] T018 [US1] Write unit tests for `DependencyAnalyzer` in `tests/unit/test_dependency_analyzer.py`.
- [ ] T019 [US1] Write unit tests for `IntegrationRecommender` in `tests/unit/test_integration_recommender.py`.
- [ ] T020 [US1] Write unit tests for `ReportGenerator` in `tests/unit/test_report_generator.py`.
- [ ] T021 [US1] Write unit tests for `AnalysisService` in `tests/unit/test_analysis_service.py`.
- [ ] T022 [US1] Write unit tests for edge case handling in `tests/unit/test_edge_cases.py`.
- [ ] T023 [P] [US1] Create contract test for `git-verifier analyze-toolset` CLI command in `tests/contract/test_cli_contracts.py`.
- [ ] T024 [US1] Write integration tests for `git-verifier analyze-toolset` in `tests/integration/test_cli.py`.

### Implementation for User Story 1

#### File Parsing (FR-001, FR-006)
- [ ] T025 [P] [US1] Implement `PythonScriptParser` using `ast` module in `src/lib/python_script_parser.py`.
- [ ] T026 [P] [US1] Implement `ShellScriptParser` using regex/string parsing in `src/lib/shell_script_parser.py`.
- [ ] T027 [P] [US1] Implement `ConfigParser` for common config files (e.g., JSON, YAML) in `src/lib/config_parser.py`.
- [ ] T028 [P] [US1] Implement `DependencyManifestParser` for `requirements.txt`, `pyproject.toml`, `uv.lock` in `src/lib/dependency_manifest_parser.py`.
- [ ] T029 [P] [US1] Implement `BranchFileFinder` to locate files in `00*` prefixed branches in `src/lib/branch_file_finder.py`.
- [ ] T030 [US1] Implement `FileParserFactory` to select appropriate parser based on file type in `src/lib/file_parser_factory.py`.

#### Dependency Identification (FR-002)
- [ ] T031 [US1] Implement `DependencyAnalyzer` to build dependency graph from parsed components in `src/services/dependency_analyzer.py`.

#### Integration Point Determination (FR-003)
- [ ] T032 [US1] Implement `IntegrationRecommender` to determine integration points in `src/services/integration_recommender.py`.

#### Report Generation (FR-004)
- [ ] T033 [US1] Implement `ReportGenerator` for structured CLI output and JSON output in `src/lib/report_generator.py`.

#### Core Analysis Service (FR-005)
- [ ] T034 [US1] Implement `AnalysisService` to orchestrate file parsing, dependency analysis, and recommendation generation in `src/services/analysis_service.py`.

#### CLI Interface (FR-004, User Request)
- [ ] T035 [US1] Implement `analyze-toolset` CLI command in `src/cli/main.py`.
- [ ] T036 [US1] Implement helpful user CLI interface guiding user how to use in `src/cli/main.py`.

#### Edge Case Handling (Edge Cases Section)
- [ ] T037 [US1] Implement edge case detection and reporting (undocumented toolset, external dependencies, conflicting dependencies) in `src/services/analysis_service.py`.
- [ ] T038 [US1] Write unit tests for edge case handling in `tests/unit/test_edge_cases.py`.

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently.

---

## Final Phase: Polish & Cross-Cutting Concerns

**Purpose**: Tasks that are not directly tied to a specific user story but are necessary for the overall project.

- [ ] T039 Review and refine performance of file parsing and dependency graph generation.
- [ ] T040 Implement caching mechanisms for performance optimization.
- [ ] T041 Update `README.md` with usage instructions and examples.
- [ ] T042 Integrate automated security scanning into CI/CD pipeline.
- [ ] T043 Integrate performance validation into CI/CD pipeline.
- [ ] T044 Ensure 90% overall code coverage, 100% for critical paths.
- [ ] T045 Define metrics and methodology for tracking resolution rate of additive integration issues (for SC-005).
- [ ] T046 Implement a mechanism to collect and analyze data on issue resolution post-feature deployment (for SC-005).
- [ ] T047 Establish baseline CI/CD pipeline failure rate for additive feature integrations (for SC-006).
- [ ] T048 Implement CI/CD metrics collection and reporting for failure rates (for SC-006).
- [ ] T049 Establish baseline for security vulnerabilities introduced by additive feature integrations (for SC-007).
- [ ] T050 Implement security vulnerability metrics collection and reporting (for SC-007).