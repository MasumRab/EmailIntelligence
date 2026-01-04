# Task 75.1: CommitHistoryAnalyzer

## Purpose
Create a reusable Python class that extracts and scores commit history metrics for branches. This analyzer is one of three Stage One components that will be integrated into the clustering pipeline.

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
- [ ] Compatible with Task 75.4 (BranchClusterer) input requirements
- [ ] Compatible with Task 75.6 (PipelineIntegration) consumption patterns
- [ ] Configuration externalized and validated
- [ ] Documentation complete and accurate

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

**Blocks:** 75.1.3, 75.1.4, 75.1.5

---

### 75.1.3: Implement Commit Recency Metric
**Purpose:** Score how recent the branch's commits are  
**Effort:** 3-4 hours  
**Depends on:** 75.1.1, 75.1.2

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

### 75.1.4: Implement Commit Frequency Metric
**Purpose:** Score how active the branch is (velocity)  
**Effort:** 3-4 hours  
**Depends on:** 75.1.1, 75.1.2

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

### 75.1.5: Implement Authorship & Stability Metrics
**Purpose:** Score author diversity and code stability  
**Effort:** 4-5 hours  
**Depends on:** 75.1.1, 75.1.2

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

### 75.1.6: Implement Merge Readiness Metric
**Purpose:** Score how synchronized branch is with main  
**Effort:** 3-4 hours  
**Depends on:** 75.1.1, 75.1.2

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

### 75.1.7: Aggregate Metrics & Output Formatting
**Purpose:** Combine 5 metrics into single score and format output  
**Effort:** 2-3 hours  
**Depends on:** 75.1.3, 75.1.4, 75.1.5, 75.1.6

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

## Integration Checkpoint

**When to move to 75.4 (BranchClusterer):**
- [ ] All 8 subtasks complete
- [ ] Unit tests passing (>90% coverage)
- [ ] Output matches specification
- [ ] No validation errors
- [ ] Commit message: "feat: complete Task 75.1 CommitHistoryAnalyzer"

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

Task 75.1 is done when:
1. All 8 subtasks marked complete
2. Unit tests pass (>95% coverage) on CI/CD
3. Code review approved
4. Outputs match specification
5. Documentation complete
6. Performance benchmarks met
7. Ready for hand-off to Task 75.4
