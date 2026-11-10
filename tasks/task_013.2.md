# Task 013.2: Implement Pre-Alignment Safety Checks

**Status:** specified
**Priority:** high
**Effort:** TBD
**Complexity:** TBD
**Dependencies:** 013.1

---

## Overview/Purpose

The pre-alignment checks are the cheapest thing in the pipeline and the ones that save the most work:
a dirty tree, a detached head or a branch that is not where the operator thinks it is will make every
later stage report a false result.

## Success Criteria

- [ ] [Success criteria to be defined]

## Prerequisites & Dependencies

### Required Before Starting
- [ ] 013.1

### Blocks (What This Task Unblocks)
- [ ] To be defined

### External Dependencies
- [ ] No external dependencies

## Sub-subtasks Breakdown


## Specification Details

### Task Interface
- **ID**: 013.2
- **Title**: Implement Pre-Alignment Safety Checks
- **Status**: pending
- **Priority**: high
- **Effort**: TBD
- **Complexity**: TBD

### Requirements
1. The checks verify, in this order: a clean working tree (`git status --porcelain` empty), a named
   branch rather than a detached HEAD, the branch's current sha recorded, and the target ref fetched.
2. Each failure names the recovery command, and none of them proceeds automatically -- the check
   stops the run rather than repairing.
3. The checks never use `git clean -xfd` or `git reset --hard`; a dirty tree is the operator's to
   resolve, because those two commands destroy untracked work that is exactly what the backup
   cannot recover.
4. The results are recorded in the run state so a resume can verify the situation has not changed
   underneath it.

## Implementation Guide

Implement `scripts/alignment/preflight.py`, or a `preflight` stage in the orchestrator.

```bash
git status --porcelain | wc -l
git rev-parse --abbrev-ref HEAD
git rev-parse HEAD
```

Test the detached-HEAD case explicitly (`git checkout --detach`) -- `rev-parse --abbrev-ref HEAD`
returns the literal string `HEAD`, which is easy to miss when the check is written as a truthiness
test.


### 013.2. Implement Pre-Alignment Safety Checks

**Effort:** 6-8 hours
**Depends on:** 013.1

**Steps:**
1. Implement repository state validation
2. Create working directory cleanliness checks
3. Add branch existence verification
4. Implement Git command availability checks
5. Add permission validation for repository operations

**Success Criteria:**
- [ ] Repository state validation implemented
- [ ] Working directory cleanliness checks operational
- [ ] Branch existence verification functional
- [ ] Git command availability validated
- [ ] Permission validation operational

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
