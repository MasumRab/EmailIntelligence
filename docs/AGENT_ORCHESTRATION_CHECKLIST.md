# Agent Checklist: Orchestration-Aware Modifications

**For**: AI agents, CI/CD systems, automated tools  
**Purpose**: Quick reference to avoid orchestration-related mistakes

---

## 🔴 CRITICAL CHECKS (Do these FIRST)

### Before modifying ANY file

```bash
# 1. What files will I modify?
git diff --name-only [optional: compare with orchestration-tools]

# 2. Are any of these MANAGED FILES?
MANAGED_FILES=(
  "setup/*"
  "deployment/*"
  "scripts/hooks/*"
  ".flake8"
  ".pylintrc"
  "setup.cfg"
  "pyproject.toml"
  "pytest.ini"
  "tsconfig.json"
  "package.json"
  "vite.config.ts"
  "tailwind.config.ts"
  "drizzle.config.ts"
  "components.json"
)

# 3. If YES to managed files, check BRANCH
git branch
# Result MUST be: orchestration-tools
# If not: ❌ STOP - Use decision tree in ORCHESTRATION_SYSTEM.md
```

---

## ✅ Safe Modification Pattern

```bash
# Step-by-step for ANY managed file change

# 1. VERIFY branch
$ git branch
* orchestration-tools  ← If this, proceed. Otherwise STOP.

# 2. FETCH latest
$ git fetch origin
$ git pull origin orchestration-tools

# 3. CHECK what you'll modify
$ git diff orchestration-tools -- [your files]
# Review each change carefully

# 4. MAKE changes
$ nano [files]

# 5. VALIDATE
$ git status  # Should show only expected files
$ git diff --stat  # Should show only setup/deployment/config

# 6. TEST locally
[Run relevant tests for your changes]

# 7. COMMIT with clear message
$ git commit -m "feat|fix|docs: [clear description]"

# 8. PUSH (this triggers sync to all branches)
$ git push origin orchestration-tools

# 9. VERIFY on remote
# Check GitHub: orchestration-tools branch
# Latest commit should be yours
```

---

## 🚨 Before Each Git Operation

### Before `git commit`

```
Checklist:
  [ ] `git branch` shows orchestration-tools
  [ ] `git diff --stat` shows only MANAGED_FILES
  [ ] No application code (src/, client/, etc.)
  [ ] No .env files
  [ ] No local-only files (.taskmaster/, temp files)
  [ ] Commit message is clear and descriptive
```

### Before `git push`

```
Checklist:
  [ ] `git log -1` shows your commit message
  [ ] `git diff origin/orchestration-tools..HEAD` shows expected changes
  [ ] Only pushing to orchestration-tools (not main, scientific, etc.)
  [ ] Changes are tested and reviewed
```

### Before `git checkout [branch]`

```
Checklist:
  [ ] All changes committed (no uncommitted files)
  [ ] Hooks are ENABLED (or intentionally disabled with reason)
  [ ] If hooks disabled: will re-enable after this work
```

### Before `git merge orchestration-tools`

```
Checklist:
  [ ] You're on a non-orchestration-tools branch (main, feature/*, etc.)
  [ ] Understand: You're bringing latest setup/deployment files
  [ ] After merge: post-merge hook will re-sync for consistency
  [ ] No conflicts expected (orchestration-tools is authoritative)
```

---

## 📊 Decision Matrix

| Situation | Check | Action |
|-----------|-------|--------|
| Want to modify setup/ | `git branch` | If orchestration-tools: ✅ proceed. Else: switch branch or use reverse-sync |
| Want to modify src/ | Any branch | ✅ OK - app code doesn't sync |
| Want to disable hooks | Any branch | Run `./scripts/disable-hooks.sh` then RE-ENABLE after work |
| Modified setup on main | Emergency | Use `git reflog` to recover, re-apply on orchestration-tools |
| Synced file disappeared | Expected | If you modified on non-source branch, post-merge overwrote it |
| Hooks not syncing | Debug | Check: `ls -la .git/hooks.disabled/` - if exists, run enable-hooks.sh |

---

## 🔒 Safety Rules (Non-negotiable)

### RULE 1: Never force-push to orchestration-tools

```bash
❌ FORBIDDEN:
  git push --force origin orchestration-tools

WHY: Breaks sync for all other branches
```

### RULE 2: Never commit app code to orchestration-tools

```bash
❌ DON'T:
  git checkout orchestration-tools
  [edit src/ files]
  git commit -m "feat: ..."
  git push  ← Breaks orchestration-tools purpose

✅ DO:
  git checkout -b feature/app-feature
  [edit src/ files]
  git commit && git push
```

### RULE 3: Never modify managed files on other branches

```bash
❌ DON'T:
  git checkout main
  nano setup/setup_environment_system.sh
  git commit  ← Will be overwritten on next sync

✅ DO:
  git checkout orchestration-tools
  nano setup/setup_environment_system.sh
  git commit && git push
```

### RULE 4: Never leave hooks disabled

```bash
❌ DON'T:
  ./scripts/disable-hooks.sh
  [make changes]
  git commit
  # Forget to enable hooks

✅ DO:
  ./scripts/disable-hooks.sh
  [make changes]
  git commit
  ./scripts/enable-hooks.sh  ← Always re-enable
```

---

## 🛠️ Emergency Recovery

### "I accidentally modified setup/ on main"

```bash
# Don't panic, it will be overwritten
# But let's recover your changes anyway

# 1. Save your change
$ git diff main > /tmp/my_change.patch

# 2. Find it in reflog (optional, for documentation)
$ git reflog
# Identifies the commit before sync happened

# 3. Switch to orchestration-tools and re-apply
$ git checkout orchestration-tools
$ git pull origin orchestration-tools

# 4. Apply your change
$ patch -p1 < /tmp/my_change.patch
$ git commit -m "fix: [description]"
$ git push origin orchestration-tools

# 5. Verify sync on main (next checkout/merge)
$ git checkout main
# post-checkout hook runs, syncs setup files
```

### "Hooks are disabled and I can't remember why"

```bash
# 1. Check status
$ ls -la .git/hooks.disabled/

# 2. If hooks truly disabled, re-enable
$ ./scripts/enable-hooks.sh

# 3. Verify
$ ls -la .git/hooks/
# Should see post-checkout, post-merge, etc.
```

### "I modified setup/ on orchestration-tools but forgot to push"

```bash
# 1. Check status
$ git status

# 2. If uncommitted changes
$ git commit -m "..."
$ git push origin orchestration-tools

# 3. Verify remote is updated
$ git log origin/orchestration-tools -1
# Should show your commit

# 4. Sync other branches
$ git checkout main
$ git pull origin orchestration-tools
# OR wait for next post-checkout hook
```

---

## 📋 File Type Reference

### Files that ALWAYS sync from orchestration-tools

```
setup/                 → All setup scripts
deployment/            → Deployment configs
scripts/hooks/         → Git hooks
.flake8                → Linting config
.pylintrc              → Pylint config
setup.cfg              → Setup config
pyproject.toml         → Python project config
pytest.ini             → Test config
tsconfig.json          → TypeScript config
package.json           → Node project config
vite.config.ts         → Build config
tailwind.config.ts     → Styling config
drizzle.config.ts      → DB config
components.json        → Component config
```

### Files that NEVER sync

```
src/                   → Application code
client/                → Frontend code
plugins/               → Plugins
tests/                 → Application tests
.env                   → Local environment variables
.taskmaster/           → Task Master database
docs/ (branch-specific) → Branch-specific docs
.github/workflows/     → Branch-specific workflows
README.md (branch-specific) → Branch-specific README
```

### Files that CONDITIONALLY sync

```
.gitignore             → Merges, may conflict
requirements.txt       → Managed, don't edit
uv.lock                → Locked deps, auto-generated
```

---

## 🔍 Pre-Commit Validation

Before committing to orchestration-tools, run:

```bash
# 1. Syntax check on shell scripts
bash -n setup/*.sh
bash -n scripts/hooks/*

# 2. Python syntax check
python -m py_compile setup/*.py
python -m pylint setup/ --errors-only

# 3. JSON validation
python -m json.tool pyproject.toml > /dev/null
python -m json.tool setup.cfg > /dev/null

# 4. Verify no app code
git diff HEAD -- src/ client/ plugins/
# Should show: nothing

# 5. Verify no local files
git diff HEAD -- .env .taskmaster/
# Should show: nothing
```

---

## 🚀 Recommended Workflow for Agents

```
1. START WITH SAFETY CHECK:
   ├─ git branch (must be orchestration-tools)
   ├─ git status (must be clean or show expected changes)
   ├─ git diff --stat (must be MANAGED_FILES only)
   └─ STOP if any check fails

2. MAKE CHANGES:
   ├─ Modify files
   ├─ Validate syntax
   ├─ Test locally
   └─ Review diff

3. COMMIT SAFELY:
   ├─ Write clear message
   ├─ Check: no unwanted files in git status
   ├─ Commit
   └─ Verify: git log -1

4. PUSH TO REMOTE:
   ├─ Push only to orchestration-tools
   ├─ Verify: git log origin/orchestration-tools -1
   └─ Document: This will sync to all branches

5. POST-PUSH:
   ├─ Update any related docs
   ├─ Link to this commit in task/PR
   ├─ Test sync on other branch: git checkout main && verify file
   └─ ✓ Done
```

---

## 🎯 Quick Reference

```
🟢 GREEN - Safe to do:
  ✅ Modify files on orchestration-tools
  ✅ Commit to orchestration-tools
  ✅ Push to orchestration-tools
  ✅ Modify app code on any branch
  ✅ Switch branches (triggers post-checkout)
  ✅ Merge orchestration-tools into other branches
  ✅ Pull origin/orchestration-tools

🟡 YELLOW - Requires caution:
  ⚠️ Disable hooks (always re-enable)
  ⚠️ Force-push to feature branches (not orchestration-tools)
  ⚠️ Merge main/scientific into orchestration-tools (if contains app changes)

🔴 RED - Never do:
  ❌ Force-push to orchestration-tools
  ❌ Commit app code to orchestration-tools
  ❌ Modify managed files on non-orchestration-tools branches
  ❌ Leave hooks disabled
  ❌ Commit .env, .taskmaster/, or temp files
  ❌ Merge feature branches containing both app + setup changes
```

---

**Updated**: November 9, 2025  
**For Questions**: See ORCHESTRATION_SYSTEM.md (detailed spec) or ORCHESTRATION.md (quick start)
