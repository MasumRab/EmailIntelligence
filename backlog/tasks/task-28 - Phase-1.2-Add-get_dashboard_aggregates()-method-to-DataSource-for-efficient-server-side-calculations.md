---
id: task-28
title: >-
  Phase 1.2: Add get_dashboard_aggregates() method to DataSource for efficient
  server-side calculations
status: To Do
assignee: []
created_date: '2025-10-31 12:43'
labels: []
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Implement get_dashboard_aggregates() method in DataSource interface to provide efficient server-side calculations for total_emails, auto_labeled, categories_count, unread_count, and weekly_growth metrics
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Add get_dashboard_aggregates() method signature to DataSource interface
- [ ] #2 Implement method in all DataSource implementations (database, notmuch)
- [ ] #3 Return aggregated statistics as dictionary with all required fields
- [ ] #4 Add proper error handling and logging
- [ ] #5 Create unit tests for the new method
<!-- AC:END -->
