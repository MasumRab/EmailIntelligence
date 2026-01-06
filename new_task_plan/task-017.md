# Task 080: Integrate Pre-merge Validation Framework

**Status:** Ready when Task 079 complete  
**Priority:** High  
**Effort:** 20-28 hours  
**Complexity:** 7/10  
**Dependencies:** Task 079 (Modular Parallel Alignment Framework)  
**Blocks:** Task 083 (E2E Testing and Reporting)

---

## Purpose

Integrate pre-merge validation scripts (Task 019) and comprehensive merge validation framework (Task 009) into the modular orchestration framework (Task 079). This is an **ALIGNMENT PROCESS TASK** - a tool for the alignment workflow, not a feature development task.

**Scope:** Validation integration points only  
**Focus:** Quality gates after each branch integration  
**Blocks:** E2E testing (Task 083) - validation must be tested end-to-end

---

## Success Criteria

Task 080 is complete when:

### Core Functionality
- [ ] Modifies run_alignment_for_branch function to include validation calls
- [ ] Integrates Task 019 (pre-merge validation scripts) correctly
- [ ] Integrates Task 009 (comprehensive merge validation framework) correctly
- [ ] Runs validations after primary integration (Task 077) succeeds
- [ ] Halts alignment if any validation fails
- [ ] Returns structured validation results per branch
- [ ] Handles all validation failure scenarios
- [ ] Generates useful failure notifications for developers
- [ ] Output matches specification exactly

### Quality Gates
- [ ] Pre-merge validation passes on successful alignments
- [ ] Comprehensive validation passes on successful alignments
- [ ] Failed validations prevent branch push
- [ ] Validation failures reported clearly
- [ ] Developer can understand and fix issues
- [ ] Validation timeout handled gracefully

### Quality Assurance
- [ ] Unit tests pass (minimum 8 test cases with >95% coverage)
- [ ] No exceptions raised for valid inputs
- [ ] Performance: <5 seconds per validation suite
- [ ] Code quality: PEP 8 compliant, comprehensive docstrings
- [ ] Validation results match expected format
- [ ] Integration with Task 079 seamless

### Integration Readiness
- [ ] Compatible with Task 079 (Orchestration Framework) output
- [ ] Compatible with Task 083 (E2E Testing) input requirements
- [ ] Configuration externalized and validated
- [ ] Documentation complete and accurate
- [ ] Error catalog from Task 076 properly integrated

---

## Prerequisites & Dependencies

### Required Before Starting
- [ ] Task 079 (orchestrator framework) complete and tested
- [ ] run_alignment_for_branch function signature defined
- [ ] Task 019 (pre-merge validation scripts) available or documented
- [ ] Task 009 (comprehensive merge validation framework) available or documented
- [ ] Python 3.8+ with subprocess module
- [ ] Test infrastructure in place

### Blocks (What This Task Unblocks)
- Task 083 (E2E Testing and Reporting) - requires working validation framework
- Full alignment execution - all branches must pass validation gates

### External Dependencies
- Task 019 validation module (pre-merge scripts)
- Task 009 validation framework (comprehensive validation)
- Task 079 orchestrator framework
- Python subprocess, logging, typing

---

## Sub-subtasks

### 080.1: Design Validation Integration Architecture
**Effort:** 2-3 hours  
**Depends on:** None

**Steps:**
1. Document validation execution points in branch alignment flow
2. Design integration interface with Task 019 and Task 009
3. Define validation result structure
4. Plan validation timeout strategy
5. Design failure notification mechanism

**Success Criteria:**
- [ ] Validation integration points documented
- [ ] Interfaces with Task 019 and 009 specified
- [ ] Validation result structure defined
- [ ] Timeout strategy clear
- [ ] Notification approach documented

---

### 080.2: Implement Task 019 Pre-merge Validation Integration
**Effort:** 3-4 hours  
**Depends on:** 080.1

**Steps:**
1. Create function to invoke Task 019 validation scripts
2. Parse validation output and results
3. Classify validation results (pass/fail/warning)
4. Capture validation errors and messages
5. Handle Task 019 module/script not found gracefully

**Success Criteria:**
- [ ] Calls Task 019 validation successfully
- [ ] Parses validation results correctly
- [ ] Captures all error messages
- [ ] Handles missing Task 019 gracefully
- [ ] Returns structured validation result

---

### 080.3: Implement Task 009 Comprehensive Validation Integration
**Effort:** 3-4 hours  
**Depends on:** 080.1

**Steps:**
1. Create function to invoke Task 009 validation framework
2. Handle API calls to CI/CD system or validation service
3. Parse framework output and results
4. Classify validation results (pass/fail/warning)
5. Handle Task 009 unavailability gracefully

**Success Criteria:**
- [ ] Calls Task 009 validation framework successfully
- [ ] Handles API interactions correctly
- [ ] Parses framework results accurately
- [ ] Classifies validation outcomes
- [ ] Returns structured validation result

---

### 080.4: Implement Validation Failure Handling
**Effort:** 2-3 hours  
**Depends on:** 080.2, 080.3

**Steps:**
1. Implement early exit on Task 019 failure
2. Implement early exit on Task 009 failure
3. Create developer notification function
4. Format failure messages (clear and actionable)
5. Integrate with Task 079 status tracking

**Success Criteria:**
- [ ] Halts alignment on Task 019 failure
- [ ] Halts alignment on Task 009 failure
- [ ] Notifications sent with branch name and failure reason
- [ ] Failure messages clear and helpful
- [ ] Status tracking shows validation failure

---

### 080.5: Implement Logging & Result Formatting
**Effort:** 3-4 hours  
**Depends on:** 080.4

**Steps:**
1. Add detailed logging before validation calls
2. Log validation execution progress
3. Log validation results (success/failure details)
4. Create comprehensive validation report structure
5. Add audit trail with timestamps

**Success Criteria:**
- [ ] Logging clear and helpful for debugging
- [ ] All validation outcomes logged
- [ ] Report structure includes key details
- [ ] Timestamps recorded for all validation steps
- [ ] Audit trail complete

---

### 080.6: Implement Validation Metrics & Tracking
**Effort:** 2-3 hours  
**Depends on:** 080.5

**Steps:**
1. Add validation success rate tracking
2. Track validation failure categories
3. Monitor validation execution times
4. Create per-branch validation summary
5. Add aggregated metrics

**Success Criteria:**
- [ ] Tracks validation success/failure rates
- [ ] Categorizes failure types
- [ ] Records validation durations
- [ ] Per-branch summaries available
- [ ] Aggregated metrics for reports

---

### 080.7: Implement Output Formatting & Schema Validation
**Effort:** 2-3 hours  
**Depends on:** 080.6

**Steps:**
1. Create validation result dict schema
2. Implement output formatting (JSON serialization)
3. Validate output against schema
4. Add field presence validation
5. Format for Task 083 consumption

**Success Criteria:**
- [ ] Validation results structured and formatted
- [ ] Output matches specification schema
- [ ] All required fields present
- [ ] Schema validation passes
- [ ] Ready for Task 083 reporting

---

### 080.8: Write Unit Tests & Integration Tests
**Effort:** 3-4 hours  
**Depends on:** 080.7

**Steps:**
1. Create test fixtures with mock validation responses
2. Implement 8+ unit test cases
3. Test successful validations
4. Test validation failures
5. Test timeout handling
6. Generate coverage report (>95%)

**Success Criteria:**
- [ ] 8+ comprehensive test cases
- [ ] All tests pass consistently
- [ ] Code coverage >95%
- [ ] Successful/failed validations both tested
- [ ] Output format validated

---

## Specification

### Input Format

Receives branch info from Task 079 orchestrator:

```python
branch_info = {
    'branch_name': 'feature/auth',
    'target_branch': 'main',
    'integration_status': 'completed',  # from Task 077
    'errors_detected': [],              # from Task 076
    'repo_path': '/path/to/repo',
    'integration_time_seconds': 12.5
}
```

### Output Format

```json
{
  "branch_name": "feature/auth",
  "validation_status": "passed",
  "pre_merge_validation": {
    "status": "passed",
    "execution_time_seconds": 2.3,
    "checks_run": 8,
    "checks_passed": 8,
    "checks_failed": 0,
    "messages": []
  },
  "comprehensive_validation": {
    "status": "passed",
    "execution_time_seconds": 4.1,
    "framework": "task_009_ci_cd",
    "build_status": "success",
    "test_results": "passed",
    "coverage_percent": 92.5,
    "messages": []
  },
  "overall_validation_time_seconds": 6.4,
  "can_push": true,
  "failure_reason": null,
  "validation_timestamp": "2025-12-22T14:35:30Z"
}
```

### Validation Failure Format

```json
{
  "branch_name": "feature/risky",
  "validation_status": "failed",
  "pre_merge_validation": {
    "status": "passed",
    "execution_time_seconds": 1.8,
    "checks_run": 8,
    "checks_passed": 8,
    "checks_failed": 0,
    "messages": []
  },
  "comprehensive_validation": {
    "status": "failed",
    "execution_time_seconds": 3.2,
    "framework": "task_009_ci_cd",
    "build_status": "failure",
    "test_results": "8 failures, 42 passed",
    "coverage_percent": 78.3,
    "messages": [
      "Test suite failed: test_auth.py::test_password_hash (FAILED)",
      "Code coverage below threshold (78.3% < 80% required)"
    ]
  },
  "overall_validation_time_seconds": 5.0,
  "can_push": false,
  "failure_reason": "comprehensive_validation_failed",
  "failure_details": {
    "validation_type": "comprehensive",
    "check_type": "test_coverage",
    "required": "80%",
    "actual": "78.3%"
  },
  "developer_notification": {
    "recipient": "developer@example.com",
    "subject": "Branch validation failed: feature/risky",
    "message": "Comprehensive validation failed for feature/risky. Code coverage is 78.3%, but 80% is required. Please add tests and push to this branch to retry validation."
  },
  "validation_timestamp": "2025-12-22T14:35:30Z"
}
```

### Integration with Task 079

The modified run_alignment_for_branch function:

```python
def run_alignment_for_branch_with_validation(
    branch_info: dict,
    integration_utility: object,  # Task 077
    error_detector: object,       # Task 076
    validation_framework: object  # Task 080 (this task)
) -> dict:
    """
    Execute alignment with validations.
    
    Returns Task 079 format with validation_results added.
    """
    feature_branch = branch_info['branch_name']
    primary_target = branch_info['target_branch']
    
    # Step 1: Integration (Task 077)
    integration_result = integration_utility.integrate_primary_changes(
        feature_branch, primary_target
    )
    if not integration_result['success']:
        return {
            'branch_name': feature_branch,
            'status': 'failed_integration',
            'error_message': integration_result['error']
        }
    
    # Step 2: Error detection (Task 076)
    errors = error_detector.run_error_detection(feature_branch)
    
    # Step 3: Validation (Task 080) - NEW
    validation_result = validation_framework.run_validations(
        branch_name=feature_branch,
        target_branch=primary_target,
        repo_path=repo_path
    )
    
    if not validation_result['can_push']:
        return {
            'branch_name': feature_branch,
            'status': 'failed_validation',
            'validation_results': validation_result,
            'error_message': validation_result['failure_reason']
        }
    
    # Step 4: Documentation (Task 078)
    doc_summary = doc_generator.generate_changes_summary(
        feature_branch, primary_target
    )
    
    return {
        'branch_name': feature_branch,
        'status': 'completed',
        'validation_results': validation_result,
        'changes_summary': doc_summary
    }
```

---

## Configuration Parameters

```yaml
validation:
  # Task 019 settings
  pre_merge_validation:
    enabled: true
    timeout_seconds: 30
    module_path: "validation/pre_merge_scripts.py"
    required_checks:
      - "imports"
      - "syntax"
      - "formatting"
      - "security_basic"
    
  # Task 009 settings
  comprehensive_validation:
    enabled: true
    timeout_seconds: 60
    framework: "ci_cd"  # or "local_tests"
    ci_cd_endpoint: "http://ci.example.com/api/v1"
    required_checks:
      - "build"
      - "unit_tests"
      - "integration_tests"
      - "code_coverage"
    min_coverage_percent: 80
    
  # Failure handling
  developer_notifications:
    enabled: true
    method: "email"  # or "slack", "console"
    recipients:
      - "team@example.com"
    include_failure_details: true
    include_remediation_hints: true
  
  # Validation reporting
  validation_results_dir: "./validation_reports"
  save_failure_artifacts: true
```

---

## Performance Targets

### Per Component
- Pre-merge validation (Task 019): <30 seconds
- Comprehensive validation (Task 009): <60 seconds
- Failure handling: <5 seconds
- Notifications: <10 seconds

### Full Validation Suite
- Per branch: <5 minutes
- 7 branches: <35 minutes
- 50 branches: <250 minutes (batch processing)

---

## Testing Strategy

### Unit Tests

Minimum 8 test cases:

```python
def test_pre_merge_validation_success():
    """Task 019 validation passes on clean code"""
    
def test_pre_merge_validation_failure():
    """Task 019 catches code issues"""
    
def test_comprehensive_validation_success():
    """Task 009 framework passes on good alignment"""
    
def test_comprehensive_validation_failure():
    """Task 009 framework catches test failures"""
    
def test_validation_failure_halts_alignment():
    """Alignment stops on validation failure"""
    
def test_developer_notification_sent():
    """Notifications sent on validation failure"""
    
def test_validation_result_schema_valid():
    """Output matches specification schema"""
    
def test_validation_timeout_handled():
    """Graceful handling of validation timeout"""
```

### Coverage Target
- Code coverage: >95%
- All validation paths tested
- Success and failure scenarios covered

---

## Common Gotchas & Solutions

**Gotcha 1: Validation framework unavailable**
```python
# WRONG: Crash if Task 009 unavailable
result = ci_cd_api.trigger_build(branch)

# RIGHT: Graceful fallback
try:
    result = ci_cd_api.trigger_build(branch)
except ServiceUnavailable:
    logger.warning("CI/CD unavailable, skipping comprehensive validation")
    result = {'status': 'skipped', 'can_push': True}
```

**Gotcha 2: Validation timeout hangs alignment**
```python
# WRONG: No timeout specified
result = subprocess.run(validation_cmd)

# RIGHT: Always set timeout
result = subprocess.run(validation_cmd, timeout=30)
```

**Gotcha 3: Invalid notification recipients fail silently**
```python
# WRONG: Ignore notification failures
send_notification(recipient, message)

# RIGHT: Log and track notification failures
try:
    send_notification(recipient, message)
except InvalidEmail:
    logger.error(f"Invalid recipient email: {recipient}")
```

**Gotcha 4: Validation result parsing fails on unexpected format**
```python
# WRONG: Assume expected structure
coverage = result['coverage']['percent']

# RIGHT: Validate structure and provide defaults
coverage = result.get('coverage', {}).get('percent', 0)
assert isinstance(coverage, (int, float)), "Coverage must be numeric"
```

**Gotcha 5: Multiple concurrent validations corrupt logs**
```python
# WRONG: Direct file writes from multiple threads
with open('validation.log', 'a') as f:
    f.write(message)  # Race condition

# RIGHT: Use thread-safe logging
logger = logging.getLogger(__name__)
logger.info(message)  # Thread-safe handler
```

---

## Helper Tools (Optional)

The following tools are available to accelerate work or provide validation. **None are required** - every task is completable using only the steps in this file.

### Progress Logging

After completing each sub-subtask, optionally log progress for multi-session continuity:

```python
from memory_api import AgentMemory

memory = AgentMemory()
memory.load_session()

# After completing sub-subtask 080.4
memory.add_work_log(
    action="Completed Task 080.4: Implement Validation Failure Handling",
    details="Early-exit logic working, developer notifications implemented, 10 test cases passing"
)
memory.update_todo("task_080_4", "completed")
memory.save_session()
```

**What this does:** Maintains session state across work sessions, enables agent handoffs, documents progress.  
**Required?** No - git commits are sufficient.  
**See:** MEMORY_API_FOR_TASKS.md for full usage patterns.

---

## Tools Reference

| Tool | Purpose | When to Use | Required? |
|------|---------|-----------|----------|
| Memory API | Progress logging | After each sub-subtask | No |
| next_task.py | Find next task | After completion | No |

**For detailed usage and troubleshooting:** See SCRIPTS_IN_TASK_WORKFLOW.md

---

## Integration Checkpoint

**When to move to Task 083 (E2E Testing and Reporting):**

- [ ] All 8 sub-subtasks complete
- [ ] Unit tests passing (>90% coverage)
- [ ] Integrates with Task 079 orchestrator seamlessly
- [ ] Task 019 validation integration working
- [ ] Task 009 validation integration working
- [ ] Validation failures halt alignment correctly
- [ ] Output matches specification exactly
- [ ] Developer notifications functional
- [ ] Code review approved
- [ ] Ready for Task 083 to test end-to-end

---

## Done Definition

Task 080 is done when:

1. ✅ All 8 sub-subtasks marked complete
2. ✅ Unit tests pass (>95% coverage)
3. ✅ Code review approved
4. ✅ Integrates with Task 079 successfully
5. ✅ Task 019 and Task 009 validations functional
6. ✅ Output matches specification exactly
7. ✅ Documentation complete and accurate
8. ✅ Ready for hand-off to Task 083
9. ✅ Commit: "feat: complete Task 080 Validation Framework Integration"
10. ✅ All success criteria checkboxes marked complete

---

## Next Steps

1. **Immediate:** Implement sub-subtask 080.1 (Design Validation Integration Architecture)
2. **Days 1-2:** Complete all 8 sub-subtasks
3. **Day 3:** Write and test unit tests (target: >95% coverage)
4. **Day 4:** Code review and refinement
5. **Day 5:** Ready for Task 083 (E2E Testing and Reporting)

**Reference:** This validation framework ensures alignment quality - all branches must pass validation gates before merging.

---

**Last Updated:** January 6, 2026  
**Structure:** TASK_STRUCTURE_STANDARD.md  
**Phase:** Retrofit - Legacy task format to complete standard format
