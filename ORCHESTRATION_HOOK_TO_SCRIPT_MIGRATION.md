# Orchestration Hook Management & Hook-to-Script Migration Planning

**Document Status**: Planning & Reference  
**Last Updated**: Nov 20, 2025  
**Current Session**: Cleanup Complete, Ready for Boundary Updates

---

## Executive Summary

This document consolidates the orchestration hook system architecture and explores potential hook-to-script migration strategies. The current hook system is **working well** with remote-first installation ensuring consistency. Any migration should preserve this reliability.

**Current Status**:
- ✅ Cleanup complete (7 analysis docs deleted, 3 utility scripts committed)
- ✅ Git status clean
- ✅ All hook mechanics documented
- ⏳ Ready for boundary clarification and optional migration planning

---

## Section 1: Current Hook Architecture

### 1.1 Hook Locations & Purposes

| Hook | Location | Purpose | Trigger |
|------|----------|---------|---------|
| **pre-commit** | `scripts/hooks/pre-commit` | Prevent changes to orchestration-managed files on non-orchestration-tools branches | Before commit |
| **post-checkout** | `scripts/hooks/post-checkout` | Sync essential files, reinstall hooks, cleanup worktrees | After branch switch |
| **post-commit** | `scripts/hooks/post-commit` | Trigger worktree sync on orchestration-tools | After commit |
| **post-merge** | `scripts/hooks/post-merge` | Sync files, update hooks, resolve conflicts | After merge |
| **post-push** | `scripts/hooks/post-push` | Detect orchestration changes, create/update PRs | After push |

### 1.2 Installation System: Remote-First Approach

**Key File**: `scripts/install-hooks.sh`

**Mechanism**:
```bash
# Fetch latest hooks from remote
git fetch origin orchestration-tools

# Install hooks directly from remote into .git/hooks/
# Uses remote-first to prevent version mismatches
```

**Benefits**:
- Prevents stale hook issues from local/unpushed versions
- Ensures all environments use identical hook versions
- Single source of truth on `origin/orchestration-tools`
- Automatic via post-checkout hook

**Usage**:
```bash
# Manual installation
scripts/install-hooks.sh --force --verbose

# Automatic on branch switch (post-checkout)
git checkout main  # Hooks auto-install
```

### 1.3 File Synchronization Pattern

**Orchestration-tools branch ONLY** (not synced to other branches):
- `scripts/` - Raw orchestration tooling
- `scripts/hooks/` - Hook source files
- `scripts/lib/` - Utility libraries
- `scripts/cleanup_orchestration.sh`

**Synced to ALL branches** (essentials):
- `setup/` - Launch scripts and environment setup
- `launch.py` - Root wrapper script
- `pyproject.toml`, `requirements*.txt` - Dependencies
- `.flake8`, `.pylintrc` - Linting configuration
- `.gitignore`, `.gitattributes` - Git configuration
- Documentation in `docs/orchestration_*.md`
- **Installed hooks in `.git/hooks/`** (via install-hooks.sh)

---

## Section 2: Hook System Behavior by Branch

### 2.1 On `orchestration-tools` Branch

**pre-commit hook**:
- ✅ Allows all changes (this is the source of truth)
- Developers can safely modify hooks here

**post-checkout hook**:
- Smart bypass for orchestration-tools
- Skips syncs when switching TO orchestration-tools
- Allows pure tool development without interference

**post-commit hook**:
- Offers to run `sync_setup_worktrees.sh`
- Helps distribute changes to worktrees

### 2.2 On Other Branches (main, scientific, feature/*)

**pre-commit hook**:
- ⚠️ Warns if you modify orchestration-managed files
- Suggests creating a PR to orchestration-tools
- Allows project-specific changes

**post-checkout hook**:
- Auto-syncs essential files from orchestration-tools
- Auto-installs/updates hooks via `install-hooks.sh`
- Cleans up orphaned worktrees

**post-merge hook**:
- Syncs `setup/` directory
- Reinstalls hooks
- Updates shared configuration

**post-push hook**:
- Detects if orchestration-managed files changed on non-orchestration-tools branch
- Creates draft PR to orchestration-tools automatically

---

## Section 3: Hook-to-Script Migration Feasibility

### 3.1 Current Strengths (Why Hooks Work Well)

✅ **Automatic Execution**
- Users don't need to remember to run sync commands
- Prevents accidents through enforcement
- Transparent to developers

✅ **Consistency Guaranteed**
- All branches always have latest hooks
- Remote-first installation prevents version skew
- No manual sync steps required

✅ **Low Friction**
- No additional commands to learn
- Works seamlessly with normal git workflow
- Handles edge cases automatically

### 3.2 Migration Scenarios & Impacts

#### Scenario A: Full Hook-to-Script Migration ⚠️
**Replace all hooks with standalone scripts**

**Impacts**:
- ❌ Breaks automation (users must remember to run scripts)
- ❌ Increases friction in workflow
- ❌ Potential for stale files if scripts forgotten
- ✅ Makes hook logic more visible and testable
- ✅ Easier to debug step-by-step

**Not Recommended**: Loses the main benefit of hooks.

#### Scenario B: Hybrid Approach (Recommended) ✅
**Keep hooks + provide optional scripts**

**Structure**:
```bash
# Core automation (hooks remain)
.git/hooks/pre-commit          # Installed from scripts/hooks/pre-commit
.git/hooks/post-checkout       # Installed from scripts/hooks/post-checkout
.git/hooks/post-merge          # Installed from scripts/hooks/post-merge
.git/hooks/post-push           # Installed from scripts/hooks/post-push

# Optional standalone scripts (new)
scripts/validate-commit.sh     # Can be called manually
scripts/sync-essential-files.sh    # Can be called manually
scripts/detect-orchestration-changes.sh  # For CI/CD use
```

**Benefits**:
- ✅ Hooks remain automatic and reliable
- ✅ Scripts available for CI/CD systems
- ✅ Scripts can be tested independently
- ✅ Users can run scripts manually if needed
- ✅ Debugging possible with script versions

#### Scenario C: Git Hooks Disabled Workflow ℹ️
**Current system already supports this**

```bash
# Disable hooks for independent work
./scripts/disable-hooks.sh

# Do isolated work on setup files
cd setup/ && make changes

# Re-enable hooks when done
./scripts/enable-hooks.sh
```

This satisfies the "explicit script use" requirement while keeping hooks default.

### 3.3 Migration Roadmap (If Pursued)

**Phase 1: Document** ✅
- [x] Document hook purposes
- [x] Document file sync rules
- [x] Document install-hooks.sh mechanism
- [x] Document orchestration_branch_scope.md

**Phase 2: Create Wrapper Scripts** (Optional)
```bash
# Extract hook logic into testable scripts
scripts/run-pre-commit-validation.sh
scripts/sync-and-install-hooks.sh
scripts/detect-and-create-prs.sh
```

**Phase 3: Update CI/CD** (If needed)
- Use wrapper scripts in GitHub Actions
- Ensure CI runs orchestration checks
- Validate across multiple branches

**Phase 4: Keep Hooks as Default** (Recommended)
- Hooks remain primary automation
- Scripts serve CI/CD and manual use
- No breaking changes to workflow

---

## Section 4: Understanding "Update Boundaries"

Based on the codebase structure, "update boundaries" likely means clarifying:

### 4.1 Branch Boundaries

**orchestration-tools**:
- ✅ KEEP: Scripts, hooks, setup/, configuration
- ❌ REMOVE: src/, modules/, tests/, data/, backend/, client/

**main/scientific/feature branches**:
- ✅ KEEP: Application code, features, tests
- ✅ GET (via sync): setup/, launch.py, configurations, installed hooks
- ❌ DON'T GET: Raw orchestration scripts

**Boundary Rule**: Orchestration branch is **development environment tools only**.

### 4.2 Worktree Boundaries

**Main worktree** (current directory):
- Application code
- Feature branches
- Ready for testing and deployment

**Setup worktree** (optional):
- Only `setup/` and `launch.py`
- Isolated environment testing
- No app code interference

**Task worktrees** (git worktree add):
- Task-specific feature branches
- Independent from main worktree
- Clean isolation

### 4.3 Hook Execution Boundaries

**Always Execute**:
- pre-commit (validation)
- post-checkout (sync)
- post-merge (sync)

**Conditional Execute**:
- post-checkout skips on orchestration-tools branch
- pre-commit allows changes on orchestration-tools branch
- post-push only acts on orchestration changes

**Manual/CI Execute**:
- install-hooks.sh (manual or post-checkout)
- cleanup_orchestration.sh (manual cleanup)
- sync_setup_worktrees.sh (manual distribution)

### 4.4 File Synchronization Boundaries

**Matrix of What Syncs Where**:

| File/Directory | orchestration-tools | main | scientific | feature/* |
|---|:---:|:---:|:---:|:---:|
| scripts/ | ✅ | ❌ | ❌ | ❌ |
| setup/ | ✅ | ✅ | ✅ | ✅ |
| launch.py | ✅ | ✅ | ✅ | ✅ |
| .flake8, .pylintrc | ✅ | ✅ | ✅ | ✅ |
| src/, modules/ | ❌ | ✅ | ✅ | ✅ |
| tests/ | ❌ | ✅ | ✅ | ✅ |
| .git/hooks/ | (source) | (installed) | (installed) | (installed) |

---

## Section 5: Recommended Actions

### Immediate (Next Session)

- [ ] Verify branch boundaries are correctly documented
- [ ] Confirm no application code exists in orchestration-tools
- [ ] Test post-checkout hook sync on each branch

### Short Term (This Sprint)

- [ ] Create optional wrapper scripts for CI/CD:
  ```bash
  scripts/run-pre-commit-validation.sh
  scripts/sync-essential-files.sh
  scripts/handle-orchestration-push.sh
  ```
- [ ] Add these scripts to GitHub Actions workflows
- [ ] Document when to use hooks vs. scripts

### Medium Term (This Quarter)

- [ ] If hybrid approach adopted:
  - Extract hook logic to functions
  - Source functions from both hooks and scripts
  - Add tests for validation logic

- [ ] If CI/CD needs refinement:
  - Use scripts in workflows
  - Add branch-specific checks
  - Improve error messages

### Long Term (As Needed)

- [ ] Monitor for hook issues
- [ ] Consider performance optimization
- [ ] Evaluate against other projects' approaches

---

## Section 6: Troubleshooting Guide

### Hooks Not Running

```bash
# Check if installed
ls -la .git/hooks/

# Check if executable
chmod +x .git/hooks/*

# Force reinstall
scripts/install-hooks.sh --force --verbose
```

### Stale Files After Switch

```bash
# This shouldn't happen, but if it does:
git checkout orchestration-tools -- setup/
scripts/install-hooks.sh --force
```

### Need to Skip Hooks Temporarily

```bash
# Disable hooks for independent work
./scripts/disable-hooks.sh

# Do isolated work
# ... make changes ...

# Re-enable hooks
./scripts/enable-hooks.sh
```

---

## Section 7: Key Principles

1. **orchestration-tools is source of truth** for environment tools
2. **Remote-first installation** prevents version mismatches
3. **Hooks are transparent automation** for consistency
4. **Branch separation** keeps concerns clear
5. **File synchronization** is automatic via hooks
6. **Scripts can be optional** for explicit control
7. **Boundaries are fixed** - don't blur orchestration with application code

---

## Appendix A: File Organization

```
orchestration-tools branch:
├── scripts/
│   ├── install-hooks.sh          ← Main installation script
│   ├── cleanup_orchestration.sh   ← Cleanup utility
│   ├── sync_setup_worktrees.sh    ← Worktree sync
│   ├── hooks/                      ← Hook source files
│   │   ├── pre-commit
│   │   ├── post-checkout
│   │   ├── post-commit
│   │   ├── post-merge
│   │   └── post-push
│   └── lib/                        ← Shared utilities
│       ├── git-utils.sh
│       └── path-utils.sh
├── setup/
│   ├── launch.py                  ← Synced to all branches
│   ├── requirements.txt            ← Synced to all branches
│   └── ...
├── docs/
│   ├── orchestration_summary.md           ← Synced to all
│   ├── orchestration_branch_scope.md      ← Synced to all
│   ├── orchestration_hook_management.md   ← Synced to all
│   └── ...
└── Configuration files             ← Synced to all branches
    ├── .flake8
    ├── .pylintrc
    ├── pyproject.toml
    └── .gitignore
```

---

## Appendix B: Glossary

- **orchestration-tools**: Branch containing development environment tools (not application code)
- **Remote-first installation**: Fetching hooks from `origin/orchestration-tools` instead of local branch
- **File synchronization**: Automatic copying of essential files to all branches via hooks
- **Hybrid approach**: Keeping hooks + providing optional standalone scripts
- **Boundary**: Clear separation between orchestration tools and application code
- **Worktree**: Isolated git working directory using `git worktree`

---

**Document Purpose**: Reference for understanding the orchestration hook system and planning any future migrations to script-based approaches.

**Recommendation**: Keep the current hook system - it works well. If additional transparency is needed, add optional wrapper scripts rather than removing hooks.
