# Task 75.1: CommitHistoryAnalyzer Implementation

## Quick Summary
Implement the `CommitHistoryAnalyzer` class that extracts and scores commit history metrics for Git branches. This is a Stage One analyzer—no dependencies on other tasks in this batch.

**Effort:** 24-32 hours | **Complexity:** 7/10 | **Parallelizable:** Yes

---

## What to Build

A Python class `CommitHistoryAnalyzer` that:
1. Extracts commit data for a target branch relative to main/master
2. Computes 5 normalized metrics (0-1 scale)
3. Returns aggregated score weighted by metric importance

### Class Signature
```python
class CommitHistoryAnalyzer:
    def __init__(self, repo_path: str, main_branch: str = "main")
    def analyze(self, branch_name: str) -> dict
```

---

## Metrics to Compute

| Metric | Weight | Description |
|--------|--------|-------------|
| `commit_recency` | 25% | Recent commits weighted higher (exponential decay, 30-day window) |
| `commit_frequency` | 20% | Activity velocity (commits/day over branch lifetime) |
| `authorship_diversity` | 20% | Unique authors count (normalized by total commits) |
| `merge_readiness` | 20% | Commits since last merge to main (closer = higher) |
| `stability_score` | 15% | Inverse of commit churn (% lines changed per commit) |

All metrics normalized to `[0, 1]`.

---

## Input/Output Specification

### Input
- `branch_name` (str): Full branch name (e.g., "feature/auth-system")
- `repo_path` (str): Path to git repository

### Output (dict)
```json
{
  "branch_name": "feature/auth-system",
  "metrics": {
    "commit_recency": 0.87,
    "commit_frequency": 0.65,
    "authorship_diversity": 0.72,
    "merge_readiness": 0.91,
    "stability_score": 0.58
  },
  "aggregate_score": 0.749,
  "commit_count": 42,
  "days_active": 18,
  "unique_authors": 3,
  "analysis_timestamp": "2025-12-22T10:30:00Z"
}
```

---

## Git Commands Reference

```bash
# Get commits unique to branch (not in main)
git log main..BRANCH_NAME --pretty=format:"%H|%ai|%an|%s"

# Get commit diff stats (for stability_score)
git log main..BRANCH_NAME --pretty=format:"%H" | \
  xargs -I {} git diff main...{} --stat

# Get merge base (for merge_readiness)
git merge-base main BRANCH_NAME

# Get commit date
git log -1 --format=%ai BRANCH_NAME
```

---

## Implementation Checklist

- [ ] Initialize with repo validation (check if `.git` exists)
- [ ] Extract commit data with error handling for non-existent branches
- [ ] Implement each metric calculation function
- [ ] Normalize metrics to [0, 1] range with sensible defaults
- [ ] Weight and aggregate metrics
- [ ] Handle edge cases: branches with 0 commits, single commit, new branches
- [ ] Return dict matching output spec exactly
- [ ] Add docstrings (Google style)

---

## Test Cases

1. **Normal branch**: 42 commits, 3 authors, 18 days active
2. **New branch**: 2 commits, 1 author, 1 day old
3. **Stale branch**: 100+ days old, no recent commits
4. **High-activity branch**: 200+ commits, 5+ authors
5. **Non-existent branch**: Should raise `BranchNotFoundError`

---

## Dependencies

- `GitPython` or subprocess calls to `git` CLI
- No internal dependencies on other Task 75.x components
- Output feeds into **Task 75.4 (BranchClusterer)**

---

## Configuration

Accept these parameters in `__init__` or config file:

```python
COMMIT_RECENCY_WEIGHT = 0.25
COMMIT_FREQUENCY_WEIGHT = 0.20
AUTHORSHIP_DIVERSITY_WEIGHT = 0.20
MERGE_READINESS_WEIGHT = 0.20
STABILITY_SCORE_WEIGHT = 0.15
RECENCY_WINDOW_DAYS = 30
```

---

## Next Steps After Completion

1. Unit test with 5+ branch fixtures
2. Integration test with real repo
3. Pass output to Task 75.4 integration point
4. Verify metrics sum to 0-1 range

**Parallel tasks ready:** 75.2, 75.3 (no dependencies)
