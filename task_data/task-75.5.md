# Task 75.5: IntegrationTargetAssigner

## Purpose
Assign integration targets to clustered branches with comprehensive tagging system. This Stage Two task uses cluster outputs and applies four-level decision hierarchy to assign targets and generate 30+ tags per branch.

**Scope:** IntegrationTargetAssigner class only  
**Effort:** 24-32 hours | **Complexity:** 7/10  
**Status:** Ready when 75.4 complete  
**Blocks:** Task 75.6

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

**Quality Assurance:**
- [ ] Unit tests pass (minimum 8 test cases with >95% coverage)
- [ ] No exceptions raised for valid inputs
- [ ] Performance: <1 second per branch assignment
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

## Configuration Parameters

- Assignment hierarchy rules
- Tag definitions and semantics
- Confidence scoring weights
- Affinity calculation parameters
- Reasoning template configurations

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
