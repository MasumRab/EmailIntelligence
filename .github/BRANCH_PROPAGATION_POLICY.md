# Branch Propagation & Merge Policy

## Overview

This document defines strict propagation rules for branch relationships in the EmailIntelligence project. These rules prevent context contamination and ensure proper separation of concerns between orchestration infrastructure and application code.

---

## Branch Roles & File Ownership

### 1. **main** (Public Distribution)
**Purpose:** Production-ready application code

**OWNS (exclusive):**
- Application source code: `src/`, `backend/`, `client/`
- Application plugins: `plugins/`
- Configuration files: `tsconfig.json`, `package.json`, `pyproject.toml`, etc.
- CI/CD workflows: `.github/workflows/`
- Production documentation: `README.md`, `docs/` (excluding orchestration docs)
- Distribution-approved orchestration docs (max 4 files):
  - `ORCHESTRATION_PROCESS_GUIDE.md`
  - `PHASE3_ROLLBACK_OPTIONS.md`
  - `docs/orchestration_summary.md`
  - `docs/env_management.md`

**BLOCKS (cannot merge):**
- Internal hooks: `.git/hooks/`
- Agent guidance: `AGENTS.md`, `CRUSH.md`, `GEMINI.md`, `IFLOW.md`, `LLXPRT.md`, `QWEN.md`, etc.
- Internal process files: `.taskmaster/`, `.claude/`, `.clinerules/`, etc.
- Testing/validation scripts: `scripts/validate-*.sh`, `scripts/extract-*.sh`
- Debug files: `MERGE_CONFLICT_RESOLUTION_REPORT.md`, `ORCHESTRATION_TEST_*.md`, etc.

**Merge Rules:**
```
✓ FROM: orchestration-tools (approved files only)
✓ FROM: feature branches (with validation)
✓ INTO: other feature branches
✗ NEVER FROM: orchestration-tools-changes (working branch)
✗ NEVER: Merge if pre-merge hook detects blocks
```

---

### 2. **orchestration-tools** (Tool Infrastructure)
**Purpose:** Hooks, scripts, internal infrastructure

**OWNS (exclusive):**
- Git hooks: `.git/hooks/`
- Validation scripts: `scripts/validate-*.sh`, `scripts/extract-*.sh`
- Setup infrastructure: `setup/`, `scripts/install-hooks.sh`, `scripts/enable-hooks.sh`
- Orchestration workflow files: `.orchestration-push-debounce`, `.orchestration-push-state`
- Internal documentation: `ORCHESTRATION_PROCESS_GUIDE.md`, `PHASE3_ROLLBACK_OPTIONS.md`
- Git notes metadata (Strategy 7)

**DOES NOT CONTAIN:**
- Application code: `src/`, `backend/`, `client/`, `plugins/` (deleted/not tracked)
- Distribution-only docs (they remain on main)
- Agent guidance docs (remain on main)

**Merge Rules:**
```
✓ FROM: orchestration-tools-changes (aggregated changes)
✓ FROM: main (for distribution doc updates only)
✓ INTO: orchestration-tools-changes (sync latest)
✗ NEVER FROM: main (for application code)
✗ NEVER: Accept application code contamination
✗ NEVER: Merge to main (breaks propagation)
✗ NEVER: Merge to scientific (breaks scientific branch)
```

---

### 3. **orchestration-tools-changes** (Working/Staging)
**Purpose:** Agent work area for orchestration changes

**Workflow:**
1. Branch from `orchestration-tools`
2. Make changes (multiple commits allowed)
3. Push to trigger aggregation (Strategy 5/7)
4. Create PR: `orchestration-tools-changes` → `orchestration-tools`
5. After merge: sync with `git merge origin/orchestration-tools`

**Merge Rules:**
```
✓ FROM: orchestration-tools (stay in sync)
✓ INTO: orchestration-tools (via PR only)
✗ NEVER: Direct merge to main
✗ NEVER: Merge to other branches
✗ NEVER: Used for application code changes
```

---

### 4. **scientific** (Alternative Distribution)
**Purpose:** Research/scientific computing variant

**Merge Rules:**
```
✓ FROM: main (for verified application code)
✓ FROM: feature branches (with scientific validation)
✓ FROM: orchestration-tools (for docs only)
✗ NEVER: Merge orchestration-tools completely
✗ NEVER: Propagate back to main (breaks main)
```

**Note:** orchestration-tools changes do NOT automatically propagate to scientific. Manual sync required for documentation updates only.

---

### 5. **Feature Branches** (feature/*, fix/*, docs/*)
**Purpose:** Development of specific features

**Merge Rules:**
```
✓ FROM: main (base)
✓ INTO: main (via PR with approval)
✓ INTO: scientific (if applicable)
✗ NEVER: FROM orchestration-tools (unless file list approved)
✗ NEVER: FROM orchestration-tools-changes
```

---

## Propagation Paths

### Forward Path (safe, one-way)
```
main
  ↓ (application changes)
feature branches → main
  ↓
PR merges automatically included
```

### Orchestration Tool Distribution
```
orchestration-tools-changes
  ↓ (PR aggregation: Strategy 5/7)
orchestration-tools
  ↓ (docs distribution only, manual approval)
main (4 approved files)
  ↓ (available for CI/CD, users)
```

### Scientific Branch
```
main
  ↓ (forked variant)
scientific
  ↓
orchestration-tools (doc updates only, manual)
```

---

## Merge Prevention Rules

### Pre-merge Hook Validation (`pre-merge-abort`)
**BLOCKS merge if any of these files detected:**

```bash
PROTECTED_FILES=(
    "backend"
    "src"
    "client"
    "plugins"
    "AGENTS.md"
    "CRUSH.md"
    "GEMINI.md"
    "IFLOW.md"
    "LLXPRT.md"
    "QWEN.md"
    ".taskmaster"
    ".claude"
    ".clinerules"
)
```

**When triggered:** Before `git merge --no-commit` completes

**Recovery:**
```bash
git merge --abort

# Use selective cherry-pick instead:
./scripts/extract-orchestration-changes.sh <branch> <commit>
```

### Pre-commit Hook Validation (`pre-commit`)
**WARNS (but allows) if:**
- Orchestration script changes on non-orchestration-tools branch
- Setup files modified on non-orchestration-tools branch
- Shared config files changed on non-orchestration-tools branch

**Action:** Developer must create PR to orchestration-tools for approval

---

## Validation Checklist

### Before Merging to main
```bash

# 1. Validate no orchestration files
./scripts/validate-orchestration-context.sh main

# 2. Check application code is present
git show main:src/ > /dev/null && echo "✓ Application code verified"

# 3. Verify protected files NOT present
git show main:.git/hooks/post-commit 2>/dev/null && echo "❌ FAIL: Hooks present" || echo "✓ No hooks"
```

### Before Merging to orchestration-tools
```bash

# 1. Validate ONLY orchestration files
./scripts/validate-orchestration-context.sh

# 2. Check no application code present
git show HEAD:src/ 2>/dev/null && echo "❌ FAIL: Application code found" || echo "✓ Clean"

# 3. Verify hooks are present
git show HEAD:.git/hooks/post-commit > /dev/null && echo "✓ Hooks verified"
```

### Before Merging to scientific
```bash

# 1. Validate scientific-specific requirements
./scripts/validate-orchestration-context.sh scientific

# 2. Check compatibility with scientific branch config
grep -q "SCIENTIFIC_MODE" scientific-branch-config.sh && echo "✓ Scientific config valid"
```

---

## Common Merge Scenarios

### Scenario 1: Feature Complete → main
```bash
git checkout feature/new-feature
git pull origin main  # Get latest

# Merge validation runs automatically
git push origin feature/new-feature

# Create PR in GitHub
```

**Validation:** pre-commit hook warns if orchestration files present

### Scenario 2: Orchestration Update → orchestration-tools
```bash
git checkout orchestration-tools-changes

# Make changes
git push origin orchestration-tools-changes

# Strategy 5: Post-commit hook creates aggregated PR

# After PR merges:
git fetch origin
git checkout orchestration-tools-changes
git merge origin/orchestration-tools
```

**Validation:** pre-merge-abort blocks if app code detected

### Scenario 3: Distribute Doc to main
```bash
git checkout main
git pull origin main

# Cherry-pick approved doc from orchestration-tools
git cherry-pick <commit> -- ORCHESTRATION_PROCESS_GUIDE.md

# Verify only docs changed
git diff --name-only HEAD~1 | grep -E "\.md$"

git commit --amend -m "chore: update orchestration docs"
git push origin main
```

**Validation:** pre-commit hook warns, manual approval required

### Scenario 4: BLOCKED - Cannot Merge
```bash
git checkout main
git merge orchestration-tools

# ❌ BLOCKED: pre-merge-abort detects .git/hooks/

# Recovery:
git merge --abort
./scripts/extract-orchestration-changes.sh orchestration-tools <commit>

# Manual cherry-pick approved files only
```

---

## Emergency Procedures

### Detect Propagation Violation
```bash

# Check if hooks are on main (BAD)
git show main:.git/hooks/post-commit > /dev/null 2>&1
if [[ $? -eq 0 ]]; then
    echo "❌ CONTAMINATION: Hooks found on main branch"

    # See: PHASE3_ROLLBACK_OPTIONS.md
fi

# Check if app code on orchestration-tools (BAD)
git show orchestration-tools:src/ > /dev/null 2>&1
if [[ $? -eq 0 ]]; then
    echo "❌ CONTAMINATION: App code found on orchestration-tools"

    # See: PHASE3_ROLLBACK_OPTIONS.md
fi
```

### Rollback Contaminated Branch
```bash

# Option 1: Reset to last known good state
git checkout <branch>
git log --oneline | grep -E "correct message"  # Find last good commit
git reset --hard <good-commit-sha>
git push origin <branch> --force-with-lease

# Option 2: Revert contamination commit
git revert <contamination-commit-sha>
git push origin <branch>
```

---

## Monitoring & Auditing

### Daily Checks
```bash

# 1. Verify branch integrity
./scripts/validate-orchestration-context.sh main
./scripts/validate-orchestration-context.sh orchestration-tools

# 2. Check for pending propagation
git log main..orchestration-tools-changes --oneline

# 3. Monitor merge queue
gh pr list --state open | grep -E "orchestration|main"
```

### Audit Log
```bash

# List all merges to main
git log main --oneline --grep="Merge" | head -20

# Check for suspicious commits
git log main --oneline --author="<suspicious-user>" | head -10

# Verify no hooks accidentally added to main
git log main --all --oneline -- ".git/hooks" | wc -l

# Output should be: 0
```

---

## Policy Enforcement

### Automated Enforcement
- **Pre-merge hook:** Blocks merge if protected files detected
- **Pre-commit hook:** Warns if files modified on wrong branch
- **CI/CD workflow:** Validates on every PR

### Manual Enforcement
- **Code review:** Inspect file changes before approval
- **Cherry-pick:** Use selective commit picking for cross-branch updates
- **Documentation:** Update BRANCH_PROPAGATION_POLICY.md when rules change

### Escalation Path
1. **Prevention:** Pre-merge hook blocks invalid merge
2. **Detection:** CI/CD validation fails
3. **Recovery:** See PHASE3_ROLLBACK_OPTIONS.md
4. **Review:** Update this policy if edge case discovered

---

## File Status by Branch

| File/Path | main | orchestration-tools | orchestration-tools-changes | scientific |
|-----------|------|-------------------|---------------------------|-----------|
| src/, backend/, client/ | ✓ | ✗ | ✗ | ✓ |
| plugins/ | ✓ | ✗ | ✗ | ✓ |
| .git/hooks/ | ✗ | ✓ | ✓ | ✗ |
| scripts/validate-*.sh | ✗ | ✓ | ✓ | ✗ |
| AGENTS.md, CRUSH.md | ✗ | ✗ | ✗ | ✗ |
| ORCHESTRATION_PROCESS_GUIDE.md | ✓ | ✓ | ✓ | ✗ |
| docs/orchestration_*.md | ✓ | ✓ | ✓ | ✗ |
| setup/ | ✗ | ✓ | ✓ | ✗ |
| .taskmaster/ | ✗ | ✗ | ✗ | ✗ |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-11-10 | Initial propagation policy |

---

## Questions & Support

For violations or unclear rules, see:
- PHASE3_ROLLBACK_OPTIONS.md (recovery procedures)
- ORCHESTRATION_PROCESS_GUIDE.md (orchestration workflow)
- scripts/validate-orchestration-context.sh (validation tool)

**Last Updated:** 2025-11-10
