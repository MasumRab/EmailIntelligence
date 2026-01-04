# Integration Example: task-75.1.md with HANDOFF Content

This file shows **BEFORE** and **AFTER** for Task 75.1, demonstrating how to integrate HANDOFF content into task files.

---

## BEFORE (Current Separation)

### task-75.1.md excerpt (only purpose and first subtask shown)

```markdown
# Task 75.1: CommitHistoryAnalyzer

## Purpose
Create a reusable Python class that extracts and scores commit history metrics for branches. 
This analyzer is one of three Stage One components that will be integrated into the clustering pipeline.

**Scope:** CommitHistoryAnalyzer class only  
**Effort:** 24-32 hours | **Complexity:** 7/10  
**Status:** Ready for implementation  
**No dependencies** - can start immediately

---

## Success Criteria

Task 75.1 is complete when:

**Core Functionality:**
- [ ] `CommitHistoryAnalyzer` class accepts `repo_path` (str) and `branch_name` (str) parameters
- [ ] Successfully extracts commit data using git log commands with proper parsing
[... more criteria ...]

---

## Subtasks

### 75.1.1: Design Metric System
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

**Blocks:** 75.1.2, 75.1.3, 75.1.4, 75.1.5
```

### HANDOFF_75.1_CommitHistoryAnalyzer.md excerpt

```markdown
# Task 75.1: CommitHistoryAnalyzer Implementation

## Quick Summary
Implement the `CommitHistoryAnalyzer` class that extracts and scores commit history metrics 
for Git branches. This is a Stage One analyzer—no dependencies on other tasks in this batch.

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
```

**Problem:** Developer must read both files to get complete picture.

---

## AFTER (Integrated)

### task-75.1.md (enriched version)

```markdown
# Task 75.1: CommitHistoryAnalyzer

## Purpose
Create a reusable Python class that extracts and scores commit history metrics for branches. 
This analyzer is one of three Stage One components that will be integrated into the clustering pipeline.

**Scope:** CommitHistoryAnalyzer class only  
**Effort:** 24-32 hours | **Complexity:** 7/10  
**Status:** Ready for implementation  
**No dependencies** - can start immediately

---

## Developer Quick Reference

**Build:** A Python class `CommitHistoryAnalyzer` that:
1. Extracts commit data for a target branch relative to main/master
2. Computes 5 normalized metrics (0-1 scale)
3. Returns aggregated score weighted by metric importance

### Class Signature
```python
class CommitHistoryAnalyzer:
    def __init__(self, repo_path: str, main_branch: str = "main")
    def analyze(self, branch_name: str) -> dict
```

**See:** HANDOFF_75.1_CommitHistoryAnalyzer.md for full implementation guide and commands

---

## Success Criteria

Task 75.1 is complete when:

**Core Functionality:**
- [ ] `CommitHistoryAnalyzer` class accepts `repo_path` (str) and `branch_name` (str) parameters
- [ ] Successfully extracts commit data using git log commands with proper parsing
[... more criteria ...]

---

## Subtasks

### 75.1.1: Design Metric System
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

### Implementation Checklist (From HANDOFF)
- [ ] Initialize with repo validation (check if `.git` exists)
- [ ] Define metrics table with formulas (see Metrics to Compute below)
- [ ] Create weighting formula: 0.25 * m1 + 0.20 * m2 + 0.20 * m3 + 0.20 * m4 + 0.15 * m5
- [ ] Plan normalization strategy for each metric to [0, 1] range
- [ ] Document sensible defaults for edge cases

### Metrics to Compute (From HANDOFF)

| Metric | Weight | Description |
|--------|--------|-------------|
| `commit_recency` | 25% | Recent commits weighted higher (exponential decay, 30-day window) |
| `commit_frequency` | 20% | Activity velocity (commits/day over branch lifetime) |
| `authorship_diversity` | 20% | Unique authors count (normalized by total commits) |
| `merge_readiness` | 20% | Commits since last merge to main (closer = higher) |
| `stability_score` | 15% | Inverse of commit churn (% lines changed per commit) |

All metrics normalized to `[0, 1]`.

**Blocks:** 75.1.2, 75.1.3, 75.1.4, 75.1.5

---

### 75.1.2: Set Up Git Data Extraction
**Purpose:** Create functions to extract commit data from git repository  
**Effort:** 4-5 hours  
**Depends on:** 75.1.1

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

### Implementation Checklist (From HANDOFF)
- [ ] Use subprocess with timeout for git commands
- [ ] Git command for commits: `git log main..BRANCH_NAME --pretty=format:"%H|%ai|%an|%s"`
- [ ] Git command for stats: `git log main..BRANCH_NAME --pretty=format:"%H" | xargs -I {} git diff main...{} --stat`
- [ ] Git command for merge base: `git merge-base main BRANCH_NAME`
- [ ] Handle non-existent branches gracefully (raise BranchNotFoundError)
- [ ] Parse output into structured format (list of dicts with keys: hash, timestamp, author, message)
- [ ] Implement retry logic for transient git errors

---

[... more subtasks ...]

### 75.1.8: Write Unit Tests
**Purpose:** Verify CommitHistoryAnalyzer works correctly  
**Effort:** 3-4 hours  
**Depends on:** 75.1.7

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

### Test Case Examples (From HANDOFF)

Implement these specific test cases:

1. **test_normal_branch**
   - Input: Branch with 42 commits, 3 authors, 18 days active
   - Expected: All metrics in [0, 1], aggregate_score in [0, 1]
   - Validates: Normal operation, aggregation formula correct

2. **test_new_branch**
   - Input: Brand new branch, 2 commits, 1 author, 1 day old
   - Expected: commit_frequency lower, recency high, all metrics defined
   - Validates: Handling of new branches

3. **test_stale_branch**
   - Input: Old branch, 100+ days old, no recent commits
   - Expected: commit_recency low, but other metrics calculated
   - Validates: Handling of stale branches

4. **test_high_activity_branch**
   - Input: 200+ commits, 5+ authors
   - Expected: authorship_diversity appropriate, all metrics in [0, 1]
   - Validates: Handling of high-activity branches

5. **test_nonexistent_branch**
   - Input: Branch name that doesn't exist
   - Expected: Raises `BranchNotFoundError`
   - Validates: Error handling

6. **test_single_commit_branch**
   - Input: Branch with single commit
   - Expected: All metrics defined (no division by zero)
   - Validates: Edge case handling

7. **test_binary_only_branch**
   - Input: Branch with only binary file commits
   - Expected: Metrics calculated (stability_score may differ)
   - Validates: Handling of non-code files

8. **test_performance**
   - Input: Large repository (10,000+ commits), measure execution time
   - Expected: Analysis completes in <2 seconds
   - Validates: Performance target met

---

## Configuration Parameters

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

## Technical Reference (From HANDOFF)

### Git Commands Reference

```bash
# Get commits unique to branch (not in main)
git log main..BRANCH_NAME --pretty=format:"%H|%ai|%an|%s"

# Parse output format: hash|timestamp|author|message
# Example: abc123|2025-01-04 10:30:00 +0000|John Doe|feat: add feature

# Get commit diff stats (for stability_score)
git log main..BRANCH_NAME --pretty=format:"%H" | \
  xargs -I {} git diff main...{} --stat

# Get merge base (for merge_readiness)
git merge-base main BRANCH_NAME

# Get commit date
git log -1 --format=%ai BRANCH_NAME

# Count unique authors
git log main..BRANCH_NAME --pretty=format:"%an" | sort | uniq | wc -l
```

### Dependencies
- **GitPython** or subprocess calls to git CLI (preferred: subprocess for reliability)
- No internal dependencies on other Task 75.x components
- Output feeds into **Task 75.4 (BranchClusterer)**

### Parallel Tasks Ready to Start
- **Task 75.2** (CodebaseStructureAnalyzer) - no dependencies
- **Task 75.3** (DiffDistanceCalculator) - no dependencies

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

## Integration Checkpoint

**When to move to 75.4 (BranchClusterer):**
- [ ] All 8 subtasks complete
- [ ] Unit tests passing (>90% coverage)
- [ ] Output matches specification
- [ ] No validation errors
- [ ] Commit message: "feat: complete Task 75.1 CommitHistoryAnalyzer"

---

## Done Definition

Task 75.1 is done when:
1. All 8 subtasks marked complete
2. Unit tests pass (>95% coverage) on CI/CD
3. Code review approved
4. Outputs match specification
5. Documentation complete
6. Performance benchmarks met
7. Ready for hand-off to Task 75.4
```

---

## Key Changes Made

| Section | Before | After | Benefit |
|---------|--------|-------|---------|
| Quick Start | None | Developer Quick Reference added | Immediate context |
| Class Signature | Only in HANDOFF | Now in task file | No context switching |
| Metrics Table | Only in HANDOFF | Added to 75.1.1 subtask | Visible where needed |
| Git Commands | Only in HANDOFF | Added to Technical Reference | Developers can copy-paste |
| Implementation Steps | General "Steps" only | Specific checklist per subtask | Actionable guidance |
| Test Cases | Only in HANDOFF | 8 concrete examples in task | Clear expectations |
| Edge Cases | Notes section only | In Technical Reference | Comprehensive coverage |
| Dependencies | Implied | Explicit at end | Clear parallel work |

---

## Lines of Code Impact

- **Before:** task-75.1.md (280 lines) + HANDOFF_75.1.md (139 lines) = 419 lines total
- **After:** task-75.1.md (420 lines, integrated) + optional HANDOFF reference
- **Result:** Single authoritative source, +140 lines of practical guidance embedded

---

## Developer Experience

### Before (Current)
1. Developer opens task-75.1.md
2. Reads purpose and success criteria
3. "What class signature?" → Opens HANDOFF file
4. "What git commands?" → Searches HANDOFF file
5. "What test cases?" → Back to HANDOFF file
6. Constantly switching between files

### After (Integrated)
1. Developer opens task-75.1.md
2. Reads Developer Quick Reference → Understands what to build
3. Reads subtasks with embedded Implementation Checklist → Knows steps
4. Reads Testing subtask with Test Case Examples → Knows what to test
5. References Technical Reference for commands → Finds git commands
6. All in one file, no switching needed
7. Can still reference HANDOFF for additional details if needed

---

## Recommendation

**Integrate all 9 task files using this pattern.** The integrated task files become the authoritative source while HANDOFF files remain available as quick-reference guides for developers who prefer concise documents.

This provides:
- ✓ Complete context in one place
- ✓ Practical guidance embedded at the right spots
- ✓ No loss of detail or rigor
- ✓ Better developer experience
- ✓ Easier to track progress
- ✓ Single source of truth per task
