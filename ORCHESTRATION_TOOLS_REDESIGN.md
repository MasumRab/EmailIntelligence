# Orchestration-Tools Redesign & Refactoring
**Status**: In Progress  
**Date Started**: 2025-11-18  
**Last Updated**: 2025-11-18 17:20  

---

## Executive Summary

Refactoring the orchestration-tools system to:
1. **Reduce hook scope** - Prevent actions & maintain branch safety only
2. **Eliminate file distribution logic from hooks** - Move to dedicated sync script
3. **Create SOLID centralized sync script** - Single source of truth for file distribution
4. **Maintain orchestration-tools* and taskmaster* branch isolation** - Separate workflows

---

## Current State Analysis

### ✗ Problems with Current Design

1. **Oversized Hooks**
   - Hooks doing too much (distribution + validation + syncing)
   - `post-commit`, `post-merge`, `post-checkout` are complex
   - Difficult to maintain and debug

2. **Distributed Logic**
   - File distribution scattered across multiple hooks
   - `post-commit-setup-sync` duplicates work
   - No single source of truth

3. **Unclear Responsibilities**
   - Hooks mixing concerns: safety checks, file distribution, branch management
   - Scripts unclear about when they execute
   - Hard to trace which script does what

4. **Maintenance Burden**
   - Every change requires updating multiple hooks
   - Risk of inconsistency between hooks
   - Testing difficult due to interdependencies

### ✓ What's Working

- Branch detection for orchestration-tools* variants
- Pre-commit safety checks preventing bad commits
- Post-checkout hook recognizing branch switches
- Critical file restoration from git history

---

## Design Goals

### Primary Objectives

1. **Hooks → Safety Only**
   - `pre-commit`: Prevent dangerous commits
   - `post-checkout`: Safety checks on branch switch
   - `post-merge`: Conflict detection
   - Remove all file distribution from hooks

2. **Centralized Sync Script**
   - Single source of truth: `scripts/sync_orchestration_files.sh`
   - SOLID principles: Single Responsibility, Open/Closed, Liskov Substitution
   - Clear, testable, maintainable
   - Called by: user, CI/CD, or hooks (minimal)

3. **Branch Isolation**
   - orchestration-tools* branches: Distribute from central setup/
   - taskmaster* branches: Isolated (no distribution)
   - main/scientific branches: No orchestration involvement

4. **Clear Workflow**
   - User runs sync script explicitly or via launch.py
   - CI/CD runs sync as part of pipeline
   - Hooks only validate and prevent bad states

---

## Implementation Plan

### Phase 1: Audit & Documentation (✓ Complete)
- [x] Identify missing files and restore from git history
- [x] Document current hook functionality (in this file)
- [x] Map which hooks do file distribution (in this file)
- [x] List all files currently distributed (File Distribution Map)

### Phase 2: Design Centralized Sync Script (✓ Complete)
- [x] Create `scripts/sync_orchestration_files.sh` with modular design
- [x] Define sync strategy for each file type (hooks, setup/, configs)
- [x] Add dry-run mode for testing
- [x] Add validation and integrity checking
- [x] Document sync script thoroughly (--help built-in)

### Phase 3: Reduce Hook Scope
- [ ] Remove distribution logic from `post-commit`
- [ ] Remove distribution logic from `post-merge`
- [ ] Remove distribution logic from `post-checkout`
- [ ] Simplify to validation and safety checks only
- [ ] Update hook documentation

### Phase 4: Integration & Testing
- [ ] Test sync script with all branch types
- [ ] Verify hooks work with reduced scope
- [ ] Document new orchestration workflow
- [ ] Create user guide for sync script
- [ ] Add CI/CD integration tests

### Phase 5: Deployment
- [ ] Commit redesigned hooks and sync script
- [ ] Update documentation and guides
- [ ] Test on orchestration-tools branch
- [ ] Deploy to main and scientific branches
- [ ] Monitor for issues

---

## File Distribution Map

### Files Currently Distributed

#### Setup Directory (`setup/`)
- `launch.py` - Main launcher script
- `validation.py` - Environment validation
- `services.py` - Service management
- `environment.py` - Environment setup
- `utils.py` - Utility functions
- `project_config.py` - Project configuration
- `test_stages.py` - Test stage management
- `pyproject.toml` - Project metadata
- `requirements.txt` - Dependencies
- `requirements-dev.txt` - Dev dependencies

#### Scripts Directory (`scripts/`)
- `hooks/` - All git hooks
- `lib/` - Shared libraries
- `install-hooks.sh` - Hook installation
- Other orchestration scripts

#### Configuration Files
- `.flake8` - Flake8 config
- `.pylintrc` - Pylint config
- `.gitignore` - Git ignore rules

#### Root Wrapper
- `launch.py` - Root wrapper to setup/launch.py

---

## Centralized Sync Script Design

### File: `scripts/sync_orchestration_files.sh`

```
Strategy:
1. Source control library (scripts/lib/sync_functions.sh)
2. Define sync_setup_directory()
3. Define sync_hooks()
4. Define sync_config_files()
5. Provide --dry-run, --verify, --rollback options
6. Clear logging and error handling
7. Support both local sync and CI/CD sync
```

### Usage Examples

```bash
# Dry-run to see what would be synced
./scripts/sync_orchestration_files.sh --dry-run

# Sync all files
./scripts/sync_orchestration_files.sh

# Sync specific directory
./scripts/sync_orchestration_files.sh --setup-only

# Verify integrity
./scripts/sync_orchestration_files.sh --verify

# Rollback previous sync
./scripts/sync_orchestration_files.sh --rollback
```

---

## Hook Simplification Target

### Current vs. Desired Hook Size

| Hook | Current Lines | Desired Lines | Reduction |
|------|---------------|---------------|-----------|
| pre-commit | ~130 | ~60 | -54% |
| post-commit | ~150 | ~40 | -73% |
| post-merge | ~75 | ~30 | -60% |
| post-checkout | ~80 | ~35 | -56% |

### Hook Responsibilities (Post-Redesign)

**pre-commit** (60 lines)
- Check for sensitive data leaks
- Prevent commits on wrong branch
- Validate hook integrity

**post-commit** (40 lines)
- Log successful commits
- Verify commit integrity
- Branch tracking only

**post-merge** (30 lines)
- Detect merge conflicts
- Update branch tracking
- No file distribution

**post-checkout** (35 lines)
- Detect branch switches
- Run safety checks
- Suggest sync if needed

---

## Testing Strategy

### Unit Tests
- [ ] Test sync_orchestration_files.sh with mock directories
- [ ] Test dry-run mode output
- [ ] Test rollback functionality
- [ ] Test on orchestration-tools* branches
- [ ] Test on taskmaster* branches
- [ ] Test on main/scientific branches (should skip)

### Integration Tests
- [ ] Full sync workflow from repository clone
- [ ] Verify file integrity after sync
- [ ] Test with modified local files
- [ ] Test concurrent syncs
- [ ] Test with network issues (robustness)

### Hook Tests
- [ ] Simplified hooks still catch bad commits
- [ ] Hooks don't interfere with CI/CD
- [ ] Branch switch detection works
- [ ] No false positives in validation

---

## Tracking Changes

### Recent Commits
1. **3d59ccf8** (2025-11-18 17:20) - Restored missing setup modules and post-commit-setup-sync hook
2. **ab6b3671** (2025-11-18 17:25) - Add centralized sync script + redesign tracking doc
3. **[CURRENT]** (2025-11-18 17:30) - Add quick reference guide

### Next Commits (Planned)
1. [THIS COMMIT] - Add `scripts/sync_orchestration_files.sh` + redesign tracking
2. Reduce hook scope (pre-commit) - Remove distribution logic
3. Reduce hook scope (post-commit) - Remove distribution logic
4. Reduce hook scope (post-merge) - Remove distribution logic
5. Reduce hook scope (post-checkout) - Remove distribution logic
6. Add integration tests for sync script
7. Update hooks documentation
8. Integrate sync into launch.py

---

## Branch Strategy

### Branches Affected
- `orchestration-tools` - Main orchestration branch (will be updated)
- `orchestration-tools-*` - Variant branches (will use new sync)
- `taskmaster` - Isolated (sync script will skip)
- Other feature branches - Unaffected

### Implementation Branch
- Consider creating `orchestration-tools-redesign` for safe testing
- Merge back to `orchestration-tools` after validation
- Deploy to main and scientific

---

## Risk Assessment

### Low Risk
- Adding sync script (additive, not breaking)
- Improving documentation
- Adding tests

### Medium Risk
- Reducing hook scope (need thorough testing)
- Changing sync logic
- File distribution changes (must verify integrity)

### Mitigation
- Thorough testing before merge
- Dry-run mode for verification
- Rollback capability
- Parallel testing (new script + old hooks)

---

## Success Criteria

- [ ] Sync script successfully distributes all files
- [ ] Hooks reduced to <60 lines each
- [ ] All tests passing (unit + integration + hook)
- [ ] Documentation clear and complete
- [ ] No regression in branch safety
- [ ] Easier to maintain and debug
- [ ] User can understand workflow in <5 minutes

---

## Related Documentation

- `ORCHESTRATION_DOCS_INDEX.md` - Current orchestration docs
- `.taskmaster/AGENTS.md` - Agent integration guide
- `TASKMASTER_BRANCH_CONVENTIONS.md` - Taskmaster branch rules
- `scripts/hooks/` - Current hook implementations
- `setup/` - Files being distributed

---

## Questions & Decisions

1. **Should sync script be idempotent?**
   - Yes - Safe to run multiple times
   - Enables CI/CD integration

2. **Handle file conflicts (modified locally)?**
   - Default: Skip modified files (preserve local changes)
   - Option: `--force` to overwrite
   - Option: `--merge` to merge strategically

3. **Include in launch.py?**
   - Yes - Add `launch.py sync` command
   - Makes it discoverable to users

4. **CI/CD integration timing?**
   - Run after checkout, before build
   - Or run as part of environment setup
   - Decision: After checkout, before tests

---

## Notes & Ideas

- Consider using git attributes for file distribution patterns
- Could use `.sync_manifest` to define distribution scope
- Explore making hooks entirely optional (advanced users)
- Document manual sync procedure for edge cases

---

## Implementation Log

### Phase 2 Completion (2025-11-18 17:25)

#### Created: `scripts/sync_orchestration_files.sh`

**Features Implemented**:
- ✓ Modular design with focused functions
- ✓ Branch detection (orchestration-tools*, taskmaster* handling)
- ✓ Dry-run mode for safe testing
- ✓ Verify mode for integrity checking
- ✓ Python syntax validation
- ✓ Colored output with logging
- ✓ Built-in help system
- ✓ Support for selective sync (--setup-only, --hooks-only, --config-only)
- ✓ Comprehensive error handling

**Usage Examples Tested**:
```bash
# Show help
./scripts/sync_orchestration_files.sh --help
✓ Works

# Dry-run to preview
./scripts/sync_orchestration_files.sh --dry-run
✓ Shows 27 files would be synced
✓ No changes made

# Verify integrity
./scripts/sync_orchestration_files.sh --verify
✓ Validates all critical files present
✓ Checks Python syntax on all files
✓ All checks pass
```

**Files Synced**:
- 10 setup/ files
- 6 git hooks
- 4 config files
- 1 root wrapper

**Next**: Phase 3 - Reduce hook scope

---

**Next Step**: Reduce hook scope and simplify from 150+ lines to <60 lines each
