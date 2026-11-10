# Task 014.8: Integration with Alignment Workflow

**Status:** specified
**Priority:** high
**Effort:** TBD
**Complexity:** TBD
**Dependencies:** 014.7

---

## Overview/Purpose

The detector has to run at the right moment in the alignment pipeline: before the aligner starts,
because that is when the operator can still choose a different target and avoid the conflict entirely.

## Success Criteria

- [ ] [Success criteria to be defined]

## Prerequisites & Dependencies

### Required Before Starting
- [ ] 014.7

### Blocks (What This Task Unblocks)
- [ ] To be defined

### External Dependencies
- [ ] No external dependencies

## Sub-subtasks Breakdown


## Specification Details

### Task Interface
- **ID**: 014.8
- **Title**: Integration with Alignment Workflow
- **Status**: pending
- **Priority**: high
- **Effort**: TBD
- **Complexity**: TBD

### Requirements
1. The pipeline runs prediction before the alignment stage and hard-conflict detection after it, and
   the stage table (011.1) is the only place that ordering is declared.
2. A predicted conflict does not stop the run; an actual conflict does. The distinction is recorded
   in the run state.
3. The stage passes the branch and target as arguments through the table, never through a shell
   string, and both are validated by `safe_ref` before reaching `git`.
4. On conflict, the run prints the report path and the backup path from task 013 and stops.

## Implementation Guide

Wire into the runner from task 012, reusing `check_conflicts(target_branch, source_branch)`.

```bash
python scripts/alignment/orchestrator.py detect --branch <name> --target main
```

Test the argument path with a branch name containing a shell metacharacter; `safe_ref` must reject it
before any command runs.


### 014.8. Integration with Alignment Workflow

**Effort:** 6-8 hours
**Depends on:** 014.7

**Steps:**
1. Create integration API for Task 010
2. Implement workflow hooks for conflict handling
3. Add resolution state management
4. Create status reporting for alignment process
5. Implement error propagation to parent tasks

**Success Criteria:**
- [ ] Integration API for Task 010 implemented
- [ ] Workflow hooks for conflict handling operational
- [ ] Resolution state management functional
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
