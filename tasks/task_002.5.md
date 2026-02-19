# Task 002.5: IntegrationTargetAssigner

**Status:** Ready for Implementation
**Priority:** High
**Effort:** 24-32 hours
**Complexity:** 7/10
**Dependencies:** 002.4

---

## Overview/Purpose

Implement the `IntegrationTargetAssigner` class that assigns branches to integration targets (main, scientific, orchestration-tools) using a four-level decision hierarchy and generates 30+ categorization tags per branch. This is a Stage Two component that transforms cluster data into actionable integration assignments with rich metadata.

**Scope:** IntegrationTargetAssigner class only
**Depends on:** BranchClusterer (002.4) output

---

## Success Criteria

Task 002.5 is complete when:

### Core Functionality
- [ ] `IntegrationTargetAssigner` class accepts `repo_path` (str)
- [ ] `assign()` method accepts cluster_data dict from Task 002.4
- [ ] Implements 4-level decision hierarchy (Heuristic → Affinity → Consensus → Default)
- [ ] Correctly assigns each branch to one of: main, scientific, orchestration-tools
- [ ] Generates 30+ tags per branch across 9 categories
- [ ] Each assignment includes confidence score and decision rationale
- [ ] Output matches JSON schema exactly

### Quality Assurance
- [ ] Unit tests pass (minimum 5 test scenarios with >95% coverage)
- [ ] Tag generation produces valid tags from the defined catalog
- [ ] Confidence scores are well-calibrated per decision level
- [ ] No exceptions for valid inputs including edge cases
- [ ] Code quality: PEP 8 compliant, Google-style docstrings

### Integration Readiness
- [ ] Input format compatible with Task 002.4 output schema
- [ ] Output format compatible with Task 002.6 pipeline input
- [ ] Tag catalog is complete (all 9 categories populated)
- [ ] Configuration externalized and validated

---

## Prerequisites & Dependencies

### Required Before Starting
- [ ] Task 002.4 (BranchClusterer) complete — provides cluster assignments and quality metrics
- [ ] Development environment configured

### Blocks (What This Task Unblocks)
- Task 002.6 (PipelineIntegration)

### External Dependencies
- Python built-in `re` for branch name pattern matching
- Python built-in `math` for cosine similarity
- No external ML dependencies (affinity is basic cosine similarity)

---

## Sub-subtasks Breakdown

### 002.5.1: Level 1 — Heuristic Rules Engine
**Effort:** 5-6 hours
**Depends on:** None (within this task)

**Steps:**
1. Define heuristic rules with confidence thresholds
2. Implement metric-based rules (merge_readiness, integration_risk, code_churn)
3. Implement branch-name-based rules (pattern matching)
4. Return assignment with 95% confidence threshold

**Rules:**
```
IF (merge_readiness > 0.9 AND integration_risk < 0.2) → main (95%)
IF (branch_name contains "science" OR "data") → scientific (92%)
IF (branch_name contains "orchestration" OR "devops") → orchestration-tools (94%)
IF (code_churn < 0.3 AND files_affected < 10) → main (90%)
IF (code_churn > 0.7 AND files_affected > 30) → scientific (85%)
```

**Success Criteria:**
- [ ] All 5 heuristic rules implemented and tested
- [ ] Confidence threshold of 95% enforced
- [ ] Pattern matching is case-insensitive
- [ ] Returns (target, confidence, rationale) tuple

---

### 002.5.2: Level 2 — Affinity Scoring
**Effort:** 4-5 hours
**Depends on:** 002.5.1

**Steps:**
1. Define target archetypes (main, scientific, orchestration-tools)
2. Compute cosine similarity between branch metrics and each archetype
3. Assign to highest-similarity target if above 70% threshold

**Archetypes:**
```python
main_archetype = {
    "commit_history_weight": 0.85,
    "codebase_structure_weight": 0.90,
    "diff_distance_weight": 0.75
}
scientific_archetype = {
    "commit_history_weight": 0.65,
    "codebase_structure_weight": 0.70,
    "diff_distance_weight": 0.50
}
orchestration_archetype = {
    "commit_history_weight": 0.70,
    "codebase_structure_weight": 0.75,
    "diff_distance_weight": 0.65
}
```

**Success Criteria:**
- [ ] Cosine similarity computed correctly
- [ ] 70% confidence threshold enforced
- [ ] Falls through to Level 3 if no archetype matches

---

### 002.5.3: Level 3 — Cluster Consensus
**Effort:** 3-4 hours
**Depends on:** 002.5.2

**Steps:**
1. Examine all branches in same cluster
2. If 70%+ of cluster assigned to one target → assign to that target
3. Confidence = cluster_cohesion × consensus_percentage
4. 60% confidence threshold enforced

**Success Criteria:**
- [ ] Consensus percentage computed correctly
- [ ] Cohesion-weighted confidence calculated
- [ ] Falls through to Level 4 if no consensus

---

### 002.5.4: Level 4 — Default Fallback
**Effort:** 1-2 hours
**Depends on:** 002.5.3

**Steps:**
1. Assign to "main" with 65% confidence
2. Rationale: "No heuristic, affinity, or consensus match; defaulting to main"

**Success Criteria:**
- [ ] Every branch always gets an assignment (no unassigned branches)
- [ ] Default confidence is exactly 0.65

---

### 002.5.5: Tag Generation Engine
**Effort:** 6-8 hours
**Depends on:** 002.5.1

**Steps:**
1. Implement all 9 tag categories (see Tag Definitions below)
2. Generate tags based on branch metrics and assignment
3. Deduplicate tags
4. Build tag_catalog grouped by category

**Success Criteria:**
- [ ] All 30+ tag definitions implemented
- [ ] Tags are consistent with metric thresholds
- [ ] No duplicate tags in output
- [ ] Tag catalog organized by 9 categories

---

### 002.5.6: Output Formatting and Testing
**Effort:** 4-5 hours
**Depends on:** 002.5.4, 002.5.5

**Steps:**
1. Build categorized_branches output
2. Build integration_target_summary grouped by target
3. Build tag_catalog by category
4. Test all 5 scenarios

**Success Criteria:**
- [ ] Output dict matches specification exactly
- [ ] Summary statistics are accurate
- [ ] All test scenarios pass

---

## Specification Details

### Class Interface

```python
class IntegrationTargetAssigner:
    def __init__(self, repo_path: str):
        """Initialize IntegrationTargetAssigner.

        Args:
            repo_path: Path to the git repository.
        """

    def assign(self, cluster_data: dict) -> dict:
        """Assign branches to integration targets with tags.

        Args:
            cluster_data: Output dict from BranchClusterer.cluster().

        Returns:
            Dict with categorized_branches, integration_target_summary, tag_catalog.
        """
```

### Input Schema

From Task 002.4 output:

```json
{
  "clusters": [{"cluster_id": 0, "branches": [...], "cluster_center": {...}}],
  "branch_assignments": {"feature/auth-system": 0},
  "quality_metrics": {"silhouette_avg": 0.71},
  "clustering_timestamp": "..."
}
```

### Output Schema

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
        "core-feature", "security-sensitive", "high-priority", "low-risk",
        "user-facing", "authentication", "active-development", "moderate-churn",
        "stable-codebase", "low-file-impact", "non-orchestration", "testing-required-high"
      ]
    }
  },
  "integration_target_summary": {
    "main": {"branch_count": 8, "total_confidence": 0.89, "key_tags": ["core-feature", "stable", "low-risk"]},
    "scientific": {"branch_count": 3, "total_confidence": 0.76, "key_tags": ["experiment", "research", "data-science"]},
    "orchestration-tools": {"branch_count": 2, "total_confidence": 0.81, "key_tags": ["orchestration-branch", "devops"]}
  },
  "tag_catalog": {
    "by_category": {
      "scope": ["core-feature", "minor-feature", "experiment", "refactoring", "bug-fix", "infrastructure"],
      "risk_level": ["low-risk", "medium-risk", "high-risk"],
      "complexity": ["simple", "moderate", "complex"],
      "dev_status": ["active-development", "stale", "ready-for-merge", "requires-review", "staging"],
      "file_impact": ["low-file-impact", "moderate-file-impact", "high-file-impact", "massive-impact"],
      "domain": ["authentication", "api-changes", "orchestration", "data-science", "testing", "documentation"],
      "validation": ["testing-required-high", "testing-required-medium", "testing-optional", "auto-mergeable"],
      "target": ["main-ready", "scientific-branch", "orchestration-branch"],
      "special_flags": ["has-breaking-changes", "concurrent-development", "merge-conflict-risk"]
    }
  },
  "assignment_timestamp": "2025-12-22T10:50:00Z"
}
```

### Complete Tag Definitions (All 9 Categories)

#### Category 1: Scope (6 tags)
| Tag | Rule |
|-----|------|
| `core-feature` | codebase_structure aggregate > 0.85 |
| `minor-feature` | files_affected < 5 |
| `experiment` | High uncertainty metrics (scientific patterns) |
| `refactoring` | Structure changes without new features |
| `bug-fix` | Focused changes to existing code |
| `infrastructure` | Build, config, deployment files |

#### Category 2: Risk Level (3 tags)
| Tag | Rule |
|-----|------|
| `low-risk` | integration_risk > 0.75 AND code_churn < 0.4 |
| `medium-risk` | 0.5 < integration_risk < 0.75 AND 0.4 < churn < 0.7 |
| `high-risk` | integration_risk < 0.5 AND code_churn > 0.7 |

#### Category 3: Complexity (3 tags)
| Tag | Rule |
|-----|------|
| `simple` | All metrics > 0.8, minimal changes |
| `moderate` | Mixed metrics, typical feature |
| `complex` | Multiple high-impact areas, complexity score > 0.75 |

#### Category 4: Development Status (5 tags)
| Tag | Rule |
|-----|------|
| `active-development` | commit_recency > 0.8 and recent activity |
| `stale` | No commits > 30 days |
| `ready-for-merge` | merge_readiness > 0.85 |
| `requires-review` | Ambiguous metrics, needs human review |
| `staging` | In preparation, not yet ready |

#### Category 5: File Impact (4 tags)
| Tag | Rule |
|-----|------|
| `low-file-impact` | files_affected < 5 |
| `moderate-file-impact` | 5-15 files |
| `high-file-impact` | 15-30 files |
| `massive-impact` | >30 files (potential refactoring alert) |

#### Category 6: Codebase Domain (6+ tags, branch-name dependent)
| Tag | Pattern |
|-----|---------|
| `authentication` | auth, login, user, session |
| `api-changes` | api, endpoint, rest, graphql |
| `orchestration` | orchestration, pipeline, scheduler, dask |
| `data-science` | ml, ai, data, science, analytics |
| `testing` | test, spec, coverage, qa |
| `documentation` | docs, readme, guide |

#### Category 7: Validation Strategy (4 tags)
| Tag | Rule |
|-----|------|
| `testing-required-high` | integration_risk > 0.7 OR high-impact |
| `testing-required-medium` | medium-risk |
| `testing-optional` | low-risk, isolated changes |
| `auto-mergeable` | All metrics excellent, no review needed |

#### Category 8: Integration Target (3 tags)
| Tag | Rule |
|-----|------|
| `main-ready` | Target = main |
| `scientific-branch` | Target = scientific |
| `orchestration-branch` | Target = orchestration-tools |

#### Category 9: Special Flags (3 tags)
| Tag | Rule |
|-----|------|
| `has-breaking-changes` | core_module_stability < 0.8 |
| `concurrent-development` | authorship_diversity > 0.7 |
| `merge-conflict-risk` | Changed files overlap with recent main commits |

---

## Implementation Guide

### Step 1: Decision Hierarchy Engine

```python
def assign(self, cluster_data: dict) -> dict:
    results = {}

    for branch_name, cluster_id in cluster_data['branch_assignments'].items():
        branch_metrics = self._extract_branch_metrics(branch_name, cluster_data)

        # Level 1: Heuristic Rules
        target, confidence, rationale = self._apply_heuristics(branch_name, branch_metrics)

        # Level 2: Affinity Scoring (if Level 1 inconclusive)
        if confidence < self.HEURISTIC_CONFIDENCE_THRESHOLD:
            target, confidence, rationale = self._affinity_scoring(branch_metrics)

        # Level 3: Cluster Consensus (if Level 2 inconclusive)
        if confidence < self.AFFINITY_CONFIDENCE_THRESHOLD:
            target, confidence, rationale = self._cluster_consensus(
                cluster_id, cluster_data, results
            )

        # Level 4: Default to main
        if confidence < self.CLUSTER_CONSENSUS_THRESHOLD:
            target = "main"
            confidence = 0.65
            rationale = "Default assignment (no rule matched)"

        # Generate tags
        tags = self._generate_tags(branch_name, branch_metrics, target)

        results[branch_name] = {
            "branch_name": branch_name,
            "integration_target": target,
            "cluster_id": cluster_id,
            "confidence": confidence,
            "decision_rationale": rationale,
            "tags": tags
        }

    return self._format_output(results)
```

### Step 2: Tag Generation

```python
def _generate_tags(self, branch_name: str, metrics: dict, assignment: str) -> list:
    tags = []

    # Scope tags
    if metrics.get('codebase_structure', 0) > 0.85:
        tags.append("core-feature")
    if metrics.get('files_affected', 0) < 5:
        tags.append("minor-feature")

    # Risk tags
    risk = metrics.get('integration_risk', 0.5)
    churn = metrics.get('code_churn', 0.5)
    if risk > 0.75 and churn < 0.4:
        tags.append("low-risk")
    elif risk < 0.5 and churn > 0.7:
        tags.append("high-risk")
    else:
        tags.append("medium-risk")

    # Domain tags (from branch name)
    name_lower = branch_name.lower()
    domain_patterns = {
        "authentication": ["auth", "login", "user", "session"],
        "api-changes": ["api", "endpoint", "rest", "graphql"],
        "orchestration": ["orchestration", "pipeline", "scheduler", "dask"],
        "data-science": ["ml", "ai", "data", "science", "analytics"],
        "testing": ["test", "spec", "coverage", "qa"],
        "documentation": ["docs", "readme", "guide"]
    }
    for tag, patterns in domain_patterns.items():
        if any(p in name_lower for p in patterns):
            tags.append(tag)

    # Status tags
    if metrics.get('merge_readiness', 0) > 0.85:
        tags.append("ready-for-merge")
    if metrics.get('commit_recency', 0) > 0.8:
        tags.append("active-development")
    if metrics.get('commit_recency', 1) < 0.1:
        tags.append("stale")

    # Target tags
    target_tag_map = {"main": "main-ready", "scientific": "scientific-branch",
                      "orchestration-tools": "orchestration-branch"}
    tags.append(target_tag_map.get(assignment, "main-ready"))

    # Special flags
    if metrics.get('core_module_stability', 1) < 0.8:
        tags.append("has-breaking-changes")
    if metrics.get('authorship_diversity', 0) > 0.7:
        tags.append("concurrent-development")

    return list(set(tags))
```

---

## Configuration & Defaults

```python
INTEGRATION_TARGETS = ["main", "scientific", "orchestration-tools"]
HEURISTIC_CONFIDENCE_THRESHOLD = 0.95
AFFINITY_CONFIDENCE_THRESHOLD = 0.70
CLUSTER_CONSENSUS_THRESHOLD = 0.60
DEFAULT_TARGET = "main"
DEFAULT_CONFIDENCE = 0.65

TARGET_ARCHETYPES = {
    "main": {"commit_history_weight": 0.85, "codebase_structure_weight": 0.90, "diff_distance_weight": 0.75},
    "scientific": {"commit_history_weight": 0.65, "codebase_structure_weight": 0.70, "diff_distance_weight": 0.50},
    "orchestration-tools": {"commit_history_weight": 0.70, "codebase_structure_weight": 0.75, "diff_distance_weight": 0.65}
}

HEURISTIC_RULES = [
    {"condition": "merge_readiness > 0.9 AND integration_risk < 0.2", "target": "main", "confidence": 0.95},
    {"condition": "branch_name contains 'science' OR 'data'", "target": "scientific", "confidence": 0.92},
    {"condition": "branch_name contains 'orchestration' OR 'devops'", "target": "orchestration-tools", "confidence": 0.94},
    {"condition": "code_churn < 0.3 AND files_affected < 10", "target": "main", "confidence": 0.90},
    {"condition": "code_churn > 0.7 AND files_affected > 30", "target": "scientific", "confidence": 0.85}
]
```

---

## Typical Development Workflow

1. **Day 1-2:** Implement Level 1 heuristic rules engine (002.5.1)
2. **Day 2-3:** Implement Level 2 affinity scoring with archetypes (002.5.2)
3. **Day 3-4:** Implement Level 3 cluster consensus and Level 4 default (002.5.3, 002.5.4)
4. **Day 4-6:** Build tag generation engine with all 30+ tags (002.5.5)
5. **Day 6-7:** Output formatting, summary generation, testing (002.5.6)
6. **Day 7-8:** Code review, docstrings, edge case hardening

---

## Integration Handoff

### Downstream Tasks

| Task | Consumes | Purpose |
|------|----------|---------|
| **002.6** (PipelineIntegration) | Full output dict (categorized_branches, summary, tag_catalog) | Generates final JSON output files for downstream consumers |

### Tag Consumption by Downstream Tasks

| Downstream Task | Tags Consumed | Usage |
|-----------------|---------------|-------|
| Task 79 (Execution Control) | `parallel_capability` tags | Determines parallel vs serial execution |
| Task 80 (Validation Intensity) | `simple`, `moderate`, `complex` | Selects validation intensity |
| Task 83 (Test Suite Selection) | `testing-required-*` tags | Determines test suite scope |
| Task 101 (Orchestration Filter) | `orchestration-branch` | Filters orchestration-only branches |

---

## Common Gotchas & Solutions

**Gotcha 1: Branch name patterns too broad**
```python
# WRONG: "data" matches "update-database" (false positive)
if "data" in branch_name:
    tags.append("data-science")

# RIGHT: Match on path segments
segments = branch_name.lower().split("/")
if any(s in ["data", "science", "ml", "ai"] for s in segments):
    tags.append("data-science")
```

**Gotcha 2: Missing metrics for some branches**
```python
# WRONG: KeyError if metric not present
risk = metrics['integration_risk']

# RIGHT: Default values for missing metrics
risk = metrics.get('integration_risk', 0.5)
```

**Gotcha 3: Confidence levels not cascading correctly**
```python
# WRONG: Level 2 runs even if Level 1 succeeded
target1, conf1, rat1 = self._apply_heuristics(...)
target2, conf2, rat2 = self._affinity_scoring(...)  # Wasteful

# RIGHT: Only cascade on insufficient confidence
target, conf, rat = self._apply_heuristics(...)
if conf < self.HEURISTIC_CONFIDENCE_THRESHOLD:
    target, conf, rat = self._affinity_scoring(...)
```

**Gotcha 4: Empty cluster during consensus**
```python
# WRONG: Division by zero if cluster has no assigned branches yet
consensus = assigned_count / total_in_cluster

# RIGHT: Guard against empty
total = max(1, total_in_cluster)
consensus = assigned_count / total
```

---

## Integration Checkpoint

**When to move to Task 002.6 (PipelineIntegration):**

- [ ] All 6 sub-subtasks complete
- [ ] 4-level decision hierarchy tested (each level independently)
- [ ] Tag generation produces 30+ tags across 9 categories
- [ ] Confidence scores well-calibrated per decision level
- [ ] Output matches specification schema exactly
- [ ] All 5 test scenarios pass (low-risk, high-churn, orchestration, ambiguous, mixed)
- [ ] Code review approved
- [ ] Commit message: `feat: complete Task 002.5 IntegrationTargetAssigner`

---

## Done Definition

Task 002.5 is done when:

1. All 6 sub-subtasks marked complete
2. Unit tests pass (>95% coverage) for all test scenarios
3. Code review approved
4. 4-level decision hierarchy produces correct assignments
5. 30+ tags generated correctly across 9 categories
6. Output matches specification schema exactly
7. Documentation complete (Google-style docstrings)
8. Tag catalog is complete and accurate
9. Ready for hand-off to Task 002.6
10. Commit: `feat: complete Task 002.5 IntegrationTargetAssigner`

---

## Provenance

- **Primary source:** HANDOFF_75.5_IntegrationTargetAssigner.md (archived in task_data/migration_backup_20260129/)
- **Task ID mapping:** Original Task 75.5 → Current Task 002.5
- **Structure standard:** TASK_STRUCTURE_STANDARD.md (14-section format, approved January 6, 2026)
- **Upstream dependency:** Task 002.4 (BranchClusterer)
- **Downstream consumer:** Task 002.6 (PipelineIntegration)
- **Tag consumption:** Tasks 79, 80, 83, 101 (downstream orchestration tasks)

---

## Next Steps

1. **Immediate:** Begin with sub-subtask 002.5.1 (Design Assignment Architecture and Decision Hierarchy)
2. **Week 1:** Complete all 8 sub-subtasks with proper target assignment logic
3. **Week 1-2:** Implement four-level decision hierarchy (heuristic, affinity, consensus, default)
4. **Week 2:** Generate 30+ categorization tags per branch with proper classification
5. **Week 2:** Write comprehensive tests for all 5 assignment scenarios
6. **Week 2-3:** Performance validation and confidence scoring calibration
7. **Week 3:** Code review and documentation completion
8. **Upon completion:** Ready for hand-off to Task 002.6 (PipelineIntegration)
9. **Parallel tasks:** Task 002.7 (VisualizationReporting), Task 002.8 (TestingSuite) can proceed in parallel
