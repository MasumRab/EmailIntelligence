# Task 75.3: DiffDistanceCalculator

## Purpose
Create a reusable Python class that computes code distance metrics between branches using diff analysis. This is a Stage One analyzer with no dependencies on other tasks in this batch.

**Scope:** DiffDistanceCalculator class only  
**Effort:** 32-40 hours | **Complexity:** 8/10  
**Status:** Ready for implementation  
**No dependencies** - can start immediately (parallel with 75.1, 75.2)

---

## Success Criteria

Task 75.3 is complete when:

**Core Functionality:**
- [ ] `DiffDistanceCalculator` class accepts `repo_path` (str) and `branch_name` (str)
- [ ] Computes detailed diff metrics between target branch and main
- [ ] Analyzes code churn, complexity, and integration risk
- [ ] Returns 4 normalized metrics in [0,1] range
- [ ] Handles all specified edge cases (binary files, large diffs, no changes)
- [ ] Output matches JSON schema exactly

**Quality Assurance:**
- [ ] Unit tests pass (minimum 8 test cases with >95% coverage)
- [ ] No exceptions raised for valid inputs
- [ ] Performance: <3 seconds per branch analysis
- [ ] Code quality: PEP 8 compliant, comprehensive docstrings

**Integration Readiness:**
- [ ] Compatible with Task 75.4 (BranchClusterer) input requirements
- [ ] Configuration externalized and validated
- [ ] Documentation complete and accurate

---

## Metrics to Compute

| Metric | Weight | Description |
|--------|--------|-------------|
| `code_churn` | 30% | Lines changed ratio (inverse) |
| `change_concentration` | 25% | Files affected count (lower = higher) |
| `diff_complexity` | 25% | Large diffs in few files |
| `integration_risk` | 20% | Pattern-based risk scoring |

All metrics normalized to [0, 1].

---

## Output Specification

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

## Subtasks

### 75.3.1: Design Diff Analysis Architecture
**Purpose:** Define diff metrics and risk categorization  
**Effort:** 3-4 hours

**Steps:**
1. Design code churn calculation
2. Define change concentration logic
3. Document diff complexity analysis
4. Define risk categories (critical, high, medium, low)
5. Create risk file patterns

**Success Criteria:**
- [ ] All metrics mathematically defined
- [ ] Risk categories documented
- [ ] File patterns specified
- [ ] Calculation approach clear

### Implementation Checklist (From HANDOFF)
- [ ] Design code churn calculation: total_changes / estimated_codebase_size
- [ ] Define change concentration: normalize files affected count
- [ ] Document diff complexity: concentration ratio of changes
- [ ] Define risk file patterns: critical, high, medium, low
- [ ] Document integration_risk calculation: sum of risk weights per file

---

### 75.3.2: Implement Git Diff Extraction
**Purpose:** Extract detailed diff data from git  
**Effort:** 4-5 hours

**Steps:**
1. Implement `git diff --numstat` execution
2. Extract added/deleted lines per file
3. Parse output into structured format
4. Identify file types
5. Add error handling for large diffs

**Success Criteria:**
- [ ] Extracts diff data without error
- [ ] Parses numstat format correctly
- [ ] Returns structured data (per-file stats)
- [ ] Handles binary files
- [ ] Performance: <2 seconds per extraction

### Implementation Checklist (From HANDOFF)
- [ ] Use subprocess with timeout for git commands
- [ ] Implement `git diff main...BRANCH_NAME --numstat` execution
- [ ] Parse numstat output: added_lines | deleted_lines | filepath
- [ ] Extract added/deleted lines per file
- [ ] Identify file types (for risk categorization)
- [ ] Handle binary files (ignore in line counts)

---

### 75.3.3: Implement Code Churn Metric
**Purpose:** Score lines changed ratio (lower = higher)  
**Effort:** 3-4 hours

**Steps:**
1. Calculate total changes (added + deleted)
2. Estimate codebase size
3. Calculate churn ratio
4. Invert to score (lower churn = higher)
5. Cap at 1.0 and normalize

**Success Criteria:**
- [ ] Returns value in [0, 1] range
- [ ] Minimal churn scores > 0.8
- [ ] High churn scores < 0.3
- [ ] Handles edge cases (empty repos)

### Implementation Checklist (From HANDOFF)
- [ ] Calculate total changes (added + deleted lines)
- [ ] Estimate codebase size (baseline: 5000 lines)
- [ ] Compute churn_ratio = total_changes / estimated_codebase_size
- [ ] Invert to score: 1 - min(churn_ratio, 1.0)
- [ ] Handle edge case: no changes returns 0.5
- [ ] Verify metric in [0, 1] range

---

### 75.3.4: Implement Change Concentration Metric
**Purpose:** Score files affected count  
**Effort:** 3-4 hours

**Steps:**
1. Count unique files changed
2. Normalize by reasonable max (e.g., 50)
3. Invert (fewer files = higher score)
4. Return concentration score
5. Test with various file counts

**Success Criteria:**
- [ ] Returns value in [0, 1] range
- [ ] Single file changes score > 0.9
- [ ] Many files score lower
- [ ] Handles 0-file case

### Implementation Checklist (From HANDOFF)
- [ ] Count unique files changed
- [ ] Normalize by reasonable max (e.g., 50 files)
- [ ] Invert: metric = 1 - (files_affected / max_expected), cap at 1.0
- [ ] Test with various file counts
- [ ] Handle zero files case

---

### 75.3.5: Implement Diff Complexity Metric
**Purpose:** Score complexity (large changes in few files)  
**Effort:** 3-4 hours

**Steps:**
1. Identify largest file change
2. Calculate average change per file
3. Compute concentration ratio
4. Score complexity (high ratio = complex)
5. Cap at 1.0

**Success Criteria:**
- [ ] Returns value in [0, 1] range
- [ ] Concentrated changes score higher
- [ ] Scattered changes score lower
- [ ] Handles single-file diffs

### Implementation Checklist (From HANDOFF)
- [ ] Identify largest file change per branch
- [ ] Calculate average change per file
- [ ] Compute concentration_ratio = largest / average
- [ ] Score complexity: min(concentration_ratio / 3, 1.0)
- [ ] Handle single-file diffs gracefully

---

### 75.3.6: Implement Integration Risk Metric
**Purpose:** Pattern-based risk scoring  
**Effort:** 4-5 hours

**Steps:**
1. Categorize files by risk level
2. Sum risk weights for affected files
3. Normalize by files affected
4. Invert to score (lower risk = higher)
5. Test with risky file patterns

**Success Criteria:**
- [ ] Returns value in [0, 1] range
- [ ] Config file changes lower score
- [ ] Documentation-only changes high score
- [ ] Identifies all risk patterns

### Implementation Checklist (From HANDOFF)
- [ ] Define risk categories with file patterns (critical, high, medium, low)
- [ ] Sum risk weights for affected files
- [ ] Normalize by files affected count
- [ ] Invert: metric = 1 - (normalized_risk), high risk = lower score
- [ ] Test with risky file patterns (config/, core/, etc.)

---

### 75.3.7: Aggregate Metrics & Output Formatting
**Purpose:** Combine metrics and format output  
**Effort:** 2-3 hours

**Steps:**
1. Define metric weights (sum to 1.0)
2. Create aggregation function
3. Verify all metrics in [0,1]
4. Format output dict with statistics
5. Validate against JSON schema

**Success Criteria:**
- [ ] Aggregate score = weighted sum
- [ ] Returns value in [0, 1] range
- [ ] Output has all required fields
- [ ] Statistics accurately reflect changes

---

### 75.3.8: Write Unit Tests
**Purpose:** Comprehensive test coverage  
**Effort:** 4-5 hours

**Steps:**
1. Create test fixtures with various diff scenarios
2. Implement 8+ test cases covering different patterns
3. Mock git diff output for reliable testing
4. Add performance tests
5. Generate coverage report (>95%)

**Success Criteria:**
- [ ] 8+ test cases implemented
- [ ] All tests pass
- [ ] Code coverage >95%
- [ ] Edge cases covered (binary files, large diffs)
- [ ] Performance tests pass

### Test Case Examples (From HANDOFF)

1. **test_minimal_changes**: 5 files, 50 lines total changed
   - Expected: code_churn > 0.9, change_concentration > 0.9, all metrics in [0,1]

2. **test_focused_feature**: 12 files, 300 lines changed (1 large file 150 lines)
   - Expected: change_concentration ~0.75, diff_complexity high (concentrated)

3. **test_wide_refactoring**: 30 files, 500 lines changed (scattered)
   - Expected: change_concentration ~0.4, diff_complexity lower

4. **test_risky_changes**: Includes config/ and core/ modifications
   - Expected: integration_risk < 0.6 (high risk = lower score)

5. **test_large_rewrite**: 1000+ lines in few files
   - Expected: code_churn low, diff_complexity high

6. **test_documentation_only**: Only changes to docs/ and README
   - Expected: integration_risk > 0.8 (low risk files)

7. **test_binary_files**: Branch adds binary files and code
   - Expected: Metrics based only on code changes, binary ignored

8. **test_performance**: Analyze branch with 10,000+ lines changed
   - Expected: Complete in <3 seconds, reasonable memory usage

---

## Risk Category Files

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

## Configuration Parameters

- `CODE_CHURN_WEIGHT` = 0.30
- `CHANGE_CONCENTRATION_WEIGHT` = 0.25
- `DIFF_COMPLEXITY_WEIGHT` = 0.25
- `INTEGRATION_RISK_WEIGHT` = 0.20
- `ESTIMATED_CODEBASE_SIZE` = 5000
- `MAX_EXPECTED_FILES` = 50
- `RISK_CATEGORY_FILES` = {...}

---

## Git Commands Reference

```bash
# Get diff stats (additions/deletions per file)
git diff main...BRANCH_NAME --numstat

# Get unified diff with context
git diff main...BRANCH_NAME

# Get file-level change summary
git diff main...BRANCH_NAME --compact-summary

# Count lines in specific file
git show BRANCH_NAME:path/to/file | wc -l
```

---

## Edge Cases to Handle

1. **Binary files**: Ignore in line counts
2. **Large diffs**: Cap metrics at 1.0
3. **Deleted files**: Count as deletions
4. **Merge commits**: Use `...` in git diff
5. **No diff**: Return all metrics as 0.5

---


## Technical Reference (From HANDOFF)

### Metric Calculation Details

**Code Churn**
```
total_changes = lines_added + lines_deleted
estimated_codebase_size = 5000  # Configurable baseline
churn_ratio = total_changes / estimated_codebase_size
metric = max(0, 1 - min(churn_ratio, 1.0))
# Lower churn = higher score (closer to 1.0)
```

**Change Concentration**
```
files_affected = count of unique files changed
max_expected_files = 50
concentration = min(files_affected / max_expected_files, 1.0)
metric = 1 - concentration  # Fewer files = higher score
```

**Diff Complexity**
```
largest_file_change = max(changes per file)
avg_file_change = total_changes / files_affected
concentration_ratio = largest_file_change / avg_file_change
metric = min(concentration_ratio / 3, 1.0)  # Cap at 1.0
```

**Integration Risk**
```
risk_score = sum of risk weights for affected files
normalized_risk = risk_score / files_affected
metric = 1 - normalized_risk  # Lower risk = higher score
```

### Risk Category Files
```python
RISKY_FILE_PATTERNS = {
    "critical": ["config/", "settings/", ".env", "secrets", "core/", "main.py", "__init__.py"],
    "high": ["tests/", "test_*.py", "*_test.py", "setup.py", "requirements.txt", "pyproject.toml"],
    "medium": ["src/", "lib/", "utils/"],
    "low": ["docs/", "README", "examples/"]
}
```

### Dependencies & Parallel Tasks
- **No dependencies on other Task 75.x components** - can start immediately (parallel with 75.1, 75.2)
- **Output feeds into:** Task 75.4 (BranchClusterer)
- **External libraries:** GitPython or subprocess (git CLI), re (regex)

---

## Integration Checkpoint

**When to move to 75.4:**
- [ ] All 8 subtasks complete
- [ ] Unit tests passing (>90% coverage)
- [ ] Output matches specification
- [ ] Handles all edge cases
- [ ] Ready for integration with other Stage One analyzers

---

## Done Definition

Task 75.3 is done when:
1. All 8 subtasks marked complete
2. Unit tests pass (>95% coverage)
3. Code review approved
4. Outputs match specification
5. Documentation complete
6. Ready for hand-off to Task 75.4
