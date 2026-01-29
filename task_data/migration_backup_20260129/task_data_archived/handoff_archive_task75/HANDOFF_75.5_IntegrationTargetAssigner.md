# Task 75.5: IntegrationTargetAssigner Implementation

## Quick Summary
Implement the `IntegrationTargetAssigner` class that assigns branches to integration targets (main/scientific/orchestration-tools) and generates 30+ categorization tags. This is a Stage Two component—depends on Task 75.4 output.

**Effort:** 24-32 hours | **Complexity:** 7/10 | **Parallelizable:** No (depends on 75.4)

---

## What to Build

A Python class `IntegrationTargetAssigner` that:
1. Accepts cluster assignments from BranchClusterer
2. Applies four-level decision hierarchy to assign integration targets
3. Generates 30+ descriptive tags per branch
4. Returns tagged categorizations

### Class Signature
```python
class IntegrationTargetAssigner:
    def __init__(self, repo_path: str)
    def assign(self, cluster_data: dict) -> dict
```

---

## Input Specification

Input from Task 75.4 (BranchClusterer):

```json
{
  "clusters": [...],
  "branch_assignments": {
    "feature/auth-system": 0,
    "feature/api-refactor": 1
  },
  "quality_metrics": {...},
  "clustering_timestamp": "..."
}
```

---

## Output Specification

```json
{
  "categorized_branches": {
    "feature/auth-system": {
      "branch_name": "feature/auth-system",
      "integration_target": "main",
      "cluster_id": 0,
      "confidence": 0.92,
      "decision_rationale": "Heuristic rule match (high merge_readiness + low integration_risk)",
      "tags": [
        "core-feature",
        "security-sensitive",
        "high-priority",
        "low-risk",
        "user-facing",
        "authentication",
        "active-development",
        "moderate-churn",
        "stable-codebase",
        "low-file-impact",
        "non-orchestration",
        "testing-required-high"
      ]
    }
  },
  "integration_target_summary": {
    "main": {
      "branch_count": 8,
      "total_confidence": 0.89,
      "key_tags": ["core-feature", "stable", "low-risk"]
    },
    "scientific": {
      "branch_count": 3,
      "total_confidence": 0.76,
      "key_tags": ["experiment", "research", "data-science"]
    },
    "orchestration-tools": {
      "branch_count": 2,
      "total_confidence": 0.81,
      "key_tags": ["orchestration-branch", "devops"]
    }
  },
  "tag_catalog": {
    "by_category": {
      "scope": ["core-feature", "minor-feature", "experiment", ...],
      "risk_level": ["low-risk", "medium-risk", "high-risk", ...],
      "complexity": ["simple", "moderate", "complex", ...],
      "validation": ["testing-required-high", "testing-required-medium", ...]
    }
  },
  "assignment_timestamp": "2025-12-22T10:50:00Z"
}
```

---

## Decision Hierarchy (4 Levels)

### Level 1: Heuristic Rules (95% confidence threshold)
Apply predefined rules based on metrics and branch names:

```
IF (merge_readiness > 0.9 AND integration_risk < 0.2) → main (95%)
IF (branch_name contains "science" OR "data") → scientific (92%)
IF (branch_name contains "orchestration" OR "devops") → orchestration-tools (94%)
IF (code_churn < 0.3 AND files_affected < 10) → main (90%)
IF (code_churn > 0.7 AND files_affected > 30) → scientific (85%)
```

### Level 2: Affinity Scoring (70% confidence threshold)
Compare metrics against target archetypes:

```
main_archetype = {
    commit_history_weight: 0.85,      # High merge readiness
    codebase_structure_weight: 0.90,  # Stable structure
    diff_distance_weight: 0.75        # Low risk
}
scientific_archetype = {
    commit_history_weight: 0.65,
    codebase_structure_weight: 0.70,
    diff_distance_weight: 0.50
}
orchestration_archetype = {
    commit_history_weight: 0.70,
    codebase_structure_weight: 0.75,
    diff_distance_weight: 0.65
}

# Compute cosine similarity to each archetype
# Highest similarity = target assignment (if > 0.70 threshold)
```

### Level 3: Cluster Consensus (60% confidence threshold)
If Level 1-2 inconclusive:

```
# Examine all branches in same cluster
# If 70%+ of cluster assigned to one target → assign to that target
# Confidence = cluster cohesion * consensus %
```

### Level 4: Default to main (65% confidence)
Fallback: assign to main with low confidence if no other rule matches.

---

## Tag Generation (30+ Tags)

Tags are generated dynamically based on metrics and assignment:

### Category: Scope (5-6 tags)
```python
"core-feature"           # Core functionality (>0.85 codebase_stability)
"minor-feature"          # Limited scope (<5 files affected)
"experiment"             # Scientific/research (high uncertainty metrics)
"refactoring"            # Structure changes without new features
"bug-fix"                # Focused changes to existing code
"infrastructure"         # Build, config, deployment
```

### Category: Risk Level (3 tags)
```python
"low-risk"               # integration_risk > 0.75, code_churn < 0.4
"medium-risk"            # 0.5 < integration_risk < 0.75, 0.4 < churn < 0.7
"high-risk"              # integration_risk < 0.5, code_churn > 0.7
```

### Category: Complexity (3 tags)
```python
"simple"                 # All metrics > 0.8, minimal changes
"moderate"               # Mixed metrics, typical feature
"complex"                # Multiple high-impact areas, >0.75 complexity score
```

### Category: Development Status (4-5 tags)
```python
"active-development"     # commit_recency > 0.8 and recent activity
"stale"                  # No commits > 30 days
"ready-for-merge"        # merge_readiness > 0.85
"requires-review"        # Ambiguous metrics, needs human review
"staging"                # In preparation, not yet ready
```

### Category: File Impact (4 tags)
```python
"low-file-impact"        # files_affected < 5
"moderate-file-impact"   # 5-15 files
"high-file-impact"       # 15-30 files
"massive-impact"         # >30 files (potential refactoring alert)
```

### Category: Codebase Domain (6+ tags, branch-name dependent)
```python
"authentication"         # auth, login, user, session
"api-changes"            # api, endpoint, rest, graphql
"orchestration"          # orchestration, pipeline, scheduler, dask
"data-science"           # ml, ai, data, science, analytics
"testing"                # test, spec, coverage, qa
"documentation"          # docs, readme, guide
```

### Category: Validation Strategy (4 tags)
```python
"testing-required-high"  # integration_risk > 0.7 OR high-impact
"testing-required-medium"# medium-risk
"testing-optional"       # low-risk, isolated changes
"auto-mergeable"         # All metrics excellent, no review needed
```

### Category: Integration Target Tags (3 tags)
```python
"main-ready"             # Target = main
"scientific-branch"      # Target = scientific
"orchestration-branch"   # Target = orchestration-tools
```

### Category: Special Flags (2-3 tags, as applicable)
```python
"has-breaking-changes"   # If core_module_stability < 0.8
"concurrent-development" # authorship_diversity > 0.7
"merge-conflict-risk"    # If changed files overlap with recent commits on main
```

---

## Implementation Checklist

- [ ] Parse cluster data from Task 75.4
- [ ] Extract metrics for each branch
- [ ] Implement Level 1 heuristic rules (with confidence scoring)
- [ ] Implement Level 2 affinity scoring to archetypes
- [ ] Implement Level 3 cluster consensus fallback
- [ ] Implement Level 4 default-to-main fallback
- [ ] Build tag generation engine (rules-based)
- [ ] Generate all 30+ tags per branch based on metrics
- [ ] Calculate confidence score for each assignment
- [ ] Generate integration_target_summary grouped by target
- [ ] Build tag_catalog by category
- [ ] Return dict matching output spec exactly
- [ ] Add docstrings (Google style)

---

## Configuration

Accept these parameters in `__init__` or config file:

```python
INTEGRATION_TARGETS = ["main", "scientific", "orchestration-tools"]
HEURISTIC_CONFIDENCE_THRESHOLD = 0.95
AFFINITY_CONFIDENCE_THRESHOLD = 0.70
CLUSTER_CONSENSUS_THRESHOLD = 0.60
DEFAULT_TARGET = "main"
DEFAULT_CONFIDENCE = 0.65

# Archetype definitions (can be learned/tuned)
TARGET_ARCHETYPES = {
    "main": {...},
    "scientific": {...},
    "orchestration-tools": {...}
}

# Heuristic rules (configurable)
HEURISTIC_RULES = [...]  # See Level 1 above
```

---

## Test Cases

1. **Low-risk, stable branch**: Should assign to `main` with high confidence
2. **High-churn experimental branch**: Should assign to `scientific`
3. **Orchestration-related branch**: Should assign to `orchestration-tools`
4. **Ambiguous branch**: Should use cluster consensus or default to main
5. **Mixed metrics branch**: Should generate appropriate tags

---

## Dependencies

- Outputs from **Task 75.4 (BranchClusterer)** (required)
- Python built-in `re` for branch name pattern matching
- No external ML dependencies (affinity is basic cosine similarity)
- Feeds into **Task 75.6 (Pipeline Integration)**

---

## Tag Generation Algorithm Pseudocode

```python
def generate_tags(self, branch_metrics: dict, assignment: str) -> list:
    tags = []
    
    # Scope tags
    if branch_metrics['codebase_structure'] > 0.85:
        tags.append("core-feature")
    if branch_metrics['files_affected'] < 5:
        tags.append("minor-feature")
    # ... more scope rules
    
    # Risk tags
    if branch_metrics['integration_risk'] > 0.75:
        tags.append("low-risk")
    # ... more risk rules
    
    # Domain tags (from branch name)
    if 'auth' in branch_name.lower():
        tags.append("authentication")
    # ... more domain rules
    
    # Status tags
    if branch_metrics['merge_readiness'] > 0.85:
        tags.append("ready-for-merge")
    # ... more status rules
    
    # Assignment tags
    if assignment == "main":
        tags.append("main-ready")
    # ... more assignment rules
    
    return list(set(tags))  # Remove duplicates
```

---

## Next Steps After Completion

1. Unit test with 10+ branch fixtures
2. Validate tag generation (spot-check tags make sense)
3. Verify confidence scores are well-calibrated
4. Cross-check assignments against known branch purposes
5. Pass output to Task 75.6 (Pipeline Integration)

**Blocked by:** 75.4 (must complete first)
**Enables:** 75.6, 75.7-75.9 (Stage Two and Three)
