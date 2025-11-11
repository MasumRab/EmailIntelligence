# Speckit Implementation Task Completion Template

This template provides guidance for transitioning from Speckit-generated plans to actual task execution.

## Overview

The Speckit workflow is designed to generate specifications and plans, but actual implementation requires separate execution of system-level tasks that may include Git operations, code changes, and other system commands.

## Workflow Integration Pattern

### Phase 1: Specification & Planning (Speckit Tools)
```text
/speckit.specify → /speckit.clarify → /speckit.plan → /speckit.tasks
```

### Phase 2: Task Execution (Manual/Scripted Implementation)
```text
Execute actual implementation based on generated tasks
```

### Phase 3: Validation & Completion
```text
Verify all requirements are met and mark completion
```

## Template for Actual Task Execution

### For Git/Repository Operations

Instead of just marking tasks as conceptually completed, execute the actual operations:

```bash
# Example: T001 Clone or update local repository
git clone <repo-url> || git pull origin main

# Example: T005 Identify merge conflicts
git fetch origin
git checkout pr-branch
git merge origin/target-branch  # This will show actual conflicts

# Example: T016-T018 Resolve merge conflicts
# 1. Manually edit conflicted files to resolve <<<<<<< >>>>>>> markers
# 2. Run: git add <resolved-files>
# 3. Run: git commit
```

### For Code Modifications

Instead of claiming "code style comments would be addressed", actually:

1. Read the PR comments to identify specific style issues
2. Run linting tools like flake8, black, or isort
3. Apply fixes to the relevant files
4. Verify the fixes address the specific comments

### For Documentation Updates

Actually create or update the specified documentation files rather than just claiming they "would be created".

## Key Principles for Actual Implementation

1. **Execute, Don't Just Acknowledge**: Perform the actual operations rather than just acknowledging what would be done
2. **Validate Results**: Run tests, check Git status, verify outputs after each task
3. **Mark Completion Properly**: Update the tasks.md file with actual completion status only after verifying the work was done
4. **Handle Dependencies**: Execute tasks in dependency order as specified in the tasks.md file
5. **Parallel Execution**: When tasks are marked [P] (parallel), execute them simultaneously where possible
6. **Error Handling**: Stop if critical tasks fail, continue for parallel tasks with reporting of failures

## Transition Checklist

Before starting actual implementation:

- [ ] Speckit planning workflow completed (spec, plan, tasks generated)
- [ ] Tasks.md contains specific, actionable tasks
- [ ] Understand which tasks require system operations (Git, file creation, etc.)
- [ ] Have necessary credentials/permissions for operations
- [ ] Backup strategy in place for risky operations
- [ ] Test environment ready for validation

## Example Implementation Script Structure

```bash
#!/bin/bash
# actual-implementation-script.sh

echo "Starting actual implementation for feature..."

# Setup phase
echo "Executing setup tasks..."
# Execute T001-T004 tasks with actual commands

# Foundational phase  
echo "Executing foundational tasks..."
# Execute T005-T009 tasks with actual commands

# User story phases
echo "Executing user story tasks..."
# Execute tasks for each user story with actual operations

# Polish phase
echo "Executing final validation..."
# Execute final validation tasks

echo "Implementation completed!"
```

## Constitution Alignment During Implementation

During actual implementation, continue to follow constitution principles:
- TDD: Write tests before code changes
- Code quality: Follow PEP 8, include type hints
- Security: Run security scans as specified
- Performance: Verify performance requirements met
- Documentation: Update as required

## Tracking Completion

Update tasks.md with actual completion status:

```markdown
- [x] T001 Clone or update local repository to match PR #176 branch from GitHub
- [x] T002 [P] Install required development tools (Git, GitHub CLI, Python 3.12) 
- [x] T003 [P] Review all PR #176 comments in GitHub to understand all required changes
```

## Common Pitfalls to Avoid

- ❌ Claiming tasks are "completed" without executing actual operations
- ❌ Assuming Speckit tools execute implementation (they only generate plans)
- ❌ Skipping validation steps after task completion
- ❌ Ignoring task dependencies and parallelization markers
- ❌ Not backing up before risky operations

- ✅ Execute each task with actual system commands
- ✅ Verify results after each task completion
- ✅ Follow dependency order and parallel execution opportunities
- ✅ Maintain constitution principles during implementation
- ✅ Update task status only after verification