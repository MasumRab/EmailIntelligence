# Task 015.2: Implement Post-Rebase Validation

**Status:** specified
**Priority:** high
**Effort:** TBD
**Complexity:** TBD
**Dependencies:** 015.1

---

## Overview/Purpose

A rebase rewrites every commit id. The failure this task exists to catch is the quiet one: the rebase
succeeds, the tests pass, and one commit's change was dropped in a conflict resolution.

## Success Criteria

- [ ] [Success criteria to be defined]

## Prerequisites & Dependencies

### Required Before Starting
- [ ] 015.1

### Blocks (What This Task Unblocks)
- [ ] To be defined

### External Dependencies
- [ ] No external dependencies

## Sub-subtasks Breakdown


## Specification Details

### Task Interface
- **ID**: 015.2
- **Title**: Implement Post-Rebase Validation
- **Status**: pending
- **Priority**: high
- **Effort**: TBD
- **Complexity**: TBD

### Requirements
1. Before the rebase the branch's commit list is recorded (`git rev-list --reverse <base>..<head>`)
   with subject and patch-id per commit; after it, the same list is computed and compared by
   subject and patch-id, not by sha.
2. Missing or duplicated patches fail the stage, and the report names the commit subjects.
3. The comparison is against the recorded list, never against `<old-head>..<new-head>`, which is empty
   after a rebase and would report success for any result.
4. The stage runs before the push, so a dropped commit never reaches the remote.

## Implementation Guide

Implement `scripts/validate_rebase.py` (or a stage in the 012 runner).

```bash
git rev-list --reverse origin/main..HEAD | while read c; do echo "$(git show -s --format=%s $c) $(git show $c | git patch-id --stable | cut -d' ' -f1)"; done
```

Test with a deliberate `git rebase --onto` that drops the middle commit and confirm the stage fails
with its subject.


### 015.2. Implement Post-Rebase Validation

**Effort:** 6-8 hours
**Depends on:** 015.1

**Steps:**
1. Create Git history validation checks
2. Implement linear history verification
3. Add commit integrity validation
4. Create validation reporting system
5. Add error handling for validation failures

**Success Criteria:**
- [ ] Git history validation implemented
- [ ] Linear history verification operational
- [ ] Commit integrity validation functional
- [ ] Validation reporting system operational
- [ ] Error handling for failures implemented

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
