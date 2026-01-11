# Task 001.2: Analyze Git History and Codebase Similarity

**Status:** pending
**Priority:** high
**Effort:** 4-5 hours
**Complexity:** 7/10
**Dependencies:** 001.1
**Created:** 2026-01-06
**Parent:** Task 001: Align and Architecturally Integrate Feature Branches with Justified Targets

---

## Purpose

Analyze Git history and codebase structure for each branch to support target determination.

---

## Details

This subtask performs detailed analysis of each active feature branch, examining commit history patterns and codebase structure to inform integration target selection.

### Steps

1. **Extract Git history for each branch**
   ```bash
   for branch in $(cat active_branches.txt); do
     echo "=== $branch ==="
     git log --oneline --since="1 year ago" origin/$branch
     git log --format="%H %ai %an" origin/$branch | head -5
   done
   ```

2. **Calculate shared commits with primary targets**
   ```bash
   # Find merge base between feature branch and each primary branch
   git merge-base origin/feature-branch origin/main
   git merge-base origin/feature-branch origin/scientific
   git merge-base origin/feature-branch origin/orchestration-tools
   ```

3. **Analyze file-level codebase similarity**
   ```bash
   # Compare file structures
   git ls-tree -r --name-only origin/$branch | sort > branch_files.txt
   git ls-tree -r --name-only origin/main | sort > main_files.txt
   diff branch_files.txt main_files.txt
   ```

4. **Assess architectural alignment**
   - Identify modified directories
   - Detect changes to core modules
   - Map imports and dependencies
   - Evaluate architectural patterns

5. **Document findings for each branch**

---

## Success Criteria

- [ ] Git history analysis complete for all branches
- [ ] Shared commit counts documented
- [ ] Codebase similarity metrics calculated
- [ ] Architectural assessment recorded
- [ ] Data ready for target assignment

---

## Test Strategy

- Verify analysis on sample branches
- Compare manual analysis with automated output
- Validate similarity calculations
- Cross-check merge base calculations

---

## Implementation Notes

### Metrics to Calculate

| Metric | Description | Calculation |
|--------|-------------|-------------|
| Commit count | Total commits on branch | `git rev-list --count origin/$branch` |
| Days active | First to last commit | `git log --format=%ai \| tail -1` / `head -1` |
| Shared commits | Commits in common with target | `git merge-base --count origin/$branch origin/target` |
| Changed files | Files modified on branch | `git diff --name-only origin/main...origin/$branch` |
| Added files | New files on branch | Compare `git ls-tree` outputs |

### Output Format

```json
{
  "branch": "feature/example",
  "metrics": {
    "commit_count": 42,
    "days_active": 28,
    "shared_with_main": 15,
    "shared_with_scientific": 8,
    "shared_with_orchestration": 3,
    "files_changed": 12,
    "files_added": 5
  },
  "analysis": {
    "primary_target": "main",
    "confidence": 0.85,
    "rationale": "75% shared history with main"
  }
}
```

---

## Common Gotchas

### Gotcha 1: Detached HEAD
```
Problem: Cannot analyze branch when in detached HEAD state

Solution: Checkout the branch locally first
git checkout origin/$branch -b local-$branch
```

### Gotcha 2: Large repositories
```
Problem: Analysis takes too long

Solution: Optimize with shallow clones for initial analysis
git fetch --depth=100 origin/$branch
```

### Gotcha 3: Missing merge bases
```
Problem: Branches with no common history

Solution: Document as "no shared history" - unique branch
```

---

## Progress Log

### 2026-01-06
- Subtask file created from Task 001 template
- Ready for implementation

---

## Next Steps

After completion, proceed to **Task 001.3**: Define Target Selection Criteria
