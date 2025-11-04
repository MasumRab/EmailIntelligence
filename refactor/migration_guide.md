# Migration Guide: Backend Refactoring

## Overview
This guide provides instructions for migrating from the legacy backend architecture to the new refactored architecture. The migration maintains full backward compatibility while providing improved performance, maintainability, and extensibility.

## Architecture Changes Summary

### Before (Legacy)
- Monolithic DatabaseManager (700+ lines)
- Mixed concerns in main application
- Inconsistent service patterns
- Scattered UI components

### After (Refactored)
- Modular database components with clear responsibilities
- Separated UI components in dedicated modules
- Standardized service layer with consistent patterns
- Modern API routing with proper error handling

## Migration Steps

### 1. Update Import Statements

#### Legacy Imports
```python
from backend.python_backend.database import DatabaseManager
from backend.python_backend.services.email_service import EmailService
```

#### New Imports
```python
from src.core.database import DatabaseManager
from src.core.services.email_service import EmailService
```

### 2. Update API Endpoint Usage

#### Legacy Endpoints
```
GET /api/emails
POST /api/emails
GET /api/categories
```

#### New Endpoints (Backward Compatible)
```
GET /api/v1/emails
POST /api/v1/emails
GET /api/v1/categories
```

The legacy endpoints continue to work but should be migrated to the new versioned API.

### 3. Service Layer Usage

#### Legacy Service Usage
```python
# Direct database access in some cases
db = await get_db()
emails = await db.get_emails()
```

#### New Service Usage
```python
# Standardized service pattern
email_service = EmailService()
result = await email_service.get_all_emails()
if result.success:
    emails = result.data
```

### 4. Error Handling Updates

#### Legacy Error Handling
```python
try:
    # operation
    pass
except Exception as e:
    # generic error handling
    pass
```

#### New Error Handling
```python
try:
    result = await service.operation()
    if result.success:
        data = result.data
    else:
        # Handle specific error codes
        if result.error_code == "INVALID_INPUT":
            # Handle validation error
            pass
except EmailNotFoundException:
    # Handle specific exception
    pass
```

## Backward Compatibility

All existing functionality remains available through the legacy API endpoints. However, new features and improvements will only be available through the new API.

### Legacy Routes Still Available
- `/api/emails` - Legacy email operations
- `/api/categories` - Legacy category operations
- Other existing endpoints

### New Routes (Recommended)
- `/api/v1/emails` - Enhanced email operations
- `/api/v1/categories` - Enhanced category operations
- Additional endpoints with improved functionality

## Testing Migration

### 1. Unit Tests
Update import statements in unit tests to use new module paths.

### 2. Integration Tests
Verify that existing integration tests still pass with the new architecture.

### 3. End-to-End Tests
Ensure all user workflows continue to function correctly.

## Deployment Recommendations

### 1. Staging Environment
Deploy the refactored code to a staging environment first.

### 2. Gradual Rollout
- Enable new API endpoints
- Monitor performance and error rates
- Gradually migrate client applications to new endpoints

### 3. Monitoring
- Watch for increased error rates
- Monitor performance metrics
- Verify all existing functionality

## Rollback Procedure

If issues are encountered:

1. Revert to the previous version
2. Restore database from backup if needed
3. Update client applications to use legacy endpoints
4. Investigate and fix issues before retrying migration

## Support

For questions about the migration, contact the development team or refer to:
- `refactor/completion_summary.md` - Detailed refactoring summary
- `refactor/analysis_report.md` - Original analysis
- API documentation in `docs/` directory

## Timeline

The migration can be performed gradually:
1. Week 1: Deploy new architecture alongside legacy
2. Week 2-3: Migrate client applications to new API
3. Week 4: Deprecate legacy endpoints (optional)
4. Week 5: Remove legacy code (optional, future phase)