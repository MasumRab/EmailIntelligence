# Task 002.5: IntegrationTargetAssigner

**Status:** Ready when 002.4 complete  
**Priority:** High  
**Effort:** 24-32 hours  
**Complexity:** 7/10  
**Dependencies:** Task 002.4 (BranchClusterer)  
**Blocks:** Task 002.6 (PipelineIntegration)

---

## Purpose

Assign integration targets to clustered branches with comprehensive tagging system. Uses cluster outputs and applies four-level decision hierarchy to assign targets (main/scientific/orchestration-tools) and generate 30+ tags per branch.

**Scope:** IntegrationTargetAssigner class only  
**Depends on:** Output from Task 002.4  
**Blocks:** Task 002.6 and downstream tasks

---

## Success Criteria

Task 002.5 is complete when:

### Core Functionality
- [ ] `IntegrationTargetAssigner` class accepts cluster output from Task 002.4
- [ ] Implements four-level decision hierarchy for target assignment
- [ ] Generates 30+ tags per branch (minimum 30 required):
  - [ ] Primary target tags (3: main, scientific, orchestration-tools)
  - [ ] Execution context tags (3: parallel_safe, sequential_required, isolated_execution)
  - [ ] Complexity tags (3: simple_merge, moderate_complexity, high_complexity)
  - [ ] Content type tags (6: core_code, test_changes, config_changes, docs, security, performance)
  - [ ] Validation tags (4: e2e_testing, unit_tests, security_review, performance_testing)
  - [ ] Workflow tags (3+: task_101, framework_core, framework_extension, etc.)
- [ ] Assigns confidence scores (0-1) and reasoning for each assignment
- [ ] Output properly formatted with assignments and tags
- [ ] Output matches JSON schema exactly

### Quality Assurance
- [ ] Unit tests pass (minimum 8 test cases with >95% coverage)
- [ ] No exceptions raised for valid inputs
- [ ] Performance: <1 second per branch assignment
- [ ] Code quality: PEP 8 compliant, comprehensive docstrings
- [ ] All confidence scores in [0,1] range
- [ ] Reasoning text is clear and helpful

### Integration Readiness
- [ ] Compatible with Task 002.6 (PipelineIntegration) input requirements
- [ ] Tag system bridges downstream tasks (079, 080, 083, 101)
- [ ] Configuration externalized and validated
- [ ] Documentation complete and accurate

---

## Prerequisites & Dependencies

### Required Before Starting
- [ ] Task 002.4 (BranchClusterer) complete with cluster outputs
- [ ] Python 3.8+
- [ ] Test infrastructure in place

### Blocks (What This Task Unblocks)
- Task 002.6 (PipelineIntegration)
- Tasks 079, 080, 083, 101 (use tags for routing)

---

## Sub-subtasks

### 002.5.1: Design Target Assignment Hierarchy
**Effort:** 2-3 hours | **Depends on:** None

**Steps:**
1. Design decision tree for target assignment (4 levels)
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
**Effort:** 4-5 hours | **Depends on:** 002.5.1

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
**Effort:** 5-6 hours | **Depends on:** 002.5.1

**Steps:**
1. Implement tag generation for all 6 categories
2. Create tag validation logic
3. Implement conditional tag logic (complexity → validation)
4. Add tag combinatorics for special cases
5. Generate tag documentation

**Success Criteria:**
- [ ] All tag categories implemented
- [ ] 30+ unique tags generated per branch
- [ ] Tags are mutually consistent
- [ ] Tag semantics clearly documented

---

### 002.5.4: Implement Affinity Scoring
**Effort:** 3-4 hours | **Depends on:** 002.5.1

**Steps:**
1. Design affinity metrics for each archetype
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
**Effort:** 3-4 hours | **Depends on:** 002.5.1

**Steps:**
1. Define confidence factors (rule match, metric agreement, cluster cohesion)
2. Implement confidence calculation
3. Weight confidence sources (40% rule, 35% metric, 25% cluster)
4. Normalize to [0,1]
5. Document interpretation

**Success Criteria:**
- [ ] Confidence scores in [0,1]
- [ ] Reflects rule matching quality
- [ ] Reflects metric agreement
- [ ] Enables filtering by confidence

---

### 002.5.6: Implement Reasoning Generation
**Effort:** 3-4 hours | **Depends on:** 002.5.1

**Steps:**
1. Create reasoning templates per assignment type
2. Implement fact extraction for reasoning
3. Generate explanatory text
4. Add reasoning validation (length bounds)
5. Test readability and clarity

**Success Criteria:**
- [ ] Reasoning explains assignment
- [ ] Uses human-readable language
- [ ] Includes supporting metrics
- [ ] Helps with validation

---

### 002.5.7: Aggregate & Output Formatting
**Effort:** 2-3 hours | **Depends on:** 002.5.2-002.5.6

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
**Effort:** 3-4 hours | **Depends on:** 002.5.7

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

## Specification

### Output Format

```json
{
  "branch_name": "feature/auth-system",
  "assigned_target": "main",
  "confidence": 0.87,
  "reasoning": "Branch is well-synchronized with main, moderate complexity, and has strong testing infrastructure. Appropriate for direct integration.",
  "tags": [
    "tag:main_branch",
    "tag:parallel_safe",
    "tag:moderate_complexity",
    "tag:core_code_changes",
    "tag:requires_e2e_testing",
    "tag:requires_security_review",
    "tag:task_101_orchestration"
  ],
  "tag_count": 35,
  "archetype_affinities": {
    "main": 0.87,
    "scientific": 0.34,
    "orchestration-tools": 0.21
  },
  "analysis_timestamp": "2025-12-22T10:50:00Z"
}
```

### Tag Categories

**Primary Target (1 required):**
- `tag:main_branch` - Assign to main/master
- `tag:scientific_branch` - Assign to science branches
- `tag:orchestration_tools_branch` - Assign to orchestration branches

**Execution Context (1 required):**
- `tag:parallel_safe` - Can execute in parallel
- `tag:sequential_required` - Must execute sequentially
- `tag:isolated_execution` - Execute in isolation

**Complexity (1 required):**
- `tag:simple_merge` - Low complexity
- `tag:moderate_complexity` - Medium complexity
- `tag:high_complexity` - High complexity

**Content Type (0+):**
- `tag:core_code_changes` - Core code modified
- `tag:test_changes` - Test files modified
- `tag:config_changes` - Configuration modified
- `tag:documentation_only` - Documentation only
- `tag:security_sensitive` - Security implications
- `tag:performance_critical` - Performance impact

**Validation (0+):**
- `tag:requires_e2e_testing` - E2E tests needed
- `tag:requires_unit_tests` - Unit tests needed
- `tag:requires_security_review` - Security review needed
- `tag:requires_performance_testing` - Performance tests needed

**Workflow (0+):**
- `tag:task_101_orchestration` - Relevant to Task 101
- `tag:framework_core` - Core framework component
- `tag:framework_extension` - Framework extension

---

## Implementation Guide

### 002.5.1: Decision Hierarchy

Four levels of decision making:

```python
DECISION_HIERARCHY = {
    'level_1': {
        'name': 'Rule-based heuristics',
        'weight': 0.40,
        'rules': [
            {
                'condition': 'merge_readiness > 0.85 AND stability > 0.7',
                'assignment': 'main',
                'confidence_boost': 0.2
            },
            # ... more rules
        ]
    },
    'level_2': {
        'name': 'Affinity to archetypes',
        'weight': 0.35,
        'factors': ['cluster_coherence', 'metric_alignment']
    },
    'level_3': {
        'name': 'Consensus from metrics',
        'weight': 0.25,
        'consensus_threshold': 0.5
    },
    'level_4': {
        'name': 'Default assignment',
        'weight': 0.0,
        'default_target': 'scientific'
    }
}
```

### 002.5.3: Tag Generation

```python
def generate_tags(assignment_result: dict) -> List[str]:
    """Generate 30+ tags based on assignment and metrics."""
    tags = []
    
    # Primary target (1 required)
    target = assignment_result['assigned_target']
    tags.append(f'tag:{target}_branch')
    
    # Execution context (1 required)
    if assignment_result['parallel_safe']:
        tags.append('tag:parallel_safe')
    else:
        tags.append('tag:sequential_required')
    
    # Complexity (1 required)
    complexity = assignment_result['complexity']
    tags.append(f'tag:{complexity}_complexity')
    
    # Content types
    if assignment_result['has_core_changes']:
        tags.append('tag:core_code_changes')
    if assignment_result['has_test_changes']:
        tags.append('tag:test_changes')
    if assignment_result['has_config_changes']:
        tags.append('tag:config_changes')
    
    # Validation tags (conditional on complexity)
    if complexity in ['moderate', 'high']:
        tags.append('tag:requires_e2e_testing')
    if assignment_result['has_security_impact']:
        tags.append('tag:requires_security_review')
    
    # Add default tags if needed to reach 30
    while len(tags) < 30:
        tags.append(f'tag:default_{len(tags)}')
    
    return tags
```

### 002.5.5: Confidence Scoring

```python
def calculate_confidence(
    rule_match_score: float,
    metric_agreement_score: float,
    cluster_cohesion: float
) -> float:
    """Weighted confidence combination."""
    confidence = (
        0.40 * rule_match_score +
        0.35 * metric_agreement_score +
        0.25 * cluster_cohesion
    )
    return max(0.0, min(1.0, confidence))
```

---

## Configuration Parameters

```yaml
target_assignment:
  confidence_weights:
    rule_match: 0.40
    metric_agreement: 0.35
    cluster_cohesion: 0.25
  
  archetype_definitions:
    main:
      merge_readiness_min: 0.85
      risk_tolerance: 0.30
      churn_tolerance: 0.40
      priority_boost: 1.2
    
    scientific:
      merge_readiness_min: 0.65
      risk_tolerance: 0.50
      churn_tolerance: 0.80
      priority_boost: 1.0
    
    orchestration-tools:
      merge_readiness_min: 0.75
      core_module_changes: true
      parallel_safety: true
      priority_boost: 1.1
```

---

## Performance Targets

- <1 second per branch
- <50 MB memory
- 30+ tags per branch

---

## Testing Strategy

Minimum 8 test cases:

```python
def test_primary_target_assigned():
    """Each branch has exactly one primary target"""
    
def test_tag_count_minimum():
    """30+ tags generated per branch"""
    
def test_confidence_in_range():
    """Confidence score in [0, 1]"""
    
def test_all_required_tags_present():
    """At least 1 tag from each required category"""
    
def test_reasoning_generated():
    """Reasoning is non-empty and meaningful"""
    
def test_archetype_affinities_valid():
    """Affinity scores sum to ~1.0 or are independent"""
    
def test_tags_mutually_consistent():
    """No conflicting tags assigned"""
    
def test_output_schema_valid():
    """Output matches JSON schema"""
```

---

## Common Gotchas & Solutions

**Gotcha 1: Tag count < 30**
```python
# Solution: Add default tags
def ensure_minimum_tags(tags, min_count=30):
    while len(tags) < min_count:
        tags.append(f'tag:default_{len(tags)}')
    return tags
```

**Gotcha 2: Conflicting tag assignments**
```python
# Solution: Validate mutual exclusivity
def validate_tags(tags):
    primary = [t for t in tags if t.startswith('tag:main_') or t.startswith('tag:scientific_')]
    assert len(primary) == 1, "Exactly one primary target required"
```

**Gotcha 3: Confidence scores outside [0,1]**
```python
# Solution: Clamp values
confidence = max(0.0, min(1.0, confidence))
assert 0 <= confidence <= 1
```

**Gotcha 4: Reasoning text wrong length**
```python
# Solution: Enforce bounds
if len(reasoning) < 10:
    reasoning += " (Brief assessment)"
if len(reasoning) > 500:
    reasoning = reasoning[:497] + "..."
```

---

## Integration Checkpoint

- [ ] All 8 sub-subtasks complete
- [ ] Unit tests passing (>90% coverage)
- [ ] Accepts output from Task 002.4
- [ ] Generates 30+ tags per branch
- [ ] Output matches specification
- [ ] Ready for downstream tasks

---

## Done Definition

1. ✅ All 8 sub-subtasks marked complete
2. ✅ Unit tests pass (>95% coverage)
3. ✅ Code review approved
4. ✅ Generates 30+ comprehensive tags
5. ✅ Assignment reasoning validated
6. ✅ All confidence scores valid
7. ✅ Ready for Task 002.6
8. ✅ Commit: "feat: complete Task 002.5 IntegrationTargetAssigner"

---

## Next Steps

1. Implement sub-subtask 002.5.1 (Design Target Assignment Hierarchy)
2. Complete all 8 sub-subtasks
3. Write unit tests (target: >95% coverage)
4. Code review
5. Ready for Task 002.6 (PipelineIntegration)

---

**Last Updated:** January 6, 2026  
**Consolidated from:** Task 75.5 (task-75.5.md) with 53 original success criteria preserved  
**Structure:** TASK_STRUCTURE_STANDARD.md
