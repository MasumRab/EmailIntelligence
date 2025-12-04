# Branch Propagation Setup Checklist

## Status: ✅ COMPLETE

This document confirms that branch propagation rules and enforcement mechanisms have been successfully implemented.

---

## Implemented Components

### 1. Policy Documentation
- [x] `.github/BRANCH_PROPAGATION_POLICY.md` - Comprehensive propagation rules
  - Branch roles and file ownership clearly defined
  - Propagation paths documented
  - Merge prevention rules specified
  - Common scenarios and emergency procedures included

### 2. Git Hooks (Updated)

#### Pre-commit Hook (`.git/hooks/pre-commit`)
- [x] Validates file modifications against branch ownership rules
- [x] Warns on cross-branch modifications
- [x] Blocks application code commits to orchestration-tools
- [x] Blocks infrastructure files commits to main
- [x] Organized file rules by category:
  - ORCHESTRATION_ONLY (setup/, hooks, validation scripts)
  - SHARED_CONFIG (config files)
  - DISTRIBUTION_DOCS (approved orchestration docs)
  - APPLICATION_CODE (src/, backend/, etc.)

**Triggers on:** Every `git commit`
**Exit code:** 
- 0: Success (warnings allowed)
- 1: Blocked commit detected

#### Pre-merge Hook (`.git/hooks/pre-merge-abort`)
- [x] Branch-aware validation
- [x] Prevents merge to orchestration-tools if app code detected
- [x] Prevents merge to main if infrastructure files detected
- [x] Prevents merge to scientific if hooks detected
- [x] Contextual error messages with recovery steps
- [x] References BRANCH_PROPAGATION_POLICY.md

**Triggers on:** `git merge --no-commit <branch>`
**Exit code:**
- 0: Safe to merge
- 1: Propagation violation detected

### 3. Validation Scripts

#### Branch Propagation Validator (`scripts/validate-branch-propagation.sh`)
- [x] Validates all branches against propagation rules
- [x] Checks for blocked files on each branch
- [x] Verifies required files are present
- [x] Validates branch relationships
- [x] Checks file sync consistency across branches
- [x] Provides detailed reporting and suggestions
- [x] Color-coded output for easy reading
- [x] Options:
  - `--details`: Show file counts
  - `--fix`: Attempt repairs (experimental)
  - `--branch <name>`: Check specific branch only

**Usage:**
```bash
./scripts/validate-branch-propagation.sh              # Check all branches
./scripts/validate-branch-propagation.sh --branch main # Check main only
./scripts/validate-branch-propagation.sh --details    # Show detailed info
```

### 4. Hook Installation
- [x] Hooks placed in `.git/hooks/` with executable permissions
- [x] Auto-installed on checkout via post-checkout hook
- [x] Backup of original hooks available (if needed)

---

## Validation Results

### Current State Check
```bash

# Verify hooks are installed
ls -la .git/hooks/ | grep -E "pre-commit|pre-merge"

# Expected: Both files present and executable

# Verify policy documents
ls -la .github/BRANCH_PROPAGATION_POLICY.md

# Expected: File exists

# Test validation script
./scripts/validate-branch-propagation.sh

# Expected: All branches pass or warnings only (no violations)
```

### File Ownership Summary

| Category | Branches | Files |
|----------|----------|-------|
| **Application Code** | main, scientific, feature/* | src/, backend/, client/, plugins/ |
| **Orchestration Infrastructure** | orchestration-tools, orchestration-tools-changes | .git/hooks/, setup/, scripts/validate-*, scripts/extract-* |
| **Shared Config** | main, orchestration-tools | .flake8, .pylintrc, tsconfig.json, etc. |
| **Distribution Docs** | main, orchestration-tools | ORCHESTRATION_PROCESS_GUIDE.md, PHASE3_ROLLBACK_OPTIONS.md |
| **Agent Guidance** | NONE (removed) | AGENTS.md, CRUSH.md, GEMINI.md, etc. |

---

## Enforcement Mechanisms

### Automatic Prevention
```
git commit  →  pre-commit hook validates  →  Warns/Blocks if violation
      ↓
git merge   →  pre-merge-abort validates  →  Blocks if violation
```

### Validation
```
Daily/Manual  →  validate-branch-propagation.sh  →  Report status/violations
```

### Recovery
```
Violation Detected  →  Check PHASE3_ROLLBACK_OPTIONS.md  →  Execute recovery step
```

---

## Branch Configuration

### main (Distribution)
```
✓ CONTAINS: Application code, tests, CI/CD, distribution docs
✗ CANNOT CONTAIN: Hooks, infrastructure, internal process docs
✓ MERGE FROM: feature branches, orchestration-tools (docs only)
✗ MERGE TO: orchestration-tools directly
```

### orchestration-tools (Infrastructure)
```
✓ CONTAINS: Hooks, setup scripts, validation tools
✗ CANNOT CONTAIN: Application code, agent guidance
✓ MERGE FROM: orchestration-tools-changes
✓ MERGE TO: none directly (distributes docs to main)
```

### orchestration-tools-changes (Staging)
```
✓ WORKFLOW: Branch from orchestration-tools
✓ WORK: Make changes, push (Strategy 5/7 aggregates)
✓ CREATE PR: orchestration-tools-changes → orchestration-tools
✗ DO NOT: Merge to main or other branches
```

### scientific (Variant Distribution)
```
✓ CONTAINS: Application code (from main fork)
✓ MERGE FROM: main (application changes)
✗ CANNOT CONTAIN: Hooks or full orchestration-tools
✓ MANUAL SYNC: Distribution docs from orchestration-tools only
```

---

## Testing & Verification

### Test Case 1: Prevent Application Code on orchestration-tools
```bash

# SHOULD BE BLOCKED:
git checkout orchestration-tools
echo "test" > src/test.ts
git add src/test.ts
git commit -m "test: add to orchestration-tools"  # ❌ BLOCKED

# Recovery:
git reset src/test.ts
git checkout -- src/test.ts
git checkout main  # Switch to correct branch
```

### Test Case 2: Prevent Hooks on main
```bash

# SHOULD BE BLOCKED:
git checkout main
cp .git/hooks/pre-commit test-hook.sh
git add test-hook.sh
git commit -m "test: add hook to main"  # ❌ BLOCKED

# Recovery:
git reset test-hook.sh
git checkout -- test-hook.sh
```

### Test Case 3: Prevent Merge with Violations
```bash

# SHOULD BE BLOCKED:
git checkout orchestration-tools
git merge --no-commit main  # If main has src/ files

# ❌ pre-merge-abort blocks merge
git merge --abort
```

### Test Case 4: Allow Valid Changes
```bash

# SHOULD SUCCEED:
git checkout orchestration-tools
echo "# New setup doc" > setup/new-doc.md
git add setup/new-doc.md
git commit -m "chore: add setup documentation"  # ✓ ALLOWED

git push origin orchestration-tools  # ✓ ALLOWED
```

---

## Documentation Files

### Primary Documentation
- `.github/BRANCH_PROPAGATION_POLICY.md` - Policy and rules
- `.github/PROPAGATION_SETUP_CHECKLIST.md` - This file, status and testing
- `ORCHESTRATION_PROCESS_GUIDE.md` - Orchestration workflow and strategies
- `PHASE3_ROLLBACK_OPTIONS.md` - Emergency recovery procedures

### Validation Tools
- `scripts/validate-branch-propagation.sh` - Branch validation utility
- `scripts/validate-orchestration-context.sh` - Context contamination check

### Git Hooks
- `.git/hooks/pre-commit` - File modification validation
- `.git/hooks/pre-merge-abort` - Merge validation
- `.git/hooks/post-checkout` - Auto-install hooks on branch switch

---

## Monitoring & Maintenance

### Daily Checks
```bash

# Verify no violations exist
./scripts/validate-branch-propagation.sh

# Check current branch status
git rev-parse --abbrev-ref HEAD
git status
```

### Weekly Audits
```bash

# Full branch validation with details
./scripts/validate-branch-propagation.sh --details

# Check for any contamination
./scripts/validate-orchestration-context.sh main
./scripts/validate-orchestration-context.sh orchestration-tools
```

### When Adding New Files
1. Update `.github/BRANCH_PROPAGATION_POLICY.md` file ownership table
2. Update `.git/hooks/pre-commit` if new file category
3. Update `.git/hooks/pre-merge-abort` if new protected pattern
4. Test with: `./scripts/validate-branch-propagation.sh --branch <target>`

---

## Troubleshooting

### Pre-commit Hook Warnings
**Problem:** Pre-commit hook warns about file modifications
**Reason:** File is being modified on non-owning branch
**Solution:** Either:
- Switch to correct branch and make changes there
- OR create PR to owning branch for approval

### Pre-merge Hook Blocks Merge
**Problem:** Cannot merge, pre-merge-abort blocks
**Reason:** Incoming changes violate propagation rules
**Solution:**
```bash
git merge --abort
./scripts/extract-orchestration-changes.sh <source-branch> <commit>

# Cherry-pick only approved files instead
```

### Files Missing from Branch
**Problem:** Required files not found on branch
**Reason:** Branch may be out of sync or files deleted
**Solution:**
```bash

# Sync branch with upstream
git fetch origin
git merge origin/<branch>

# Or manually sync specific file
git show origin/<other-branch>:<file> > <file>
git add <file>
git commit -m "sync: restore <file>"
```

### Validation Script Fails
**Problem:** `validate-branch-propagation.sh` reports violations
**Reason:** Branch contains blocked files or missing required files
**Solution:**
```bash

# See detailed violations
./scripts/validate-branch-propagation.sh --details --branch <branch>

# Identify problematic commits
git log --oneline <branch> -- <blocked-file>

# Revert or reset
git revert <commit-sha>

# OR
git reset --hard <good-commit-sha>
git push origin <branch>
```

---

## Version History

| Version | Date | Status | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-11-10 | ✅ COMPLETE | Initial implementation |

---

## Sign-off Checklist

### Setup Complete
- [x] Policy documentation created
- [x] Pre-commit hook updated
- [x] Pre-merge-abort hook updated
- [x] Validation script created
- [x] All hooks are executable
- [x] Documentation references complete

### Testing Complete
- [x] Hook installation verified
- [x] Policy enforcement confirmed
- [x] Edge cases documented
- [x] Recovery procedures validated

### Distribution Ready
- [x] Changes ready to push to orchestration-tools
- [x] Distribution documents identified
- [x] Sync process documented
- [x] All branches can be validated

---

## Next Steps

### For Team
1. **Review Policy:** Read `.github/BRANCH_PROPAGATION_POLICY.md`
2. **Test Validation:** Run `./scripts/validate-branch-propagation.sh`
3. **Enable Hooks:** Hooks auto-install on checkout
4. **Report Issues:** If violations detected, follow troubleshooting guide

### For Maintenance
1. **Monitor Daily:** Run validation checks regularly
2. **Update Policy:** Keep `.github/BRANCH_PROPAGATION_POLICY.md` current
3. **Add New Files:** Update hooks when new file categories added
4. **Audit Quarterly:** Full branch audit to ensure compliance

### For Distribution
1. **Push to orchestration-tools:** All hooks and scripts
2. **Push to main:** Policy documents and validation script only
3. **Sync scientific:** Optional - only if scientific variant used
4. **Document Changes:** Update PR with enforcement details

---

**Status:** ✅ Ready for deployment

**Last Updated:** 2025-11-10
**Maintained By:** Build & Release Team
