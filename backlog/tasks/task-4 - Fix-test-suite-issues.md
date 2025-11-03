---
id: task-4
title: Fix test suite issues
status: Done
assignee:
  - '@masum'
created_date: '2025-10-25 04:46'
updated_date: '2025-11-03 01:41'
labels:
  - testing
  - ci
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Address failing tests and test configuration problems in the CI pipeline
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Fix pytest-asyncio configuration
- [x] #2 Resolve test environment issues
- [x] #3 Update test dependencies
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Fixed test suite issues: installed missing dependencies (pydantic-settings, PyJWT, scikit-learn, notmuch, bleach), resolved import errors (ActionItem, SmartFilterManager, AdvancedAIEngine, db_manager, BaseAppException, ROOT_DIR), fixed IndentationErrors in test files. Test collection now succeeds for main tests, with only worktree notmuch issues remaining.
<!-- SECTION:NOTES:END -->
