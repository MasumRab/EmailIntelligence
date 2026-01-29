# Task 75.3: DiffDistanceCalculator

## Purpose
Create a reusable Python class that computes code distance metrics between branches using diff analysis. This is a Stage One analyzer with no dependencies on other tasks in this batch.

**Scope:** DiffDistanceCalculator class only  
**Effort:** 32-40 hours | **Complexity:** 8/10  
**Status:** Ready for implementation  
**No dependencies** - can start immediately (parallel with 75.1, 75.2)

---

## Quick Navigation

Navigate this document using these links:

- [Purpose](#purpose)
- [Developer Quick Reference](#developer-quick-reference)
- [Success Criteria](#success-criteria)
- [Metrics to Compute](#metrics-to-compute)
- [Subtasks Overview](#subtasks-overview)
- [Subtask Details](#subtasks)
- [Configuration & Defaults](#configuration--defaults)
- [Technical Reference](#technical-reference)
- [Common Gotchas & Solutions](#common-gotchas--solutions)
- [Development Workflow](#typical-development-workflow)
- [Integration Handoff](#integration-handoff)
- [Integration Checkpoint](#integration-checkpoint)
- [Done Definition](#done-definition)

**Pro tip:** Use Ctrl+F to search within sections, or click links above to jump directly

---

## Developer Quick Reference

### What to Build
A Python class `DiffDistanceCalculator` that:
1. Analyzes code diffs between target branch and main
2. Computes 4 normalized metrics (0-1 scale)
3. Returns aggregated diff distance score

### Class Signature
```python
class DiffDistanceCalculator:
    def __init__(self, repo_path: str, main_branch: str = "main")
    def analyze(self, branch_name: str) -> dict
```

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

**Performance Targets:**
- [ ] Diff calculation: **< 3 seconds** (on typical 500-commit repo with 100+ file diffs)
- [ ] Memory usage: **< 100 MB** per analysis
- [ ] Handles **10,000+ line diffs** without failure
- [ ] Distance computation: **O(n)** complexity where n = lines changed
- [ ] Git command timeout: **30 seconds max** (protects against hanging)

**Quality Assurance:**
- [ ] Unit tests pass (minimum 8 test cases with **>95% code coverage**)
- [ ] No exceptions raised for valid inputs (comprehensive error handling)
- [ ] Code quality: Passes linting, follows PEP 8, includes comprehensive docstrings

**Integration Readiness:**
- [ ] Compatible with Task 75.4 (BranchClusterer) input requirements
- [ ] Compatible with Task 75.6 (PipelineIntegration) consumption patterns
- [ ] Configuration externalized and validated
- [ ] Documentation complete and accurate

---

## Subtasks Overview

### Dependency Flow Diagram

```
75.3.1 (3-4h) ────────┐
[Diff Design]         │
                      ├─→ 75.3.2 (4-5h) ────────┐
                      │  [Diff Extraction]      │
                      │                         ├─→ 75.3.3-75.3.6 (parallel, 3-5h each) ────┐
                      │                         │   [Churn, Concentration, Complexity, Risk]  │
                      └─────────────────────────┘                                           │
                                                                                           ├─→ 75.3.7 (2-3h)
                                                                                           │  [Aggregation]
                                                                                           │
                                                                                           └─→ 75.3.8 (4-5h)
                                                                                              [Unit Tests]

Critical Path: 75.3.1 → 75.3.2 → 75.3.3-75.3.6 (parallel) → 75.3.7 → 75.3.8
Minimum Duration: 32-36 hours (with parallelization of 75.3.3-75.3.6)
```

### Parallel Opportunities

**Can run in parallel (after 75.3.2):**
- 75.3.3: Code churn metric
- 75.3.4: Change concentration metric
- 75.3.5: Diff complexity metric
- 75.3.6: Integration risk metric

All four metric tasks depend only on 75.3.2 (diff extraction) and are independent of each other. **Estimated parallel execution saves 12-16 hours.**

**Must be sequential:**
- 75.3.1 → 75.3.2 (design required before extraction)
- 75.3.2 → 75.3.3-75.3.6 (extraction required before metric calculation)
- 75.3.3-75.3.6 → 75.3.7 (all metrics needed before aggregation)
- 75.3.7 → 75.3.8 (main class needed before testing)

### Timeline with Parallelization

**Days 1-2: Design (75.3.1)**
- Define code churn, concentration, complexity metrics
- Document risk categories and patterns

**Days 2-3: Diff Extraction (75.3.2)**
- Implement git diff --numstat parsing
- Create structured output format

**Days 3-5: Metrics (75.3.3-75.3.6 in parallel)**
- Day 3-4: Implement code churn + concentration (2 people)
- Day 3-4: Implement complexity + risk scoring (2 people)
- Day 4-5: Consolidate and test

**Days 5-6: Aggregation & Testing (75.3.7-75.3.8)**
- Day 5: Implement aggregation
- Day 6: Write comprehensive unit tests

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

## Configuration & Defaults

All parameters should be externalized to configuration files (not hardcoded). Use YAML format:

```yaml
# config/diff_distance_calculator.yaml
diff_distance_calculator:
  # Metric Weights (sum must equal 1.0)
  code_churn_weight: 0.30                # Lines changed impact
  change_concentration_weight: 0.25      # Files affected impact
  diff_complexity_weight: 0.25           # Concentration of changes
  integration_risk_weight: 0.20          # Risk pattern scoring
  
  # Baselines and Thresholds
  estimated_codebase_size: 5000          # Baseline for churn calculation
  max_expected_files: 50                 # Baseline for file concentration
  git_command_timeout_seconds: 30        # Prevent hanging
  
  # Risk Category Patterns
  risk_categories:
    critical:
      - "config/"
      - "settings/"
      - ".env"
      - "secrets"
      - "core/"
      - "main.py"
      - "__init__.py"
    high:
      - "tests/"
      - "test_*.py"
      - "*_test.py"
      - "setup.py"
      - "requirements.txt"
      - "pyproject.toml"
    medium:
      - "src/"
      - "lib/"
      - "utils/"
    low:
      - "docs/"
      - "README"
      - "examples/"
```

**How to use in code:**
```python
import yaml

def load_config(config_path='config/diff_distance_calculator.yaml'):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)['diff_distance_calculator']

config = load_config()
CHURN_WEIGHT = config['code_churn_weight']
RISK_CATEGORIES = config['risk_categories']
# ... etc
```

**Why externalize?**
- Easy to adjust metrics without redeploying code
- Different organizations may weight risk differently
- Can adapt to project-specific file patterns
- No code recompilation needed

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

## Typical Development Workflow

Complete step-by-step git workflow for implementing this task. Copy-paste ready sequences:

### Setup Your Feature Branch

```bash
# 1. Create feature branch
git checkout -b feat/diff-distance-calculator
git push -u origin feat/diff-distance-calculator

# 2. Create initial file structure
mkdir -p src/analyzers tests/analyzers config
touch src/analyzers/diff_distance_calculator.py
touch src/analyzers/__init__.py
git add src/analyzers/
git commit -m "chore: create diff distance calculator module"
```

### Subtask 75.3.1: Diff Design

```bash
# Document diff analysis design
cat > docs/DIFF_DISTANCE_DESIGN.md << 'EOF'
# DiffDistanceCalculator Design

## Metrics
1. Code Churn: Lines changed / estimated codebase
2. Change Concentration: Files affected (fewer = higher)
3. Diff Complexity: Concentration of changes in files
4. Integration Risk: Pattern-based file risk scoring

## Weights: 0.30 + 0.25 + 0.25 + 0.20 = 1.0

## Risk Categories: critical, high, medium, low
EOF

git add docs/
git commit -m "docs: design diff distance metrics (75.3.1)"
```

### Subtask 75.3.2: Diff Extraction

```bash
cat > src/analyzers/git_diff_utils.py << 'EOF'
import subprocess
from typing import Dict, Tuple

def get_diff_stats(repo_path: str, branch_name: str) -> Dict:
    """Extract diff statistics from git."""
    cmd = ['git', 'diff', f'main...{branch_name}', '--numstat']
    result = subprocess.run(
        cmd,
        cwd=repo_path,
        capture_output=True,
        text=True,
        timeout=30,
        encoding='utf-8'
    )
    
    stats = {'added': 0, 'deleted': 0, 'files': []}
    for line in result.stdout.strip().split('\n'):
        if not line:
            continue
        parts = line.split('\t')
        if len(parts) >= 3:
            added, deleted, filepath = parts[0], parts[1], parts[2]
            if added != '-' and deleted != '-':  # Skip binary files
                stats['added'] += int(added)
                stats['deleted'] += int(deleted)
                stats['files'].append(filepath)
    
    return stats
EOF

git add src/analyzers/git_diff_utils.py
git commit -m "feat: implement diff extraction (75.3.2)"
```

### Subtasks 75.3.3-75.3.6: Metrics (Parallel)

```bash
# Create metric modules
cat > src/analyzers/metrics_code_churn.py << 'EOF'
def compute_code_churn(total_changes: int, estimated_size: int = 5000) -> float:
    """Score lines changed ratio (lower = higher)."""
    ratio = total_changes / estimated_size
    return max(0, 1 - min(ratio, 1.0))
EOF

touch src/analyzers/metrics_concentration.py
touch src/analyzers/metrics_complexity.py
touch src/analyzers/metrics_integration_risk.py

git add src/analyzers/metrics_*.py
git commit -m "feat: implement diff metrics (75.3.3-75.3.6)"
```

### Final Steps

```bash
# Create configuration
mkdir -p config
cat > config/diff_distance_calculator.yaml << 'EOF'
diff_distance_calculator:
  code_churn_weight: 0.30
  change_concentration_weight: 0.25
  diff_complexity_weight: 0.25
  integration_risk_weight: 0.20
  estimated_codebase_size: 5000
  max_expected_files: 50
  git_command_timeout_seconds: 30
EOF

git add config/
git commit -m "config: diff distance calculator configuration"

# Create tests and push
pytest tests/analyzers/ -v --cov=src/analyzers --cov-report=html
git add tests/
git commit -m "test: comprehensive unit tests (95%+ coverage)"
git push origin feat/diff-distance-calculator
```

---

## Integration Handoff

### What Gets Passed to Task 75.4 (BranchClusterer)

**Task 75.4 expects input in this format:**

```python
from src.analyzers import DiffDistanceCalculator

calculator = DiffDistanceCalculator(repo_path)
result = calculator.analyze("feature/branch-name")

# result is a dict like:
# {
#   "branch_name": "feature/auth-system",
#   "metrics": {
#     "code_churn": 0.72,
#     "change_concentration": 0.81,
#     "diff_complexity": 0.68,
#     "integration_risk": 0.79
#   },
#   "aggregate_score": 0.750,
#   "total_lines_added": 342,
#   "total_lines_deleted": 87,
#   "total_lines_changed": 429,
#   "files_affected": 12,
#   "largest_file_change": 156,
#   "analysis_timestamp": "2025-12-22T10:40:00Z"
# }
```

**Task 75.4 uses these outputs by:**
1. Extracting the diff metrics as one of 3 distance components
2. Combining with commit history and structure metrics
3. Computing pairwise distances between branches
4. Using distances for hierarchical clustering

**Validation before handoff:**
```bash
python -c "
from src.analyzers import DiffDistanceCalculator

calc = DiffDistanceCalculator('.')
result = calc.analyze('main')

# Verify required fields
assert 'metrics' in result
assert 'aggregate_score' in result

# Verify metrics normalized
for m in result['metrics'].values():
    assert 0 <= m <= 1

print('✓ Output ready for Task 75.4')
"
```

---

## Common Gotchas & Solutions

### Gotcha 1: Binary Files Cause Line Count Errors ⚠️

**Problem:** Git diff shows binary files as "-" instead of line counts  
**Symptom:** `ValueError` when parsing "-" as integer  
**Root Cause:** Not handling binary file markers  

**Solution:** Skip lines with binary file markers
```python
if added == '-' or deleted == '-':  # Skip binary files
    continue
```

**Test:** Branch with only binary changes, verify no error

---

### Gotcha 2: Large Diffs Exhaust Memory ⚠️

**Problem:** Repos with 100,000+ line changes cause memory overflow  
**Symptom:** Out of memory error  
**Root Cause:** Loading entire diff into memory  

**Solution:** Process diffs in streaming fashion
```python
result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True, timeout=30)
# Process line-by-line instead of loading all at once
```

**Test:** Branch with 100,000+ lines changed, verify <100 MB memory

---

### Gotcha 3: Empty Diff Handling ⚠️

**Problem:** Branch identical to main causes division by zero  
**Symptom:** ZeroDivisionError or invalid metrics  
**Root Cause:** No bounds checking  

**Solution:** Check for empty diffs
```python
if total_changes == 0:
    return 0.5  # Neutral score for identical branches
```

**Test:** Analyze branch identical to main, verify metrics computed

---

### Gotcha 4: Risk Category Matching Issues ⚠️

**Problem:** Case sensitivity prevents pattern matching  
**Symptom:** Risk detection doesn't work reliably  
**Root Cause:** String comparisons not normalized  

**Solution:** Normalize paths before matching
```python
def matches_risk_pattern(filepath: str, pattern: str) -> bool:
    normalized = filepath.lower().replace('\\', '/')
    return normalized.startswith(pattern.lower())
```

**Test:** Branch with mixed case paths, verify risk detection works

---

### Gotcha 5: Git Timeout on Large Repos ⚠️

**Problem:** Large repos take >30 seconds to diff  
**Symptom:** Process hangs and gets terminated  
**Root Cause:** No timeout protection  

**Solution:** Always set timeout
```python
result = subprocess.run(cmd, timeout=30, ...)
```

**Test:** Very large branch, verify completes or raises clear timeout error

---

### Gotcha 6: Merge Commit Diff Issues ⚠️

**Problem:** Three-dot syntax (`main...branch`) may not work with merge commits  
**Symptom:** Unexpected diff results  
**Root Cause:** Not accounting for merge commit history  

**Solution:** Use three-dot syntax correctly
```python
# Three-dot shows changes on branch NOT on main
cmd = ['git', 'diff', f'main...{branch_name}', '--numstat']
```

**Test:** Branch with merge commits, verify correct diff

---

### Gotcha 7: Concentration Ratio Edge Cases ⚠️

**Problem:** Single file with huge changes causes invalid concentration  
**Symptom:** Division by zero or invalid ratios  
**Root Cause:** Not handling single-file branches  

**Solution:** Cap concentration ratios
```python
ratio = largest_change / avg_change if avg_change > 0 else 0
metric = min(ratio / 3, 1.0)  # Cap at 1.0
```

**Test:** Single-file branch with 1000+ line change, verify valid metric

---

### Gotcha 8: Weight Sum Validation ⚠️

**Problem:** Configuration with weights not summing to 1.0 breaks aggregation  
**Symptom:** Aggregate score outside [0,1]  
**Root Cause:** No validation on config load  

**Solution:** Validate weights
```python
total = sum(config['weights'].values())
assert abs(total - 1.0) < 0.001, f"Weights sum to {total}, must be 1.0"
```

**Test:** Load config, verify weights validation

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
