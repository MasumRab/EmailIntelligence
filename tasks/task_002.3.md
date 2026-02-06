# Task 002.3: DiffDistanceCalculator

**Status:** pending
**Priority:** high
**Effort:** 32-40 hours
**Complexity:** 8/10
**Dependencies:** None

---

## Overview/Purpose

Calculate code distance metrics between feature branches and potential integration targets using various diff algorithms.

---

## Quick Navigation

Navigate this document using these links:

- [Overview/Purpose](#overview/purpose)
- [Success Criteria](#success-criteria)
- [Prerequisites & Dependencies](#prerequisites--dependencies)
- [Sub-subtasks Breakdown](#sub-subtasks-breakdown)
- [Specification Details](#specification-details)
- [Implementation Guide](#implementation-guide)
- [Configuration & Defaults](#configuration--defaults)
- [Typical Development Workflow](#typical-development-workflow)
- [Integration Handoff](#integration-handoff)
- [Common Gotchas & Solutions](#common-gotchas--solutions)
- [Subtasks Overview](#subtasks-overview)
- [Integration Checkpoint](#integration-checkpoint)
- [Done Definition](#done-definition)

**Pro tip:** Use Ctrl+F to search within sections, or click links above to jump directly

---

## Success Criteria

- [ ] Multiple distance metrics implemented
- [ ] Handles large diffs efficiently
- [ ] Weighted scoring for file importance
- [ ] Outputs comparable distance vectors
- [ ] Performance optimized for many branches

---

<!-- IMPORTED_FROM: backup_task75/task-002.3.md -->
Task 002.3 is complete when:

**Core Functionality:**
- [ ] `DiffDistanceCalculator` class accepts `repo_path` (str) and `branch_name` (str)
- [ ] Computes detailed diff metrics between target branch and main
- [ ] Analyzes code churn, complexity, and integration risk
- [ ] Returns 4 normalized metrics in [0,1] range
- [ ] Handles all specified edge cases (binary files, large diffs, no changes)
- [ ] Output matches JSON schema exactly

**Performance Targets:**
- [ ] Git diff extraction: **< 2 seconds** (on typical repository)
- [ ] Diff analysis and metric calculation: **< 1 second** (for 1000+ line changes)
- [ ] Memory usage: **< 100 MB** per operation
- [ ] Handles **repositories with 10,000+ commits** without failure
- [ ] Diff complexity calculation: **O(n)** where n = number of lines changed
- [ ] Overall analysis: **< 3 seconds max**

**Quality Assurance:**
- [ ] Unit tests pass (minimum 8 test cases with >95% coverage)
- [ ] No exceptions raised for valid inputs
- [ ] Code quality: PEP 8 compliant, comprehensive docstrings

**Integration Readiness:**
- [ ] Compatible with Task 002.4 (BranchClusterer) input requirements
- [ ] Configuration externalized and validated
- [ ] Documentation complete and accurate

---

## Prerequisites & Dependencies

### Required Before Starting
- [ ] No external prerequisites

### Blocks (What This Task Unblocks)
- [ ] No specific blocks defined

### External Dependencies
- [ ] No external dependencies

## Subtasks Overview

### Dependency Flow Diagram

```
TASK 002.3.1 (3-4h) ──────┐
[Design Diff Analysis]      │
                           ├─→ TASK 002.3.2 (4-5h) ──────┐
                           │  [Git Diff Extraction]        │
                           │                              ├─→ TASKS 002.3.3-002.3.6 (parallel) ────┐
                           │                              │   [Metrics Implementation]              │
                           │                              │                                       ├─→ TASK 002.3.7 (2-3h)
                           └──────────────────────────────┘                                       │  [Aggregate & Format]
                                                                                                │
                                                                                                └─→ TASK 002.3.8 (3-4h)
                                                                                                   [Unit Tests]

Critical Path: TASK 002.3.1 → TASK 002.3.2 → TASKS 002.3.3-002.3.6 (parallel) → TASK 002.3.7 → TASK 002.3.8
Minimum Duration: 15-20 hours (with parallelization)
```

### Parallel Opportunities

**Can run in parallel (after TASK 002.3.2):**
- TASK 002.3.3: Implement Code Churn Metric
- TASK 002.3.4: Implement Change Concentration Metric
- TASK 002.3.5: Implement Diff Complexity Metric
- TASK 002.3.6: Implement Integration Risk Metric

All tasks depend only on [parent task] and are independent of each other. **Estimated parallel execution saves 8-10 hours.**

**Must be sequential:**
- TASK 002.3.1 → TASK 002.3.2 (need architecture before extraction)
- TASK 002.3.2 → TASKS 002.3.3-002.3.6 (need extraction before metrics)
- TASKS 002.3.3-002.3.6 → TASK 002.3.7 (need metrics before aggregation)
- TASK 002.3.7 → TASK 002.3.8 (need aggregation before testing)

### Timeline with Parallelization

**Days 1-2: [First Phase] (TASK 002.3.1-TASK 002.3.2)**
- TASK 002.3.1: Design Diff Analysis Architecture
- TASK 002.3.2: Implement Git Diff Extraction

**Days 2-3: [Parallel Phase] (TASKS 002.3.3-002.3.6 in parallel)**
- Days 2-3: TASK 002.3.3 + TASK 002.3.4 (2 people)
- Days 2-3: TASK 002.3.5 + TASK 002.3.6 (2 people)

**Days 3-4: [Integration Phase] (TASKS 002.3.7-002.3.8)**
- Day 3: TASK 002.3.7 (Aggregate & Output Formatting)
- Day 4: TASK 002.3.8 (Write Unit Tests)

---

## Sub-subtasks Breakdown

### 002.3.1: Design Diff Analysis Architecture
**Purpose:** Define how diff metrics will be calculated and combined
**Effort:** 3-4 hours

**Steps:**
1. Define the 4 core metrics with mathematical formulas
2. Document calculation approach for each metric
3. Create normalization strategy (ensure all metrics in [0,1] range)
4. Create weighting scheme: 0.30/0.25/0.25/0.20 (sum = 1.0)
5. Document edge case handling for each metric

**Success Criteria:**
- [ ] All 4 metrics clearly defined with formulas
- [ ] Calculation approach specified
- [ ] Normalization approach specified
- [ ] Weights documented
- [ ] Edge case handling documented

**Blocks:** 002.3.2, 002.3.3, 002.3.4, 002.3.5

---

### 002.3.2: Set Up Git Diff Data Extraction
**Purpose:** Create functions to extract diff data from git repository
**Effort:** 4-5 hours
**Depends on:** 002.3.1

**Steps:**
1. Create utility functions for git command execution
2. Implement branch validation (check if branch exists)
3. Create diff extraction (get all changes between branches)
4. Create diff metadata extraction (additions, deletions, file changes)
5. Add error handling (invalid branch, repo not found, git errors)

**Success Criteria:**
- [ ] Can execute git diff commands without errors
- [ ] Validates branch existence before processing
- [ ] Extracts diff data with metadata
- [ ] Handles non-existent branches gracefully
- [ ] Returns structured data (list of changes)

**Blocks:** 002.3.3, 002.3.4, 002.3.5

---

### 002.3.3: Implement Code Churn Metric
**Purpose:** Score how much code has changed in the branch
**Effort:** 3-4 hours
**Depends on:** 002.3.1, 002.3.2

**Steps:**
1. Extract total lines added and deleted from diff
2. Calculate churn ratio (lines changed / total lines in branch)
3. Define churn baseline and scoring
4. Normalize to 0-1 range (higher churn = lower score)
5. Test with high-churn and low-churn branches

**Success Criteria:**
- [ ] Returns value in [0, 1] range
- [ ] Low churn (few changes) scores > 0.7
- [ ] High churn (many changes) scores < 0.4
- [ ] Correctly handles single-file changes
- [ ] Consistent calculation across test cases

---

### 002.3.4: Implement Change Concentration Metric
**Purpose:** Score how concentrated changes are (few vs many files)
**Effort:** 3-4 hours
**Depends on:** 002.3.1, 002.3.2

**Steps:**
1. Count total files changed in branch
2. Calculate concentration ratio (files changed vs total files touched)
3. Define concentration baseline and scoring
4. Normalize to 0-1 range (focused changes = higher score)
5. Test with scattered vs concentrated changes

**Success Criteria:**
- [ ] Returns value in [0, 1] range
- [ ] Focused changes (1-3 files) score > 0.8
- [ ] Scattered changes (many files) score < 0.5
- [ ] Correctly handles single-file changes
- [ ] Handles branches with many files touched

---

### 002.3.5: Implement Diff Complexity & Risk Metrics
**Purpose:** Score diff complexity and integration risk
**Effort:** 4-5 hours
**Depends on:** 002.3.1, 002.3.2

**Steps for diff_complexity:**
1. Extract change patterns from diff
2. Calculate complexity score (large changes in few files = higher complexity)
3. Define complexity baseline and scoring
4. Normalize to 0-1 range

**Steps for integration_risk:**
1. Identify risk patterns in changed files (config, core modules, etc.)
2. Count risky file types and patterns
3. Calculate risk score based on pattern frequency
4. Normalize to 0-1 range (higher risk = lower score)

**Success Criteria:**
- [ ] Diff complexity: Returns value in [0, 1] range
- [ ] Diff complexity: Concentrated changes score higher than scattered
- [ ] Integration risk: Returns value in [0, 1] range
- [ ] Integration risk: Risky patterns score lower than safe changes
- [ ] Handles edge cases (binary files, deletions)

---

### 002.3.6: Aggregate Metrics & Output Formatting
**Purpose:** Combine 4 metrics into single score and format output
**Effort:** 2-3 hours
**Depends on:** 002.3.3, 002.3.4, 002.3.5

**Steps:**
1. Define metric weights (sum to 1.0)
2. Create aggregation function (weighted sum)
3. Verify all metrics in [0,1] before aggregating
4. Format output dict (branch name, metrics dict, aggregate score, metadata)
5. Add timestamp

**Success Criteria:**
- [ ] Aggregate score = 0.30*m1 + 0.25*m2 + 0.25*m3 + 0.20*m4
- [ ] Returns value in [0, 1] range
- [ ] Output dict has all required fields
- [ ] Timestamp in ISO format
- [ ] No missing or extra fields

---

### 002.3.7: Write Unit Tests
**Purpose:** Verify DiffDistanceCalculator works correctly
**Effort:** 3-4 hours
**Depends on:** 002.3.6

**Steps:**
1. Create test fixtures with various branch characteristics
2. Implement minimum 8 test cases
3. Implement mocking for git commands
4. Add performance tests
5. Generate coverage report (>95%)

**Success Criteria:**
- [ ] Minimum 8 comprehensive test cases
- [ ] All tests pass on CI/CD
- [ ] Code coverage >95%
- [ ] Edge cases covered
- [ ] Error handling tested
- [ ] Output validation includes JSON schema
- [ ] Performance tests meet <3 second requirement

---

### 002.3.8: Performance Optimization
**Purpose:** Optimize for large repositories and many file changes
**Effort:** 2-3 hours
**Depends on:** 002.3.7

**Steps:**
1. Profile current implementation
2. Identify bottlenecks in git operations
3. Optimize diff data extraction
4. Add streaming for large diffs
5. Validate performance targets met

**Success Criteria:**
- [ ] Single branch analysis <3 seconds
- [ ] Memory usage <100MB per analysis
- [ ] Handles diffs with 5000+ file changes
- [ ] No performance degradation with large inputs
- [ ] All tests still pass after optimization

---

## Specification Details

### Task Interface
- **ID**: 002.3
- **Title**: DiffDistanceCalculator
- **Status**: pending
- **Priority**: high
- **Effort**: 32-40 hours
- **Complexity**: 8/10

### Requirements
**Core Requirements:**
- Python 3.8+ runtime environment
- Git installed and accessible from command line
- Access to local git repository with feature branches
- GitPython library or subprocess access for git commands
- YAML parser for configuration files

**Functional Requirements:**
- Must accept repository path and branch name as input parameters
- Must extract diff data using git diff commands with proper parsing
- Must compute 4 specific metrics with normalized values in [0,1] range
- Must return structured output matching JSON schema specification
- Must handle edge cases (binary files, large diffs, no changes)

**Non-functional Requirements:**
- Performance: Complete analysis in under 3 seconds per branch
- Reliability: Handle all error conditions gracefully without crashing
- Scalability: Support repositories with up to 10,000+ commits and large diffs
- Maintainability: Follow PEP 8 standards with comprehensive docstrings
- Testability: Achieve >95% code coverage with unit tests

### Task Interface
- **ID**: UNKNOWN
- **Title**: Untitled Task
- **Status**: pending
- **Priority**: high
- **Effort**: 32-40 hours
- **Complexity**: 8/10

### Requirements

**Core Requirements:**
- Python 3.8+ runtime environment
- Git installed and accessible from command line
- Access to local git repository with feature branches
- GitPython library or subprocess access for git commands
- YAML parser for configuration files

**Functional Requirements:**
- Must accept repository path and branch name as input parameters
- Must extract diff data using git diff commands with proper parsing
- Must compute 4 specific metrics with normalized values in [0,1] range
- Must return structured output matching JSON schema specification
- Must handle edge cases (binary files, large diffs, no changes)

**Non-functional Requirements:**
- Performance: Complete analysis in under 3 seconds per branch
- Reliability: Handle all error conditions gracefully without crashing
- Scalability: Support repositories with up to 10,000+ commits and large diffs
- Maintainability: Follow PEP 8 standards with comprehensive docstrings
- Testability: Achieve >95% code coverage with unit tests

## Implementation Guide

### Phase 1: Setup and Architecture (Days 1-2)
1. Create the basic class structure for `DiffDistanceCalculator`
2. Implement repository validation and initialization
3. Set up configuration loading from YAML
4. Create the basic method signatures

### Phase 2: Git Diff Data Extraction (Days 2-3)
1. Implement git command execution with proper error handling
2. Extract diff data using `git diff` commands
3. Parse diff output (additions, deletions, file changes)
4. Handle edge cases (binary files, large diffs, no changes)

### Phase 3: Metric Implementation (Days 3-5)
1. Implement the 4 core metrics:
   - Code churn metric (lines changed ratio)
   - Change concentration metric (files affected count)
   - Diff complexity metric (large changes in few files)
   - Integration risk metric (pattern-based risk scoring)
2. Ensure all metrics return values in [0,1] range
3. Add proper normalization and bounds checking

### Phase 4: Integration and Testing (Days 5-6)
1. Integrate all metrics into a weighted aggregation function
2. Format output according to specification
3. Write comprehensive unit tests (8+ test cases)
4. Perform performance testing to ensure <3s execution time

### Key Implementation Notes:
- Use subprocess with timeout for git commands to prevent hanging
- Implement proper error handling for all edge cases
- Ensure all metrics are normalized to [0,1] range
- Follow the configuration parameters specified in the Configuration section
- Add comprehensive logging and error reporting

<!-- IMPORTED_FROM: /home/masum/github/PR/.taskmaster/enhanced_improved_tasks/task-002-3.md -->

<!-- IMPORTED_FROM: /home/masum/github/PR/.taskmaster/task_data/archived/backups_archive_task002/task-002.3.md -->

# Task 002.3: DiffDistanceCalculator

<!-- IMPORTED_FROM: /home/masum/github/PR/.taskmaster/task_data/archived/handoff_archive_task002/HANDOFF_002.3_DiffDistanceCalculator.md -->

# Task 002.3: DiffDistanceCalculator Implementation

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
- No internal dependencies on other Task 002.x components
- Output feeds into **Task 002.4 (BranchClusterer)**

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
4. Pass output to Task 002.4 integration point
5. Validate risk categorization against known high-risk branches

**Parallel tasks ready:** 002.1, 002.2 (no dependencies)

## Purpose
Create a reusable Python class that computes code distance metrics between branches using diff analysis. This is a Stage One analyzer with no dependencies on other tasks in this batch.

**Scope:** DiffDistanceCalculator class only  
**Effort:** 32-40 hours | **Complexity:** 8/10  
**Status:** Ready for implementation  
**No dependencies** - can start immediately (parallel with 002.1, 002.2)

---

## Success Criteria

Task 002.3 is complete when:

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
- [ ] Compatible with Task 002.4 (BranchClusterer) input requirements
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

### 002.3.1: Design Diff Analysis Architecture
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

### 002.3.2: Implement Git Diff Extraction
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

### 002.3.3: Implement Code Churn Metric
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

### 002.3.4: Implement Change Concentration Metric
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

### 002.3.5: Implement Diff Complexity Metric
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

### 002.3.6: Implement Integration Risk Metric
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

### 002.3.7: Aggregate Metrics & Output Formatting
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

### 002.3.8: Write Unit Tests
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

## Configuration & Defaults

All parameters should be externalized to configuration files (not hardcoded). Use YAML format:

```yaml
# config/diff_distance_calculator.yaml
diff_distance_calculator:
  # Metric Weights
  code_churn_weight: 0.30           # Weight for code churn metric
  change_concentration_weight: 0.25 # Weight for change concentration metric
  diff_complexity_weight: 0.25      # Weight for diff complexity metric
  integration_risk_weight: 0.20     # Weight for integration risk metric

  # Thresholds
  estimated_codebase_size: 5000     # Baseline for churn calculation
  max_expected_files: 50            # Max files for concentration calc

  # Risk Categories
  risk_category_files:              # Risk categorization for files
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
CODE_CHURN_WEIGHT = config['code_churn_weight']
CHANGE_CONCENTRATION_WEIGHT = config['change_concentration_weight']
DIFF_COMPLEXITY_WEIGHT = config['diff_complexity_weight']
INTEGRATION_RISK_WEIGHT = config['integration_risk_weight']
ESTIMATED_CODEBASE_SIZE = config['estimated_codebase_size']
MAX_EXPECTED_FILES = config['max_expected_files']
RISK_CATEGORY_FILES = config['risk_category_files']
```

**Why externalize?**
- Easy to tune without redeploying code
- Different configurations for different environments (dev/test/prod)
- Can adjust thresholds based on organizational needs
- No code recompilation needed to adjust parameters

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

## Typical Development Workflow

Complete step-by-step git workflow for implementing this task. Copy-paste ready sequences:

### Setup Your Feature Branch

```bash
# 1. Create and push feature branch
git checkout -b feat/diff-distance-calculator
git push -u origin feat/diff-distance-calculator

# 2. Create directory structure
mkdir -p src/analyzers tests/analyzers
touch src/analyzers/__init__.py
git add src/analyzers/
git commit -m "chore: create analyzers module structure"
```

### Subtask 002.3.1: Design Diff Analysis Architecture

```bash
# Create initial module file
cat > src/analyzers/diff_distance_calculator.py << 'EOF'
"""
Diff Distance Calculator Module
"""
class DiffDistanceCalculator:
    def __init__(self, repo_path: str, main_branch: str = "main"):
        self.repo_path = repo_path
        self.main_branch = main_branch

    def analyze(self, branch_name: str) -> dict:
        """Analyze diff distance metrics and return results."""
        pass
EOF

git add src/analyzers/diff_distance_calculator.py
git commit -m "feat: implement DiffDistanceCalculator skeleton (Task 002.3)"
```

### Subtask 002.3.2: Implement Git Diff Extraction

```bash
# Update the calculator to implement git diff extraction
cat >> src/analyzers/diff_distance_calculator.py << 'EOF'

    def _extract_diff_data(self, branch_name: str) -> dict:
        """Extract diff data for a branch."""
        import subprocess
        import os

        os.chdir(self.repo_path)

        # Get diff stats (additions/deletions per file)
        result = subprocess.run([
            "git", "diff", f"{self.main_branch}...{branch_name}", "--numstat"
        ], capture_output=True, text=True, timeout=30)

        if result.returncode != 0:
            raise Exception(f"Git command failed: {result.stderr}")

        # Parse numstat output: added_lines \t deleted_lines \t filepath
        lines = result.stdout.strip().split('\n')
        diff_data = []
        for line in lines:
            if line.strip():
                parts = line.split('\t')
                if len(parts) == 3:
                    added, deleted, filepath = parts
                    diff_data.append({
                        'added': int(added) if added.isdigit() else 0,
                        'deleted': int(deleted) if deleted.isdigit() else 0,
                        'filepath': filepath
                    })

        return diff_data
EOF

git add src/analyzers/diff_distance_calculator.py
git commit -m "feat: implement git diff extraction for DiffDistanceCalculator (Task 002.3.2)"
```

[Repeat for each major subtask]

### Final Steps

```bash
# Create configuration file
mkdir -p config
cat > config/diff_distance_calculator.yaml << 'EOF'
diff_distance_calculator:
  # Metric Weights
  code_churn_weight: 0.30           # Weight for code churn metric
  change_concentration_weight: 0.25 # Weight for change concentration metric
  diff_complexity_weight: 0.25      # Weight for diff complexity metric
  integration_risk_weight: 0.20     # Weight for integration risk metric

  # Thresholds
  estimated_codebase_size: 5000     # Baseline for churn calculation
  max_expected_files: 50            # Max files for concentration calc

  # Risk Categories
  risk_category_files:              # Risk categorization for files
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
EOF

git add config/
git commit -m "config: DiffDistanceCalculator configuration parameters"

# Push to origin
git push origin feat/diff-distance-calculator

# Create pull request
gh pr create --title "Complete Task 002.3: DiffDistanceCalculator" \
             --body "Implements DiffDistanceCalculator with code churn, change concentration, diff complexity, and integration risk metrics"
```

---

## Integration Handoff

### What Gets Passed to Task 002.4 (Downstream Task)

**Task 002.4 expects input in this format:**

```python
from src.analyzers.diff_distance_calculator import DiffDistanceCalculator

calculator = DiffDistanceCalculator(repo_path, main_branch)
result = calculator.analyze(branch_name)

# result is a dict like:
# {
#   "branch_name": "feature/branch-name",
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

**Task 002.4 uses these outputs by:**
1. Collects results from multiple analyzers (002.1, 002.2, 002.3)
2. Combines metrics using weighted approach (0.35×002.1 + 0.35×002.2 + 0.30×002.3)
3. Performs hierarchical clustering on combined metrics
4. Generates cluster assignments for each branch

**Validation before handoff:**
```bash
# Verify output matches specification
python -c "
from src.analyzers.diff_distance_calculator import DiffDistanceCalculator
calculator = DiffDistanceCalculator('/path/to/repo', 'main')
result = calculator.analyze('some-branch')

# Check required fields
assert 'branch_name' in result
assert 'metrics' in result
assert 'aggregate_score' in result

# Check value ranges/types
assert isinstance(result['aggregate_score'], float)
assert 0 <= result['aggregate_score'] <= 1

print('✓ Output valid and ready for Task 002.4')
"
```

---

## Common Gotchas & Solutions

### Gotcha 1: Large Diff Handling ⚠️

**Problem:** Git diff commands fail or timeout on branches with thousands of file changes
**Symptom:** Process hangs or crashes when analyzing large diffs
**Root Cause:** Git operations on very large diffs can consume excessive memory or time

**Solution:** Add timeout and memory management to subprocess calls
```python
import subprocess
result = subprocess.run([
    "git", "diff", f"{main_branch}...{branch_name}", "--numstat"
], capture_output=True, text=True, timeout=60)  # Increased timeout for large diffs
```

**Test:** Verify timeout handling works by testing with a branch that has many changes

---

### Gotcha 2: Binary File Detection ⚠️

**Problem:** Diff analysis fails when binary files are included in the changes
**Symptom:** Error parsing diff output when binary files are present
**Root Cause:** Binary files don't have line-based changes that can be counted

**Solution:** Filter out binary files from diff analysis
```python
def _extract_diff_data(self, branch_name: str) -> dict:
    # ... git command execution ...
    for line in lines:
        if line.strip():
            # Skip binary files which show '-' for line counts
            if '\t-\t' in line:  # Binary file detected
                continue
            # ... process text files
```

**Test:** Verify that binary files are properly skipped during analysis

---

### Gotcha 3: Encoding Issues ⚠️

**Problem:** Diff analysis fails with UnicodeDecodeError on files with special encodings
**Symptom:** Process crashes when processing files with non-standard character encodings
**Root Cause:** Git diff output may contain characters that can't be decoded with default encoding

**Solution:** Handle encoding errors gracefully
```python
result = subprocess.run([...], capture_output=True, text=True, encoding='utf-8', errors='ignore')
```

**Test:** Verify that files with various encodings are processed without crashing

---

### Gotcha 4: Risk Category Matching ⚠️

**Problem:** Incorrectly categorizing files due to improper pattern matching
**Symptom:** Files being assigned wrong risk levels
**Root Cause:** Using simple string matching instead of path-based matching

**Solution:** Use proper path matching for risk categories
```python
def _categorize_file_risk(self, filepath: str) -> str:
    """Categorize file risk based on path."""
    import os.path
    for category, patterns in RISK_CATEGORIES.items():
        for pattern in patterns:
            # Handle both directory prefixes and file patterns
            if filepath.startswith(pattern.rstrip('*')) or fnmatch.fnmatch(filepath, pattern):
                return category
    return 'low'  # Default to low risk
```

**Test:** Verify that files are correctly categorized by risk level

---

## Integration Checkpoint

**When to move to 002.4:**
- [ ] All 8 subtasks complete
- [ ] Unit tests passing (>90% coverage)
- [ ] Output matches specification
- [ ] Handles all edge cases
- [ ] Ready for integration with other Stage One analyzers

---

## Done Definition

Task 002.3 is done when:
1. All 8 subtasks marked complete
2. Unit tests pass (>95% coverage)
3. Code review approved
4. Outputs match specification
5. Documentation complete
6. Ready for hand-off to Task 002.4

## Purpose

Calculate code distance metrics between feature branches and potential integration targets using various diff algorithms.

---

## Details

Implement a Python module that:
- Computes file-level diffs between branches
- Calculates similarity scores (Jaccard, edit distance, etc.)
- Identifies changed files, added/removed/changed counts
- Weights changes by significance (core files vs documentation)
- Generates distance vectors for clustering

---

## Guidance & Standards

- **Architecture:** [Comprehensive Guide](../guidance/COMPREHENSIVE_CLI_ARCHITECTURE_GUIDE.md)
- **Merging:** [Merge Guidance](../guidance/MERGE_GUIDANCE_DOCUMENTATION.md)
- **Patterns:** [Factory Pattern](../guidance/FACTORY_PATTERN_IMPLEMENTATION_GUIDE.md)
- **General:** [Project Guidance](../guidance/README.md)

---

## Success Criteria

- [ ] Multiple distance metrics implemented
- [ ] Handles large diffs efficiently
- [ ] Weighted scoring for file importance
- [ ] Outputs comparable distance vectors
- [ ] Performance optimized for many branches

---

## Test Strategy

- Compare identical branches (should be distance 0)
- Test with known similarity levels
- Benchmark performance on large repositories
- Validate weighting logic

---

---

## Implementation Notes

_Add implementation notes here as work progresses_

---

## Progress Log

### 2026-01-12
- Subtask file created from main task template
- Ready for implementation
**Priority:** high
**Effort:** 32-40 hours
**Complexity:** 8/10
**Dependencies:** None
**Created:** 2026-01-12
**Parent:** Task 002: Branch Clustering System

---

## Purpose

Calculate code distance metrics between feature branches and potential integration targets using various diff algorithms.

---

## Details

Implement a Python module that:
- Computes file-level diffs between branches
- Calculates similarity scores (Jaccard, edit distance, etc.)
- Identifies changed files, added/removed/changed counts
- Weights changes by significance (core files vs documentation)
- Generates distance vectors for clustering

---

## Guidance & Standards

- **Architecture:** [Comprehensive Guide](../guidance/COMPREHENSIVE_CLI_ARCHITECTURE_GUIDE.md)
- **Merging:** [Merge Guidance](../guidance/MERGE_GUIDANCE_DOCUMENTATION.md)
- **Patterns:** [Factory Pattern](../guidance/FACTORY_PATTERN_IMPLEMENTATION_GUIDE.md)
- **General:** [Project Guidance](../guidance/README.md)

---

## Success Criteria

- [ ] Multiple distance metrics implemented
- [ ] Handles large diffs efficiently
- [ ] Weighted scoring for file importance
- [ ] Outputs comparable distance vectors
- [ ] Performance optimized for many branches

---

## Test Strategy

- Compare identical branches (should be distance 0)
- Test with known similarity levels
- Benchmark performance on large repositories
- Validate weighting logic

---

---

## Implementation Notes

_Add implementation notes here as work progresses_

---

## Progress Log

### 2026-01-12
- Subtask file created from main task template
- Ready for implementation
**Dependencies:** None
**Created:** 2026-01-12
**Parent:** Task 002: Branch Clustering System

---

## Purpose

Calculate code distance metrics between feature branches and potential integration targets using various diff algorithms.

---

## Details

Implement a Python module that:
- Computes file-level diffs between branches
- Calculates similarity scores (Jaccard, edit distance, etc.)
- Identifies changed files, added/removed/changed counts
- Weights changes by significance (core files vs documentation)
- Generates distance vectors for clustering

---

## Guidance & Standards

- **Architecture:** [Comprehensive Guide](../guidance/COMPREHENSIVE_CLI_ARCHITECTURE_GUIDE.md)
- **Merging:** [Merge Guidance](../guidance/MERGE_GUIDANCE_DOCUMENTATION.md)
- **Patterns:** [Factory Pattern](../guidance/FACTORY_PATTERN_IMPLEMENTATION_GUIDE.md)
- **General:** [Project Guidance](../guidance/README.md)

---

## Success Criteria

- [ ] Multiple distance metrics implemented
- [ ] Handles large diffs efficiently
- [ ] Weighted scoring for file importance
- [ ] Outputs comparable distance vectors
- [ ] Performance optimized for many branches

---

## Test Strategy

- Compare identical branches (should be distance 0)
- Test with known similarity levels
- Benchmark performance on large repositories
- Validate weighting logic

---

---

## Implementation Notes

_Add implementation notes here as work progresses_

---

## Progress Log

### 2026-01-12
- Subtask file created from main task template
- Ready for implementation
**Effort:** TBD
**Complexity:** TBD

## Overview/Purpose
Implement a Python module that:
- Computes file-level diffs between branches
- Calculates similarity scores (Jaccard, edit distance, etc.)
- Identifies changed files, added/removed/changed counts
- We...

## Success Criteria

- [ ] [Success criteria to be defined]

## Prerequisites & Dependencies

### Required Before Starting
- [ ] None
**Created:** 2026-01-12
**Parent:** Task 002: Branch Clustering System

---

## Purpose

Calculate code distance metrics between feature branches and potential integration targets using various diff algorithms.

---

## Details

Implement a Python module that:
- Computes file-level diffs between branches
- Calculates similarity scores (Jaccard, edit distance, etc.)
- Identifies changed files, added/removed/changed counts
- Weights changes by significance (core files vs documentation)
- Generates distance vectors for clustering

---

## Guidance & Standards

- **Architecture:** [Comprehensive Guide](../guidance/COMPREHENSIVE_CLI_ARCHITECTURE_GUIDE.md)
- **Merging:** [Merge Guidance](../guidance/MERGE_GUIDANCE_DOCUMENTATION.md)
- **Patterns:** [Factory Pattern](../guidance/FACTORY_PATTERN_IMPLEMENTATION_GUIDE.md)
- **General:** [Project Guidance](../guidance/README.md)

---

## Success Criteria

- [ ] Multiple distance metrics implemented
- [ ] Handles large diffs efficiently
- [ ] Weighted scoring for file importance
- [ ] Outputs comparable distance vectors
- [ ] Performance optimized for many branches

---

## Test Strategy

- Compare identical branches (should be distance 0)
- Test with known similarity levels
- Benchmark performance on large repositories
- Validate weighting logic

---

---

## Implementation Notes

_Add implementation notes here as work progresses_

---

## Progress Log

### 2026-01-12
- Subtask file created from main task template
- Ready for implementation

### Blocks (What This Task Unblocks)
- [ ] None specified

### External Dependencies
- [ ] None

## Sub-subtasks Breakdown

# No subtasks defined

## Specification Details

### Task Interface
- **ID**: 
- **Title**: 
- **Status**: pending
**Priority:** high
**Effort:** 32-40 hours
**Complexity:** 8/10
**Dependencies:** None
**Created:** 2026-01-12
**Parent:** Task 002: Branch Clustering System

---

## Purpose

Calculate code distance metrics between feature branches and potential integration targets using various diff algorithms.

---

## Details

Implement a Python module that:
- Computes file-level diffs between branches
- Calculates similarity scores (Jaccard, edit distance, etc.)
- Identifies changed files, added/removed/changed counts
- Weights changes by significance (core files vs documentation)
- Generates distance vectors for clustering

---

## Guidance & Standards

- **Architecture:** [Comprehensive Guide](../guidance/COMPREHENSIVE_CLI_ARCHITECTURE_GUIDE.md)
- **Merging:** [Merge Guidance](../guidance/MERGE_GUIDANCE_DOCUMENTATION.md)
- **Patterns:** [Factory Pattern](../guidance/FACTORY_PATTERN_IMPLEMENTATION_GUIDE.md)
- **General:** [Project Guidance](../guidance/README.md)

---

## Success Criteria

- [ ] Multiple distance metrics implemented
- [ ] Handles large diffs efficiently
- [ ] Weighted scoring for file importance
- [ ] Outputs comparable distance vectors
- [ ] Performance optimized for many branches

---

## Test Strategy

- Compare identical branches (should be distance 0)
- Test with known similarity levels
- Benchmark performance on large repositories
- Validate weighting logic

---

---

## Implementation Notes

_Add implementation notes here as work progresses_

---

## Progress Log

### 2026-01-12
- Subtask file created from main task template
- Ready for implementation
- **Priority**: high
**Effort:** 32-40 hours
**Complexity:** 8/10
**Dependencies:** None
**Created:** 2026-01-12
**Parent:** Task 002: Branch Clustering System

---

## Purpose

Calculate code distance metrics between feature branches and potential integration targets using various diff algorithms.

---

## Details

Implement a Python module that:
- Computes file-level diffs between branches
- Calculates similarity scores (Jaccard, edit distance, etc.)
- Identifies changed files, added/removed/changed counts
- Weights changes by significance (core files vs documentation)
- Generates distance vectors for clustering

---

## Guidance & Standards

- **Architecture:** [Comprehensive Guide](../guidance/COMPREHENSIVE_CLI_ARCHITECTURE_GUIDE.md)
- **Merging:** [Merge Guidance](../guidance/MERGE_GUIDANCE_DOCUMENTATION.md)
- **Patterns:** [Factory Pattern](../guidance/FACTORY_PATTERN_IMPLEMENTATION_GUIDE.md)
- **General:** [Project Guidance](../guidance/README.md)

---

## Success Criteria

- [ ] Multiple distance metrics implemented
- [ ] Handles large diffs efficiently
- [ ] Weighted scoring for file importance
- [ ] Outputs comparable distance vectors
- [ ] Performance optimized for many branches

---

## Test Strategy

- Compare identical branches (should be distance 0)
- Test with known similarity levels
- Benchmark performance on large repositories
- Validate weighting logic

---

---

## Implementation Notes

_Add implementation notes here as work progresses_

---

## Progress Log

### 2026-01-12
- Subtask file created from main task template
- Ready for implementation
- **Effort**: N/A
- **Complexity**: N/A

## Implementation Guide

Implement a Python module that:
- Computes file-level diffs between branches
- Calculates similarity scores (Jaccard, edit distance, etc.)
- Identifies changed files, added/removed/changed counts
- Weights changes by significance (core files vs documentation)
- Generates distance vectors for clustering

## Configuration Parameters

- **Owner**: TBD
- **Initiative**: TBD
- **Scope**: TBD
- **Focus**: TBD

## Performance Targets

- **Effort Range**: TBD
- **Complexity Level**: TBD

## Testing Strategy

### Unit Tests
- [ ] Tests cover core functionality
- [ ] Edge cases handled appropriately
- [ ] Performance benchmarks met

### Integration Tests
- [ ] Integration with dependent components verified
- [ ] End-to-end workflow tested
- [ ] Error handling verified

### Test Strategy Notes
- Compare identical branches (should be distance 0)
- Test with known similarity levels
- Benchmark performance on large repositories
- Validate weighting logic

## Common Gotchas & Solutions

- [ ] [Common issues and solutions to be documented]

## Integration Checkpoint

### Criteria for Moving Forward
- [ ] All success criteria met
- [ ] Code reviewed and approved
- [ ] Tests passing
- [ ] Documentation updated
- [ ] No critical or high severity issues

## Done Definition

### Completion Criteria
- [ ] All success criteria checkboxes marked complete
- [ ] Code quality standards met (PEP 8, documentation)
- [ ] Performance targets achieved
- [ ] All subtasks completed
- [ ] Integration checkpoint criteria satisfied

## Next Steps

1. **Implementation Phase**: Begin with Phase 1 implementation focusing on class structure and architecture
2. **Unit Testing**: Develop comprehensive test suite with 8+ test cases covering all metrics
3. **Integration Testing**: Verify output compatibility with Task 002.4 (BranchClusterer) input requirements
4. **Performance Validation**: Confirm analysis completes in under 3 seconds per branch
5. **Code Review**: Submit for peer review ensuring PEP 8 compliance and comprehensive documentation
6. **Handoff Preparation**: Prepare for integration with Task 002.4 once implementation is complete
7. **Documentation**: Complete any remaining documentation gaps identified during implementation


<!-- EXTENDED_METADATA
END_EXTENDED_METADATA -->

## Configuration Parameters

- **Owner**: TBD
- **Initiative**: TBD
- **Scope**: TBD
- **Focus**: TBD

---

<!-- IMPORTED_FROM: backup_task75/task-002.3.md -->
- `CODE_CHURN_WEIGHT` = 0.30
- `CHANGE_CONCENTRATION_WEIGHT` = 0.25
- `DIFF_COMPLEXITY_WEIGHT` = 0.25
- `INTEGRATION_RISK_WEIGHT` = 0.20
- `ESTIMATED_CODEBASE_SIZE` = 5000
- `MAX_EXPECTED_FILES` = 50
- `RISK_CATEGORY_FILES` = {...}

---

## Performance Targets

- **Effort Range**: 32-40 hours
- **Complexity Level**: 8/10

## Testing Strategy

### Unit Testing Approach
- **Minimum 8 test cases** covering all 4 metrics individually
- **Edge case testing** for binary files, large diffs, empty diffs
- **Performance testing** to ensure <3 second execution time
- **Code coverage** >95% across all functions and branches

### Test Cases to Implement

**Test Case 1: Normal Branch Analysis**
- Input: Branch with 420 lines changed, 12 files modified, moderate churn
- Expected: All metrics return values in [0,1], aggregate score calculated correctly
- Validation: Output matches JSON schema exactly

**Test Case 2: High Churn Branch**
- Input: Branch with 5000+ lines changed in few files
- Expected: High code churn and complexity scores
- Validation: Performance remains under 3 seconds

**Test Case 3: Low Churn Branch**
- Input: Branch with 10-20 lines changed, few files
- Expected: Low churn metrics, high stability scores
- Validation: No exceptions raised, proper handling

**Test Case 4: Binary File Branch**
- Input: Branch with binary files only
- Expected: Proper handling of binary files without errors
- Validation: Binary files filtered out gracefully

**Test Case 5: Non-existent Branch**
- Input: Branch name that doesn't exist
- Expected: Appropriate error handling without exception
- Validation: Returns error object or raises specific exception

**Test Case 6: Empty Diff Branch**
- Input: Branch with no differences from main
- Expected: Neutral scores (around 0.5) for most metrics
- Validation: No calculation errors, valid output

**Test Case 7: Single File Change**
- Input: Branch with only 1 file changed
- Expected: Proper handling of edge case for all metrics
- Validation: No calculation errors, valid output

**Test Case 8: Large Repository Branch**
- Input: Branch in repository with 10,000+ commits and large diffs
- Expected: Performance under 3 seconds, no memory issues
- Validation: Proper timeout handling, memory usage <100MB

### Integration Testing
- Test with real repository fixtures
- Verify output compatibility with Task 002.4 (BranchClusterer)
- End-to-end pipeline validation
- Cross-validation with manual analysis

## Common Gotchas & Solutions

### Gotcha 1: Git Command Timeouts ⚠️
**Problem:** Git diff commands hang on large diffs with 10,000+ file changes
**Symptom:** Process hangs for more than 30 seconds during git diff
**Root Cause:** Git operations on very large diffs can take a long time
**Solution:** Add timeout to subprocess calls
```python
import subprocess
result = subprocess.run([
    "git", "diff", f"{main_branch}...{branch_name}", "--numstat"
], capture_output=True, text=True, timeout=30)  # 30-second timeout
```

### Gotcha 2: Binary File Handling ⚠️
**Problem:** Binary files cause parsing errors in diff analysis
**Symptom:** ValueError when parsing diff output with binary files
**Root Cause:** Binary files don't have line-based changes that can be counted
**Solution:** Filter out binary files from diff analysis
```python
def _extract_diff_data(self, branch_name: str) -> dict:
    # ... git command execution ...
    for line in lines:
        if line.strip():
            # Skip binary files which show '-' for line counts
            if '\t-\t' in line:  # Binary file detected
                continue
            # ... process text files
```

### Gotcha 3: Division by Zero ⚠️
**Problem:** Calculations fail when denominators are zero
**Symptom:** ZeroDivisionError during metric calculations
**Root Cause:** Not checking for zero values in denominators
**Solution:** Add checks for zero values
```python
def calculate_churn_ratio(lines_changed, total_lines):
    if total_lines == 0:
        total_lines = 1  # Prevent division by zero
    return lines_changed / total_lines
```

### Gotcha 4: Bounds Checking for Metrics ⚠️
**Problem:** Metrics fall outside [0,1] range
**Symptom:** Values less than 0 or greater than 1 in metrics
**Root Cause:** Not clamping calculated values to valid range
**Solution:** Ensure all metrics are in [0,1] range
```python
def clamp(value, min_val=0, max_val=1):
    return max(min_val, min(max_val, value))

churn_score = clamp(calculated_churn)
```

### Gotcha 5: Large Repository Memory Usage ⚠️
**Problem:** High memory consumption when processing large diffs
**Symptom:** Process killed by OS due to memory limits
**Root Cause:** Loading all diff data into memory at once
**Solution:** Process diffs in chunks or use streaming
```python
def _process_large_diff(self, diff_output: str):
    # Process diff output line by line instead of loading all at once
    # Use generators for memory efficiency
    # Consider processing in batches for very large diffs
```

## Integration Checkpoint

### Criteria for Moving Forward
- [ ] All success criteria met
- [ ] Code reviewed and approved
- [ ] Tests passing
- [ ] Documentation updated
- [ ] No critical or high severity issues

---

<!-- IMPORTED_FROM: backup_task75/task-002.3.md -->
**When to move to 002.4:**
- [ ] All 8 subtasks complete
- [ ] Unit tests passing (>90% coverage)
- [ ] Output matches specification
- [ ] Handles all edge cases
- [ ] Ready for integration with other Stage One analyzers

---

## Done Definition

### Completion Criteria
- [ ] All success criteria met
- [ ] Code reviewed and approved
- [ ] Tests passing
- [ ] Documentation updated

---

<!-- IMPORTED_FROM: backup_task75/task-002.3.md -->
Task 002.3 is done when:
1. All 8 subtasks marked complete
2. Unit tests pass (>95% coverage)
3. Code review approved
4. Outputs match specification
5. Documentation complete
6. Ready for hand-off to Task 002.4

## Next Steps

1. **Implementation Phase**: Begin with Phase 1 implementation focusing on class structure and architecture
2. **Unit Testing**: Develop comprehensive test suite with 8+ test cases covering all metrics
3. **Integration Testing**: Verify output compatibility with Task 002.4 (BranchClusterer) input requirements
4. **Performance Validation**: Confirm analysis completes in under 3 seconds per branch
5. **Code Review**: Submit for peer review ensuring PEP 8 compliance and comprehensive documentation
6. **Handoff Preparation**: Prepare for integration with Task 002.4 once implementation is complete
7. **Documentation**: Complete any remaining documentation gaps identified during implementation
