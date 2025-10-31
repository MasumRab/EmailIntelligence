---
id: task-33
title: >-
  Phase 1.7: Implement time_saved calculation logic (2 minutes per auto-labeled
  email) in dashboard routes
status: To Do
assignee: []
created_date: '2025-10-31 13:50'
updated_date: '2025-10-31 14:52'
labels: []
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Implement the time_saved calculation logic in the consolidated dashboard routes using the formula of 2 minutes saved per auto-labeled email, matching the legacy implementation
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Add time_saved calculation function to dashboard routes
- [ ] #2 Implement formula: time_saved_minutes = auto_labeled * 2
- [ ] #3 Format time_saved as 'Xh Ym' string format
- [ ] #4 Handle edge cases (zero auto-labeled emails)
- [ ] #5 Add unit tests for time calculation logic
- [ ] #6 Ensure calculation matches legacy implementation
<!-- AC:END -->
