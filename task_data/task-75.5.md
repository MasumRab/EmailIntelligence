# Task 75.5: IntegrationTargetAssigner

## Purpose
Assign integration targets to clustered branches with comprehensive tagging system. This Stage Two task uses cluster outputs and applies four-level decision hierarchy to assign targets and generate 30+ tags per branch.

**Scope:** IntegrationTargetAssigner class only  
**Effort:** 24-32 hours | **Complexity:** 7/10  
**Status:** Ready when 75.4 complete  
**Blocks:** Task 75.6

---

## Quick Navigation

Navigate this document using these links:

- [Purpose](#purpose)
- [Success Criteria](#success-criteria)
- [Tag System Overview](#tag-system-overview)
- [Subtasks Overview](#subtasks-overview)
- [Subtask Details](#subtasks)
- [Configuration & Defaults](#configuration--defaults)
- [Technical Reference](#technical-reference)
- [Common Gotchas & Solutions](#common-gotchas--solutions)
- [Development Workflow](#typical-development-workflow)
- [Integration Handoff](#integration-handoff)
- [Integration Checkpoint](#integration-checkpoint)
- [Done Definition](#done-definition)

**Pro tip:** Use Ctrl+F to search within sections, or click links above to jump directly

---

## Success Criteria

Task 75.5 is complete when:

**Core Functionality:**
- [ ] `IntegrationTargetAssigner` class accepts cluster output from Task 75.4
- [ ] Implements four-level decision hierarchy for target assignment
- [ ] Generates 30+ tags per branch (primary, execution, complexity, content, validation, workflow)
- [ ] Assigns confidence scores and reasoning for each assignment
- [ ] Outputs properly formatted dict with assignments and tags
- [ ] Output matches JSON schema exactly

**Performance Targets:**
- [ ] Assignment: **< 1 second** per branch
- [ ] Tag generation: **< 500ms** per branch
- [ ] Confidence scoring: **< 200ms** per branch
- [ ] Reasoning generation: **< 300ms** per branch
- [ ] Full batch (13 branches): **< 10 seconds**
- [ ] Memory: **< 50 MB** for assignment operations
- [ ] All scores: **[0,1] range** with no NaN values

**Quality Assurance:**
- [ ] Unit tests pass (minimum 8 test cases with **>95% code coverage**)
- [ ] No exceptions raised for valid inputs
- [ ] All confidence scores normalized
- [ ] Code quality: PEP 8 compliant, comprehensive docstrings

**Integration Readiness:**
- [ ] Compatible with Task 75.6 (PipelineIntegration) input requirements
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

## Subtasks Overview

### Dependency Flow Diagram

```
75.5.1 (2-3h)
[Design Hierarchy]
    │
    ├─→ 75.5.2 (4-5h)
    │   [Heuristic Rules]
    │       │
    │       ├─→ 75.5.3 (5-6h) ────────┐
    │       │   [Tag Generation]       │
    │       │                          ├─→ 75.5.7 (2-3h) ──┐
    │       ├─→ 75.5.4 (3-4h) ────────┤  [Output]          │
    │       │   [Affinity Scoring]     │                    ├─→ 75.5.8 (3-4h)
    │       │                          │  [Tests]           │
    │       ├─→ 75.5.5 (3-4h) ────────┤                     │
    │       │   [Confidence]           │                    │
    │       │                          │                    │
    │       └─→ 75.5.6 (3-4h) ────────┘                    │
    │           [Reasoning]                                │
    │                                                      │
    └─ (blocking 75.5.2-6, 75.5.7-8)

Critical Path: 75.5.1 → 75.5.2 → 75.5.3-6 (partial parallel) → 75.5.7 → 75.5.8
Minimum Duration: 24-32 hours (with parallelization)
```

### Parallel Opportunities

**Can run in parallel (after 75.5.2):**
- 75.5.3: Tag generation (5-6 hours)
- 75.5.4: Affinity scoring (3-4 hours)
- 75.5.5: Confidence scoring (3-4 hours)
- 75.5.6: Reasoning generation (3-4 hours)

These four tasks depend only on heuristic rules (75.5.2) and can be done independently. **Estimated parallel execution saves 9-12 hours.**

**Must be sequential:**
- 75.5.1 → 75.5.2 (design prerequisites)
- 75.5.2 → 75.5.3-6 (need rule engine first)
- 75.5.3-6 → 75.5.7 (need all scoring/tagging complete)
- 75.5.7 → 75.5.8 (need output format for testing)

### Timeline with Parallelization

**Days 1: Design (75.5.1)**
- Design 4-level decision hierarchy
- Document confidence scoring approach
- Create reasoning templates

**Days 1-2: Heuristic Rules (75.5.2)**
- Implement rule evaluation engine
- Create Level 1 conditions
- Add confidence scoring mechanism

**Days 2-4: Parallel Implementation (75.5.3-75.5.6)**
- **75.5.3 (Person A, Days 2-4):** Tag generation (30+ tags)
- **75.5.4 (Person B, Days 2-3):** Affinity scoring
- **75.5.5 (Person C, Days 2-3):** Confidence scoring
- **75.5.6 (Person D, Days 2-3):** Reasoning generation
- Merge results at end of Day 3

**Days 4-5: Output & Tests (75.5.7-75.5.8)**
- Day 4: Format output, validation
- Day 5: Implement 8+ unit tests, >95% coverage

---

## Subtasks

### 75.5.1: Design Target Assignment Hierarchy
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


### Implementation Checklist (From HANDOFF)
- [ ] Define 4-level decision hierarchy (heuristics, affinity, consensus, default)
- [ ] Document confidence scoring approach
- [ ] Create reasoning templates for each assignment
- [ ] Document edge cases and fallbacks
- [ ] Define target archetypes (main, scientific, orchestration-tools)
---

### 75.5.2: Implement Heuristic Rule Engine
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


### Implementation Checklist (From HANDOFF)
- [ ] Implement rule evaluation engine
- [ ] Create conditions for Level 1 (heuristic rules)
- [ ] Implement confidence scoring mechanism
- [ ] Add reasoning generation
- [ ] Handle rule conflicts gracefully
---

### 75.5.3: Implement Tag Generation System
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


### Implementation Checklist (From HANDOFF)
- [ ] Generate tags from all 6 categories (scope, risk, complexity, status, impact, domain, validation, integration)
- [ ] Implement tag validation logic
- [ ] Create conditional tag logic (complexity → validation)
- [ ] Generate 30+ unique tags per branch
- [ ] Document tag semantics
---

### 75.5.4: Implement Affinity Scoring
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


### Implementation Checklist (From HANDOFF)
- [ ] Design affinity metrics based on cluster cohesion
- [ ] Implement cluster-based affinity calculation
- [ ] Implement change-based affinity calculation
- [ ] Combine affinities into weighted scores
- [ ] Normalize scores to [0,1]
---

### 75.5.5: Implement Confidence Scoring
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


### Implementation Checklist (From HANDOFF)
- [ ] Define confidence factors (rule matching, metric agreement)
- [ ] Implement confidence calculation
- [ ] Weight confidence sources appropriately
- [ ] Normalize to [0,1] range
- [ ] Document confidence interpretation
---

### 75.5.6: Implement Reasoning Generation
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


### Implementation Checklist (From HANDOFF)
- [ ] Create reasoning templates for each target
- [ ] Implement fact extraction for reasoning
- [ ] Generate explanatory text per assignment
- [ ] Add reasoning validation
- [ ] Test readability and clarity
---

### 75.5.7: Aggregate & Output Formatting
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

### 75.5.8: Write Unit Tests
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



### Test Case Examples (From HANDOFF)

1. **test_main_target_assignment**: High merge_readiness + low risk
   - Expected: target='main', confidence > 0.9, appropriate tags

2. **test_scientific_target_assignment**: High-churn experimental branch
   - Expected: target='scientific', confidence > 0.7

3. **test_orchestration_target_assignment**: Branch name contains 'orchestration'
   - Expected: target='orchestration-tools', tags include orchestration-branch

4. **test_ambiguous_branch**: Mixed metrics, no clear target
   - Expected: Use cluster consensus or default to main with lower confidence

5. **test_tag_generation_comprehensive**: Various branch characteristics
   - Expected: 30+ tags generated, mutually consistent

6. **test_confidence_score_range**: Any branch
   - Expected: 0 <= confidence <= 1

7. **test_reasoning_generation**: Each assignment
   - Expected: Non-empty, human-readable reasoning text

8. **test_edge_case_new_branch**: 1-2 commits, no merge history
   - Expected: Graceful handling, reasonable assignment

---

## Configuration & Defaults

All parameters should be externalized to configuration files (not hardcoded). Use YAML format:

```yaml
# config/integration_target_assigner.yaml
integration_target_assigner:
  # Decision Hierarchy Thresholds
  level1_merge_readiness_threshold: 0.9  # Level 1 heuristic rule
  level1_integration_risk_threshold: 0.2
  level2_affinity_threshold: 0.70  # Level 2 affinity scoring
  level3_cluster_consensus_threshold: 0.70  # Level 3 consensus
  
  # Confidence Scoring Weights
  heuristic_confidence: 0.95  # Level 1 confidence
  affinity_confidence: 0.70   # Level 2 confidence
  cluster_confidence: 0.60    # Level 3 confidence
  default_confidence: 0.65    # Level 4 fallback
  
  # Affinity Calculation
  commit_history_weight: 0.35  # From Task 75.1
  codebase_structure_weight: 0.35  # From Task 75.2
  diff_distance_weight: 0.30   # From Task 75.3
  
  # Tag Configuration
  enable_content_tags: true  # Generate content type tags
  enable_validation_tags: true  # Generate validation tags
  enable_workflow_tags: true  # Generate workflow tags
  
  # Reasoning Configuration
  include_metric_details: true  # Include supporting metrics in reasoning
  reasoning_length_min: 50  # Minimum characters for reasoning
  reasoning_length_max: 500  # Maximum characters for reasoning
```

**How to use in code:**
```python
import yaml

def load_config(config_path='config/integration_target_assigner.yaml'):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)['integration_target_assigner']

config = load_config()
MERGE_READINESS_THRESHOLD = config['level1_merge_readiness_threshold']
AFFINITY_THRESHOLD = config['level2_affinity_threshold']
# ... etc
```

**Why externalize?**
- Tune thresholds without code recompilation
- Different configurations for different project types
- Adjust confidence weights based on organizational risk tolerance
- Enable/disable tag types based on needs
- Easy A/B testing of decision rules

---


## Technical Reference (From HANDOFF)

### Four-Level Decision Hierarchy

**Level 1: Heuristic Rules (95% confidence)**
```
IF (merge_readiness > 0.9 AND integration_risk < 0.2) → main (95%)
IF (branch_name contains "science" OR "data") → scientific (92%)
IF (branch_name contains "orchestration" OR "devops") → orchestration-tools (94%)
IF (code_churn < 0.3 AND files_affected < 10) → main (90%)
```

**Level 2: Affinity Scoring (70% confidence)**
- Compare metrics against target archetypes
- Compute cosine similarity to each archetype
- Highest similarity with >0.70 threshold = assignment

**Level 3: Cluster Consensus (60% confidence)**
- If Levels 1-2 inconclusive, examine cluster members
- If 70%+ of cluster assigned to one target → assign to that target
- Confidence = cluster cohesion * consensus percentage

**Level 4: Default (65% confidence)**
- Fallback: assign to main with low confidence if no other rule matches

### Target Archetypes
```python
main_archetype = {
    "commit_history": 0.85,  # High merge readiness
    "codebase_structure": 0.90,  # Stable structure
    "diff_distance": 0.75  # Low risk
}
scientific_archetype = {
    "commit_history": 0.65,
    "codebase_structure": 0.70,
    "diff_distance": 0.50
}
orchestration_archetype = {
    "commit_history": 0.70,
    "codebase_structure": 0.75,
    "diff_distance": 0.65
}
```

### Tag Categories (30+ tags total)
- **Scope**: core-feature, minor-feature, experiment, refactoring, bug-fix, infrastructure
- **Risk**: low-risk, medium-risk, high-risk
- **Complexity**: simple, moderate, complex
- **Status**: active-development, stale, ready-for-merge, requires-review, staging
- **File Impact**: low-file-impact, moderate-file-impact, high-file-impact, massive-impact
- **Domain**: authentication, api-changes, orchestration, data-science, testing, documentation
- **Validation**: testing-required-high, testing-required-medium, testing-optional, auto-mergeable
- **Integration**: main-ready, scientific-branch, orchestration-branch
- **Special**: has-breaking-changes, concurrent-development, merge-conflict-risk

### Dependencies & Integration
- **Blocked by:** Task 75.4 (BranchClusterer) (required)
- **Feeds into:** Task 75.6 (PipelineIntegration)
- **No external ML dependencies** - uses basic cosine similarity

---

## Typical Development Workflow

Complete step-by-step git workflow for implementing this task:

### Setup Your Feature Branch

```bash
git checkout -b feat/integration-target-assigner
git push -u origin feat/integration-target-assigner

mkdir -p src/assignment tests/assignment
touch src/assignment/__init__.py
git add src/assignment/
git commit -m "chore: create assignment module structure"
```

### Subtask 75.5.1-75.5.2: Design & Heuristic Rules

```bash
cat > src/assignment/rules.py << 'EOF'
class DecisionHierarchy:
    """Four-level assignment decision hierarchy."""
    
    # Level 1: Heuristic Rules (95% confidence)
    def level1_heuristic_rules(self, branch_metrics):
        if branch_metrics['merge_readiness'] > 0.9 and branch_metrics['integration_risk'] < 0.2:
            return 'main', 0.95
        if 'science' in branch_metrics['name'] or 'data' in branch_metrics['name']:
            return 'scientific', 0.92
        if 'orchestration' in branch_metrics['name']:
            return 'orchestration-tools', 0.94
        return None, None
    
    # Level 2: Affinity Scoring (70% confidence)
    def level2_affinity_scoring(self, branch_metrics, archetypes):
        # Compare against target archetypes
        pass
    
    # Level 3: Cluster Consensus (60% confidence)
    def level3_cluster_consensus(self, branch_id, cluster_assignments):
        # Check cluster consensus
        pass
    
    # Level 4: Default (65% confidence)
    def level4_default(self):
        return 'main', 0.65
EOF

git add src/assignment/rules.py
git commit -m "feat: implement decision hierarchy (75.5.1, 75.5.2)"
```

### Subtasks 75.5.3-75.5.6: Parallel Implementation

```bash
# All 4 subtasks can run in parallel
# Person A: Tag Generation (75.5.3)
cat > src/assignment/tags.py << 'EOF'
def generate_tags(branch_metrics):
    """Generate 30+ tags from branch characteristics."""
    tags = []
    
    # Primary targets (1 required)
    if target == 'main':
        tags.append('tag:main_branch')
    elif target == 'scientific':
        tags.append('tag:scientific_branch')
    
    # Execution context (1 required)
    if parallel_safe:
        tags.append('tag:parallel_safe')
    else:
        tags.append('tag:sequential_required')
    
    # 30+ total tags...
    return tags
EOF

# Person B: Affinity Scoring (75.5.4)
# Person C: Confidence Scoring (75.5.5)
# Person D: Reasoning Generation (75.5.6)

git add src/assignment/tags.py
git commit -m "feat: implement tag generation, affinity, confidence, reasoning (75.5.3-75.5.6)"
```

### Subtasks 75.5.7-75.5.8: Output & Tests

```bash
cat > src/assignment/output.py << 'EOF'
def format_output(assignments, tags, confidence, reasoning):
    """Format into output schema."""
    return {
        'branches': [{
            'branch_name': ...,
            'target_assignment': ...,
            'confidence_score': ...,
            'reasoning': ...,
            'tags': ...
        }]
    }
EOF

cat > tests/assignment/test_assigner.py << 'EOF'
def test_main_target_assignment():
    # High merge_readiness + low risk → main
    pass

def test_confidence_score_range():
    # All confidence in [0,1]
    pass

# 8+ test cases
EOF

git add src/assignment/output.py tests/assignment/
git commit -m "feat: output formatting and comprehensive tests (75.5.7, 75.5.8)"

git push origin feat/integration-target-assigner
gh pr create --title "Complete Task 75.5: IntegrationTargetAssigner" \
             --body "Implements 4-level decision hierarchy, 30+ tag generation, confidence scoring, and reasoning generation. 24-32 hours with 9-12 hour parallelization savings."
```

---

## Integration Handoff

### What Gets Passed to Task 75.6

**Task 75.6 (PipelineIntegration) expects input in this format:**

```python
from src.assignment.assigner import IntegrationTargetAssigner

assigner = IntegrationTargetAssigner(config)
assignment_output = assigner.assign(clustering_output)

# Output is a dict with:
# {
#   "branches": [
#     {
#       "branch_name": "feature-x",
#       "target_assignment": "main",
#       "confidence_score": 0.95,
#       "reasoning": "High stability and merge readiness...",
#       "tags": ["tag:main_branch", "tag:sequential_required", ...],
#       "affinity_score": 0.87,
#       "cluster_id": 1
#     }
#   ],
#   "summary": {
#     "total_branches": 13,
#     "main_target_count": 4,
#     "science_target_count": 5,
#     "orchestration_target_count": 4
#   }
# }
```

**Task 75.6 uses these outputs by:**
1. Reading branch assignments to categorize branches by target
2. Using confidence scores to filter low-confidence assignments
3. Using tags to inform downstream decisions (Tests, Validation, Orchestration)
4. Using reasoning to explain decisions to developers
5. Using affinity scores for prioritization

**Validation before handoff:**
```bash
python -c "
from src.assignment.assigner import IntegrationTargetAssigner
assigner = IntegrationTargetAssigner({...})
result = assigner.assign(clustering_output)

# Check required fields
assert 'branches' in result
assert 'summary' in result

# Check branch structure
for branch in result['branches']:
    assert 'branch_name' in branch
    assert 'target_assignment' in branch
    assert 'confidence_score' in branch
    assert 0 <= branch['confidence_score'] <= 1
    assert len(branch['tags']) >= 30
    assert 'reasoning' in branch and len(branch['reasoning']) > 0

# Check summary
summary = result['summary']
assert summary['total_branches'] == len(result['branches'])
assert 'main_target_count' in summary
assert 'science_target_count' in summary
assert 'orchestration_target_count' in summary

print('✓ Output valid and ready for Task 75.6')
"
```

---

## Common Gotchas & Solutions

### Gotcha 1: Low-Confidence Assignments in Ambiguous Cases ⚠️

**Problem:** Decision hierarchy returns low confidence (0.65) for ambiguous branches
**Symptom:** Downstream tasks uncertain how to process assignment
**Root Cause:** Branch metrics don't clearly match any target archetype

**Solution:**
```python
def assign_with_min_confidence(branch_metrics, min_confidence=0.70):
    """Assignment with fallback to higher-confidence defaults."""
    assignment, confidence = decision_hierarchy(branch_metrics)
    
    if confidence < min_confidence:
        # Fall back to more conservative assignment
        assignment = 'main'  # Main is safest default
        confidence = 0.60  # Flag as low confidence
        reasoning = f"Ambiguous metrics; defaulting to main with low confidence"
    
    return assignment, confidence, reasoning
```

**Test:**
```python
def test_ambiguous_branch_assignment():
    metrics = {'merge_readiness': 0.5, 'risk': 0.5}  # Ambiguous
    assignment, confidence, _ = assign_with_min_confidence(metrics)
    assert assignment == 'main'
    assert confidence <= 0.70
```

---

### Gotcha 2: Tag Count Less Than 30 ⚠️

**Problem:** Generated tags total < 30, failing requirement
**Symptom:** Test fails on tag count validation
**Root Cause:** Not generating all tag categories, or conditional logic filters too aggressively

**Solution:**
```python
def ensure_min_tags(branch_metrics, tags, min_count=30):
    """Ensure minimum tag count."""
    if len(tags) < min_count:
        # Add default tags for missing categories
        tags = add_default_tags(tags, branch_metrics)
    
    assert len(tags) >= min_count, f"Only {len(tags)} tags, need {min_count}"
    return tags
```

**Test:**
```python
def test_minimum_tag_count():
    result = generate_tags(branch_metrics)
    assert len(result['tags']) >= 30, f"Only {len(result['tags'])} tags"
```

---

### Gotcha 3: Conflicting Tag Assignments ⚠️

**Problem:** Generate mutually exclusive tags (e.g., both "simple_merge" and "high_complexity")
**Symptom:** Downstream tasks confused by contradictory tags
**Root Cause:** Complexity tags not validated for consistency

**Solution:**
```python
def validate_tag_consistency(tags):
    """Check for mutually exclusive tags."""
    complexity_tags = [t for t in tags if 'complexity' in t]
    target_tags = [t for t in tags if 'branch' in t]
    
    # Each category should have exactly one mutually exclusive tag
    assert len(complexity_tags) == 1, f"Multiple complexity tags: {complexity_tags}"
    assert len(target_tags) == 1, f"Multiple target tags: {target_tags}"
    
    return tags
```

**Test:**
```python
def test_tag_consistency():
    tags = generate_tags(metrics)
    assert validate_tag_consistency(tags)
```

---

### Gotcha 4: Confidence Scores Not Normalized ⚠️

**Problem:** Confidence scores outside [0, 1] range
**Symptom:** Downstream tasks fail validation
**Root Cause:** Weights not properly normalized, or arithmetic error

**Solution:**
```python
def compute_normalized_confidence(factors):
    """Compute confidence with normalization."""
    confidence = (
        0.40 * factors['rule_match'] +
        0.35 * factors['metric_agreement'] +
        0.25 * factors['cluster_cohesion']
    )
    
    # Clip to [0, 1] range
    confidence = max(0.0, min(1.0, confidence))
    
    assert 0 <= confidence <= 1, f"Confidence out of range: {confidence}"
    return confidence
```

**Test:**
```python
def test_confidence_always_normalized():
    for _ in range(100):
        confidence = compute_normalized_confidence(random_factors)
        assert 0 <= confidence <= 1
```

---

### Gotcha 5: Reasoning Text Too Short or Too Long ⚠️

**Problem:** Generated reasoning too brief (<50 chars) or too long (>500 chars)
**Symptom:** Reasoning validation fails
**Root Cause:** Template text too minimal, or too verbose

**Solution:**
```python
def generate_bounded_reasoning(branch_metrics, target, min_len=50, max_len=500):
    """Generate reasoning within length bounds."""
    template = f"Assigning to {target} because: "
    
    reasoning = template + generate_reasons(branch_metrics)
    
    # Enforce bounds
    if len(reasoning) < min_len:
        reasoning += generate_details(branch_metrics)
    elif len(reasoning) > max_len:
        reasoning = reasoning[:max_len-3] + "..."
    
    assert min_len <= len(reasoning) <= max_len
    return reasoning
```

**Test:**
```python
def test_reasoning_length_bounds():
    reasoning = generate_bounded_reasoning(metrics, 'main')
    assert 50 <= len(reasoning) <= 500
```

---

### Gotcha 6: Target Archetype Mismatch ⚠️

**Problem:** Affinity scoring compares branch metrics against wrong archetype
**Symptom:** Branches assigned to wrong target despite high affinity
**Root Cause:** Archetype definitions inconsistent with actual target characteristics

**Solution:**
```python
def validate_archetypes(archetypes, sample_branches):
    """Validate archetypes match known branch characteristics."""
    for target, archetype in archetypes.items():
        for branch in sample_branches:
            if branch['known_target'] == target:
                # Known correct targets should have high affinity
                affinity = compute_affinity(branch['metrics'], archetype)
                assert affinity > 0.70, f"{branch['name']} low affinity to {target}"
```

**Test:**
```python
def test_archetypes_correct():
    # Known good examples
    main_branch = {'name': 'main', 'merge_readiness': 0.95, 'risk': 0.1}
    aff = compute_affinity(main_branch, archetypes['main'])
    assert aff > 0.80
```

---

### Gotcha 7: Decision Hierarchy Skips Levels ⚠️

**Problem:** Hierarchy returns Level 4 default without checking Levels 2-3
**Symptom:** Branches get wrong target with low confidence
**Root Cause:** Early return in hierarchy, or missing level implementation

**Solution:**
```python
def hierarchical_assignment(branch_metrics, config):
    """Execute all levels, don't skip."""
    # Level 1: Heuristics
    target, conf = level1_heuristics(branch_metrics)
    if conf > 0.90:
        return target, conf, "Level 1: Heuristic match"
    
    # Level 2: Affinity (always check)
    target2, conf2 = level2_affinity(branch_metrics)
    if conf2 > 0.70:
        return target2, conf2, "Level 2: Affinity match"
    
    # Level 3: Cluster (always check)
    target3, conf3 = level3_consensus(branch_metrics)
    if conf3 > 0.60:
        return target3, conf3, "Level 3: Cluster consensus"
    
    # Level 4: Default (always available)
    return level4_default(config)
```

**Test:**
```python
def test_all_levels_checked():
    # Ambiguous metrics - should try all levels
    metrics = {'merge_readiness': 0.50, 'risk': 0.50}
    target, conf, source = hierarchical_assignment(metrics, config)
    # May use any level, but assignment must exist
    assert target in ['main', 'scientific', 'orchestration-tools']
```

---

### Gotcha 8: Tag Generation Loses Context ⚠️

**Problem:** Tags generated without understanding cluster assignment context
**Symptom:** Tags contradictory to assigned target (e.g., "high_risk" tag but "main" assignment)
**Root Cause:** Tag generation doesn't use cluster data

**Solution:**
```python
def generate_contextual_tags(branch_metrics, cluster_data, target_assignment):
    """Generate tags considering cluster context."""
    tags = []
    
    # Use cluster quality metrics
    silhouette = cluster_data['quality_metrics']['silhouette_score']
    
    # Target-specific tags
    if target_assignment == 'main':
        tags.append('tag:main_branch')
        if silhouette > 0.70:
            tags.append('tag:stable_cluster')
    
    # ... more context-aware tagging
    return tags
```

**Test:**
```python
def test_tags_match_target():
    for assignment in ['main', 'scientific', 'orchestration-tools']:
        tags = generate_contextual_tags(metrics, cluster, assignment)
        # Should have target-specific tag
        target_tags = [t for t in tags if assignment in t]
        assert len(target_tags) > 0
```

---

## Integration Checkpoint

**When to move to 75.6:**
- [ ] All 8 subtasks complete
- [ ] Unit tests passing (>90% coverage)
- [ ] Accepts output from Task 75.4
- [ ] Generates 30+ tags per branch
- [ ] Output matches specification
- [ ] Ready for pipeline integration

---

## Done Definition

Task 75.5 is done when:
1. All 8 subtasks marked complete
2. Unit tests pass (>95% coverage)
3. Code review approved
4. Generates 30+ comprehensive tags
5. Assignment reasoning validated
6. Ready for hand-off to Task 75.6
