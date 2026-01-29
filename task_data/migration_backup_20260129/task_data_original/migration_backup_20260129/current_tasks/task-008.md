# Task ID: 008

**Title:** Develop Automated Error Detection Scripts for Merges

**Status:** pending

**Dependencies:** 007

**Priority:** high

**Description:** Implement scripts to automatically detect and flag common merge-related errors such as merge artifacts (<<<<<<<, =======, >>>>>>>), garbled text/encoding issues, missing imports, and accidentally deleted modules after a branch alignment operation.

**Details:**

Create Python scripts to analyze changed files post-merge/rebase. 
1.  **Merge Artifacts:** Use `git diff --check` or `grep -E '^(<<<<<<<|=======|>>>>>>>)'` in changed files to find uncleaned merge markers. 
2.  **Garbled Text/Encoding:** Implement checks for common encoding errors. Files can be opened with `utf-8` and fallbacks (e.g., `errors='replace'`) and then checked for replacement characters or patterns indicating malformed text. Consider using `chardet` for initial encoding detection if files are not strictly UTF-8. 
3.  **Missing Imports:** For Python files, parse the AST (`ast` module) to extract import statements and verify that the imported modules/packages exist in the current environment or codebase. For other languages (if applicable), use `grep` or language-specific parsers to identify import/require statements and check for corresponding file paths. 
4.  **Accidentally Deleted Modules:** Compare the file list before and after alignment using `git diff --name-only --diff-filter=D` to identify deleted files. For modules, check if any deleted files were part of an active import path. The scripts should log findings and, if possible, suggest corrective actions. Output should be concise for a single developer.

**Test Strategy:**

Create test branches with deliberate merge conflicts, garbled text (e.g., inserting non-UTF8 chars), removing an imported file, and introducing un-resolved merge markers. Run the developed scripts on these branches and verify that all error types are correctly identified and reported. Ensure false positives are minimized.

---

## Overview/Purpose

Develop automated error detection scripts that identify and flag common merge-related errors after branch alignment operations. These scripts provide immediate feedback on merge artifacts, encoding issues, missing imports, and deleted modules.

**Scope:** Merge artifact detection, encoding validation, import checking, module deletion detection
**Focus:** Post-merge validation for single developer workflow
**Value Proposition:** Prevents merge-related regressions and data loss

---

## Success Criteria

Task 008 is complete when:

### Functional Requirements
- [ ] Merge artifact detection operational
- [ ] Garbled text/encoding detection working
- [ ] Missing import detection for Python
- [ ] Deleted module detection operational
- [ ] Comprehensive reporting generated
- [ ] False positives minimized
- [ ] Integration with Task 007 complete

### Non-Functional Requirements
- [ ] Script execution time: <15 seconds
- [ ] Code coverage: >90%
- [ ] Error reports clear and actionable
- [ ] AST parsing safe for large files

### Quality Gates
- [ ] Unit tests pass for all detection mechanisms
- [ ] Integration tests pass with Git operations
- [ ] Code review approved
- [ ] Documentation complete

---

## Prerequisites & Dependencies

### Required Before Starting
- [ ] Git repository with feature branches
- [ ] Python 3.8+ environment
- [ ] Task 007: Branch alignment framework
- [ ] chardet library installed
- [ ] ast module available

### Blocks (What This Task Unblocks)
- [ ] Task 016: Branch alignment operations with error detection
- [ ] Task 017: Merge operations with validation
- [ ] Task 022+: All downstream alignment operations

### External Dependencies
- [ ] Python 3.8+
- [ ] Git 2.20+
- [ ] chardet library

### Assumptions & Constraints
- [ ] Developer has access to Git diff output
- [ ] Python files follow standard AST structure
- [ ] Encoding issues are detectable via chardet

---

## Subtasks

### 005.1. Develop Merge Artifact and Deleted Module Detection

**Status:** pending  
**Dependencies:** None  

Create Python scripts to efficiently detect uncleaned merge markers (<<<<<<<, =======, >>>>>>>) within changed files and identify accidentally deleted modules post-merge or rebase operations.

**Details:**

Implement detection for merge artifacts using 'git diff --check' or 'grep -E '^(<<<<<<<|=======|>>>>>>>)' on staged/changed files. For deleted modules, compare the file list before and after alignment using 'git diff --name-only --diff-filter=D' to identify deleted files and check if any were part of an active import path.

### 005.2. Implement Garbled Text and Initial Import Statement Extraction

**Status:** pending  
**Dependencies:** 005.1  

Develop functionality to detect garbled text/encoding issues in changed files and perform initial extraction of import statements from Python files, paying special attention to potential issues from a 'backend' to 'src' migration.

**Details:**

For garbled text, iterate through changed files. Attempt to open files with 'utf-8' encoding and 'errors='replace''. Subsequently, check the content for common replacement characters (e.g., '') that indicate encoding errors. Consider using 'chardet' for more robust encoding detection for non-UTF-8 files. For Python files, use regular expressions or simple string parsing to extract 'import' and 'from ... import' statements to build a list of potential module dependencies. Specifically note any imports referencing 'backend' paths.

### 005.3. Consolidate Error Detection and Implement Comprehensive Import Validation

**Status:** pending  
**Dependencies:** 005.1, 005.2  

Integrate all previously developed error detection mechanisms into a single, robust Python script. This includes performing comprehensive AST-based import validation for Python files, ensuring safe execution, and providing clear, actionable reporting, specifically for `backend` to `src` migration-related import issues.

**Details:**

Combine the detection logic for merge artifacts, deleted modules, garbled text, and import issues. For Python files, use the 'ast' module to parse the Abstract Syntax Tree (AST) to accurately extract all import statements. For each extracted import, verify if the module or package exists in the current environment or codebase. Validate that 'backend' imports are either correctly migrated to 'src' paths or flagged as missing if they still point to non-existent 'backend' locations. Implement safety measures to ensure the script does not perform Git operations that could lead to wrong-branch pushes. The script should output a concise report of all detected errors, including file paths, error types, and suggested corrective actions.

---

## Specification Details

### Technical Interface
```
MergeErrorDetector:
  - __init__(config_path: str)
  - detect_merge_artifacts() -> List[dict]
  - detect_garbled_text() -> List[dict]
  - detect_missing_imports() -> List[dict]
  - detect_deleted_modules() -> List[dict]
  - generate_report() -> dict
```

### Data Models
```python
class MergeArtifact:
  file_path: str
  line_number: int
  marker_type: str  # 'start', 'separator', 'end'

class ImportIssue:
  file_path: str
  import_statement: str
  module_name: str
  missing: bool
  migration_issue: bool

class ErrorReport:
  merge_artifacts: List[MergeArtifact]
  garbled_text: List[dict]
  missing_imports: List[ImportIssue]
  deleted_modules: List[dict]
  total_errors: int
```

### Business Logic
1. Get list of changed files from Git diff
2. For each changed file:
   - Check for merge artifacts
   - Detect garbled text/encoding issues
   - Parse imports (for Python files)
   - Validate import existence
3. Get list of deleted files from Git diff
4. Check if deleted files are imported modules
5. Aggregate all errors
6. Generate comprehensive report

---

## Implementation Guide

### Approach
Implement four detection mechanisms (merge artifacts, garbled text, missing imports, deleted modules) and consolidate into single script with comprehensive reporting.

Rationale: Multiple detection mechanisms ensure all merge-related errors are caught, AST-based import validation ensures accuracy, consolidated script provides unified reporting.

### Code Structure
```
scripts/
  merge_error_detector.py
  detectors/
    merge_artifacts.py
    garbled_text.py
    missing_imports.py
    deleted_modules.py
tests/
  test_merge_error_detector.py
  test_detectors/
```

### Key Implementation Steps
1. Implement merge artifact detection
2. Implement garbled text detection
3. Implement import statement extraction
4. Implement import validation
5. Implement deleted module detection
6. Consolidate all detection mechanisms
7. Create comprehensive reporting
8. Write unit and integration tests

### Integration Points
- Git diff operations
- Task 007: Branch alignment framework
- AST parsing for Python files
- chardet library for encoding detection

---

## Configuration Parameters

### Required Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| git_working_dir | str | "." | Path to Git working directory |
| encoding | str | "utf-8" | Default file encoding |
| backend_migration | bool | False | Check for backend to src migration issues |

### Environmental Variables
| Variable | Required | Description |
|----------|----------|-------------|
| GIT_WORKING_DIR | no | Path to Git working directory |
| DEFAULT_ENCODING | no | Default file encoding |

---

## Performance Targets

### Response Time
- Merge artifact detection: <3 seconds
- Garbled text detection: <5 seconds
- Import validation: <7 seconds
- Deleted module detection: <3 seconds
- Total script execution: <15 seconds

### Resource Utilization
- Memory: <100MB
- Disk I/O: Minimal (Git diff operations)
- CPU: Moderate (AST parsing)

### Scalability
- Support up to 100 changed files
- Support large Python files (>1000 lines)
- Support multiple encoding types

---

## Testing Strategy

### Unit Tests
- Merge artifact detection: 10+ test cases
- Garbled text detection: 10+ test cases
- Import validation: 15+ test cases
- Deleted module detection: 10+ test cases
- Reporting: 10+ test cases

### Integration Tests
- Git diff integration: 5+ test scenarios
- AST parsing safety: 5+ scenarios
- End-to-end detection: 3+ scenarios

### Edge Case Tests
- Large files: Test performance
- Complex merge conflicts: Detect all markers
- Nested imports: Validate correctly
- Mixed encodings: Detect all issues

---

## Common Gotchas & Solutions

### Gotcha 1: AST parsing fails on syntax errors

```python
# WRONG
ast.parse(file_content)  # Crashes on syntax errors

# RIGHT
try:
    ast.parse(file_content)
except SyntaxError:
    logger.warning(f"Syntax error in {file_path}")
    return []  # Skip parsing
```

### Gotcha 2: Git diff includes staged files

```bash
# WRONG
git diff  # Only shows unstaged changes

# RIGHT
git diff --cached  # Shows staged changes
git diff HEAD  # Shows all changes
```

### Gotcha 3: Encoding detection is slow

```python
# WRONG
chardet.detect(content)  # Slow for large files

# RIGHT
# Check first 1000 bytes
chardet.detect(content[:1000])  # Faster
```

---

## Integration Checkpoint

**When to move to downstream tasks:**

- [ ] All 3 subtasks complete
- [ ] All detection mechanisms operational
- [ ] Comprehensive reporting working
- [ ] Tests pass (>90% coverage)
- [ ] Integration with Task 007 tested
- [ ] Code review approved
- [ ] Documentation complete

---

## Done Definition

Task 008 is done when:

1. ✅ All 3 subtasks marked complete
2. ✅ Merge artifact detection operational
3. ✅ Garbled text detection working
4. ✅ Missing import detection operational
5. ✅ Deleted module detection operational
6. ✅ Comprehensive reporting generated
7. ✅ Unit tests pass (>90% coverage)
8. ✅ Integration tests pass
9. ✅ Code review approved
10. ✅ Integration with Task 007 verified
11. ✅ Commit: "feat: implement merge error detection scripts"
12. ✅ All success criteria checkboxes marked complete

---

## Next Steps

1. Test detection with various merge scenarios
2. Validate integration with Task 007
3. Document detection rules and thresholds
4. Optimize performance for large files
5. Move to downstream tasks when validated

---
