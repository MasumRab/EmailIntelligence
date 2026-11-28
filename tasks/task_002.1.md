# Task 002.1: CommitHistoryAnalyzer

**Status:** Ready for Implementation
**Priority:** High
**Effort:** 24-32 hours
**Complexity:** 7/10
**Dependencies:** None

---

## Overview/Purpose

Implement the `CommitHistoryAnalyzer` class that extracts and scores commit history metrics for Git branches. This is a Stage One analyzer — one of three independent components (002.1, 002.2, 002.3) that feed into the clustering pipeline (Task 002.4).

**Scope:** CommitHistoryAnalyzer class only
**No dependencies** — can start immediately
**Parallel with:** Task 002.2 (CodebaseStructureAnalyzer), Task 002.3 (DiffDistanceCalculator)

---

## Success Criteria

Task 002.1 is complete when:

### Core Functionality
- [ ] `CommitHistoryAnalyzer` class accepts `repo_path` (str) and `main_branch` (str, default "main")
- [ ] `analyze(branch_name)` extracts commit data using git log commands
- [ ] Computes exactly 5 normalized metrics in [0, 1] range
- [ ] Returns properly formatted dict with all required fields
- [ ] Handles all edge cases (non-existent, new, stale, orphaned branches)
- [ ] Output matches JSON schema exactly

### Quality Assurance
- [ ] Unit tests pass (minimum 8 test cases with >95% coverage)
- [ ] No exceptions raised for valid inputs
- [ ] Performance: <2 seconds per branch analysis
- [ ] Code quality: PEP 8 compliant, Google-style docstrings

### Integration Readiness
- [ ] Output compatible with Task 002.4 (BranchClusterer) downstream requirements
- [ ] Configuration externalized and validated
- [ ] Documentation complete and accurate

---

## Prerequisites & Dependencies

### Required Before Starting
- [ ] Development environment configured (Python 3.8+)
- [ ] Test infrastructure in place (pytest)
- [ ] Access to a git repository with multiple branches for testing

### Blocks (What This Task Unblocks)
- Task 002.4 (BranchClusterer) — consumes this analyzer's output

### External Dependencies
- Python 3.8+
- GitPython or subprocess for git commands
- scipy for numerical operations (optional)

---

## Sub-subtasks Breakdown

### 002.1.1: Design Metric System
**Effort:** 2-3 hours | **Depends on:** None

Define 5 core metrics with mathematical formulas, normalization strategy (ensure [0,1] range), and weighting scheme (0.25/0.20/0.20/0.20/0.15, sum = 1.0). Document edge case handling for each metric.

### 002.1.2: Set Up Git Data Extraction
**Effort:** 4-5 hours | **Depends on:** 002.1.1

Create subprocess-based git command execution. Implement branch validation (check if branch exists). Extract commit log with metadata (dates, authors, messages). Add error handling for invalid branches.

### 002.1.3: Implement Commit Recency Metric
**Effort:** 3-4 hours | **Depends on:** 002.1.2

Extract commit dates, calculate time since last commit, apply exponential decay with 30-day window. Clamp to [0, 1].

### 002.1.4: Implement Commit Frequency Metric
**Effort:** 2-3 hours | **Depends on:** 002.1.2

Calculate commits/day over branch lifetime. Guard against division by zero (min 1 day).

### 002.1.5: Implement Authorship Diversity Metric
**Effort:** 2-3 hours | **Depends on:** 002.1.2

Compute unique_authors / total_commits ratio. Handle single-commit branches.

### 002.1.6: Implement Merge Readiness Metric
**Effort:** 3-4 hours | **Depends on:** 002.1.2

Use `git merge-base` to determine distance from main. Compute 1 - (commits_behind / max_behind). Handle orphaned branches gracefully.

### 002.1.7: Implement Stability Score Metric
**Effort:** 3-4 hours | **Depends on:** 002.1.2

Calculate inverse of commit churn (% lines changed per commit). Normalize against baseline_churn.

### 002.1.8: Aggregate, Test, and Document
**Effort:** 4-6 hours | **Depends on:** 002.1.3–002.1.7

Weight and aggregate all 5 metrics. Write 8+ unit tests. Validate output schema. Write docstrings.

---

## Specification Details

### Class Interface

```python
class CommitHistoryAnalyzer:
    def __init__(self, repo_path: str, main_branch: str = "main")
    def analyze(self, branch_name: str) -> dict
```

### Metrics Definitions

| Metric | Weight | Formula | Notes |
|--------|--------|---------|-------|
| `commit_recency` | 25% | `exp(-days_since_last / 30)` | 30-day window, exponential decay |
| `commit_frequency` | 20% | `commits / max(1, branch_lifetime_days)` | Guard div-by-zero |
| `authorship_diversity` | 20% | `unique_authors / total_commits` | Ratio metric |
| `merge_readiness` | 20% | `1 - (commits_behind_main / max_behind)` | Inverse normalized |
| `stability_score` | 15% | `1 - (avg_churn / baseline_churn)` | Inverse churn |

### Output JSON Schema

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

## Implementation Guide

### Step 1: Repository Validation
```python
def __init__(self, repo_path: str, main_branch: str = "main"):
    if not os.path.exists(os.path.join(repo_path, ".git")):
        raise ValueError(f"Not a git repository: {repo_path}")
    self.repo_path = repo_path
    self.main_branch = main_branch
```

### Step 2: Git Data Extraction
```python
def _run_git(self, *args, timeout=30) -> str:
    result = subprocess.run(
        ["git", "-C", self.repo_path] + list(args),
        capture_output=True, text=True, timeout=timeout
    )
    if result.returncode != 0:
        raise GitCommandError(result.stderr)
    return result.stdout.strip()
```

### Step 3: Commit Recency
```python
def _commit_recency(self, branch_name: str) -> float:
    date_str = self._run_git("log", "-1", "--format=%ai", branch_name)
    last_commit = datetime.fromisoformat(date_str.strip())
    days = (datetime.now(timezone.utc) - last_commit).days
    return min(1.0, math.exp(-days / RECENCY_WINDOW_DAYS))
```

### Step 4: Remaining Metrics
Implement `_commit_frequency`, `_authorship_diversity`, `_merge_readiness`, `_stability_score` following the formulas in the Specification Details section.

### Step 5: Aggregation
```python
def analyze(self, branch_name: str) -> dict:
    metrics = {
        "commit_recency": self._commit_recency(branch_name),
        "commit_frequency": self._commit_frequency(branch_name),
        "authorship_diversity": self._authorship_diversity(branch_name),
        "merge_readiness": self._merge_readiness(branch_name),
        "stability_score": self._stability_score(branch_name),
    }
    weights = [0.25, 0.20, 0.20, 0.20, 0.15]
    aggregate = sum(m * w for m, w in zip(metrics.values(), weights))
    return {"branch_name": branch_name, "metrics": metrics, "aggregate_score": round(aggregate, 3), ...}
```

### Step 6: Unit Tests
Write tests for all 5 test cases listed below plus 3 additional edge cases.

---

## Configuration & Defaults

```python
COMMIT_RECENCY_WEIGHT = 0.25
COMMIT_FREQUENCY_WEIGHT = 0.20
AUTHORSHIP_DIVERSITY_WEIGHT = 0.20
MERGE_READINESS_WEIGHT = 0.20
STABILITY_SCORE_WEIGHT = 0.15
RECENCY_WINDOW_DAYS = 30
```

Load via `config/task_002_clustering.yaml` or constructor parameters.

---

## Typical Development Workflow

```bash
git checkout -b feature/002.1-commit-history-analyzer
# Implement class in src/analyzers/commit_history.py
# Write tests in tests/test_commit_history.py
pytest tests/test_commit_history.py -v --cov=src/analyzers/commit_history
# Verify output schema against specification
python -c "from src.analyzers.commit_history import CommitHistoryAnalyzer; print(CommitHistoryAnalyzer('.').analyze('main'))"
git add -A && git commit -m "feat: complete Task 002.1 CommitHistoryAnalyzer"
```

---

## Integration Handoff

**Downstream:** Task 002.4 (BranchClusterer) consumes the output dict directly.

**Contract:** The `analyze()` return dict must contain exactly the keys shown in the Output JSON Schema. Task 002.4 reads `metrics` and `aggregate_score`.

**Parallel with:** Task 002.2 (CodebaseStructureAnalyzer), Task 002.3 (DiffDistanceCalculator) — no cross-dependencies.

---

## Common Gotchas & Solutions

**Gotcha 1: Metrics outside [0,1] range**
```python
# WRONG
recency = math.exp(-days / 30)  # Can be slightly > 1.0 due to float precision

# RIGHT
recency = min(1.0, math.exp(-days / 30))
assert 0 <= recency <= 1, f"Metric out of range: {recency}"
```

**Gotcha 2: Division by zero**
```python
# WRONG
frequency = commits / days_active  # Crashes if days_active = 0

# RIGHT
days_active = max(1, days_active)
frequency = commits / days_active
```

**Gotcha 3: Git timeout on large repos**
```python
# WRONG
result = subprocess.run(cmd, ...)  # No timeout

# RIGHT
result = subprocess.run(cmd, timeout=30, ...)
```

**Gotcha 4: Non-ASCII author names**
```python
# WRONG
author = output.decode('utf-8')  # May fail

# RIGHT
author = output.decode('utf-8', errors='replace')
```

---

## Integration Checkpoint

**When to move to Task 002.4 (BranchClusterer):**

- [ ] All 8 sub-subtasks complete
- [ ] Unit tests passing (>95% coverage)
- [ ] Output matches specification exactly
- [ ] No validation errors on test data
- [ ] Performance targets met (<2s per branch)
- [ ] Edge cases handled correctly
- [ ] Code review approved
- [ ] Commit message: `feat: complete Task 002.1 CommitHistoryAnalyzer`

---

## Done Definition

Task 002.1 is done when:

1. All 8 sub-subtasks marked complete
2. Unit tests pass (>95% coverage) on CI/CD
3. Code review approved
4. Outputs match specification exactly
5. Output schema validation passes
6. Documentation complete and accurate
7. Performance benchmarks met (<2s per branch)
8. Ready for hand-off to Task 002.4
9. Commit: `feat: complete Task 002.1 CommitHistoryAnalyzer`
10. All success criteria checkboxes marked complete

---

## Provenance

- **Primary source:** HANDOFF_75.1_CommitHistoryAnalyzer.md (archived: task_data/migration_backup_20260129/task_data_original/archived/handoff_archive_task75/)
- **Structure standard:** TASK_STRUCTURE_STANDARD.md (approved January 6, 2026)
- **ID mapping:** 75.1 → 002.1 (migration performed January 29, 2026)
- **Test cases:** 5 scenarios from HANDOFF_75.1 (Normal, New, Stale, High-activity, Non-existent)
- **Git commands:** 4 commands from HANDOFF_75.1 Git Commands Reference section

## Performance Targets

[Performance targets to be defined]


## Testing Strategy

[Testing strategy to be defined]


## Next Steps

[Next steps to be defined]
