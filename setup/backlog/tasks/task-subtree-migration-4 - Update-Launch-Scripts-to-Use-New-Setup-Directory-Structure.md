# Task: Update Launch Scripts to Use New Setup Directory Structure

## Description
Update all launch scripts and related code to work with the new `/setup` directory structure and subtree approach.

## Steps
1. Update paths in launch scripts to reference setup files correctly
2. Modify any configuration or import paths affected by the restructuring
3. Ensure launch scripts still function properly from repository root
4. Test that all launch functionality works after restructuring

## Subtasks
- [ ] Update import paths in launch.py if needed
- [ ] Update paths in launch.sh to reference setup files
- [ ] Update paths in launch.bat to reference setup files
- [ ] Verify all setup scripts execute correctly from new location
- [ ] Test the entire launch process from repository root
- [ ] Update any hardcoded paths in setup scripts

## Acceptance Criteria
- [ ] Launch scripts work correctly with new directory structure
- [ ] All setup functionality maintained
- [ ] No broken paths or missing references
- [ ] Launch process fully functional

## Task Dependencies
- task-subtree-migration-3 - Initialize-Git-Subtree-for-Setup-Directory.md

## Priority
High

## Effort Estimate
4 hours

## Status
Pending