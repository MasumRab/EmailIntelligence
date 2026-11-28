# Task 012.11: Integrate Documentation Generation (Task 015) into Workflow

**Status:** specified
**Priority:** high
**Effort:** TBD
**Complexity:** TBD
**Dependencies:** 012.6, 012.10

---

## Overview/Purpose

[Overview to be defined]

## Success Criteria

- [ ] [Success criteria to be defined]

## Prerequisites & Dependencies

### Required Before Starting
- [ ] 012.6, 012.10

### Blocks (What This Task Unblocks)
- [ ] To be defined

### External Dependencies
- [ ] No external dependencies

## Sub-subtasks Breakdown


## Specification Details

### Task Interface
- **ID**: 012.11
- **Title**: Integrate Documentation Generation (Task 015) into Workflow
- **Status**: specified
- **Priority**: high
- **Effort**: TBD
- **Complexity**: TBD

### Requirements
1. The documentation stage invokes task 015 (`CHANGES_SUMMARY.md` generation) after validation, and
   the cross-reference is to task 015, not task 008 -- task 008 is the merge validation framework.
2. The generated summary is written to the branch's worktree, and the stage records its path and
   size in the run state.
3. The stage refuses to overwrite an existing `CHANGES_SUMMARY.md` unless `--force` is passed.
4. A summary shorter than a stated minimum (for example 200 characters) is treated as generation
   failure, because an empty template would otherwise be committed as documentation.

## Implementation Guide

Fix the title's "(Task 008)" to "(Task 015)" in the heading, the `### Task Interface` block and the
section sub-heading, then implement the stage in `scripts/alignment/orchestrator.py document`.

```bash
python scripts/alignment/orchestrator.py document --plan docs/alignment-run.json --branch <name>
wc -c CHANGES_SUMMARY.md
```

Task 015 is the documentation generator; the checked-in helper today is `scripts/doc_generator.py`.


### 012.11. Integrate Documentation Generation (Task 015) into Workflow

**Status:** pending  
**Dependencies:** 012.6, 012.10  

Implement the mechanism to prompt for or automatically generate `CHANGES_SUMMARY.md` via Task 015 after successful validation of a feature branch.

**Details:**

Once Task 011 (Subtask 10) indicates successful validation, invoke Task 015 (the external documentation tool). This might involve presenting a prompt to the developer for input, or passing collected alignment information to Task 015 for automatic generation of `CHANGES_SUMMARY.md`.


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
