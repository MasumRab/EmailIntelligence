# Task 002: Branch Clustering System - Sequential Execution Framework

**Clean ID:** 002  
**Original ID:** Task 75  
**Status:** Restructured for Early Sequential Execution  
**Timeline:** 6-8 weeks (sequential) | 4-6 weeks (parallel-ready)  
**Priority:** High  
**Parallelizable:** Yes (Stage One after Week 2)

---

## Overview

Task 002 is restructured to support **early sequential execution** while maintaining parallel capabilities later. The key insight: Stage One analyzers (21.1, 002.2, 002.3) can start immediately in sequence, then enable parallel work starting Week 4.

This approach:
- ✅ Works for single developer (sequential 6-8 weeks)
- ✅ Enables team scaling (parallel saves 2-3 weeks)
- ✅ Produces preliminary outputs by Week 2 for Task 001 feedback
- ✅ Creates clear checkpoints for quality gates
- ✅ Allows pivot to parallel execution at Week 3

---

## Sequential Execution Plan (Weeks 1-8)

### Week 1: Task 002.1 (CommitHistoryAnalyzer) - 24-32 hours
**Status:** Sequential start, independent  
**Output:** `commit_history_metrics.json`

**Days 1-2:** Design & Git Extraction
- 002.1.1: Design metric system (2-3h)
- 002.1.2: Git data extraction (4-5h)

**Days 3-4:** Metric Implementation (parallel if 2+ people)
- 002.1.3: Recency metric (3-4h)
- 002.1.4: Frequency metric (3-4h)
- 002.1.5: Authorship diversity (3-4h)

**Days 5-6:** Merge Readiness & Testing
- 002.1.6: Merge readiness metric (3-4h)
- 002.1.7: Aggregation (2-3h)
- 002.1.8: Unit tests (3-4h)

**Quality Gate:** 
- [ ] All metrics ∈ [0,1]
- [ ] 8+ unit tests passing
- [ ] Documentation complete
- [ ] Output JSON matches spec

**Checkpoint Output:** `commit_history_metrics.json` (13 branches, each with 5 metrics)

---

### Week 2: Task 002.2 (CodebaseStructureAnalyzer) - 28-36 hours
**Status:** Depends on 002.1 (structurally only, no data dependency)  
**Output:** `codebase_structure_metrics.json`

**Days 1-2:** Design & File Structure Mapping
- 002.2.1: Analyzer design (2-3h)
- 002.2.2: Directory/file mapping (4-5h)

**Days 3-4:** Similarity Metrics (parallel if 2+ people)
- 002.2.3: Directory similarity (3-4h)
- 002.2.4: File additions metric (3-4h)
- 002.2.5: Module stability (3-4h)

**Days 5-6:** Namespace & Testing
- 002.2.6: Namespace isolation (3-4h)
- 002.2.7: Aggregation (2-3h)
- 002.2.8: Unit tests (3-4h)

**Quality Gate:**
- [ ] All metrics ∈ [0,1]
- [ ] Handles 1000+ file repos
- [ ] 8+ unit tests passing
- [ ] JSON schema validation

**Checkpoint Output:** `codebase_structure_metrics.json`

**PARALLEL OPTION:** If you have 2 people, start 002.2 on Week 1 Day 3 (after 002.1.1-21.1.2 complete)

---

### Week 3: Task 002.3 (DiffDistanceCalculator) - 32-40 hours
**Status:** Depends on 002.1, 002.2 (structurally only)  
**Output:** `diff_distance_metrics.json`

**Days 1-2:** Diff Strategy & Extraction
- 002.3.1: Diff metrics design (3-4h)
- 002.3.2: Diff extraction (4-5h)

**Days 3-4:** Code Analysis (parallel if 2+ people)
- 002.3.3: Code churn metric (3-4h)
- 002.3.4: Concentration metric (3-4h)
- 002.3.5: Complexity metric (3-4h)

**Days 5-6:** Risk Assessment & Testing
- 002.3.6: Integration risk (3-4h)
- 002.3.7: Aggregation (2-3h)
- 002.3.8: Unit tests (4-5h)

**Quality Gate:**
- [ ] All metrics ∈ [0,1]
- [ ] Handles 10,000+ line diffs
- [ ] 8+ unit tests passing
- [ ] Risk scores normalized

**Checkpoint Output:** `diff_distance_metrics.json`

**PARALLEL OPTION:** If you have 2+ people, start 002.3 on Week 1 Day 3 or Week 2 Day 1

---

## Parallel Execution Pivot Point (Week 4)

**IF starting Week 4 with 3+ developers:**

### Option A: Full Parallel (Saves 2 weeks)
- **Team 1:** Task 002.4 (BranchClusterer) - 28-36h
- **Team 2:** Refactor 002.6 (PipelineIntegration) - start early
- **Team 3:** Prepare tests (21.8) from specification

### Option B: Staggered (Saves 1 week)
- **Week 4:** Serial - 002.4 only
- **Week 5:** Parallel - 002.5 & 002.6 together
- **Week 6:** Parallel - 002.7 & 002.8 together

---

### Week 4: Task 002.4 (BranchClusterer) - 28-36 hours
**Status:** Depends on 002.1, 002.2, 002.3 (data inputs)  
**Output:** `clustered_branches.json`

**Inputs Required:**
- `commit_history_metrics.json` from 002.1
- `codebase_structure_metrics.json` from 002.2
- `diff_distance_metrics.json` from 002.3

**Days 1-2:** Design & Metric Combination
- 002.4.1: Clustering design (3-4h)
- 002.4.2: Metric combination (0.35/0.35/0.30 weighting) (4-5h)

**Days 3-4:** Distance & Clustering (parallel if 2+ people)
- 002.4.3: Distance matrix (3-4h)
- 002.4.4: Ward linkage clustering (4-5h)
- 002.4.5: Quality metrics (silhouette, Davies-Bouldin) (3-4h)

**Days 5-6:** Output & Testing
- 002.4.6: Aggregation & output format (2-3h)
- 002.4.7: Unit tests (4-5h)

**Quality Gate:**
- [ ] Silhouette score > 0.5
- [ ] No NaN or Inf values
- [ ] Cluster count reasonable (3-8 clusters)
- [ ] 8+ unit tests passing

**Checkpoint Output:** `clustered_branches.json` with quality metrics

---

### Week 5: Task 002.5 (IntegrationTargetAssigner) - 24-32 hours
**Status:** Depends on 002.4  
**Output:** `target_assignments.json` with 30+ tags per branch

**Days 1-2:** Design & Framework Integration
- 002.5.1: Assignment design (3-4h)
- 002.5.2: Tag system design (3-4h)

**Days 3-4:** Assignment Logic (parallel if 2+ people)
- 002.5.3: Target selection (3-4h)
- 002.5.4: Confidence scoring (3-4h)
- 002.5.5: Tag generation (4-5h)

**Days 5-6:** Downstream Bridges & Testing
- 002.5.6: Bridge functions (2-3h)
- 002.5.7: Unit tests (3-4h)

**Quality Gate:**
- [ ] 30+ unique tags per branch
- [ ] Confidence scores ∈ [0,1]
- [ ] All downstream bridges working
- [ ] 8+ unit tests passing

**Checkpoint Output:** `target_assignments.json` with tags

---

### Week 5-6: Task 002.6 (PipelineIntegration) - 20-28 hours
**Status:** Depends on 002.1-21.5  
**Output:** `enhanced_orchestration_branches.json` (final)

**Days 1-2:** Pipeline Design & Configuration
- 002.6.1: Pipeline design (2-3h)
- 002.6.2: Configuration management (3-4h)

**Days 3-4:** Integration (parallel if 2+ people)
- 002.6.3: Task 002.1 integration (2-3h)
- 002.6.4: Task 002.4-21.5 integration (3-4h)
- 002.6.5: Caching & optimization (3-4h)

**Days 5-6:** End-to-End & Testing
- 002.6.6: End-to-end workflow (2-3h)
- 002.6.7: Unit tests (3-4h)

**Quality Gate:**
- [ ] Full pipeline execution < 2 minutes (13 branches)
- [ ] Caching working properly
- [ ] All outputs generated
- [ ] JSON schema validation passing

**Checkpoint Output:** `enhanced_orchestration_branches.json`

---

### Week 6-7: Tasks 002.7 & 002.8 (Parallel)
**Status:** Depends on 002.6

#### Task 002.7 (VisualizationReporting) - 20-28 hours
**Output:** dendrogram.html, dashboard.html, report.html

**Subtasks:**
- 002.7.1: Dendrogram visualization (5-7h)
- 002.7.2: Dashboard creation (7-9h)
- 002.7.3: Report generation (5-7h)
- 002.7.4: Unit tests (3-4h)

#### Task 002.8 (TestingSuite) - 24-32 hours
**Output:** Test report with >90% coverage

**Subtasks:**
- 002.8.1: Unit test suite (8-10h)
- 002.8.2: Integration tests (8-10h)
- 002.8.3: Edge case tests (4-6h)
- 002.8.4: Coverage report (2-3h)

**Quality Gate:**
- [ ] >90% code coverage
- [ ] All tests passing
- [ ] HTML visualizations rendering
- [ ] Reports readable and informative

---

### Week 8: Task 002.9 (FrameworkIntegration) - 16-24 hours
**Status:** Depends on 002.1-21.8  
**Output:** Production-ready framework

**Subtasks:**
- 002.9.1: Framework integration (4-6h)
- 002.9.2: Downstream bridges (4-6h)
- 002.9.3: Documentation (4-6h)
- 002.9.4: Final validation (2-3h)

**Quality Gate:**
- [ ] All downstream tasks can use framework
- [ ] Documentation complete
- [ ] No breaking changes
- [ ] Ready for Tasks 77, 79, 80, 81, 83, 101

---

## Subtask Numbering Convention

### Format: `21.X.Y`
- `21.X` = Main subtask (21.1 through 002.9)
- `Y` = Sub-subtask within main subtask

### Hierarchy:
```
21 (Branch Clustering System)
├─ 002.1 (CommitHistoryAnalyzer)
│  ├─ 002.1.1 (Design)
│  ├─ 002.1.2 (Git Extraction)
│  ├─ 002.1.3-21.1.7 (Metrics)
│  └─ 002.1.8 (Tests)
├─ 002.2 (CodebaseStructureAnalyzer)
│  ├─ 002.2.1 (Design)
│  ├─ 002.2.2-21.2.6 (Metrics)
│  ├─ 002.2.7 (Aggregation)
│  └─ 002.2.8 (Tests)
├─ 002.3 (DiffDistanceCalculator)
│  ├─ 002.3.1-21.3.2 (Design & Extraction)
│  ├─ 002.3.3-21.3.6 (Metrics)
│  ├─ 002.3.7 (Aggregation)
│  └─ 002.3.8 (Tests)
├─ 002.4 (BranchClusterer)
│  ├─ 002.4.1-21.4.2 (Design)
│  ├─ 002.4.3-21.4.5 (Clustering)
│  ├─ 002.4.6 (Output)
│  └─ 002.4.7 (Tests)
├─ 002.5 (IntegrationTargetAssigner)
│  ├─ 002.5.1-21.5.2 (Design)
│  ├─ 002.5.3-21.5.5 (Assignment)
│  ├─ 002.5.6 (Bridges)
│  └─ 002.5.7 (Tests)
├─ 002.6 (PipelineIntegration)
│  ├─ 002.6.1-21.6.2 (Design)
│  ├─ 002.6.3-21.6.5 (Integration)
│  ├─ 002.6.6 (End-to-End)
│  └─ 002.6.7 (Tests)
├─ 002.7 (VisualizationReporting)
│  ├─ 002.7.1-21.7.3 (Visualizations)
│  └─ 002.7.4 (Tests)
├─ 002.8 (TestingSuite)
│  ├─ 002.8.1-21.8.3 (Tests)
│  └─ 002.8.4 (Coverage)
└─ 002.9 (FrameworkIntegration)
   ├─ 002.9.1 (Framework)
   ├─ 002.9.2 (Bridges)
   ├─ 002.9.3 (Documentation)
   └─ 002.9.4 (Validation)
```

---

## Early Execution Checkpoints

### End of Week 1 (Day 5)
**Completed:** Task 002.1  
**Deliverable:** `commit_history_metrics.json`  
**Check:** Share preliminary metrics with Task 001 team

**Quality Gate:**
- [ ] 13 branches analyzed
- [ ] 5 metrics per branch
- [ ] All values ∈ [0,1]
- [ ] Unit tests >95% passing

---

### End of Week 2 (Day 10)
**Completed:** Tasks 002.1 + 002.2  
**Deliverable:** `commit_history_metrics.json` + `codebase_structure_metrics.json`  
**Check:** Task 001 team refines criteria based on real data

**Quality Gate:**
- [ ] Both files valid JSON
- [ ] Combined metrics show variance
- [ ] Task 001 can use for validation

---

### End of Week 3 (Day 15)
**Completed:** Tasks 002.1-21.3  
**Deliverable:** All three analyzer outputs  
**Check:** Ready for clustering integration

**Quality Gate:**
- [ ] All three metrics available
- [ ] Data consistency verified
- [ ] Can combine for clustering

---

### Parallel Pivot (Week 4)
**Decision Point:** Do you have 2+ developers available?

**YES:** Start parallel execution
- 002.4 sequential, then 002.5-21.6, then 002.7 & 002.8 parallel
- **Timeline:** 6-8 weeks (saves 2 weeks vs pure sequential)

**NO:** Continue sequential
- 002.4 → 002.5 → 002.6 → 002.7 → 002.8 → 002.9
- **Timeline:** 8 weeks

---

### End of Week 6 (Day 30)
**Completed:** Tasks 002.1-21.6  
**Deliverable:** `enhanced_orchestration_branches.json` (final format)  
**Check:** Framework ready for visualization & testing

**Quality Gate:**
- [ ] Pipeline executes end-to-end
- [ ] All 13 branches processed
- [ ] Output < 2 minutes
- [ ] JSON schema validation passing

---

### End of Week 8 (Day 40)
**Completed:** All tasks 002.1-21.9  
**Deliverable:** Production-ready framework  
**Check:** Ready for downstream tasks (77, 79, 80, 81, 83, 101)

**Quality Gate:**
- [ ] >90% test coverage
- [ ] Visualizations complete
- [ ] Documentation done
- [ ] Downstream bridges working

---

## Synchronization with Task 001

### Week 1 (Task 001.1-001.2 + Task 002.1)
**Status:** Initial framework design
- Task 001 defines hypothesis-based criteria (no data)
- Task 002 begins analyzer implementation
- **Action:** No sync needed (independent work)

---

### Week 2 (Task 001.2-001.3 + Task 002.2)
**Status:** Criteria refinement begins
- Task 001 completes target selection criteria (hypothesis)
- Task 002 produces preliminary commit metrics
- **Action:** Friday sync meeting
  - Task 001 team reviews preliminary metrics
  - Validates if criteria assumptions are correct
  - Identifies any needed adjustments

---

### Week 3 (Task 001.4-001.5 + Task 002.3)
**Status:** Data-driven refinement
- Task 001 refines conflict resolution & architecture rules
- Task 002 produces all three Stage One metrics
- **Action:** Friday sync meeting
  - Task 001 team analyzes full metric set
  - Validates clustering assumptions
  - Adjusts weights if metrics show unexpected distribution

---

### Week 4-8 (Task 001.6-001.7 + Task 002.4-21.9)
**Status:** Framework + system integration
- Task 001 finalizes documentation with real examples
- Task 002 integrates metrics into clustering
- **Action:** Weekly sync meetings (every Friday)
  - Share clustering results with Task 001 team
  - Validate cluster quality against framework criteria
  - Refine both systems iteratively

---

## Critical Dependencies

### Hard Dependencies (Must Complete)
1. **21.1 → 002.4:** Commit metrics required for clustering
2. **21.2 → 002.4:** Structure metrics required for clustering
3. **21.3 → 002.4:** Diff metrics required for clustering
4. **21.4 → 002.5:** Clustering required for target assignment
5. **21.5 → 002.6:** Assignments required for pipeline
6. **21.6 → 002.7, 002.8:** Pipeline outputs required for visualization and testing
7. **21.7, 002.8 → 002.9:** All components required for framework integration

### Soft Dependencies (Can Start Early)
1. **21.2 can start during 002.1.3-21.1.8** (after 002.1 design complete)
2. **21.3 can start during 002.2.3-21.2.8** (after 002.2 design complete)
3. **21.7 & 002.8 can start during 002.6.1-21.6.2** (during design phase)

### Task 001 Dependencies
1. **Weak dependency:** Task 001 benefits from 002.1-21.3 outputs (real metrics for validation)
2. **Feedback loop:** Task 001 refined criteria inform 002.4 configuration (weights)
3. **No blocking:** Task 001 can progress independently in Week 1-3

---

## Effort Timeline Comparison

### Pure Sequential (1 person, 8 weeks)
```
Week 1: 24-32h (21.1)
Week 2: 28-36h (21.2)
Week 3: 32-40h (21.3)
Week 4: 28-36h (21.4)
Week 5: 24-32h (21.5)
Week 5-6: 20-28h (21.6)
Week 6-7: 20-28h (21.7)
Week 6-7: 24-32h (21.8) [parallel with 002.7]
Week 8: 16-24h (21.9)
─────────────────────
Total: 212-288h (6-8 weeks)
```

### Early Sequential with Week 3 Parallel (2 people, 6-7 weeks)
```
Week 1: 24-32h (21.1, Person 1) | —— (Person 2 starts Friday)
Week 2: 28-36h (21.2, Person 2) | 24-32h (21.1 cont, Person 1)
Week 3: 32-40h (21.3) | —— (parallel pivot decision)
  OR split: 002.3 takes 5 days (one person)
Week 4: 28-36h (21.4)
Week 5: 24-32h (21.5) | —— (parallel if scaled)
Week 5-6: 20-28h (21.6)
Week 6-7: 002.7 (20-28h) | 002.8 (24-32h) [parallel]
Week 8: 16-24h (21.9)
─────────────────────
Total: 212-288h (6-7 weeks) [saves 1 week]
```

### Early Parallel (3+ people, 4-6 weeks)
```
Week 1: 002.1 (24-32h) | 002.2 (start) | (prep for 002.3)
Week 2: 002.1 finish | 002.2 (28-36h) | 002.3 (start)
Week 3: 002.3 (32-40h) | (pivot decision made)
Week 4: 002.4 (28-36h)
Week 5: 002.5 (24-32h) | 002.6 (start)
Week 5-6: 002.6 (20-28h) | 002.7 (20-28h) | 002.8 (24-32h) [all parallel]
Week 7: 002.9 (16-24h)
─────────────────────
Total: 212-288h (4-6 weeks) [saves 2-3 weeks]
```

---

## How to Use This Framework

### For Single Developer (Pure Sequential)
1. Follow Week 1-8 schedule exactly as written
2. Complete 002.X subtasks in order
3. Use checkpoints to validate progress
4. Sync with Task 001 every Friday (15-min review)
5. Expected completion: 8 weeks

### For 2 Developers (Early Sequential + Parallel Pivot)
1. **Weeks 1-2:** Both on different Stage One analyzers
   - Dev 1: 002.1 (Mon-Fri)
   - Dev 2: Supports 002.1 (Mon-Wed), then starts 002.2 (Wed-Fri)
2. **Week 3:** Dev 2 finishes 002.2, Dev 1 on 002.3
3. **Week 4+:** Decide on parallel execution
4. Expected completion: 6-7 weeks

### For 3+ Developers (Full Parallel)
1. **Weeks 1-3:** Stage One in parallel
   - Dev 1: 002.1
   - Dev 2: 002.2
   - Dev 3: 002.3
2. **Week 4:** Dev 1 starts 002.4 (depends on outputs)
3. **Week 5:** Dev 2 starts 002.5, Dev 3 starts 002.6
4. **Week 6-7:** Dev 4 & 5 on 002.7 & 002.8
5. **Week 8:** Dev 6 on 002.9
6. Expected completion: 4-6 weeks

---

## Quality Gates at Each Stage

### After 002.1 (Commit History)
- [ ] 5 metrics computed for each branch
- [ ] All metrics ∈ [0,1] range
- [ ] Aggregate score = weighted sum of metrics
- [ ] Unit tests >95% passing
- [ ] Edge cases: orphaned branches, single-commit, stale

### After 002.2 (Codebase Structure)
- [ ] 4 metrics computed for each branch
- [ ] All metrics ∈ [0,1] range
- [ ] Jaccard similarity computed correctly
- [ ] Unit tests >95% passing
- [ ] Handles 1000+ file repositories

### After 002.3 (Diff Distance)
- [ ] 4 metrics computed for each branch
- [ ] All metrics ∈ [0,1] range
- [ ] Code churn normalized properly
- [ ] Unit tests >95% passing
- [ ] Handles 10,000+ line diffs

### After 002.4 (Clustering)
- [ ] Metrics combined with 35/35/30 weights
- [ ] Distance matrix computed (< 1 second for 50 branches)
- [ ] Ward linkage clustering performed
- [ ] Quality metrics (silhouette > 0.5)
- [ ] Cluster dendrogram valid
- [ ] Output JSON schema valid

### After 002.5 (Target Assignment)
- [ ] 30+ tags generated per branch
- [ ] Confidence scores ∈ [0,1]
- [ ] Downstream bridge functions working
- [ ] Tags align with Task 001 framework
- [ ] Unit tests >95% passing

### After 002.6 (Pipeline)
- [ ] Full pipeline executes < 2 minutes
- [ ] All 13 branches processed
- [ ] Final JSON output matches schema
- [ ] Caching working properly
- [ ] Configuration validation passing

### After 002.7 (Visualization)
- [ ] Dendrogram HTML renders correctly
- [ ] Dashboard interactive
- [ ] Reports readable and informative
- [ ] All visualizations valid

### After 002.8 (Testing)
- [ ] >90% code coverage
- [ ] All unit tests passing
- [ ] All integration tests passing
- [ ] Edge case tests covering 8+ scenarios

### After 002.9 (Framework)
- [ ] Framework complete and documented
- [ ] Downstream bridges functional
- [ ] Compatible with Tasks 77, 79, 80, 81, 83, 101
- [ ] Production-ready

---

## Pivot Points for Parallel Acceleration

### Pivot 1: Week 3 Day 2 (After 002.1.2 & 002.2.2)
**Triggered when:** Designer/architecture person available  
**Action:** Start 002.3 while 002.2 metrics computing  
**Benefit:** 002.3 starts 5 days earlier, saves 5 days

### Pivot 2: Week 4 Day 1 (Before 002.4)
**Triggered when:** Infrastructure/testing person available  
**Action:** Start 002.6 design phase while 002.4 clustering  
**Benefit:** 002.6 integration ready by end of Week 5

### Pivot 3: Week 6 Day 1 (Before 002.7 & 002.8)
**Triggered when:** 2+ testing/visualization people available  
**Action:** Start 002.7 & 002.8 immediately after 002.6 release  
**Benefit:** Both complete by end of Week 6

---

## Success Criteria

Task 002 is complete when:

1. ✅ All 9 subtasks (21.1-21.9) implemented
2. ✅ JSON outputs generated and validated:
   - `commit_history_metrics.json`
   - `codebase_structure_metrics.json`
   - `diff_distance_metrics.json`
   - `clustered_branches.json`
   - `target_assignments.json`
   - `enhanced_orchestration_branches.json`
3. ✅ 30+ tags generated per branch
4. ✅ Downstream compatibility verified (Tasks 77, 79, 80, 81, 83, 101)
5. ✅ Unit tests >90% coverage, all passing
6. ✅ Integration tests passing
7. ✅ Performance: 13 branches in <2 minutes
8. ✅ Documentation complete
9. ✅ Framework deployed and ready for use

---

**Framework Created:** January 4, 2026  
**Sequencing:** Optimized for both sequential (8 weeks) and parallel (4-6 weeks) execution  
**Next Phase:** Extract task-021-1 through task-021-9 files from task-75.*.md sources
