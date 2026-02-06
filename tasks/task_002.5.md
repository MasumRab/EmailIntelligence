# Task 002.5: IntegrationTargetAssigner

**Status:** pending
**Priority:** high
**Effort:** 24-32 hours
**Complexity:** 7/10
**Dependencies:** 002.4

---

## Overview/Purpose

Assign optimal integration targets (main, scientific, orchestration-tools) to each feature branch based on clustering results and Task 001 criteria.

---

## Quick Navigation

Navigate this document using these links:

- [Overview/Purpose](#overview/purpose)
- [Success Criteria](#success-criteria)
- [Prerequisites & Dependencies](#prerequisites--dependencies)
- [Sub-subtasks Breakdown](#sub-subtasks-breakdown)
- [Specification Details](#specification-details)
- [Implementation Guide](#implementation-guide)
- [Configuration & Defaults](#configuration--defaults)
- [Typical Development Workflow](#typical-development-workflow)
- [Integration Handoff](#integration-handoff)
- [Common Gotchas & Solutions](#common-gotchas--solutions)
- [Subtasks Overview](#subtasks-overview)
- [Integration Checkpoint](#integration-checkpoint)
- [Done Definition](#done-definition)

**Pro tip:** Use Ctrl+F to search within sections, or click links above to jump directly

---

## Success Criteria

- [ ] Assigns targets to all feature branches
- [ ] Provides confidence scores per assignment
- [ ] Generates justification documentation
- [ ] Integrates with Task 001 criteria
- [ ] Outputs standard JSON format

---

<!-- IMPORTED_FROM: backup_task75/task-002.5.md -->
Task 002.5 is complete when:

**Core Functionality:**
- [ ] `IntegrationTargetAssigner` class accepts cluster output from Task 002.4
- [ ] Implements four-level decision hierarchy for target assignment
- [ ] Generates 30+ tags per branch (primary, execution, complexity, content, validation, workflow)
- [ ] Assigns confidence scores and reasoning for each assignment
- [ ] Outputs properly formatted dict with assignments and tags
- [ ] Output matches JSON schema exactly

**Quality Assurance:**
- [ ] Unit tests pass (minimum 8 test cases with >95% coverage)
- [ ] No exceptions raised for valid inputs
- [ ] Performance: <1 second per branch assignment
- [ ] Code quality: PEP 8 compliant, comprehensive docstrings

**Integration Readiness:**
- [ ] Compatible with Task 002.6 (PipelineIntegration) input requirements
- [ ] Tag system bridges downstream tasks (79, 80, 83, 101)
- [ ] Configuration externalized and validated
- [ ] Documentation complete and accurate

---

## Prerequisites & Dependencies

### Required Before Starting
- [ ] No external prerequisites

### Blocks (What This Task Unblocks)
- [ ] No specific blocks defined

### External Dependencies
- [ ] No external dependencies

## Sub-subtasks Breakdown

### 002.5.1: Design Assignment Architecture
**Purpose:** Define the four-level decision hierarchy and confidence scoring system
**Effort:** 2-3 hours

**Steps:**
1. Define the four-level decision hierarchy (heuristic, affinity, consensus, default)
2. Document confidence thresholds for each level (95%, 70%, 60%, 65%)
3. Create decision tree for target assignment logic
4. Define reasoning generation approach for each assignment
5. Document edge case handling for each decision level

**Success Criteria:**
- [ ] Four-level hierarchy clearly defined with thresholds
- [ ] Decision tree logic specified
- [ ] Reasoning approach documented
- [ ] Edge case handling documented
- [ ] Integration with Task 001 criteria specified

**Blocks:** 002.5.2, 002.5.3, 002.5.4, 002.5.5

---

### 002.5.2: Implement Heuristic Rule Engine
**Purpose:** Create rules-based assignment for clear-cut cases
**Effort:** 4-5 hours
**Depends on:** 002.5.1

**Steps:**
1. Create rule definitions for common branch patterns
2. Implement rule matching algorithm
3. Create confidence scoring for rule matches
4. Add reasoning generation for rule-based assignments
5. Test with clear-cut branch examples

**Success Criteria:**
- [ ] Rule engine matches patterns correctly
- [ ] Confidence scores > 0.95 for perfect matches
- [ ] Reasoning generated for each assignment
- [ ] Handles edge cases gracefully
- [ ] Performance: <0.1 seconds per branch

**Blocks:** 002.5.3, 002.5.4

---

### 002.5.3: Implement Affinity Scoring System
**Purpose:** Score branch similarity to target archetypes
**Effort:** 4-5 hours
**Depends on:** 002.5.1

**Steps:**
1. Define target archetypes (main, scientific, orchestration-tools)
2. Create similarity metrics for each archetype
3. Implement scoring algorithm (cosine similarity, Jaccard, etc.)
4. Normalize scores to [0,1] range with confidence interpretation
5. Test with branches of known archetype similarity

**Success Criteria:**
- [ ] Returns value in [0, 1] range
- [ ] Known main-target branches score > 0.85 on main archetype
- [ ] Known scientific branches score > 0.80 on scientific archetype
- [ ] Handles edge cases (new branches, empty metrics)
- [ ] Performance: <0.2 seconds per branch

---

### 002.5.4: Implement Cluster Consensus Logic
**Purpose:** Use cluster membership to inform target assignment
**Effort:** 3-4 hours
**Depends on:** 002.5.1

**Steps:**
1. Extract cluster assignments from Task 002.4 output
2. Identify target preferences of other branches in same cluster
3. Calculate consensus confidence based on cluster agreement
4. Handle clusters with mixed target preferences
5. Generate reasoning based on cluster analysis

**Success Criteria:**
- [ ] Correctly identifies cluster membership
- [ ] Consensus confidence reflects cluster agreement
- [ ] Handles mixed-preference clusters appropriately
- [ ] Generates clear reasoning for cluster-based decisions
- [ ] Performance: <0.1 seconds per branch

---

### 002.5.5: Implement Default Assignment & Task 001 Integration
**Purpose:** Handle cases that don't fit other levels, integrate Task 001 criteria
**Effort:** 3-4 hours
**Depends on:** 002.5.1

**Steps:**
1. Define default assignment logic (usually to main)
2. Integrate Task 001 criteria into assignment process
3. Apply Task 001 filters and requirements
4. Set default confidence level (65%)
5. Generate default reasoning for fallback cases

**Success Criteria:**
- [ ] Default assignment works for all edge cases
- [ ] Task 001 criteria properly applied
- [ ] Confidence score set to 0.65 for defaults
- [ ] Reasoning explains default assignment
- [ ] Handles all unassigned branches

**Blocks:** 002.5.6

---

### 002.5.6: Implement Tag Generation System
**Purpose:** Generate 30+ categorization tags per branch
**Effort:** 4-5 hours
**Depends on:** 002.5.2, 002.5.3, 002.5.4, 002.5.5

**Steps:**
1. Define 6 tag categories (scope, complexity, risk, content, validation, workflow)
2. Create tag generation rules for each category
3. Implement conditional tag logic (some tags trigger others)
4. Validate tag consistency and mutual exclusivity where needed
5. Test with branches of known characteristics

**Success Criteria:**
- [ ] 30+ tags generated per branch
- [ ] All 6 categories represented
- [ ] Tags are internally consistent
- [ ] Conditional tags triggered appropriately
- [ ] Handles all branch types correctly

**Blocks:** 002.5.7

---

### 002.5.7: Format Output & Validation
**Purpose:** Structure results into JSON dict with validation
**Effort:** 2-3 hours
**Depends on:** 002.5.6

**Steps:**
1. Create output dict structure matching specification exactly
2. Populate with target assignment, confidence, reasoning, and tags
3. Include metadata (timestamp, version, source data)
4. Validate output against JSON schema
5. Add error handling for validation failures

**Success Criteria:**
- [ ] Output dict has all required fields per specification
- [ ] All assignments include target, confidence, and reasoning
- [ ] 30+ tags included per branch
- [ ] Schema validation passes without errors
- [ ] Error handling catches validation issues

**Blocks:** 002.5.8

---

### 002.5.8: Write Unit Tests
**Purpose:** Verify IntegrationTargetAssigner works correctly
**Effort:** 3-4 hours
**Depends on:** 002.5.7

**Steps:**
1. Create test fixtures with various branch characteristics
2. Implement minimum 8 test cases covering all assignment levels
3. Mock clustering inputs for reliable testing
4. Add performance tests
5. Generate coverage report (>95%)

**Success Criteria:**
- [ ] Minimum 8 comprehensive test cases
- [ ] All tests pass on CI/CD
- [ ] Code coverage >95%
- [ ] Edge cases covered
- [ ] Error handling tested
- [ ] Output validation includes JSON schema
- [ ] Performance tests meet <2 second requirement

---

## Specification Details

### Task Interface
- **ID**: 002.5
- **Title**: IntegrationTargetAssigner
- **Status**: pending
- **Priority**: high
- **Effort**: 24-32 hours
- **Complexity**: 7/10

### Requirements
**Core Requirements:**
- Python 3.8+ runtime environment
- Access to clustering outputs from Task 002.4
- Integration with Task 001 criteria and requirements
- YAML parser for configuration files
- Memory sufficient to hold cluster assignments and target criteria

**Functional Requirements:**
- Must accept cluster assignment data from Task 002.4 as input
- Must apply four-level decision hierarchy for target assignment
- Must generate 30+ categorization tags per branch
- Must assign confidence scores and reasoning for each assignment
- Must return properly formatted dict with assignments and metadata

**Non-functional Requirements:**
- Performance: Complete assignment of 50+ branches in under 2 seconds
- Reliability: Handle all error conditions gracefully without crashing
- Scalability: Support up to 200 branches in single assignment operation
- Maintainability: Follow PEP 8 standards with comprehensive docstrings
- Testability: Achieve >95% code coverage with unit tests

### Task Interface
- **ID**: 002.5
- **Title**: IntegrationTargetAssigner
- **Status**: pending
- **Priority**: high
- **Effort**: 24-32 hours
- **Complexity**: 7/10

### Requirements

**Core Requirements:**
- Python 3.8+ runtime environment
- Access to clustering outputs from Task 002.4
- Integration with Task 001 criteria and requirements
- YAML parser for configuration files
- Memory sufficient to hold cluster assignments and target criteria

**Functional Requirements:**
- Must accept cluster assignment data from Task 002.4 as input
- Must apply four-level decision hierarchy for target assignment
- Must generate 30+ categorization tags per branch
- Must assign confidence scores and reasoning for each assignment
- Must return properly formatted dict with assignments and metadata

**Non-functional Requirements:**
- Performance: Complete assignment of 50+ branches in under 2 seconds
- Reliability: Handle all error conditions gracefully without crashing
- Scalability: Support up to 200 branches in single assignment operation
- Maintainability: Follow PEP 8 standards with comprehensive docstrings
- Testability: Achieve >95% code coverage with unit tests

## Implementation Guide

### Phase 1: Setup and Architecture (Days 1-2)
1. Create the basic class structure for `IntegrationTargetAssigner`
2. Implement input validation for cluster assignment data
3. Set up configuration loading from YAML
4. Create the basic method signatures

### Phase 2: Decision Hierarchy Implementation (Days 2-3)
1. Implement the four-level decision hierarchy:
   - Level 1: Heuristic rules (95% confidence threshold)
   - Level 2: Affinity scoring (70% confidence threshold)
   - Level 3: Cluster consensus (60% confidence threshold)
   - Level 4: Default assignment (65% confidence)
2. Create confidence scoring system
3. Implement reasoning generation for each assignment
4. Add proper error handling for all levels

### Phase 3: Tag Generation System (Days 3-4)
1. Implement tag generation for all 6 categories (30+ tags)
2. Create tag validation logic
3. Implement conditional tag logic (complexity → validation tags)
4. Add tag combinatorics for special cases
5. Generate tag documentation

### Phase 4: Integration and Testing (Days 4-5)
1. Integrate all components into complete assignment system
2. Format output according to specification
3. Write comprehensive unit tests (8+ test cases)
4. Perform performance testing to ensure <2s execution time

### Key Implementation Notes:
- Use the four-level hierarchy with proper confidence thresholds
- Implement comprehensive error handling for all edge cases
- Ensure all confidence scores are in [0,1] range
- Follow the configuration parameters specified in the Configuration section
- Add comprehensive logging and error reporting

<!-- IMPORTED_FROM: /home/masum/github/PR/.taskmaster/enhanced_improved_tasks/task-002-5.md -->

<!-- IMPORTED_FROM: /home/masum/github/PR/.taskmaster/task_data/archived/backups_archive_task002/task-002.5.md -->

# Task 002.5: IntegrationTargetAssigner

<!-- IMPORTED_FROM: /home/masum/github/PR/.taskmaster/task_data/archived/handoff_archive_task002/HANDOFF_002.5_IntegrationTargetAssigner.md -->

# Task 002.5: IntegrationTargetAssigner Implementation

## Quick Summary
Implement the `IntegrationTargetAssigner` class that assigns branches to integration targets (main/scientific/orchestration-tools) and generates 30+ categorization tags. This is a Stage Two component—depends on Task 002.4 output.

**Effort:** 24-32 hours | **Complexity:** 7/10 | **Parallelizable:** No (depends on 002.4)

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

Input from Task 002.4 (BranchClusterer):

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
Apply predefined rules based on metrics and branch names, including explicit integration_risk mapping:

```
IF (merge_readiness > 0.9 AND integration_risk < 0.2) → main (95%)
IF (integration_risk <= 0.3) → main (90%)
IF (integration_risk >= 0.7) → scientific (85%)
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

### Integration Risk → Target Mapping
```text
integration_risk <= 0.3  → prefer main
integration_risk 0.3-0.7 → use affinity + cluster consensus
integration_risk >= 0.7  → prefer scientific
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

- [ ] Parse cluster data from Task 002.4
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

- Outputs from **Task 002.4 (BranchClusterer)** (required)
- Python built-in `re` for branch name pattern matching
- No external ML dependencies (affinity is basic cosine similarity)
- Feeds into **Task 002.6 (Pipeline Integration)**

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
5. Pass output to Task 002.6 (Pipeline Integration)

**Blocked by:** 002.4 (must complete first)
**Enables:** 002.6, 002.7-002.9 (Stage Two and Three)

## Purpose
Assign integration targets to clustered branches with comprehensive tagging system. This Stage Two task uses cluster outputs and applies four-level decision hierarchy to assign targets and generate 30+ tags per branch.

**Scope:** IntegrationTargetAssigner class only  
**Effort:** 24-32 hours | **Complexity:** 7/10  
**Status:** Ready when 002.4 complete  
**Blocks:** Task 002.6

---

## Success Criteria

Task 002.5 is complete when:

**Core Functionality:**
- [ ] `IntegrationTargetAssigner` class accepts cluster output from Task 002.4
- [ ] Implements four-level decision hierarchy for target assignment
- [ ] Generates 30+ tags per branch (primary, execution, complexity, content, validation, workflow)
- [ ] Assigns confidence scores and reasoning for each assignment
- [ ] Outputs properly formatted dict with assignments and tags
- [ ] Output matches JSON schema exactly

**Quality Assurance:**
- [ ] Unit tests pass (minimum 8 test cases with >95% coverage)
- [ ] No exceptions raised for valid inputs
- [ ] Performance: <1 second per branch assignment
- [ ] Code quality: PEP 8 compliant, comprehensive docstrings

**Integration Readiness:**
- [ ] Compatible with Task 002.6 (PipelineIntegration) input requirements
- [ ] Tag system bridges downstream tasks (79, 80, 83, 101)
- [ ] Configuration externalized and validated
- [ ] Documentation complete and accurate

---

## Tag System Overview

### Primary Target Tags (1 required)
- `tag:main_branch` - Assign to main/master
- `tag:scientific_branch` - Assign to science branches
- `tag:orchestration_tools_branch` - Assign to orchestration branches

### Execution Context Tags (1 required)
- `tag:parallel_safe` - Can execute in parallel
- `tag:sequential_required` - Must execute sequentially
- `tag:isolated_execution` - Execute in isolation

### Complexity Tags (1 required)
- `tag:simple_merge` - Low complexity
- `tag:moderate_complexity` - Medium complexity
- `tag:high_complexity` - High complexity

### Content Type Tags (0+)
- `tag:core_code_changes` - Core code modified
- `tag:test_changes` - Test files modified
- `tag:config_changes` - Configuration modified
- `tag:documentation_only` - Documentation only
- `tag:security_sensitive` - Security implications
- `tag:performance_critical` - Performance impact

### Validation Tags (0+)
- `tag:requires_e2e_testing` - E2E tests needed
- `tag:requires_unit_tests` - Unit tests needed
- `tag:requires_security_review` - Security review needed
- `tag:requires_performance_testing` - Performance tests needed

### Workflow Tags (0+)
- `tag:task_101_orchestration` - Relevant to Task 101
- `tag:framework_core` - Core framework component
- `tag:framework_extension` - Framework extension

---

## Subtasks

### 002.5.1: Design Target Assignment Hierarchy
**Purpose:** Define four-level decision hierarchy  
**Effort:** 2-3 hours

**Steps:**
1. Design decision tree for target assignment
2. Define heuristic rules at each level
3. Document confidence scoring approach
4. Create reasoning generation rules
5. Document edge cases and fallbacks

**Success Criteria:**
- [ ] Decision hierarchy fully documented
- [ ] All rules specified with conditions
- [ ] Confidence scoring approach clear
- [ ] Edge cases identified

---

### 002.5.2: Implement Heuristic Rule Engine
**Purpose:** Create rules-based assignment logic  
**Effort:** 4-5 hours

**Steps:**
1. Implement rule evaluation engine
2. Create conditions for each decision point
3. Implement confidence scoring
4. Add reasoning generation
5. Handle rule conflicts and edge cases

**Success Criteria:**
- [ ] Rules evaluate correctly
- [ ] Confidence scores in [0,1]
- [ ] Reasoning generated for each assignment
- [ ] Edge cases handled gracefully

---

### 002.5.3: Implement Tag Generation System
**Purpose:** Generate 30+ tags per branch  
**Effort:** 5-6 hours

**Steps:**
1. Implement tag generation for all 6 categories
2. Create tag validation logic
3. Implement conditional tag logic (complexity → validation)
4. Add tag combinatorics for special cases
5. Generate tag documentation

**Success Criteria:**
- [ ] All tag categories implemented
- [ ] 30+ unique tags generated
- [ ] Tags are mutually consistent
- [ ] Tag semantics clearly documented

---

### 002.5.4: Implement Affinity Scoring
**Purpose:** Score branches for integration readiness  
**Effort:** 3-4 hours

**Steps:**
1. Design affinity metrics
2. Implement cluster-based affinity
3. Implement change-based affinity
4. Combine affinities into scores
5. Normalize scores to [0,1]

**Success Criteria:**
- [ ] Affinity scores in [0,1]
- [ ] Reflects cluster coherence
- [ ] Reflects change characteristics
- [ ] Enables smart prioritization

---

### 002.5.5: Implement Confidence Scoring
**Purpose:** Score confidence in assignments  
**Effort:** 3-4 hours

**Steps:**
1. Define confidence factors
2. Implement confidence calculation
3. Weight confidence sources
4. Normalize to [0,1]
5. Document interpretation

**Success Criteria:**
- [ ] Confidence scores in [0,1]
- [ ] Reflects rule matching quality
- [ ] Reflects metric agreement
- [ ] Enables filtering by confidence

---

### 002.5.6: Implement Reasoning Generation
**Purpose:** Generate human-readable reasoning  
**Effort:** 3-4 hours

**Steps:**
1. Create reasoning templates per assignment type
2. Implement fact extraction for reasoning
3. Generate explanatory text
4. Add reasoning validation
5. Test readability and clarity

**Success Criteria:**
- [ ] Reasoning explains assignment
- [ ] Uses human-readable language
- [ ] Includes supporting metrics
- [ ] Helps with validation

---

### 002.5.7: Aggregate & Output Formatting
**Purpose:** Combine results and format output  
**Effort:** 2-3 hours

**Steps:**
1. Create output dict structure
2. Combine targets, tags, confidence, reasoning
3. Validate output completeness
4. Format for downstream consumption
5. Validate against JSON schema

**Success Criteria:**
- [ ] Output has all required fields
- [ ] Tags are complete and consistent
- [ ] Assignment is well-reasoned
- [ ] Schema validation passes

---

### 002.5.8: Write Unit Tests
**Purpose:** Comprehensive test coverage  
**Effort:** 3-4 hours

**Steps:**
1. Create test fixtures with various cluster characteristics
2. Implement 8+ test cases
3. Mock cluster inputs
4. Add rule coverage tests
5. Generate coverage report (>95%)

**Success Criteria:**
- [ ] 8+ test cases implemented
- [ ] All tests pass
- [ ] Code coverage >95%
- [ ] All rules tested
- [ ] Edge cases covered

---

## Configuration Parameters

- Assignment hierarchy rules
- Tag definitions and semantics
- Confidence scoring weights
- Affinity calculation parameters
- Reasoning template configurations

---

## Integration Checkpoint

**When to move to 002.6:**
- [ ] All 8 subtasks complete
- [ ] Unit tests passing (>90% coverage)
- [ ] Accepts output from Task 002.4
- [ ] Generates 30+ tags per branch
- [ ] Output matches specification
- [ ] Ready for pipeline integration

---

## Done Definition

Task 002.5 is done when:
1. All 8 subtasks marked complete
2. Unit tests pass (>95% coverage)
3. Code review approved
4. Generates 30+ comprehensive tags
5. Assignment reasoning validated
6. Ready for hand-off to Task 002.6

## Purpose

Assign optimal integration targets (main, scientific, orchestration-tools) to each feature branch based on clustering results and Task 001 criteria.

---

## Details

Implement a Python module that:
- Takes clustered branches and metrics as input
- Applies Task 001 framework criteria to refine assignments
- Calculates confidence scores for each target assignment
- Generates justification for recommendations
- Outputs categorized_branches.json

---

## Guidance & Standards

- **Architecture:** [Comprehensive Guide](../guidance/COMPREHENSIVE_CLI_ARCHITECTURE_GUIDE.md)
- **Merging:** [Merge Guidance](../guidance/MERGE_GUIDANCE_DOCUMENTATION.md)
- **Patterns:** [Factory Pattern](../guidance/FACTORY_PATTERN_IMPLEMENTATION_GUIDE.md)
- **General:** [Project Guidance](../guidance/README.md)

---

## Success Criteria

- [ ] Assigns targets to all feature branches
- [ ] Provides confidence scores per assignment
- [ ] Generates justification documentation
- [ ] Integrates with Task 001 criteria
- [ ] Outputs standard JSON format

---

## Test Strategy

- Compare with manual assignments
- Test edge cases (equally similar to multiple targets)
- Validate justification quality
- Test integration with Task 001

---

---

## Implementation Notes

_Add implementation notes here as work progresses_

---

## Progress Log

### 2026-01-12
- Subtask file created from main task template
- Ready for implementation
**Priority:** high
**Effort:** 24-32 hours
**Complexity:** 7/10
**Dependencies:** 002.4
**Created:** 2026-01-12
**Parent:** Task 002: Branch Clustering System

---

## Purpose

Assign optimal integration targets (main, scientific, orchestration-tools) to each feature branch based on clustering results and Task 001 criteria.

---

## Details

Implement a Python module that:
- Takes clustered branches and metrics as input
- Applies Task 001 framework criteria to refine assignments
- Calculates confidence scores for each target assignment
- Generates justification for recommendations
- Outputs categorized_branches.json

---

## Guidance & Standards

- **Architecture:** [Comprehensive Guide](../guidance/COMPREHENSIVE_CLI_ARCHITECTURE_GUIDE.md)
- **Merging:** [Merge Guidance](../guidance/MERGE_GUIDANCE_DOCUMENTATION.md)
- **Patterns:** [Factory Pattern](../guidance/FACTORY_PATTERN_IMPLEMENTATION_GUIDE.md)
- **General:** [Project Guidance](../guidance/README.md)

---

## Success Criteria

- [ ] Assigns targets to all feature branches
- [ ] Provides confidence scores per assignment
- [ ] Generates justification documentation
- [ ] Integrates with Task 001 criteria
- [ ] Outputs standard JSON format

---

## Test Strategy

- Compare with manual assignments
- Test edge cases (equally similar to multiple targets)
- Validate justification quality
- Test integration with Task 001

---

---

## Implementation Notes

_Add implementation notes here as work progresses_

---

## Progress Log

### 2026-01-12
- Subtask file created from main task template
- Ready for implementation
**Dependencies:** 002.4
**Created:** 2026-01-12
**Parent:** Task 002: Branch Clustering System

---

## Purpose

Assign optimal integration targets (main, scientific, orchestration-tools) to each feature branch based on clustering results and Task 001 criteria.

---

## Details

Implement a Python module that:
- Takes clustered branches and metrics as input
- Applies Task 001 framework criteria to refine assignments
- Calculates confidence scores for each target assignment
- Generates justification for recommendations
- Outputs categorized_branches.json

---

## Guidance & Standards

- **Architecture:** [Comprehensive Guide](../guidance/COMPREHENSIVE_CLI_ARCHITECTURE_GUIDE.md)
- **Merging:** [Merge Guidance](../guidance/MERGE_GUIDANCE_DOCUMENTATION.md)
- **Patterns:** [Factory Pattern](../guidance/FACTORY_PATTERN_IMPLEMENTATION_GUIDE.md)
- **General:** [Project Guidance](../guidance/README.md)

---

## Success Criteria

- [ ] Assigns targets to all feature branches
- [ ] Provides confidence scores per assignment
- [ ] Generates justification documentation
- [ ] Integrates with Task 001 criteria
- [ ] Outputs standard JSON format

---

## Test Strategy

- Compare with manual assignments
- Test edge cases (equally similar to multiple targets)
- Validate justification quality
- Test integration with Task 001

---

---

## Implementation Notes

_Add implementation notes here as work progresses_

---

## Progress Log

### 2026-01-12
- Subtask file created from main task template
- Ready for implementation
**Effort:** TBD
**Complexity:** TBD

## Overview/Purpose
Implement a Python module that:
- Takes clustered branches and metrics as input
- Applies Task 001 framework criteria to refine assignments
- Calculates confidence scores for each target assignment
- ...

## Success Criteria

- [ ] [Success criteria to be defined]

## Prerequisites & Dependencies

### Required Before Starting
- [ ] 002.4
**Created:** 2026-01-12
**Parent:** Task 002: Branch Clustering System

---

## Purpose

Assign optimal integration targets (main, scientific, orchestration-tools) to each feature branch based on clustering results and Task 001 criteria.

---

## Details

Implement a Python module that:
- Takes clustered branches and metrics as input
- Applies Task 001 framework criteria to refine assignments
- Calculates confidence scores for each target assignment
- Generates justification for recommendations
- Outputs categorized_branches.json

---

## Guidance & Standards

- **Architecture:** [Comprehensive Guide](../guidance/COMPREHENSIVE_CLI_ARCHITECTURE_GUIDE.md)
- **Merging:** [Merge Guidance](../guidance/MERGE_GUIDANCE_DOCUMENTATION.md)
- **Patterns:** [Factory Pattern](../guidance/FACTORY_PATTERN_IMPLEMENTATION_GUIDE.md)
- **General:** [Project Guidance](../guidance/README.md)

---

## Success Criteria

- [ ] Assigns targets to all feature branches
- [ ] Provides confidence scores per assignment
- [ ] Generates justification documentation
- [ ] Integrates with Task 001 criteria
- [ ] Outputs standard JSON format

---

## Test Strategy

- Compare with manual assignments
- Test edge cases (equally similar to multiple targets)
- Validate justification quality
- Test integration with Task 001

---

---

## Implementation Notes

_Add implementation notes here as work progresses_

---

## Progress Log

### 2026-01-12
- Subtask file created from main task template
- Ready for implementation

### Blocks (What This Task Unblocks)
- [ ] None specified

### External Dependencies
- [ ] None

## Sub-subtasks Breakdown

# No subtasks defined

## Specification Details

### Task Interface
- **ID**: 
- **Title**: 
- **Status**: pending
**Priority:** high
**Effort:** 24-32 hours
**Complexity:** 7/10
**Dependencies:** 002.4
**Created:** 2026-01-12
**Parent:** Task 002: Branch Clustering System

---

## Purpose

Assign optimal integration targets (main, scientific, orchestration-tools) to each feature branch based on clustering results and Task 001 criteria.

---

## Details

Implement a Python module that:
- Takes clustered branches and metrics as input
- Applies Task 001 framework criteria to refine assignments
- Calculates confidence scores for each target assignment
- Generates justification for recommendations
- Outputs categorized_branches.json

---

## Guidance & Standards

- **Architecture:** [Comprehensive Guide](../guidance/COMPREHENSIVE_CLI_ARCHITECTURE_GUIDE.md)
- **Merging:** [Merge Guidance](../guidance/MERGE_GUIDANCE_DOCUMENTATION.md)
- **Patterns:** [Factory Pattern](../guidance/FACTORY_PATTERN_IMPLEMENTATION_GUIDE.md)
- **General:** [Project Guidance](../guidance/README.md)

---

## Success Criteria

- [ ] Assigns targets to all feature branches
- [ ] Provides confidence scores per assignment
- [ ] Generates justification documentation
- [ ] Integrates with Task 001 criteria
- [ ] Outputs standard JSON format

---

## Test Strategy

- Compare with manual assignments
- Test edge cases (equally similar to multiple targets)
- Validate justification quality
- Test integration with Task 001

---

---

## Implementation Notes

_Add implementation notes here as work progresses_

---

## Progress Log

### 2026-01-12
- Subtask file created from main task template
- Ready for implementation
- **Priority**: high
**Effort:** 24-32 hours
**Complexity:** 7/10
**Dependencies:** 002.4
**Created:** 2026-01-12
**Parent:** Task 002: Branch Clustering System

---

## Purpose

Assign optimal integration targets (main, scientific, orchestration-tools) to each feature branch based on clustering results and Task 001 criteria.

---

## Details

Implement a Python module that:
- Takes clustered branches and metrics as input
- Applies Task 001 framework criteria to refine assignments
- Calculates confidence scores for each target assignment
- Generates justification for recommendations
- Outputs categorized_branches.json

---

## Guidance & Standards

- **Architecture:** [Comprehensive Guide](../guidance/COMPREHENSIVE_CLI_ARCHITECTURE_GUIDE.md)
- **Merging:** [Merge Guidance](../guidance/MERGE_GUIDANCE_DOCUMENTATION.md)
- **Patterns:** [Factory Pattern](../guidance/FACTORY_PATTERN_IMPLEMENTATION_GUIDE.md)
- **General:** [Project Guidance](../guidance/README.md)

---

## Success Criteria

- [ ] Assigns targets to all feature branches
- [ ] Provides confidence scores per assignment
- [ ] Generates justification documentation
- [ ] Integrates with Task 001 criteria
- [ ] Outputs standard JSON format

---

## Test Strategy

- Compare with manual assignments
- Test edge cases (equally similar to multiple targets)
- Validate justification quality
- Test integration with Task 001

---

---

## Implementation Notes

_Add implementation notes here as work progresses_

---

## Progress Log

### 2026-01-12
- Subtask file created from main task template
- Ready for implementation
- **Effort**: N/A
- **Complexity**: N/A

## Implementation Guide

Implement a Python module that:
- Takes clustered branches and metrics as input
- Applies Task 001 framework criteria to refine assignments
- Calculates confidence scores for each target assignment
- Generates justification for recommendations
- Outputs categorized_branches.json

## Configuration Parameters

- **Owner**: TBD
- **Initiative**: TBD
- **Scope**: TBD
- **Focus**: TBD

## Performance Targets

- **Effort Range**: TBD
- **Complexity Level**: TBD

## Testing Strategy

### Unit Tests
- [ ] Tests cover core functionality
- [ ] Edge cases handled appropriately
- [ ] Performance benchmarks met

### Integration Tests
- [ ] Integration with dependent components verified
- [ ] End-to-end workflow tested
- [ ] Error handling verified

### Test Strategy Notes
- Compare with manual assignments
- Test edge cases (equally similar to multiple targets)
- Validate justification quality
- Test integration with Task 001

## Common Gotchas & Solutions

- [ ] [Common issues and solutions to be documented]

## Integration Checkpoint

### Criteria for Moving Forward
- [ ] All success criteria met
- [ ] Code reviewed and approved
- [ ] Tests passing
- [ ] Documentation updated
- [ ] No critical or high severity issues

## Done Definition

### Completion Criteria
- [ ] All success criteria checkboxes marked complete
- [ ] Code quality standards met (PEP 8, documentation)
- [ ] Performance targets achieved
- [ ] All subtasks completed
- [ ] Integration checkpoint criteria satisfied

## Next Steps

1. **Implementation Phase**: Begin with Phase 1 implementation focusing on class structure and architecture
2. **Unit Testing**: Develop comprehensive test suite with 8+ test cases covering all assignment aspects
3. **Integration Testing**: Verify output compatibility with Task 002.6 (PipelineIntegration) input requirements
4. **Performance Validation**: Confirm assignment completes in under 2 seconds for 50+ branches
5. **Code Review**: Submit for peer review ensuring PEP 8 compliance and comprehensive documentation
6. **Handoff Preparation**: Prepare for integration with Task 002.6 once implementation is complete
7. **Documentation**: Complete any remaining documentation gaps identified during implementation


<!-- EXTENDED_METADATA
END_EXTENDED_METADATA -->

## Configuration Parameters

- **Owner**: TBD
- **Initiative**: TBD
- **Scope**: TBD
- **Focus**: TBD

---

<!-- IMPORTED_FROM: backup_task75/task-002.5.md -->
- Assignment hierarchy rules
- Tag definitions and semantics
- Confidence scoring weights
- Affinity calculation parameters
- Reasoning template configurations

---

## Performance Targets

- **Effort Range**: 24-32 hours
- **Complexity Level**: 7/10

## Testing Strategy

### Unit Testing Approach
- **Minimum 8 test cases** covering all assignment aspects
- **Edge case testing** for ambiguous branches, new branches, outlier branches
- **Performance testing** to ensure <2 second execution time
- **Code coverage** >95% across all functions and branches

### Test Cases to Implement

**Test Case 1: Clear Target Assignment**
- Input: Branch with clear characteristics matching main target
- Expected: Assignment to main with high confidence (>0.85)
- Validation: Correct target, confidence score, and reasoning

**Test Case 2: Scientific Branch Assignment**
- Input: Branch with research/experimental characteristics
- Expected: Assignment to scientific with high confidence (>0.80)
- Validation: Correct target, appropriate tags generated

**Test Case 3: Orchestration Tools Assignment**
- Input: Branch with infrastructure/devops characteristics
- Expected: Assignment to orchestration-tools with high confidence (>0.80)
- Validation: Correct target, appropriate tags generated

**Test Case 4: Ambiguous Branch Assignment**
- Input: Branch with mixed characteristics
- Expected: Assignment with moderate confidence (0.60-0.75)
- Validation: Appropriate reasoning for assignment

**Test Case 5: Low Confidence Assignment**
- Input: Branch with very unclear characteristics
- Expected: Assignment with low confidence (<0.65) and human review tag
- Validation: Low confidence score, appropriate review tag

**Test Case 6: Tag Generation Validation**
- Input: Branch with specific characteristics
- Expected: 30+ appropriate tags generated
- Validation: All 6 tag categories represented appropriately

**Test Case 7: Large Batch Assignment**
- Input: 200+ branches with mixed characteristics
- Expected: Performance under 2 seconds, no memory issues
- Validation: All branches assigned, memory usage <100MB

**Test Case 8: Integration Pipeline Test**
- Input: Real clustering outputs from Task 002.4
- Expected: Successful assignment with proper output format
- Validation: Output matches specification exactly

### Integration Testing
- Test with real clustering outputs from Task 002.4
- Verify output compatibility with Task 002.6 (PipelineIntegration)
- End-to-end pipeline validation
- Cross-validation with manual assignment assessment

## Common Gotchas & Solutions

### Gotcha 1: Confidence Score Calibration ⚠️
**Problem:** Confidence scores don't accurately reflect assignment certainty
**Symptom:** High confidence scores for ambiguous assignments or low scores for clear assignments
**Root Cause:** Not properly calibrating confidence thresholds across different decision levels
**Solution:** Implement proper confidence calibration with validation
```python
def calculate_confidence(self, decision_level: str, metric_values: dict) -> float:
    """
    Calculate confidence based on decision level and metric values
    Level 1 (heuristic): 0.95 if rule matches perfectly
    Level 2 (affinity): Based on distance to archetype
    Level 3 (consensus): Based on cluster agreement
    Level 4 (default): Fixed 0.65
    """
    if decision_level == "heuristic":
        return 0.95 if self._rule_matches_perfectly(metric_values) else 0.0
    elif decision_level == "affinity":
        # Calculate based on distance to archetype
        distance = self._calculate_distance_to_archetype(metric_values)
        return max(0.0, min(1.0, 1.0 - distance))  # Invert distance
    elif decision_level == "consensus":
        # Based on cluster agreement percentage
        return self._calculate_cluster_agreement(metric_values)
    else:  # default
        return 0.65  # Fixed confidence for default assignments
```

### Gotcha 2: Tag Generation Logic ⚠️
**Problem:** Generated tags don't accurately reflect branch characteristics
**Symptom:** Inconsistent or irrelevant tags generated for branches
**Root Cause:** Not properly linking metrics to appropriate tag categories
**Solution:** Implement systematic tag generation with metric-to-tag mapping
```python
def generate_tags(self, branch_metrics: dict, assignment: str) -> list:
    tags = []

    # Scope tags based on metric values
    if branch_metrics['code_churn'] > 0.7:
        tags.extend(['high-churn', 'refactoring', 'breaking-changes'])
    elif branch_metrics['code_churn'] < 0.3:
        tags.extend(['low-churn', 'incremental', 'safe'])

    # Complexity tags
    if branch_metrics['complexity_score'] > 0.8:
        tags.extend(['high-complexity', 'requires-expert-review'])
    elif branch_metrics['complexity_score'] < 0.4:
        tags.extend(['low-complexity', 'junior-friendly'])

    # Integration target tags
    if assignment == 'main':
        tags.extend(['production-ready', 'high-confidence', 'stable'])
    elif assignment == 'scientific':
        tags.extend(['experimental', 'research', 'prototype'])
    elif assignment == 'orchestration-tools':
        tags.extend(['infrastructure', 'devops', 'automation'])

    # Add conditional tags based on combinations
    if 'high-churn' in tags and 'core-module' in branch_metrics.get('affected_modules', []):
        tags.append('high-risk')

    return list(set(tags))  # Remove duplicates
```

### Gotcha 3: Decision Hierarchy Conflicts ⚠️
**Problem:** Different decision levels produce conflicting assignments
**Symptom:** Heuristic rules suggest main but cluster consensus suggests scientific
**Root Cause:** Not properly prioritizing decision levels in hierarchy
**Solution:** Implement clear hierarchy with proper precedence rules
```python
def assign_integration_target(self, branch_data: dict) -> dict:
    # Level 1: Heuristic rules (highest priority)
    heuristic_result = self._apply_heuristic_rules(branch_data)
    if heuristic_result and heuristic_result.confidence > 0.90:
        return {
            'target': heuristic_result.target,
            'confidence': heuristic_result.confidence,
            'reasoning': f"Heuristic match: {heuristic_result.reason}",
            'decision_level': 'heuristic'
        }

    # Level 2: Affinity scoring
    affinity_result = self._calculate_affinity_scores(branch_data)
    if affinity_result.max_score > 0.75:
        return {
            'target': affinity_result.best_target,
            'confidence': affinity_result.max_score,
            'reasoning': f"Affinity match: {affinity_result.reason}",
            'decision_level': 'affinity'
        }

    # Level 3: Cluster consensus
    cluster_result = self._get_cluster_consensus(branch_data)
    if cluster_result.confidence > 0.65:
        return {
            'target': cluster_result.target,
            'confidence': cluster_result.confidence,
            'reasoning': f"Cluster consensus: {cluster_result.reason}",
            'decision_level': 'consensus'
        }

    # Level 4: Default assignment
    return {
        'target': 'main',  # Default to main
        'confidence': 0.60,
        'reasoning': "Default assignment based on Task 001 criteria",
        'decision_level': 'default'
    }
```

### Gotcha 4: Integration with Task 001 Criteria ⚠️
**Problem:** Not properly incorporating Task 001 criteria into assignments
**Symptom:** Assignments don't align with established Task 001 requirements
**Root Cause:** Not accessing or applying Task 001 criteria during assignment
**Solution:** Integrate Task 001 criteria into decision process
```python
def _apply_task_001_criteria(self, branch_data: dict, candidate_targets: list) -> list:
    """
    Apply Task 001 criteria to filter/reweight candidate targets
    """
    # Load Task 001 criteria (from config or API)
    task_001_criteria = self._load_task_001_criteria()

    adjusted_targets = []
    for target in candidate_targets:
        score_adjustment = 0.0

        # Apply criteria adjustments
        if target == 'main' and task_001_criteria.get('production_readiness', False):
            if self._is_production_ready(branch_data):
                score_adjustment += 0.1
            else:
                score_adjustment -= 0.2

        if target == 'scientific' and task_001_criteria.get('research_alignment', False):
            if self._shows_research_characteristics(branch_data):
                score_adjustment += 0.15
            else:
                score_adjustment -= 0.1

        adjusted_targets.append({
            'target': target['target'],
            'original_score': target['score'],
            'adjusted_score': max(0.0, min(1.0, target['score'] + score_adjustment)),
            'criteria_applied': task_001_criteria
        })

    return sorted(adjusted_targets, key=lambda x: x['adjusted_score'], reverse=True)
```

### Gotcha 5: Performance with Large Branch Sets ⚠️
**Problem:** Slow performance when processing 100+ branch assignments
**Symptom:** Assignment taking more than 2 seconds for large sets
**Root Cause:** Not optimizing for bulk operations or using inefficient algorithms
**Solution:** Implement batch processing and optimization strategies
```python
def assign_targets_batch(self, branch_list: list) -> dict:
    """
    Efficiently assign targets to multiple branches
    """
    # Pre-process common data
    cluster_data = self._preprocess_cluster_data(branch_list)

    # Batch process with optimized operations
    results = {}
    batch_size = 50  # Process in batches to manage memory

    for i in range(0, len(branch_list), batch_size):
        batch = branch_list[i:i+batch_size]

        # Process batch with shared computations
        batch_results = []
        for branch in batch:
            result = self.assign_integration_target(
                branch_data=branch,
                precomputed_cluster_data=cluster_data
            )
            batch_results.append(result)

        # Add batch results to main results
        for j, result in enumerate(batch_results):
            branch_name = batch[j]['branch_name']
            results[branch_name] = result

    return results
```

## Integration Checkpoint

### Criteria for Moving Forward
- [ ] All success criteria met
- [ ] Code reviewed and approved
- [ ] Tests passing
- [ ] Documentation updated
- [ ] No critical or high severity issues

---

<!-- IMPORTED_FROM: backup_task75/task-002.5.md -->
**When to move to 002.6:**
- [ ] All 8 subtasks complete
- [ ] Unit tests passing (>90% coverage)
- [ ] Accepts output from Task 002.4
- [ ] Generates 30+ tags per branch
- [ ] Output matches specification
- [ ] Ready for pipeline integration

---

## Done Definition

### Completion Criteria
- [ ] All success criteria met
- [ ] Code reviewed and approved
- [ ] Tests passing
- [ ] Documentation updated

---

<!-- IMPORTED_FROM: backup_task75/task-002.5.md -->
Task 002.5 is done when:
1. All 8 subtasks marked complete
2. Unit tests pass (>95% coverage)
3. Code review approved
4. Generates 30+ comprehensive tags
5. Assignment reasoning validated
6. Ready for hand-off to Task 002.6

## Next Steps

1. **Implementation Phase**: Begin with Phase 1 implementation focusing on class structure and architecture
2. **Unit Testing**: Develop comprehensive test suite with 8+ test cases covering all assignment aspects
3. **Integration Testing**: Verify output compatibility with Task 002.6 (PipelineIntegration) input requirements
4. **Performance Validation**: Confirm assignment completes in under 2 seconds for 50+ branches
5. **Code Review**: Submit for peer review ensuring PEP 8 compliance and comprehensive documentation
6. **Handoff Preparation**: Prepare for integration with Task 002.6 once implementation is complete
7. **Documentation**: Complete any remaining documentation gaps identified during implementation
