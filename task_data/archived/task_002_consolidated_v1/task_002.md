# Task 002: Branch Clustering System

**Status:** Ready for Implementation  
**Priority:** High  
**Effort:** 136-176 hours (Phase 1: Tasks 002.1-002.5)  
**Timeline:** 3-4 weeks  
**Parallelizable:** Yes (Subtasks 002.1-002.3 can run in parallel)

---

## Overview

Implement a complete branch clustering and intelligent categorization system for automated branch analysis, similarity assessment, and target branch assignment. This Phase 1 implementation covers:

- **Task 002.1:** CommitHistoryAnalyzer - Extract and score commit history metrics
- **Task 002.2:** CodebaseStructureAnalyzer - Analyze directory/file structure similarity  
- **Task 002.3:** DiffDistanceCalculator - Compute code distance metrics
- **Task 002.4:** BranchClusterer - Combine metrics and perform hierarchical clustering
- **Task 002.5:** IntegrationTargetAssigner - Assign target branches with comprehensive tagging

**Phase 2-3** (deferred) will include PipelineIntegration, VisualizationReporting, TestingSuite, and FrameworkIntegration.

---

## Success Criteria

Task 002 Phase 1 is complete when:

1. ✓ All 5 subtasks (002.1-002.5) implemented and passing tests
2. ✓ CommitHistoryAnalyzer produces normalized metrics in [0,1] range
3. ✓ CodebaseStructureAnalyzer measures codebase similarity with Jaccard metric
4. ✓ DiffDistanceCalculator computes code distance from diff analysis
5. ✓ BranchClusterer performs hierarchical clustering and produces dendrogram
6. ✓ IntegrationTargetAssigner generates 30+ tags per branch with confidence scores
7. ✓ Unit test coverage >90% across all components
8. ✓ Integration tests verify data flow between components
9. ✓ Performance: Process 13 branches in <120 seconds
10. ✓ Documentation complete with implementation guides
11. ✓ Ready for Phase 2 (PipelineIntegration and full testing suite)

---

## Quick Navigation

- [Overview](#overview)
- [Success Criteria](#success-criteria)
- [Execution Strategies](#execution-strategies)
- [Subtasks Summary](#subtasks-summary)
- [Architecture](#architecture)
- [Configuration](#configuration)
- [Dependencies](#dependencies)

---

## Execution Strategies

### Strategy 1: Full Parallel (Recommended - 3 weeks)

**Week 1:** Stage One (Parallel Implementation)
- **Team A:** Task 002.1 (CommitHistoryAnalyzer) - 24-32 hours
- **Team B:** Task 002.2 (CodebaseStructureAnalyzer) - 28-36 hours
- **Team C:** Task 002.3 (DiffDistanceCalculator) - 32-40 hours

**Week 2:** Stage One Integration
- **Team D:** Task 002.4 (BranchClusterer) - 28-36 hours
  - Receives outputs from 002.1, 002.2, 002.3
  - Implements hierarchical clustering with Ward linkage

**Week 3:** Stage Two & Testing
- **Team E:** Task 002.5 (IntegrationTargetAssigner) - 24-32 hours
  - Receives outputs from 002.4
  - Generates comprehensive tags and assignments
- **All Teams:** Integration testing and performance tuning

### Strategy 2: Sequential (4 weeks)

Follow order: 002.1 → 002.2 → 002.3 → 002.4 → 002.5

**Best for:** Single developer or very limited resources

### Strategy 3: Hybrid (3.5 weeks)

- **Week 1:** Tasks 002.1 + 002.2 (sequential, parallel with each other possible)
- **Week 2:** Tasks 002.3 + 002.4 (start 002.4 once 002.1-002.2 complete)
- **Week 3:** Task 002.5 + comprehensive testing

---

## Subtasks Summary

### Task 002.1: CommitHistoryAnalyzer (24-32 hours, Complexity 7/10)

**Purpose:** Extract and score commit history metrics for branches

**What it does:**
- Extracts commit data for a target branch relative to main/master
- Computes 5 normalized metrics (0-1 scale):
  - `commit_recency`: How recent are the latest commits (0=old, 1=very recent)
  - `commit_frequency`: Commit rate relative to branch age
  - `authorship_diversity`: Number of unique contributors
  - `merge_readiness`: Commits behind main branch (inverse normalized)
  - `stability_score`: Consistency of commit patterns
- Returns aggregated score weighted by metric importance

**Output Format:**
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

**Key Implementation Details:**
- Use subprocess with 30-second timeout for git commands
- Implement exponential decay for recency metric
- Handle edge cases: new branches, stale branches, orphaned branches
- Performance: <2 seconds per branch on typical 500-commit repos
- Memory: <50 MB per analysis

**See:** task_002-clustering.md § 002.1 for complete implementation guide

---

### Task 002.2: CodebaseStructureAnalyzer (28-36 hours, Complexity 7/10)

**Purpose:** Measure codebase structure similarity between branches

**What it does:**
- Maps directory/file structure for target branch vs. main
- Computes 4 normalized metrics:
  - `directory_similarity`: Jaccard similarity of directory trees (30% weight)
  - `file_additions`: Ratio of new files added, inverted (25% weight)
  - `core_module_stability`: Preservation of core modules (25% weight)
  - `namespace_isolation`: Isolation score for new packages (20% weight)
- Returns aggregated similarity score

**Output Format:**
```json
{
  "branch_name": "feature/auth-system",
  "metrics": {
    "directory_similarity": 0.82,
    "file_additions": 0.68,
    "core_module_stability": 0.95,
    "namespace_isolation": 0.71
  },
  "aggregate_score": 0.794,
  "directory_count": 23,
  "file_count": 156,
  "new_files": 14,
  "modified_files": 28,
  "analysis_timestamp": "2025-12-22T10:35:00Z"
}
```

**Key Implementation Details:**
- Use `git ls-tree -r --name-only` for directory extraction
- Implement Jaccard similarity: |intersection| / |union|
- Define core modules list (src/, tests/, config/, build/, etc.)
- Performance: <2 seconds per branch on repos with 500+ files
- Memory: <50 MB per analysis
- Handle: Binary files, large repos, UTF-8 encoding

**See:** task_002-clustering.md § 002.2 for complete implementation guide

---

### Task 002.3: DiffDistanceCalculator (32-40 hours, Complexity 8/10)

**Purpose:** Compute code distance metrics between branches using diff analysis

**What it does:**
- Analyzes code diffs between target branch and main
- Computes 4 normalized metrics:
  - `code_churn`: Lines changed ratio (inverse normalized)
  - `change_concentration`: Files affected count impact
  - `diff_complexity`: Large diffs in few files
  - `integration_risk`: Pattern-based risk scoring
- Returns aggregated diff distance score

**Output Format:**
```json
{
  "branch_name": "feature/auth-system",
  "metrics": {
    "code_churn": 0.72,
    "change_concentration": 0.81,
    "diff_complexity": 0.68,
    "integration_risk": 0.79
  },
  "aggregate_score": 0.750,
  "total_lines_added": 342,
  "total_lines_deleted": 87,
  "total_lines_changed": 429,
  "files_affected": 12,
  "largest_file_change": 156,
  "analysis_timestamp": "2025-12-22T10:40:00Z"
}
```

**Key Implementation Details:**
- Use `git diff main...BRANCH_NAME --numstat` for metrics
- Define risk categories: critical, high, medium, low
- Create risk file patterns (config files, security files, etc.)
- Performance: <3 seconds per branch on repos with 100+ file diffs
- Memory: <100 MB per analysis
- Handle: Binary files, large diffs, merge commits, empty branches

**See:** task_002-clustering.md § 002.3 for complete implementation guide

---

### Task 002.4: BranchClusterer (28-36 hours, Complexity 8/10)

**Purpose:** Combine normalized metrics and perform hierarchical clustering

**What it does:**
- Accepts output from Tasks 002.1, 002.2, 002.3
- Combines metrics using weighted formula: 0.35×(002.1) + 0.35×(002.2) + 0.30×(002.3)
- Performs hierarchical agglomerative clustering with Ward linkage
- Computes cluster quality metrics:
  - Silhouette score: [-1, 1] range (higher = better)
  - Davies-Bouldin index: [0, ∞) (lower = better)
  - Calinski-Harabasz index: [0, ∞) (higher = better)
- Outputs cluster assignments with quality metrics

**Output Format:**
```json
{
  "clusters": [
    {
      "cluster_id": 0,
      "branches": ["feature/auth", "feature/user-management"],
      "size": 2,
      "characteristics": {
        "avg_recency": 0.79,
        "avg_complexity": 0.65,
        "avg_risk": 0.45
      }
    }
  ],
  "quality_metrics": {
    "silhouette_score": 0.68,
    "davies_bouldin_index": 0.82,
    "calinski_harabasz_index": 12.45,
    "threshold_used": 0.5,
    "dendrogram_height": 2.34
  },
  "analysis_timestamp": "2025-12-22T10:45:00Z"
}
```

**Key Implementation Details:**
- Use scipy.cluster.hierarchy for Ward linkage
- Compute Euclidean distance on normalized vectors
- Dendrogram threshold strategy: default 0.5 (configurable)
- Performance: <10 seconds for 50+ branches
- Memory: <100 MB for clustering operations
- Ensure minimum 2 clusters (if only 1, adjust threshold)

**See:** task_002-clustering.md § 002.4 for complete implementation guide

---

### Task 002.5: IntegrationTargetAssigner (24-32 hours, Complexity 7/10)

**Purpose:** Assign integration targets to clustered branches with comprehensive tagging

**What it does:**
- Accepts cluster output from Task 002.4
- Implements 4-level decision hierarchy:
  1. **Level 1:** Heuristic rules (confidence threshold >0.90)
  2. **Level 2:** Affinity scoring to archetypes (confidence >0.70)
  3. **Level 3:** Cluster consensus voting (confidence >0.60)
  4. **Level 4:** Default assignment (fallback)
- Assigns one of three targets: `main`, `scientific`, `orchestration-tools`
- Generates 30+ tags per branch across 6 categories:
  - **Primary Target Tags (1 required):** `tag:main_branch`, `tag:scientific_branch`, `tag:orchestration_tools_branch`
  - **Execution Context Tags (1 required):** `tag:parallel_safe`, `tag:sequential_required`, `tag:isolated_execution`
  - **Complexity Tags (1 required):** `tag:simple_merge`, `tag:moderate_complexity`, `tag:high_complexity`
  - **Content Type Tags:** `tag:core_code_changes`, `tag:test_changes`, `tag:config_changes`, `tag:documentation_only`, `tag:security_sensitive`, `tag:performance_critical`
  - **Validation Tags:** `tag:requires_e2e_testing`, `tag:requires_unit_tests`, `tag:requires_security_review`, `tag:requires_performance_testing`
  - **Workflow Tags:** `tag:task_101_orchestration`, `tag:framework_core`, `tag:framework_extension`

**Output Format:**
```json
{
  "branch_name": "feature/auth-system",
  "assigned_target": "main",
  "confidence": 0.87,
  "assignment_source": "Level 2: Affinity scoring",
  "reasoning": "High merge readiness (0.91) and low risk (0.2) indicate main branch target",
  "tags": [
    "tag:main_branch",
    "tag:parallel_safe",
    "tag:moderate_complexity",
    "tag:core_code_changes",
    "tag:requires_unit_tests",
    ...35 more tags...
  ],
  "archetype_affinities": {
    "main": 0.87,
    "scientific": 0.34,
    "orchestration-tools": 0.21
  },
  "analysis_timestamp": "2025-12-22T10:50:00Z"
}
```

**Key Implementation Details:**
- Define target archetypes based on metric profiles
- Implement confidence scoring mechanism (weighted factors)
- Generate tags conditionally based on metrics and assignment
- Performance: <1 second per branch
- Memory: <50 MB for assignment operations
- Ensure all confidence scores in [0,1] range with no NaN values

**See:** task_002-clustering.md § 002.5 for complete implementation guide

---

## Architecture

### Data Flow Diagram

```
INPUT: Git Repository + Branch List
   ↓
┌──────────────────────────────────────┐
│ Task 002.1: CommitHistoryAnalyzer    │ (Parallel)
│ Output: 5 metrics, aggregate score   │
└──────────────────────────────────────┘
   ↓
┌──────────────────────────────────────┐
│ Task 002.2: CodebaseStructureAnalyzer│ (Parallel)
│ Output: 4 metrics, similarity score  │
└──────────────────────────────────────┘
   ↓
┌──────────────────────────────────────┐
│ Task 002.3: DiffDistanceCalculator   │ (Parallel)
│ Output: 4 metrics, distance score    │
└──────────────────────────────────────┘
   ↓
┌──────────────────────────────────────┐
│ Task 002.4: BranchClusterer          │
│ Combines all metrics + performs HAC  │
│ Output: Cluster assignments + quality│
└──────────────────────────────────────┘
   ↓
┌──────────────────────────────────────┐
│ Task 002.5: IntegrationTargetAssigner│
│ Assigns targets + generates tags     │
│ Output: Assignments with 30+ tags    │
└──────────────────────────────────────┘
   ↓
OUTPUT: Categorized & Clustered Branches
```

---

## Configuration

All tasks use externalized YAML configuration. Example config/task-002-clustering.yaml:

```yaml
metrics:
  commit_history_weight: 0.35
  codebase_structure_weight: 0.35
  diff_distance_weight: 0.30

commit_history:
  recency_window_days: 30
  frequency_normalization: 5
  stability_threshold: 0.5
  git_command_timeout_seconds: 30

codebase_structure:
  core_modules:
    - src/
    - tests/
    - config/
    - build/
    - dist/
  git_command_timeout_seconds: 30

diff_distance:
  estimated_codebase_size: 5000
  max_expected_files: 50
  git_command_timeout_seconds: 30
  risk_categories:
    critical: ["security/", "auth/", "database/migrations/"]
    high: ["src/", "core/", "main.py"]
    medium: ["utils/", "helpers/", "tests/"]
    low: ["docs/", "examples/", "README.md"]

clustering:
  threshold: 0.5
  linkage_method: "ward"
  distance_metric: "euclidean"
  min_cluster_size: 2
  max_clusters: 10

target_assignment:
  confidence_weights:
    rule_match: 0.40
    metric_agreement: 0.35
    cluster_cohesion: 0.25
  archetype_definitions:
    main:
      merge_readiness: 0.85
      risk_tolerance: 0.3
    scientific:
      merge_readiness: 0.65
      churn_tolerance: 0.8
    orchestration-tools:
      core_module_changes: true
      parallel_safety: true
```

---

## Dependencies & Integration

### Dependencies

**None** - All subtasks are independent until Task 002.4

- Task 002.1 can start immediately
- Task 002.2 can start immediately
- Task 002.3 can start immediately
- Task 002.4 requires 002.1 + 002.2 + 002.3 complete
- Task 002.5 requires 002.4 complete

### Blocks (Future Tasks)

- **Task 007:** Feature Branch Identification (can use outputs)
- **Task 079:** Execution context setup
- **Task 080:** Validation intensity
- **Task 083:** Test suite selection
- **Task 101:** Orchestration filtering

### Downstream Integration

Outputs feed into:
- Task-002-generated tags used by Tasks 007, 079, 080, 083, 101
- Cluster assignments guide branch integration strategy
- Confidence scores inform decision automation

---

## Performance Targets

| Component | Target | Memory | Notes |
|-----------|--------|--------|-------|
| 002.1 (CommitHistoryAnalyzer) | <2s per branch | <50 MB | On 500-commit repos |
| 002.2 (CodebaseStructureAnalyzer) | <2s per branch | <50 MB | On 500+ file repos |
| 002.3 (DiffDistanceCalculator) | <3s per branch | <100 MB | On 100+ file diffs |
| 002.4 (BranchClusterer) | <10s for 50 branches | <100 MB | HAC computation |
| 002.5 (IntegrationTargetAssigner) | <1s per branch | <50 MB | Tag generation |
| **Full Pipeline** | **<120s for 13 branches** | **<100 MB peak** | All tasks sequentially |

---

## Common Pitfalls & Solutions

### Key Gotchas

**002.1 Specific:**
- Git timeout on large repos (>10,000 commits) → Use 30s timeout
- Merge base not found on orphaned branches → Handle gracefully with defaults
- Division by zero in frequency metric → Ensure minimum 1 day
- Binary files cause parsing errors → Skip binary file markers
- Non-ASCII author names cause encoding errors → Specify UTF-8

**002.2 Specific:**
- Directory vs. file set confusion → Extract directories explicitly
- Division by zero with empty repos → Check denominators
- Core module matching fails on case sensitivity → Normalize paths
- Large file counts cause memory issues → Use streaming
- Missing branch validation → Check branch exists first

**002.3 Specific:**
- Binary files as "-" instead of line counts → Skip binary markers
- Large diffs exhaust memory → Process streaming
- Empty diff causes division by zero → Check for zero changes
- Risk category matching fails → Normalize paths
- Large repo diffs hang → Use 30s timeout

**002.4 Specific:**
- All branches cluster together → Ensure multiple clusters
- Ward linkage needs Euclidean distance → Use correct distance metric
- Distance matrix symmetry issues → Validate and enforce
- Memory explosion with 100+ branches → Use condensed distance format
- Invalid threshold values → Validate and normalize

**002.5 Specific:**
- Tag count < 30 → Add default tags for missing categories
- Conflicting tag assignments → Validate mutual exclusivity
- Confidence scores outside [0,1] → Normalize and clip
- Reasoning text wrong length → Enforce bounds

**See:** task_002-clustering.md for detailed gotchas & solutions for each task

---

## Integration Checkpoint

**When ready to move to Phase 2:**
- [ ] All 5 subtasks complete and passing tests (>90% coverage)
- [ ] Integration tests verify data flow between components
- [ ] Performance benchmarks met (full pipeline <120s for 13 branches)
- [ ] Output formats validated against schemas
- [ ] Configuration system externalized and working
- [ ] Documentation complete and accurate
- [ ] Ready for handoff to Phase 2 (PipelineIntegration)

---

## Done Definition

Task 002 Phase 1 is complete when:

1. All 5 subtasks (002.1-002.5) implemented
2. Unit test coverage >95% across all components
3. Code review approved
4. Integration tests passing
5. Performance targets met
6. Output formats validated
7. Documentation complete
8. Commit message: "feat: complete Task 002 Phase 1 - Branch Clustering System"
9. Ready for Phase 2 work (PipelineIntegration, comprehensive testing, deployment)

---

## Next Steps

1. **Preparation:** Review task_002-clustering.md for detailed implementation guide
2. **Execution:** Choose execution strategy (recommended: Full Parallel)
3. **Implementation:** Follow subtask guides in order of dependency chain
4. **Testing:** Implement unit and integration tests as you go
5. **Validation:** Run performance benchmarks and quality checks
6. **Handoff:** Prepare for Phase 2 (PipelineIntegration, testing, framework)

---

**Last Updated:** January 6, 2026  
**Consolidated from:** Old Task 75 (task-75.md, task-75.1.md through task-75.5.md)  
**Implementation Guide:** See task_002-clustering.md
