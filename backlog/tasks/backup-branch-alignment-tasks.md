# Backup Branch Alignment Tasks

## Overview
This document outlines the tasks required to align the `backup-branch` with the `scientific` branch before merging. The `backup-branch` contains significant architectural changes, particularly around the repository pattern and data source abstractions, that need to be aligned with the current state of the `scientific` branch.

## Key Differences Identified

### 1. Data Source Interface
- **Backup Branch**: Basic DataSource interface with core methods only
- **Scientific Branch**: Enhanced DataSource interface with additional methods:
  - `delete_email(email_id: int) -> bool`
  - `get_dashboard_aggregates() -> Dict[str, Any]`
  - `get_category_breakdown(limit: int = 10) -> Dict[str, int]`

### 2. Database Implementation
- **Backup Branch**: Basic JSON file storage implementation with:
  - Simple file paths
  - Basic initialization
  - Minimal error handling
- **Scientific Branch**: Enhanced implementation with:
  - Schema versioning and migration tracking
  - Security path validation using `validate_path_safety` and `sanitize_path`
  - Backup functionality with separate backup directory
  - Environment-configurable data directory via `DATA_DIR = os.environ.get("DATA_DIR", "data")`
  - DatabaseConfig class for proper dependency injection
  - Improved initialization with explicit schema management

### 3. Notmuch Implementation
- **Backup-Branch**: Mock implementation with print statements for all methods
- **Scientific Branch**: Functional NotmuchDataSource with:
  - Actual notmuch database integration
  - Proper query implementation
  - Content extraction from email parts
  - Tag-based category mapping
  - Implementation of all required DataSource methods including dashboard statistics

### 4. Repository Pattern
- Both branches have the same EmailRepository abstract class
- Both have DatabaseEmailRepository implementation
- The key difference is that the scientific branch's DataSource has more methods that need to be implemented

## Detailed Alignment Tasks

### Task 1: Update DataSource Interface (High Priority)
- [ ] Add the missing methods to the DataSource interface in backup-branch:
  - `delete_email(self, email_id: int) -> bool`
  - `get_dashboard_aggregates(self) -> Dict[str, Any]`
  - `get_category_breakdown(self, limit: int = 10) -> Dict[str, int]`

### Task 2: Update Database Implementation (High Priority)
- [ ] Add DatabaseConfig class for proper dependency injection
- [ ] Modify DatabaseManager.__init__ to accept DatabaseConfig instance
- [ ] Make data directory configurable via environment variables
- [ ] Add schema versioning and migration tracking capabilities
- [ ] Implement security path validation using validate_path_safety and sanitize_path
- [ ] Add backup functionality with separate backup directory
- [ ] Update file path construction to use config-based paths
- [ ] Add validation to ensure directories exist or can be created

### Task 3: Implement Notmuch DataSource (High Priority)
- [ ] Replace mock NotmuchDataSource with functional implementation
- [ ] Add notmuch database integration
- [ ] Implement proper query functionality for all DataSource methods
- [ ] Add content extraction from email parts
- [ ] Implement tag-based category mapping
- [ ] Add proper error handling and logging

### Task 4: Implement Dashboard Statistics Methods (High Priority)
- [ ] Implement `get_dashboard_aggregates()` in both DatabaseManager and NotmuchDataSource
- [ ] Implement `get_category_breakdown()` in both DatabaseManager and NotmuchDataSource
- [ ] Ensure proper data aggregation and calculation logic
- [ ] Add caching mechanisms where appropriate

### Task 5: Security Enhancements (High Priority)
- [ ] Integrate path safety validation from scientific branch
- [ ] Ensure all file operations are properly validated
- [ ] Add input sanitization for all user-provided data
- [ ] Implement proper error handling without exposing sensitive information

### Task 6: Dependency Injection Alignment (Medium Priority)
- [ ] Update DatabaseManager to support both new config-based initialization and legacy initialization
- [ ] Create factory functions for proper dependency injection
- [ ] Provide backward compatible get_db() function for existing code
- [ ] Remove global singleton approach in favor of proper dependency injection

### Task 7: Performance Monitoring Alignment (Medium Priority)
- [ ] Update performance monitoring to match scientific branch implementation
- [ ] Ensure compatibility with new repository pattern
- [ ] Add proper logging and metrics collection

### Task 8: Module and Route Integration (Medium Priority)
- [ ] Update module imports and registrations to match scientific branch
- [ ] Ensure dashboard routes are properly integrated with new data source
- [ ] Verify API endpoints work with enhanced DataSource interface

## Merge Strategy
1. **Phase 1**: Address high-priority alignment tasks (DataSource interface, security, Notmuch implementation)
2. **Phase 2**: Update database implementation with enhanced features (config, schema, backup, security)
3. **Phase 3**: Implement dashboard statistics functionality
4. **Phase 4**: Align dependency injection and performance monitoring
5. **Phase 5**: Final testing and validation

## Potential Conflicts
- The repository pattern in backup-branch may conflict with dashboard statistics implementation in scientific branch
- NotmuchDataSource implementations differ significantly between branches (mock vs functional)
- Database file path handling has different approaches (static vs environment-configurable)
- Performance monitoring systems have diverged
- Security implementations are different (minimal vs comprehensive)

## Testing Requirements
- All repository pattern implementations must be tested with both data source types
- Dashboard statistics functionality must work with new repository pattern
- Notmuch integration must be validated with actual notmuch database
- Security features must be verified after integration
- Performance monitoring must be validated with realistic workloads
- Backward compatibility must be maintained for existing code