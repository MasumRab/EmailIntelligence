# Task 75.1: CommitHistoryAnalyzer

## Purpose
Create a reusable Python class that extracts and scores commit history metrics for branches. This analyzer is one of three Stage One components that will be integrated into the clustering pipeline.

**Scope:** CommitHistoryAnalyzer class only  
**Effort:** 24-32 hours | **Complexity:** 7/10  
**Status:** Ready for implementation  
**No dependencies** - can start immediately

---

## Quick Navigation

Navigate this document using these links:

- [Purpose](#purpose)
- [Developer Quick Reference](#developer-quick-reference)
- [Success Criteria](#success-criteria)
- [Subtasks Overview](#subtasks-overview)
- [Subtask Details](#subtasks)
- [Configuration & Defaults](#configuration-parameters)
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

### Output Specification
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

**See HANDOFF_75.1_CommitHistoryAnalyzer.md for full implementation guide.**

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

**Performance Targets:**
- [ ] Single branch analysis: **< 2 seconds** (on typical 500-commit repository)
- [ ] Memory usage: **< 50 MB** per analysis
- [ ] Handles **10,000+ commit repositories** without failure
- [ ] Metric computation: **O(n)** where n = commit count
- [ ] Git command timeout: **30 seconds max** (protects against hanging on very large repos)

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
75.1.1 (2-3h) ────────┐
[Metric Design]       │
                      ├─→ 75.1.2 (4-5h) ────────┐
                      │  [Git Extraction]       │
                      │                         ├─→ 75.1.3-75.1.6 (parallel, 3-5h each) ────┐
                      │                         │   [Recency, Frequency, Auth, Stability]  │
                      │                         │                                          ├─→ 75.1.7 (2-3h)
                      └─────────────────────────┘                                          │  [Aggregation]
                                                                                           │
                                                                                           └─→ 75.1.8 (3-4h)
                                                                                              [Unit Tests]

Critical Path: 75.1.1 → 75.1.2 → 75.1.3-75.1.6 (parallel) → 75.1.7 → 75.1.8
Minimum Duration: 24-28 hours (with parallelization of 75.1.3-75.1.6)
```

### Parallel Opportunities

**Can run in parallel (after 75.1.2):**
- 75.1.3: Recency metric
- 75.1.4: Frequency metric
- 75.1.5: Authorship & stability metrics
- 75.1.6: Merge readiness metric

All four metric tasks depend only on 75.1.2 (git extraction) and are independent of each other. **Estimated parallel execution saves 10-12 hours.**

**Must be sequential:**
- 75.1.1 → 75.1.2 (metrics design required before extraction)
- 75.1.2 → 75.1.3-75.1.6 (extraction required before metric calculation)
- 75.1.3-75.1.6 → 75.1.7 (all metrics needed before aggregation)
- 75.1.7 → 75.1.8 (main class needed before testing)

### Timeline with Parallelization

**Days 1-2: Design (75.1.1)**
- Define metric formulas, weights, normalization
- Document edge case handling

**Days 2-3: Git Extraction (75.1.2)**
- Implement subprocess-based git log
- Create structured output format

**Days 3-5: Metrics (75.1.3-75.1.6 in parallel)**
- Day 3-4: Implement recency + frequency (2 people)
- Day 3-4: Implement authorship + stability (2 people) 
- Day 4-5: Merge readiness (1 person, can overlap)

**Days 5-6: Aggregation & Testing (75.1.7-75.1.8)**
- Day 5: Implement aggregation
- Day 6: Write comprehensive unit tests

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
- [ ] Define the 5 core metrics (recency, frequency, authorship, merge_readiness, stability)
- [ ] Document exponential decay function for recency
- [ ] Create normalization strategy for each metric
- [ ] Define weighting formula: sum = 1.0
- [ ] Document edge cases for each metric

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
- [ ] Implement git command: `git log main..BRANCH_NAME --pretty=format:"%H|%ai|%an|%s"`
- [ ] Implement branch validation (check git show-ref)
- [ ] Extract metadata: hash, date, author, message
- [ ] Handle non-existent branches with clear error messages

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

### Implementation Checklist (From HANDOFF)
- [ ] Extract most recent commit date from branch
- [ ] Implement exponential decay: exp(-(days_since_last_commit) / RECENCY_WINDOW_DAYS)
- [ ] Normalize result to [0, 1] range
- [ ] Handle single-commit branches
- [ ] Test with branches aged 7 days, 30 days, 90+ days

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

### Implementation Checklist (From HANDOFF)
- [ ] Count total commits on branch
- [ ] Calculate branch lifetime in days (first to last commit)
- [ ] Compute velocity: commits / days (handle single commit)
- [ ] Define baseline: 5 commits/week (velocity = 0.71 commits/day)
- [ ] Normalize: velocity / baseline, cap at 1.0

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

### Implementation Checklist (From HANDOFF)
- [ ] Extract unique author names from commit metadata
- [ ] Calculate diversity: unique_authors / total_commits
- [ ] Apply sigmoid function to normalize authorship
- [ ] Extract line changes: git diff --stat per commit
- [ ] Calculate churn: total_lines_changed / commit_count
- [ ] Stability: 1 - min(churn / baseline, 1.0)

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

### Implementation Checklist (From HANDOFF)
- [ ] Find merge base: `git merge-base main BRANCH_NAME`
- [ ] Count commits on main since merge base
- [ ] Count commits on branch since merge base
- [ ] Calculate "commits behind": commits_on_main_after_merge_base
- [ ] Formula: 1 - min(commits_behind / 50, 1.0)

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

### Implementation Checklist (From HANDOFF)
- [ ] Verify all metrics in [0, 1] range (add assertions)
- [ ] Implement weighted sum: 0.25*recency + 0.20*frequency + 0.20*authorship + 0.20*merge_readiness + 0.15*stability
- [ ] Create output dict with all required fields
- [ ] Add ISO 8601 timestamp: datetime.utcnow().isoformat() + 'Z'
- [ ] Round aggregate_score to 3 decimal places

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

### Test Case Examples (From HANDOFF)

1. **test_normal_branch**: 42 commits, 3 authors, 18 days active
   - Expected: All metrics in [0,1], aggregate_score > 0.5

2. **test_new_branch**: 2 commits, 1 author, 1 day old
   - Expected: High recency (>0.9), handle single-commit gracefully

3. **test_stale_branch**: 100+ days old, no recent commits
   - Expected: Low recency (<0.2), appropriate other metrics

4. **test_high_activity_branch**: 200+ commits, 5+ authors
   - Expected: High frequency and authorship diversity, aggregation correct

5. **test_nonexistent_branch**: Attempt to analyze non-existent branch
   - Expected: Raise BranchNotFoundError with clear message

6. **test_single_commit_branch**: Branch with only 1 commit
   - Expected: All metrics defined, handle edge case without errors

7. **test_binary_only_branch**: Branch with only binary file changes
   - Expected: Metrics computed ignoring binary files

8. **test_performance**: Analyze branch with 10,000+ commits
   - Expected: Complete in <2 seconds, reasonable memory usage

---

## Configuration & Defaults

All parameters should be externalized to configuration files (not hardcoded). Use YAML format:

```yaml
# config/analyzers.yaml
commit_history_analyzer:
  # Metric Weights (sum must equal 1.0)
  recency_weight: 0.25
  frequency_weight: 0.20
  authorship_diversity_weight: 0.20
  merge_readiness_weight: 0.20
  stability_score_weight: 0.15
  
  # Recency Scoring
  recency_window_days: 30
  recency_recent_threshold_days: 7  # Threshold for "recent" classification
  
  # Frequency Scoring
  frequency_baseline_commits_per_week: 5
  frequency_active_threshold: 3  # Commits per week for "active" classification
  
  # Stability Scoring
  stability_baseline_lines_per_commit: 50
  stability_large_change_threshold: 200  # Lines for "large change"
  
  # Merge Readiness Scoring
  merge_readiness_max_commits_behind: 50
  merge_readiness_sync_threshold: 5  # Commits behind for "synchronized"
  
  # Git Execution
  git_command_timeout_seconds: 30
  git_batch_size: 100  # Process commits in batches for memory efficiency
```

**How to use in code:**
```python
import yaml

def load_config(config_path='config/analyzers.yaml'):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)['commit_history_analyzer']

config = load_config()
RECENCY_WEIGHT = config['recency_weight']
RECENCY_WINDOW_DAYS = config['recency_window_days']
# ... etc
```

**Why externalize?**
- Easy to tune without redeploying code
- Different configurations for different environments (dev/test/prod)
- Can adjust thresholds based on organizational needs
- No code recompilation needed to adjust parameters

---

## Technical Reference

### Git Commands Reference

```bash
# Get commits unique to branch (not in main)
git log main..BRANCH_NAME --pretty=format:"%H|%ai|%an|%s"

# Get commit diff stats (for stability_score)
git log main..BRANCH_NAME --pretty=format:"%H" | \
  xargs -I {} git diff main...{} --stat

# Get merge base (for merge_readiness)
git merge-base main BRANCH_NAME

# Get commit date for branch
git log -1 --format=%ai BRANCH_NAME

# Check if branch exists
git show-ref --quiet refs/heads/BRANCH_NAME
```

### Code Patterns

**Using subprocess with timeout:**
```python
import subprocess
result = subprocess.run(
    ['git', 'log', ...],
    capture_output=True,
    text=True,
    timeout=30
)
```

**Metrics normalization pattern:**
```python
def normalize(value: float, min_val: float = 0, max_val: float = 1) -> float:
    """Normalize value to [0, 1] range."""
    return max(0, min(1, (value - min_val) / (max_val - min_val)))
```

### Dependencies & Parallel Tasks

- **No dependencies on other Task 75.x components** - can start immediately
- **Output feeds into:** Task 75.4 (BranchClusterer)
- **Can work in parallel with:** Task 75.2 (CodebaseStructureAnalyzer), Task 75.3 (DiffDistanceCalculator)
- **External libraries:** GitPython or subprocess (git CLI)

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
git commit -m "chore: create analyzer module structure"
```

### Subtask 75.1.1: Metric System Design

```bash
# Create design document
cat > docs/METRIC_DESIGN.md << 'EOF'
# Commit History Metrics

## Metric 1: commit_recency
Formula: exp(-(days_since_last_commit / WINDOW_DAYS))
Range: [0, 1]
Interpretation: 1.0 = very recent, 0.0 = very old

## Metric 2: commit_frequency
Formula: (commits / days_active) / baseline
Range: [0, 1]
Interpretation: 1.0 = high activity, 0.0 = inactive

[... define remaining 3 metrics ...]
EOF

git add docs/METRIC_DESIGN.md
git commit -m "docs: define commit history metrics (75.1.1)"
```

### Subtask 75.1.2: Git Data Extraction

```bash
cat > src/analyzers/git_utils.py << 'EOF'
import subprocess
from typing import List, Dict

def get_commits_on_branch(repo_path: str, branch: str, 
                         main_branch: str = "main") -> List[Dict]:
    """Extract commits unique to this branch."""
    cmd = [
        'git', 'log', f'{main_branch}..{branch}',
        '--pretty=format:%H|%ai|%an|%s'
    ]
    result = subprocess.run(
        cmd, cwd=repo_path,
        capture_output=True, text=True,
        timeout=30, encoding='utf-8'
    )
    
    commits = []
    for line in result.stdout.strip().split('\n'):
        if line:
            hash, date, author, msg = line.split('|', 3)
            commits.append({'hash': hash, 'date': date, 'author': author})
    return commits
EOF

git add src/analyzers/git_utils.py
git commit -m "feat: implement git data extraction (75.1.2)"
```

### Subtasks 75.1.3-75.1.6: Metrics (Parallel)

```bash
# These can be implemented in parallel by different team members

# Create recency metric
cat > src/analyzers/metrics_recency.py << 'EOF'
import math
from datetime import datetime

def compute_recency(last_commit_date: str, window_days: int = 30) -> float:
    """Score branch by how recent last commit is."""
    last = datetime.fromisoformat(last_commit_date.replace('Z', '+00:00'))
    now = datetime.utcnow()
    days_since = max(0, (now - last).days)
    recency = math.exp(-days_since / window_days)
    return min(1.0, max(0.0, recency))
EOF

# Create frequency metric
cat > src/analyzers/metrics_frequency.py << 'EOF'
def compute_frequency(commits: int, days_active: int, 
                     baseline: float = 5.0) -> float:
    """Score branch by development velocity."""
    days_active = max(1, days_active)  # Avoid division by zero
    commits_per_day = commits / days_active
    baseline_per_day = baseline / 7
    frequency = commits_per_day / baseline_per_day
    return min(1.0, max(0.0, frequency))
EOF

# Create other metrics files
touch src/analyzers/metrics_authorship.py
touch src/analyzers/metrics_stability.py
touch src/analyzers/metrics_merge_readiness.py

git add src/analyzers/metrics_*.py
git commit -m "feat: implement metric modules (75.1.3-75.1.6)"
```

### Subtask 75.1.7: Aggregation

```bash
cat > src/analyzers/aggregator.py << 'EOF'
from typing import Dict

def aggregate_metrics(metrics: Dict[str, float], 
                     weights: Dict[str, float]) -> float:
    """Combine individual metrics into aggregate score."""
    total = sum(metrics.get(k, 0) * weights.get(k, 0) 
                for k in metrics.keys())
    return min(1.0, max(0.0, total))
EOF

git add src/analyzers/aggregator.py
git commit -m "feat: implement metric aggregation (75.1.7)"
```

### Subtask 75.1.8: Unit Tests

```bash
cat > tests/analyzers/test_commit_history_analyzer.py << 'EOF'
import pytest
from src.analyzers import CommitHistoryAnalyzer

@pytest.fixture
def test_repo(tmp_path):
    """Create test repository."""
    # Initialize git repo with sample commits
    pass

def test_normal_branch(test_repo):
    analyzer = CommitHistoryAnalyzer(test_repo)
    result = analyzer.analyze("feature")
    assert result['aggregate_score'] > 0.5
    assert all(0 <= m <= 1 for m in result['metrics'].values())

def test_single_commit_branch(test_repo):
    analyzer = CommitHistoryAnalyzer(test_repo)
    result = analyzer.analyze("single-commit")
    assert result['commit_count'] == 1
    assert all(0 <= m <= 1 for m in result['metrics'].values())

[... implement remaining tests ...]
EOF

# Run tests
pytest tests/analyzers/ -v --cov=src/analyzers --cov-report=html

git add tests/
git commit -m "test: unit tests for CommitHistoryAnalyzer (95%+ coverage)"
```

### Final Steps

```bash
# Create configuration file
mkdir -p config
cat > config/analyzers.yaml << 'EOF'
commit_history_analyzer:
  recency_weight: 0.25
  frequency_weight: 0.20
  [... rest of config ...]
EOF

git add config/
git commit -m "config: analyzer configuration parameters"

# Push to origin
git push origin feat/commit-history-analyzer

# Create pull request
gh pr create --title "Complete Task 75.1: CommitHistoryAnalyzer" \
             --body "Implements commit history analysis with 5 metrics"
```

---

## Integration Handoff

### What Gets Passed to Task 75.4 (BranchClusterer)

**Task 75.4 expects input in this format:**

```python
from src.analyzers import CommitHistoryAnalyzer

analyzer = CommitHistoryAnalyzer(repo_path=".", main_branch="main")
result = analyzer.analyze(branch_name="feature/auth")

# result is a dict like:
# {
#   "branch_name": "feature/auth",
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

**Task 75.4 uses these outputs by:**
1. Collecting results from all three Stage One analyzers (75.1, 75.2, 75.3)
2. Combining metrics using weighted formula: 0.35*c1 + 0.35*c2 + 0.30*c3
3. Building distance matrix from combined scores
4. Running hierarchical clustering on distances
5. Outputting cluster assignments

**Validation before handoff:**
```bash
# Verify output matches specification
python -c "
from src.analyzers import CommitHistoryAnalyzer
analyzer = CommitHistoryAnalyzer('.')
result = analyzer.analyze('main')

# Check required fields
assert 'branch_name' in result
assert 'metrics' in result
assert 'aggregate_score' in result

# Check metrics are normalized
for m in result['metrics'].values():
    assert 0 <= m <= 1, f'Metric {m} not in [0,1]'

assert 0 <= result['aggregate_score'] <= 1

print('✓ Output valid and ready for Task 75.4')
"
```

---

## Common Gotchas & Solutions

### Gotcha 1: Git Timeout on Large Repos ⚠️

**Problem:** `subprocess.run()` hangs indefinitely on repos with 10,000+ commits  
**Symptom:** Process stuck at "Analyzing commits...", never returns  
**Root Cause:** No timeout set, large repos take too long  

**Solution:** Always set timeout parameter
```python
result = subprocess.run(
    cmd, 
    timeout=30,  # ← CRITICAL: 30 second timeout
    capture_output=True,
    text=True
)
```

**Test:** Run against large branch (15k+ commits), verify completes in <30 seconds

---

### Gotcha 2: Merge Base Not Found on Orphaned Branches ⚠️

**Problem:** Some branches have no common ancestor with main (orphaned)  
**Symptom:** `CalledProcessError` from `git merge-base main BRANCH`  
**Root Cause:** Branch created without merging from main  

**Solution:** Handle gracefully with try-except
```python
try:
    result = subprocess.run(['git', 'merge-base', 'main', branch_name], 
                          timeout=30, capture_output=True, text=True, check=True)
    merge_base = result.stdout.strip()
except subprocess.CalledProcessError:
    # Orphaned branch - use conservative defaults
    merge_base = None
    commits_behind = float('inf')
```

**Test:** Create test orphaned branch, verify metrics computed correctly

---

### Gotcha 3: Division by Zero in Frequency Metric 🔴

**Problem:** Single-commit branches have < 1 day lifetime, frequency = commits / days fails  
**Symptom:** `ZeroDivisionError` or invalid frequency metric  
**Root Cause:** `days_active = last_date - first_date` = 0 for same-day commits  

**Solution:** Use maximum of calculated value and 1 day minimum
```python
days_active_raw = (last_commit_date - first_commit_date).days
days_active = max(1, days_active_raw)  # ← Minimum 1 day
frequency = commits / days_active  # Now safe
```

**Test:** Create single-commit branch, verify frequency ∈ [0,1]

---

### Gotcha 4: Binary Files Cause Line Count Parsing Errors ⚠️

**Problem:** `git diff --stat` shows binary files differently: "Bin 1KB -> 2KB"  
**Symptom:** `ValueError` when parsing "Bin 1KB -> 2KB" as integer  
**Root Cause:** Binary file stat format differs from text files  

**Solution:** Skip binary files in line counting
```python
lines_changed_total = 0
for line in diff_stats.split('\n'):
    if 'Bin' not in line:  # ← Skip binary files
        parts = line.split('|')
        if len(parts) >= 2:
            changes = parts[1].strip()
            lines = changes.count('+') + changes.count('-')
            lines_changed_total += lines
```

**Test:** Branch with only binary changes (.zip files), verify no error

---

### Gotcha 5: Author Names with Non-ASCII Characters 🔴

**Problem:** Author names from non-English locales have special characters  
**Symptom:** `UnicodeDecodeError` when parsing git output  
**Root Cause:** Default encoding not UTF-8  

**Solution:** Explicitly specify UTF-8 encoding
```python
result = subprocess.run(
    cmd,
    capture_output=True,
    text=True,
    encoding='utf-8'  # ← Explicit UTF-8
)
```

**Test:** Analyze branches with authors like "François" or "李明", verify no errors

---

### Gotcha 6: Recency Metric Breaks with Future System Clocks ⚠️

**Problem:** Developer with wrong system clock → future commit dates → negative days  
**Symptom:** `math.exp()` produces huge numbers, metric > 1.0  
**Root Cause:** No bounds checking on date calculation  

**Solution:** Cap days_since at 0, clamp final metric
```python
now = datetime.utcnow()
last_commit = datetime.fromisoformat(last_commit_date)
days_since = max(0, (now - last_commit).days)  # ← Cap at 0
recency = math.exp(-days_since / RECENCY_WINDOW_DAYS)
recency = min(1.0, max(0.0, recency))  # ← Clamp to [0,1]
```

**Test:** Verify metric always in [0,1] even with future dates

---

### Gotcha 7: NaN Values from Empty Branch Metrics ⚠️

**Problem:** Branch with no commits on metrics calculation causes NaN  
**Symptom:** Output dict contains NaN instead of valid metric  
**Root Cause:** Division by zero or missing data handling  

**Solution:** Handle empty branches gracefully
```python
if not commits:
    return {
        'commit_recency': 0.5,  # Default neutral value
        'commit_frequency': 0.5,
        'authorship_diversity': 0.5,
        'merge_readiness': 0.5,
        'stability_score': 0.5,
        'aggregate_score': 0.5,
        'error': 'No commits found on branch'
    }
```

**Test:** Analyze newly-created empty branch, verify defaults returned

---

### Gotcha 8: Subprocess Encoding Issues on Windows ⚠️

**Problem:** Git output encoding differs on Windows vs Linux  
**Symptom:** `UnicodeDecodeError` on Windows systems  
**Root Cause:** Windows uses different default encoding  

**Solution:** Explicitly set encoding and error handling
```python
result = subprocess.run(
    cmd,
    capture_output=True,
    text=True,
    encoding='utf-8',
    errors='replace'  # ← Replace invalid characters instead of failing
)
```

**Test:** Run on Windows system, verify no encoding errors

---

### Gotcha 9: Cache Invalidation for Repository Changes ⚠️

**Problem:** If repo is modified between runs, cached results are stale  
**Symptom:** Metrics show old values even after new commits  
**Root Cause:** No validation that repo state hasn't changed  

**Solution:** Include repo hash in cache key
```python
import hashlib

def get_repo_state_hash(repo_path):
    # Get hash of repo state (HEAD commit, last modified)
    result = subprocess.run(
        ['git', 'rev-parse', 'HEAD'],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

cache_key = f"{branch_name}_{get_repo_state_hash(repo_path)}"
```

**Test:** Modify repo, verify cache is invalidated and fresh results returned

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
