# Task 0075.5: IntegrationTargetAssigner

## Purpose
Assign integration targets to clustered branches with comprehensive tagging system. This Stage Two task uses cluster outputs and applies four-level decision hierarchy to assign targets and generate 30+ tags per branch.

**Scope:** IntegrationTargetAssigner class only  
**Effort:** 24-32 hours | **Complexity:** 7/10  
**Status:** Ready when 075.4 complete  
**Blocks:** Task 0075.6

---

## Success Criteria

Task 0075.5 is complete when:

**Core Functionality:**
- [ ] `IntegrationTargetAssigner` class accepts cluster output from Task 0075.4
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
- [ ] Compatible with Task 0075.6 (PipelineIntegration) input requirements
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

### 075.5.1: Design Target Assignment Hierarchy
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

### 075.5.2: Implement Heuristic Rule Engine
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

### 075.5.3: Implement Tag Generation System
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

### 075.5.4: Implement Affinity Scoring
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

### 075.5.5: Implement Confidence Scoring
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

### 075.5.6: Implement Reasoning Generation
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

### 075.5.7: Aggregate & Output Formatting
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

### 075.5.8: Write Unit Tests
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

**When to move to 075.6:**
- [ ] All 8 subtasks complete
- [ ] Unit tests passing (>90% coverage)
- [ ] Accepts output from Task 0075.4
- [ ] Generates 30+ tags per branch
- [ ] Output matches specification
- [ ] Ready for pipeline integration

---


---

## Helper Tools (Optional)

The following tools are available to accelerate work or provide validation. **None are required** - every task is completable using only the steps in this file.

### Progress Logging

After completing each sub-subtask, optionally log progress for multi-session continuity:

```python
from memory_api import AgentMemory

memory = AgentMemory()
memory.load_session()

# After completing a sub-subtask
memory.add_work_log(
    action="Completed Task 075.X.Y",
    details="Implementation details and progress"
)
memory.update_todo("task_075_x_y", "completed")
memory.save_session()
```

**What this does:** Maintains session state across work sessions, enables agent handoffs, documents progress.  
**Required?** No - git commits are sufficient.  
**See:** MEMORY_API_FOR_TASKS.md for full usage patterns and examples.

### Check Next Task

After completing this task, see what's next:

```bash
python scripts/next_task.py
```

**See:** SCRIPTS_IN_TASK_WORKFLOW.md § next_task.py for details.

---

## Tools Reference

| Tool | Purpose | When to Use | Required? |
|------|---------|-----------|----------|
| Memory API | Progress logging | After each sub-subtask | No |
| next_task.py | Find next task | After completion | No |

**For detailed usage and troubleshooting:** See SCRIPTS_IN_TASK_WORKFLOW.md (all optional tools documented there)

## Done Definition

Task 0075.5 is done when:
1. All 8 subtasks marked complete
2. Unit tests pass (>95% coverage)
3. Code review approved
4. Generates 30+ comprehensive tags
5. Assignment reasoning validated
6. Ready for hand-off to Task 0075.6


**Last Updated:** January 6, 2026  
**Phase:** 2 Shallow Retrofit  
**Structure:** TASK_STRUCTURE_STANDARD.md
