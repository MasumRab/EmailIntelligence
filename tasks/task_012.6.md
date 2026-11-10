# Task 012.6: Implement Sequential Execution Control Flow for Branches

**Status:** specified
**Priority:** high
**Effort:** TBD
**Complexity:** TBD
**Dependencies:** 012.1, 012.4, 012.5

---

## Overview/Purpose

[Overview to be defined]

## Success Criteria

- [ ] [Success criteria to be defined]

## Prerequisites & Dependencies

### Required Before Starting
- [ ] 012.1, 012.4, 012.5

### Blocks (What This Task Unblocks)
- [ ] To be defined

### External Dependencies
- [ ] No external dependencies

## Sub-subtasks Breakdown


## Specification Details

### Task Interface
- **ID**: 012.6
- **Title**: Implement Sequential Execution Control Flow for Branches
- **Status**: specified
- **Priority**: high
- **Effort**: TBD
- **Complexity**: TBD

### Requirements
1. The control flow is a loop over the queue with explicit pre/post hooks per stage, not nested
   conditionals; each stage's failure policy comes from the design (task 012.1).
2. Before each branch is processed the orchestrator records `before_sha` via `git rev-parse`; after
   the branch's stages it records `after_sha`. An unchanged sha with `status: done` is an error,
   because it means the stages were no-ops.
3. A stage that changes the working tree must fail if the tree was dirty on entry; the orchestrator
   checks `git status --porcelain` and refuses rather than mixing the operator's edits into the
   result.
4. Nothing in the loop calls `git reset --hard` or `git clean -xfd`; recovery uses the backup from
   task 006.

## Implementation Guide

Implement `scripts/alignment/orchestrator.py run`. Reuse `scripts/atomic_commit_manager.py` when the
run needs to commit intermediate results, so a failure part-way leaves a coherent history.

```bash
python scripts/alignment/orchestrator.py run --plan docs/alignment-run.json --dry-run
```

`--dry-run` must print every command it would run and execute none; that output is also the fixture
for the tests.


### 012.6. Implement Sequential Execution Control Flow for Branches

**Status:** pending  
**Dependencies:** 012.1, 012.4, 012.5  

Develop the core loop that iterates through the branch processing queue, managing the sequential execution of all alignment steps for each selected feature branch.

**Details:**

This central loop will be the primary driver, calling subsequent integration subtasks (e.g., backup, alignment, error checking, validation, documentation) for each branch. It must manage the current branch's context throughout its processing lifecycle.


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
