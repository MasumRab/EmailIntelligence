# Task 001.1: Identify All Active Feature Branches

**Status:** pending
**Priority:** high
**Effort:** 2-3 hours
**Complexity:** 4/10
**Dependencies:** None
**Created:** 2026-01-06
**Parent:** Task 001: Align and Architecturally Integrate Feature Branches with Justified Targets

---

## Purpose

Identify and catalog all active feature branches that need alignment analysis.

---

## Details

This subtask focuses on discovering and documenting all active feature branches in the repository that require alignment assessment. The goal is to create a comprehensive inventory that will be used throughout Tasks 001.2-001.8.

### Steps

1. **List all remote branches**
   ```bash
   git fetch --all --prune
   git branch -r | grep -v '->' | sort
   ```

2. **Identify feature branches**
   - Look for patterns: `feature/*`, `docs/*`, `fix/*`, `enhancement/*`
   - Exclude: `main`, `scientific`, `orchestration-tools`, `HEAD`

3. **Filter out merged branches**
   ```bash
   for branch in $(git branch -r --format='%(refname:short)' | grep feature); do
     if git merge-base --is-ancestor $(git rev-parse $branch) HEAD; then
       echo "Merged: $branch"
     else
       echo "Active: $branch"
     fi
   done
   ```

4. **Document branch metadata**
   - Branch name
   - Creation date (from first commit)
   - Last activity date
   - Author(s)
   - Current status (active/stale)

5. **Create initial list for further analysis**

---

## Success Criteria

- [ ] Complete list of active feature branches created
- [ ] All branches documented with branch names and creation dates
- [ ] Excluded merged branches identified
- [ ] List ready for assessment phase

---

## Test Strategy

- Verify branch list matches `git branch -r` output
- Confirm merged branches correctly excluded
- Validate metadata completeness
- Cross-check with GitHub/GitLab UI

---

## Implementation Notes

### Branch Categories to Include

| Category | Pattern | Include? |
|----------|---------|----------|
| Feature branches | `feature/*` | Yes |
| Documentation | `docs/*` | Yes |
| Enhancements | `enhancement/*` | Yes |
| Bug fixes | `fix/*` | Yes |
| Main branches | `main`, `scientific`, `orchestration-tools` | No |
| Remote tracking | `HEAD` | No |
| Merged branches | Check with `git merge-base` | No |

### Specific Branches to Identify

- `feature/backlog-ac-updates`
- `docs-cleanup`
- `feature/search-in-category`
- `feature/merge-clean`
- `feature/merge-setup-improvements`

### Specific Branches to Exclude

- `fix/import-error-corrections` (handled by Task 011)

---

## Common Gotchas

### Gotcha 1: Shallow clones
```
Problem: git log missing history for some branches

Solution: Ensure repository is not a shallow clone
git fetch --unshallow
```

### Gotcha 2: Stale remote references
```
Problem: Deleted branches still appearing

Solution: Prune stale references
git remote prune origin
```

### Gotcha 3: Multiple origins
```
Problem: Branches from different remotes missed

Solution: Fetch from all remotes
git fetch --all
```

---

## Progress Log

### 2026-01-06
- Subtask file created from Task 001 template
- Ready for implementation

---

## Next Steps

After completion, proceed to **Task 001.2**: Analyze Git History and Codebase Similarity
