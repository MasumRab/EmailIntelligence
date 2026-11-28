# Task 012.9: Integrate Error Detection & Handling (Task 005) into Workflow

**Status:** specified
**Priority:** high
**Effort:** TBD
**Complexity:** TBD
**Dependencies:** 012.6, 012.8

---

## Overview/Purpose

[Overview to be defined]

## Success Criteria

- [ ] [Success criteria to be defined]

## Prerequisites & Dependencies

### Required Before Starting
- [ ] 012.6, 012.8

### Blocks (What This Task Unblocks)
- [ ] To be defined

### External Dependencies
- [ ] No external dependencies

## Sub-subtasks Breakdown


## Specification Details

### Task Interface
- **ID**: 012.9
- **Title**: Integrate Error Detection & Handling (Task 005) into Workflow
- **Status**: specified
- **Priority**: high
- **Effort**: TBD
- **Complexity**: TBD

### Requirements
1. The error-detection stage runs `scripts/detect_merge_markers.py` and the task 005 detection suite
   against the branch's working tree, and its findings are a stage result, not a printed warning.
2. Conflict markers, `<<<<<<<`, `=======` and `>>>>>>>`, are a hard failure of the stage; the source
   is parsed, not grepped, because a marker inside a string literal is still a marker and a marker
   inside a fixture is not.
3. The stage treats a detection script that exits 0 while printing "0 files checked" as a failure,
   since a detector that examined nothing did not pass.
4. Findings are appended to the run state with file and line, so the documentation stage can cite
   them.

## Implementation Guide

Call `scripts/detect_merge_markers.py` from `scripts/alignment/orchestrator.py errors`.

```bash
python scripts/detect_merge_markers.py --root . ; echo "exit=$?"
python -c "import ast,sys; [ast.parse(open(p).read()) for p in sys.argv[1:]]" <changed files>
```

Note that `ast.parse` alone is not a syntax check -- `await` outside `async def` parses fine; use
`compile()` when the task means "valid Python".


### 012.9. Integrate Error Detection & Handling (Task 005) into Workflow

**Status:** pending  
**Dependencies:** 012.6, 012.8  

Implement the invocation of Task 005's error detection scripts after the alignment step for each feature branch and process its results.

**Details:**

Following the alignment step (Task 009/010), call Task 005 (the external error detection tool) with the context of the aligned branch. Interpret its results to determine if alignment introduced new issues or if existing ones were detected, logging any findings.


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
