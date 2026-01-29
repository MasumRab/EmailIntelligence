# Two-Stage Branch Identification and Clustering Framework

## Overview

This framework enhances Task 75 (branch categorization) with a sophisticated two-stage clustering approach before final integration target assignment. It provides robust similarity-based grouping before associating branches with main/scientific/orchestration-tools targets.

---

## Stage One: Branch Similarity Clustering

### Objective
Group branches into natural similarity clusters based on:
1. **Commit History Analysis** - Shared ancestry, divergence patterns, commit frequency
2. **NLP/Codebase Structure Similarity** - File path patterns, code metrics, documentation
3. **Minimal Diff Distance** - File overlap, code change proximity, interdependencies

### Components

#### 1.1 Commit History Analyzer
```python
class CommitHistoryAnalyzer:
    """Analyzes Git commit patterns and history divergence"""
    
    def calculate_metrics(branch_name: str, primary_branch: str) -> dict:
        # Metrics:
        # - merge_base_distance: commits since divergence
        # - divergence_ratio: feature commits / primary commits since split
        # - commit_frequency: commits per day
        # - shared_committer_count: number of shared contributors
        # - commit_message_similarity: semantic similarity of messages
        
        return {
            'merge_base_distance': int,
            'divergence_ratio': float,
            'commit_frequency': float,
            'shared_contributors': int,
            'message_similarity_score': float
        }
```

**Git Commands Used:**
- `git merge-base <branch1> <branch2>` - Find common ancestor
- `git log --format=%an,%ae,%ai` - Extract commit metadata
- `git rev-list <commit1>..<commit2> --count` - Count divergent commits

#### 1.2 NLP/Codebase Structure Analyzer
```python
class CodebaseStructureAnalyzer:
    """Analyzes file patterns, directory structure, and code characteristics"""
    
    def calculate_metrics(branch_name: str) -> dict:
        # Metrics:
        # - modified_paths: set of directories/files touched
        # - file_type_distribution: distribution of file extensions
        # - code_metrics: lines added/deleted, cyclomatic complexity indicators
        # - directory_clustering: which top-level dirs are affected
        # - documentation_changes: doc file modifications
        # - configuration_changes: config file modifications
        
        return {
            'core_directories': list[str],
            'file_type_distribution': dict,
            'code_volume': int,
            'affects_core': bool,
            'affects_tests': bool,
            'affects_infrastructure': bool,
            'documentation_intensity': float,
            'config_change_count': int
        }
```

**NLP Approaches:**
- Path tokenization: Split paths into semantic tokens
- Commit message embedding: Use pre-trained models (e.g., Sentence-BERT)
- Directory name similarity: Semantic similarity between directory names

#### 1.3 Diff Distance Calculator
```python
class DiffDistanceCalculator:
    """Calculates file and code change distance between branches"""
    
    def calculate_metrics(branch1: str, branch2: str) -> dict:
        # Metrics:
        # - file_overlap_ratio: percentage of files both modify
        # - min_edit_distance: Levenshtein distance on changed file lists
        # - code_change_proximity: how close together in code are changes
        # - conflict_likelihood: estimated merge conflict probability
        
        return {
            'file_overlap_ratio': float,  # 0.0 - 1.0
            'edit_distance': int,
            'change_proximity_score': float,
            'conflict_probability': float  # 0.0 - 1.0
        }
```

**Git Commands Used:**
- `git diff --name-only <branch1> <branch2>` - Changed files
- `git diff --stat <branch1> <branch2>` - Change statistics
- `git diff <branch1> <branch2>` - Full diffs for analysis

### Stage One Output: Similarity Matrix

```json
{
  "clusters": [
    {
      "cluster_id": "C1",
      "cluster_name": "Core Feature Development",
      "members": [
        {
          "branch": "feature/auth-system",
          "similarity_score": 0.92,
          "cluster_confidence": 0.95
        },
        {
          "branch": "feature/oauth-integration",
          "similarity_score": 0.89,
          "cluster_confidence": 0.93
        }
      ],
      "cluster_characteristics": {
        "avg_divergence_days": 45,
        "avg_file_overlap": 0.68,
        "primary_directories": ["src/auth", "src/security"],
        "commit_frequency": "daily",
        "avg_conflict_probability": 0.15
      }
    }
  ],
  "branch_metrics": {
    "feature/auth-system": {
      "commit_history": { /* 1.1 metrics */ },
      "codebase_structure": { /* 1.2 metrics */ },
      "diff_distance": { /* 1.3 metrics */ }
    }
  }
}
```

---

## Stage Two: Integration Target Assignment & Tagging

### Objective
Map clusters to integration targets (main/scientific/orchestration-tools) using:
1. Cluster characteristics
2. Directory affinity heuristics
3. Historical precedent
4. User-defined rules

### 2.1 Target Assignment Logic

```python
class IntegrationTargetAssigner:
    """Assigns branches to integration targets based on clustering"""
    
    def assign_target(cluster: dict, branch: dict) -> dict:
        """
        Decision tree for target assignment:
        
        1. Heuristic Rules (highest priority)
           - If branch name contains "orchestration" → orchestration-tools
           - If modifies "scientific/" → scientific
           - If modifies "ai/" → scientific
           
        2. Directory Affinity Scoring
           - orchestration_tools_affinity = score if modifies orchestration/* 
           - scientific_affinity = score if modifies scientific/* or ai/*
           - main_affinity = default if no strong signal
           
        3. Cluster Consensus
           - If cluster members mostly target one branch → assign same
           - Use weighted voting across cluster members
           
        4. Historical Precedent
           - Check if similar branches (by commit author, similar files) 
             targeted specific branch historically
        """
        
        return {
            'primary_target': 'main' | 'scientific' | 'orchestration-tools',
            'secondary_targets': list[str],
            'confidence': float,
            'reasoning': str,
            'override_applicable': bool
        }
```

**Heuristic Rules:**
```
IF branch_name CONTAINS ('orchestration', 'orchestration-tools')
  THEN target = 'orchestration-tools'

IF branch_name CONTAINS ('scientific', 'ml', 'ai', 'model')
  THEN target = 'scientific'

IF modified_paths CONTAIN 'orchestration/'
  THEN target = 'orchestration-tools' (high confidence)

IF modified_paths CONTAIN 'scientific/' OR 'ai/'
  THEN target = 'scientific' (high confidence)

IF cluster_centroid CLOSER_TO scientific_cluster
  THEN target = 'scientific'
```

### 2.2 Tag System Definition

Tags differentiate task execution contexts and resources:

#### Primary Tags (Integration Target)
- `tag:main-branch` - Tasks targeting main branch integration
- `tag:scientific-branch` - Tasks targeting scientific branch integration  
- `tag:orchestration-tools-branch` - Tasks targeting orchestration-tools branch integration

#### Execution Context Tags
- `tag:parallel-safe` - Can run in parallel with other branches
- `tag:sequential-required` - Must run serially (high conflict risk)
- `tag:isolated-execution` - Requires independent resource allocation

#### Complexity Tags
- `tag:simple-merge` - Fast-forward or trivial merge
- `tag:moderate-complexity` - Resolvable conflicts, standard rebase
- `tag:high-complexity` - Long-lived, many conflicts, needs integration branch

#### Content Type Tags
- `tag:core-code-changes` - Affects core system functionality
- `tag:test-changes` - Primarily test file modifications
- `tag:config-changes` - Configuration/infrastructure changes
- `tag:documentation-only` - Documentation-only changes

#### Validation Tags
- `tag:requires-e2e-testing` - Needs end-to-end test suite
- `tag:requires-unit-tests` - Needs unit test validation
- `tag:requires-security-review` - Security implications present
- `tag:requires-performance-testing` - Performance-sensitive changes

#### Workflow Tags
- `tag:task-101-orchestration` - Part of Task 101 orchestration batch
- `tag:framework-core` - Part of core framework (Tasks 74-83)
- `tag:framework-extension` - Extends framework for specific case

### 2.3 Task Creation Template

For each branch cluster + target combination, create/tag tasks:

```json
{
  "id": "75.X",
  "title": "Align [Cluster Name] branches to [Target]",
  "description": "Align cluster [C1] (N members) to [target] branch",
  "tags": [
    "tag:main-branch",           // primary target
    "tag:parallel-safe",          // execution context
    "tag:moderate-complexity",    // complexity
    "tag:core-code-changes",      // content type
    "tag:requires-e2e-testing"    // validation
  ],
  "details": {
    "cluster_id": "C1",
    "cluster_members": ["branch1", "branch2", ...],
    "target_branch": "main",
    "similarity_metrics": { /* from Stage One */ },
    "affinity_scores": { /* scoring details */ },
    "estimated_conflict_count": 3,
    "estimated_complexity": "moderate",
    "estimated_time_hours": 4.5
  },
  "dependencies": ["75.Y"]  // depends on similar cluster completion
}
```

---

## Integration with Existing Framework

### Modification to Task 75

**Current Task 75:** Basic branch identification and categorization
**Enhanced Task 75:** Two-stage clustering + categorization + tagging

```python
def enhanced_branch_categorization():
    """Enhanced Task 75 implementation"""
    
    # Stage One: Clustering
    branches = get_remote_feature_branches()
    history_analyzer = CommitHistoryAnalyzer()
    structure_analyzer = CodebaseStructureAnalyzer()
    diff_calculator = DiffDistanceCalculator()
    
    branch_metrics = {}
    for branch in branches:
        branch_metrics[branch] = {
            'commit_history': history_analyzer.calculate_metrics(branch, 'main'),
            'codebase_structure': structure_analyzer.calculate_metrics(branch),
            'diff_distances': {
                other: diff_calculator.calculate_metrics(branch, other)
                for other in branches if other != branch
            }
        }
    
    # Clustering using hierarchical or k-means
    clusters = cluster_branches(branch_metrics)
    
    # Stage Two: Target Assignment & Tagging
    assigner = IntegrationTargetAssigner()
    results = []
    for cluster in clusters:
        for branch in cluster['members']:
            target_assignment = assigner.assign_target(cluster, branch)
            tags = generate_tags(cluster, branch, target_assignment)
            
            results.append({
                'branch': branch,
                'cluster': cluster['id'],
                'target': target_assignment['primary_target'],
                'secondary_targets': target_assignment['secondary_targets'],
                'confidence': target_assignment['confidence'],
                'tags': tags,
                'reasoning': target_assignment['reasoning']
            })
    
    # Output both categorized_branches.json and clustered_branches.json
    save_categorized_branches(results)
    save_clustered_branches({
        'clusters': clusters,
        'branch_metrics': branch_metrics
    })
    
    return results
```

### Task 79 Modifications (Parallel Execution)

Use tags to control parallel execution:

```python
def run_alignment_for_target_group(target: str, branches: list):
    """Modified from Task 79"""
    
    # Filter by execution context tags
    parallel_safe = [b for b in branches if 'tag:parallel-safe' in b['tags']]
    sequential = [b for b in branches if 'tag:sequential-required' in b['tags']]
    
    # Execute sequential first
    for branch in sequential:
        run_alignment_for_branch(branch)
    
    # Then execute parallel-safe concurrently
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(run_alignment_for_branch, b) for b in parallel_safe]
        for future in as_completed(futures):
            result = future.result()
```

### Task 101 Integration

Task 101 (orchestration-tools branches) automatically filtered:

```python
def task_101_orchestrator():
    """Filter Task 101 branches using tags"""
    
    all_branches = load_categorized_branches()
    orchestration_branches = [
        b for b in all_branches 
        if 'tag:orchestration-tools-branch' in b['tags']
    ]
    
    # Process orchestration branches with local framework
    for branch in orchestration_branches:
        run_task_101_alignment(branch)
```

---

## Data Structures

### orchestration_branches.json (Enhanced)

```json
{
  "orchestration_branches": [
    {
      "name": "orchestration-tools",
      "cluster_id": "C_orch_1",
      "similarity_score": 0.95,
      "target": "orchestration-tools",
      "tags": [
        "tag:orchestration-tools-branch",
        "tag:parallel-safe",
        "tag:high-complexity",
        "tag:core-code-changes"
      ],
      "metrics": {
        "divergence_days": 120,
        "commit_count": 47,
        "file_overlap_with_main": 0.23
      }
    }
  ],
  "metadata": {
    "clustering_version": "2.0",
    "stage_one_complete": true,
    "stage_two_complete": true,
    "generated_at": "2025-12-22T00:00:00.000Z"
  }
}
```

### clustered_branches.json (New)

```json
{
  "clusters": [
    {
      "id": "C1",
      "name": "Core Feature Development",
      "size": 3,
      "members": [
        "feature/auth-system",
        "feature/oauth-integration",
        "feature/mfa-support"
      ],
      "metrics": {
        "avg_commit_history_distance": 45,
        "avg_code_similarity": 0.78,
        "avg_file_overlap": 0.62,
        "avg_conflict_probability": 0.18,
        "recommended_execution_order": ["feature/auth-system", "feature/oauth-integration", "feature/mfa-support"]
      }
    },
    {
      "id": "C_orch_1", 
      "name": "Orchestration Tools Cluster",
      "size": 8,
      "members": ["orchestration-tools", "orchestration-tools-changes", ...],
      "metrics": { /* orchestration-specific */ }
    }
  ],
  "affinity_assignments": {
    "C1": {
      "main_affinity": 0.92,
      "scientific_affinity": 0.15,
      "orchestration_affinity": 0.08,
      "assigned_target": "main"
    }
  }
}
```

---

## Implementation Phases

### Phase 1: Stage One Implementation (Task 75.1)
- Implement CommitHistoryAnalyzer
- Implement CodebaseStructureAnalyzer
- Implement DiffDistanceCalculator
- Generate similarity matrix and clusters
- Output: `clustered_branches.json`

### Phase 2: Stage Two Implementation (Task 75.2)
- Implement IntegrationTargetAssigner
- Define heuristic rules
- Implement tag generation
- Modify output to include tags
- Output: Enhanced `categorized_branches.json` with tags

### Phase 3: Framework Integration (Task 75.3)
- Integrate with Task 79 parallel execution
- Update Task 101 for tag-based filtering
- Update Task 80 validation for tag-based execution
- Implement tag-aware logging and reporting

### Phase 4: Visualization & Reporting (Task 75.4)
- Generate cluster dendrograms
- Create similarity heatmaps
- Generate target assignment explanations
- Build tag-based execution plan visualization

---

## Configuration & Thresholds

```python
# Stage One: Clustering Parameters
COMMIT_HISTORY_WEIGHT = 0.35
CODEBASE_STRUCTURE_WEIGHT = 0.35
DIFF_DISTANCE_WEIGHT = 0.30

# Clustering algorithm: Hierarchical Agglomerative (HAC)
CLUSTERING_METHOD = 'ward'
DISTANCE_THRESHOLD = 0.25  # Maximum distance to merge clusters

# Stage Two: Target Assignment
ORCHESTRATION_TOOLS_CONFIDENCE_THRESHOLD = 0.75
SCIENTIFIC_CONFIDENCE_THRESHOLD = 0.70
MAIN_CONFIDENCE_THRESHOLD = 0.65

# Tag-based execution
MAX_PARALLEL_WORKERS = 4
SEQUENTIAL_REQUIRED_COOLDOWN = 30  # seconds between sequential tasks
```

---

## Benefits Over Current Approach

| Aspect | Current (Task 75) | Enhanced Two-Stage | Benefit |
|--------|---|---|---|
| **Grouping** | Individual branch analysis | Cluster-based | Identifies related features, enables batch alignment |
| **Similarity Detection** | Keyword/directory heuristics | Multi-dimensional metrics | More accurate target assignment |
| **Conflict Prediction** | Post-merge discovery | Pre-alignment probability | Enables proactive strategy selection |
| **Execution Planning** | Flat list of branches | Cluster + tag-based DAG | Better parallelization and risk isolation |
| **Documentation** | Basic categorization | Detailed reasoning + confidence | Transparency and auditability |
| **Maintainability** | Hard-coded rules | Configuration-based + ML-ready | Easier to adapt and improve |

---

## Future Enhancements

1. **Machine Learning Integration**
   - Train model on historical successful/failed alignments
   - Use for target prediction and conflict likelihood estimation

2. **Interactive Conflict Resolution**
   - Suggest conflict resolution strategies based on cluster patterns
   - Learn from developer choices

3. **Automated Reordering**
   - Suggest optimal alignment order to minimize cascading conflicts
   - Use topological sort on cluster dependency graph

4. **Cross-Cluster Integration**
   - Identify branches that depend on other clusters
   - Add inter-cluster dependencies to Task 79 orchestrator

5. **Continuous Learning**
   - Track actual vs. predicted metrics
   - Refine heuristics based on outcomes
