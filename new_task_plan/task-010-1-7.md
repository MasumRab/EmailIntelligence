# Task 010.1-7: Core Primary-to-Feature Branch Alignment Logic

**Status:** pending
**Priority:** high
**Effort:** 4-6 hours each
**Complexity:** 6-8/10
**Dependencies:** Varies
**Created:** 2026-01-06
**Parent:** Task 010: Develop Core Primary-to-Feature Branch Alignment Logic

---

## Purpose

Implement core Git operations for primary-to-feature branch alignment.

---

## Details

Grouped implementation for Tasks 59.1-59.7.

### Subtask Breakdown

**010.1: Optimal Primary Target Determination**
- Validate primary branch input (main/scientific/orchestration-tools)
- Check branch existence and accessibility
- Return validated target

**010.2: Environment Setup and Safety Checks**
- Verify clean working directory
- Check for uncommitted changes
- Prompt for stash/commit

**010.3: Local Branch Backup**
- Create temporary backup branch
- Store current branch state
- Enable rollback capability

**010.4: Branch Switching Logic**
- Implement git checkout programmatically
- Handle errors gracefully
- Verify switch success

**010.5: Remote Fetch Logic**
- Fetch latest from primary target
- Handle network errors
- Verify fetch completion

**010.6: Core Rebase Initiation**
- Execute git rebase command
- Capture rebase output
- Detect rebase success/failure

**010.7: Conflict Detection and Pause**
- Detect merge conflicts
- Pause for manual resolution
- Provide resolution instructions

---

## Implementation

```python
# scripts/align_branch.py
import subprocess
import sys
from pathlib import Path

def validate_target(target):
    """Validate primary branch target."""
    valid = ["main", "scientific", "orchestration-tools"]
    if target not in valid:
        raise ValueError(f"Invalid target: {target}. Valid: {valid}")
    return target

def check_working_directory():
    """Ensure clean working directory."""
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True, text=True
    )
    if result.stdout.strip():
        print("WARNING: Uncommitted changes detected")
        return False
    return True

def create_backup(branch_name):
    """Create temporary backup."""
    timestamp = subprocess.run(
        ["date", "+%Y%m%d-%H%M%S"],
        capture_output=True, text=True
    ).stdout.strip()
    backup_name = f"backup-{branch_name}-{timestamp}"
    subprocess.run(["git", "branch", backup_name, branch_name])
    return backup_name

def rebase_branch(feature_branch, primary_target):
    """Execute rebase operation."""
    subprocess.run(["git", "checkout", feature_branch])
    subprocess.run(["git", "fetch", "origin", primary_target])
    
    result = subprocess.run(
        ["git", "rebase", f"origin/{primary_target}"],
        capture_output=True, text=True
    )
    
    if result.returncode != 0:
        if "CONFLICT" in result.stdout:
            print("CONFLICT DETECTED - Manual resolution required")
            print("Run: git rebase --abort to cancel")
        return False
    
    return True
```

---

## Success Criteria

- [ ] Target validation working
- [ ] Safety checks preventing data loss
- [ ] Backup enabling rollback
- [ ] Rebase executing correctly
- [ ] Conflicts detected and reported

---

## Progress Log

### 2026-01-06
- Consolidated subtask file created
- Ready for implementation

---

## Next Steps

After completion, continue with **010.8-15**: Advanced rebase and conflict handling
