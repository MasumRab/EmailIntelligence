# Task 012.10: Integrate Validation Framework (Task 011) into Workflow

**Status:** specified
**Priority:** high
**Effort:** TBD
**Complexity:** TBD
**Dependencies:** 012.6, 012.9

---

## Overview/Purpose

[Overview to be defined]

## Success Criteria

- [ ] [Success criteria to be defined]

## Prerequisites & Dependencies

### Required Before Starting
- [ ] 012.6, 012.9

### Blocks (What This Task Unblocks)
- [ ] To be defined

### External Dependencies
- [ ] No external dependencies

## Sub-subtasks Breakdown


## Specification Details

### Task Interface
- **ID**: 012.10
- **Title**: Integrate Validation Framework (Task 011) into Workflow
- **Status**: specified
- **Priority**: high
- **Effort**: TBD
- **Complexity**: TBD

### Requirements
1. The validation stage invokes task 011's integrated validation and consumes its machine-readable
   report; it does not scrape stdout for the word "pass".
2. A validation exit code of 0 with an empty report is a failure of the stage, because the two
   disagree.
3. The stage records the validation report path in the run state so a reviewer can open it after the
   run.
4. If validation is advisory for the branch's category, the run state says `advisory` rather than
   `pass`; conflating the two loses the distinction the operator needs.

## Implementation Guide

Wire `scripts/alignment/orchestrator.py validate` to the task 011 entry point, reusing
`scripts/parallel_validator.py` and `scripts/validation_cache.py` where they fit.

```bash
python scripts/alignment/orchestrator.py validate --plan docs/alignment-run.json --branch <name>
```

Test the empty-report path with a stub that exits 0 and writes nothing.


### 012.10. Integrate Validation Framework (Task 011) into Workflow

**Status:** pending  
**Dependencies:** 012.6, 012.9  

Implement the trigger for Task 011's integrated validation process after error detection for each feature branch, using its output to confirm alignment success.

**Details:**

After error detection (Task 005), invoke Task 011 (the external validation tool) for the aligned branch. Await its completion and use its output to confirm the overall success or identify the need for further manual resolution.


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
