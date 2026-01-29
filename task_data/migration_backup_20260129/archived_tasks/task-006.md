# Task ID: 006

**Title:** Develop and Integrate Pre-merge Validation Scripts

**Status:** pending

**Dependencies:** 005

**Priority:** high

**Description:** Create validation scripts to check for the existence of critical files before merges, preventing merge conflicts that cause data loss or missing files.

**Details:**

Identify a list of critical files (e.g., `setup/commands/__init__.py`, `AGENTS.md`, `data/processed/email_data.json` for core JSON data schemas) whose absence would lead to regressions. Develop a script (e.g., Python `scripts/validate_critical_files.py`, or Bash) that checks for the existence and perhaps basic integrity (e.g., non-empty, valid JSON) for critical branches.

### Tags:
- `work_type:script-development`
- `work_type:ci-cd`
- `component:pre-merge-checks`
- `component:file-integrity`
- `scope:devops`
- `scope:quality-assurance`
- `purpose:regression-prevention`
- `purpose:data-integrity`

---

## Overview/Purpose

Develop and integrate automated pre-merge validation scripts to prevent regression-causing file deletions during branch alignment operations. This task ensures critical files are present and valid before allowing merges to main, protecting core system components from accidental removal.

**Scope:** Validation scripts, CI/CD integration, team documentation
**Focus:** Prevention of data loss through automated checks
**Value Proposition:** Blocks merges that would delete critical system files

---

## Success Criteria

Task 006 is complete when:

### Functional Requirements
- [ ] All critical files identified and documented
- [ ] Validation script checks file existence
- [ ] Validation script checks basic file integrity (non-empty, valid JSON where applicable)
- [ ] Script returns non-zero exit code on failure
- [ ] Script returns zero exit code on success
- [ ] CI/CD integration blocks merges when validation fails
- [ ] Documentation created and shared with team

### Non-Functional Requirements
- [ ] Script execution time: <10 seconds for typical repository
- [ ] Code coverage: >90% for validation script
- [ ] Error messages clear and actionable
- [ ] Team documentation comprehensive

### Quality Gates
- [ ] Unit tests pass for validation script
- [ ] Integration tests pass with CI/CD integration
- - [ ] Team review and approval
- - [ ] Documentation complete

---

## Prerequisites & Dependencies

### Required Before Starting
- [ ] Git repository with CI/CD pipeline configured
- [ ] Python 3.8+ environment
- [ ] Write access to project root
- [ ] List of critical files from project documentation

### Blocks (What This Task Unblocks)
- [ ] Task 016: Branch alignment operations with validation safety
- [ ] Task 017: Merge operations with pre-checks
- [ ] Task 022+: All downstream alignment operations

### External Dependencies
- [ ] Python 3.8+
- [ ] Git hooks or CI/CD platform (GitHub Actions, GitLab CI, Jenkins)
- [ ] JSON validation library (jsonschema)

### Assumptions & Constraints
- [ ] CI/CD pipeline has ability to run custom scripts
- [ ] Team has authority to enforce pre-merge checks
- [ ] Critical files list is comprehensive and accurate

---

## Subtasks

### 003.1. Define critical files and validation criteria for pre-merge checks

**Status:** pending  
**Dependencies:** None  

Analyze the codebase to identify all critical files and directories whose absence or emptiness would cause regressions. Specify exact paths and define the validation logic (e.g., existence, non-empty, valid JSON schema for specific files).

**Details:**

Review project structure, specifically `setup/commands/`, `setup/container/`, `AGENTS.md`, `src/core/`, `config/`, and `data/` directories to pinpoint files like `setup/commands/__init__.py`, `setup/container/__init__.py`, `AGENTS.md`, core JSON data schemas (e.g., `data/processed/email_data.json`), configuration files, and any other crucial components. Create a definitive list of absolute or relative paths that must be checked. For JSON files, determine if basic parsing or full schema validation is required.

### 003.2. Develop core file existence and integrity validation script

**Status:** pending  
**Dependencies:** 003.1  

Implement a script (preferably Python for its robust file handling and JSON capabilities, or Bash for simplicity) that takes the defined list of critical files and criteria, then checks for their existence and basic integrity. The script must return a non-zero exit code on failure and a zero exit code on success.

**Details:**

Create a Python script, e.g., `scripts/validate_critical_files.py`. The script should iterate through the list of critical files identified in subtask 1. For each file, it must perform checks such as `os.path.exists()` (or equivalent for Bash), file size (`os.path.getsize() > 0`), and for designated JSON files (like `data/processed/email_data.json`), attempt to load them using `json.loads()` to ensure basic syntactic validity. Detailed error messages should be logged for any detected failures.

### 003.3. Develop unit and integration tests for validation script

**Status:** pending  
**Dependencies:** None  

Create a comprehensive suite of unit and integration tests to ensure the newly developed validation script correctly identifies missing or malformed critical files. These tests should cover both success and various failure scenarios.

**Details:**

For unit tests, mock file system operations to simulate various file states (e.g., missing, empty, malformed JSON). For integration tests, set up a temporary directory structure that mimics a simplified project with critical files. Run the validation script against this temporary structure with valid, missing, and invalid critical files, asserting the correct exit codes and error outputs.

### 003.4. Integrate validation script into CI/CD pipeline as a pre-merge check

**Status:** pending  
**Dependencies:** None  

Configure the project's CI/CD pipeline (e.g., GitHub Actions, GitLab CI, Jenkins) to execute the developed validation script as a mandatory status check for all pull requests targeting critical branches (e.g., `main`, `develop`) before merging is allowed.

**Details:**

Add a new job or step to the relevant CI configuration file, likely `.github/workflows/pull_request.yml`. This job must execute the validation script (e.g., `python scripts/validate_critical_files.py`). Configure the CI system to interpret a non-zero exit code from the script as a build failure, thereby blocking the pull request merge until all critical files are present and valid according to the defined criteria.

### 003.5. Document and communicate pre-merge validation process to the development team

**Status:** pending  
**Dependencies:** 003.4  

Create clear and concise documentation explaining the purpose, scope, functionality, and impact of the new pre-merge validation process. Effectively communicate these changes and their implications to the entire development team, including guidance on how to debug and resolve validation failures.

**Details:**

Update existing developer guidelines (e.g., `CONTRIBUTING.md`) or create a new document in `docs/dev_guides/pre_merge_checks.md` outlining the critical file checks. Include the full list of critical files being validated, an explanation of how the script operates, common scenarios for validation failures, and steps for developers to troubleshoot and rectify issues. Conduct a team announcement or brief meeting to ensure all developers are aware of and understand the new mandatory pre-merge checks.

---

## Specification Details

### Technical Interface
```
validate_critical_files.py:
  - __init__(critical_files: list)
  - validate() -> bool
  - get_validation_report() -> dict
```

### Data Models
```python
class CriticalFile:
    path: str
    required: bool
    integrity_check: str  # 'existence', 'non_empty', 'json_valid'
    description: str

class ValidationResult:
    passed: bool
    failures: List[dict]
    total_files_checked: int
```

### Business Logic
1. Load critical files list from configuration
2. For each critical file, check:
   - File existence
   - File size > 0
   - JSON validity (if applicable)
3. Aggregate results
4. Return exit code: 0 if all checks pass, 1 if any check fails
5. Generate detailed validation report

---

## Implementation Guide

### Approach
Develop Python validation script with JSON schema validation, integrate with CI/CD pipeline, create comprehensive documentation.

Rationale: Python provides robust file handling, JSON validation ensures data integrity, CI/CD integration ensures mandatory checks.

### Code Structure
```
scripts/
  validate_critical_files.py
tests/
  test_validate_critical_files.py
docs/
  dev_guides/
    pre_merge_checks.md
.github/
  workflows/
    pull_request.yml
```

### Key Implementation Steps
1. Create critical files configuration
2. Implement validation script
3. Write unit tests
4. Integrate with CI/CD
5. Create documentation
6. Test with validation failure scenarios

### Integration Points
- CI/CD pipeline (pre-merge check)
- Git hooks (optional local validation)
- Team documentation
- Developer workflow

---

## Configuration Parameters

### Required Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| critical_files_config | str | None | Path to JSON config with critical files list |
| validation_level | str | "standard" | Validation strictness (basic/standard/strict) |

### Environmental Variables
| Variable | Required | Description |
|----------|----------|-------------|
| VALIDATION_CONFIG | yes | Path to critical files configuration |

---

## Performance Targets

### Response Time
- Validation script execution: <10 seconds
- CI/CD check completion: <30 seconds

### Resource Utilization
- Memory: <50MB
- Disk I/O: Minimal (file existence checks only)

### Scalability
- Support up to 100 critical files
- Support validation on large repositories

---

## Testing Strategy

### Unit Tests
- File existence checks: 10+ test cases
- Integrity checks: 10+ test cases
- JSON validation: 10+ test cases
- Edge cases: 10+ test cases

### Integration Tests
- CI/CD integration: 5+ test scenarios
- Team communication: 2+ scenarios
- End-to-end workflow: 3+ scenarios

### Edge Case Tests
- Missing configuration file: Handle gracefully
- Empty critical files: Detect and report
- Malformed JSON: Detect and report
- Large repositories: Test performance

---

## Common Gotchas & Solutions

### Gotcha 1: Relative paths not working

```python
# WRONG
critical_files = ["setup/commands/__init__.py"]  # May fail

# RIGHT
critical_files = ["/full/path/to/setup/commands/__init__.py"]  # Use absolute paths
```

### Gotcha 2: Exit codes not blocking CI/CD

```yaml
# WRONG
- name: Run validation
  run: python scripts/validate_critical_files.py  # May not fail build

# RIGHT
- name: Run validation
  run: |
    python scripts/validate_critical_files.py
    exit $?  # Exit with script's exit code
```

### Gotcha 3: JSON validation too strict

```python
# WRONG
jsonschema.validate(data, schema)  # Fails on any extra fields

# RIGHT
jsonschema.validate(data, schema, ignore_extra_fields=True)  # More lenient
```

---

## Integration Checkpoint

**When to move to downstream tasks:**

- [ ] All 5 subtasks complete
- [ ] Validation script works correctly
- [ ] CI/CD integration tested
- [ ] Documentation complete
- [ ] Team informed
- [ ] Code review approved

---

## Done Definition

Task 006 is done when:

1. ✅ All 5 subtasks marked complete
2. ✅ Validation script created and tested
3. ✅ CI/CD integration operational
4. ✅ Team documentation complete
5. ✅ Unit tests pass (>90% coverage)
6. ✅ Integration tests pass
7. ✅ Code review approved
8. ✅ Team notified
9. ✅ Commit: "feat: implement pre-merge validation scripts"
10. ✅ All success criteria checkboxes marked complete

---

## Next Steps

1. Test validation script with missing critical file
2. Integrate with CI/CD pipeline
3. Create team documentation
4. Communicate changes to team
5. Move to downstream tasks when validated

---
