# Task 075.1: CommitHistoryAnalyzer

**Status:** Ready for Implementation  
**Priority:** High  
**Effort:** 24-32 hours  
**Complexity:** 7/10  
**Dependencies:** None - can start immediately  
**Blocks:** Task 075.4 (BranchClusterer)

---

## Purpose

Create a reusable Python class that extracts and scores commit history metrics for branches. This analyzer is one of three Stage One components that will be integrated into the clustering pipeline.

**Scope:** CommitHistoryAnalyzer class only  
**No dependencies** - can start immediately  
**Parallelizable with:** Task 075.2 and Task 075.3

---

## Success Criteria

Task 075.1 is complete when:

### Core Functionality
- [ ] `CommitHistoryAnalyzer` class accepts `repo_path` (str) and `main_branch` (str) parameters
- [ ] Successfully extracts commit data using git log commands with proper parsing
- [ ] Computes exactly 5 normalized metrics in [0,1] range with specified formulas:
  - [ ] `commit_recency` - How recent are the latest commits
  - [ ] `commit_frequency` - Commit rate relative to branch age
  - [ ] `authorship_diversity` - Number of unique contributors
  - [ ] `merge_readiness` - Commits behind main branch (inverse normalized)
  - [ ] `stability_score` - Consistency of commit patterns
- [ ] Returns properly formatted dict with all required fields and aggregate score
- [ ] Handles all specified edge cases gracefully:
  - [ ] Non-existent branches (returns error without crashing)
  - [ ] New branches (single commit, < 1 hour old)
  - [ ] Stale branches (90+ days old)
  - [ ] Orphaned branches (no common ancestor with main)
  - [ ] Repositories with corrupted git history
- [ ] Output matches JSON schema exactly (all required fields present)

### Quality Assurance
- [ ] Unit tests pass (minimum 8 test cases with >95% code coverage)
- [ ] No exceptions raised for valid inputs (comprehensive error handling)
- [ ] Performance: <2 seconds per branch analysis on standard hardware
- [ ] Code quality: Passes linting, follows PEP 8, includes comprehensive docstrings
- [ ] Stateless and thread-safe design
- [ ] Memory usage <50 MB per analysis

### Integration Readiness
- [ ] Compatible with Task 075.4 (BranchClusterer) input requirements
- [ ] Compatible with Task 075.6 (PipelineIntegration) consumption patterns
- [ ] Configuration externalized and validated (not hardcoded)
- [ ] Documentation complete and accurate
- [ ] All metrics verified to be in [0,1] range with bounds checking

---

## Prerequisites & Dependencies

### Required Before Starting
- [ ] Git installed and accessible via subprocess
- [ ] Python 3.8+ with subprocess module
- [ ] Test infrastructure in place
- [ ] Project structure created (src/analyzers/, tests/analyzers/)

### Blocks (What This Task Unblocks)
- Task 075.4 (BranchClusterer) - requires output from this task
- Task 075.6 (PipelineIntegration) - may use outputs

### External Dependencies
- Python subprocess (built-in)
- GitPython (optional, or use subprocess.run)
- Standard library: datetime, json, typing

### No Dependency On
- Task 075.2 (CodebaseStructureAnalyzer) - can start in parallel
- Task 075.3 (DiffDistanceCalculator) - can start in parallel

---

## Sub-subtasks

### 075.1.1: Design Metric System
**Effort:** 2-3 hours  
**Depends on:** None

**Steps:**
1. Define the 5 core metrics with mathematical formulas
2. Document calculation approach for each metric
3. Create normalization strategy (ensure all metrics in [0,1] range)
4. Create weighting scheme: 0.25/0.20/0.20/0.20/0.15 (sum = 1.0)
5. Document edge case handling for each metric

**Success Criteria:**
- [ ] All 5 metrics clearly defined with formulas
- [ ] Calculation approach specified for each
- [ ] Normalization approach specified (how to ensure [0,1])
- [ ] Weights documented and sum to 1.0
- [ ] Edge case handling documented for each metric

---

### 075.1.2: Set Up Git Data Extraction
**Effort:** 4-5 hours  
**Depends on:** 075.1.1

**Steps:**
1. Create subprocess-based git command execution utility
2. Implement branch validation (check if branch exists before processing)
3. Create commit log extraction function (get all commits on branch)
4. Create commit metadata extraction (dates, authors, messages)
5. Add error handling (invalid branch, repo not found, git errors)

**Success Criteria:**
- [ ] Can execute git commands without errors
- [ ] Validates branch existence before processing
- [ ] Extracts commit list with metadata (date, author, message)
- [ ] Handles non-existent branches gracefully (no crash)
- [ ] Returns structured data (list of dicts with commit info)

---

### 075.1.3: Implement Commit Recency Metric
**Effort:** 3-4 hours  
**Depends on:** 075.1.1, 075.1.2

**Steps:**
1. Extract most recent commit date from branch
2. Calculate time since last commit (days)
3. Implement exponential decay function
4. Define time window (e.g., 30 days)
5. Normalize to [0,1] range
6. Test with recent, old, and edge-case branches

**Success Criteria:**
- [ ] Returns value in [0, 1] range
- [ ] Recent commits (last 7 days) score > 0.8
- [ ] Old commits (90+ days) score < 0.3
- [ ] Correctly handles single-commit branches
- [ ] Consistent calculation across test cases
- [ ] Handles future-dated commits gracefully

---

### 075.1.4: Implement Commit Frequency Metric
**Effort:** 3-4 hours  
**Depends on:** 075.1.1, 075.1.2

**Steps:**
1. Count total commits on branch
2. Calculate branch lifetime (days from first to last commit)
3. Compute velocity (commits per day)
4. Define frequency baseline and scoring
5. Normalize to [0,1] range
6. Test with high-activity and low-activity branches

**Success Criteria:**
- [ ] Returns value in [0, 1] range
- [ ] High activity (>5 commits/week) scores > 0.7
- [ ] Low activity (<1 commit/week) scores < 0.4
- [ ] Correctly handles single-commit branches (avoids division by zero)
- [ ] Handles very old branches (>100 days) without overflow

---

### 075.1.5: Implement Authorship & Stability Metrics
**Effort:** 4-5 hours  
**Depends on:** 075.1.1, 075.1.2

**Steps for authorship_diversity:**
1. Extract unique author names from commits
2. Count total commits vs unique authors
3. Calculate diversity ratio (unique / total)
4. Normalize to [0,1] range

**Steps for stability_score:**
1. Extract line change statistics per commit (additions + deletions)
2. Calculate average churn per commit (lines changed / lines in file)
3. Define stability baseline (inverse of churn)
4. Normalize to [0,1] range

**Success Criteria:**
- [ ] Authorship: Returns value in [0, 1] range
- [ ] Authorship: Single author scores ~0.3, multiple authors score higher
- [ ] Stability: Returns value in [0, 1] range
- [ ] Stability: Low churn scores > 0.7, high churn scores < 0.4
- [ ] Handles edge cases (binary files, deletions, large commits)

---

### 075.1.6: Implement Merge Readiness Metric
**Effort:** 3-4 hours  
**Depends on:** 075.1.1, 075.1.2

**Steps:**
1. Find merge base between branch and main
2. Count commits since merge base on both branches
3. Calculate how far behind main the branch is
4. Define readiness formula (closer to main = higher score)
5. Normalize to [0,1] range
6. Test with various sync states

**Success Criteria:**
- [ ] Returns value in [0, 1] range
- [ ] Recently synced (<5 commits behind) scores > 0.85
- [ ] Far behind (>50 commits behind) scores < 0.4
- [ ] Correctly handles branches merged from main
- [ ] Handles newly-created branches
- [ ] Handles orphaned branches (no common ancestor)

---

### 075.1.7: Implement Aggregation & Weighting
**Effort:** 2-3 hours  
**Depends on:** 075.1.3, 075.1.4, 075.1.5, 075.1.6

**Steps:**
1. Define metric weights: 0.25/0.20/0.20/0.20/0.15 (sum = 1.0)
2. Create weighted aggregation function
3. Verify all metrics in [0,1] before aggregating
4. Format output dict with all required fields
5. Add ISO timestamp (e.g., "2025-12-22T10:30:00Z")

**Success Criteria:**
- [ ] Aggregate score = 0.25×m1 + 0.20×m2 + 0.20×m3 + 0.20×m4 + 0.15×m5
- [ ] Returns value in [0, 1] range
- [ ] Output dict has all required fields (branch_name, metrics, aggregate_score, counts, timestamp)
- [ ] Timestamp in ISO format
- [ ] No missing or extra fields
- [ ] Output can be serialized to JSON without errors

---

### 075.1.8: Unit Testing & Edge Cases
**Effort:** 3-4 hours  
**Depends on:** 075.1.7

**Steps:**
1. Create test fixtures with various branch characteristics
2. Implement minimum 8 unit test cases
3. Mock git commands for reliable testing (no actual git dependency)
4. Add performance benchmarks
5. Generate coverage report (target: >95%)

**Success Criteria:**
- [ ] Minimum 8 comprehensive test cases implemented
- [ ] All tests pass on CI/CD
- [ ] Code coverage >95%
- [ ] Edge cases (new branches, stale branches, orphaned) covered
- [ ] Performance benchmarks recorded and acceptable

---

## Specification

### Class Interface

```python
class CommitHistoryAnalyzer:
    def __init__(self, repo_path: str, main_branch: str = "main"):
        """Initialize analyzer with repository path and main branch name."""
        
    def analyze(self, branch_name: str) -> dict:
        """Analyze commit history for a branch.
        
        Args:
            branch_name: Name of branch to analyze
            
        Returns:
            dict with structure:
            {
                "branch_name": "feature/auth",
                "metrics": {
                    "commit_recency": 0.85,
                    "commit_frequency": 0.72,
                    "authorship_diversity": 0.45,
                    "merge_readiness": 0.92,
                    "stability_score": 0.78
                },
                "aggregate_score": 0.74,
                "counts": {
                    "total_commits": 42,
                    "unique_authors": 3,
                    "days_since_last_commit": 5,
                    "commits_behind_main": 3
                },
                "timestamp": "2025-12-22T10:30:00Z"
            }
        """
```

### Output JSON Schema

All metrics in [0,1] range, aggregate score is weighted sum.

---

## Performance Targets

### Per Component
- Single branch analysis: <2 seconds
- Memory usage: <50 MB per analysis
- Handle repositories with 10,000+ commits

### Scalability
- 13 branches total: <26 seconds
- 50 branches: <100 seconds

### Quality Metrics
- No timeouts on standard hardware
- Consistent performance across repo sizes
- All metrics computed without memory overflow

---

## Testing Strategy

### Unit Tests

Minimum 8 test cases:

```python
def test_commit_recency_recent_commits():
    """Commits from last 7 days should score > 0.8"""
    
def test_commit_recency_old_commits():
    """Commits from 90+ days ago should score < 0.3"""
    
def test_commit_recency_single_commit():
    """Single-commit branches should be handled"""
    
def test_commit_frequency_high_activity():
    """High activity (>5 commits/week) should score > 0.7"""
    
def test_merge_readiness_recently_synced():
    """< 5 commits behind main: score > 0.85"""
    
def test_merge_readiness_far_behind():
    """> 50 commits behind: score < 0.4"""
    
def test_merge_readiness_orphaned_branch():
    """Branch with no common ancestor: handled gracefully"""
    
def test_output_schema_validation():
    """Output matches JSON schema with all required fields"""
```

### Coverage Target
- Code coverage: >95%
- All edge cases covered
- All error paths tested

---

## Common Gotchas & Solutions

**Gotcha 1: Metrics outside [0,1] range**
```python
# WRONG
recency = math.exp(-days / 30)  # Can be slightly > 1.0

# RIGHT
recency = min(1.0, math.exp(-days / 30))
assert 0 <= recency <= 1, f"Metric out of range: {recency}"
```

**Gotcha 2: Division by zero**
```python
# WRONG
frequency = commits / days_active  # Crashes if days_active = 0

# RIGHT
days_active = max(1, days_active)  # Minimum 1 day
frequency = commits / days_active
```

**Gotcha 3: Git timeout on large repos**
```python
# WRONG
result = subprocess.run(cmd, ...)  # No timeout, hangs on huge repos

# RIGHT
result = subprocess.run(cmd, timeout=30, ...)  # Always add timeout
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

# After completing sub-subtask 075.1.3
memory.add_work_log(
    action="Completed Task 075.1.3: Commit Recency Metric",
    details="Exponential decay function implemented, bounds checking added, test coverage 100%"
)
memory.update_todo("task_075_1_3", "completed")
memory.save_session()
```

**What this does:** Maintains session state across work sessions, enables agent handoffs, documents progress.  
**Required?** No - git commits are sufficient.  
**See:** MEMORY_API_FOR_TASKS.md for full usage patterns and examples.

### Output Validation

After completing sub-subtask 075.1.8 (Unit Testing), optionally validate output format:

```bash
python scripts/compare_task_files.py \
  --validate src/analyzers/commit_history.py \
  --schema specification.json
```

**What this does:** Checks your analyzer output JSON matches the schema in the Specification section above.  
**Expected output:** `✓ Valid schema` (means you're ready to move to Task 075.4)  
**Required?** No - manual verification against Specification section is sufficient.  
**See:** SCRIPTS_IN_TASK_WORKFLOW.md § compare_task_files.py for troubleshooting.

---

## Tools Reference

| Tool | Purpose | When to Use | Required? |
|------|---------|-----------|----------|
| Memory API | Progress logging | After each sub-subtask | No |
| compare_task_files.py | Output validation | After 075.1.8 | No |
| next_task.py | Find next task | After completion | No |

**For detailed usage and troubleshooting:** See SCRIPTS_IN_TASK_WORKFLOW.md (all optional tools documented there)

---

## Done Definition

Task 075.1 is done when:

1. ✅ All 8 sub-subtasks marked complete
2. ✅ Unit tests pass (>95% coverage) on CI/CD
3. ✅ Code review approved
4. ✅ Outputs match specification exactly
5. ✅ Output schema validation passes
6. ✅ Documentation complete and accurate
7. ✅ Performance benchmarks met (<2 seconds per branch)
8. ✅ Edge cases handled gracefully
9. ✅ Ready for hand-off to Task 075.4
10. ✅ Commit: "feat: complete Task 075.1 CommitHistoryAnalyzer"
11. ✅ All success criteria checkboxes marked complete

---

## Next Steps

1. **Immediate:** Implement sub-subtask 075.1.1 (Design Metric System)
2. **Week 1:** Complete all 8 sub-subtasks
3. **Week 1-2:** Write and test unit tests (target: >95% coverage)
4. **Week 2:** Code review and refinement
5. **Week 2:** Ready for Task 075.4 (BranchClusterer)

---

**Last Updated:** January 6, 2026  
**Consolidated from:** Task 75.1 (task-75.1.md) with 61 original success criteria preserved  
**Structure:** TASK_STRUCTURE_STANDARD.md (Phase 2 Shallow Retrofit)
