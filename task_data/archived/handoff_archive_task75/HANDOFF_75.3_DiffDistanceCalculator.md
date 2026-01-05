# Task 75.3: DiffDistanceCalculator Implementation

## Quick Summary
Implement the `DiffDistanceCalculator` class that computes code distance metrics between branches using diff analysis. This is a Stage One analyzer—no dependencies on other tasks in this batch.

**Effort:** 32-40 hours | **Complexity:** 8/10 | **Parallelizable:** Yes

---

## What to Build

A Python class `DiffDistanceCalculator` that:
1. Computes detailed diff metrics between target branch and main
2. Analyzes code churn, complexity, and integration risk
3. Returns 4 normalized metrics (0-1 scale)

### Class Signature
```python
class DiffDistanceCalculator:
    def __init__(self, repo_path: str, main_branch: str = "main")
    def analyze(self, branch_name: str) -> dict
```

---

## Metrics to Compute

| Metric | Weight | Description |
|--------|--------|-------------|
| `code_churn` | 30% | Lines changed ratio (inverse: lower churn = higher score) |
| `change_concentration` | 25% | Files affected count (lower = more focused = higher score) |
| `diff_complexity` | 25% | Heuristic: large diffs in few files = higher complexity |
| `integration_risk` | 20% | Pattern matching: risky files (config, core, tests) scoring |

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

## Git Commands Reference

```bash
# Get diff stats (additions/deletions per file)
git diff main...BRANCH_NAME --stat

# Get unified diff with context
git diff main...BRANCH_NAME

# Get numstat (tab-separated: added, deleted, filename)
git diff main...BRANCH_NAME --numstat

# Get file-level change summary
git diff main...BRANCH_NAME --compact-summary

# Count lines in specific file
git show BRANCH_NAME:path/to/file | wc -l
```

---

## Implementation Checklist

- [ ] Extract diff using `git diff main...branch --numstat`
- [ ] Parse numstat output: `added_lines | deleted_lines | filepath`
- [ ] Calculate total churn (added + deleted lines)
- [ ] Count unique files affected
- [ ] Identify file types (risk categorization)
- [ ] Implement code_churn metric (normalized by file size estimates)
- [ ] Implement change_concentration (inverse of files affected count)
- [ ] Implement diff_complexity (analyzes line concentration)
- [ ] Implement integration_risk (pattern matching on risky files)
- [ ] Normalize all metrics to [0, 1]
- [ ] Weight and aggregate metrics
- [ ] Handle edge cases: no changes, binary files, very large diffs
- [ ] Return dict matching output spec exactly
- [ ] Add docstrings (Google style)

---

## Risk Category Files (Configurable)

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

---

## Metric Calculation Details

### Code Churn
```
total_changes = lines_added + lines_deleted
# Estimate codebase size (check largest files or config)
estimated_codebase_size = 5000  # Configurable baseline
churn_ratio = total_changes / estimated_codebase_size
metric = max(0, 1 - min(churn_ratio, 1.0))
# Lower churn = higher score (closer to 1.0)
```

### Change Concentration
```
files_affected = count of unique files changed
# Normalize by reasonable max (e.g., 50 files)
max_expected_files = 50
concentration = min(files_affected / max_expected_files, 1.0)
metric = 1 - concentration  # Fewer files = higher score
```

### Diff Complexity
```
# If most changes in 1-2 files: high complexity
# If changes spread across many files: lower complexity
largest_file_change = max(changes per file)
avg_file_change = total_changes / files_affected
concentration_ratio = largest_file_change / avg_file_change
# High concentration = higher complexity
metric = min(concentration_ratio / 3, 1.0)  # Cap at 1.0
```

### Integration Risk
```
risk_score = sum of risk weights for affected files
# Critical files: 0.8 weight per file
# High risk: 0.5 weight per file
# Medium: 0.2 weight per file
# Low: 0.05 weight per file
normalized_risk = risk_score / files_affected
metric = 1 - normalized_risk  # Lower risk = higher score
```

---

## Test Cases

1. **Minimal changes**: 5 files, 50 lines total changed
2. **Focused feature**: 12 files, 300 lines changed (1 large file)
3. **Wide refactoring**: 30 files, 500 lines changed (scattered)
4. **Risky changes**: Includes config/ and core/ modifications
5. **Large rewrite**: 1000+ lines changed in few files

---

## Dependencies

- `GitPython` or subprocess for git calls
- Python built-in `re` for file pattern matching
- No internal dependencies on other Task 75.x components
- Output feeds into **Task 75.4 (BranchClusterer)**

---

## Configuration

Accept these parameters in `__init__` or config file:

```python
CODE_CHURN_WEIGHT = 0.30
CHANGE_CONCENTRATION_WEIGHT = 0.25
DIFF_COMPLEXITY_WEIGHT = 0.25
INTEGRATION_RISK_WEIGHT = 0.20
ESTIMATED_CODEBASE_SIZE = 5000
MAX_EXPECTED_FILES = 50
RISK_CATEGORY_FILES = {...}  # See above
```

---

## Edge Cases to Handle

1. **Binary files**: Ignore in line counts (detect by file extension)
2. **Large diffs**: Cap metrics at 1.0 (don't overflow)
3. **Deleted files**: Count as deletions, not new files
4. **Merge commits**: Use `...` in git diff to exclude merge commits
5. **No diff**: Return all metrics as 0.5 (neutral)

---

## Next Steps After Completion

1. Unit test with 5+ branch fixtures (vary file counts, churn levels)
2. Integration test with real repo
3. Verify metrics normalize to 0-1 range
4. Pass output to Task 75.4 integration point
5. Validate risk categorization against known high-risk branches

**Parallel tasks ready:** 75.1, 75.2 (no dependencies)
