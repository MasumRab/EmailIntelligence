# Backup Branch Alignment Tasks

## Overview
This document outlines the tasks required to align the `backup-branch` with the `scientific` branch before merging. The `backup-branch` contains significant architectural changes, particularly around the repository pattern and data source abstractions, that need to be aligned with the current state of the `scientific` branch.

## Key Differences Identified

### 1. Data Source Interface
- **Backup Branch**: Basic DataSource interface with core methods
- **Scientific Branch**: Enhanced DataSource interface with additional methods:
  - `delete_email(email_id: int) -> bool`
  - `get_dashboard_aggregates() -> Dict[str, Any]`
  - `get_category_breakdown(limit: int = 10) -> Dict[str, int]`

### 2. Database Implementation
- **Backup Branch**: Basic JSON file storage implementation
- **Scientific Branch**: Enhanced implementation with:
  - Schema versioning and migration tracking
  - Security path validation
  - Backup functionality
  - Environment-configurable data directory
  - Additional performance monitoring

### 3. Notmuch Implementation
- **Backup Branch**: Mock implementation of NotmuchDataSource
- **Scientific Branch**: Functional NotmuchDataSource with actual database integration

### 4. Repository Pattern
- **Backup Branch**: Basic Repository pattern with EmailRepository abstract class
- **Scientific Branch**: Same Repository pattern but needs to be updated to match the enhanced DataSource interface

## Alignment Tasks

### Task 1: Update DataSource Interface (High Priority)
- [ ] Add the missing methods to the DataSource interface in backup-branch:
  - delete_email()
  - get_dashboard_aggregates()
  - get_category_breakdown()

### Task 2: Update Repository Implementation (High Priority)
- [ ] Update DatabaseEmailRepository to implement the new DataSource methods
- [ ] Ensure the repository pattern remains consistent with the enhanced DataSource interface

### Task 3: Integrate Enhanced Database Features (Medium Priority)
- [ ] Add schema versioning and migration tracking
- [ ] Implement security path validation
- [ ] Add backup functionality
- [ ] Make data directory environment-configurable

### Task 4: Enhance Notmuch Implementation (Medium Priority)
- [ ] Replace mock NotmuchDataSource with functional implementation
- [ ] Integrate proper notmuch database functionality

### Task 5: Merge Dashboard Statistics Implementation (Medium Priority)
- [ ] Integrate the dashboard aggregation features from scientific branch
- [ ] Ensure compatibility with repository pattern

### Task 6: Performance Monitoring Alignment (Low Priority)
- [ ] Update performance monitoring to match scientific branch implementation
- [ ] Ensure compatibility with new repository pattern

### Task 7: Security Enhancements (High Priority)
- [ ] Integrate path safety validation from scientific branch
- [ ] Ensure all file operations are properly validated

### Task 8: Module and Route Integration (Medium Priority)
- [ ] Update module imports and registrations to match scientific branch
- [ ] Ensure dashboard routes are properly integrated with new data source

## Merge Strategy
1. **Phase 1**: Address high-priority alignment tasks (DataSource interface, security)
2. **Phase 2**: Update repository implementation to match new interface
3. **Phase 3**: Integrate enhanced database features
4. **Phase 4**: Replace mock implementations with functional ones
5. **Phase 5**: Final testing and validation

## Potential Conflicts
- The repository pattern in backup-branch may conflict with dashboard statistics implementation in scientific branch
- NotmuchDataSource implementations differ significantly between branches
- Database file path handling has different approaches
- Performance monitoring systems have diverged

## Testing Requirements
- All repository pattern implementations must be tested with both data source types
- Dashboard statistics functionality must work with new repository pattern
- Notmuch integration must be validated
- Security features must be verified after integration