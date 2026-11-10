# Task 012.3: Develop Interactive Branch Selection & Prioritization UI

**Status:** specified
**Priority:** high
**Effort:** TBD
**Complexity:** TBD
**Dependencies:** 012.2

---

## Overview/Purpose

[Overview to be defined]

## Success Criteria

- [ ] [Success criteria to be defined]

## Prerequisites & Dependencies

### Required Before Starting
- [ ] 012.2

### Blocks (What This Task Unblocks)
- [ ] To be defined

### External Dependencies
- [ ] No external dependencies

## Sub-subtasks Breakdown


## Specification Details

### Task Interface
- **ID**: 012.3
- **Title**: Develop Interactive Branch Selection & Prioritization UI
- **Status**: specified
- **Priority**: high
- **Effort**: TBD
- **Complexity**: TBD

### Requirements
1. The interactive selection is a numbered list on stdout with a `readline` prompt, and it works
   when stdin is not a TTY by accepting `--select <ids>` instead. A workflow that requires a
   terminal cannot run in CI or in a background step.
2. The default selection is the priority order from task 012.5, and pressing Enter accepts it; an
   operator who does not care still gets a correct order.
3. Selecting a branch that does not exist in the categorised list is refused with the list of valid
   ids, not silently ignored.
4. The UI never prints a branch name without its `commits_ahead` and category, because the decision
   to align a branch depends on both.

## Implementation Guide

Use `argparse` plus one `input()` loop in `scripts/alignment/orchestrator.py select`. Keep the
non-interactive flag first-class in the tests.

```bash
printf '\n' | python scripts/alignment/orchestrator.py select --plan docs/alignment-run.json
python scripts/alignment/orchestrator.py select --plan docs/alignment-run.json --select 3,1
```

Both invocations must produce the same order for the same priorities; assert it.


### 012.3. Develop Interactive Branch Selection & Prioritization UI

**Status:** pending  
**Dependencies:** 012.2  

Create a command-line interface (CLI) to display categorized branches and allow the developer to select branches for processing, including optional prioritization based on P7.

**Details:**

The UI should clearly present branches grouped by their categories ('main', 'scientific', 'orchestration-tools'). Use interactive prompts (e.g., `inquirer` or simple `input` loops) to enable selection and reordering. Implement logic to apply 'P7' prioritization if chosen by the user, adjusting the processing order.


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
