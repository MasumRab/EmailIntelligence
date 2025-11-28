# External Data References in Task Master

## Overview
This document describes the approach for managing precalculated values and external data in Task Master tasks by referencing external JSON files instead of hardcoding values directly in the task definitions.

## Motivation
Previously, Task Master tasks contained hardcoded lists of values (such as branch names, file paths, etc.) directly embedded in the task descriptions. This led to several issues:

1. **Maintainability**: Changes to the lists required updates in multiple places
2. **Security**: Large hardcoded lists increased potential attack surfaces
3. **Flexibility**: Impossible to update values without modifying the task definitions
4. **Readability**: Task files became bloated with data rather than focusing on logic

## Implementation Pattern

### 1. External Data Files
Store precalculated values in dedicated JSON files in the `task_data/` directory:

```json
{
  "orchestration_branches": [
    "001-orchestration-tools-consistency",
    "001-orchestration-tools-verification-review", 
    "002-validate-orchestration-tools",
    "add-comparison-files-to-orchestration-tools",
    "diverged-orchestration-tools-20251115161102",
    // ... more items
  ],
  "metadata": {
    "generated_at": "2025-11-28T00:00:00.000Z",
    "description": "Precalculated list of orchestration-tools branches for alignment tasks",
    "source": "Task 101 in tasks.json",
    "file_reference": "task_data/orchestration_branches.json"
  },
  "count": 24
}
```

### 2. Task File References
Replace hardcoded lists in tasks.json with references to external data files:

**Before (Hardcoded)**:
```
details: "Precalculated orchestration-tools branches to align: branch1,branch2,branch3,..."
```

**After (External Reference)**:
```
details: "Referenced orchestration-tools branches to align: See task_data/orchestration_branches.json for complete list of 24 branches to align"
```

### 3. File Organization
- Store external data in `task_data/` directory
- Use descriptive filenames that match the task's purpose
- Include metadata in JSON files to provide context
- Keep data files separate from task logic

## Benefits
1. **Separation of Concerns**: Task logic remains separate from task data
2. **Maintainability**: Data can be updated without modifying task definitions
3. **Security**: Reduced attack surface from long hardcoded strings
4. **Flexibility**: Data can be generated dynamically or updated by processes
5. **Readability**: Task files are cleaner and more focused

## Best Practices
1. Always use external file references for lists containing more than 5 items
2. Include a count in the external JSON file for verification
3. Include metadata about when the file was generated and its purpose
4. Use descriptive file names that clearly indicate the data's purpose
5. Reference the external file in both the task details and test strategy sections

This pattern has been successfully implemented for the orchestration-tools branch alignment task (Task 101) as a proof of concept.