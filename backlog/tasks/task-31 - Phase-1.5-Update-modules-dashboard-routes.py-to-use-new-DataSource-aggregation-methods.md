---
id: task-31
title: >-
  Phase 1.5: Update modules/dashboard/routes.py to use new DataSource
  aggregation methods
status: To Do
assignee: []
created_date: '2025-10-31 12:44'
labels: []
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Refactor the modular dashboard routes to use the new efficient DataSource aggregation methods instead of fetching all emails, implementing the consolidated dashboard logic
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Replace email fetching with DataSource.get_dashboard_aggregates()
- [ ] #2 Use DataSource.get_category_breakdown() for category stats
- [ ] #3 Implement time_saved and weekly_growth calculations
- [ ] #4 Update performance metrics handling
- [ ] #5 Maintain existing API contract while improving performance
<!-- AC:END -->
