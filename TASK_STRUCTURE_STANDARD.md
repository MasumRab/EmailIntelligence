# Task Structure Standard (Project-Wide)

**Status:** APPROVED  
**Effective:** January 6, 2026  
**Applies to:** All tasks (002+, retrofitted tasks)

---

## Purpose

Establish a consistent, predictable structure for all task files to ensure:
- ✅ No information is lost during consolidation
- ✅ All success criteria preserved and complete
- ✅ Every team member knows where to find everything
- ✅ Easy to hand off and verify completeness
- ✅ Scalable across all project tasks

---

## Standard File Structure

### One File Per Subtask

Each subtask gets its own complete file with everything needed.

**Naming:** `task_XXX.Y.md`
- Example: `task_002.1.md`, `task_002.2.md`, `task_007.3.md`

**File contains:** Specification + Implementation in one place, clearly separated by sections

---

## Required Sections (In Order)

### 1. Task Header
```markdown
# Task 002.1: CommitHistoryAnalyzer

**Status:** [Ready for Implementation | In Progress | Complete | Deferred | Blocked]
**Priority:** [High | Medium | Low]
**Effort:** 24-32 hours
**Complexity:** 7/10
**Dependencies:** [None | List task IDs]
```

---

### 2. Overview/Purpose
Brief explanation of what this subtask accomplishes and why it matters.

```markdown
## Purpose

Create a reusable Python class that extracts and scores commit history metrics 
for branches. This analyzer is one of three Stage One components that will be 
integrated into the clustering pipeline.

**Scope:** CommitHistoryAnalyzer class only  
**No dependencies** - can start immediately
```

---

### 3. Success Criteria (DETAILED)

**All original success criteria preserved here** - this is critical.

Organized by category:

```markdown
## Success Criteria

Task 002.1 is complete when:

### Core Functionality
- [ ] `CommitHistoryAnalyzer` class accepts `repo_path` (str) and `branch_name` (str)
- [ ] Successfully extracts commit data using git log commands
- [ ] Computes exactly 5 normalized metrics in [0,1] range
- [ ] Returns properly formatted dict with all required fields
- [ ] Handles all edge cases (non-existent, new, stale, orphaned branches)
- [ ] Output matches JSON schema exactly

### Quality Assurance
- [ ] Unit tests pass (minimum 8 test cases with >95% coverage)
- [ ] No exceptions raised for valid inputs
- [ ] Performance: <2 seconds per branch analysis
- [ ] Code quality: PEP 8 compliant, comprehensive docstrings

### Integration Readiness
- [ ] Compatible with Task XXX downstream requirements
- [ ] Configuration externalized and validated
- [ ] Documentation complete and accurate
```

---

### 4. Prerequisites & Dependencies

Clear statement of what must be done before this task starts.

```markdown
## Prerequisites & Dependencies

### Required Before Starting
- [ ] Task 002.0 (project setup) complete
- [ ] Development environment configured
- [ ] Test infrastructure in place

### Blocks (What This Task Unblocks)
- Task 002.4 (BranchClusterer)
- Task 002.6 (PipelineIntegration)

### External Dependencies
- Python 3.8+
- GitPython or subprocess for git commands
- scipy for numerical operations
```

---

### 5. Sub-subtasks Breakdown

Detailed breakdown with effort and dependencies.

```markdown
## Sub-subtasks

### 002.1.1: Design Metric System
**Effort:** 2-3 hours  
**Depends on:** None

**Steps:**
1. Define the 5 core metrics with mathematical formulas
2. Document calculation approach
3. Create normalization strategy (ensure [0,1] range)
4. Create weighting scheme: 0.25/0.20/0.20/0.20/0.15 (sum = 1.0)
5. Document edge case handling

**Success Criteria:**
- [ ] All 5 metrics clearly defined with formulas
- [ ] Calculation approach specified
- [ ] Normalization approach specified
- [ ] Weights documented (sum to 1.0)
- [ ] Edge case handling documented

---

### 002.1.2: Set Up Git Data Extraction
**Effort:** 4-5 hours  
**Depends on:** 002.1.1

**Steps:**
1. Create subprocess-based git command execution
2. Implement branch validation (check if branch exists)
3. Extract commit log with metadata (dates, authors, messages)
4. Add error handling for invalid branches

**Success Criteria:**
- [ ] Can execute git commands without errors
- [ ] Validates branch existence before processing
- [ ] Extracts commit list with metadata
- [ ] Handles non-existent branches gracefully
- [ ] Returns structured data (list of dicts)

---

[Continue through 002.1.8...]
```

---

### 6. Specification Details

What to build (in detail).

```markdown
## Specification

### Class Interface

```python
class CommitHistoryAnalyzer:
    def __init__(self, repo_path: str, main_branch: str = "main")
    def analyze(self, branch_name: str) -> dict
```

### Output Format

```json
{
  "branch_name": "feature/auth",
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

### Metrics Definitions

| Metric | Formula | Notes |
|--------|---------|-------|
| commit_recency | exponential_decay(days_since_last) | 30-day window |
| commit_frequency | commits / branch_lifetime_days | Handle div-by-zero |
| authorship_diversity | unique_authors / total_commits | Ratio metric |
| merge_readiness | 1 - (commits_behind_main / max_behind) | Inverse normalized |
| stability_score | 1 - (avg_churn / baseline_churn) | Inverse churn |
```

---

### 7. Implementation Guide

Step-by-step how-to for each sub-subtask.

```markdown
## Implementation Guide

### 002.1.3: Implement Commit Recency Metric

**Objective:** Score how recent the branch's commits are

**Detailed Steps:**

1. Extract commit dates from branch
   ```python
   def get_commit_dates(self, branch_name: str) -> List[datetime]:
       cmd = f"git log {branch_name} --format=%ai"
       # Parse ISO dates
   ```

2. Calculate time since last commit
   ```python
   last_commit_date = max(dates)
   days_since_last = (now - last_commit_date).days
   ```

3. Implement exponential decay function
   ```python
   def exponential_decay(days: float, window: int = 30) -> float:
       return math.exp(-days / window)
   ```

4. Normalize to [0,1] range
   ```python
   # Already in [0,1] from exp() but cap at 1.0
   score = min(1.0, exponential_decay(days))
   ```

5. Test with recent, old, and edge-case branches

**Testing:**
- Recent commits (< 7 days) should score > 0.8
- Old commits (90+ days) should score < 0.3
- Single-commit branches should be handled

**Performance:**
- Must complete in < 0.1 seconds
- Memory: < 5 MB per call
```

---

### 8. Configuration Parameters

All externalized, non-hardcoded parameters.

```markdown
## Configuration

Create `config/task_002_clustering.yaml`:

```yaml
commit_history:
  recency_window_days: 30
  frequency_baseline_commits_per_week: 5
  stability_baseline_lines_per_commit: 50
  merge_readiness_max_commits_behind: 50
  git_command_timeout_seconds: 30
  
  weights:
    commit_recency: 0.25
    commit_frequency: 0.20
    authorship_diversity: 0.20
    merge_readiness: 0.20
    stability_score: 0.15
```

Load in code:
```python
import yaml

with open('config/task_002_clustering.yaml') as f:
    CONFIG = yaml.safe_load(f)

# Use: CONFIG['commit_history']['recency_window_days']
```
```

---

### 9. Performance Targets

Clear performance requirements.

```markdown
## Performance Targets

### Per Component
- Single branch analysis: < 2 seconds
- Memory usage: < 50 MB per analysis
- Handle repositories with 10,000+ commits

### Scalability
- 13 branches total: < 26 seconds
- 50 branches: < 100 seconds

### Quality Metrics
- No timeouts on standard hardware
- Consistent performance across repo sizes
```

---

### 10. Testing Strategy

How to verify the implementation.

```markdown
## Testing Strategy

### Unit Tests

Minimum 8 test cases:

```python
def test_commit_recency_recent_commits():
    # Commits from last 7 days should score > 0.8
    
def test_commit_recency_old_commits():
    # Commits from 90+ days ago should score < 0.3
    
def test_commit_recency_single_commit():
    # Single-commit branches should be handled
    
def test_merge_readiness_recently_synced():
    # < 5 commits behind main: score > 0.85
    
def test_merge_readiness_far_behind():
    # > 50 commits behind: score < 0.4
    
def test_merge_readiness_orphaned_branch():
    # Branch with no common ancestor: handled gracefully
    
def test_output_format():
    # Output matches JSON schema
    
def test_performance():
    # < 2 seconds per branch
```

### Integration Tests

After all sub-subtasks complete:

```python
def test_full_pipeline_with_all_metrics():
    # Verify 002.1 output is compatible with 002.4 input
    
def test_output_schema_validation():
    # Validate against JSON schema
```

### Coverage Target
- Code coverage: > 95%
- All edge cases covered
- All error paths tested
```

---

### 11. Common Gotchas & Solutions

Prevent common mistakes.

```markdown
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

**Gotcha 4: Non-ASCII author names**
```python
# WRONG
author = output.decode('utf-8')  # May fail on non-ASCII

# RIGHT
author = output.decode('utf-8', errors='replace')  # Graceful fallback
```
```

---

### 12. Integration Checkpoint

Gate for moving to next task.

```markdown
## Integration Checkpoint

**When to move to Task 002.4 (BranchClusterer):**

- [ ] All 8 sub-subtasks complete
- [ ] Unit tests passing (>90% coverage)
- [ ] Output matches specification exactly
- [ ] No validation errors on test data
- [ ] Performance targets met (< 2s per branch)
- [ ] Edge cases handled correctly
- [ ] Code review approved
- [ ] Commit message: "feat: complete Task 002.1 CommitHistoryAnalyzer"
```

---

### 13. Done Definition

Checklist for "complete."

```markdown
## Done Definition

Task 002.1 is done when:

1. ✅ All 8 sub-subtasks marked complete
2. ✅ Unit tests pass (>95% coverage) on CI/CD
3. ✅ Code review approved
4. ✅ Outputs match specification exactly
5. ✅ Output schema validation passes
6. ✅ Documentation complete and accurate
7. ✅ Performance benchmarks met
8. ✅ Ready for hand-off to Task 002.4
9. ✅ Commit: "feat: complete Task 002.1 CommitHistoryAnalyzer"
10. ✅ All success criteria checkboxes marked complete
```

---

### 14. Next Steps

What to do after this task.

```markdown
## Next Steps

1. **Immediate:** Implement sub-subtask 002.1.1 (Design Metric System)
2. **Week 1:** Complete all 8 sub-subtasks
3. **Week 1-2:** Write and test unit tests (target: >95%)
4. **Week 2:** Code review
5. **Week 2:** Ready for Task 002.4 (BranchClusterer)

**Reference:** See IMPLEMENTATION_INDEX.md for team coordination
```

---

## Template Summary

**Every task file includes these 14 sections in this order:**

1. Task Header
2. Overview/Purpose
3. Success Criteria (detailed, complete)
4. Prerequisites & Dependencies
5. Sub-subtasks Breakdown
6. Specification Details
7. Implementation Guide
8. Configuration Parameters
9. Performance Targets
10. Testing Strategy
11. Common Gotchas & Solutions
12. Integration Checkpoint
13. Done Definition
14. Next Steps

---

## Apply This Standard To:

### Immediate (Task 002)
- [ ] task_002.1.md (CommitHistoryAnalyzer)
- [ ] task_002.2.md (CodebaseStructureAnalyzer)
- [ ] task_002.3.md (DiffDistanceCalculator)
- [ ] task_002.4.md (BranchClusterer)
- [ ] task_002.5.md (IntegrationTargetAssigner)

### Retrofit (Next Phase)
- [ ] task_001.md → split into task_001.1.md, task_001.2.md, etc.
- [ ] task_007.md → split and restructure
- [ ] task_075.md → already have task-75.1.md through task-75.5.md, convert to standard format
- [ ] Other existing tasks as time permits

### Going Forward
- All new tasks follow this structure automatically

---

## Benefits

✅ **Consistency:** Every task organized identically  
✅ **Completeness:** All information in one place (no scattered criteria)  
✅ **Discoverability:** Team knows exactly where to find anything  
✅ **Handoff-ready:** Give someone the file, they have everything  
✅ **Verification:** Easy to audit for missing information  
✅ **Scalable:** Works for 5 tasks or 50 tasks

---

**This standard prevents the consolidation problem forever by making it impossible to lose information.**

Approved: January 6, 2026
