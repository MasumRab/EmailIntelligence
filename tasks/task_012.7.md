# Task 012.7: Integrate Backup Procedure (Task 006) into Workflow

**Status:** specified
**Priority:** high
**Effort:** TBD
**Complexity:** TBD
**Dependencies:** 012.6

---

## Overview/Purpose

[Overview to be defined]

## Success Criteria

- [ ] [Success criteria to be defined]

## Prerequisites & Dependencies

### Required Before Starting
- [ ] 012.6

### Blocks (What This Task Unblocks)
- [ ] To be defined

### External Dependencies
- [ ] No external dependencies

## Sub-subtasks Breakdown


## Specification Details

### Task Interface
- **ID**: 012.7
- **Title**: Integrate Backup Procedure (Task 006) into Workflow
- **Status**: specified
- **Priority**: high
- **Effort**: TBD
- **Complexity**: TBD

### Requirements
1. The backup stage calls `scripts/branch_ref_backup.py`'s `snapshot()` (or its CLI) before the
   first stage that can move a ref, and records the backup file path in the run state.
2. The stage verifies the backup exists and is non-empty after writing, and aborts the run if it is
   not, because a missing backup turns the first failure into data loss.
3. The restore path is exercised by a test on a scratch branch: create, snapshot, move the branch,
   restore, assert the sha is the original one.
4. Backups are written under a run-scoped name that includes the branch and the timestamp, so a
   second run does not overwrite the first run's recovery point.

## Implementation Guide

Use `scripts/branch_ref_backup.py` -- it already exposes `snapshot(backup_file=...)`,
`restore(backup_file=...)` and an argparse CLI. Extend `tests/test_branch_ref_backup.py` with the
move-and-restore case.

```bash
python scripts/branch_ref_backup.py snapshot --file backups/<branch>-<ts>.json
python scripts/branch_ref_backup.py restore --file backups/<branch>-<ts>.json
```

Do not re-implement the file format; the existing module's format is what the tests assert.


### 012.7. Integrate Backup Procedure (Task 006) into Workflow

**Status:** pending  
**Dependencies:** 012.6  

Implement the invocation of Task 006's backup procedure for the currently processed feature branch at the beginning of its alignment process.

**Details:**

Modify the execution loop to call Task 006 (the external backup tool) for the current branch before any alignment operations begin. Ensure the orchestrator correctly passes necessary branch identifiers to Task 006 and handles its return values or potential exceptions.


## Configuration Parameters

- **Owner**: TBD
- **Initiative**: TBD
- **Scope**: TBD
- **Focus**: TBD

## Performance Targets

- **Effort Range**: TBD
- **Complexity Level**: TBD

## Testing Strategy

Test strategy to be defined

## Common Gotchas & Solutions

- [ ] No common gotchas identified

## Integration Checkpoint

### Criteria for Moving Forward
- [ ] All success criteria met
- [ ] Code reviewed and approved
- [ ] Tests passing
- [ ] Documentation updated
- [ ] No critical or high severity issues

## Done Definition

### Completion Criteria
- [ ] All success criteria met
- [ ] Code reviewed and approved
- [ ] Tests passing
- [ ] Documentation updated

## Next Steps

- [ ] Next steps to be defined
