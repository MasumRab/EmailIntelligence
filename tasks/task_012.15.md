# Task 012.15: Integrate Architectural Migration (Task 022) into Workflow

**Status:** specified
**Priority:** high
**Effort:** TBD
**Complexity:** TBD
**Dependencies:** 012.7, 022

---

## Overview/Purpose

[Overview to be defined]

## Success Criteria

- [ ] [Success criteria to be defined]

## Prerequisites & Dependencies

### Required Before Starting
- [ ] 012.7, 022

### Blocks (What This Task Unblocks)
- [ ] To be defined

### External Dependencies
- [ ] No external dependencies

## Sub-subtasks Breakdown


## Specification Details

### Task Interface
- **ID**: 012.15
- **Title**: Integrate Architectural Migration (Task 022) into Workflow
- **Status**: specified
- **Priority**: high
- **Effort**: TBD
- **Complexity**: TBD

### Requirements
1. The migration stage calls task 022's `backend` -> `src` migration before alignment, and the run
   state records whether the branch needed migration and what it changed.
2. The stage refuses to migrate a branch whose working tree is dirty, and refuses to run twice on the
   same branch without `--force`, because a migration applied twice moves files that are already
   moved.
3. Files the migration cannot classify are reported and left in place, never deleted; an unclassified
   file is a decision for a human.
4. The stage verifies the result with a compile of every moved module before declaring success.

## Implementation Guide

Implement `scripts/alignment/orchestrator.py migrate`. Task 022 is the migration design; there is no
checked-in migration entry point today, so the stage must fail with a clear message until it exists
rather than silently doing nothing.

```bash
python scripts/alignment/orchestrator.py migrate --plan docs/alignment-run.json --branch <name>
python -m compileall -q src/ ; echo "exit=$?"
```

`compile()` is the check that catches `await` outside `async def`; `ast.parse` does not.


### 012.15. Integrate Architectural Migration (Task 022) into Workflow

**Status:** pending
**Dependencies:** 012.7, 022

Implement the invocation of Task 022's automated migration script after the backup step (012.7) and before the alignment step (012.8).

**Details:**

Call the migration tool to normalize the feature branch's directory structure (`backend` -> `src/backend`) and inject the factory pattern. Capture the migration status. If migration fails, halt the workflow or prompt the user, depending on severity. Ensure this step allows the subsequent alignment (Task 009/010) to work on a structurally compatible branch.
- **Effort**: N/A
- **Complexity**: N/A

## Configuration Parameters

- **Owner**: TBD
- **Initiative**: TBD
- **Scope**: TBD
- **Focus**: TBD

## Performance Targets

- **Effort Range**: TBD
- **Complexity Level**: TBD

## Testing Strategy

### Unit Tests
- [ ] Tests cover core functionality
- [ ] Edge cases handled appropriately
- [ ] Performance benchmarks met

### Integration Tests
- [ ] Integration with dependent components verified
- [ ] End-to-end workflow tested
- [ ] Error handling verified

### Test Strategy Notes


## Common Gotchas & Solutions

- [ ] [Common issues and solutions to be documented]

## Integration Checkpoint

### Criteria for Moving Forward
- [ ] All success criteria met
- [ ] Code reviewed and approved
- [ ] Tests passing
- [ ] Documentation updated
- [ ] No critical or high severity issues

## Done Definition

### Completion Criteria
- [ ] All success criteria checkboxes marked complete
- [ ] Code quality standards met (PEP 8, documentation)
- [ ] Performance targets achieved
- [ ] All subtasks completed
- [ ] Integration checkpoint criteria satisfied

## Next Steps

- [ ] No next steps specified
- [ ] Additional steps to be defined


<!-- EXTENDED_METADATA
END_EXTENDED_METADATA -->
