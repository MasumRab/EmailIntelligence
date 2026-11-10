# Task 014.4: Implement Interactive Resolution Guidance

**Status:** specified
**Priority:** high
**Effort:** TBD
**Complexity:** TBD
**Dependencies:** 014.3

---

## Overview/Purpose

The interactive guidance is the operator-facing half of the framework: for each conflict, what the two
sides did and which command to run. It is guidance, not action -- nothing here resolves anything.

## Success Criteria

- [ ] [Success criteria to be defined]

## Prerequisites & Dependencies

### Required Before Starting
- [ ] 014.3

### Blocks (What This Task Unblocks)
- [ ] To be defined

### External Dependencies
- [ ] No external dependencies

## Sub-subtasks Breakdown


## Specification Details

### Task Interface
- **ID**: 014.4
- **Title**: Implement Interactive Resolution Guidance
- **Status**: pending
- **Priority**: high
- **Effort**: TBD
- **Complexity**: TBD

### Requirements
1. For each conflicting file the tool prints, in this order: the class, the two sides' one-line
   summaries, and the exact command that opens the conflict (`git mergetool <path>` or
   `git checkout --ours/--theirs <path>` with the consequence of each stated).
2. It never runs a resolution command; it prints one.
3. It refuses to start when the tree is already in a conflicted state -- guidance for a merge that is
   already open belongs to `git status`, and mixing the two confuses the operator about what has
   happened.
4. It works with output redirected to a file, so a long list can be read in a pager.

## Implementation Guide

Add a `guide` subcommand to `scripts/conflict_detection.py` or a small `scripts/conflict_guide.py`.

```bash
python scripts/conflict_detection.py guide --target main --head HEAD > /tmp/guidance.txt
wc -l /tmp/guidance.txt
```

The redirect is the requirement-4 test: a tool that prompts stops dead when stdout is not a TTY.


### 014.4. Implement Interactive Resolution Guidance

**Effort:** 8-10 hours
**Depends on:** 014.3

**Steps:**
1. Create user interaction interface
2. Implement step-by-step resolution guidance
3. Add command suggestions for resolution
4. Create progress tracking for resolution
5. Add resolution success verification

**Success Criteria:**
- [ ] User interaction interface implemented
- [ ] Step-by-step guidance operational
- [ ] Command suggestions functional
- [ ] Progress tracking implemented
- [ ] Success verification operational

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
