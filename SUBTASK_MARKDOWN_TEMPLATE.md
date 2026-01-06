# Subtask Markdown Definition Template

**Use this template for ALL new and updated subtask files**  
**Standard:** TASK_STRUCTURE_STANDARD.md  
**Effective Date:** January 6, 2026  
**Format Version:** 1.0

---

## Instructions

1. Copy this entire template
2. Replace ALL placeholders `[...]` with actual content
3. Keep section order identical
4. Maintain heading levels (## for sections, ### for subsections)
5. Ensure all 14 sections are present in every file
6. Target: **350-400+ lines per task file**

---

## COMPLETE TEMPLATE (Copy Below This Line)

```markdown
# Task [ID]: [Component Name]

**Status:** [Ready for Implementation | In Progress | Complete | Deferred | Blocked]  
**Priority:** [High | Medium | Low]  
**Effort:** [X-Y hours]  
**Complexity:** [Z/10]  
**Dependencies:** [None | Task IDs if applicable]

---

## Purpose

[2-3 sentence explanation of what this subtask accomplishes and why it matters]

**Scope:** [What's included in this subtask]  
**Key Outputs:** [What this produces that downstream tasks consume]  
**No dependencies** - can start immediately [ONLY IF TRUE; omit otherwise]

---

## Success Criteria

Task [ID] is complete when ALL of the following are met:

### Core Functionality
- [ ] [Specific, measurable requirement 1]
- [ ] [Specific, measurable requirement 2]
- [ ] [Specific, measurable requirement 3]
- [ ] [Continue for all functional requirements...]

### Quality Assurance
- [ ] Unit tests pass (minimum [N] test cases with >[M]% code coverage)
- [ ] No exceptions raised for valid inputs
- [ ] Performance: [specific performance requirement]
- [ ] Code quality: [PEP 8 compliant | Linting passes | etc]
- [ ] Documentation: [Complete docstrings | Type hints | etc]

### Integration Readiness
- [ ] Output format matches [JSON schema | specification | etc] exactly
- [ ] Compatible with [downstream task ID] input requirements
- [ ] Configuration externalized and validated
- [ ] Error handling implemented for all edge cases

---

## Prerequisites & Dependencies

### Required Before Starting
- [ ] [Prerequisite 1: e.g., Task X.Y complete]
- [ ] [Prerequisite 2: e.g., Environment setup complete]
- [ ] [Prerequisite 3: e.g., Development environment configured]

### Blocks / Unblocks
**This task unblocks:**
- Task [ID] (downstream dependency)
- Task [ID] (downstream dependency)

**Blocked by:**
- Task [ID] (if applicable)

### External Dependencies
- Python [version]
- [Library Name] [version]
- [Tool Name] [version]
- [System requirement]

---

## Sub-subtasks Breakdown

### [ID].1: [First sub-subtask name]

**Effort:** [X-Y hours]  
**Depends on:** [None | Task IDs]  
**Complexity:** [Beginner | Intermediate | Advanced]

**What:** [1-sentence description of what this sub-subtask delivers]

**Steps:**
1. [Detailed step 1 with full context and explanation]
   - Why: [Why this step matters]
   - How: [Any special techniques needed]

2. [Detailed step 2]
   - Why: [Explanation]
   - How: [Any special techniques]

3. [Detailed step 3]

[Continue for all steps needed to complete this sub-subtask]

**Success Criteria:**
- [ ] [Measurable criterion 1]
- [ ] [Measurable criterion 2]
- [ ] [Measurable criterion 3]

**Deliverable:** [What code/output this step produces]

---

### [ID].2: [Second sub-subtask name]

**Effort:** [X-Y hours]  
**Depends on:** [[ID].1 | other dependencies]  
**Complexity:** [Beginner | Intermediate | Advanced]

**What:** [1-sentence description]

**Steps:**
1. [Detailed step 1]
   - Why: [Explanation]
   - How: [Techniques]

2. [Detailed step 2]

[Continue...]

**Success Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]

**Deliverable:** [Specific output]

---

[CONTINUE THIS PATTERN FOR ALL SUB-SUBTASKS]

---

## Specification Details

### Class/Function Interface

```python
class [ClassName]:
    def __init__(self, [parameter1]: [type], [parameter2]: [type] = [default]):
        """
        Initialize the [ClassName].
        
        Args:
            [parameter1]: [Description of parameter 1]
            [parameter2]: [Description of parameter 2, default=[default]]
        """
        
    def [method1](self, [param]: [type]) -> [return_type]:
        """
        [1-line description of what method does].
        
        Args:
            [param]: [Description]
            
        Returns:
            [return_type]: [Description of return value]
            
        Raises:
            [ExceptionType]: [When this exception occurs]
        """
```

### Input Format

```json
{
  "field_1": "type_description",
  "field_2": 123,
  "nested": {
    "sub_field": "value"
  }
}
```

### Output Format

```json
{
  "status": "success",
  "result": {
    "metric_1": 0.85,
    "metric_2": 0.92,
    "aggregate": 0.88
  },
  "timestamp": "2026-01-06T10:30:00Z",
  "execution_time_ms": 1234
}
```

### Metric Definitions

| Metric Name | Formula | Range | Notes |
|-------------|---------|-------|-------|
| [metric_1] | [Formula/explanation] | [0, 1] | [Important notes] |
| [metric_2] | [Formula/explanation] | [0, 1] | [Important notes] |
| [aggregate] | weighted_sum([weights]) | [0, 1] | Weighted combination |

### Configuration Schema

```python
DEFAULT_CONFIG = {
    "max_workers": 4,
    "timeout_seconds": 30,
    "cache_enabled": True,
    "log_level": "INFO"
}
```

---

## Implementation Guide

### [ID].1: [Sub-subtask name]

**Objective:** [What this achieves and why it matters]

**Approach:** [High-level description of how to solve this]

**Detailed Implementation Steps:**

**Step 1: [Specific implementation step 1]**

Description of what to do:

```python
def [function_name]([parameters]) -> [return_type]:
    """[Function description]"""
    # Implementation example
    result = process_data(input_data)
    return validate_output(result)
```

Key points:
- [Key point 1]
- [Key point 2]

---

**Step 2: [Specific implementation step 2]**

Description:

```python
def [function_name]([parameters]) -> [return_type]:
    """[Description]"""
    # Your implementation here
    pass
```

Key points:
- [Key point]

---

[CONTINUE FOR ALL STEPS IN THIS SUB-SUBTASK]

**Integration Notes:**
- This output feeds into [downstream task ID]
- Expected usage: [how downstream tasks use this output]

---

### [ID].2: [Next sub-subtask]

**Objective:** [What this achieves]

**Approach:** [High-level approach]

**Detailed Implementation Steps:**

[Same format as above for each step]

---

[CONTINUE FOR ALL SUB-SUBTASKS]

---

## Configuration Parameters

All configurable values should be externalized to a config file or constants:

```python
# Default configuration values
CONFIGURATION = {
    # Performance
    "max_workers": 4,
    "timeout_seconds": 30,
    "batch_size": 100,
    
    # Feature flags
    "enable_caching": True,
    "enable_logging": True,
    "enable_validation": True,
    
    # Thresholds
    "similarity_threshold": 0.7,
    "quality_threshold": 0.85,
    
    # Paths
    "cache_dir": ".taskmaster/cache",
    "output_dir": "./outputs",
    
    # Logging
    "log_level": "INFO",
    "log_file": "task_execution.log"
}
```

**To modify:**
1. Edit the config dictionary
2. Validate against schema
3. Pass to component on initialization

---

## Performance Targets

### Per Component Performance

- Single execution: [X seconds]
- Memory usage: [Y MB]
- Maximum handles: [Z items]

### Scalability Requirements

- [N] items: < [time] seconds
- [M] items: < [time] seconds
- [K] items: < [time] seconds

### Quality Metrics

- No timeouts on standard hardware
- Consistent performance across input sizes
- Graceful degradation on resource constraints

---

## Testing Strategy

### Unit Tests

Minimum test cases required: [N]

```python
# Test 1: Normal operation
def test_normal_case():
    """Verify component works with standard input."""
    input_data = {"field": "value"}
    result = [component].process(input_data)
    assert result["status"] == "success"
    assert 0 <= result["metric"] <= 1


# Test 2: Edge case - minimum input
def test_minimum_input():
    """Verify component handles minimal valid input."""
    input_data = {"field": "minimal"}
    result = [component].process(input_data)
    assert result is not None


# Test 3: Edge case - maximum input
def test_maximum_input():
    """Verify component handles maximum valid input."""
    large_input = generate_large_dataset()
    result = [component].process(large_input)
    assert result["status"] == "success"


# Test 4: Error handling - invalid input
def test_invalid_input():
    """Verify component rejects invalid input gracefully."""
    with pytest.raises(ValueError):
        [component].process({"invalid": "data"})


# Test 5: Error handling - missing fields
def test_missing_fields():
    """Verify component handles missing required fields."""
    partial_input = {"field": "incomplete"}
    with pytest.raises(KeyError):
        [component].process(partial_input)


# Test 6: Output format validation
def test_output_schema():
    """Verify output matches expected schema."""
    result = [component].process(valid_input)
    schema = load_json_schema("output_schema.json")
    jsonschema.validate(result, schema)


# Test 7: Performance requirement
def test_performance():
    """Verify component meets performance targets."""
    start = time.time()
    result = [component].process(standard_input)
    elapsed = time.time() - start
    assert elapsed < 2.0, f"Took {elapsed}s, max 2.0s"


# Test 8: Metric bounds
def test_metric_bounds():
    """Verify all metrics stay in [0, 1] range."""
    result = [component].process(standard_input)
    for metric_name, metric_value in result["metrics"].items():
        assert 0 <= metric_value <= 1, \
            f"{metric_name} out of range: {metric_value}"
```

### Integration Tests

After all sub-subtasks complete:

```python
def test_full_pipeline():
    """Verify this task's output integrates with downstream."""
    # Output from this task
    output = [this_task].run()
    
    # Input to downstream task
    downstream_input = prepare_for_downstream(output)
    
    # Verify downstream can consume this
    downstream_result = [downstream_task].run(downstream_input)
    assert downstream_result["status"] == "success"


def test_output_schema_compliance():
    """Verify output matches JSON schema exactly."""
    result = [component].run()
    with open("output_schema.json") as f:
        schema = json.load(f)
    jsonschema.validate(result, schema)
```

### Coverage Target

- **Minimum code coverage:** >[M]%
- **All branches covered:** Yes
- **All edge cases tested:** Yes
- **Error paths tested:** Yes
- **Integration points tested:** Yes

---

## Common Gotchas & Solutions

### Gotcha 1: [Common mistake 1 - e.g., "Metrics outside range"]

**The Problem:**
[Explanation of what goes wrong]

```python
# WRONG - This can happen:
metric = math.exp(-days / 30)  # Can be > 1.0 sometimes
```

**The Solution:**
[How to fix it]

```python
# RIGHT - Always clamp values:
metric = min(1.0, math.exp(-days / 30))
assert 0 <= metric <= 1, f"Invalid metric: {metric}"
```

**Why:** [Explanation of why this matters]

---

### Gotcha 2: [Common mistake 2 - e.g., "Division by zero"]

**The Problem:**
```python
# WRONG
frequency = commits / days_active  # Crashes if days_active = 0
```

**The Solution:**
```python
# RIGHT
days_active = max(1, days_active)  # Minimum 1 day
frequency = commits / days_active
```

**Why:** [Explanation]

---

### Gotcha 3: [Common mistake 3 - e.g., "Timeout on large inputs"]

**The Problem:**
```python
# WRONG
result = subprocess.run(cmd, ...)  # No timeout, may hang
```

**The Solution:**
```python
# RIGHT
result = subprocess.run(cmd, timeout=30, ...)
try:
    return result.stdout
except subprocess.TimeoutExpired:
    logger.error("Command timed out")
    return None
```

**Why:** [Explanation]

---

### Gotcha 4: [Common mistake 4 - e.g., "Unicode handling"]

**The Problem:**
```python
# WRONG
output = subprocess.check_output(cmd).decode('utf-8')  # May fail
```

**The Solution:**
```python
# RIGHT
output = subprocess.check_output(cmd).decode('utf-8', errors='replace')
```

**Why:** [Explanation]

---

## Integration Checkpoint

**Prerequisites for moving to [next task ID]:**

- [ ] All [N] sub-subtasks marked complete
- [ ] Unit tests passing ([>M]% code coverage)
- [ ] Output matches specification exactly
- [ ] All validation checks passing
- [ ] No validation errors on test data
- [ ] Performance benchmarks met ([X] seconds per operation)
- [ ] Edge cases handled correctly
- [ ] Code review completed and approved
- [ ] Commit message: "feat: complete Task [ID] [Component Name]"

**Sign-off:** When all checkboxes above are marked, this task is ready for integration with [next task].

---

## Done Definition

Task [ID] is **DONE** when ALL of the following are true:

1. ✅ All [N] sub-subtasks marked complete and verified
2. ✅ Unit test suite passes with >[M]% code coverage
3. ✅ Code review completed and approved by [reviewer role]
4. ✅ Output format and values match specification exactly
5. ✅ Output schema validation passes (jsonschema or equivalent)
6. ✅ Documentation complete:
   - [ ] Docstrings on all public methods
   - [ ] README with usage examples
   - [ ] Configuration guide
7. ✅ Performance benchmarks verified
8. ✅ All success criteria checkboxes marked complete
9. ✅ Ready for hand-off to Task [next ID]
10. ✅ Final commit: "feat: complete Task [ID] [Component Name]"

**The task is NOT done if ANY of the above are unchecked.**

---

## Next Steps

### Immediate (Start Now)
1. Implement sub-subtask [ID].1 following the detailed steps
2. Reference the [ID].1 section in "Implementation Guide" above
3. Create unit tests from "Testing Strategy" section

### Week 1
1. Complete all [N] sub-subtasks
2. Write comprehensive unit tests (target: >[M]% coverage)
3. Run full test suite to verify everything works

### Week 2
1. Submit code for review
2. Address review feedback
3. Verify integration checkpoint (all checkboxes above)

### Week 3 (If Multi-Week Task)
1. Complete final integration testing
2. Prepare hand-off to [next task ID]
3. Mark task as complete

**Reference:** See IMPLEMENTATION_INDEX.md for team coordination and other active tasks.

---

## Appendix: Quick Reference

### File Structure
- This file: `task-[ID].md` (complete specification + implementation guide)
- Live code: `[git_location]/[module_name].py`
- Tests: `tests/test_[module_name].py`
- Outputs: `.taskmaster/outputs/`

### Key Documents
- **Standard:** TASK_STRUCTURE_STANDARD.md
- **Dependencies:** COMPREHENSIVE_DEPENDENCY_FRAMEWORK.md
- **Status:** PROJECT_STATE_PHASE_3_READY.md

### Getting Help
- Questions about spec: See "Specification Details" section above
- Implementation questions: See "Implementation Guide" + "Common Gotchas"
- Integration questions: See "Integration Checkpoint" + "Next Steps"
- Project questions: See PROJECT_STATE_PHASE_3_READY.md

---

**Document Version:** 1.0  
**Last Updated:** [Current Date]  
**Status:** [Ready for Implementation | In Progress | Complete]
```

---

## How to Use This Template

### For Creating New Tasks:
1. Copy the template above
2. Replace placeholders with actual content
3. Ensure all 14 sections are present
4. Target: 350-400+ lines

### For Updating Existing Tasks:
1. Open existing task file (e.g., task-002-2.md)
2. Compare with template structure
3. Add missing sections in correct order
4. Expand existing sections to full detail
5. Validate: `grep "^##" task-002-2.md | wc -l` (should = 14)

### Section Validation Checklist:
```bash
# Check that file has all 14 sections
grep "^##" task-XXX.md | wc -l  # Should output: 14

# Check section order
grep "^##" task-XXX.md  # Should show sections in this order:
# 1. Purpose
# 2. Success Criteria
# 3. Prerequisites & Dependencies
# 4. Sub-subtasks Breakdown
# 5. Specification Details
# 6. Implementation Guide
# 7. Configuration Parameters
# 8. Performance Targets
# 9. Testing Strategy
# 10. Common Gotchas & Solutions
# 11. Integration Checkpoint
# 12. Done Definition
# 13. Next Steps
```

---

**Apply this template to ALL tasks in `/new_task_plan/`**

Current Status: task-002-1.md ✅ | task-002-2.md ❌ | ... | task-002-9.md ❌

See MIGRATION_STATUS_ANALYSIS.md for complete audit and action plan.
