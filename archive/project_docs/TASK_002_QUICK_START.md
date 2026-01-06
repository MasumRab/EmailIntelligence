# Task 002: Branch Clustering System - Quick Start

**Status:** Ready to implement  
**Location:** `tasks/task_002.md` and `tasks/task_002-clustering.md`  
**Effort:** 136-176 hours (3-4 weeks)  
**Parallelizable:** Yes (recommended)

---

## What to Build (5 minutes)

A system that analyzes git branches and clusters them by similarity using three stages:

1. **Analyze** (tasks 002.1-002.3): Extract metrics from each branch
   - CommitHistoryAnalyzer: commit patterns, recency, authorship
   - CodebaseStructureAnalyzer: directory/file structure similarity
   - DiffDistanceCalculator: code changes and risk assessment

2. **Cluster** (task 002.4): Group similar branches using hierarchical clustering

3. **Assign** (task 002.5): Assign integration targets (main/scientific/orchestration-tools) and generate 30+ descriptive tags

---

## 3 Execution Options (Choose One)

### Option A: Full Parallel ⭐ RECOMMENDED (3 weeks)

**Best for:** Team with 5+ people

```
Week 1 (Parallel):
  Team A → Task 002.1 (CommitHistoryAnalyzer)
  Team B → Task 002.2 (CodebaseStructureAnalyzer)
  Team C → Task 002.3 (DiffDistanceCalculator)

Week 2:
  Team D → Task 002.4 (BranchClusterer)

Week 3:
  Team E → Task 002.5 (IntegrationTargetAssigner)
  All → Integration testing + performance tuning
```

**Files to read:**
- tasks/task_002.md (Execution Strategies section)
- tasks/task_002-clustering.md (Execution Strategies & Timeline)

### Option B: Sequential (4 weeks)

**Best for:** 1-2 person team

Follow order: 002.1 → 002.2 → 002.3 → 002.4 → 002.5

Each person/team completes tasks in sequence, allowing previous outputs to be used by next task.

### Option C: Hybrid (3.5 weeks)

**Best for:** 3-4 person team

```
Weeks 1-2: Sequential 002.1 → 002.2 → 002.3
Weeks 2-3: Parallel 002.4 + 002.5 + testing
```

---

## 5-Step Implementation Plan

### Step 1: Setup (15 minutes)
```bash
# Clone repo, navigate to project root
cd /home/masum/github/PR/.taskmaster

# Create feature branch
git checkout -b feat/task-002-clustering

# Create directories
mkdir -p src/analyzers
mkdir -p config
mkdir -p tests/analyzers

# Create __init__.py files
touch src/analyzers/__init__.py
touch tests/analyzers/__init__.py
```

### Step 2: Read Documentation (1 hour)
```bash
# Quick overview (5 min)
cat tasks/task_002.md | head -100

# Full details for your task (20 min)
# If doing 002.1: grep -A 200 "^### Task 002.1:" tasks/task_002.md
# If doing 002.2: grep -A 200 "^### Task 002.2:" tasks/task_002.md
# etc.

# Implementation guide (30 min)
cat tasks/task_002-clustering.md | grep -A 300 "^## Subtask 002.X"
```

### Step 3: Implement Sub-subtasks (Varies by task)

**Example for Task 002.1 (CommitHistoryAnalyzer):**

```bash
# 002.1.1: Design Metric System (2-3 hours)
# - Read tasks/task_002-clustering.md § "Subtask 002.1: CommitHistoryAnalyzer"
# - Define 5 metrics with formulas
# - Create normalization approach
# - Document weighting scheme

# 002.1.2: Set Up Git Data Extraction (4-5 hours)
# - Implement subprocess-based git command execution
# - Create branch validation
# - Extract commit metadata

# ... continue through 002.1.8
```

**Each sub-subtask follows pattern:**
1. Read description and success criteria
2. Check "Key Implementation Notes"
3. Review code examples
4. Implement code
5. Write unit tests
6. Verify success criteria
7. Commit with clear message

### Step 4: Testing (Continuous)

```bash
# During implementation - run tests after each sub-subtask
pytest tests/analyzers/test_YOUR_TASK.py -v --cov

# Target metrics:
# - Code coverage: >95%
# - Performance: <2s per branch (varies by task)
# - All success criteria met

# Full pipeline test (after all 5 tasks complete)
pytest tests/test_full_pipeline.py -v
```

### Step 5: Integration & Code Review

```bash
# Merge to main after:
# - All unit tests passing (>95% coverage)
# - Integration tests passing
# - Code review approved
# - Performance benchmarks met

git commit -m "feat: implement Task 002.X - [ComponentName]"
git push origin feat/task-002-clustering
# Create PR for code review
```

---

## Task-Specific Quick References

### Task 002.1: CommitHistoryAnalyzer
**What it does:** Extract commit patterns and score branch maturity  
**Effort:** 24-32 hours  
**Complexity:** 7/10  
**Key metrics:** recency, frequency, authorship, merge-readiness, stability  
**Performance target:** <2s per branch  
**Sub-subtasks:** 8 (design → git extraction → 5 metrics → aggregation → tests)

**Quick implementation checklist:**
- [ ] Design 5 metrics with formulas
- [ ] Implement git command execution with 30s timeout
- [ ] Create recency metric (exponential decay)
- [ ] Create frequency metric (commits per day, avoid div-by-zero)
- [ ] Create authorship metric (unique authors)
- [ ] Create merge-readiness metric (commits behind main)
- [ ] Create stability metric (commit pattern consistency)
- [ ] Implement weighted aggregation
- [ ] Write 8+ unit tests
- [ ] Performance: <2s per branch

### Task 002.2: CodebaseStructureAnalyzer
**What it does:** Measure directory/file structure similarity  
**Effort:** 28-36 hours  
**Complexity:** 7/10  
**Key metrics:** directory similarity (Jaccard), file additions, core module stability, namespace isolation  
**Performance target:** <2s per branch  
**Sub-subtasks:** 8 (design → git extraction → 4 metrics → aggregation → tests)

**Quick implementation checklist:**
- [ ] Design structure analysis with Jaccard similarity
- [ ] Implement `git ls-tree` extraction
- [ ] Extract directory sets from file paths
- [ ] Create directory similarity metric (Jaccard)
- [ ] Create file additions metric (inverted)
- [ ] Create core module stability metric
- [ ] Create namespace isolation metric
- [ ] Implement weighted aggregation
- [ ] Write 8+ unit tests
- [ ] Performance: <2s per branch

### Task 002.3: DiffDistanceCalculator
**What it does:** Analyze code diffs and compute distance metrics  
**Effort:** 32-40 hours  
**Complexity:** 8/10  
**Key metrics:** code churn, change concentration, diff complexity, integration risk  
**Performance target:** <3s per branch  
**Sub-subtasks:** 8 (design → diff extraction → 4 metrics → aggregation → tests)

**Quick implementation checklist:**
- [ ] Define 4 metrics and risk categories
- [ ] Implement `git diff --numstat` parsing
- [ ] Handle binary files gracefully
- [ ] Create code churn metric (lines changed ratio)
- [ ] Create change concentration metric
- [ ] Create diff complexity metric
- [ ] Create integration risk metric (pattern-based)
- [ ] Implement weighted aggregation
- [ ] Write 8+ unit tests
- [ ] Performance: <3s per branch

### Task 002.4: BranchClusterer
**What it does:** Combine metrics and perform hierarchical clustering  
**Effort:** 28-36 hours  
**Complexity:** 8/10  
**Key algorithm:** Ward linkage hierarchical agglomerative clustering  
**Quality metrics:** Silhouette, Davies-Bouldin, Calinski-Harabasz  
**Performance target:** <10s for 50+ branches  
**Sub-subtasks:** 8 (design → combine metrics → distance matrix → clustering → quality metrics → output → tests)

**Quick implementation checklist:**
- [ ] Design clustering architecture (Ward linkage, Euclidean distance)
- [ ] Implement metric combination (0.35×002.1 + 0.35×002.2 + 0.30×002.3)
- [ ] Compute distance matrix (pairwise Euclidean distances)
- [ ] Perform hierarchical clustering with Ward linkage
- [ ] Generate dendrogram
- [ ] Compute silhouette score
- [ ] Compute Davies-Bouldin index
- [ ] Compute Calinski-Harabasz index
- [ ] Format cluster output
- [ ] Write 8+ unit tests
- [ ] Performance: <10s for 50 branches

### Task 002.5: IntegrationTargetAssigner
**What it does:** Assign targets (main/scientific/orchestration-tools) and generate 30+ tags  
**Effort:** 24-32 hours  
**Complexity:** 7/10  
**Decision levels:** 4-level hierarchy (heuristic → affinity → consensus → default)  
**Output:** Target assignment + 30+ tags across 6 categories  
**Performance target:** <1s per branch  
**Sub-subtasks:** 8 (design → heuristics → tags → affinity → confidence → reasoning → output → tests)

**Quick implementation checklist:**
- [ ] Design 4-level decision hierarchy
- [ ] Implement heuristic rule engine
- [ ] Create tag generation system (6 categories, 30+ tags)
- [ ] Implement affinity scoring to archetypes
- [ ] Implement confidence scoring (weighted factors)
- [ ] Generate human-readable reasoning
- [ ] Format assignment output
- [ ] Write 8+ unit tests
- [ ] Generate 30+ tags per branch
- [ ] Performance: <1s per branch

---

## Key Success Metrics

### Performance Targets
| Component | Target | Memory |
|-----------|--------|--------|
| 002.1 | <2s per branch | <50 MB |
| 002.2 | <2s per branch | <50 MB |
| 002.3 | <3s per branch | <100 MB |
| 002.4 | <10s for 50 branches | <100 MB |
| 002.5 | <1s per branch | <50 MB |
| **Full pipeline** | **<120s for 13 branches** | **<100 MB** |

### Code Quality
- [ ] Unit test coverage: >95%
- [ ] All success criteria met for each task
- [ ] Code follows PEP 8
- [ ] Comprehensive docstrings
- [ ] Edge cases handled gracefully
- [ ] All metrics in [0,1] range (normalized)
- [ ] No NaN or infinite values
- [ ] Integration tests passing

---

## Documentation Resources

**Always available:**
- `tasks/task_002.md` - Full task specification and success criteria
- `tasks/task_002-clustering.md` - Detailed implementation guide
- `TASK_002_MIGRATION_COMPLETE.md` - Context and history
- `TASK_75_CLEANUP_AND_RENUMBERING_PLAN.md` - Architecture rationale

**During implementation:**
- Each sub-subtask has "Key Implementation Notes"
- Code examples and patterns
- Common gotchas and solutions
- Configuration templates (YAML)
- Testing strategy

---

## Common Gotchas (Don't Get Stuck!)

**Timeout Issues?**
```python
# Always add timeout to subprocess calls
result = subprocess.run(cmd, timeout=30, ...)
```

**Metrics outside [0,1]?**
```python
# Clamp all metrics
metric = max(0.0, min(1.0, metric))
```

**Division by zero?**
```python
# Check denominators
if days == 0: days = 1
if total_files == 0: return 0.5
```

**Too few clusters?**
```python
# Ensure minimum cluster count
if len(unique_clusters) < 2:
    clusters = fcluster(Z, t=5, criterion='maxclust')
```

**Need more examples?**
→ See tasks/task_002-clustering.md § "Common Gotchas & Solutions"

---

## Get Started Now

1. **Choose your team/strategy** (Full Parallel recommended)
2. **Create feature branch**
   ```bash
   git checkout -b feat/task-002-clustering
   ```
3. **Read task overview**
   ```bash
   cat tasks/task_002.md
   ```
4. **Read your specific task**
   ```bash
   cat tasks/task_002-clustering.md | grep -A 500 "^## Subtask 002.X"
   ```
5. **Start implementing** (follow sub-subtask checklist)
6. **Test continuously** (unit tests after each sub-subtask)
7. **Integrate & review** (PR when all tests pass)

---

## Getting Help

**Questions about the task?**
→ Check tasks/task_002.md § "Success Criteria" and "Architecture"

**Stuck on implementation?**
→ Check tasks/task_002-clustering.md § "Subtask X" for that component

**Performance issues?**
→ Check "Performance Targets" section in relevant sub-subtask

**Edge cases?**
→ Check tasks/task_002-clustering.md § "Common Gotchas & Solutions"

**General context?**
→ Check TASK_002_MIGRATION_COMPLETE.md for history and rationale

---

**Ready to build something great? Let's go! 🚀**

Task 002: Branch Clustering System - Phase 1

Start with either:
- Task 002.1 (CommitHistoryAnalyzer) - Simplest entry point
- Task 002.2 (CodebaseStructureAnalyzer) - Moderate complexity
- Task 002.3 (DiffDistanceCalculator) - Most complex analyzer

All can start in parallel - no dependencies until Task 002.4!
