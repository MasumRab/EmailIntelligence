# Task: Update Setup Subtree Integration in Scientific Branch

## Task ID: task-update-setup-subtree-integration

## Priority: High

## Status: Todo

## Description
Update the scientific branch to use the new setup subtree methodology that has been implemented in the main branch. This will align the architecture for easier merging and future maintenance.

## Target Branch
- Branch: `scientific`
- Based on: Current scientific branch state
- Integration target: Main branch setup subtree structure

## Specific Changes to Include
1. Verify the setup subtree is properly integrated
2. Update launch scripts to match main branch implementation
3. Ensure all path references are consistent
4. Update documentation to reflect new structure

## Action Plan

### Part 1: Assessment
1. Check current setup subtree configuration in scientific branch
2. Compare with main branch setup subtree implementation
3. Identify any differences in integration approach
4. Document current vs. target state

### Part 2: Implementation
1. Update launch scripts to reference setup subtree correctly
2. Ensure all path references are consistent with main branch
3. Verify symbolic links to configuration files are correct
4. Update any hardcoded paths that should reference the subtree

### Part 3: Testing
1. Test all launch methods (Python, bash, batch)
2. Verify application starts correctly with new structure
3. Ensure all services (backend, frontend, etc.) work as expected
4. Test environment setup functionality

### Part 4: Validation
1. Run existing test suite with new structure
2. Verify no functionality has been broken
3. Ensure all dependencies are properly handled
4. Document any changes needed for development workflow

## Success Criteria
- [ ] Setup subtree is properly integrated in scientific branch
- [ ] Launch scripts work consistently with main branch approach
- [ ] All application services start correctly with new structure
- [ ] Test suite passes with new setup structure
- [ ] Documentation updated to reflect changes
- [ ] PR created and ready for review

## Dependencies
- main branch setup subtree implementation completed
- Development environment validation procedures established

## Estimated Effort
1-2 days: Assessment and implementation
0.5 days: Testing and validation
0.5 days: Documentation and PR creation

## Notes
- This task is critical for architecture alignment between branches
- Careful testing is needed to ensure no regressions
- Team members should be notified of any changes to launch procedures
- Maintain backward compatibility where possible during transition