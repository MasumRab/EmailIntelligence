# Task 003: Develop and Integrate Pre-merge Validation Scripts

**Status:** pending
**Priority:** high
**Effort:** 16-20 hours
**Complexity:** 5/10
**Dependencies:** None

---

## Purpose

Create validation scripts to check for the existence and integrity of critical files before merges, preventing merge conflicts that cause data loss or missing files. The scripts will be integrated as mandatory CI/CD status checks on pull requests targeting critical branches (`main`, `develop`).

**Scope:** Pre-merge file validation pipeline (script + CI integration + documentation)
**No dependencies** — can start immediately

## Success Criteria

- [ ] Critical file list defined with specific paths and validation rules (existence, non-empty, valid JSON)
- [ ] `scripts/validate_critical_files.py` validates all critical files and returns non-zero on failure
- [ ] Script produces clear, actionable error messages for each failure type
- [ ] Unit tests cover success, missing file, empty file, and malformed JSON scenarios
- [ ] Integration tests verify script behavior against a temporary directory structure
- [ ] CI/CD pipeline runs validation as a mandatory pre-merge check on pull requests
- [ ] Developer documentation explains the process, common failures, and troubleshooting
- [ ] Validation blocks merge when critical files are missing or invalid

## Prerequisites & Dependencies

### Required Before Starting
- [ ] No external prerequisites

### Blocks (What This Task Unblocks)
- Tasks that depend on merge safety guarantees

### External Dependencies
- Python 3.x (standard library: `os`, `json`, `sys`)
- CI/CD platform (GitHub Actions)
- Project test framework (pytest)

## Sub-subtasks Breakdown

### 003.1. Define critical files and validation criteria for pre-merge checks
- **Status:** pending
- **Dependencies:** None
- Analyze the codebase to identify all critical files and directories whose absence or emptiness would cause regressions. Specify exact paths and define validation logic (existence, non-empty, valid JSON). Review `setup/commands/`, `setup/container/`, `src/core/`, `config/`, and `data/` directories. Create a definitive list of paths and validation rules.

### 003.2. Develop core file existence and integrity validation script
- **Status:** pending
- **Dependencies:** 003.1
- Implement `scripts/validate_critical_files.py` that iterates through the critical file list, checking existence via `os.path.exists()`, non-empty via `os.path.getsize() > 0`, and JSON validity via `json.loads()` for designated files. Return exit code 0 on success, non-zero on failure. Log detailed error messages for each failure.

### 003.3. Develop unit and integration tests for validation script
- **Status:** pending
- **Dependencies:** 003.2
- Create pytest tests covering: missing files, empty files, malformed JSON, and all-valid scenarios. Unit tests mock file system operations. Integration tests create a temporary directory structure mimicking the project and run the validation script, asserting correct exit codes and error output.

### 003.4. Integrate validation script into CI/CD pipeline as a pre-merge check
- **Status:** pending
- **Dependencies:** 003.2
- Add a job to `.github/workflows/pull_request.yml` that runs `python scripts/validate_critical_files.py` as a mandatory status check. Configure the CI system to interpret non-zero exit codes as build failures, blocking merge until all critical files pass validation.

### 003.5. Document and communicate pre-merge validation process
- **Status:** pending
- **Dependencies:** 003.4
- Create `docs/dev_guides/pre_merge_checks.md` documenting critical file list, script operation, common failure scenarios, and troubleshooting steps. Update `CONTRIBUTING.md` to reference the new checks.

## Specification Details

### Task Interface
- **ID**: 003
- **Title**: Develop and Integrate Pre-merge Validation Scripts
- **Status**: pending
- **Priority**: high
- **Effort**: 16-20 hours
- **Complexity**: 5/10

### Requirements
- Configurable list of critical files with per-file validation rules
- Exit code 0 on success, non-zero on any failure
- Clear error messages identifying which file failed and why
- CI/CD integration as a blocking pre-merge check
- Developer-facing documentation with troubleshooting guidance

### Key Files
| File | Validation |
|------|------------|
| `setup/commands/__init__.py` | Must exist, non-empty |
| `setup/container/__init__.py` | Must exist, non-empty |
| `AGENTS.md` | Must exist, non-empty |
| `data/processed/email_data.json` | Must exist, valid JSON |

## Implementation Guide

### Phase 1: Discovery (003.1)
Audit the repository to build the definitive critical file list. Categorize files by validation type (existence-only, non-empty, JSON-valid). Document rationale for each file's inclusion.

### Phase 2: Script Development (003.2)
Build `scripts/validate_critical_files.py` with a data-driven design: the critical file list and validation rules should be easily maintainable (e.g., a dict or config at the top of the script). Implement clear logging with file path, expected check, and failure reason.

### Phase 3: Testing (003.3)
Write pytest tests using `tmp_path` fixtures. Cover edge cases: symlinks, permission errors, zero-byte files, JSON with trailing commas. Ensure the script's exit code behavior is tested end-to-end.

### Phase 4: CI/CD Integration (003.4)
Add a lightweight GitHub Actions job that installs Python and runs the validation script. Ensure it runs early in the pipeline to provide fast feedback.

### Phase 5: Documentation (003.5)
Write concise developer docs. Include a "Quick Fix" section for each common failure type.

## Configuration Parameters

- **critical_files**: List of file paths to validate
- **validation_rules**: Per-file validation type (`exists`, `non_empty`, `valid_json`)
- **target_branches**: Branches protected by the check (default: `main`, `develop`)

## Performance Targets

- **Full validation run**: < 5 seconds for up to 50 critical files
- **CI job overhead**: < 30 seconds total (including Python setup)

## Testing Strategy

### Unit Tests
- [ ] Missing file detected and reported correctly
- [ ] Empty file detected for non-empty checks
- [ ] Malformed JSON detected and error message includes parse details
- [ ] Valid file set produces exit code 0
- [ ] Script handles permission errors gracefully

### Integration Tests
- [ ] Temporary directory with valid files → exit code 0
- [ ] Temporary directory with one missing file → exit code non-zero, correct error
- [ ] Temporary directory with invalid JSON → exit code non-zero, correct error
- [ ] Script output parseable by CI systems

### End-to-End Tests
- [ ] Create feature branch, delete a critical file, open PR → validation fails
- [ ] Restore file, re-run → validation passes
- [ ] Verify CI pipeline correctly blocks/allows merge based on validation result

## Common Gotchas & Solutions

| Issue | Solution |
|-------|----------|
| File exists but is empty | Check `os.path.getsize() > 0` separately from `os.path.exists()` |
| JSON file with BOM or encoding issues | Open with `encoding='utf-8-sig'` |
| Path differences across OS | Use `pathlib.Path` for cross-platform paths |
| CI environment lacks project files | Ensure checkout step runs before validation |
| New critical files added but not in list | Document process for updating the critical file list |

## Integration Checkpoint

### Criteria for Moving Forward
- [ ] Critical file list reviewed and approved by team
- [ ] Validation script runs successfully locally
- [ ] All unit and integration tests pass
- [ ] CI pipeline correctly blocks merge on validation failure
- [ ] At least one team member has reviewed the documentation

## Done Definition

### Completion Criteria
- [ ] All 5 subtasks completed and verified
- [ ] `scripts/validate_critical_files.py` handles all validation types
- [ ] All unit, integration, and end-to-end tests passing
- [ ] CI/CD pipeline enforces validation on all PRs to protected branches
- [ ] Developer documentation published and team notified
- [ ] Code quality: PEP 8 compliant, docstrings on public functions

## Next Steps

- [ ] Begin with 003.1 (define critical files) — no dependencies
- [ ] After 003.1, proceed to 003.2 (validation script)
- [ ] 003.3 (tests) and 003.4 (CI/CD) can proceed in parallel after 003.2
- [ ] 003.5 (documentation) after 003.4 is complete
