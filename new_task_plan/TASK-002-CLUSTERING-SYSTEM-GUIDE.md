# Task 002: Branch Clustering System - Integration Guide

**Clean ID:** 002  
**Original ID:** Task 75  
**Status:** Ready for HANDOFF + Refactoring Integration  
**Timeline:** 6-8 weeks (212-288 hours)  
**Priority:** High  
**Parallelizable:** Yes (Stage One independent)  
**Refactoring:** Task 007 (I2.T4) integrated into 002.6 (PipelineIntegration) - Jan 4, 2026

---

## 5-Minute Overview

Task 002 is an advanced intelligent branch clustering and target assignment system. It analyzes the actual branches in your repository using three independent analyzers:

1. **CommitHistoryAnalyzer (21.1)** - Analyzes Git commit patterns (24-32h)
2. **CodebaseStructureAnalyzer (21.2)** - Analyzes code similarity and structure (28-36h)
3. **DiffDistanceCalculator (21.3)** - Measures code differences (32-40h)

These three run **in parallel** (Stage One), then feed into:

4. **BranchClusterer (21.4)** - Groups similar branches (28-36h)
5. **IntegrationTargetAssigner (21.5)** - Recommends target branches (24-32h)
6. **PipelineIntegration (21.6)** - Orchestrates the system (20-28h)

And finally produces outputs via:

7. **VisualizationReporting (21.7)** - HTML dashboards (20-28h)
8. **TestingSuite (21.8)** - Comprehensive tests (24-32h)
9. **FrameworkIntegration (21.9)** - Final integration (16-24h)

**Key Insight:** This task runs PARALLEL with Task 001 (Framework). Your Stage One outputs (21.1, 002.2, 002.3) provide real branch data to validate Task 001 criteria. Weekly sync ensures both systems improve through bidirectional feedback.

---

## REFACTORING ALERT: Task 007 (I2.T4) Integration into 002.6

**Status:** Ready for Implementation  
**ID:** i2t4-into-756  
**When:** During or after initial 002.6 implementation  
**Impact:** Medium (20-28h → 24-34h for Task 002.6)  

### What's Changing

Task 007 (Feature Branch Identification - I2.T4) is being integrated into Task 002.6 (PipelineIntegration) to create a unified framework supporting three execution modes:

1. **Identification Mode** - Fast branch identification (I2.T4 style, <30s)
2. **Clustering Mode** - Full clustering analysis (Task 21 original, <120s)
3. **Hybrid Mode** - Combined mode with optional clustering (<90s)

### What This Means for Task 002.6

**Before:** Task 002.6 orchestrated the full clustering pipeline only  
**After:** Task 002.6 orchestrates three different execution modes

**New Additions to 002.6:**
- `MigrationAnalyzer` class (~140 lines) - analyzes backend→src migration patterns
- `OutputGenerator` class (~120 lines) - generates simple/detailed/all output formats
- `execute()` routing method - directs to appropriate pipeline
- `_validate_mode()` validation method
- `execute_identification_pipeline()` - fast identification workflow
- `execute_hybrid_pipeline()` - combined workflow

**Configuration Updates:**
```yaml
execution:
  mode: clustering  # NEW: select identification | clustering | hybrid
  enable_migration_analysis: true
  enable_clustering_in_hybrid: true
  output_format: detailed  # NEW: simple | detailed | all
```

### Implementation Impact

**Phase 2: Implementation** (add ~14 tasks to 002.6)
- Add MigrationMetrics dataclass
- Add MigrationAnalyzer class with git analysis
- Add OutputGenerator class with format handlers
- Update BranchClusteringEngine for mode routing
- Update configuration schema

**Phase 4: Testing** (add ~10 test cases)
- Test all three execution modes
- Test output format generation
- Test migration analysis accuracy
- Test backward compatibility

**Performance:**
- Identification mode: <30s, <50MB memory
- Clustering mode: <120s, <100MB memory (unchanged)
- Hybrid mode: <90s, <75MB memory

### Backward Compatibility

✅ **Full backward compatibility maintained** - existing 002.6 consumers see no changes  
✅ **Default behavior unchanged** - mode defaults to "clustering" (original behavior)  
✅ **I2.T4 clients supported** - use "identification" mode for fast analysis  

### Documentation

Three comprehensive guides provided:
- **QUICK_REFERENCE.md** - TL;DR with execution examples
- **CHANGE_SUMMARY.md** - Full change breakdown by phase
- **IMPLEMENTATION_GUIDE.md** - Step-by-step with code snippets

### Next Steps When Implementing 002.6

1. Review IMPLEMENTATION_GUIDE.md before starting
2. Implement MigrationAnalyzer first (prerequisite)
3. Update BranchClusteringEngine.__init__ with new parameters
4. Add three execute methods (routing, identification, hybrid)
5. Add OutputGenerator for format generation
6. Test all modes before integration
7. Update configuration schema in task-75.6.md
8. Add 10 new test cases

---

## Execution Strategies

### Strategy 1: Full Parallel (Recommended, 6-8 weeks)

**Best for:** Team with 6+ developers

**Weeks 1-2:** Stage One (Parallel)
- Team 1: Task 002.1 (CommitHistoryAnalyzer)
- Team 2: Task 002.2 (CodebaseStructureAnalyzer)
- Team 3: Task 002.3 (DiffDistanceCalculator)
- **All three teams work simultaneously**

**Week 3:** Stage One Integration
- Team 4: Task 002.4 (BranchClusterer) - integrates 002.1, 002.2, 002.3 outputs

**Week 4:** Stage Two
- Team 5: Task 002.5 (IntegrationTargetAssigner)
- Team 6: Task 002.6 (PipelineIntegration)

**Weeks 5-6:** Stage Three (Parallel)
- Team 7: Task 002.7 (VisualizationReporting)
- Team 8: Task 002.8 (TestingSuite)

**Week 7:** Final Integration
- Team 9: Task 002.9 (FrameworkIntegration)

**Timeline:** 6-8 weeks | **Effort:** 212-288 hours | **Team Size:** 6+

---

### Strategy 2: Sequential (6-8 weeks)

**Best for:** Single developer or small team

**Week 1:** Task 002.1 (24-32h)
**Week 2:** Task 002.2 (28-36h)
**Week 2-3:** Task 002.3 (32-40h)
**Week 3:** Task 002.4 (28-36h)
**Week 4:** Task 002.5 (24-32h)
**Week 4-5:** Task 002.6 (20-28h)
**Week 5:** Task 002.7 (20-28h)
**Week 6:** Task 002.8 (24-32h)
**Week 7:** Task 002.9 (16-24h)

**Timeline:** 6-8 weeks | **Effort:** 212-288 hours | **Team Size:** 1

---

### Strategy 3: Hybrid (6-8 weeks)

**Best for:** 2-3 developers

**Weeks 1-3:** Tasks 002.1-21.6 sequentially (foundation)
- One person does 002.1, then 002.2, then 002.3
- Another person does 002.4, 002.5, 002.6 starting in Week 3

**Weeks 4-5:** Tasks 002.7 & 002.8 in parallel
- Person A: 002.7 (Visualization)
- Person B: 002.8 (Testing)

**Week 6:** Task 002.9 (Framework Integration)

**Timeline:** 6-8 weeks | **Effort:** 212-288 hours | **Team Size:** 2-3

---

## Where to Work From

**Stage One HANDOFF Documents** (will be extracted Week 3):
- `task_files/task-021-1.md` (from HANDOFF_75.1_CommitHistoryAnalyzer.md)
- `task_files/task-021-2.md` (from HANDOFF_75.2_CodebaseStructureAnalyzer.md)
- `task_files/task-021-3.md` (from HANDOFF_75.3_DiffDistanceCalculator.md)
- `task_files/task-021-4.md` (from HANDOFF_75.4_BranchClusterer.md)
- `task_files/task-021-5.md` (from HANDOFF_75.5_IntegrationTargetAssigner.md)
- `task_files/task-021-6.md` (from HANDOFF_75.6_PipelineIntegration.md)
- `task_files/task-021-7.md` (from HANDOFF_75.7_VisualizationReporting.md)
- `task_files/task-021-8.md` (from HANDOFF_75.8_TestingSuite.md)
- `task_files/task-021-9.md` (from HANDOFF_75.9_FrameworkIntegration.md)

**Each task file will include:**
- 2-3 sentence overview
- Input/Output specifications
- 4-6 working code examples
- Edge case handling
- Test cases with pass/fail criteria
- Implementation checklist

---

## Success Criteria Checklist

Task 002 is complete when:

**Deliverables:**
- [ ] `categorized_branches.json` - Complete branch categorization
- [ ] `clustered_branches.json` - Clustering results with similarity scores
- [ ] `enhanced_orchestration_branches.json` - Target assignments and 30+ tags per branch
- [ ] HTML dashboards - dendrogram.html, dashboard.html, report.html
- [ ] Comprehensive test suite - >90% code coverage
- [ ] Integration framework - Bridge functions for downstream tasks

**Quality Metrics:**
- [ ] Stage One (21.1-21.3) produces metrics in [0,1] range
- [ ] Stage Two (21.4-21.6) produces valid clustering with quality metrics
- [ ] Stage Three (21.7-21.9) produces passing tests
- [ ] All outputs match JSON schemas exactly
- [ ] Downstream compatibility verified (Tasks 77, 79, 80, 83, 101)

**Integration:**
- [ ] Framework integrated with Task 001 guidance
- [ ] Weekly sync feedback incorporated
- [ ] Documentation complete with examples
- [ ] Ready for production use

---

## Information Flow: Parallel Execution with Task 001

### Week 1-2: Stage One (Data Collection)
- **You:** Run 002.1, 002.2, 002.3 in parallel
- **Task 001:** Defines hypothesis-based criteria
- **Action:** Share preliminary metrics with Task 001 team for validation

### Week 2-3: Bidirectional Feedback
- **You:** Receive refined criteria from Task 001
- **Task 001:** Receives branch metrics from your Stage One
- **You:** Use refined criteria for BranchClusterer configuration (21.4)
- **Action:** Weekly sync meeting to share findings

### Week 4-8: Full System
- **You:** Stages Two & Three (21.5-21.9) with validated configuration
- **Task 001:** Framework refined and complete
- **Action:** Both systems working together, downstream tasks can proceed

**Key Point:** This is NOT dependent work (Task 001 blocking you). Both start simultaneously. The sync meetings ensure quality improvement, not blocking.

---

## Day-by-Day for Stage One (Weeks 1-3)

### Parallel Execution (If 3+ people)

**Person A (21.1): CommitHistoryAnalyzer**
- Days 1-3: Implement core analyzer
- Days 4-5: Add edge cases and tests
- **Output:** commit_metrics.json with branch similarity scores

**Person B (21.2): CodebaseStructureAnalyzer**
- Days 1-3: Implement code structure analysis
- Days 4-5: Add edge cases and tests
- **Output:** structure_metrics.json with codebase similarity

**Person C (21.3): DiffDistanceCalculator**
- Days 1-3: Implement diff distance calculation
- Days 4-5: Add edge cases and tests
- **Output:** diff_metrics.json with difference scores

### Sequential Execution (If 1 person)

**Days 1-5: Implement 002.1**
- Full implementation with tests
- **Output:** commit_metrics.json

**Days 6-10: Implement 002.2**
- Full implementation with tests
- **Output:** structure_metrics.json

**Days 11-15: Implement 002.3**
- Full implementation with tests
- **Output:** diff_metrics.json

---

## Stage Two & Three (Weeks 4-8)

### Week 4: Stage Two Integration (21.4)
Combine Stage One metrics using BranchClusterer.

- **Input:** commit_metrics, structure_metrics, diff_metrics
- **Configuration:** Use weights from Task 001 framework (default: 0.35, 0.35, 0.30)
- **Output:** clusters.json with branch groupings
- **Effort:** 28-36 hours
- **Key Deliverable:** Branch similarity groups

### Week 4-5: Target Assignment (21.5)
Recommend target branches for each cluster.

- **Input:** clusters.json + Task 001 target selection criteria
- **Output:** target_assignments.json + 30+ tags per branch
- **Effort:** 24-32 hours
- **Key Deliverable:** Tag system for downstream tasks

### Week 5: Pipeline Integration (21.6)
Orchestrate the entire system end-to-end. **REFACTORED:** Now includes Task 007 (I2.T4) integration for three execution modes.

- **Input:** All 002.1-21.5 outputs
- **Output:** orchestration_branches.json (final integrated format) + identification/hybrid mode outputs
- **Effort:** 20-28 hours (→ 24-34 hours with refactoring)
- **Key Deliverable:** Ready for Stage Three + Fast identification mode support
- **Refactoring:** Add MigrationAnalyzer, OutputGenerator, three execute methods, configuration updates

### Week 5-6: Visualization & Testing (21.7, 002.8)
Create dashboards and test suite.

- **21.7 Output:** dendrogram.html, dashboard.html, report.html
- **21.8 Output:** test_report.json (>90% coverage)
- **Effort:** 44-60 hours combined
- **Key Deliverable:** Visualizations and verification

### Week 7: Framework Integration (21.9)
Final integration with Task 001 and downstream task bridges.

- **Input:** All 002.1-21.8 outputs
- **Output:** clustering_framework.py (production-ready)
- **Effort:** 16-24 hours
- **Key Deliverable:** System ready for deployment

---

## Configuration Parameters

All tasks use these shared parameters (can be overridden):

```yaml
metrics:
  commit_history_weight: 0.35       # From Task 001 criteria (default)
  codebase_structure_weight: 0.35   # From Task 001 criteria (default)
  diff_distance_weight: 0.30        # From Task 001 criteria (default)

clustering:
  threshold: 0.5                    # From Task 001 framework
  linkage_method: "ward"            # Hierarchical clustering method
  distance_metric: "euclidean"      # Distance calculation method

output:
  json_format: "enhanced_orchestration_branches.json"
  schema_version: "1.0"
```

**Update these based on Task 001 refined criteria (Week 2-3).**

---

## JSON Output Schemas

### Stage One Output (21.1-21.3)
```json
{
  "branch_name": "feature/auth-refactor",
  "analyzer": "commit_history",
  "aggregate_score": 0.68,
  "metrics": {
    "commit_frequency": 0.7,
    "author_patterns": 0.65,
    "history_depth": 0.71
  },
  "timestamp": "2026-01-04T14:00:00Z"
}
```

### Clustering Output (21.4)
```json
{
  "cluster_id": "cluster_1",
  "branches": ["feature/auth", "feature/api-design"],
  "centroid": {
    "commit_score": 0.68,
    "structure_score": 0.72,
    "diff_score": 0.65
  },
  "quality_metrics": {
    "silhouette": 0.72,
    "distance_to_nearest": 0.15
  }
}
```

### Target Assignment Output (21.5)
```json
{
  "branch": "feature/auth",
  "suggested_target": "main",
  "confidence": 0.89,
  "tags": [
    "orchestration-branch",
    "parallel-safe",
    "testing-required-medium",
    "complexity-moderate",
    ...30 more tags...
  ]
}
```

---

## Downstream Integration Bridges

After Task 002.9, bridge functions available for downstream tasks:

**For Task 79 (Alignment Execution):**
```python
def get_execution_context_for_branch(branch_name):
    # Returns execution mode (serial/parallel) based on tags
```

**For Task 80 (Validation Intensity):**
```python
def get_test_intensity_for_branch(branch_name):
    # Returns test level (low/medium/high) based on complexity tags
```

**For Task 83 (Test Suite Selection):**
```python
def get_test_suites_for_branch(branch_name):
    # Returns which test suites to run based on tags
```

**For Task 101 (Orchestration Filtering):**
```python
def passes_orchestration_filter(branch_name):
    # Returns True if branch should be in orchestration
```

---

## Getting Help If Stuck

**Stuck on Stage One analyzers?**
→ See `../task_data/HANDOFF_INDEX.md` for data flow architecture and example inputs

**Stuck on metrics normalization?**
→ All 002.1-21.3 must produce [0,1] range scores. Use min-max normalization.

**Stuck on clustering algorithm?**
→ Use scipy.cluster.hierarchy with "ward" linkage method (industry standard)

**Stuck on test cases?**
→ Each HANDOFF file includes 5-7 test case scenarios with expected outputs

**Stuck on Task 001 integration?**
→ Weekly sync meetings happen Fridays. Share metrics and ask for feedback.

---

## Key Files

- **task_files/task-021-1.md through task-021-9.md** - Individual subtask files (will exist Week 3)
- **../task_data/HANDOFF_INDEX.md** - Background, data flow, edge cases
- **../task_data/task-75.1.md through task-75.9.md** - Original HANDOFF documents
- **TASK-001-INTEGRATION-GUIDE.md** - Task 001 (parallel partner)
- **../OPTIMIZED_TASK_SEQUENCE_WITH_EARLY_CLUSTERING.md** - Parallel execution context

---

## Next Steps

1. **Week 1:** This integration guide is created
2. **Week 1-2:** Task 001 runs in parallel (framework definition)
3. **Week 2:** First sync meeting - share preliminary metrics
4. **Week 3 Monday:** task-021-1 through task-021-9.md files extracted and ready
5. **Week 3 Monday:** Begin implementation using chosen execution strategy
6. **Week 3 Friday:** Stage One (21.1-21.3) complete or in progress
7. **Week 4-8:** Stages Two & Three with Task 001 feedback integrated
8. **Week 8:** Framework deployed and ready for Tasks 77, 79, 80, 81, 83, 101

---

## Quick Reference

| Subtask | Title | Effort | Stage | Status | Note |
|---------|-------|--------|-------|--------|------|
| **21.1** | CommitHistoryAnalyzer | 24-32h | One | Pending | |
| **21.2** | CodebaseStructureAnalyzer | 28-36h | One | Pending | |
| **21.3** | DiffDistanceCalculator | 32-40h | One | Pending | |
| **21.4** | BranchClusterer | 28-36h | One(I) | Pending | |
| **21.5** | IntegrationTargetAssigner | 24-32h | Two | Pending | |
| **21.6** | PipelineIntegration + I2.T4 | 24-34h | Two | Pending | REFACTORED: +3 modes, MigrationAnalyzer, OutputGenerator |
| **21.7** | VisualizationReporting | 20-28h | Three | Pending | |
| **21.8** | TestingSuite | 24-32h | Three | Pending | +10 tests for refactoring |
| **21.9** | FrameworkIntegration | 16-24h | Final | Pending | |
| **TOTAL** | Branch Clustering System | 216-298h | All | Pending | +4-10h for refactoring integration |

---

**Status:** Ready for Week 3 HANDOFF Extraction + Refactoring Integration  
**Created:** January 4, 2026  
**Updated:** January 4, 2026 - Integrated i2t4-into-756 refactoring plan  
**Next Phase:** Extract task-021-1 through task-021-9.md from HANDOFF files, then integrate refactoring changes into 002.6  

### Refactoring Documentation
- **QUICK_REFERENCE.md** - TL;DR summary with 5 execution modes and performance targets
- **CHANGE_SUMMARY.md** - Complete change breakdown across 3 files and 4 phases
- **IMPLEMENTATION_GUIDE.md** - Detailed step-by-step with code snippets and exact line numbers
