# Task 001.6: Choose Between Merge and Rebase per Branch

**Status:** specified
**Priority:** medium
**Effort:** 3-4 hours
**Complexity:** 6/10
**Dependencies:** 001.3

---

## Overview/Purpose

Document the strategy for choosing between `git merge` and `git rebase` based on branch characteristics and team workflows.

## Success Criteria

- [ ] Merge vs rebase decision criteria defined
- [ ] Strategy documented for each branch type
- [ ] Conflict resolution procedures specified
- [ ] Visual merge tool usage documented
- [ ] Safety mechanisms defined

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
- **ID**: 001.6
- **Title**: Choose Between Merge and Rebase per Branch
- **Status**: specified
- **Priority**: medium
- **Effort**: 3-4 hours
- **Complexity**: 6/10

### Requirements
1. The strategy document gives one deciding rule per case: reproducible history vs. conflict cost,
   and names the observation that selects it.
2. For a branch that has already been pushed and reviewed, the rule accounts for the published SHAs
   that a rebase destroys; the rule is not "rebase when the branch is small".
3. Each rule states the exact command it implies and whether that command needs `--force-with-lease`.
4. The document names the situations where neither applies and the branch must be re-cut from the
   target instead.
5. The rule is expressible as a one-line predicate over the inventory, so the choice can be automated
   for 100+ branches.

## Implementation Guide

Write the decision table into the strategy section of `TARGET_SELECTION_CRITERIA.md`, and add a
`--strategy` flag to `scripts/alignment/render_checklist.py` that emits `merge` or `rebase` per row.
The repository forbids plain force-push and uses `--force-with-lease` where a rewrite is required;
state that in the table rather than leaving it to the operator.

```bash
git log --oneline --merges origin/main..<branch> | wc -l
```


## Purpose

Document the strategy for choosing between `git merge` and `git rebase` based on branch characteristics and team workflows.

---

## Details

This subtask establishes guidelines for selecting the appropriate Git operation (merge vs rebase) for each branch alignment scenario.

### Steps

1. **Document when to use merge**
   - Preserve complete history
   - Large team collaboration
   - Public/shared branches
   - Audit trail importance

2. **Document when to use rebase**
   - Clean linear history desired
   - Small team or solo work
   - Private feature branches
   - Before squash merge

3. **Define strategy per branch type**
   - Feature branches → rebase (typically)
   - Long-running branches → merge
   - Documentation → rebase
   - Core changes → evaluate case-by-case

4. **Document conflict resolution procedures**
   - Interactive rebase workflow
   - Merge conflict handling
   - Visual merge tool integration

5. **Specify when to use visual merge tools**
   - Complex multi-file conflicts
   - Binary file changes
   - Three-way merge scenarios

---

## Test Strategy

- Apply to sample branches
- Review decision logic
- Validate against best practices
- Test conflict resolution flow

---

## Implementation Notes

### Decision Matrix

| Branch Type | Recommended | Rationale | Exceptions |
|-------------|-------------|-----------|------------|
| Feature (short-lived) | Rebase | Clean history, easy review | Large teams → merge |
| Feature (long-lived) | Merge | Preserve collaboration history | - |
| Documentation | Rebase | Simple changes, single author | - |
| Bug fix | Rebase | Quick integration | Hotfix → merge |
| Core changes | Evaluate | Depends on scope | - |
| Research/experiment | Rebase | Can be abandoned easily | - |

### Command Reference

```bash
# Rebase workflow
git checkout feature-branch
git fetch origin
git rebase origin/main
# Resolve conflicts
git add .
git rebase --continue

# Merge workflow
git checkout main
git merge --no-ff feature-branch
# Resolve conflicts
git commit -m "Merge feature-branch"

# Squash merge
git merge --squash feature-branch
git commit -m "feat: add feature (closes #123)"
```

### Conflict Resolution

| Scenario | Tool | Command |
|----------|------|---------|
| Simple conflicts | Editor | `git mergetool` |
| Complex conflicts | GUI | `git mergetool --tool=vscode` |
| Three-way merge | CLI | `git merge -Xignore-space-change` |

---

## Common Gotchas

### Gotcha 1: Rewriting public history
```
Problem: Rebasing shared/remote branch

Solution: Never rebase published branches
Only rebase local or private branches
```

### Gotcha 2: Merge bubbles
```
Problem: Excessive merge commits cluttering history

Solution: Use rebase before merge
Consider --no-ff for feature branches
```

### Gotcha 3: Lost commits
```
Problem: Rebase resulted in lost work

Solution: Use reflog to recover
git reflog
git checkout HEAD@{1}
```

---

## Progress Log

### 2026-01-06
- Subtask file created from Task 001 template
- Ready for implementation

---

## Next Steps

After completion, proceed to **Task 001.7**: Create Architectural Prioritization Guidelines
**Priority:** medium
**Effort:** 3-4 hours
**Complexity:** 6/10
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
- Apply to sample branches
- Review decision logic
- Validate against best practices
- Test conflict resolution flow

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
