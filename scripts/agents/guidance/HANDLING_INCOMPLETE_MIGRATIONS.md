# Handling Incomplete Migration Branches

## Overview
This document provides guidance on how to merge branches that have attempted architectural changes similar to the current implementation but not completed them.

## Identifying Incomplete Migration Branches

### 1. **Mixed Directory Structures**
Look for branches that have both old and new directory patterns:
```bash
# Check for both old and new structures
find . -name "backend" -type d
find . -name "src" -type d
```

### 2. **Inconsistent Import Paths**
Search for mixed import patterns:
```bash
# Look for both old and new import patterns in the same branch
git grep -r "from backend\." -- "*.py"
git grep -r "from src\." -- "*.py"
```

### 3. **Partial Component Migrations**
Check if some components were moved but dependencies weren't:
```bash
# Verify that related components were moved together
ls -la src/backend/  # Should have complete backend implementation
ls -la backend/      # Should be empty or have deprecated files only
```

## Safe Merge Strategy for Incomplete Migration Branches

### 1. **Assessment Phase**
- Identify which components were partially migrated
- Map dependencies between old and new structures
- Document which functionality works and which is broken

### 2. **Isolation Phase**
- Create a temporary branch for testing
- Isolate the incomplete migration changes
- Test functionality independently

### 3. **Integration Phase**
- Apply the completed architectural changes from this implementation
- Ensure all components are properly migrated
- Verify that no functionality is lost

### 4. **Validation Phase**
- Test all functionality works with the new architecture
- Verify service startup patterns work correctly
- Run comprehensive tests

## Prevention of Automatic Merge Mistakes

### 1. **Manual Verification Required**
- Never rely solely on Git's automatic merge for architectural changes
- Always verify functionality after merging
- Test service startup and core features

### 2. **Component Integration Testing**
- Test that components work together, not just in isolation
- Verify that import chains are complete
- Check that dependencies are properly resolved

### 3. **Architecture Compatibility Verification**
- Ensure the merged code satisfies both architectural patterns
- Test factory functions and service startup configurations
- Validate security and performance measures

## Recovery from Failed Merges

### 1. **Immediate Actions**
- Stop the merge process if functionality is broken
- Revert to backup branches
- Document what went wrong

### 2. **Analysis**
- Identify which components caused the issues
- Determine if it was a partial migration problem
- Plan a safer integration approach

### 3. **Retry with Safeguards**
- Use the hybrid approach that preserves functionality
- Implement proper adapter layers
- Test incrementally

## Best Practices

1. **Always backup before merging** architectural changes
2. **Test functionality, not just syntax** after merges
3. **Verify service startup** works with merged code
4. **Check for mixed import paths** that could cause runtime errors
5. **Validate that all related components** were migrated together
6. **Run comprehensive tests** to ensure no functionality is broken
7. **Document the merge process** for future reference