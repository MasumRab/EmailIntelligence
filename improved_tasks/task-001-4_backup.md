# Task 001.4: Propose Optimal Targets with Justifications

**Status:** pending
**Priority:** high
**Effort:** 4-5 hours
**Complexity:** 8/10
**Dependencies:** 001.3
**Created:** 2026-01-06
**Parent:** Task 001: Align and Architecturally Integrate Feature Branches with Justified Targets

---

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

## Success Criteria

- [ ] Optimal target proposed for each branch
- [ ] Justification explicit for each choice
- [ ] No default assignments (each justified)
- [ ] Branches needing rename identified
- [ ] Mapping document complete

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
