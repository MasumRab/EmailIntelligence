---
assignee: []
created_date: '2025-11-01'
dependencies:
- task-database-refactoring
id: task-223
labels:
- architecture
- database
- dependency-injection
- refactoring
priority: medium
status: Not Started
title: Complete Database Dependency Injection Alignment
updated_date: '2025-11-01'
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Complete the alignment of database dependency injection with the DatabaseConfig approach to ensure proper configuration management and dependency injection throughout the application.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Add DatabaseConfig class for proper dependency injection
- [ ] #2 Modify DatabaseManager.__init__ to accept DatabaseConfig instance
- [ ] #3 Make data directory configurable via environment variables
- [ ] #4 Add schema versioning and migration tracking capabilities
- [ ] #5 Implement security path validation using validate_path_safety and sanitize_path
- [ ] #6 Add backup functionality with separate backup directory
- [ ] #7 Update file path construction to use config-based paths
- [ ] #8 Add validation to ensure directories exist or can be created
- [ ] #9 Update DatabaseManager to support both new config-based initialization and legacy initialization
- [ ] #10 Create factory functions for proper dependency injection
- [ ] #11 Provide backward compatible get_db() function for existing code
- [ ] #12 Remove global singleton approach in favor of proper dependency injection
- [ ] #13 Test with existing code to ensure backward compatibility
- [ ] #14 Update documentation for new configuration options
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
This task focuses on completing the dependency injection alignment for the database layer. The goal is to ensure that the DatabaseManager properly supports dependency injection while maintaining backward compatibility with existing code that relies on the global singleton approach.
<!-- SECTION:NOTES:END -->