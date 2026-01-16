# Task 001.6: Define Merge vs Rebase Strategy

**Status:** pending
**Priority:** medium
**Effort:** 3-4 hours
**Complexity:** 6/10
**Dependencies:** 001.3
**Created:** 2026-01-06
**Parent:** Task 001: Align and Architecturally Integrate Feature Branches with Justified Targets

---

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

## Success Criteria

- [ ] Merge vs rebase decision criteria defined
- [ ] Strategy documented for each branch type
- [ ] Conflict resolution procedures specified
- [ ] Visual merge tool usage documented
- [ ] Safety mechanisms defined

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
