# Task 001.3: Define Integration Target Selection Criteria

**Status:** specified
**Priority:** high
**Effort:** 3-4 hours
**Complexity:** 7/10
**Dependencies:** 001.2

---

## Overview/Purpose

Define explicit, reproducible criteria for selecting integration targets (main, scientific, orchestration-tools).

## Success Criteria

- [ ] All target selection criteria documented
- [ ] Criteria measurable and reproducible
- [ ] Decision tree clear and unambiguous
- [ ] Examples provided for each target type
- [ ] Ready for application to all branches

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
- **ID**: 001.3
- **Title**: Define Integration Target Selection Criteria
- **Status**: specified
- **Priority**: high
- **Effort**: 3-4 hours
- **Complexity**: 7/10

### Requirements
1. `TARGET_SELECTION_CRITERIA.md` states, for each of `main`, `scientific` and `orchestration-tools`,
   what belongs on that branch in one sentence, so a reader can classify a branch without reading the
   rest of the document.
2. Each criterion is decidable from repository evidence -- a path, a commit range, a file-set
   overlap -- and names the command that produces the evidence.
3. The criteria are ordered, and the document says what to do when two criteria disagree.
4. A worked example applies the criteria to one real branch end to end.
5. The document names the failure mode it exists to prevent: a branch assigned to a target because
   that is where its file paths look familiar, which is how `scientific` accumulated 138 PRs.

## Implementation Guide

Edit the existing `TARGET_SELECTION_CRITERIA.md` at the repository root rather than creating a new
document; it already holds the early draft. Ground each criterion in the repository as it exists at
`71b9bcbe8`: `src/` for application code, `scripts/` for tooling, `.github/workflows/ci.yml` for what
CI actually checks. Confirm every path with `git ls-tree -r --name-only HEAD -- <path>` before
citing it.

```bash
git show HEAD:TARGET_SELECTION_CRITERIA.md | head -40
```


## Purpose

Define explicit, reproducible criteria for selecting integration targets (main, scientific, orchestration-tools).

---

## Details

This subtask establishes the decision framework that will be used to assign each feature branch to its optimal integration target. Criteria must be measurable and reproducible.

### Steps

1. **Define main branch targeting criteria**
   - Stability requirements
   - Completeness standards
   - Quality thresholds
   - Shared history expectations
   - Dependency satisfaction

2. **Define scientific branch targeting criteria**
   - Research/experimentation scope
   - Innovation tolerance
   - Stability expectations
   - History requirements
   - Architecture flexibility

3. **Define orchestration-tools targeting criteria**
   - Infrastructure focus
   - Orchestration specificity
   - Core module changes
   - Parallel safety requirements
   - Integration needs

4. **Document criteria weights and priorities**
   - Primary criteria (must have)
   - Secondary criteria (should have)
   - Tertiary criteria (nice to have)

5. **Create decision tree for target assignment**

---

## Test Strategy

- Apply criteria to sample branches
- Verify reproducible results
- Review decision logic completeness
- Validate against historical assignments

---

## Implementation Notes

### Main Branch Criteria

| Criterion | Weight | Threshold | Description |
|-----------|--------|-----------|-------------|
| Stability | High | >90% tests passing | Code is production-ready |
| Completeness | High | Feature complete | All planned features implemented |
| Test Coverage | Medium | >90% | Comprehensive test suite |
| Shared History | High | >50% commits shared | Significant overlap with main |
| Dependencies | High | All in main | No external dependencies |

### Scientific Branch Criteria

| Criterion | Weight | Threshold | Description |
|-----------|--------|-----------|-------------|
| Research Scope | High | Yes/No | Exploratory work identified |
| Innovation | Medium | Yes/No | New approaches being tried |
| Stability | Low | >70% tests | Acceptable for research |
| History | Low | Any | Limited shared history OK |
| Architecture | Low | Any | Divergence from main OK |

### Orchestration-Tools Criteria

| Criterion | Weight | Threshold | Description |
|-----------|--------|-----------|-------------|
| Infrastructure | High | Yes/No | Deployment/configuration focus |
| Core Changes | High | Yes/No | setup.py or orchestration files modified |
| Parallel Safety | Medium | Yes/No | Special execution requirements |
| Integration | Medium | Yes/No | Orchestration system integration |

### Decision Tree

```
Branch has infrastructure changes?
├── Yes → orchestration-tools
└── No
    ├── Research/experimentation focus?
    │   ├── Yes → scientific
    │   └── No
    │       ├── >50% shared with main AND stable?
    │       │   ├── Yes → main
    │       │   └── No → Analyze further
    │       └── Default → scientific (must justify)
```

---

## Common Gotchas

### Gotcha 1: Ambiguous criteria
```
Problem: Criteria too vague, different analysts get different results

Solution: Quantify criteria with specific thresholds
```

### Gotcha 2: Defaulting to scientific
```
Problem: All branches assigned to scientific by default

Solution: Rule: Each branch requires explicit justification
If target is scientific by default, require additional analysis
```

### Gotcha 3: Circular reasoning
```
Problem: Branch targeting affects its own categorization

Solution: Analyze based on current state, not intended changes
```

---

## Progress Log

### 2026-01-06
- Subtask file created from Task 001 template
- Ready for implementation

---

## Next Steps

After completion, proceed to **Task 001.4**: Propose Optimal Targets with Justifications
**Priority:** high
**Effort:** 3-4 hours
**Complexity:** 7/10
**Dependencies:** 001.2
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
- Apply criteria to sample branches
- Verify reproducible results
- Review decision logic completeness
- Validate against historical assignments

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
