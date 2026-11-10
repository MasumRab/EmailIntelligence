# Task 002: Branch Clustering System - Implementation Guide

**Complete Step-by-Step Guide for Implementing All Subtasks**

---

## Table of Contents

1. [Execution Strategies & Timeline](#execution-strategies--timeline)
2. [Subtask 002.1: CommitHistoryAnalyzer](#subtask-0021-commithistoryanalyzer)
3. [Subtask 002.2: CodebaseStructureAnalyzer](#subtask-0022-codebasestructureanalyzer)
4. [Subtask 002.3: DiffDistanceCalculator](#subtask-0023-diffdistancecalculator)
5. [Subtask 002.4: BranchClusterer](#subtask-0024-branchclusterer)
6. [Subtask 002.5: IntegrationTargetAssigner](#subtask-0025-integrationtargetassigner)
7. [Integration Testing](#integration-testing)
8. [Performance Benchmarking](#performance-benchmarking)
9. [Troubleshooting](#troubleshooting)

---

## Execution Strategies & Timeline

### Strategy 1: Full Parallel (Recommended - 3 weeks)

**Week 1: Parallel Stage One (24-40 hours each)**

| Day | Team A | Team B | Team C |
|-----|--------|--------|--------|
| 1-2 | 002.1.1-002.1.2 | 002.2.1-002.2.2 | 002.3.1-002.3.2 |
| 2-3 | 002.1.3-002.1.5 | 002.2.3-002.2.5 | 002.3.3-002.3.5 |
| 3-4 | 002.1.6-002.1.8 | 002.2.6-002.2.8 | 002.3.6-002.3.8 |
| 4 | Unit testing & code review | Unit testing & code review | Unit testing & code review |

**Week 2: Sequential Stage One Integration (28-36 hours)**

- All teams integrate outputs into Task 002.4
- Team D implements 002.4 (BranchClusterer)
- Takes input from all three analyzer teams

**Week 3: Target Assignment & Integration Testing (24-32 hours)**

- Team E implements 002.5 (IntegrationTargetAssigner)
- All teams perform integration testing
- Performance benchmarking and tuning
- Final code review and documentation

### Strategy 2: Sequential (4 weeks)

Follow order: 002.1 → 002.2 → 002.3 → 002.4 → 002.5

**Best for:** Single developer or limited resources. Slower but simpler coordination.

### Strategy 3: Hybrid (3.5 weeks)

- Week 1: Tasks 002.1 + 002.2 (some parallelization possible)
- Week 2: Tasks 002.3 + 002.4 (start 002.4 once 002.1-002.2 complete)
- Week 3: Task 002.5 + comprehensive testing

---

## Subtask 002.1: CommitHistoryAnalyzer

### Overview

Extract and score commit history metrics for branches. This analyzer measures:
- **Commit Recency:** How recent are the latest commits?
- **Commit Frequency:** Commit rate relative to branch age
- **Authorship Diversity:** Number of unique contributors
- **Merge Readiness:** How many commits behind main?
- **Stability Score:** Consistency of commit patterns

### Quick Reference

```python
class CommitHistoryAnalyzer:
    def __init__(self, repo_path: str, main_branch: str = "main")
    def analyze(self, branch_name: str) -> dict
```

Returns:
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

### Sub-subtasks & Timeline

#### **002.1.1: Design Metric System (2-3 hours)**

**Steps:**
1. Define all 5 metrics with mathematical formulas
2. Document normalization approach (ensure [0,1] range)
3. Create weighting scheme (must sum to 1.0)
4. Document edge case handling

**Success Criteria:**
- [ ] All 5 metrics clearly defined with formulas
- [ ] Calculation approach specified
- [ ] Normalization approach specified
- [ ] Weights documented
- [ ] Edge case handling documented

---

#### **002.1.2: Set Up Git Data Extraction (4-5 hours)**

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

#### **002.1.3: Implement Commit Recency Metric (3-4 hours)**

**Steps:**
1. Extract most recent commit date
2. Calculate time since last commit
3. Implement exponential decay function
4. Normalize to [0,1] range
5. Test with recent, old branches

**Success Criteria:**
- [ ] Returns value in [0, 1] range
- [ ] Recent commits (last 7 days) score > 0.8
- [ ] Old commits (90+ days) score < 0.3
- [ ] Correctly handles single-commit branches
- [ ] Consistent calculation across test cases

---

#### **002.1.4: Implement Commit Frequency Metric (3-4 hours)**

**Steps:**
1. Calculate commits per day (commits/branch_lifetime_days)
2. Handle single-commit branches (avoid division by zero)
3. Define frequency baseline and scoring
4. Normalize to [0,1] range
5. Test with high and low activity branches

**Success Criteria:**
- [ ] Returns value in [0, 1] range
- [ ] High activity (>5 commits/week) scores > 0.7
- [ ] Low activity (<1 commit/week) scores < 0.4
- [ ] Correctly handles single-commit branches
- [ ] Handles very old branches (>100 days)

---

#### **002.1.5: Implement Authorship & Stability Metrics (4-5 hours)**

**Steps for authorship_diversity:**
1. Extract unique author names from commits
2. Calculate diversity ratio (unique authors / total commits)
3. Normalize to [0,1] range

**Steps for stability_score:**
1. Extract line change statistics per commit
2. Calculate average churn per commit
3. Define stability baseline (inverse of churn)
4. Normalize to [0,1] range

**Success Criteria:**
- [ ] Authorship: Returns value in [0, 1] range
- [ ] Authorship: Single author scores ~0.3, multiple authors score higher
- [ ] Stability: Returns value in [0, 1] range
- [ ] Stability: Low churn scores > 0.7, high churn scores < 0.4
- [ ] Handles edge cases (binary files, deletions)

---

#### **002.1.6: Implement Merge Readiness Metric (3-4 hours)**

**Steps:**
1. Find merge base between branch and main
2. Count commits behind main
3. Calculate how far behind as normalized score
4. Normalize to [0,1] (inverse: more behind = lower score)

**Success Criteria:**
- [ ] Returns value in [0, 1] range
- [ ] Recently synced (<5 commits behind) scores > 0.85
- [ ] Far behind (>50 commits behind) scores < 0.4
- [ ] Correctly handles branches merged from main
- [ ] Handles newly-created branches

---

#### **002.1.7: Implement Aggregation & Weighting (2-3 hours)**

**Steps:**
1. Define metric weights (0.25/0.20/0.20/0.20/0.15, sum = 1.0)
2. Create weighted aggregation function
3. Verify all metrics in [0,1] before aggregating
4. Format output dict with all required fields
5. Add ISO timestamp

**Success Criteria:**
- [ ] Aggregate score = 0.25×m1 + 0.20×m2 + 0.20×m3 + 0.20×m4 + 0.15×m5
- [ ] Returns value in [0, 1] range
- [ ] Output dict has all required fields
- [ ] Timestamp in ISO format
- [ ] No missing or extra fields

---

#### **002.1.8: Unit Testing & Edge Cases (3-4 hours)**

**Steps:**
1. Create test fixtures with various branch characteristics
2. Implement minimum 8 unit test cases
3. Mock git commands for reliable testing
4. Add performance benchmarks
5. Generate coverage report (target: >95%)

**Success Criteria:**
- [ ] Minimum 8 comprehensive test cases implemented
- [ ] All tests pass on CI/CD
- [ ] Code coverage >95%
- [ ] Edge cases covered (new, stale, orphaned branches)
- [ ] Error handling tested
- [ ] Output validation includes JSON schema check
- [ ] Performance tests meet <2 second requirement

### Key Implementation Notes

**Git Commands:**
```bash
# Get commits on branch relative to main
git log main..BRANCH_NAME --pretty=format:"%H|%ai|%an|%s"

# Get merge base
git merge-base main BRANCH_NAME

# Count commits behind
git rev-list --count BRANCH_NAME..main
```

**Timeout Strategy:**
```python
result = subprocess.run(
    cmd, 
    timeout=30,  # CRITICAL: Prevents hanging on large repos
    capture_output=True,
    text=True,
    encoding='utf-8'
)
```

**Edge Cases:**
- New branch (single commit, <1 hour old) → Default safe values
- Stale branch (90+ days old) → Low recency score
- Orphaned branch (no common ancestor) → Handle gracefully
- Large repos (10,000+ commits) → Use timeout protection

---

## Subtask 002.2: CodebaseStructureAnalyzer

### Overview

Measure codebase structure similarity between branches using directory and file analysis.

Metrics:
- **Directory Similarity:** Jaccard similarity of directory trees
- **File Additions:** Ratio of new files (inverted)
- **Core Module Stability:** Preservation of critical modules
- **Namespace Isolation:** New packages properly isolated

### Quick Reference

```python
class CodebaseStructureAnalyzer:
    def __init__(self, repo_path: str, main_branch: str = "main")
    def analyze(self, branch_name: str) -> dict
```

Returns:
```json
{
  "branch_name": "feature/auth",
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

### Sub-subtasks & Timeline

**002.2.1: Design Structure Analysis Architecture (2-3 hours)**
- Design Jaccard similarity calculation
- Define core modules list
- Document file addition scoring
- Design namespace isolation logic

**002.2.2: Implement Git Tree Extraction (3-4 hours)**
- Implement `git ls-tree -r --name-only` execution
- Extract file lists for both main and target branch
- Parse into directory sets
- Handle non-existent branches

**002.2.3: Implement Directory Similarity Metric (3-4 hours)**
- Extract directories from file paths
- Compute Jaccard similarity
- Normalize to [0,1]
- Test with various branch types

**002.2.4: Implement File Additions Metric (3-4 hours)**
- Count new files relative to main
- Invert score (many new files = lower score)
- Normalize to [0,1]
- Test edge cases

**002.2.5: Implement Core Module Stability Metric (3-4 hours)**
- Define critical modules (src/, tests/, config/, etc.)
- Check if modified or deleted
- Score: 1.0 if unchanged, 0.5 if modified, 0.0 if deleted
- Normalize to [0,1]

**002.2.6: Implement Namespace Isolation Metric (3-4 hours)**
- Measure how well new files are grouped
- Use clustering coefficient for isolation
- Normalize to [0,1]
- Test with well-isolated and scattered changes

**002.2.7: Implement Aggregation & Weighting (2-3 hours)**
- Combine 4 metrics using weights: 0.30/0.25/0.25/0.20
- Ensure result in [0,1]
- Format output JSON

**002.2.8: Unit Testing & Validation (3-4 hours)**
- Write 8+ unit tests (>95% coverage)
- Test large repos (1,000+ files)
- Performance: <2 seconds per branch
- Test UTF-8 and special characters in paths

### Key Implementation Notes

**Git Commands:**
```bash
# Get all files in a branch
git ls-tree -r --name-only BRANCH_NAME

# Compare with main
git diff --name-only main BRANCH_NAME
```

**Jaccard Similarity:**
```python
def jaccard_similarity(set1, set2):
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    if union == 0:
        return 0.5  # Default for identical empty sets
    return intersection / union
```

**Core Modules:**
```python
CORE_MODULES = [
    'src/',
    'tests/',
    'config/',
    'build/',
    'dist/',
    'docs/',
    'setup.py',
    'requirements.txt'
]
```

---

## Subtask 002.3: DiffDistanceCalculator

### Overview

Compute code distance metrics by analyzing diffs between branches.

Metrics:
- **Code Churn:** Lines changed relative to codebase size
- **Change Concentration:** How files changes are distributed
- **Diff Complexity:** Large diffs in few files
- **Integration Risk:** Pattern-based risk categorization

### Quick Reference

```python
class DiffDistanceCalculator:
    def __init__(self, repo_path: str, main_branch: str = "main")
    def analyze(self, branch_name: str) -> dict
```

Returns:
```json
{
  "branch_name": "feature/auth",
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

### Sub-subtasks & Timeline

**002.3.1: Design Diff Analysis Architecture (3-4 hours)**
- Design code churn calculation
- Define risk categories (critical, high, medium, low)
- Create risk file patterns
- Document metrics approach

**002.3.2: Implement Git Diff Extraction (4-5 hours)**
- Implement `git diff main...BRANCH_NAME --numstat`
- Parse added/deleted lines per file
- Identify file types
- Handle binary files

**002.3.3: Implement Code Churn Metric (3-4 hours)**
- Calculate total changes (added + deleted)
- Normalize by estimated codebase size
- Invert (lower churn = higher score)
- Normalize to [0,1]

**002.3.4: Implement Change Concentration Metric (3-4 hours)**
- Count files affected
- Calculate distribution ratio
- Normalize to [0,1]
- Test single-file and multi-file branches

**002.3.5: Implement Diff Complexity Metric (3-4 hours)**
- Find largest diff
- Compute concentration ratio
- Normalize to [0,1]
- Test edge cases

**002.3.6: Implement Integration Risk Metric (3-4 hours)**
- Categorize files by risk level
- Weight by file type and location
- Sum weighted risks
- Normalize to [0,1]

**002.3.7: Implement Aggregation & Weighting (2-3 hours)**
- Combine 4 metrics using weights: 0.30/0.25/0.25/0.20
- Ensure result in [0,1]
- Format output JSON

**002.3.8: Unit Testing & Validation (4-5 hours)**
- Write 8+ unit tests (>95% coverage)
- Test large diffs (100,000+ lines)
- Test binary files and merge commits
- Performance: <3 seconds per branch

### Key Implementation Notes

**Git Commands:**
```bash
# Get diff statistics
git diff main...BRANCH_NAME --numstat

# Use three-dot syntax to exclude merge commits
```

**Risk Categorization:**
```python
RISK_PATTERNS = {
    'critical': ['security/', 'auth/', 'database/migrations/'],
    'high': ['src/', 'core/', 'main.py'],
    'medium': ['utils/', 'helpers/', 'tests/'],
    'low': ['docs/', 'examples/', 'README.md']
}
```

**Handle Binary Files:**
```python
if added == '-' or deleted == '-':
    continue  # Skip binary files in line counting
```

---

## Subtask 002.4: BranchClusterer

### Overview

Perform hierarchical agglomerative clustering on analyzed branches using Ward linkage.

Input: Outputs from 002.1, 002.2, 002.3
Output: Cluster assignments + quality metrics

### Quick Reference

```python
class BranchClusterer:
    def __init__(self, repo_path: str)
    def cluster(self, analyzer_outputs: List[dict]) -> dict
```

### Sub-subtasks & Timeline

**002.4.1: Design Clustering Architecture (3-4 hours)**
- Review hierarchical agglomerative clustering
- Document Ward linkage method
- Define quality metrics (silhouette, Davies-Bouldin, Calinski-Harabasz)
- Document dendrogram threshold strategy

**002.4.2: Implement Metric Combination System (4-5 hours)**
- Accept outputs from 002.1, 002.2, 002.3
- Validate all required fields
- Implement weighted combination: 0.35×002.1 + 0.35×002.2 + 0.30×002.3
- Test with multiple branches

**002.4.3: Implement Distance Matrix Calculation (3-4 hours)**
- Extract metric vectors for all branches
- Compute pairwise Euclidean distances
- Verify symmetry and zero diagonal
- Performance: <1 second for 50 branches

**002.4.4: Implement Hierarchical Clustering Engine (4-5 hours)**
- Perform Ward linkage clustering
- Generate dendrogram
- Cut dendrogram at threshold
- Assign clusters

**002.4.5: Implement Quality Metrics (3-4 hours)**
- Compute silhouette score
- Compute Davies-Bouldin index
- Compute Calinski-Harabasz index
- All complete <2 seconds for 50 branches

**002.4.6: Implement Output Formatting (2-3 hours)**
- Format cluster assignments with characteristics
- Include quality metrics and threshold
- Generate JSON output
- Validate schema

**002.4.7: Implement Validation & Edge Cases (2-3 hours)**
- Handle all-similar branches (ensure multiple clusters)
- Validate Ward linkage requirements
- Check distance matrix properties
- Test with 50+ branches

**002.4.8: Unit Testing & Performance (4-5 hours)**
- Write 8+ unit tests (>95% coverage)
- Test clustering algorithms
- Performance: <10 seconds for 50+ branches
- Memory: <100 MB

### Key Implementation Notes

**Metric Combination:**
```python
combined_score = (
    0.35 * commit_history_analyzer.aggregate_score +
    0.35 * codebase_structure_analyzer.aggregate_score +
    0.30 * diff_distance_calculator.aggregate_score
)
```

**Distance Matrix:**
```python
from scipy.spatial.distance import pdist, squareform

condensed = pdist(vectors, metric='euclidean')
distance_matrix = squareform(condensed)

# Ensure symmetry
distance_matrix = (distance_matrix + distance_matrix.T) / 2.0
np.fill_diagonal(distance_matrix, 0)
```

**Ward Linkage:**
```python
from scipy.cluster.hierarchy import linkage, fcluster

Z = linkage(distance_matrix, method='ward')
clusters = fcluster(Z, t=threshold, criterion='distance')
```

**Quality Metrics:**
```python
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score

silhouette = silhouette_score(vectors, clusters)  # Range: [-1, 1], higher is better
davies_bouldin = davies_bouldin_score(vectors, clusters)  # Range: [0, ∞], lower is better
calinski_harabasz = calinski_harabasz_score(vectors, clusters)  # Range: [0, ∞], higher is better
```

---

## Subtask 002.5: IntegrationTargetAssigner

### Overview

Assign integration targets to branches and generate comprehensive tagging system.

Input: Cluster output from 002.4
Output: Target assignments + 30+ tags per branch

### Quick Reference

```python
class IntegrationTargetAssigner:
    def __init__(self, repo_path: str)
    def assign(self, cluster_output: dict) -> dict
```

### Sub-subtasks & Timeline

**002.5.1: Design Target Assignment Hierarchy (2-3 hours)**
- Design 4-level decision hierarchy
- Define heuristic rules for Level 1
- Document affinity scoring for Level 2
- Define fallback for Level 4

**002.5.2: Implement Heuristic Rule Engine (4-5 hours)**
- Create rules-based assignment logic
- Implement confidence scoring
- Add reasoning generation
- Handle rule conflicts

**002.5.3: Implement Tag Generation System (5-6 hours)**
- Generate tags from 6 categories
- Ensure 30+ unique tags per branch
- Validate tag mutual exclusivity
- Create conditional tag logic

**002.5.4: Implement Affinity Scoring (3-4 hours)**
- Define target archetypes (main, scientific, orchestration-tools)
- Compute affinity to each archetype
- Normalize to [0,1]
- Test against known examples

**002.5.5: Implement Confidence Scoring (3-4 hours)**
- Weight factors: rule match, metric agreement, cluster cohesion
- Ensure result in [0,1]
- Validate no NaN values
- Test edge cases

**002.5.6: Implement Reasoning Generation (3-4 hours)**
- Generate human-readable reasoning for assignment
- Template-based explanation
- Include supporting metrics
- Enforce 50-500 character bounds

**002.5.7: Implement Output Formatting (2-3 hours)**
- Format assignments with all metadata
- Include archetypes affinities
- Generate JSON output
- Validate schema

**002.5.8: Unit Testing & Validation (3-4 hours)**
- Write 8+ unit tests (>95% coverage)
- Test tag generation (30+ per branch)
- Test confidence scoring
- Performance: <1 second per branch

### Key Implementation Notes

**4-Level Decision Hierarchy:**
```python
def hierarchical_assignment(branch_metrics, cluster_data):
    # Level 1: Heuristic rules
    target, conf = level1_heuristics(branch_metrics)
    if conf > 0.90:
        return target, conf, "Level 1: Heuristic match"
    
    # Level 2: Affinity scoring
    target, conf = level2_affinity(branch_metrics, archetypes)
    if conf > 0.70:
        return target, conf, "Level 2: Affinity match"
    
    # Level 3: Cluster consensus
    target, conf = level3_consensus(branch_metrics, cluster_data)
    if conf > 0.60:
        return target, conf, "Level 3: Cluster consensus"
    
    # Level 4: Default
    return level4_default(), 0.50, "Level 4: Default assignment"
```

**Tag Categories:**
```python
TAG_CATEGORIES = {
    'primary_target': 3,  # main_branch, scientific_branch, orchestration_tools_branch
    'execution_context': 3,  # parallel_safe, sequential_required, isolated_execution
    'complexity': 3,  # simple_merge, moderate_complexity, high_complexity
    'content_type': 6,  # core_code, test_changes, config_changes, docs, security, performance
    'validation': 4,  # e2e_testing, unit_tests, security_review, performance_testing
    'workflow': 3,  # task_101, framework_core, framework_extension
    # Total minimum: 3+3+3+6+4+3 = 22, need 30+ total → add conditional tags
}
```

**Archetype Definition:**
```python
ARCHETYPES = {
    'main': {
        'merge_readiness_min': 0.85,
        'risk_tolerance': 0.30,
        'churn_tolerance': 0.40,
        'priority_boost': 1.2
    },
    'scientific': {
        'merge_readiness_min': 0.65,
        'risk_tolerance': 0.50,
        'churn_tolerance': 0.80,
        'priority_boost': 1.0
    },
    'orchestration-tools': {
        'merge_readiness_min': 0.75,
        'core_module_changes': True,
        'parallel_safety': True,
        'priority_boost': 1.1
    }
}
```

---

## Integration Testing

### Cross-Component Tests

**Test 1: End-to-End Pipeline**
```python
def test_full_pipeline():
    repo = TestRepository()  # Create test repo with branches
    
    # Run all analyzers
    commit_results = CommitHistoryAnalyzer(repo).analyze('feature/test')
    structure_results = CodebaseStructureAnalyzer(repo).analyze('feature/test')
    diff_results = DiffDistanceCalculator(repo).analyze('feature/test')
    
    # Validate analyzer outputs
    assert commit_results['aggregate_score'] in [0, 1]
    assert structure_results['aggregate_score'] in [0, 1]
    assert diff_results['aggregate_score'] in [0, 1]
    
    # Cluster
    analyzer_outputs = [commit_results, structure_results, diff_results]
    clusterer = BranchClusterer(repo)
    cluster_results = clusterer.cluster(analyzer_outputs)
    
    # Assign targets
    assigner = IntegrationTargetAssigner(repo)
    assignments = assigner.assign(cluster_results)
    
    # Validate final output
    assert 'branch_name' in assignments
    assert 'assigned_target' in assignments
    assert len(assignments['tags']) >= 30
    assert assignments['confidence'] in [0, 1]
```

**Test 2: Data Format Consistency**
```python
def test_data_format_consistency():
    # Ensure all outputs follow expected schemas
    
    # Validate analyzer outputs are dicts with required fields
    assert all(k in result for k in ['metrics', 'aggregate_score', 'branch_name'])
    
    # Validate cluster output structure
    assert 'clusters' in cluster_result
    assert 'quality_metrics' in cluster_result
    
    # Validate assignment output
    assert 'assigned_target' in assignment_result
    assert assignment_result['assigned_target'] in ['main', 'scientific', 'orchestration-tools']
```

**Test 3: Performance Under Load**
```python
def test_performance_with_many_branches():
    # Test with 50+ branches
    repo = LargeTestRepository(branches=50)
    
    # Run full pipeline
    start = time.time()
    results = run_full_pipeline(repo)
    elapsed = time.time() - start
    
    # All 5 subtasks should complete in <120 seconds
    assert elapsed < 120, f"Pipeline took {elapsed}s, max 120s"
    
    # Memory usage <100 MB
    memory = get_memory_usage()
    assert memory < 100_000_000, f"Memory {memory}B, max 100MB"
```

---

## Performance Benchmarking

### Benchmark Setup

```python
import time
import psutil

def benchmark_component(analyzer_class, repo, branches):
    """Benchmark a single component."""
    times = []
    memories = []
    
    for branch in branches:
        analyzer = analyzer_class(repo)
        
        # Measure time
        start = time.time()
        result = analyzer.analyze(branch)
        elapsed = time.time() - start
        times.append(elapsed)
        
        # Measure memory
        memory = psutil.Process().memory_info().rss
        memories.append(memory)
    
    return {
        'avg_time': sum(times) / len(times),
        'max_time': max(times),
        'avg_memory': sum(memories) / len(memories),
        'max_memory': max(memories)
    }

def benchmark_full_pipeline(repo, branches):
    """Benchmark complete pipeline."""
    results = {}
    
    # 002.1
    results['002.1'] = benchmark_component(CommitHistoryAnalyzer, repo, branches)
    
    # 002.2
    results['002.2'] = benchmark_component(CodebaseStructureAnalyzer, repo, branches)
    
    # 002.3
    results['002.3'] = benchmark_component(DiffDistanceCalculator, repo, branches)
    
    # 002.4
    clusterer = BranchClusterer(repo)
    start = time.time()
    cluster_result = clusterer.cluster(analyzer_outputs)
    results['002.4'] = {'time': time.time() - start}
    
    # 002.5
    assigner = IntegrationTargetAssigner(repo)
    start = time.time()
    assignments = assigner.assign(cluster_result)
    results['002.5'] = {'time': time.time() - start}
    
    return results
```

### Target Performance

| Component | Per Branch | Total (13 branches) | Memory |
|-----------|-----------|-----------------|--------|
| 002.1 | <2s | <26s | <50 MB |
| 002.2 | <2s | <26s | <50 MB |
| 002.3 | <3s | <39s | <100 MB |
| 002.4 | N/A | <10s | <100 MB |
| 002.5 | <1s | <13s | <50 MB |
| **Total** | N/A | **<120s** | **<100 MB** |

---

## Troubleshooting

### Common Issues

**Issue: Metrics outside [0,1] range**
```python
# Solution: Clamp values
metric = max(0.0, min(1.0, metric))
assert 0 <= metric <= 1
```

**Issue: Division by zero**
```python
# Solution: Check denominators
if days_active == 0:
    days_active = 1  # Minimum 1 day
if total_files == 0:
    return 0.5  # Default neutral score
```

**Issue: Git command timeout**
```python
# Solution: Always use timeout
result = subprocess.run(cmd, timeout=30, ...)
```

**Issue: All branches cluster together**
```python
# Solution: Adjust threshold or minimum cluster count
if len(unique_clusters) < 2:
    # Use different threshold or criterion
    clusters = fcluster(Z, t=5, criterion='maxclust')  # Force 5 clusters
```

**Issue: Tag count < 30**
```python
# Solution: Add default tags
def ensure_minimum_tags(tags, min_count=30):
    if len(tags) < min_count:
        tags.extend(generate_default_tags(len(tags)))
    return tags
```

---

## Next Steps

1. Choose execution strategy (recommended: Full Parallel)
2. Create feature branches for each team
3. Implement subtasks in order of dependency chain
4. Run unit tests continuously
5. Perform integration testing after each stage
6. Run performance benchmarks
7. Final code review and deployment

---

**This guide provides all necessary details for implementing Task 002 Phase 1. Each section can be expanded based on team needs.**

Last Updated: January 6, 2026
