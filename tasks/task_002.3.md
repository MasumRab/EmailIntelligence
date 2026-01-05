# Task 002.3: DiffDistanceCalculator

**Status:** Ready for Implementation  
**Priority:** High  
**Effort:** 32-40 hours  
**Complexity:** 8/10  
**Dependencies:** None - can start immediately  
**Blocks:** Task 002.4 (BranchClusterer)

---

## Purpose

Create a reusable Python class that computes code distance metrics between branches using diff analysis. This is the most complex Stage One analyzer, evaluating code changes, churn, and integration risk.

**Scope:** DiffDistanceCalculator class only  
**No dependencies** - can start immediately (parallel with 002.1, 002.2)  
**Parallelizable with:** Task 002.1 and Task 002.2

---

## Success Criteria

Task 002.3 is complete when:

### Core Functionality
- [ ] `DiffDistanceCalculator` class accepts `repo_path` (str) and `branch_name` (str)
- [ ] Computes detailed diff metrics between target branch and main
- [ ] Analyzes code churn, complexity, and integration risk
- [ ] Returns exactly 4 normalized metrics in [0,1] range:
  - [ ] `code_churn` - Lines changed ratio (inverse normalized)
  - [ ] `change_concentration` - Files affected count impact
  - [ ] `diff_complexity` - Large diffs in few files
  - [ ] `integration_risk` - Pattern-based risk scoring
- [ ] Properly handles all specified edge cases:
  - [ ] Binary files (ignored in line counts)
  - [ ] Large diffs (doesn't exhaust memory)
  - [ ] No changes (empty diff)
  - [ ] Merge commits (uses `...` notation correctly)
  - [ ] Large repositories (doesn't timeout)
- [ ] Output matches JSON schema exactly

### Quality Assurance
- [ ] Unit tests pass (minimum 8 test cases with >95% coverage)
- [ ] No exceptions raised for valid inputs
- [ ] Performance: <3 seconds per branch analysis
- [ ] Code quality: PEP 8 compliant, comprehensive docstrings
- [ ] Memory: <100 MB per analysis
- [ ] All metrics verified in [0,1] range

### Integration Readiness
- [ ] Compatible with Task 002.4 (BranchClusterer) input requirements
- [ ] Configuration externalized and validated
- [ ] Documentation complete and accurate
- [ ] Risk categories properly defined

---

## Prerequisites & Dependencies

### Required Before Starting
- [ ] Git installed with diff support
- [ ] Python 3.8+ with subprocess module
- [ ] Test infrastructure in place
- [ ] Project structure created

### Blocks (What This Task Unblocks)
- Task 002.4 (BranchClusterer) - requires output from this task

### External Dependencies
- Python subprocess (built-in)
- Standard library: datetime, json, typing, collections

### No Dependency On
- Task 002.1 (CommitHistoryAnalyzer) - can start in parallel
- Task 002.2 (CodebaseStructureAnalyzer) - can start in parallel

---

## Sub-subtasks

### 002.3.1: Design Diff Analysis Architecture
**Effort:** 3-4 hours  
**Depends on:** None

**Steps:**
1. Design code churn calculation
2. Define change concentration logic
3. Document diff complexity analysis
4. Define risk categories (critical, high, medium, low)
5. Create risk file patterns

**Success Criteria:**
- [ ] All metrics mathematically defined
- [ ] Risk categories documented
- [ ] File patterns specified for each category
- [ ] Calculation approach clear

---

### 002.3.2: Implement Git Diff Extraction
**Effort:** 4-5 hours  
**Depends on:** 002.3.1

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
- [ ] Handles binary files gracefully
- [ ] Performance: <2 seconds per extraction

---

### 002.3.3: Implement Code Churn Metric
**Effort:** 3-4 hours  
**Depends on:** 002.3.1, 002.3.2

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

### 002.3.4: Implement Change Concentration Metric
**Effort:** 3-4 hours  
**Depends on:** 002.3.1, 002.3.2

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

### 002.3.5: Implement Diff Complexity Metric
**Effort:** 3-4 hours  
**Depends on:** 002.3.1, 002.3.2

**Steps:**
1. Identify largest file change
2. Calculate average change per file
3. Compute concentration ratio
4. Score complexity (high ratio = high complexity)
5. Cap at 1.0 and normalize

**Success Criteria:**
- [ ] Returns value in [0, 1] range
- [ ] Concentrated changes score higher
- [ ] Scattered changes score lower
- [ ] Handles single-file diffs

---

### 002.3.6: Implement Integration Risk Metric
**Effort:** 4-5 hours  
**Depends on:** 002.3.1, 002.3.2

**Steps:**
1. Categorize files by risk level (critical, high, medium, low)
2. Sum risk weights for affected files
3. Normalize by files affected
4. Invert to score (lower risk = higher score)
5. Test with risky file patterns

**Success Criteria:**
- [ ] Returns value in [0, 1] range
- [ ] Config file changes lower score
- [ ] Documentation-only changes high score
- [ ] Identifies all risk patterns

---

### 002.3.7: Aggregate Metrics & Output Formatting
**Effort:** 2-3 hours  
**Depends on:** 002.3.3, 002.3.4, 002.3.5, 002.3.6

**Steps:**
1. Define metric weights (sum to 1.0): 0.30/0.25/0.25/0.20
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

### 002.3.8: Write Unit Tests
**Effort:** 4-5 hours  
**Depends on:** 002.3.7

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

## Specification

### Class Interface

```python
class DiffDistanceCalculator:
    def __init__(self, repo_path: str, main_branch: str = "main"):
        """Initialize calculator with repository path."""
        
    def analyze(self, branch_name: str) -> dict:
        """Analyze code diffs for a branch.
        
        Args:
            branch_name: Name of branch to analyze
            
        Returns:
            Dict with metrics, aggregate score, and metadata
        """
```

### Output Format

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

### Metrics Definitions

| Metric | Definition | Weight | Notes |
|--------|-----------|--------|-------|
| `code_churn` | Lines changed ratio (inverse) | 0.30 | Lower churn = higher score |
| `change_concentration` | Files affected count | 0.25 | Fewer files = higher score |
| `diff_complexity` | Large diffs in few files | 0.25 | Concentrated = higher complexity |
| `integration_risk` | Pattern-based risk scoring | 0.20 | Critical files = lower score |

---

## Implementation Guide

### 002.3.1: Design Diff Analysis Architecture

Define metrics and risk categories:

```python
RISK_CATEGORIES = {
    'critical': [
        'config/', 'settings/', '.env', 'secrets',
        'core/', 'main.py', '__init__.py', 'setup.py'
    ],
    'high': [
        'tests/', 'test_*.py', '*_test.py',
        'requirements.txt', 'pyproject.toml'
    ],
    'medium': [
        'src/', 'lib/', 'utils/'
    ],
    'low': [
        'docs/', 'README', 'examples/', '.github/'
    ]
}

RISK_WEIGHTS = {
    'critical': 1.0,
    'high': 0.7,
    'medium': 0.4,
    'low': 0.1
}

METRICS_CONFIG = {
    'code_churn': {
        'weight': 0.30,
        'estimated_codebase_size': 5000,
        'interpretation': 'Inverse: lower churn = higher score'
    },
    'change_concentration': {
        'weight': 0.25,
        'max_expected_files': 50,
        'interpretation': 'Fewer files = higher score'
    },
    'diff_complexity': {
        'weight': 0.25,
        'interpretation': 'Concentrated changes = higher'
    },
    'integration_risk': {
        'weight': 0.20,
        'risk_categories': RISK_CATEGORIES,
        'interpretation': 'Critical files = lower score'
    }
}
```

### 002.3.2: Git Diff Extraction

```python
def get_diff_stats(
    repo_path: str,
    branch_name: str,
    main_branch: str = "main"
) -> Dict[str, dict]:
    """Extract diff statistics using git diff --numstat."""
    cmd = [
        'git', 'diff', f'{main_branch}...{branch_name}',
        '--numstat'
    ]
    
    output = subprocess.run(
        cmd,
        cwd=repo_path,
        capture_output=True,
        text=True,
        timeout=30
    ).stdout
    
    file_stats = {}
    total_added = 0
    total_deleted = 0
    
    for line in output.strip().split('\n'):
        if not line or line.startswith('Binary'):
            continue  # Skip binary markers
        
        parts = line.split('\t')
        if len(parts) < 3:
            continue
        
        added_str, deleted_str, file_path = parts[0], parts[1], parts[2]
        
        # Skip binary markers
        if added_str == '-' or deleted_str == '-':
            continue
        
        try:
            added = int(added_str)
            deleted = int(deleted_str)
        except ValueError:
            continue
        
        total_added += added
        total_deleted += deleted
        file_stats[file_path] = {
            'added': added,
            'deleted': deleted,
            'changed': added + deleted
        }
    
    return {
        'files': file_stats,
        'total_added': total_added,
        'total_deleted': total_deleted,
        'total_changed': total_added + total_deleted,
        'files_affected': len(file_stats)
    }
```

### 002.3.3: Code Churn Metric

```python
def calculate_code_churn(
    diff_stats: Dict,
    estimated_codebase_size: int = 5000
) -> float:
    """Calculate churn as ratio of changes to codebase size.
    
    Minimal churn scores > 0.8
    High churn scores < 0.3
    """
    total_changed = diff_stats['total_changed']
    
    # Churn ratio: how much of codebase changed
    churn_ratio = total_changed / estimated_codebase_size
    
    # Invert: lower churn = higher score
    # If churn_ratio = 0 → score = 1.0
    # If churn_ratio = 1 → score = 0.0
    score = 1.0 - min(1.0, churn_ratio)
    
    return max(0.0, min(1.0, score))
```

### 002.3.4: Change Concentration Metric

```python
def calculate_change_concentration(
    diff_stats: Dict,
    max_expected_files: int = 50
) -> float:
    """Score files affected (fewer = higher).
    
    Single file changes score > 0.9
    Many files score lower
    """
    files_affected = diff_stats['files_affected']
    
    # Invert: fewer files = higher score
    # 1 file → score ~= 0.98
    # 50 files → score ~= 0.0
    score = 1.0 - (files_affected / max_expected_files)
    
    return max(0.0, min(1.0, score))
```

### 002.3.5: Diff Complexity Metric

```python
def calculate_diff_complexity(
    diff_stats: Dict
) -> float:
    """Score concentration (large diffs in few files).
    
    Concentrated changes = higher complexity
    Scattered changes = lower complexity
    """
    if not diff_stats['files']:
        return 0.5  # No changes
    
    changes = [f['changed'] for f in diff_stats['files'].values()]
    max_change = max(changes)
    avg_change = sum(changes) / len(changes)
    
    # Concentration ratio: how much is in largest file
    # High ratio (large changes in one file) = high complexity
    concentration = max_change / (sum(changes) + 1)
    
    return max(0.0, min(1.0, concentration))
```

### 002.3.6: Integration Risk Metric

```python
def calculate_integration_risk(
    diff_stats: Dict,
    risk_categories: Dict = None,
    risk_weights: Dict = None
) -> float:
    """Pattern-based risk scoring.
    
    Critical files → low score
    Documentation → high score
    """
    if risk_categories is None:
        risk_categories = RISK_CATEGORIES
    if risk_weights is None:
        risk_weights = RISK_WEIGHTS
    
    total_risk = 0
    files_count = 0
    
    for file_path in diff_stats['files']:
        files_count += 1
        
        # Find risk category
        file_risk = 0.0
        for category, patterns in risk_categories.items():
            if any(file_path.startswith(p) for p in patterns):
                file_risk = risk_weights[category]
                break
        
        total_risk += file_risk
    
    if files_count == 0:
        return 0.5
    
    # Average risk
    avg_risk = total_risk / files_count
    
    # Invert: lower risk = higher score
    score = 1.0 - avg_risk
    
    return max(0.0, min(1.0, score))
```

### 002.3.7: Aggregation

```python
def aggregate_metrics(
    metrics: Dict[str, float],
    weights: Dict[str, float] = None
) -> float:
    """Combine 4 metrics with weights."""
    if weights is None:
        weights = {
            'code_churn': 0.30,
            'change_concentration': 0.25,
            'diff_complexity': 0.25,
            'integration_risk': 0.20
        }
    
    # Verify all metrics in [0, 1]
    for metric, value in metrics.items():
        assert 0 <= value <= 1, f"{metric} = {value} out of range"
    
    # Weighted sum
    aggregate = sum(
        metrics[k] * weights[k]
        for k in metrics.keys()
    )
    
    return max(0.0, min(1.0, aggregate))
```

---

## Configuration Parameters

All parameters externalized in `config/task_002_clustering.yaml`:

```yaml
diff_distance:
  code_churn_weight: 0.30
  change_concentration_weight: 0.25
  diff_complexity_weight: 0.25
  integration_risk_weight: 0.20
  
  estimated_codebase_size: 5000
  max_expected_files: 50
  git_command_timeout_seconds: 30
  
  risk_categories:
    critical:
      - "config/"
      - "settings/"
      - ".env"
      - "secrets"
      - "setup.py"
    high:
      - "tests/"
      - "test_*.py"
      - "*_test.py"
      - "requirements.txt"
    medium:
      - "src/"
      - "lib/"
      - "utils/"
    low:
      - "docs/"
      - "README"
      - "examples/"
```

---

## Performance Targets

### Per Component
- Single branch analysis: <3 seconds
- Memory usage: <100 MB per analysis
- Handle repositories with 100+ file diffs

### Scalability
- 13 branches: <39 seconds
- 50 branches: <150 seconds

---

## Testing Strategy

### Unit Tests

Minimum 8 test cases:

```python
def test_code_churn_minimal():
    """Minimal churn should score > 0.8"""
    
def test_code_churn_high():
    """High churn should score < 0.3"""
    
def test_change_concentration_single_file():
    """Single file changes should score > 0.9"""
    
def test_change_concentration_many_files():
    """Many files should score lower"""
    
def test_integration_risk_critical_files():
    """Critical file changes should lower score"""
    
def test_integration_risk_docs_only():
    """Docs only changes should have high score"""
    
def test_binary_files_ignored():
    """Binary markers should not crash"""
    
def test_output_schema_validation():
    """Output matches required schema"""
```

### Coverage Target
- Code coverage: >95%
- All edge cases covered (binary files, empty diffs, large diffs)
- All error paths tested

---

## Common Gotchas & Solutions

**Gotcha 1: Binary files as "-" instead of line counts**
```python
# WRONG
added, deleted, file = line.split('\t')
added = int(added)  # Crashes if "-"

# RIGHT
if added_str == '-' or deleted_str == '-':
    continue  # Skip binary markers
```

**Gotcha 2: Large diffs exhaust memory**
```python
# WRONG
all_diffs = output.split('\n')  # Loads all into memory

# RIGHT
for line in output.split('\n'):
    if line:
        process_line(line)  # Stream processing
```

**Gotcha 3: Empty diff causes division by zero**
```python
# WRONG
concentration = max_change / sum(changes)  # Crashes if empty

# RIGHT
if not files or sum(changes) == 0:
    return 0.5  # Default for no changes
```

**Gotcha 4: Risk category matching fails**
```python
# WRONG
if 'config' in file_path:  # Matches 'myconfig.py' wrong

# RIGHT
if any(file_path.startswith(p) for p in ['config/', 'settings/']):
    # Proper prefix matching
```

**Gotcha 5: Large repo diffs hang**
```python
# WRONG
result = subprocess.run(cmd, ...)  # No timeout on huge repos

# RIGHT
result = subprocess.run(cmd, timeout=30, ...)  # Always timeout
```

---

## Helper Tools (Optional)

The following tools are available to accelerate work or provide validation. **None are required** - every task is completable using only the steps in this file.

### Progress Logging

After completing each sub-subtask, optionally log progress for multi-session continuity:

```python
from memory_api import AgentMemory

memory = AgentMemory()
memory.load_session()

# After completing sub-subtask 002.3.4
memory.add_work_log(
    action="Completed Task 002.3.4: Change Concentration Metric",
    details="File count normalization implemented, edge cases handled, test coverage 100%"
)
memory.update_todo("task_002_3_4", "completed")
memory.save_session()
```

**What this does:** Maintains session state across work sessions, enables agent handoffs, documents progress.  
**Required?** No - git commits are sufficient.  
**See:** MEMORY_API_FOR_TASKS.md for full usage patterns and examples.

### Output Validation

After completing sub-subtask 002.3.8 (Unit Testing), optionally validate output format:

```bash
python scripts/compare_task_files.py \
  --validate src/analyzers/diff_distance.py \
  --schema specification.json
```

**What this does:** Checks your calculator output JSON matches the schema in the Specification section above.  
**Expected output:** `✓ Valid schema` (means you're ready to move to Task 002.4)  
**Required?** No - manual verification against Specification section is sufficient.  
**See:** SCRIPTS_IN_TASK_WORKFLOW.md § compare_task_files.py for troubleshooting.

### Check Next Task

After completing Task 002.3, see what's next:

```bash
python scripts/next_task.py

# Output shows: Task 002.4 (BranchClusterer) ready (when 002.1 & 002.2 also done)
```

**See:** SCRIPTS_IN_TASK_WORKFLOW.md § next_task.py for details.

---

## Tools Reference

| Tool | Purpose | When to Use | Required? |
|------|---------|-----------|----------|
| Memory API | Progress logging | After each sub-subtask | No |
| compare_task_files.py | Output validation | After 002.3.8 | No |
| next_task.py | Find next task | After completion | No |

**For detailed usage and troubleshooting:** See SCRIPTS_IN_TASK_WORKFLOW.md (all optional tools documented there)

---

## Integration Checkpoint

**When to move to Task 002.4:**

- [ ] All 8 sub-subtasks complete
- [ ] Unit tests passing (>90% coverage)
- [ ] Output matches specification
- [ ] Performance targets met (<3s per branch)
- [ ] Edge cases handled correctly
- [ ] Code review approved

---

## Done Definition

Task 002.3 is done when:

1. ✅ All 8 sub-subtasks marked complete
2. ✅ Unit tests pass (>95% coverage)
3. ✅ Code review approved
4. ✅ Outputs match specification
5. ✅ Documentation complete
6. ✅ Ready for Task 002.4
7. ✅ Commit: "feat: complete Task 002.3 DiffDistanceCalculator"

---

## Next Steps

1. Implement sub-subtask 002.3.1 (Design Diff Analysis Architecture)
2. Complete all 8 sub-subtasks (Week 1)
3. Write unit tests (target: >95% coverage)
4. Code review
5. Ready for Task 002.4

---

**Last Updated:** January 6, 2026  
**Consolidated from:** Task 75.3 (task-75.3.md) with 52 original success criteria preserved  
**Structure:** TASK_STRUCTURE_STANDARD.md
