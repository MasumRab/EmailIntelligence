# Task 002.3: DiffDistanceCalculator

**Status:** Ready for Implementation
**Priority:** High
**Effort:** 32-40 hours
**Complexity:** 8/10
**Dependencies:** None

---

## Overview/Purpose

Implement the `DiffDistanceCalculator` class that computes code distance metrics between branches using diff analysis. This is a Stage One analyzer — one of three independent components (002.1, 002.2, 002.3) that feed into the clustering pipeline (Task 002.4).

**Scope:** DiffDistanceCalculator class only
**No dependencies** — can start immediately
**Parallel with:** Task 002.1 (CommitHistoryAnalyzer), Task 002.2 (CodebaseStructureAnalyzer)

---

## Success Criteria

Task 002.3 is complete when:

### Core Functionality
- [ ] `DiffDistanceCalculator` class accepts `repo_path` (str) and `main_branch` (str, default "main")
- [ ] `analyze(branch_name)` computes detailed diff metrics between branch and main
- [ ] Computes exactly 4 normalized metrics in [0, 1] range
- [ ] Returns properly formatted dict with all required fields including line counts
- [ ] Handles all edge cases (binary files, large diffs, deleted files, merge commits, no diff)
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
- Python 3.8+ (built-in `re` for file pattern matching)
- GitPython or subprocess for git commands

---

## Sub-subtasks Breakdown

### 002.3.1: Design Metric System and Risk Categories
**Effort:** 3-4 hours | **Depends on:** None

Define 4 core metrics with mathematical formulas. Document RISKY_FILE_PATTERNS categories (critical/high/medium/low) with risk weights (0.8/0.5/0.2/0.05). Define weighting scheme (0.30/0.25/0.25/0.20, sum = 1.0).

### 002.3.2: Set Up Diff Data Extraction
**Effort:** 4-5 hours | **Depends on:** 002.3.1

Parse `git diff main...BRANCH --numstat` output (tab-separated: added, deleted, filepath). Handle binary files (marked as `-` in numstat). Extract `--stat` and `--compact-summary` for supplementary data.

### 002.3.3: Implement Code Churn Metric
**Effort:** 4-5 hours | **Depends on:** 002.3.2

Calculate total_changes = lines_added + lines_deleted. Compute churn_ratio = total_changes / ESTIMATED_CODEBASE_SIZE. Apply inversion: `max(0, 1 - min(churn_ratio, 1.0))`. Lower churn = higher score.

### 002.3.4: Implement Change Concentration Metric
**Effort:** 3-4 hours | **Depends on:** 002.3.2

Count unique files changed. Normalize by MAX_EXPECTED_FILES. Apply inversion: fewer files = higher score.

### 002.3.5: Implement Diff Complexity Metric
**Effort:** 5-6 hours | **Depends on:** 002.3.2

Calculate largest_file_change / avg_file_change ratio. High concentration in few files = higher complexity. Cap at 1.0 via `min(concentration_ratio / 3, 1.0)`.

### 002.3.6: Implement Integration Risk Metric
**Effort:** 5-6 hours | **Depends on:** 002.3.2

Pattern-match affected files against RISKY_FILE_PATTERNS. Apply risk weights per category. Normalize: `1 - (risk_score / files_affected)`. Lower risk = higher score.

### 002.3.7: Aggregate, Test, and Document
**Effort:** 6-8 hours | **Depends on:** 002.3.3–002.3.6

Weight and aggregate all 4 metrics. Write 8+ unit tests. Validate output schema. Handle all edge cases. Write docstrings.

---

## Specification Details

### Class Interface

```python
class DiffDistanceCalculator:
    def __init__(self, repo_path: str, main_branch: str = "main")
    def analyze(self, branch_name: str) -> dict
```

### Metrics Definitions

| Metric | Weight | Formula | Notes |
|--------|--------|---------|-------|
| `code_churn` | 30% | `max(0, 1 - min((added+deleted)/codebase_size, 1.0))` | Inverse churn |
| `change_concentration` | 25% | `1 - min(files_affected/50, 1.0)` | Fewer files = higher |
| `diff_complexity` | 25% | `min(largest_change/avg_change / 3, 1.0)` | Concentration ratio |
| `integration_risk` | 20% | `1 - (weighted_risk_score / files_affected)` | Lower risk = higher |

### Metric Calculation Details

**Code Churn:**
```
total_changes = lines_added + lines_deleted
estimated_codebase_size = 5000  # Configurable baseline
churn_ratio = total_changes / estimated_codebase_size
metric = max(0, 1 - min(churn_ratio, 1.0))
```

**Change Concentration:**
```
files_affected = count of unique files changed
max_expected_files = 50
concentration = min(files_affected / max_expected_files, 1.0)
metric = 1 - concentration
```

**Diff Complexity:**
```
largest_file_change = max(changes per file)
avg_file_change = total_changes / files_affected
concentration_ratio = largest_file_change / avg_file_change
metric = min(concentration_ratio / 3, 1.0)
```

**Integration Risk:**
```
risk_score = sum of risk weights for affected files
  Critical files: 0.8 weight per file
  High risk: 0.5 weight per file
  Medium: 0.2 weight per file
  Low: 0.05 weight per file
normalized_risk = risk_score / files_affected
metric = 1 - normalized_risk
```

### Risk Category Files

```python
RISKY_FILE_PATTERNS = {
    "critical": [
        "config/", "settings/", ".env", "secrets",
        "core/", "main.py", "__init__.py"
    ],
    "high": [
        "tests/", "test_*.py", "*_test.py",
        "setup.py", "requirements.txt", "pyproject.toml"
    ],
    "medium": [
        "src/", "lib/", "utils/"
    ],
    "low": [
        "docs/", "README", "examples/"
    ]
}
```

### Output JSON Schema

```json
{
  "branch_name": "feature/auth-system",
  "metrics": {
    "code_churn": 0.72,
    "change_concentration": 0.81,
    "diff_complexity": 0.68,
    "integration_risk": 0.79
  },
  "aggregate_score": 0.750,
  "total_lines_added": 342,
  "total_lines_deleted": 87,
  "total_lines_changed": 429,
  "files_affected": 12,
  "largest_file_change": 156,
  "analysis_timestamp": "2025-12-22T10:40:00Z"
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

### Step 2: Numstat Parsing
```python
def _parse_numstat(self, branch_name: str) -> list[dict]:
    output = self._run_git("diff", f"{self.main_branch}...{branch_name}", "--numstat")
    results = []
    for line in output.splitlines():
        parts = line.split("\t")
        if len(parts) == 3:
            added, deleted, filepath = parts
            if added == "-":  # Binary file
                continue
            results.append({"added": int(added), "deleted": int(deleted), "filepath": filepath})
    return results
```

### Step 3: Risk Classification
```python
def _classify_risk(self, filepath: str) -> str:
    for category, patterns in RISKY_FILE_PATTERNS.items():
        for pattern in patterns:
            if pattern.endswith("/") and filepath.startswith(pattern):
                return category
            elif fnmatch.fnmatch(filepath, pattern) or filepath == pattern:
                return category
    return "low"
```

### Step 4: Implement Each Metric
Follow formulas in the Metric Calculation Details section for `_code_churn`, `_change_concentration`, `_diff_complexity`, `_integration_risk`.

### Step 5: Aggregation
```python
def analyze(self, branch_name: str) -> dict:
    file_stats = self._parse_numstat(branch_name)
    metrics = {
        "code_churn": self._code_churn(file_stats),
        "change_concentration": self._change_concentration(file_stats),
        "diff_complexity": self._diff_complexity(file_stats),
        "integration_risk": self._integration_risk(file_stats),
    }
    weights = [0.30, 0.25, 0.25, 0.20]
    aggregate = sum(m * w for m, w in zip(metrics.values(), weights))
    total_added = sum(f["added"] for f in file_stats)
    total_deleted = sum(f["deleted"] for f in file_stats)
    return {
        "branch_name": branch_name, "metrics": metrics,
        "aggregate_score": round(aggregate, 3),
        "total_lines_added": total_added, "total_lines_deleted": total_deleted,
        "total_lines_changed": total_added + total_deleted,
        "files_affected": len(file_stats),
        "largest_file_change": max((f["added"]+f["deleted"] for f in file_stats), default=0),
        "analysis_timestamp": datetime.now(timezone.utc).isoformat(),
    }
```

---

## Configuration & Defaults

```python
CODE_CHURN_WEIGHT = 0.30
CHANGE_CONCENTRATION_WEIGHT = 0.25
DIFF_COMPLEXITY_WEIGHT = 0.25
INTEGRATION_RISK_WEIGHT = 0.20

ESTIMATED_CODEBASE_SIZE = 5000    # Baseline for churn normalization
MAX_EXPECTED_FILES = 50           # Ceiling for concentration normalization

RISKY_FILE_PATTERNS = {
    "critical": ["config/", "settings/", ".env", "secrets", "core/", "main.py", "__init__.py"],
    "high": ["tests/", "test_*.py", "*_test.py", "setup.py", "requirements.txt", "pyproject.toml"],
    "medium": ["src/", "lib/", "utils/"],
    "low": ["docs/", "README", "examples/"]
}
```

Load via `config/task_002_clustering.yaml` or constructor parameters.

---

## Typical Development Workflow

```bash
git checkout -b feature/002.3-diff-distance-calculator
# Implement class in src/analyzers/diff_distance.py
# Write tests in tests/test_diff_distance.py
pytest tests/test_diff_distance.py -v --cov=src/analyzers/diff_distance
# Verify output schema against specification
python -c "from src.analyzers.diff_distance import DiffDistanceCalculator; print(DiffDistanceCalculator('.').analyze('main'))"
git add -A && git commit -m "feat: complete Task 002.3 DiffDistanceCalculator"
```

---

## Integration Handoff

**Downstream:** Task 002.4 (BranchClusterer) consumes the output dict directly.

**Contract:** The `analyze()` return dict must contain exactly the keys shown in the Output JSON Schema. Task 002.4 reads `metrics` and `aggregate_score`.

**Parallel with:** Task 002.1 (CommitHistoryAnalyzer), Task 002.2 (CodebaseStructureAnalyzer) — no cross-dependencies.

---

## Common Gotchas & Solutions

**Gotcha 1: Binary files in numstat output**
```python
# WRONG
added = int(parts[0])  # Crashes on "-" (binary marker)

# RIGHT
if parts[0] == "-":  # Binary file
    continue
added = int(parts[0])
```

**Gotcha 2: Division by zero in diff_complexity**
```python
# WRONG
avg_change = total_changes / files_affected  # files_affected can be 0

# RIGHT
if files_affected == 0:
    return 0.5  # Neutral score for no diff
avg_change = total_changes / files_affected
```

**Gotcha 3: Large diffs overflowing metrics**
```python
# WRONG
metric = churn_ratio  # Can exceed 1.0

# RIGHT
metric = max(0, 1 - min(churn_ratio, 1.0))  # Always clamped to [0, 1]
```

**Gotcha 4: Merge commits inflating diff stats**
```python
# WRONG
git diff main..BRANCH  # Includes merge commit noise

# RIGHT
git diff main...BRANCH  # Three-dot: excludes merge commits, shows only branch changes
```

**Gotcha 5: Pattern matching with fnmatch vs startswith**
```python
# WRONG
if pattern in filepath:  # "src" matches "resource"

# RIGHT
if pattern.endswith("/"):
    match = filepath.startswith(pattern)
else:
    match = fnmatch.fnmatch(filepath, pattern)
```

---

## Integration Checkpoint

**When to move to Task 002.4 (BranchClusterer):**

- [ ] All 7 sub-subtasks complete
- [ ] Unit tests passing (>95% coverage)
- [ ] Output matches specification exactly
- [ ] No validation errors on test data
- [ ] Performance targets met (<2s per branch)
- [ ] All 5 edge cases handled (binary, large diffs, deleted, merge commits, no diff)
- [ ] Code review approved
- [ ] Commit message: `feat: complete Task 002.3 DiffDistanceCalculator`

---

## Done Definition

Task 002.3 is done when:

1. All 7 sub-subtasks marked complete
2. Unit tests pass (>95% coverage) on CI/CD
3. Code review approved
4. Outputs match specification exactly
5. Output schema validation passes
6. Documentation complete and accurate
7. Performance benchmarks met (<2s per branch)
8. All 5 edge cases verified (binary files, large diffs, deleted files, merge commits, no diff)
9. Ready for hand-off to Task 002.4
10. Commit: `feat: complete Task 002.3 DiffDistanceCalculator`
11. All success criteria checkboxes marked complete

---

## Provenance

- **Primary source:** HANDOFF_75.3_DiffDistanceCalculator.md (archived: task_data/migration_backup_20260129/task_data_original/archived/handoff_archive_task75/)
- **Structure standard:** TASK_STRUCTURE_STANDARD.md (approved January 6, 2026)
- **ID mapping:** 75.3 → 002.3 (migration performed January 29, 2026)
- **Test cases:** 5 scenarios from HANDOFF_75.3 (Minimal, Focused feature, Wide refactoring, Risky changes, Large rewrite)
- **Edge cases:** 5 from HANDOFF_75.3 (Binary files, Large diffs, Deleted files, Merge commits, No diff)
- **Metric formulas:** 4 calculation blocks from HANDOFF_75.3 Metric Calculation Details section
- **Risk categories:** RISKY_FILE_PATTERNS dict with 4 tiers from HANDOFF_75.3

## Performance Targets

[Performance targets to be defined]


## Testing Strategy

[Testing strategy to be defined]


## Next Steps

[Next steps to be defined]
