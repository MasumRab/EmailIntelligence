# Task: Global State Management Refactoring

## Priority
HIGH

## Description
Refactor global state management in database.py to use proper dependency injection.

## Issue
Several TODO comments about global state management in database.py.

## Requirements
1. Implement proper dependency injection for database manager instance
2. Remove global state where possible
3. Ensure thread safety for shared resources
4. Maintain backward compatibility during transition

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Implement proper dependency injection for database manager instance
- [ ] #2 Remove global state where possible
- [ ] #3 Ensure thread safety for shared resources
- [ ] #4 Maintain backward compatibility during transition
<!-- AC:END -->

## Estimated Effort
12 hours

## Dependencies
None

## Related Files
- src/core/database.py
- src/core/factory.py
- All files that use database manager

## Implementation Notes
- Review all TODO comments in database.py
- Implement proper singleton pattern with dependency injection
- Ensure thread-safe initialization of shared resources
- Update factory to provide properly scoped instances