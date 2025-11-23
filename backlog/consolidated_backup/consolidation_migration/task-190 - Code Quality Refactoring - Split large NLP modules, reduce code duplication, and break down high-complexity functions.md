---
assignee: []
created_date: 2025-10-25 04:50
dependencies: []
id: task-231
labels:
- refactoring
- quality
priority: low
status: To Do
title: Code Quality Refactoring - Split large NLP modules, reduce code duplication,
  and break down high-complexity functions
updated_date: 2025-10-28 08:54
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Address identified code quality issues: large modules, duplication, and high complexity functions
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Split smart_filters.py (1598 lines) into smaller focused components
- [ ] #2 Split smart_retrieval.py (1198 lines) into smaller modules
- [ ] #3 Reduce code duplication in AI engine modules (165-195 occurrences)
- [ ] #4 Break down setup_dependencies function (complexity: 21)
- [ ] #5 Refactor migrate_sqlite_to_json function (complexity: 17)
- [ ] #6 Refactor run function in email_filter_node.py (complexity: 16)
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
---
**Migration Context:** This task is part of the larger [Backend Migration to src/ (task-238)](backlog/tasks/task-238 - Backend-Migration-to-src.md) effort. Refer to the [Backend Migration Guide](docs/backend_migration_guide.md) for overall strategy and details.
<!-- SECTION:NOTES:END -->
