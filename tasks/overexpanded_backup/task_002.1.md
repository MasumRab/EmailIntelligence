# Task 002.1: CommitHistoryAnalyzer

**Status:** pending
**Priority:** high
**Effort:** 24-32 hours
**Complexity:** 7/10
**Dependencies:** None

---

## Overview/Purpose

Analyze Git commit history for each feature branch to extract metrics like commit frequency, author patterns, merge points, and branch divergence dates.

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

- [ ] Module fetches and analyzes all feature branches
- [ ] Generates commit history metrics for each branch
- [ ] Identifies merge bases with all primary targets
- [ ] Outputs structured JSON for downstream processing
- [ ] Unit tests cover all extraction functions

---

<!-- IMPORTED_FROM: backup_task75/task-002.1.md -->
Task 002.1 is complete when:

**Core Functionality:**
- [ ] `CommitHistoryAnalyzer` class accepts `repo_path` (str) and `branch_name` (str) parameters
- [ ] Successfully extracts commit data using git log commands with proper parsing
- [ ] Computes exactly 5 normalized metrics in [0,1] range with specified formulas
- [ ] Returns properly formatted dict with all required fields and aggregate score
- [ ] Handles all specified edge cases gracefully (non-existent, new, stale, orphaned branches)
- [ ] Output matches JSON schema exactly (validated against schema specification)

**Quality Assurance:**
- [ ] Unit tests pass (minimum 8 test cases with >95% code coverage)
- [ ] No exceptions raised for valid inputs (comprehensive error handling)
- [ ] Performance: <2 seconds per branch analysis on standard hardware
- [ ] Code quality: Passes linting, follows PEP 8, includes comprehensive docstrings

**Integration Readiness:**
- [ ] Compatible with Task 002.4 (BranchClusterer) input requirements
- [ ] Compatible with Task 002.6 (PipelineIntegration) consumption patterns
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
TASK 002.1.1 (2-3h) ──────┐
[Design Metric System]       │
                           ├─→ TASK 002.1.2 (4-5h) ──────┐
                           │  [Set Up Git Data Extraction] │
                           │                              ├─→ TASKS 002.1.3-002.1.7 (sequential) ────┐
                           │                              │   [Metrics Implementation]                  │
                           │                              │                                         ├─→ TASK 002.1.8 (3-4h)
                           └──────────────────────────────┘                                         │  [Unit Tests]
                                                                                                  │
                                                                                                  └─→ TASK 002.1.8 (3-4h)
                                                                                                     [Unit Tests]

Critical Path: TASK 002.1.1 → TASK 002.1.2 → TASKS 002.1.3-002.1.7 (sequential) → TASK 002.1.8
Minimum Duration: 18-25 hours (mostly sequential)
```

### Parallel Opportunities

**Can run in parallel (after TASK 002.1.2):**
- TASK 002.1.3: Implement Commit Recency Metric
- TASK 002.1.4: Implement Commit Frequency Metric
- TASK 002.1.5: Implement Authorship & Stability Metrics
- TASK 002.1.6: Implement Merge Readiness Metric

All tasks depend only on [parent task] and are independent of each other. **Estimated parallel execution saves 6-8 hours.**

**Must be sequential:**
- TASK 002.1.1 → TASK 002.1.2 (need architecture before extraction)
- TASK 002.1.2 → TASKS 002.1.3-002.1.6 (need extraction before metrics)
- TASKS 002.1.3-002.1.6 → TASK 002.1.7 (need metrics before aggregation)
- TASK 002.1.7 → TASK 002.1.8 (need aggregation before testing)

### Timeline with Parallelization

**Days 1-2: [First Phase] (TASK 002.1.1-TASK 002.1.2)**
- TASK 002.1.1: Design Metric System
- TASK 002.1.2: Set Up Git Data Extraction

**Days 2-4: [Parallel Phase] (TASKS 002.1.3-002.1.6 in parallel)**
- Days 2-3: TASK 002.1.3 + TASK 002.1.4 (2 people)
- Days 3-4: TASK 002.1.5 + TASK 002.1.6 (2 people)

**Days 4-5: [Integration Phase] (TASKS 002.1.7-002.1.8)**
- Day 4: TASK 002.1.7 (Aggregate Metrics & Output Formatting)
- Day 5: TASK 002.1.8 (Write Unit Tests)

---

## Sub-subtasks Breakdown

### 002.1.1: Design Metric System
**Purpose:** Define how metrics will be calculated and combined
**Effort:** 2-3 hours

**Steps:**
1. Define the 5 core metrics with mathematical formulas
2. Document calculation approach for each metric
3. Create normalization strategy (ensure all metrics in [0,1] range)
4. Create weighting scheme: 0.25/0.20/0.20/0.20/0.15 (sum = 1.0)
5. Document edge case handling for each metric

**Success Criteria:**
- [ ] All 5 metrics clearly defined with formulas
- [ ] Calculation approach specified
- [ ] Normalization approach specified
- [ ] Weights documented
- [ ] Edge case handling documented

**Blocks:** 002.1.2, 002.1.3, 002.1.4, 002.1.5

---

### 002.1.2: Set Up Git Data Extraction
**Purpose:** Create functions to extract commit data from git repository
**Effort:** 4-5 hours
**Depends on:** 002.1.1

**Steps:**
1. Create utility functions for git command execution
2. Implement branch validation (check if branch exists)
3. Create commit log extraction (get all commits on branch)
4. Create commit metadata extraction (dates, authors, messages)
5. Add error handling (invalid branch, repo not found, git errors)

**Success Criteria:**
- [ ] Can execute git commands without errors
- [ ] Validates branch existence before processing
- [ ] Extracts commit list with metadata
- [ ] Handles non-existent branches gracefully
- [ ] Returns structured data (list of dicts)

**Blocks:** 002.1.3, 002.1.4, 002.1.5

---

### 002.1.3: Implement Commit Recency Metric
**Purpose:** Score how recent the branch's commits are
**Effort:** 3-4 hours
**Depends on:** 002.1.1, 002.1.2

**Steps:**
1. Extract commit dates from branch
2. Calculate time since last commit
3. Define recency decay function
4. Set time window (e.g., 30 days)
5. Normalize to 0-1 range
6. Test with recent and old branches

**Success Criteria:**
- [ ] Returns value in [0, 1] range
- [ ] Recent commits (last 7 days) score > 0.8
- [ ] Old commits (90+ days) score < 0.3
- [ ] Correctly handles single-commit branches
- [ ] Consistent calculation across test cases

---

### 002.1.4: Implement Commit Frequency Metric
**Purpose:** Score how active the branch is (velocity)
**Effort:** 3-4 hours
**Depends on:** 002.1.1, 002.1.2

**Steps:**
1. Count total commits on branch
2. Calculate branch lifetime (days from first to last commit)
3. Compute velocity (commits per day)
4. Define frequency baseline and scoring
5. Normalize to 0-1 range
6. Test with high-activity and low-activity branches

**Success Criteria:**
- [ ] Returns value in [0, 1] range
- [ ] High activity (>5 commits/week) scores > 0.7
- [ ] Low activity (<1 commit/week) scores < 0.4
- [ ] Correctly handles single-commit branches
- [ ] Handles very old branches (>100 days)

---

### 002.1.5: Implement Authorship & Stability Metrics
**Purpose:** Score author diversity and code stability
**Effort:** 4-5 hours
**Depends on:** 002.1.1, 002.1.2

**Steps for authorship_diversity:**
1. Extract unique author names from commits
2. Count total commits vs unique authors
3. Calculate diversity ratio (unique / total)
4. Normalize to 0-1 range

**Steps for stability_score:**
1. Extract line change statistics per commit
2. Calculate average churn per commit
3. Define stability baseline (inverse of churn)
4. Normalize to 0-1 range

**Success Criteria:**
- [ ] Authorship: Returns value in [0, 1] range
- [ ] Authorship: Single author scores ~0.3, multiple authors score higher
- [ ] Stability: Returns value in [0, 1] range
- [ ] Stability: Low churn scores > 0.7, high churn scores < 0.4
- [ ] Handles edge cases (binary files, deletions)

---

### 002.1.6: Implement Merge Readiness Metric
**Purpose:** Score how synchronized branch is with main
**Effort:** 3-4 hours
**Depends on:** 002.1.1, 002.1.2

**Steps:**
1. Find merge base between branch and main
2. Count commits since merge base on both branches
3. Calculate how far behind main the branch is
4. Define readiness formula (closer to main = higher score)
5. Normalize to 0-1 range

**Success Criteria:**
- [ ] Returns value in [0, 1] range
- [ ] Recently synced (<5 commits behind) scores > 0.85
- [ ] Far behind (>50 commits behind) scores < 0.4
- [ ] Correctly handles branches merged from main
- [ ] Handles newly-created branches

---

### 002.1.7: Aggregate Metrics & Output Formatting
**Purpose:** Combine 5 metrics into single score and format output
**Effort:** 2-3 hours
**Depends on:** 002.1.3, 002.1.4, 002.1.5, 002.1.6

**Steps:**
1. Define metric weights (sum to 1.0)
2. Create aggregation function (weighted sum)
3. Verify all metrics in [0,1] before aggregating
4. Format output dict (branch name, metrics dict, aggregate score, metadata)
5. Add timestamp

**Success Criteria:**
- [ ] Aggregate score = 0.25*m1 + 0.20*m2 + 0.20*m3 + 0.20*m4 + 0.15*m5
- [ ] Returns value in [0, 1] range
- [ ] Output dict has all required fields
- [ ] Timestamp in ISO format
- [ ] No missing or extra fields

---

### 002.1.8: Write Unit Tests
**Purpose:** Verify CommitHistoryAnalyzer works correctly
**Effort:** 3-4 hours
**Depends on:** 002.1.7

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
- [ ] Performance tests meet <2 second requirement

---

## Specification Details

### Task Interface
- **ID**: 002.1
- **Title**: CommitHistoryAnalyzer
- **Status**: pending
- **Priority**: high
- **Effort**: 24-32 hours
- **Complexity**: 7/10

### Requirements
**Core Requirements:**
- Python 3.8+ runtime environment
- Git installed and accessible from command line
- Access to local git repository with feature branches
- GitPython library or subprocess access for git commands
- YAML parser for configuration files

**Functional Requirements:**
- Must accept repository path and branch name as input parameters
- Must extract commit history data using git log commands
- Must compute 5 specific metrics with normalized values in [0,1] range
- Must return structured output matching JSON schema specification
- Must handle edge cases (non-existent branches, new branches, etc.)

**Non-functional Requirements:**
- Performance: Complete analysis in under 2 seconds per branch
- Reliability: Handle all error conditions gracefully without crashing
- Scalability: Support repositories with up to 10,000+ commits
- Maintainability: Follow PEP 8 standards with comprehensive docstrings
- Testability: Achieve >95% code coverage with unit tests

### Task Interface
- **ID**: UNKNOWN
- **Title**: Untitled Task
- **Status**: pending
- **Priority**: high
- **Effort**: 24-32 hours
- **Complexity**: 7/10

### Requirements

**Core Requirements:**
- Python 3.8+ runtime environment
- Git installed and accessible from command line
- Access to local git repository with feature branches
- GitPython library or subprocess access for git commands
- YAML parser for configuration files

**Functional Requirements:**
- Must accept repository path and branch name as input parameters
- Must extract commit history data using git log commands
- Must compute 5 specific metrics with normalized values in [0,1] range
- Must return structured output matching JSON schema specification
- Must handle edge cases (non-existent branches, new branches, etc.)

**Non-functional Requirements:**
- Performance: Complete analysis in under 2 seconds per branch
- Reliability: Handle all error conditions gracefully without crashing
- Scalability: Support repositories with up to 10,000+ commits
- Maintainability: Follow PEP 8 standards with comprehensive docstrings
- Testability: Achieve >95% code coverage with unit tests

## Implementation Guide

### Phase 1: Setup and Architecture (Days 1-2)
1. Create the basic class structure for `CommitHistoryAnalyzer`
2. Implement repository validation and initialization
3. Set up configuration loading from YAML
4. Create the basic method signatures

### Phase 2: Git Data Extraction (Days 2-3)
1. Implement git command execution with proper error handling
2. Extract commit data using `git log` commands
3. Parse commit metadata (dates, authors, messages)
4. Handle edge cases (non-existent branches, invalid repos)

### Phase 3: Metric Implementation (Days 3-5)
1. Implement the 5 core metrics:
   - Commit recency metric (exponential decay function)
   - Commit frequency metric (velocity calculation)
   - Authorship diversity metric (ratio calculation)
   - Merge readiness metric (comparison with main branch)
   - Stability score metric (churn calculation)
2. Ensure all metrics return values in [0,1] range
3. Add proper normalization and bounds checking

### Phase 4: Integration and Testing (Days 5-6)
1. Integrate all metrics into a weighted aggregation function
2. Format output according to specification
3. Write comprehensive unit tests (8+ test cases)
4. Perform performance testing to ensure <2s execution time

### Key Implementation Notes:
- Use subprocess with timeout for git commands to prevent hanging
- Implement proper error handling for all edge cases
- Ensure all metrics are normalized to [0,1] range
- Follow the configuration parameters specified in the Configuration section
- Add comprehensive logging and error reporting

<!-- IMPORTED_FROM: /home/masum/github/PR/.taskmaster/enhanced_improved_tasks/task-002-1.md -->

<!-- IMPORTED_FROM: /home/masum/github/PR/.taskmaster/task_data/archived/backups_archive_task002/task-002.1.md -->

# Task 002.1: CommitHistoryAnalyzer

<!-- IMPORTED_FROM: /home/masum/github/PR/.taskmaster/task_data/archived/handoff_archive_task002/HANDOFF_002.1_CommitHistoryAnalyzer.md -->

# Task 002.1: CommitHistoryAnalyzer Implementation

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
- No internal dependencies on other Task 002.x components
- Output feeds into **Task 002.4 (BranchClusterer)**

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
3. Pass output to Task 002.4 integration point
4. Verify metrics sum to 0-1 range

**Parallel tasks ready:** 002.2, 002.3 (no dependencies)

## Purpose
Create a reusable Python class that extracts and scores commit history metrics for branches. This analyzer is one of three Stage One components that will be integrated into the clustering pipeline.

**Scope:** CommitHistoryAnalyzer class only  
**Effort:** 24-32 hours | **Complexity:** 7/10  
**Status:** Ready for implementation  
**No dependencies** - can start immediately

---

## Success Criteria

Task 002.1 is complete when:

**Core Functionality:**
- [ ] `CommitHistoryAnalyzer` class accepts `repo_path` (str) and `branch_name` (str) parameters
- [ ] Successfully extracts commit data using git log commands with proper parsing
- [ ] Computes exactly 5 normalized metrics in [0,1] range with specified formulas
- [ ] Returns properly formatted dict with all required fields and aggregate score
- [ ] Handles all specified edge cases gracefully (non-existent, new, stale, orphaned branches)
- [ ] Output matches JSON schema exactly (validated against schema specification)

**Quality Assurance:**
- [ ] Unit tests pass (minimum 8 test cases with >95% code coverage)
- [ ] No exceptions raised for valid inputs (comprehensive error handling)
- [ ] Performance: <2 seconds per branch analysis on standard hardware
- [ ] Code quality: Passes linting, follows PEP 8, includes comprehensive docstrings

**Integration Readiness:**
- [ ] Compatible with Task 002.4 (BranchClusterer) input requirements
- [ ] Compatible with Task 002.6 (PipelineIntegration) consumption patterns
- [ ] Configuration externalized and validated
- [ ] Documentation complete and accurate

---

## Subtasks

### 002.1.1: Design Metric System
**Purpose:** Define how metrics will be calculated and combined  
**Effort:** 2-3 hours

**Steps:**
1. Define the 5 core metrics with mathematical formulas
2. Document calculation approach for each metric
3. Create normalization strategy (ensure all metrics in [0,1] range)
4. Create weighting scheme: 0.25/0.20/0.20/0.20/0.15 (sum = 1.0)
5. Document edge case handling for each metric

**Success Criteria:**
- [ ] All 5 metrics clearly defined with formulas
- [ ] Calculation approach specified
- [ ] Normalization approach specified
- [ ] Weights documented
- [ ] Edge case handling documented

**Blocks:** 002.1.2, 002.1.3, 002.1.4, 002.1.5

---

### 002.1.2: Set Up Git Data Extraction
**Purpose:** Create functions to extract commit data from git repository  
**Effort:** 4-5 hours  
**Depends on:** 002.1.1

**Steps:**
1. Create utility functions for git command execution
2. Implement branch validation (check if branch exists)
3. Create commit log extraction (get all commits on branch)
4. Create commit metadata extraction (dates, authors, messages)
5. Add error handling (invalid branch, repo not found, git errors)

**Success Criteria:**
- [ ] Can execute git commands without errors
- [ ] Validates branch existence before processing
- [ ] Extracts commit list with metadata
- [ ] Handles non-existent branches gracefully
- [ ] Returns structured data (list of dicts)

**Blocks:** 002.1.3, 002.1.4, 002.1.5

---

### 002.1.3: Implement Commit Recency Metric
**Purpose:** Score how recent the branch's commits are  
**Effort:** 3-4 hours  
**Depends on:** 002.1.1, 002.1.2

**Steps:**
1. Extract commit dates from branch
2. Calculate time since last commit
3. Define recency decay function
4. Set time window (e.g., 30 days)
5. Normalize to 0-1 range
6. Test with recent and old branches

**Success Criteria:**
- [ ] Returns value in [0, 1] range
- [ ] Recent commits (last 7 days) score > 0.8
- [ ] Old commits (90+ days) score < 0.3
- [ ] Correctly handles single-commit branches
- [ ] Consistent calculation across test cases

---

### 002.1.4: Implement Commit Frequency Metric
**Purpose:** Score how active the branch is (velocity)  
**Effort:** 3-4 hours  
**Depends on:** 002.1.1, 002.1.2

**Steps:**
1. Count total commits on branch
2. Calculate branch lifetime (days from first to last commit)
3. Compute velocity (commits per day)
4. Define frequency baseline and scoring
5. Normalize to 0-1 range
6. Test with high-activity and low-activity branches

**Success Criteria:**
- [ ] Returns value in [0, 1] range
- [ ] High activity (>5 commits/week) scores > 0.7
- [ ] Low activity (<1 commit/week) scores < 0.4
- [ ] Correctly handles single-commit branches
- [ ] Handles very old branches (>100 days)

---

### 002.1.5: Implement Authorship & Stability Metrics
**Purpose:** Score author diversity and code stability  
**Effort:** 4-5 hours  
**Depends on:** 002.1.1, 002.1.2

**Steps for authorship_diversity:**
1. Extract unique author names from commits
2. Count total commits vs unique authors
3. Calculate diversity ratio (unique / total)
4. Normalize to 0-1 range

**Steps for stability_score:**
1. Extract line change statistics per commit
2. Calculate average churn per commit
3. Define stability baseline (inverse of churn)
4. Normalize to 0-1 range

**Success Criteria:**
- [ ] Authorship: Returns value in [0, 1] range
- [ ] Authorship: Single author scores ~0.3, multiple authors score higher
- [ ] Stability: Returns value in [0, 1] range
- [ ] Stability: Low churn scores > 0.7, high churn scores < 0.4
- [ ] Handles edge cases (binary files, deletions)

---

### 002.1.6: Implement Merge Readiness Metric
**Purpose:** Score how synchronized branch is with main  
**Effort:** 3-4 hours  
**Depends on:** 002.1.1, 002.1.2

**Steps:**
1. Find merge base between branch and main
2. Count commits since merge base on both branches
3. Calculate how far behind main the branch is
4. Define readiness formula (closer to main = higher score)
5. Normalize to 0-1 range

**Success Criteria:**
- [ ] Returns value in [0, 1] range
- [ ] Recently synced (<5 commits behind) scores > 0.85
- [ ] Far behind (>50 commits behind) scores < 0.4
- [ ] Correctly handles branches merged from main
- [ ] Handles newly-created branches

---

### 002.1.7: Aggregate Metrics & Output Formatting
**Purpose:** Combine 5 metrics into single score and format output  
**Effort:** 2-3 hours  
**Depends on:** 002.1.3, 002.1.4, 002.1.5, 002.1.6

**Steps:**
1. Define metric weights (sum to 1.0)
2. Create aggregation function (weighted sum)
3. Verify all metrics in [0,1] before aggregating
4. Format output dict (branch name, metrics dict, aggregate score, metadata)
5. Add timestamp

**Success Criteria:**
- [ ] Aggregate score = 0.25*m1 + 0.20*m2 + 0.20*m3 + 0.20*m4 + 0.15*m5
- [ ] Returns value in [0, 1] range
- [ ] Output dict has all required fields
- [ ] Timestamp in ISO format
- [ ] No missing or extra fields

---

### 002.1.8: Write Unit Tests
**Purpose:** Verify CommitHistoryAnalyzer works correctly  
**Effort:** 3-4 hours  
**Depends on:** 002.1.7

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
- [ ] Performance tests meet <2 second requirement

---

## Configuration & Defaults

All parameters should be externalized to configuration files (not hardcoded). Use YAML format:

```yaml
# config/commit_history_analyzer.yaml
commit_history_analyzer:
  # Metric Weights
  commit_recency_weight: 0.25          # Weight for commit recency metric
  commit_frequency_weight: 0.20        # Weight for commit frequency metric
  authorship_diversity_weight: 0.20    # Weight for authorship diversity metric
  merge_readiness_weight: 0.20         # Weight for merge readiness metric
  stability_score_weight: 0.15         # Weight for stability score metric

  # Time Windows
  recency_window_days: 30              # Window for recency calculation
  frequency_baseline_commits_per_week: 5 # Baseline for frequency scoring

  # Thresholds
  stability_baseline_lines_per_commit: 50 # Baseline for stability scoring
  merge_readiness_max_commits_behind: 50 # Max commits behind main for high readiness
  git_command_timeout_seconds: 30      # Timeout for git commands
```

**How to use in code:**
```python
import yaml

def load_config(config_path='config/commit_history_analyzer.yaml'):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)['commit_history_analyzer']

config = load_config()
COMMIT_RECENCY_WEIGHT = config['commit_recency_weight']
COMMIT_FREQUENCY_WEIGHT = config['commit_frequency_weight']
AUTHORSHIP_DIVERSITY_WEIGHT = config['authorship_diversity_weight']
MERGE_READINESS_WEIGHT = config['merge_readiness_weight']
STABILITY_SCORE_WEIGHT = config['stability_score_weight']
RECENCY_WINDOW_DAYS = config['recency_window_days']
FREQUENCY_BASELINE_COMMITS_PER_WEEK = config['frequency_baseline_commits_per_week']
STABILITY_BASELINE_LINES_PER_COMMIT = config['stability_baseline_lines_per_commit']
MERGE_READINESS_MAX_COMMITS_BEHIND = config['merge_readiness_max_commits_behind']
GIT_COMMAND_TIMEOUT_SECONDS = config['git_command_timeout_seconds']
```

**Why externalize?**
- Easy to tune without redeploying code
- Different configurations for different environments (dev/test/prod)
- Can adjust thresholds based on organizational needs
- No code recompilation needed to adjust parameters

---

## Typical Development Workflow

Complete step-by-step git workflow for implementing this task. Copy-paste ready sequences:

### Setup Your Feature Branch

```bash
# 1. Create and push feature branch
git checkout -b feat/commit-history-analyzer
git push -u origin feat/commit-history-analyzer

# 2. Create directory structure
mkdir -p src/analyzers tests/analyzers
touch src/analyzers/__init__.py
git add src/analyzers/
git commit -m "chore: create analyzers module structure"
```

### Subtask 002.1.1: Design Metric System

```bash
# Create initial module file
cat > src/analyzers/commit_history_analyzer.py << 'EOF'
"""
Commit History Analyzer Module
"""
class CommitHistoryAnalyzer:
    def __init__(self, repo_path: str, main_branch: str = "main"):
        self.repo_path = repo_path
        self.main_branch = main_branch

    def analyze(self, branch_name: str) -> dict:
        """Analyze commit history and return metrics."""
        pass
EOF

git add src/analyzers/commit_history_analyzer.py
git commit -m "feat: implement CommitHistoryAnalyzer skeleton (Task 002.1)"
```

### Subtask 002.1.2: Set Up Git Data Extraction

```bash
# Update the analyzer to implement git data extraction
cat >> src/analyzers/commit_history_analyzer.py << 'EOF'

    def _extract_git_data(self, branch_name: str) -> dict:
        """Extract commit data for a branch."""
        import subprocess
        import os
        from datetime import datetime

        os.chdir(self.repo_path)

        # Get commits unique to branch (not in main)
        result = subprocess.run([
            "git", "log", f"{self.main_branch}..{branch_name}",
            "--pretty=format:%H|%ai|%an|%s"
        ], capture_output=True, text=True, timeout=30)

        if result.returncode != 0:
            raise Exception(f"Git command failed: {result.stderr}")

        commits = []
        for line in result.stdout.strip().split('\n'):
            if line.strip():
                parts = line.split('|')
                if len(parts) == 4:
                    commits.append({
                        'hash': parts[0],
                        'date': parts[1],
                        'author': parts[2],
                        'message': parts[3]
                    })

        return {'commits': commits}
EOF

git add src/analyzers/commit_history_analyzer.py
git commit -m "feat: implement git data extraction for CommitHistoryAnalyzer (Task 002.1.2)"
```

[Repeat for each major subtask]

### Final Steps

```bash
# Create configuration file
mkdir -p config
cat > config/commit_history_analyzer.yaml << 'EOF'
commit_history_analyzer:
  # Metric Weights
  commit_recency_weight: 0.25          # Weight for commit recency metric
  commit_frequency_weight: 0.20        # Weight for commit frequency metric
  authorship_diversity_weight: 0.20    # Weight for authorship diversity metric
  merge_readiness_weight: 0.20         # Weight for merge readiness metric
  stability_score_weight: 0.15         # Weight for stability score metric

  # Time Windows
  recency_window_days: 30              # Window for recency calculation
  frequency_baseline_commits_per_week: 5 # Baseline for frequency scoring

  # Thresholds
  stability_baseline_lines_per_commit: 50 # Baseline for stability scoring
  merge_readiness_max_commits_behind: 50 # Max commits behind main for high readiness
  git_command_timeout_seconds: 30      # Timeout for git commands
EOF

git add config/
git commit -m "config: CommitHistoryAnalyzer configuration parameters"

# Push to origin
git push origin feat/commit-history-analyzer

# Create pull request
gh pr create --title "Complete Task 002.1: CommitHistoryAnalyzer" \
             --body "Implements CommitHistoryAnalyzer with commit recency, frequency, authorship diversity, merge readiness, and stability metrics"
```

---

## Integration Handoff

### What Gets Passed to Task 002.4 (Downstream Task)

**Task 002.4 expects input in this format:**

```python
from src.analyzers.commit_history_analyzer import CommitHistoryAnalyzer

analyzer = CommitHistoryAnalyzer(repo_path, main_branch)
result = analyzer.analyze(branch_name)

# result is a dict like:
# {
#   "branch_name": "feature/branch-name",
#   "metrics": {
#     "commit_recency": 0.87,
#     "commit_frequency": 0.65,
#     "authorship_diversity": 0.72,
#     "merge_readiness": 0.91,
#     "stability_score": 0.58
#   },
#   "aggregate_score": 0.749,
#   "commit_count": 42,
#   "days_active": 18,
#   "unique_authors": 3,
#   "analysis_timestamp": "2025-12-22T10:30:00Z"
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
from src.analyzers.commit_history_analyzer import CommitHistoryAnalyzer
analyzer = CommitHistoryAnalyzer('/path/to/repo', 'main')
result = analyzer.analyze('some-branch')

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

### Gotcha 1: Git Command Timeout ⚠️

**Problem:** Git commands hang on large repositories with 10,000+ commits
**Symptom:** Process hangs for more than 30 seconds during git log
**Root Cause:** Git operations on very large repositories can take a long time

**Solution:** Add timeout to subprocess calls
```python
import subprocess
result = subprocess.run([
    "git", "log", f"{main_branch}..{branch_name}", "--pretty=format:%H|%ai|%an|%s"
], capture_output=True, text=True, timeout=30)  # 30-second timeout
```

**Test:** Verify timeout handling works by testing with a temporarily large repository

---

### Gotcha 2: Division by Zero ⚠️

**Problem:** Calculations fail when denominators are zero
**Symptom:** ZeroDivisionError during metric calculations
**Root Cause:** Not checking for zero values in denominators

**Solution:** Add checks for zero values
```python
def calculate_frequency(commits, days_active):
    if days_active == 0:
        days_active = 1  # Prevent division by zero
    return len(commits) / days_active
```

**Test:** Verify that branches with 0 days active don't cause errors

---

### Gotcha 3: Date Parsing Issues ⚠️

**Problem:** Date parsing fails with unexpected formats
**Symptom:** ValueError when parsing commit dates
**Root Cause:** Git date formats vary depending on configuration

**Solution:** Use robust date parsing
```python
from datetime import datetime
import dateutil.parser

def parse_git_date(date_str):
    try:
        return dateutil.parser.parse(date_str)
    except ValueError:
        # Fallback to manual parsing
        return datetime.strptime(date_str.split()[0], '%Y-%m-%d')
```

**Test:** Verify that various date formats are handled correctly

---

### Gotcha 4: Bounds Checking for Metrics ⚠️

**Problem:** Metrics fall outside [0,1] range
**Symptom:** Values less than 0 or greater than 1 in metrics
**Root Cause:** Not clamping calculated values to valid range

**Solution:** Ensure all metrics are in [0,1] range
```python
def clamp(value, min_val=0, max_val=1):
    return max(min_val, min(max_val, value))

recency_score = clamp(calculated_recency)
```

**Test:** Verify that all output metrics are between 0 and 1

---

## Integration Checkpoint

**When to move to 002.4 (BranchClusterer):**
- [ ] All 8 subtasks complete
- [ ] Unit tests passing (>90% coverage)
- [ ] Output matches specification
- [ ] No validation errors
- [ ] Commit message: "feat: complete Task 002.1 CommitHistoryAnalyzer"

---

## Notes for Implementer

**Technical Requirements:**
1. Use subprocess with timeout for git commands
2. Implement comprehensive error handling
3. Guarantee all metrics ∈ [0,1] with bounds checking
4. Ensure stateless and thread-safe design
5. Process commits in streaming fashion

**Edge Cases (Must Handle):**
- New branches (single commit, < 1 hour old)
- Stale branches (90+ days old)
- Orphaned branches (no common ancestor)
- Repositories with corrupted git history
- Branches with binary files only

**Performance Targets:**
- Single branch analysis: <2 seconds
- Memory usage: <50MB per analysis
- Handle repositories with 10,000+ commits

---

## Done Definition

Task 002.1 is done when:
1. All 8 subtasks marked complete
2. Unit tests pass (>95% coverage) on CI/CD
3. Code review approved
4. Outputs match specification
5. Documentation complete
6. Performance benchmarks met
7. Ready for hand-off to Task 002.4

## Purpose

Analyze Git commit history for each feature branch to extract metrics like commit frequency, author patterns, merge points, and branch divergence dates.

---

## Details

Implement a Python module that:
- Fetches all remote feature branches
- Extracts commit metadata (hash, date, author, message)
- Calculates divergence metrics from main/scientific/orchestration-tools
- Identifies shared history points and merge bases
- Outputs structured metrics for clustering

---

## Guidance & Standards

- **Architecture:** [Comprehensive Guide](../guidance/COMPREHENSIVE_CLI_ARCHITECTURE_GUIDE.md)
- **Merging:** [Merge Guidance](../guidance/MERGE_GUIDANCE_DOCUMENTATION.md)
- **Patterns:** [Factory Pattern](../guidance/FACTORY_PATTERN_IMPLEMENTATION_GUIDE.md)
- **General:** [Project Guidance](../guidance/README.md)

---

## Success Criteria

- [ ] Module fetches and analyzes all feature branches
- [ ] Generates commit history metrics for each branch
- [ ] Identifies merge bases with all primary targets
- [ ] Outputs structured JSON for downstream processing
- [ ] Unit tests cover all extraction functions

---

## Test Strategy

- Create test repository with known branch structures
- Verify metrics match expected values
- Test with empty branches, single commits, long histories

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
**Effort:** 24-32 hours
**Complexity:** 7/10
**Dependencies:** None
**Created:** 2026-01-12
**Parent:** Task 002: Branch Clustering System

---

## Purpose

Analyze Git commit history for each feature branch to extract metrics like commit frequency, author patterns, merge points, and branch divergence dates.

---

## Details

Implement a Python module that:
- Fetches all remote feature branches
- Extracts commit metadata (hash, date, author, message)
- Calculates divergence metrics from main/scientific/orchestration-tools
- Identifies shared history points and merge bases
- Outputs structured metrics for clustering

---

## Guidance & Standards

- **Architecture:** [Comprehensive Guide](../guidance/COMPREHENSIVE_CLI_ARCHITECTURE_GUIDE.md)
- **Merging:** [Merge Guidance](../guidance/MERGE_GUIDANCE_DOCUMENTATION.md)
- **Patterns:** [Factory Pattern](../guidance/FACTORY_PATTERN_IMPLEMENTATION_GUIDE.md)
- **General:** [Project Guidance](../guidance/README.md)

---

## Success Criteria

- [ ] Module fetches and analyzes all feature branches
- [ ] Generates commit history metrics for each branch
- [ ] Identifies merge bases with all primary targets
- [ ] Outputs structured JSON for downstream processing
- [ ] Unit tests cover all extraction functions

---

## Test Strategy

- Create test repository with known branch structures
- Verify metrics match expected values
- Test with empty branches, single commits, long histories

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

Analyze Git commit history for each feature branch to extract metrics like commit frequency, author patterns, merge points, and branch divergence dates.

---

## Details

Implement a Python module that:
- Fetches all remote feature branches
- Extracts commit metadata (hash, date, author, message)
- Calculates divergence metrics from main/scientific/orchestration-tools
- Identifies shared history points and merge bases
- Outputs structured metrics for clustering

---

## Guidance & Standards

- **Architecture:** [Comprehensive Guide](../guidance/COMPREHENSIVE_CLI_ARCHITECTURE_GUIDE.md)
- **Merging:** [Merge Guidance](../guidance/MERGE_GUIDANCE_DOCUMENTATION.md)
- **Patterns:** [Factory Pattern](../guidance/FACTORY_PATTERN_IMPLEMENTATION_GUIDE.md)
- **General:** [Project Guidance](../guidance/README.md)

---

## Success Criteria

- [ ] Module fetches and analyzes all feature branches
- [ ] Generates commit history metrics for each branch
- [ ] Identifies merge bases with all primary targets
- [ ] Outputs structured JSON for downstream processing
- [ ] Unit tests cover all extraction functions

---

## Test Strategy

- Create test repository with known branch structures
- Verify metrics match expected values
- Test with empty branches, single commits, long histories

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
- Fetches all remote feature branches
- Extracts commit metadata (hash, date, author, message)
- Calculates divergence metrics from main/scientific/orchestration-tools
...

## Success Criteria

- [ ] [Success criteria to be defined]

## Prerequisites & Dependencies

### Required Before Starting
- [ ] None
**Created:** 2026-01-12
**Parent:** Task 002: Branch Clustering System

---

## Purpose

Analyze Git commit history for each feature branch to extract metrics like commit frequency, author patterns, merge points, and branch divergence dates.

---

## Details

Implement a Python module that:
- Fetches all remote feature branches
- Extracts commit metadata (hash, date, author, message)
- Calculates divergence metrics from main/scientific/orchestration-tools
- Identifies shared history points and merge bases
- Outputs structured metrics for clustering

---

## Guidance & Standards

- **Architecture:** [Comprehensive Guide](../guidance/COMPREHENSIVE_CLI_ARCHITECTURE_GUIDE.md)
- **Merging:** [Merge Guidance](../guidance/MERGE_GUIDANCE_DOCUMENTATION.md)
- **Patterns:** [Factory Pattern](../guidance/FACTORY_PATTERN_IMPLEMENTATION_GUIDE.md)
- **General:** [Project Guidance](../guidance/README.md)

---

## Success Criteria

- [ ] Module fetches and analyzes all feature branches
- [ ] Generates commit history metrics for each branch
- [ ] Identifies merge bases with all primary targets
- [ ] Outputs structured JSON for downstream processing
- [ ] Unit tests cover all extraction functions

---

## Test Strategy

- Create test repository with known branch structures
- Verify metrics match expected values
- Test with empty branches, single commits, long histories

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
**Effort:** 24-32 hours
**Complexity:** 7/10
**Dependencies:** None
**Created:** 2026-01-12
**Parent:** Task 002: Branch Clustering System

---

## Purpose

Analyze Git commit history for each feature branch to extract metrics like commit frequency, author patterns, merge points, and branch divergence dates.

---

## Details

Implement a Python module that:
- Fetches all remote feature branches
- Extracts commit metadata (hash, date, author, message)
- Calculates divergence metrics from main/scientific/orchestration-tools
- Identifies shared history points and merge bases
- Outputs structured metrics for clustering

---

## Guidance & Standards

- **Architecture:** [Comprehensive Guide](../guidance/COMPREHENSIVE_CLI_ARCHITECTURE_GUIDE.md)
- **Merging:** [Merge Guidance](../guidance/MERGE_GUIDANCE_DOCUMENTATION.md)
- **Patterns:** [Factory Pattern](../guidance/FACTORY_PATTERN_IMPLEMENTATION_GUIDE.md)
- **General:** [Project Guidance](../guidance/README.md)

---

## Success Criteria

- [ ] Module fetches and analyzes all feature branches
- [ ] Generates commit history metrics for each branch
- [ ] Identifies merge bases with all primary targets
- [ ] Outputs structured JSON for downstream processing
- [ ] Unit tests cover all extraction functions

---

## Test Strategy

- Create test repository with known branch structures
- Verify metrics match expected values
- Test with empty branches, single commits, long histories

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
**Effort:** 24-32 hours
**Complexity:** 7/10
**Dependencies:** None
**Created:** 2026-01-12
**Parent:** Task 002: Branch Clustering System

---

## Purpose

Analyze Git commit history for each feature branch to extract metrics like commit frequency, author patterns, merge points, and branch divergence dates.

---

## Details

Implement a Python module that:
- Fetches all remote feature branches
- Extracts commit metadata (hash, date, author, message)
- Calculates divergence metrics from main/scientific/orchestration-tools
- Identifies shared history points and merge bases
- Outputs structured metrics for clustering

---

## Guidance & Standards

- **Architecture:** [Comprehensive Guide](../guidance/COMPREHENSIVE_CLI_ARCHITECTURE_GUIDE.md)
- **Merging:** [Merge Guidance](../guidance/MERGE_GUIDANCE_DOCUMENTATION.md)
- **Patterns:** [Factory Pattern](../guidance/FACTORY_PATTERN_IMPLEMENTATION_GUIDE.md)
- **General:** [Project Guidance](../guidance/README.md)

---

## Success Criteria

- [ ] Module fetches and analyzes all feature branches
- [ ] Generates commit history metrics for each branch
- [ ] Identifies merge bases with all primary targets
- [ ] Outputs structured JSON for downstream processing
- [ ] Unit tests cover all extraction functions

---

## Test Strategy

- Create test repository with known branch structures
- Verify metrics match expected values
- Test with empty branches, single commits, long histories

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
- Fetches all remote feature branches
- Extracts commit metadata (hash, date, author, message)
- Calculates divergence metrics from main/scientific/orchestration-tools
- Identifies shared history points and merge bases
- Outputs structured metrics for clustering

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
- Create test repository with known branch structures
- Verify metrics match expected values
- Test with empty branches, single commits, long histories

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

- [ ] No next steps specified
- [ ] Additional steps to be defined


<!-- EXTENDED_METADATA
END_EXTENDED_METADATA -->

## Configuration Parameters

- **Owner**: TBD
- **Initiative**: TBD
- **Scope**: TBD
- **Focus**: TBD

---

<!-- IMPORTED_FROM: backup_task75/task-002.1.md -->
Configurable parameters (not hardcoded):

- `COMMIT_RECENCY_WEIGHT` = 0.25
- `COMMIT_FREQUENCY_WEIGHT` = 0.20
- `AUTHORSHIP_DIVERSITY_WEIGHT` = 0.20
- `MERGE_READINESS_WEIGHT` = 0.20
- `STABILITY_SCORE_WEIGHT` = 0.15
- `RECENCY_WINDOW_DAYS` = 30
- `FREQUENCY_BASELINE_COMMITS_PER_WEEK` = 5
- `STABILITY_BASELINE_LINES_PER_COMMIT` = 50
- `MERGE_READINESS_MAX_COMMITS_BEHIND` = 50
- `GIT_COMMAND_TIMEOUT_SECONDS` = 30

---

## Performance Targets

- **Effort Range**: 24-32 hours
- **Complexity Level**: 7/10

## Testing Strategy

### Unit Testing Approach
- **Minimum 8 test cases** covering all 5 metrics individually
- **Edge case testing** for new branches, stale branches, non-existent branches
- **Performance testing** to ensure <2 second execution time
- **Code coverage** >95% across all functions and branches

### Test Cases to Implement

**Test Case 1: Normal Branch Analysis**
- Input: Branch with 42 commits, 3 authors, 18 days active
- Expected: All metrics return values in [0,1], aggregate score calculated correctly
- Validation: Output matches JSON schema exactly

**Test Case 2: New Branch Analysis**
- Input: Branch with 2 commits, 1 author, 1 day old
- Expected: Appropriate scores for new branch (likely high recency, low frequency)
- Validation: No exceptions raised, proper handling of small datasets

**Test Case 3: Stale Branch Analysis**
- Input: Branch with 100+ days since last commit
- Expected: Low recency score, appropriate other metrics
- Validation: Handles old dates gracefully

**Test Case 4: High-Activity Branch Analysis**
- Input: Branch with 200+ commits, 5+ authors
- Expected: High frequency, appropriate diversity metrics
- Validation: Performance remains under 2 seconds

**Test Case 5: Non-existent Branch**
- Input: Branch name that doesn't exist
- Expected: Appropriate error handling without exception
- Validation: Returns error object or raises specific exception

**Test Case 6: Single-Commit Branch**
- Input: Branch with only 1 commit
- Expected: Proper handling of edge case for all metrics
- Validation: No division-by-zero errors, valid output

**Test Case 7: Binary File Branch**
- Input: Branch with binary files
- Expected: Proper handling of non-text files
- Validation: Skips binary files gracefully

**Test Case 8: Large Repository Branch**
- Input: Branch in repository with 10,000+ commits
- Expected: Performance under 2 seconds, no memory issues
- Validation: Proper timeout handling

### Integration Testing
- Test with real repository fixtures
- Verify output compatibility with Task 002.4 (BranchClusterer)
- End-to-end pipeline validation
- Cross-validation with manual analysis

## Common Gotchas & Solutions

### Gotcha 1: Git Command Timeouts ⚠️
**Problem:** Git commands hang on large repositories with 10,000+ commits
**Symptom:** Process hangs for more than 30 seconds during git log
**Root Cause:** Git operations on very large repositories can take a long time
**Solution:** Add timeout to subprocess calls
```python
import subprocess
result = subprocess.run([
    "git", "log", f"{main_branch}..{branch_name}", "--pretty=format:%H|%ai|%an|%s"
], capture_output=True, text=True, timeout=30)  # 30-second timeout
```

### Gotcha 2: Division by Zero ⚠️
**Problem:** Calculations fail when denominators are zero
**Symptom:** ZeroDivisionError during metric calculations
**Root Cause:** Not checking for zero values in denominators
**Solution:** Add checks for zero values
```python
def calculate_frequency(commits, days_active):
    if days_active == 0:
        days_active = 1  # Prevent division by zero
    return len(commits) / days_active
```

### Gotcha 3: Date Parsing Issues ⚠️
**Problem:** Date parsing fails with unexpected formats
**Symptom:** ValueError when parsing commit dates
**Root Cause:** Git date formats vary depending on configuration
**Solution:** Use robust date parsing
```python
from datetime import datetime
import dateutil.parser

def parse_git_date(date_str):
    try:
        return dateutil.parser.parse(date_str)
    except ValueError:
        # Fallback to manual parsing
        return datetime.strptime(date_str.split()[0], '%Y-%m-%d')
```

### Gotcha 4: Bounds Checking for Metrics ⚠️
**Problem:** Metrics fall outside [0,1] range
**Symptom:** Values less than 0 or greater than 1 in metrics
**Root Cause:** Not clamping calculated values to valid range
**Solution:** Ensure all metrics are in [0,1] range
```python
def clamp(value, min_val=0, max_val=1):
    return max(min_val, min(max_val, value))

recency_score = clamp(calculated_recency)
```

### Gotcha 5: Non-existent Branches ⚠️
**Problem:** Git commands fail when branch doesn't exist
**Symptom:** Git error when trying to analyze non-existent branch
**Root Cause:** Branch validation not performed before git operations
**Solution:** Check branch existence before processing
```python
def branch_exists(repo_path, branch_name):
    import subprocess
    result = subprocess.run([
        "git", "show-ref", "--verify", f"refs/heads/{branch_name}"
    ], cwd=repo_path, capture_output=True)
    return result.returncode == 0
```

## Integration Checkpoint

### Criteria for Moving Forward
- [ ] All success criteria met
- [ ] Code reviewed and approved
- [ ] Tests passing
- [ ] Documentation updated
- [ ] No critical or high severity issues

---

<!-- IMPORTED_FROM: backup_task75/task-002.1.md -->
**When to move to 002.4 (BranchClusterer):**
- [ ] All 8 subtasks complete
- [ ] Unit tests passing (>90% coverage)
- [ ] Output matches specification
- [ ] No validation errors
- [ ] Commit message: "feat: complete Task 002.1 CommitHistoryAnalyzer"

---

## Done Definition

### Completion Criteria
- [ ] All success criteria met
- [ ] Code reviewed and approved
- [ ] Tests passing
- [ ] Documentation updated

---

<!-- IMPORTED_FROM: backup_task75/task-002.1.md -->
Task 002.1 is done when:
1. All 8 subtasks marked complete
2. Unit tests pass (>95% coverage) on CI/CD
3. Code review approved
4. Outputs match specification
5. Documentation complete
6. Performance benchmarks met
7. Ready for hand-off to Task 002.4

## Next Steps

1. **Implementation Phase**: Begin with Phase 1 implementation focusing on class structure and architecture
2. **Unit Testing**: Develop comprehensive test suite with 8+ test cases covering all metrics
3. **Integration Testing**: Verify output compatibility with Task 002.4 (BranchClusterer) input requirements
4. **Performance Validation**: Confirm analysis completes in under 2 seconds per branch
5. **Code Review**: Submit for peer review ensuring PEP 8 compliance and comprehensive documentation
6. **Handoff Preparation**: Prepare for integration with Task 002.4 once implementation is complete
7. **Documentation**: Complete any remaining documentation gaps identified during implementation
