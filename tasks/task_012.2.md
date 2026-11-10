# Task 012.2: Integrate Feature Branch Identification & Categorization Tool

**Status:** specified
**Priority:** high
**Effort:** TBD
**Complexity:** TBD
**Dependencies:** None

---

## Overview/Purpose

[Overview to be defined]

## Success Criteria

- [ ] [Success criteria to be defined]

## Prerequisites & Dependencies

### Required Before Starting
- [ ] None

### Blocks (What This Task Unblocks)
- [ ] To be defined

### External Dependencies
- [ ] No external dependencies

## Sub-subtasks Breakdown


## Specification Details

### Task Interface
- **ID**: 012.2
- **Title**: Integrate Feature Branch Identification & Categorization Tool
- **Status**: specified
- **Priority**: high
- **Effort**: TBD
- **Complexity**: TBD

### Requirements
1. The orchestrator calls the categorisation stage through a Python function or a documented CLI,
   never by re-implementing `git branch` parsing, and the interface is written down.
2. The categoriser's output schema is fixed before integration: a list of
   `{branch, category, commits_ahead, merge_base, reason}`.
3. An empty categoriser result is an error state with a distinct exit code, not "no branches to
   process". A silent zero-item run is indistinguishable from a crash in a batch script.
4. The integration records the categoriser's commit or version in the run state, so a run can be
   reproduced with the same input.

## Implementation Guide

The categoriser to call is task 007's tool; the checked-in starting point is
`scripts/alignment/check_alignment.py`. Wrap it, do not copy it.

```bash
python scripts/alignment/orchestrator.py categorise --out docs/alignment-run.json
python -c "import json;d=json.load(open('docs/alignment-run.json'));print(len(d['branches']))"
```

Confirm the second command prints the same count the orchestrator reports; a wrapper that loses
entries is the common failure here.


### 012.2. Integrate Feature Branch Identification & Categorization Tool

**Status:** pending  
**Dependencies:** None  

Implement the functionality to call Task 007's tool to identify and categorize feature branches, capturing its output.

**Details:**

Develop Python code to invoke Task 007's tool (which is assumed to be an external script or function), capture its output (a list of categorized branches), and parse this information into a structured format within the orchestrator's internal state.


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
