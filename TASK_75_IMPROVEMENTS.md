# Task 75 Files - Specific Improvement Opportunities

**Date:** January 4, 2026  
**Based on:** Analysis of Task 75 files, archived HANDOFF files, and comparison with branch alignment tasks  
**Goal:** Enhance Task 75 files to be even more developer-friendly

---

## Executive Summary

Task 75 files are **excellent** but can be improved in 8 key areas:

1. **Navigation & TOC** - Long files (400-650 lines) need better in-file navigation
2. **Subtask Sequencing** - Missing step-sequence within individual subtasks
3. **Performance Baselines** - Need concrete metrics for "done"
4. **Git Workflow Examples** - Show exact step-by-step git sequences
5. **Common Gotchas** - Extract patterns from HANDOFF files about what breaks
6. **Configuration Externalizing** - Some configs still hardcoded in HANDOFF
7. **Integration Bridges** - Explicit hand-off points to downstream tasks
8. **Quick Reference Cards** - One-page per-task cheat sheets

---

## Current Strengths (Keep These)

✅ **Developer Quick Reference section** - Essential and well-done  
✅ **Implementation Checklists** - Practical and detailed  
✅ **Test Case Examples** - Concrete with expected outputs  
✅ **Technical Reference section** - Git commands, code patterns  
✅ **Metadata** - Clear ID, Status, Priority, Effort  
✅ **Dependencies clearly marked** - What blocks what  
✅ **Success Criteria** - Quantified and measurable  

---

## Improvement 1: Add Table of Contents & Section Navigation

### Current Issue
Long files (446-642 lines) require scrolling. No quick way to jump to specific sections.

### Solution
Add auto-indexed TOC at top + section anchors.

### Example for task-75.1.md (after Metadata section):

```markdown
## Quick Navigation
- [Purpose](#purpose)
- [Developer Quick Reference](#developer-quick-reference)
- [Success Criteria](#success-criteria)
- [Subtasks Overview](#subtasks-overview) ← New
- [Subtask Details](#subtasks)
- [Configuration](#configuration-parameters)
- [Technical Reference](#technical-reference)
- [Integration Checkpoint](#integration-checkpoint)
- [Done Definition](#done-definition)

**Pro tip:** Jump to section with Ctrl+F search
```

### Impact
- 30 seconds to find any section
- Better for skimming
- Mobile-friendly navigation

### Files to Update
All 9 task files: task-75.1.md through task-75.9.md

---

## Improvement 2: Add Subtask Sequencing & Order Dependencies

### Current Issue
Subtasks shown in order but dependencies are only listed in each subtask. No visual "critical path".

### Solution
Add "Subtasks Overview" section showing:
- Which subtasks can run in parallel
- Critical path (tasks that block others)
- Estimated timeline with dependencies

### Example Addition (after Success Criteria):

```markdown
## Subtasks Overview

### Dependency Flow
```
75.1.1 (2-3h) ────┐
                  ├─→ 75.1.2 (4-5h) ────┐
                                         ├─→ 75.1.3-75.1.6 (parallel) ────┐
                  (No deps)              │
75.1.1 (2-3h) ────┴─────────────────────┘

Parallel = {75.1.3, 75.1.4, 75.1.5, 75.1.6} after 75.1.2
Critical path = 75.1.1 → 75.1.2 → [parallel] → 75.1.7 → 75.1.8
Total sequential: 24-32 hours
```

### Pro Format
```markdown
### Parallel Opportunities
- **Can run in parallel:** 75.1.3, 75.1.4, 75.1.5, 75.1.6
  (All depend only on 75.1.1 & 75.1.2, independent of each other)
  
- **Must be sequential:** 75.1.1 → 75.1.2 → 75.1.7 → 75.1.8
  (Each blocks the next)

### Timeline with Dependencies
- Day 1-2: 75.1.1 (metric design)
- Day 2-3: 75.1.2 (git extraction)
- Day 3-4: Run 75.1.3, 75.1.4, 75.1.5, 75.1.6 in parallel
- Day 4-5: 75.1.7 (aggregation)
- Day 5-6: 75.1.8 (testing)
```

### Impact
- Developers understand critical path immediately
- Enables better task scheduling
- Shows parallelization opportunities
- Realistic timeline planning

### Files to Update
task-75.1.md through task-75.9.md (all 9)

---

## Improvement 3: Add Performance Baselines to Success Criteria

### Current Issue
Success criteria are qualitative ("Output matches specification") - missing quantitative targets.

### Solution
Add measurable performance targets in Success Criteria.

### Example Addition to task-75.1.md Success Criteria:

```markdown
**Performance Targets:**
- [ ] Single branch analysis: < 2 seconds (typical 500-commit repo)
- [ ] Memory usage: < 50 MB per analysis
- [ ] Handle repos with 10,000+ commits
- [ ] Metric computation: O(n) where n = commit count
- [ ] Git command timeout: 30 seconds max
```

### Where This Helps
- Developers know exact targets before coding
- Easy to validate completion with benchmarks
- Prevents "good enough" implementations
- Clear DoD (Definition of Done)

### Additional: Performance Validation Checklist

```markdown
**Performance Validation (Subtask 75.1.8):**
- [ ] Run test on repo with 100 commits → < 1s
- [ ] Run test on repo with 1,000 commits → < 2s
- [ ] Run test on repo with 10,000+ commits → < 5s
- [ ] Confirm memory never exceeds 50 MB
- [ ] Profile code for bottlenecks
```

### Files to Update
All 9 task files (add to Success Criteria section)

---

## Improvement 4: Add Exact Git Workflow Examples (Step-by-Step)

### Current Issue
Git commands listed individually. Missing: "Here's the exact sequence a developer should run."

### Solution
Add "Typical Development Workflow" section showing copy-paste sequences.

### Example Addition to task-75.1.md (after Technical Reference):

```markdown
## Typical Development Workflow

### Setting Up Your Branch
```bash
# 1. Create feature branch
git checkout -b feat/commit-history-analyzer
git push -u origin feat/commit-history-analyzer

# 2. Create initial file structure
mkdir -p src/analyzers
touch src/analyzers/commit_history_analyzer.py
touch src/analyzers/__init__.py
git add src/analyzers/
git commit -m "chore: create analyzer module structure"
```

### Subtask 75.1.1: Metric Design Workflow
```bash
# Document metrics in design doc
cat > METRIC_DESIGN.md << 'EOF'
# Metrics for CommitHistoryAnalyzer

## Metric 1: commit_recency
Formula: exp(-(days_since_last / 30))
Range: [0, 1]
EOF

git add METRIC_DESIGN.md
git commit -m "docs: define metric system for 75.1.1"
```

### Subtask 75.1.2: Git Extraction Workflow
```bash
# Create git utility module
cat > src/analyzers/git_utils.py << 'EOF'
import subprocess

def get_commits(repo_path, branch_name):
    cmd = ['git', 'log', f'main..{branch_name}', 
           '--pretty=format:%H|%ai|%an|%s']
    result = subprocess.run(cmd, cwd=repo_path, 
                          capture_output=True, text=True)
    return result.stdout.split('\n')
EOF

git add src/analyzers/git_utils.py
git commit -m "feat: implement git data extraction for 75.1.2"
```

### Subtask 75.1.3-75.1.5: Parallel Implementation
```bash
# Create metric computation modules
touch src/analyzers/metrics_recency.py
touch src/analyzers/metrics_frequency.py
touch src/analyzers/metrics_authorship.py
touch src/analyzers/metrics_stability.py
touch src/analyzers/metrics_merge_readiness.py

git add src/analyzers/metrics_*.py
git commit -m "feat: create metric computation modules (75.1.3-75.1.5)"
```

### Subtask 75.1.7: Aggregation Workflow
```bash
# Create aggregation module
cat > src/analyzers/aggregator.py << 'EOF'
def aggregate_metrics(metrics_dict, weights):
    """Combine individual metrics into aggregate score."""
    total = sum(metrics_dict[k] * weights[k] 
                for k in metrics_dict.keys())
    return min(1.0, max(0.0, total))  # Clamp to [0,1]
EOF

git add src/analyzers/aggregator.py
git commit -m "feat: implement metric aggregation for 75.1.7"
```

### Subtask 75.1.8: Testing Workflow
```bash
# Create test file with test cases
mkdir -p tests/analyzers
cat > tests/analyzers/test_commit_history_analyzer.py << 'EOF'
import pytest
from src.analyzers import CommitHistoryAnalyzer

def test_normal_branch():
    """Test typical branch with 42 commits."""
    analyzer = CommitHistoryAnalyzer(repo_path="/path/to/repo")
    result = analyzer.analyze("feature/example")
    assert result['aggregate_score'] > 0.5
    assert 'metrics' in result
EOF

git add tests/analyzers/
git commit -m "test: add unit tests for CommitHistoryAnalyzer (75.1.8)"
```

### Final Push
```bash
# When all subtasks complete
git log --oneline | head -10  # Verify commits

# Create summary commit
git commit --allow-empty -m "feat: Task 75.1 CommitHistoryAnalyzer complete

- 75.1.1: Metric system defined
- 75.1.2: Git extraction implemented
- 75.1.3: Recency metric implemented
- 75.1.4: Frequency metric implemented
- 75.1.5: Authorship & stability metrics implemented
- 75.1.6: Merge readiness metric implemented
- 75.1.7: Metrics aggregation implemented
- 75.1.8: Unit tests (>95% coverage) complete

All success criteria met. Ready for 75.4 (BranchClusterer)."

git push origin feat/commit-history-analyzer
```

### Impact
- Copy-paste ready sequences
- Developers don't have to invent git workflow
- Consistent commit messages across team
- Clear milestone markers
- Safer (less chance of git accidents)

### Files to Update
All 9 task files (add "Typical Development Workflow" section)

---

## Improvement 5: Add "Common Gotchas" & Edge Cases

### Current Issue
Edge cases mentioned but scattered. Missing: What actually breaks in practice?

### Solution
Extract patterns from HANDOFF files and create "Gotchas" section.

### Example Addition to task-75.1.md (before Done Definition):

```markdown
## Common Gotchas & How to Avoid Them

### Gotcha 1: Git Timeout on Large Repos
**Problem:** `subprocess.run()` hangs on repos with 10,000+ commits
**Solution:** Always set timeout=30
```python
subprocess.run(cmd, timeout=30, capture_output=True)
```
**Test:** Try with `orchestration-tools` branch (15k+ commits)

---

### Gotcha 2: Merge Base Not Found
**Problem:** Orphaned branches have no merge base with main
**Solution:** Handle gracefully, return default metrics
```python
try:
    merge_base = subprocess.run(['git', 'merge-base', 'main', branch], 
                               timeout=30, capture_output=True, text=True)
    if not merge_base.stdout.strip():
        # Orphaned branch - use defaults
        commits_behind = float('inf')
except subprocess.TimeoutExpired:
    commits_behind = float('inf')
```

---

### Gotcha 3: Single Commit Branches Cause Division by Zero
**Problem:** Frequency = commits / days, but single-commit branches have < 1 day
**Solution:** Add minimum values
```python
days_active = max(1, (last_commit_date - first_commit_date).days)
frequency = commits / days_active
```

---

### Gotcha 4: Binary Files Cause Line Count Errors
**Problem:** `git diff --stat` shows binary files as "Bin X -> Y bytes"
**Solution:** Skip binary files in stability calculation
```python
lines_changed = 0
for line in diff_output.split('\n'):
    if 'Bin' not in line:  # Skip binary files
        # Parse lines from "file.py | 42 +++++---"
```

---

### Gotcha 5: Author Names Have Encoding Issues
**Problem:** Author names from `git log` can have non-ASCII characters
**Solution:** Handle UTF-8 explicitly
```python
result = subprocess.run(cmd, capture_output=True, 
                       text=True, encoding='utf-8')
```

---

### Gotcha 6: Recency Metric Breaks with Future Dates
**Problem:** Developer commits with wrong system clock → negative days
**Solution:** Cap at 0
```python
days_since = max(0, (now - last_commit_date).days)
recency = math.exp(-days_since / 30)
```

---

### Gotcha 7: Metric Normalization Produces NaN
**Problem:** Division by zero in normalization
**Solution:** Clamp all intermediate results
```python
def safe_normalize(value, baseline):
    if baseline == 0:
        return 0.0
    ratio = value / baseline
    return min(1.0, max(0.0, ratio))
```
```

### Testing Gotchas
```markdown
### Gotcha 8: Test Fixtures Need Real Commits
**Problem:** Mocking git commands makes tests brittle
**Solution:** Use test repository with actual commits
- Create `tests/fixtures/test_repo.git` (minimal but real)
- Run tests against real repo
- Faster than actual repos, more realistic than mocks

---

### Gotcha 9: Performance Tests Fail on Slow Disks
**Problem:** SSD vs HDD performance varies 10x
**Solution:** Test relative performance, not absolute
```python
# Bad: assert seconds < 2.0
# Good: assert seconds < baseline_seconds * 1.5
```
```

### Impact
- Developers avoid expensive mistakes
- Faster debugging when tests fail
- Confidence in edge case handling
- Better error messages in code

### Files to Update
All 9 task files (add "Common Gotchas" section before "Done Definition")

---

## Improvement 6: Extract Configuration Constants

### Current Issue
Some configs still in HANDOFF files. Configuration scattered across sections.

### Solution
Create dedicated "Configuration & Defaults" section with ALL tunable parameters.

### Example Addition to task-75.1.md:

```markdown
## Configuration & Defaults

### Required Configuration Parameters
Store in `config/analyzers.yaml`:

```yaml
commit_history_analyzer:
  # Metric weights (sum = 1.0)
  metric_weights:
    commit_recency: 0.25
    commit_frequency: 0.20
    authorship_diversity: 0.20
    merge_readiness: 0.20
    stability_score: 0.15
  
  # Time windows and baselines
  recency_window_days: 30
  frequency_baseline_commits_per_week: 5
  stability_baseline_lines_per_commit: 50
  merge_readiness_max_commits_behind: 50
  
  # Git command settings
  git_command_timeout_seconds: 30
  git_max_commits_for_stats: 10000
  
  # Edge case handling
  min_branch_age_days: 0
  max_divergence_for_simple: 0.1
  max_conflict_probability_for_simple: 0.1
```

### Loading in Code
```python
import yaml

def load_config():
    with open('config/analyzers.yaml') as f:
        config = yaml.safe_load(f)
    return config['commit_history_analyzer']

config = load_config()
RECENCY_WEIGHT = config['metric_weights']['commit_recency']
RECENCY_WINDOW_DAYS = config['recency_window_days']
```

### Why This Matters
- ✅ Easy to tune without code changes
- ✅ Different environments can override values
- ✅ Clear all tunable parameters in one place
- ✅ Easy to compare across Task 75.1-75.9
- ✅ Production vs. test configs separate

### Default Values Reference
```markdown
### Recommended Defaults (Tested)

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| `commit_recency` weight | 0.25 | Recent activity is important indicator |
| `recency_window_days` | 30 | Standard sprint length |
| `frequency_baseline` | 5 commits/week | Active development baseline |
| `git_command_timeout` | 30 seconds | Protects against hanging on large repos |
| `merge_readiness_max_behind` | 50 commits | Practical sync point |
```
```

### Files to Update
task-75.1.md through task-75.9.md (add explicit "Configuration & Defaults")

---

## Improvement 7: Add Integration Handoff Points

### Current Issue
Success Criteria show when task is done, but not explicitly what gets handed off.

### Solution
Add "Integration Handoff" section showing:
- What artifact/class is produced
- How downstream tasks consume it
- Example usage code

### Example for task-75.1.md:

```markdown
## Integration Handoff

### Output Artifact
**Class:** `CommitHistoryAnalyzer`  
**Location:** `src/analyzers/commit_history_analyzer.py`  
**Responsibility:** Analyze individual branch commit history

### How Task 75.4 Consumes This
Task 75.4 (BranchClusterer) will import and use:

```python
from src.analyzers import CommitHistoryAnalyzer

class BranchClusterer:
    def __init__(self):
        self.commit_analyzer = CommitHistoryAnalyzer(
            repo_path=self.repo_path
        )
    
    def analyze_branches(self, branches):
        # For each branch, get commit history metrics
        for branch in branches:
            commit_metrics = self.commit_analyzer.analyze(branch)
            # → passes to 75.2 & 75.3, then combined in 75.4
```

### Validation Before Handoff
Before moving to Task 75.4, ensure:
- [ ] `CommitHistoryAnalyzer.analyze()` returns valid dict
- [ ] All metrics in [0, 1] range (test with validators)
- [ ] Performance: < 2 seconds per branch
- [ ] Example output matches spec exactly

### What Task 75.2 & 75.3 Need
They will produce similar outputs:
- `CodebaseStructureAnalyzer.analyze()` → dict with codebase metrics
- `DiffDistanceCalculator.analyze()` → dict with diff metrics

All three feed into Task 75.4 which combines them.

### Integration Timeline
```
Week 1: Task 75.1-75.3 complete independently
Week 2: Hand off to Task 75.4 (BranchClusterer)
       Task 75.4 integrates all 3 analyzers
```
```

### Files to Update
All 9 task files (add "Integration Handoff" section)

---

## Improvement 8: Create One-Page Quick Reference Cards

### Current Issue
Long task files are hard to print or post on desk.

### Solution
Create single-page cheat sheet for each task.

### Example: task-75.1-QUICK-REFERENCE.md

```markdown
# Task 75.1: CommitHistoryAnalyzer - Quick Reference

## What to Build
Python class analyzing branch commit history with 5 metrics → aggregate score.

## Class & Methods
```python
class CommitHistoryAnalyzer:
    def __init__(self, repo_path: str, main_branch: str = "main")
    def analyze(self, branch_name: str) -> dict
```

## 5 Metrics (All [0,1])
1. **commit_recency** (25%) - Recent commits weighted higher
2. **commit_frequency** (20%) - Activity velocity (commits/day)
3. **authorship_diversity** (20%) - Unique authors / total commits
4. **merge_readiness** (20%) - Commits since merge base with main
5. **stability_score** (15%) - Inverse of churn (lines changed/commit)

## Key Git Commands
```bash
git log main..BRANCH --pretty=format:"%H|%ai|%an|%s"
git merge-base main BRANCH
git log -1 --format=%ai BRANCH
```

## 8 Subtasks (24-32 hours total)
| Subtask | Effort | Prerequisites | Parallelizable |
|---------|--------|---------------|-----------------|
| 75.1.1: Design metrics | 2-3h | None | - |
| 75.1.2: Git extraction | 4-5h | 75.1.1 | No (blocks 75.1.3-6) |
| 75.1.3: Recency metric | 3-4h | 75.1.2 | **Yes (with 75.1.4-6)** |
| 75.1.4: Frequency metric | 3-4h | 75.1.2 | **Yes (with 75.1.3,5-6)** |
| 75.1.5: Auth & stability | 4-5h | 75.1.2 | **Yes (with 75.1.3-4,6)** |
| 75.1.6: Merge readiness | 3-4h | 75.1.2 | **Yes (with 75.1.3-5)** |
| 75.1.7: Aggregation | 2-3h | 75.1.3-6 | No |
| 75.1.8: Unit tests | 3-4h | 75.1.7 | - |

## Output Format
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

## Success Criteria (Checklist)
- [ ] All 5 metrics computed correctly
- [ ] All metrics in [0, 1] range
- [ ] Aggregate = 0.25*m1 + 0.20*m2 + 0.20*m3 + 0.20*m4 + 0.15*m5
- [ ] < 2 seconds per branch analysis
- [ ] 8 unit tests, >95% coverage
- [ ] Handles edge cases: new/old/single-commit/stale branches

## Configuration
```yaml
commit_recency_weight: 0.25
commit_frequency_weight: 0.20
authorship_diversity_weight: 0.20
merge_readiness_weight: 0.20
stability_score_weight: 0.15
recency_window_days: 30
frequency_baseline_commits_per_week: 5
stability_baseline_lines_per_commit: 50
merge_readiness_max_commits_behind: 50
git_command_timeout_seconds: 30
```

## Common Gotchas
1. **Git timeout on large repos** → Set timeout=30
2. **Merge base not found** → Handle orphaned branches gracefully
3. **Single-commit branches** → Avoid division by zero
4. **Binary files in stats** → Skip in line counting
5. **Future dates** → Cap days_since at 0
6. **NaN from normalization** → Clamp intermediate results

## Development Workflow (Copy-Paste Ready)
```bash
# 1. Setup
git checkout -b feat/commit-history-analyzer
mkdir -p src/analyzers && touch src/analyzers/commit_history_analyzer.py

# 2. Subtask 75.1.1 (Design)
cat > METRIC_DESIGN.md << 'EOF'
# Metrics
EOF
git add METRIC_DESIGN.md && git commit -m "docs: metric design"

# 3. Subtask 75.1.2 (Git extraction)
# ... (implement git_utils.py)
git add src/analyzers/git_utils.py && git commit -m "feat: git extraction"

# 4. Subtasks 75.1.3-6 (Metrics - parallel)
# ... (implement 5 metric modules)
git add src/analyzers/metrics_*.py && git commit -m "feat: metrics (75.1.3-6)"

# 5. Subtask 75.1.7 (Aggregation)
# ... (implement aggregator.py)
git add src/analyzers/aggregator.py && git commit -m "feat: aggregation"

# 6. Subtask 75.1.8 (Tests)
# ... (implement test_commit_history_analyzer.py)
git add tests/ && git commit -m "test: unit tests (>95% coverage)"

# 7. Final
git push origin feat/commit-history-analyzer
```

## Hands To: Task 75.4 (BranchClusterer)
When complete, CommitHistoryAnalyzer is imported by:
```python
from src.analyzers import CommitHistoryAnalyzer
analyzer = CommitHistoryAnalyzer(repo_path)
metrics = analyzer.analyze(branch_name)  # Used in 75.4
```

## Files
- Implementation: `src/analyzers/commit_history_analyzer.py`
- Tests: `tests/analyzers/test_commit_history_analyzer.py`
- Config: `config/analyzers.yaml`
```

### How to Create
1. Read full task-75.X.md
2. Extract key info into 1-page format
3. Include all success criteria as checklist
4. Add development workflow (copy-paste ready)
5. Keep metrics/config reference

### Create Using Template
```bash
for i in {1..9}; do
  cp QUICK_REFERENCE_TEMPLATE.md task-75.$i-QUICK-REFERENCE.md
  # Fill in task-specific info
done
```

### Impact
- Print and post on desk
- Share with team via Slack
- Quick validation before starting
- Easy to verify completion
- One-screen overview

### Files to Create
task-75.1-QUICK-REFERENCE.md through task-75.9-QUICK-REFERENCE.md

---

## Implementation Priority & Effort

### Must-Have (High Impact, Low Effort)
| Improvement | Files | Effort | Impact |
|-------------|-------|--------|--------|
| Add TOC & Navigation | 9 files | 2 hours | Huge (findability) |
| Add Performance Baselines | 9 files | 3 hours | High (clarity) |
| Add Common Gotchas | 9 files | 4 hours | High (debugging) |
| Extract Configuration | 9 files | 3 hours | High (flexibility) |

**Total: ~12 hours → Massive clarity improvement**

### Should-Have (Medium Impact, Medium Effort)
| Improvement | Files | Effort | Impact |
|-------------|-------|--------|--------|
| Add Subtask Sequencing | 9 files | 5 hours | Medium (planning) |
| Add Git Workflows | 9 files | 6 hours | Medium (confidence) |
| Add Integration Handoff | 9 files | 3 hours | Medium (clarity) |

**Total: ~14 hours → Better execution planning**

### Nice-to-Have (Medium Impact, Low Effort)
| Improvement | Files | Effort | Impact |
|-------------|-------|--------|--------|
| Create Quick References | 9 new files | 5 hours | Medium (desk reference) |

---

## Suggested Rollout

### Week 1: Must-Haves
- [ ] Add TOC & Navigation to all 9 files
- [ ] Add Performance Baselines to Success Criteria
- [ ] Add Common Gotchas sections
- [ ] Extract all Configuration constants

**Result:** Significantly clearer, more actionable files

### Week 2: Should-Haves  
- [ ] Add Subtask Sequencing diagrams
- [ ] Add step-by-step Git Workflow examples
- [ ] Add Integration Handoff sections

**Result:** Better execution, fewer surprises

### Week 3: Nice-to-Haves
- [ ] Create Quick Reference cards (1 per task)
- [ ] Print and distribute

**Result:** Easy desk reference, faster onboarding

---

## Example Changes Summary

### Before (Current task-75.1.md)
```
✓ Purpose
✓ Developer Quick Reference
✓ Success Criteria (qualitative)
✓ Subtasks with steps
✓ Configuration Parameters
✓ Technical Reference
✓ Integration Checkpoint
✓ Done Definition
- NO navigation (400+ lines)
- NO performance targets
- NO common pitfalls
- NO git workflow examples
- NO subtask dependencies diagram
```

### After (Enhanced task-75.1.md)
```
✓ Quick Navigation (jump to sections)
✓ Purpose
✓ Developer Quick Reference
✓ Success Criteria (quantitative + baselines)
✓ Subtasks Overview (dependencies + parallel opportunities)
✓ Subtasks with steps + gotchas
✓ Configuration & Defaults (YAML)
✓ Technical Reference + Git Workflows
✓ Common Gotchas & Solutions
✓ Integration Handoff (what gets passed to 75.4)
✓ Integration Checkpoint
✓ Done Definition
```

### Result
- **Better clarity:** Know exactly what to do
- **Better planning:** Understand dependencies
- **Better execution:** Copy-paste workflows
- **Better debugging:** Know what breaks and why
- **Better integration:** Know what to hand off

---

## Quick Links to Implement

**Create Template Documents:**
1. `QUICK_REFERENCE_TEMPLATE.md` (for quick reference cards)
2. `SUBTASK_SEQUENCING_TEMPLATE.md` (for dependency diagrams)
3. `GIT_WORKFLOW_TEMPLATE.md` (for workflow examples)

**Then apply to each task-75.X.md file:**
- Add sections from templates
- Customize for specific task
- Validate completeness

---

## Bottom Line

Task 75 files are **80% there**. These 8 improvements take them to **95%+ developer-friendly**.

**Most impactful improvements:**
1. Add TOC (30 seconds to find any section)
2. Add Performance Baselines (clear DoD)
3. Add Common Gotchas (avoid expensive mistakes)
4. Add Git Workflows (copy-paste ready code)

These 4 alone would transform developer experience from "pretty good" to "excellent."
