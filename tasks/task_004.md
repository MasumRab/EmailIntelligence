# Task 004: Establish Core Branch Alignment Framework

**Status:** pending
**Priority:** high
**Effort:** 20-28 hours
**Complexity:** 6/10
**Dependencies:** None

---

## Overview/Purpose

Configure and integrate foundational elements for branch management, including branch protection rules, merge guards, pre-merge validation scripts, and comprehensive merge validation frameworks, adapted for a single developer workflow.

This task sets up the environment by ensuring existing dependencies (Task 008, 003, 018, 015) are properly configured and integrated into a unified workflow. Local Git settings will reflect branch protection rules via pre-commit hooks and local configuration checks. The goal is to create a local version of these rules and frameworks that a single developer can run before pushing changes, ensuring adherence to governance without needing full CI/CD for every step.

---

## Success Criteria

Task 004 is complete when:

### Core Functionality
- [ ] Git hooks (pre-commit, pre-push) installed and functional in local environment
- [ ] Branch protection rules enforced locally (block direct commits to `main`, `scientific`, `orchestration-tools`)
- [ ] Branch naming conventions validated (require `feature/`, `docs/`, `fix/`, `enhancement/` prefixes)
- [ ] Pre-merge validation scripts (Task 003) executable from hook context
- [ ] Comprehensive merge validation framework (Task 008) invocable from orchestration script

### Quality Assurance
- [ ] All hooks produce clear, actionable error messages on failure
- [ ] Hooks pass silently on valid operations (no noise)
- [ ] Setup script installs hooks idempotently
- [ ] Code follows PEP 8 with comprehensive docstrings

### Integration Readiness
- [ ] Orchestration script sequences all validation calls correctly
- [ ] Environment variables and paths configured for local execution
- [ ] Documentation (Task 015) accurately reflects local setup

---

## Prerequisites & Dependencies

### Required Before Starting
- [ ] Git repository initialized with standard branch structure
- [ ] Python 3.8+ available in development environment

### Blocks (What This Task Unblocks)
- Tasks requiring branch governance enforcement
- CI/CD pipeline integration tasks

### External Dependencies
- Python 3.8+ (subprocess, pathlib, sys)
- Git CLI available on PATH

---

## Sub-subtasks Breakdown

### 004.1: Design Local Git Hook Integration for Branch Protection

**Status:** pending
**Effort:** 6-8 hours
**Dependencies:** None

Define the structure for the local branch alignment framework. Identify appropriate Git hooks (pre-commit, pre-push) and establish the initial directory layout for scripts and configurations.

**Steps:**
1. Research Git hooks to determine suitability for local branch protection
2. Create directory structure: `.githooks/local_alignment/`
3. Document selected hooks and their intended functions
4. Create Python setup script to install hooks into local `.git/hooks/`
5. Verify hook installation is idempotent

**Success Criteria:**
- [ ] Hook selection documented with rationale
- [ ] Directory structure created and committed
- [ ] Setup script installs hooks reliably
- [ ] Hooks trigger on appropriate Git operations

---

### 004.2: Integrate Existing Pre-Merge Validation Scripts and Frameworks

**Status:** pending
**Effort:** 6-8 hours
**Dependencies:** 004.1

Adapt and integrate pre-merge validation scripts (Task 003) and the merge validation framework (Task 008) into the Git hook structure. Ensure these components are executable and provide actionable feedback.

**Steps:**
1. Review interfaces of Task 003 and Task 008 outputs
2. Develop Python wrapper scripts callable by Git hooks
3. Implement result capture and developer-facing reporting
4. Configure environment variables and paths for local execution
5. Test wrapper scripts in isolation

**Success Criteria:**
- [ ] Wrapper scripts execute Task 003 validation logic
- [ ] Wrapper scripts invoke Task 008 framework
- [ ] Failures produce actionable error messages
- [ ] Environment configuration documented

---

### 004.3: Develop Centralized Local Alignment Orchestration Script

**Status:** pending
**Effort:** 8-12 hours
**Dependencies:** 004.1, 004.2

Create the primary Python orchestration script that ties together Git hooks and validation components. This script manages the flow of local branch alignment checks, enforces rules, and prevents destructive merge patterns before push.

**Steps:**
1. Design orchestration logic (branch detection, naming checks, validation sequencing)
2. Implement rule enforcement (block protected branches, require feature branch naming)
3. Create user-facing interface (status messages, error messages, help)
4. Add rollback protection for destructive operations
5. Test complete end-to-end workflow

**Success Criteria:**
- [ ] Script blocks commits to protected branches
- [ ] Script warns on non-standard branch naming
- [ ] Script sequences all validation calls correctly
- [ ] Clear pass/fail output with actionable guidance

---

## Specification Details

### Orchestration Script Interface

```python
#!/usr/bin/env python3
"""Central local alignment orchestrator."""

PROTECTED_BRANCHES = ["main", "scientific", "orchestration-tools"]
FEATURE_PREFIXES = ["feature/", "docs/", "fix/", "enhancement/"]
```

### Key Functions
- `get_current_branch()` — Detect active Git branch via `git rev-parse`
- `is_protected_branch(branch)` — Check against protected branch list
- `is_feature_branch(branch)` — Validate naming convention prefix
- `run_validation()` — Execute pre-merge validation wrapper scripts
- `main()` — Orchestrate checks and enforce rules

### Directory Layout

```
.githooks/
└── local_alignment/
    ├── setup.py              # Hook installer
    ├── orchestrator.py       # Central orchestration script
    └── wrappers/
        ├── pre_merge_wrapper.py   # Task 003 integration
        └── validation_wrapper.py  # Task 008 integration
```

---

## Implementation Guide

### Phase 1: Hook Infrastructure (004.1)
1. Create `.githooks/local_alignment/` directory
2. Write `setup.py` that symlinks or copies hooks into `.git/hooks/`
3. Implement `pre-push` hook that invokes orchestrator

### Phase 2: Validation Integration (004.2)
1. Create `wrappers/pre_merge_wrapper.py` calling Task 003 scripts
2. Create `wrappers/validation_wrapper.py` calling Task 008 framework
3. Each wrapper: execute subprocess, capture output, return exit code

### Phase 3: Orchestration (004.3)
1. Build `orchestrator.py` with branch detection and rule enforcement
2. Wire orchestrator to call wrappers in sequence
3. Implement clear pass/fail messaging

### Reference Implementation

```python
def main():
    branch = get_current_branch()
    print(f"Current branch: {branch}")

    if is_protected_branch(branch):
        print("ERROR: Direct commits to protected branches not allowed")
        print("Please create a feature branch for your changes")
        sys.exit(1)

    if not is_feature_branch(branch):
        print("WARNING: Branch does not follow naming convention")
        print("Recommended prefixes: feature/, docs/, fix/, enhancement/")

    if not run_validation():
        print("VALIDATION FAILED — please fix issues before proceeding")
        sys.exit(1)

    print("Local alignment checks passed")
```

---

## Configuration Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| Protected Branches | `main`, `scientific`, `orchestration-tools` | Configurable list |
| Feature Prefixes | `feature/`, `docs/`, `fix/`, `enhancement/` | Naming convention |
| Hook Types | `pre-commit`, `pre-push` | Primary enforcement points |
| Validation Timeout | 30 seconds | Per-script subprocess timeout |
| Script Language | Python 3.8+ | All hooks and orchestration |

---

## Performance Targets

| Metric | Target |
|--------|--------|
| Hook execution time | < 5 seconds for branch/naming checks |
| Full validation pipeline | < 30 seconds including pre-merge scripts |
| Memory usage | < 50 MB |
| Setup script execution | < 2 seconds |

---

## Testing Strategy

### Unit Tests
- [ ] `is_protected_branch()` returns True for each protected branch
- [ ] `is_protected_branch()` returns False for feature branches
- [ ] `is_feature_branch()` validates all approved prefixes
- [ ] `is_feature_branch()` rejects invalid branch names
- [ ] `get_current_branch()` returns correct branch name

### Integration Tests
- [ ] Pre-push hook blocks push from protected branch
- [ ] Pre-push hook allows push from valid feature branch
- [ ] Invalid branch naming produces warning (not block)
- [ ] Validation failure blocks push with actionable message
- [ ] Complete workflow passes on well-formed feature branch

### Manual Verification
- Test on feature branch (should pass)
- Test on protected branch (should block with error)
- Test with invalid naming (should warn)
- Test with validation failure (should block)

---

## Common Gotchas & Solutions

**Gotcha 1: Hook not executable**
```bash
# WRONG: Hook file lacks execute permission
# RIGHT: Setup script must chmod +x all hook files
chmod +x .git/hooks/pre-push
```

**Gotcha 2: Subprocess path resolution**
```python
# WRONG: Relative path breaks depending on working directory
subprocess.run(["python", "scripts/wrapper.py"])

# RIGHT: Resolve paths relative to git root
repo_root = subprocess.run(
    ["git", "rev-parse", "--show-toplevel"],
    capture_output=True, text=True
).stdout.strip()
script = Path(repo_root) / "scripts" / "wrapper.py"
```

**Gotcha 3: Detached HEAD state**
```python
# WRONG: rev-parse returns "HEAD" in detached state
# RIGHT: Handle detached HEAD explicitly
branch = get_current_branch()
if branch == "HEAD":
    print("WARNING: Detached HEAD — skipping branch checks")
```

---

## Integration Checkpoint

**When to consider Task 004 complete:**

- [ ] All 3 subtasks (004.1, 004.2, 004.3) marked done
- [ ] Hook setup script runs without errors on clean clone
- [ ] Protected branch enforcement verified manually
- [ ] Validation pipeline invokes Task 003 and Task 008 wrappers
- [ ] All unit and integration tests passing
- [ ] No false positives blocking valid developer workflow
- [ ] Documentation updated to reflect local setup

---

## Done Definition

Task 004 is done when:

1. ✅ All 3 subtasks completed and verified
2. ✅ Git hooks install cleanly via setup script
3. ✅ Protected branch commits blocked with clear error
4. ✅ Feature branch naming validated with warnings
5. ✅ Pre-merge validation scripts integrated and callable
6. ✅ Orchestration script sequences all checks correctly
7. ✅ Unit and integration tests pass
8. ✅ Code follows PEP 8, includes docstrings
9. ✅ All success criteria checkboxes marked complete
10. ✅ Commit: `feat: complete Task 004 core branch alignment framework`

---

## Next Steps

1. **Immediate:** Start 004.1 — design hook structure and directory layout
2. **After 004.1:** Implement 004.2 — integrate Task 003/008 wrappers
3. **After 004.2:** Build 004.3 — orchestration script with full rule enforcement
4. **Post-completion:** Verify downstream tasks can leverage the framework
5. **Future:** Extend to CI/CD pipeline integration when ready
