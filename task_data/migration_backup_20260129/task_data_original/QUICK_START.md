# Two-Stage Branch Clustering System - Quick Start Guide

## What Was Created

Four comprehensive documents defining an enhanced Task 75:

| Document | Purpose | Length | Key Content |
|----------|---------|--------|------------|
| **branch_clustering_framework.md** | Conceptual design | 15 KB | Two-stage approach, heuristics, integration |
| **branch_clustering_implementation.py** | Production code | 28 KB | Python implementation with 4000+ lines |
| **clustering_tasks_expansion.md** | Task breakdown | 18 KB | 9 subtasks with 60+ sub-subtasks, 220+ hours effort |
| **CLUSTERING_SYSTEM_SUMMARY.md** | Executive summary | 20 KB | Overview, metrics, outputs, integration |

---

## Three Key Concepts

### 1. Stage One: Similarity Clustering
```
Input:  List of feature branches
Process: Analyze branches across 3 dimensions
Output: Cluster assignments (C1, C2, C3, etc.)

Dimensions:
├─ Commit History (35%)
│  ├─ Merge base distance
│  ├─ Divergence ratio
│  ├─ Commit frequency
│  ├─ Shared contributors
│  └─ Message similarity
├─ Codebase Structure (35%)
│  ├─ Core directories affected
│  ├─ File type distribution
│  ├─ Code volume
│  └─ Impact type (code/test/infra/docs)
└─ Diff Distance (30%)
   ├─ File overlap ratio
   ├─ Edit distance
   ├─ Change proximity
   └─ Conflict probability
```

### 2. Stage Two: Target Assignment & Tagging
```
Input:  Clustered branches
Process: Assign integration target and tags
Output:  Categorized + tagged branches

Target: main | scientific | orchestration-tools
  ├─ Heuristic rules (95% confidence) - keyword matching
  ├─ Affinity scoring (70% confidence) - directory patterns
  └─ Default (65% confidence) - 'main'

Tags: 30+ comprehensive tags
  ├─ Primary target (1 required)
  ├─ Execution context (1 required) 
  ├─ Complexity (1 required)
  ├─ Content types (0+ optional)
  ├─ Validation requirements (0+ optional)
  └─ Workflow classification (0+ optional)
```

### 3. Integration Impact
```
Enhanced Task 75 feeds into multiple downstream tasks:

Task 75 (new clustering)
  ├─→ Task 79 (uses tags for parallel execution strategy)
  │   ├─→ Task 80 (skips/runs validation based on tags)
  │   └─→ Task 81 (selects merge strategy by complexity tag)
  ├─→ Task 101 (filters orchestration-tools-branch tagged branches)
  └─→ Task 83 (selects test suites by tag)
```

---

## Core Metrics Explained

### Commit History Metrics

**merge_base_distance** (commits since divergence)
- Lower = recently branched off
- Higher = diverged long ago
- Impact: Affects rebase complexity

**divergence_ratio** (feature commits / main commits)
- Lower = kept up with main
- Higher = heavily diverged
- Impact: Complexity indicator

**commit_frequency** (commits per day)
- Higher = active development
- Lower = stalled branch
- Impact: Risk of staleness

**shared_contributors**
- Higher = working in same domain
- Lower = isolated development
- Impact: Team awareness/collaboration

**message_similarity_score**
- Measures semantic similarity of commit messages
- 0.0 = completely different focus
- 1.0 = identical focus
- Impact: Domain similarity

### Codebase Metrics

**affects_core** / **affects_tests** / **affects_infrastructure**
- Boolean flags
- Determines validation requirements

**documentation_intensity**
- Ratio of doc files to total changes
- High = documentation-focused
- Low = code-focused

**code_volume**
- Total lines added + deleted
- Large volumes = significant changes
- Small volumes = targeted fixes

### Diff Metrics

**file_overlap_ratio** (0.0-1.0)
- 0.0 = completely different files
- 1.0 = identical files modified
- 0.6+ = high conflict risk

**conflict_probability** (0.0-1.0)
- Estimated merge conflict likelihood
- 0.1 = low conflict risk
- 0.5+ = high conflict risk

---

## Tag System Reference

### Primary Target (Exactly One)
```
tag:main_branch                    # Integrates to main
tag:scientific_branch              # Integrates to scientific
tag:orchestration_tools_branch     # Integrates to orchestration-tools
```

### Execution Context (Exactly One)
```
tag:parallel_safe                  # Can run in parallel with other branches
tag:sequential_required            # Must run serially (conflict risk)
tag:isolated_execution             # Needs dedicated resources
```

### Complexity (Exactly One)
```
tag:simple_merge                   # Low conflict, fast rebase
tag:moderate_complexity            # Resolvable conflicts, standard process
tag:high_complexity                # Many conflicts, needs integration branch
```

### Content Types (Zero or More)
```
tag:core_code_changes              # Affects core system functionality
tag:test_changes                   # Test file modifications
tag:config_changes                 # Configuration/infrastructure
tag:documentation_only             # Documentation-only
tag:security_sensitive             # Security implications
tag:performance_critical           # Performance-sensitive
```

### Validation Requirements (Zero or More)
```
tag:requires_e2e_testing           # Full end-to-end suite
tag:requires_unit_tests            # Unit test validation
tag:requires_security_review       # Security review needed
tag:requires_performance_testing   # Performance testing needed
```

### Workflow Classification (Zero or More)
```
tag:task_101_orchestration         # Part of Task 101 batch
tag:framework_core                 # Core framework (Tasks 74-83)
tag:framework_extension            # Framework extension
```

---

## Output Files

### 1. categorized_branches.json (Main Output)
```json
[
  {
    "branch": "orchestration-tools-changes",
    "cluster_id": "C_orch_1",
    "target": "orchestration-tools",
    "confidence": 0.95,
    "tags": [
      "tag:orchestration_tools_branch",
      "tag:parallel_safe",
      "tag:high_complexity",
      "tag:core_code_changes",
      "tag:requires_e2e_testing"
    ],
    "reasoning": "Branch name contains orchestration keyword with high confidence",
    "metrics": {
      "commit_history": {...},
      "codebase_structure": {...}
    }
  }
]
```

### 2. clustered_branches.json (Clustering Details)
```json
{
  "clusters": {
    "C1": {
      "name": "Core Features",
      "members": [...],
      "metrics": {...}
    }
  },
  "branch_metrics": {...},
  "total_branches": 24,
  "total_clusters": 5,
  "generated_at": "2025-12-22T..."
}
```

### 3. orchestration_branches.json (Enhanced)
```json
{
  "orchestration_branches": [
    {
      "name": "orchestration-tools",
      "cluster_id": "C_orch_1",
      "target": "orchestration-tools",
      "tags": [...]
    }
  ],
  "count": 24
}
```

---

## Implementation Phases

### Phase 1: Stage One (Weeks 1-4)
- Task 75.1: Commit History Analyzer
- Task 75.2: Codebase Structure Analyzer  
- Task 75.3: Diff Distance Calculator
- Task 75.4: Hierarchical Clustering

### Phase 2: Stage Two (Weeks 5-6)
- Task 75.5: Target Assignment Engine
- Task 75.6: Pipeline Integration

### Phase 3: Validation & Documentation (Weeks 7-8)
- Task 75.7: Visualization & Reporting
- Task 75.8: Comprehensive Testing
- Task 75.9: Framework Integration

**Total: 6-8 weeks with adequate parallelization**

---

## Key Features

### ✅ Intelligent Clustering
- Multi-dimensional similarity analysis
- Hierarchical clustering with dendrograms
- Natural grouping of related features

### ✅ Confident Target Assignment
- Heuristic rules (95% confidence)
- Affinity-based scoring (70% confidence)
- Clear reasoning for each assignment
- Secondary target suggestions

### ✅ Comprehensive Tagging
- 30+ tag types covering all aspects
- Exact counts (1 required primary/context/complexity)
- Enables smart execution strategies

### ✅ Framework Integration
- Direct integration with Tasks 79, 80, 101, 83
- Tag-aware parallel execution
- Tag-based validation selection
- Tag-based test suite selection

### ✅ Orchestration Support
- Special handling for 24 orchestration-tools branches
- Automatic clustering and tagging
- Integration with Task 101

### ✅ Operational Benefits
- Reduced manual branch categorization
- Predictive conflict detection
- Optimized execution strategies
- Better resource utilization
- Improved visibility and documentation

---

## Configuration

### Clustering Parameters
```python
HIERARCHICAL_METHOD = 'ward'        # Clustering algorithm
DISTANCE_THRESHOLD = 0.25           # Cluster separation threshold
MIN_CLUSTER_SIZE = 2                # Minimum members per cluster
```

### Metric Weights
```python
COMMIT_HISTORY_WEIGHT = 0.35        # Commit patterns
CODEBASE_STRUCTURE_WEIGHT = 0.35    # File/code patterns  
DIFF_DISTANCE_WEIGHT = 0.30         # File overlap/conflicts
```

### Target Thresholds
```python
HEURISTIC_CONFIDENCE = 0.95         # Keyword match confidence
ORCHESTRATION_THRESHOLD = 0.75      # For affinity-based assignment
SCIENTIFIC_THRESHOLD = 0.70
MAIN_THRESHOLD = 0.65
```

### Complexity Thresholds
```python
SIMPLE_DIVERGENCE = 0.1             # Divergence ratio limit
SIMPLE_CONFLICT_PROB = 0.1          # Conflict probability limit
MODERATE_DIVERGENCE = 0.5
MODERATE_CONFLICT_PROB = 0.3
```

---

## Usage Examples

### Run Full Pipeline
```bash
python .taskmaster/task_data/branch_clustering_implementation.py

# Outputs:
# - categorized_branches_enhanced.json
# - clustered_branches.json
```

### Query Results
```bash
# View all branches with targets
jq '.[] | {branch, target, confidence}' \
  .taskmaster/task_data/categorized_branches_enhanced.json

# Filter orchestration branches
jq '.[] | select(.tags[] | contains("orchestration"))' \
  .taskmaster/task_data/categorized_branches_enhanced.json

# View clusters
jq '.clusters' .taskmaster/task_data/clustered_branches.json

# Check high-complexity branches
jq '.[] | select(.tags[] | contains("high_complexity"))' \
  .taskmaster/task_data/categorized_branches_enhanced.json
```

### Use in Task 79 (Parallel Execution)
```python
branches = load_categorized_branches()

# Filter by execution tag
parallel_branches = [b for b in branches 
                     if 'tag:parallel_safe' in b['tags']]
sequential_branches = [b for b in branches 
                       if 'tag:sequential_required' in b['tags']]

# Execute sequentially first, then in parallel
for branch in sequential_branches:
    run_alignment(branch)

with ThreadPoolExecutor(max_workers=4) as executor:
    executor.map(run_alignment, parallel_branches)
```

### Use in Task 101 (Orchestration Filter)
```python
branches = load_categorized_branches()
orch_branches = [b for b in branches 
                 if 'tag:orchestration_tools_branch' in b['tags']]

for branch in orch_branches:
    run_task_101_alignment(branch)
```

### Use in Task 80 (Validation Selection)
```python
def validate(branch):
    if 'tag:simple_merge' in branch['tags']:
        run_light_validation(branch)
    elif 'tag:high_complexity' in branch['tags']:
        run_full_validation_suite(branch)
    else:
        run_standard_validation(branch)
```

---

## Success Metrics

### Clustering Quality
- ✅ Silhouette score > 0.5
- ✅ Davies-Bouldin index < 1.0
- ✅ Branches naturally grouped

### Target Assignment
- ✅ 90%+ accuracy vs. known branches
- ✅ Confidence scores well-calibrated
- ✅ Clear reasoning provided

### Tagging Completeness
- ✅ All branches have all required tags
- ✅ Conditional tags appropriately applied
- ✅ No overlapping tags in same category

### Integration Success
- ✅ Task 79 respects execution tags
- ✅ Task 101 filters correctly
- ✅ Task 80 selects validations
- ✅ Task 83 selects tests

### Performance
- ✅ < 2 minutes for 20+ branches
- ✅ < 100 MB memory
- ✅ Valid JSON output

---

## Troubleshooting

### Low Silhouette Score
- Reduce DISTANCE_THRESHOLD
- Increase CLUSTERING_MIN_SIZE
- Verify input metrics are normalized

### Unexpected Target Assignments
- Check heuristic rules applied first (95% confidence)
- Verify affinity scoring makes sense
- Review reasoning in output

### Missing or Wrong Tags
- Verify complexity thresholds are appropriate
- Check file path patterns for content type tags
- Review conditional tag logic

### Integration Issues
- Ensure JSON output format is valid
- Verify all required fields present
- Check downstream task filtering logic

---

## Next Steps

1. **Review** the four documents
2. **Validate** the approach with team
3. **Create** Task Master tasks (9 subtasks)
4. **Implement** starting with Task 75.1
5. **Test** each component progressively
6. **Integrate** with Tasks 79, 80, 101, 83
7. **Document** findings and best practices

---

## Document Map

```
.taskmaster/task_data/
├── branch_clustering_framework.md          (Design & concepts)
├── branch_clustering_implementation.py     (Production code)
├── clustering_tasks_expansion.md           (Task breakdown)
├── CLUSTERING_SYSTEM_SUMMARY.md            (This summary)
├── QUICK_START.md                          (This file)
├── orchestration_branches.json             (24 branches to align)
├── categorized_branches_enhanced.json      (Output - to be generated)
└── clustered_branches.json                 (Output - to be generated)
```

---

## Key Takeaways

### Before (Current Task 75)
```
Branch → Keyword matching → Category (main/scientific/orchestration-tools)
```

### After (Enhanced Task 75)
```
Branch → Commit analysis → Cluster assignment ↓
         Codebase analysis → 
         Diff analysis → Similarity clustering → Target assignment → Comprehensive tagging
         
Result: Categorized + 30+ tags enabling smart execution
```

### Impact
- ✅ Better categorization accuracy
- ✅ Predictive conflict detection
- ✅ Smarter parallel execution
- ✅ Optimized validation selection
- ✅ Improved orchestration handling
- ✅ Better visibility and documentation

---

**Ready to implement? Start with the framework design in `branch_clustering_framework.md`**
