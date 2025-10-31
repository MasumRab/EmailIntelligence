---
id: task-32
title: >-
  Phase 1.6: Add authentication support to dashboard routes using
  get_current_active_user dependency
status: To Do
assignee: []
created_date: '2025-10-31 13:50'
updated_date: '2025-10-31 14:51'
labels: []
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Implement authentication support in the consolidated dashboard routes using the get_current_active_user dependency to enable user-specific dashboard data and access control
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Import get_current_active_user from src.core.auth
- [ ] #2 Add current_user parameter to get_dashboard_stats route
- [ ] #3 Implement user-specific data filtering if needed
- [ ] #4 Add proper error handling for authentication failures
- [ ] #5 Update route documentation to reflect authentication requirements
- [ ] #6 Test authentication integration with existing auth system
<!-- AC:END -->
