# Task 002.1: CommitHistoryAnalyzer

**Status:** Ready for Implementation  
**Priority:** High  
**Effort:** 24-32 hours  
**Complexity:** 7/10  
**Dependencies:** None - can start immediately  
**Blocks:** Task 002.4 (BranchClusterer)

---

## Purpose

Create a reusable Python class that extracts and scores commit history metrics for branches. This analyzer is one of three Stage One components that will be integrated into the clustering pipeline.

**Scope:** CommitHistoryAnalyzer class only  
**No dependencies** - can start immediately  
**Parallelizable with:** Task 002.2 and Task 002.3

---

## Success Criteria

Task 002.1 is complete when:

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
- [ ] Compatible with Task 002.4 (BranchClusterer) input requirements
- [ ] Compatible with Task 002.6 (PipelineIntegration) consumption patterns
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
- Task 002.4 (BranchClusterer) - requires output from this task
- Task 002.6 (PipelineIntegration) - may use outputs

### External Dependencies
- Python subprocess (built-in)
- GitPython (optional, or use subprocess.run)
- Standard library: datetime, json, typing

### No Dependency On
- Task 002.2 (CodebaseStructureAnalyzer) - can start in parallel
- Task 002.3 (DiffDistanceCalculator) - can start in parallel

---

## Sub-subtasks

### 002.1.1: Design Metric System
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

### 002.1.2: Set Up Git Data Extraction
**Effort:** 4-5 hours  
**Depends on:** 002.1.1

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

### 002.1.3: Implement Commit Recency Metric
**Effort:** 3-4 hours  
**Depends on:** 002.1.1, 002.1.2

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

### 002.1.4: Implement Commit Frequency Metric
**Effort:** 3-4 hours  
**Depends on:** 002.1.1, 002.1.2

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

### 002.1.5: Implement Authorship & Stability Metrics
**Effort:** 4-5 hours  
**Depends on:** 002.1.1, 002.1.2

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

### 002.1.6: Implement Merge Readiness Metric
**Effort:** 3-4 hours  
**Depends on:** 002.1.1, 002.1.2

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

### 002.1.7: Implement Aggregation & Weighting
**Effort:** 2-3 hours  
**Depends on:** 002.1.3, 002.1.4, 002.1.5, 002.1.6

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

### 002.1.8: Unit Testing & Edge Cases
**Effort:** 3-4 hours  
**Depends on:** 002.1.7

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
- [ ] Edge cases covered (new, stale, orphaned branches)
- [ ] Error handling tested (non-existent branches, git errors)
- [ ] Output validation includes JSON schema check
- [ ] Performance tests meet <2 second requirement
- [ ] All tests use mocked git (no real git operations in tests)

---

## Specification

### Class Interface

```python
class CommitHistoryAnalyzer:
    def __init__(self, repo_path: str, main_branch: str = "main"):
        """Initialize analyzer with repository path."""
        
    def analyze(self, branch_name: str) -> dict:
        """Analyze commit history for a branch.
        
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

### Metric Definitions

| Metric | Definition | Formula Notes | Weight |
|--------|-----------|---|--------|
| `commit_recency` | How recent are the latest commits | Exponential decay, 30-day window | 0.25 |
| `commit_frequency` | Commit rate relative to branch age | commits / days_active, baseline 5/week | 0.20 |
| `authorship_diversity` | Ratio of unique contributors | unique_authors / total_commits | 0.20 |
| `merge_readiness` | How synchronized with main | Inverse of commits_behind_main | 0.20 |
| `stability_score` | Consistency of commit patterns | Inverse of average churn per commit | 0.15 |

---

## Implementation Guide

### 002.1.1: Design Metric System

Define each metric with:

```python
METRICS = {
    'commit_recency': {
        'description': 'How recent are the latest commits',
        'formula': 'exp(-days_since_last / WINDOW_DAYS)',
        'window_days': 30,
        'expected_range': [0.0, 1.0],
        'interpretation': 'Higher = more recent commits'
    },
    'commit_frequency': {
        'description': 'Commit rate relative to branch age',
        'formula': 'commits / max(1, days_active) / BASELINE',
        'baseline_commits_per_week': 5,
        'expected_range': [0.0, 1.0+],
        'normalization': 'cap at 1.0'
    },
    # ... continue for other metrics
}
```

### 002.1.2: Git Data Extraction

```python
import subprocess
from datetime import datetime

def execute_git_command(repo_path: str, cmd: List[str], timeout: int = 30) -> str:
    """Execute git command safely with timeout."""
    try:
        result = subprocess.run(
            cmd,
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        if result.returncode != 0:
            raise GitCommandError(result.stderr)
        return result.stdout
    except subprocess.TimeoutExpired:
        raise GitTimeoutError(f"Git command timed out after {timeout}s")

def get_commit_log(repo_path: str, branch_name: str) -> List[Dict]:
    """Extract commit data for a branch."""
    # Verify branch exists first
    cmd = ['git', 'rev-parse', '--verify', branch_name]
    try:
        execute_git_command(repo_path, cmd)
    except:
        raise BranchNotFoundError(f"Branch {branch_name} not found")
    
    # Get commit log
    cmd = ['git', 'log', branch_name, '--format=%ai|%an|%s']
    output = execute_git_command(repo_path, cmd)
    
    commits = []
    for line in output.strip().split('\n'):
        if not line:
            continue
        date_str, author, subject = line.split('|', 2)
        commits.append({
            'date': datetime.fromisoformat(date_str),
            'author': author.strip(),
            'subject': subject
        })
    
    return commits
```

### 002.1.3: Commit Recency Metric

```python
import math
from datetime import datetime

def calculate_commit_recency(
    commits: List[Dict],
    window_days: int = 30
) -> float:
    """Calculate recency metric using exponential decay.
    
    Recent commits (< 7 days) → score > 0.8
    Old commits (90+ days) → score < 0.3
    """
    if not commits:
        return 0.5  # Default for empty
    
    latest_commit = max(commit['date'] for commit in commits)
    days_since_last = (datetime.now() - latest_commit).days
    
    # Exponential decay: exp(-days / window)
    # At window_days: score = 0.368
    # At 0 days: score = 1.0
    # At 90 days: score = 0.030
    score = math.exp(-days_since_last / window_days)
    
    # Clamp to [0, 1]
    return max(0.0, min(1.0, score))
```

### 002.1.4: Commit Frequency Metric

```python
def calculate_commit_frequency(
    commits: List[Dict],
    baseline_commits_per_week: int = 5
) -> float:
    """Calculate frequency metric.
    
    High activity (>5 commits/week) → score > 0.7
    Low activity (<1 commit/week) → score < 0.4
    """
    if not commits:
        return 0.5
    
    # Calculate branch lifetime in days
    first_commit = min(commit['date'] for commit in commits)
    last_commit = max(commit['date'] for commit in commits)
    days_active = max(1, (last_commit - first_commit).days)
    
    # Calculate commits per week
    weeks_active = days_active / 7
    commits_per_week = len(commits) / max(1, weeks_active)
    
    # Score: normalize by baseline
    # If commits_per_week = baseline → score = 1.0
    # If commits_per_week = 0 → score = 0.0
    score = commits_per_week / baseline_commits_per_week
    
    # Clamp to [0, 1]
    return max(0.0, min(1.0, score))
```

### 002.1.5: Authorship & Stability

```python
def calculate_authorship_diversity(commits: List[Dict]) -> float:
    """Diversity ratio: unique_authors / total_commits."""
    if not commits:
        return 0.5
    
    unique_authors = len(set(c['author'] for c in commits))
    total_commits = len(commits)
    
    # Diversity ratio
    score = unique_authors / total_commits
    return max(0.0, min(1.0, score))

def calculate_stability_score(
    commits: List[Dict],
    baseline_churn: int = 50
) -> float:
    """Stability: inverse of churn per commit.
    
    Low churn (stable commits) → score > 0.7
    High churn (large commits) → score < 0.4
    """
    if not commits:
        return 0.5
    
    # This is simplified; real implementation would use git show
    # for each commit to get actual line changes
    # For now, estimate based on message length or use git diff
    
    # Average churn per commit (lines changed)
    # Lower is more stable
    avg_churn = estimate_average_churn(commits)
    
    # Inverse normalize
    score = 1.0 - (avg_churn / (baseline_churn * 2))
    return max(0.0, min(1.0, score))
```

### 002.1.6: Merge Readiness

```python
def calculate_merge_readiness(
    repo_path: str,
    branch_name: str,
    main_branch: str = "main",
    max_behind: int = 50
) -> float:
    """Score how synchronized branch is with main.
    
    Recently synced (<5 behind) → score > 0.85
    Far behind (>50 behind) → score < 0.4
    """
    try:
        # Find merge base
        cmd = ['git', 'merge-base', main_branch, branch_name]
        merge_base = execute_git_command(repo_path, cmd).strip()
        
        # Count commits on branch since merge base
        cmd = ['git', 'rev-list', f'{merge_base}..{branch_name}', '--count']
        commits_since = int(execute_git_command(repo_path, cmd).strip())
        
        # Inverse normalize
        # 0 commits behind → score = 1.0
        # max_behind commits → score = 0.0
        score = 1.0 - (commits_since / max_behind)
        return max(0.0, min(1.0, score))
        
    except GitCommandError:
        # Orphaned branch or other issue
        return 0.5  # Default
```

### 002.1.7: Aggregation

```python
def aggregate_metrics(
    metrics: Dict[str, float],
    weights: Dict[str, float] = None
) -> float:
    """Combine 5 metrics with weights."""
    if weights is None:
        weights = {
            'commit_recency': 0.25,
            'commit_frequency': 0.20,
            'authorship_diversity': 0.20,
            'merge_readiness': 0.20,
            'stability_score': 0.15
        }
    
    # Verify all metrics in [0, 1]
    for metric, value in metrics.items():
        assert 0 <= value <= 1, f"{metric} = {value} out of range"
    
    # Weighted sum
    aggregate = sum(
        metrics[k] * weights[k]
        for k in metrics.keys()
    )
    
    # Final clamp
    return max(0.0, min(1.0, aggregate))
```

---

## Configuration Parameters

All parameters externalized in `config/task_002_clustering.yaml`:

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

def load_config(config_path: str = "config/task_002_clustering.yaml"):
    with open(config_path) as f:
        return yaml.safe_load(f)

config = load_config()
recency_window = config['commit_history']['recency_window_days']
```

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
    
def test_performance_requirement():
    """Single branch analysis: <2 seconds"""
```

### Integration Tests

After all sub-subtasks:

```python
def test_full_pipeline_with_all_metrics():
    """Verify output is compatible with Task 002.4 input"""
    
def test_output_schema_validation():
    """Validate against JSON schema"""
    
def test_multiple_branches():
    """Process 13+ branches without errors"""
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

**Gotcha 4: Non-ASCII author names**
```python
# WRONG
author = output.decode('utf-8')  # May fail on non-ASCII

# RIGHT
author = output.decode('utf-8', errors='replace')  # Graceful fallback
```

**Gotcha 5: Binary files cause parsing errors**
```python
# WRONG
for line in output.split('\n'):  # Binary markers confuse parser

# RIGHT
if not line or line.startswith('Binary'):
    continue  # Skip binary file markers
```

---

## Integration Checkpoint

**When to move to Task 002.4 (BranchClusterer):**

- [ ] All 8 sub-subtasks complete
- [ ] Unit tests passing (>90% coverage)
- [ ] Output matches specification exactly
- [ ] No validation errors on test data
- [ ] Performance targets met (<2s per branch)
- [ ] Edge cases handled correctly
- [ ] Code review approved
- [ ] Commit message: "feat: complete Task 002.1 CommitHistoryAnalyzer"

---

## Done Definition

Task 002.1 is done when:

1. ✅ All 8 sub-subtasks marked complete
2. ✅ Unit tests pass (>95% coverage) on CI/CD
3. ✅ Code review approved
4. ✅ Outputs match specification exactly
5. ✅ Output schema validation passes
6. ✅ Documentation complete and accurate
7. ✅ Performance benchmarks met (<2 seconds per branch)
8. ✅ Edge cases handled gracefully
9. ✅ Ready for hand-off to Task 002.4
10. ✅ Commit: "feat: complete Task 002.1 CommitHistoryAnalyzer"
11. ✅ All success criteria checkboxes marked complete

---

## Next Steps

1. **Immediate:** Implement sub-subtask 002.1.1 (Design Metric System)
2. **Week 1:** Complete all 8 sub-subtasks
3. **Week 1-2:** Write and test unit tests (target: >95% coverage)
4. **Week 2:** Code review and refinement
5. **Week 2:** Ready for Task 002.4 (BranchClusterer)

**Reference:** See IMPLEMENTATION_INDEX.md for team coordination and full project timeline

---

**Last Updated:** January 6, 2026  
**Consolidated from:** Task 75.1 (task-75.1.md) with 61 original success criteria preserved  
**Structure:** TASK_STRUCTURE_STANDARD.md
