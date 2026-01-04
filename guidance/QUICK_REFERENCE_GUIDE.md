# Architecture Alignment: Quick Reference Guide

## Overview
This guide provides a quick reference for implementing architecture alignment between branches with different architectural approaches.

## Key Steps

### 1. Assessment Phase
- Analyze architectural differences between branches
- Identify core functionality to preserve
- Map import path dependencies
- Plan compatibility layer implementation

### 2. Implementation Phase
- Create factory pattern (e.g., `create_app()` in `src/main.py`)
- Standardize import paths to use consistent structure
- Integrate patterns from both architectures
- Preserve all functionality from both branches

### 3. Validation Phase
- Test service startup with both architectural patterns
- Verify all functionality preserved
- Run comprehensive tests
- Validate performance and security

## Critical Files to Create/Modify

### Factory Pattern Implementation
```python
# src/main.py
def create_app():
    """Factory function compatible with remote branch service startup."""
    # Create app from local implementation
    from src.backend.python_backend.main import create_app as create_local_backend
    app = create_local_backend()
    
    # Add remote branch patterns if available
    if CONTEXT_CONTROL_AVAILABLE:
        from .context_control.middleware import ContextControlMiddleware
        app.add_middleware(ContextControlMiddleware)
    
    return app
```

### Import Path Standardization
- Change `from backend.module` to `from src.backend.module`
- Update all internal imports to use new structure
- Maintain backward compatibility with deprecation warnings

## Common Issues and Solutions

### Issue: Service startup expects different patterns
**Solution**: Implement factory pattern that satisfies remote branch expectations while preserving local functionality

### Issue: Import paths don't match new structure
**Solution**: Update all imports systematically and test functionality after each change

### Issue: Missing files expected by remote branch
**Solution**: Either restore files or create compatibility adapters

### Issue: Runtime vs import-time initialization conflicts
**Solution**: Use lazy initialization patterns to defer resource-intensive operations

## Validation Commands

```bash
# Test factory pattern
SECRET_KEY=test_key python -c "from src.main import create_app; app = create_app(); print(f'App created with {len(app.routes)} routes')"

# Test service startup compatibility
uvicorn src.main:create_app --factory

# Run comprehensive validation
python validate_architecture_alignment.py
```

## Rollback Plan

If merge causes critical issues:
1. Revert to backup branches immediately
2. Document specific issues that occurred
3. Analyze root cause of problems
4. Implement fixes in isolated environment
5. Re-attempt merge with corrections

## Success Indicators

- ✅ Factory function works with remote branch service startup
- ✅ All local functionality preserved
- ✅ Remote branch patterns integrated
- ✅ No runtime errors in core functionality
- ✅ Tests pass for both architectures
- ✅ Performance maintained or improved

## Red Flags

- Direct rebasing of branches with different architectures
- Attempting to resolve every individual conflict manually
- Ignoring import-time vs runtime initialization differences
- Not testing functionality after merge steps
- Missing critical components from either branch

## Best Practices

- Always preserve functionality over resolving conflicts
- Create adapter layers rather than removing features
- Test service startup patterns work with merged code
- Validate that all related components were migrated together
- Document the merge process for future reference