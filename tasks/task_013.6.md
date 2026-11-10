# Task 013.6: Integrate with Alignment Workflow

**Status:** specified
**Priority:** high
**Effort:** TBD
**Complexity:** TBD
**Dependencies:** 013.5

---

## Overview/Purpose

A safety framework that the alignment runner calls inconsistently is worse than none, because it
looks present. This task fixes the call points so every stage that can move a ref is covered.

## Success Criteria

- [ ] [Success criteria to be defined]

## Prerequisites & Dependencies

### Required Before Starting
- [ ] 013.5

### Blocks (What This Task Unblocks)
- [ ] To be defined

### External Dependencies
- [ ] No external dependencies

## Sub-subtasks Breakdown


## Specification Details

### Task Interface
- **ID**: 013.6
- **Title**: Integrate with Alignment Workflow
- **Status**: pending
- **Priority**: high
- **Effort**: TBD
- **Complexity**: TBD

### Requirements
1. The runner's stage table (from task 011.1) is the single place that declares which stages take a
   backup, and the code reads that table rather than embedding a second list.
2. Every stage that runs `git merge`, `git rebase`, `git reset` or `git branch -f` is marked as
   requiring a backup, and a test asserts the marking for those four command families.
3. The restore path is exercised end to end on a scratch branch: snapshot, move the ref, restore,
   assert the sha matches.
4. On restore, the runner refuses if the working tree is dirty -- restoring a ref under uncommitted
   changes produces a tree that matches neither state.

## Implementation Guide

Wire the calls in `scripts/alignment/` (the runner from task 012), reusing the backup module.

```bash
uv run pytest tests/test_branch_ref_backup.py -v
git checkout -b scratch/backup-check && git commit --allow-empty -m x && git reset --hard HEAD~1
```

The test for requirement 2 is a source scan for the four command families, keyed off the same table.


### 013.6. Integrate with Alignment Workflow

**Effort:** 6-8 hours
**Depends on:** 013.5

**Steps:**
1. Create integration API for Task 010
2. Implement workflow hooks for backup operations
3. Add safety check integration points
4. Create status reporting for alignment process
5. Implement error propagation to parent tasks

**Success Criteria:**
- [ ] Integration API for Task 010 implemented
- [ ] Workflow hooks for backup operations operational
- [ ] Safety check integration points functional
- [ ] Status reporting for alignment process operational
- [ ] Error propagation to parent tasks implemented

---


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
