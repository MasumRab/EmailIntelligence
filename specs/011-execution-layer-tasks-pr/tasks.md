# Tasks: Execution Layer with PR Resolution

**Input**: `specs/011-execution-layer-tasks-pr/spec.md`
**Prerequisites**: plan.md (required)

**Tests**: Test-Driven Development (TDD) is MANDATORY.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel
- **[Story]**: US1, US2, US3

## Phase 1: Model Extensions (User Story 2)

- [ ] T001 [P] [US2] Extend `Task` model in `src/models/task.py` to include `pr_issue_ids` list.
- [ ] T002 [P] [US2] Create `PRIssue` data model in `src/models/pr.py` (id, description, status).
- [ ] T003 [US2] Write tests for serializing/deserializing tasks with PR links in `tests/unit/test_task_pr_model.py`.

## Phase 2: Issue Tracking (User Story 2)

- [ ] T004 [US2] Create `PRIssueTracker` interface in `src/services/pr_tracker.py`.
- [ ] T005 [US2] Implement `GitHubPRIssueTracker` to fetch comments via API (using `PyGithub` or `gh` CLI).
- [ ] T006 [US2] Write integration tests for `GitHubPRIssueTracker` using mocks in `tests/integration/test_pr_tracker.py`.

## Phase 3: Validation Logic (User Story 3)

- [ ] T007 [US3] Create `ResolutionValidator` service in `src/services/validator.py`.
- [ ] T008 [US3] Implement logic to check if a specific "measurable change" (file mod) occurred.
- [ ] T009 [US3] Implement logic to re-run specific tests associated with a PR issue.

## Phase 4: Execution Integration (User Story 1)

- [ ] T010 [US1] Extend `TaskExecutor` to update `PRIssueTracker` upon task completion.
- [ ] T011 [US1] Implement reporting logic: "Task X completed -> Resolved Issue Y".
- [ ] T012 [US1] Create CLI command `tm run-pr-tasks --pr <ID>` to filter tasks by PR.
