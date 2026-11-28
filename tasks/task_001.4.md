# Task 001.4: Assign and Justify an Integration Target per Branch

**Status:** specified
**Priority:** high
**Effort:** 4-5 hours
**Complexity:** 8/10
**Dependencies:** 001.3

---

## Overview/Purpose

Apply criteria to each branch and propose optimal integration targets with explicit, documented justification for each choice.

## Success Criteria

- [ ] Optimal target proposed for each branch
- [ ] Justification explicit for each choice
- [ ] No default assignments (each justified)
- [ ] Branches needing rename identified
- [ ] Mapping document complete

## Prerequisites & Dependencies

### Required Before Starting
- [ ] No external prerequisites

### Blocks (What This Task Unblocks)
- [ ] No specific blocks defined

### External Dependencies
- [ ] No external dependencies

## Sub-subtasks Breakdown


## Specification Details

### Task Interface
- **ID**: 001.4
- **Title**: Assign and Justify an Integration Target per Branch
- **Status**: specified
- **Priority**: high
- **Effort**: 4-5 hours
- **Complexity**: 8/10

### Requirements
1. Every branch in `docs/branch-inventory.json` has exactly one assigned target, or the explicit
   value `defer` with a reason.
2. Each assignment cites the criteria from `TARGET_SELECTION_CRITERIA.md` by number and the evidence
   that satisfies them, so a reviewer can re-derive the decision.
3. No assignment rests on the branch's name alone. A branch called `fix/*` is not assigned to `main`
   because of the prefix.
4. Branches that fail every criterion are collected in one section with what would have to change for
   them to qualify.
5. The output is appended to `ALIGNMENT_CHECKLIST.md` as a table, not written to a new document.

## Implementation Guide

Append a table to the existing `ALIGNMENT_CHECKLIST.md` (it already exists at the root and is the
document the parent task names as the deliverable). One row per branch:
`branch | head sha | target | criteria met | evidence command | risk`.

```bash
python scripts/alignment/branch_similarity.py --inventory docs/branch-inventory.json \
    --targets main scientific orchestration-tools > /tmp/sim.json
```


## Purpose

Apply criteria to each branch and propose optimal integration targets with explicit, documented justification for each choice.

---

## Details

This subtask takes the analysis from 001.2 and criteria from 001.3 to propose specific integration targets for each feature branch. Every assignment must have explicit justification.

### Steps

1. **Apply criteria to each branch from 001.1 list**
   - Run automated scoring using 001.3 criteria
   - Calculate scores for each target (main/scientific/orchestration)

2. **Determine proposed optimal target**
   - Select highest-scoring target
   - Document score breakdown
   - Flag any ties or near-ties

3. **Document justification for each choice**
   - Primary reason for selection
   - Supporting evidence
   - Alternative considered and rejected
   - Any concerns or risks

4. **Identify branches needing renaming**
   - Ambiguous names (feature-scientific-X targeting main)
   - Conflicting content (name says scientific, code targets main)
   - Suggestion for new name

5. **Create comprehensive mapping document**

---

## Test Strategy

- Review all justifications for completeness
- Verify no arbitrary assignments
- Validate against Task 002 analysis
- Cross-check with historical patterns

---

## Implementation Notes

### Justification Template

```markdown
## Branch: feature/example

**Proposed Target:** main

**Score Breakdown:**
- Main: 85/100
- Scientific: 60/100
- Orchestration: 30/100

**Primary Justification:**
Branch has 75% shared history with main, all tests passing, and
modifies only core modules that exist in main. No research or
experimental work identified.

**Supporting Evidence:**
- 42 commits, 28 days active
- Files changed: src/core/ (12), tests/ (8)
- No new dependencies added

**Alternative Considered:**
- Scientific: Rejected - no research scope, stable and complete

**Concerns/Risks:**
None identified
```

### Branches Requiring Renaming

| Current Name | Content Analysis | Proposed Rename |
|--------------|------------------|-----------------|
| feature-scientific-X | Targets main | feature/integration-X |
| feature-main-Y | Has research code | feature/research-Y |

---

## Common Gotchas

### Gotcha 1: Analysis paralysis
```
Problem: Too much time spent on edge cases

Solution: Set time limit per branch (15 min max)
Escalate unresolved to team review
```

### Gotcha 2: Defaulting to scientific
```
Problem: Using scientific as default without justification

Solution: Rule: Every branch must have explicit non-scientific justification
if assigned to scientific
```

### Gotcha 3: Name-content mismatch
```
Problem: Branch name suggests one target, content suggests another

Solution: Document mismatch in rename recommendations
Use content-based assignment, not name-based
```

---

## Progress Log

### 2026-01-06
- Subtask file created from Task 001 template
- Ready for implementation

---

## Next Steps

After completion, proceed to **Task 001.5**: Create ALIGNMENT_CHECKLIST.md
**Priority:** high
**Effort:** 4-5 hours
**Complexity:** 8/10
**Dependencies:** 001.3
**Created:** 2026-01-06
**Parent:** Task 001: Align and Architecturally Integrate Feature Branches with Justified Targets

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

### Unit Tests
- [ ] Tests cover core functionality
- [ ] Edge cases handled appropriately
- [ ] Performance benchmarks met

### Integration Tests
- [ ] Integration with dependent components verified
- [ ] End-to-end workflow tested
- [ ] Error handling verified

### Test Strategy Notes
- Review all justifications for completeness
- Verify no arbitrary assignments
- Validate against Task 002 analysis
- Cross-check with historical patterns

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
