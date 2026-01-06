# Task 0075.3: DiffDistanceCalculator

## Purpose
Create a reusable Python class that computes code distance metrics between branches using diff analysis. This is a Stage One analyzer with no dependencies on other tasks in this batch.

**Scope:** DiffDistanceCalculator class only  
**Effort:** 32-40 hours | **Complexity:** 8/10  
**Status:** Ready for implementation  
**No dependencies** - can start immediately (parallel with 075.1, 075.2)

---

## Success Criteria

Task 0075.3 is complete when:

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
- [ ] Compatible with Task 0075.4 (BranchClusterer) input requirements
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

### 075.3.1: Design Diff Analysis Architecture
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

---

### 075.3.2: Implement Git Diff Extraction
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

---

### 075.3.3: Implement Code Churn Metric
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

---

### 075.3.4: Implement Change Concentration Metric
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

---

### 075.3.5: Implement Diff Complexity Metric
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

---

### 075.3.6: Implement Integration Risk Metric
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

---

### 075.3.7: Aggregate Metrics & Output Formatting
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

### 075.3.8: Write Unit Tests
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

## Integration Checkpoint

**When to move to 075.4:**
- [ ] All 8 subtasks complete
- [ ] Unit tests passing (>90% coverage)
- [ ] Output matches specification
- [ ] Handles all edge cases
- [ ] Ready for integration with other Stage One analyzers

---


---

## Helper Tools (Optional)

The following tools are available to accelerate work or provide validation. **None are required** - every task is completable using only the steps in this file.

### Progress Logging

After completing each sub-subtask, optionally log progress for multi-session continuity:

```python
from memory_api import AgentMemory

memory = AgentMemory()
memory.load_session()

# After completing a sub-subtask
memory.add_work_log(
    action="Completed Task 075.X.Y",
    details="Implementation details and progress"
)
memory.update_todo("task_075_x_y", "completed")
memory.save_session()
```

**What this does:** Maintains session state across work sessions, enables agent handoffs, documents progress.  
**Required?** No - git commits are sufficient.  
**See:** MEMORY_API_FOR_TASKS.md for full usage patterns and examples.

### Check Next Task

After completing this task, see what's next:

```bash
python scripts/next_task.py
```

**See:** SCRIPTS_IN_TASK_WORKFLOW.md § next_task.py for details.

---

## Tools Reference

| Tool | Purpose | When to Use | Required? |
|------|---------|-----------|----------|
| Memory API | Progress logging | After each sub-subtask | No |
| next_task.py | Find next task | After completion | No |

**For detailed usage and troubleshooting:** See SCRIPTS_IN_TASK_WORKFLOW.md (all optional tools documented there)

## Done Definition

Task 0075.3 is done when:
1. All 8 subtasks marked complete
2. Unit tests pass (>95% coverage)
3. Code review approved
4. Outputs match specification
5. Documentation complete
6. Ready for hand-off to Task 0075.4


**Last Updated:** January 6, 2026  
**Phase:** 2 Shallow Retrofit  
**Structure:** TASK_STRUCTURE_STANDARD.md
