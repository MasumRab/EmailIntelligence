# Branch Alignment Non-Regression Guide

**Date:** 2026-03-28
**Status:** ACTIVE — Must be consulted before any branch alignment work
**Scope:** `main`, `scientific`, `orchestration-tools`, `taskmaster`

---

## Purpose

This document records **key architectural decisions** that must NOT be regressed during branch alignment, merges, cherry-picks, or propagation work. Every item here was established through deliberate decision-making and prior incident resolution.

Violating any of these invariants will reintroduce bugs, break agent workflows, or contaminate branch isolation.

---

## Decision Registry

### D1: `.taskmaster/` Is a Git Worktree, Not a Submodule

**Decision:** `.taskmaster/` is managed as a **Git worktree** pointing to the `taskmaster` branch.
**Date:** March 2026 (reverted from Dec 2025 submodule approach)
**Branches affected:** All

| Invariant | Description |
|-----------|-------------|
| No `.gitmodules` | The file `.gitmodules` must NOT exist on any branch |
| No gitlink entries | `.taskmaster` must NOT be tracked as mode `160000` (submodule) in any branch index |
| Worktree is local | The worktree is created per-clone with `git worktree add .taskmaster origin/taskmaster` — it is never committed |
| No `git submodule` commands | Never run `git submodule add`, `git submodule update`, or `git submodule init` for `.taskmaster` |

**Regression test:**
```bash
# Must fail (no .gitmodules)
test ! -f .gitmodules

# Must return empty (no tracked submodule entry)
git ls-tree HEAD | grep -c "160000.*taskmaster"  # Must be 0

# Worktree must be functional
ls .taskmaster/AGENTS.md
```

**Reference docs:** `SUBMODULE_CONFIGURATION.md`, `TASKMASTER_WORKTREE_MIGRATION.md`

---

### D2: `.taskmaster/` Must Be in `.gitignore` (Defense in Depth)

**Decision:** `.taskmaster/` is listed in `.gitignore` on ALL non-taskmaster branches.
**Date:** March 2026 (resolved prior contradiction in docs)
**Branches affected:** `main`, `scientific`, `orchestration-tools`, all feature branches

| Invariant | Description |
|-----------|-------------|
| In `.gitignore` | `.taskmaster/` must appear in `.gitignore` on every non-taskmaster branch |
| No whitelist | `!.taskmaster/**` must NEVER appear in `.gitignore` |
| No `.taskmaster/.gitignore` | Must never create a `.gitignore` file inside the worktree |
| Agents can still read | `.gitignore` only affects git tracking — agents read files on disk freely |

**Why this matters:**
- `.gitignore` prevents `git add .` / `git add -A` from staging worktree files
- Pre-commit hook catches `git add -f` as a safety net
- This is a **defense-in-depth** strategy — both layers are required

**Regression test:**
```bash
# Must match (is in .gitignore)
grep -q "^\.taskmaster/" .gitignore && echo "PASS" || echo "FAIL"

# Must NOT match (no whitelist)
grep -q "!\.taskmaster" .gitignore && echo "FAIL" || echo "PASS"

# Must NOT exist
test ! -f .taskmaster/.gitignore && echo "PASS" || echo "FAIL"
```

**Reference docs:** `TASKMASTER_BRANCH_CONVENTIONS.md`, `TASKMASTER_ISOLATION_FIX.md`

---

### D3: Pre-Commit Hook Enforces Worktree Isolation

**Decision:** A pre-commit hook at `scripts/hooks/pre-commit` blocks committing `.taskmaster/` files on non-taskmaster branches.
**Branches affected:** `orchestration-tools` (has it), `main` and `scientific` (must be added during alignment)

| Invariant | Description |
|-----------|-------------|
| Hook source exists | `scripts/hooks/pre-commit` must exist and contain `.taskmaster/` check |
| Hook blocks staging | If `.taskmaster/` files are staged, commit must be rejected with clear error |
| Hook is installable | `scripts/install-hooks.sh` copies hook source to `.git/hooks/` |
| Hook is not the only defense | `.gitignore` is layer 1; hook is layer 2 (defense in depth) |

**Regression test:**
```bash
# Hook source must contain the check
grep -q "\.taskmaster/" scripts/hooks/pre-commit && echo "PASS" || echo "FAIL"
```

**Reference docs:** `TASKMASTER_ISOLATION_FIX.md`, `scripts/hooks/pre-commit`

---

### D4: Branch Isolation — Never Merge Across Primary Branches

**Decision:** Primary branches (`main`, `scientific`, `orchestration-tools`, `taskmaster`) must NEVER be merged directly into each other.
**Date:** Established convention, documented in multiple guides

| Invariant | Description |
|-----------|-------------|
| No direct merges | Never `git merge main` from `orchestration-tools` or vice versa |
| Cherry-pick only | Use `git cherry-pick` or file-level backport for cross-branch updates |
| File-level backport | `git show source-branch:path/to/file > path/to/file` is the safest method |
| Branch structures differ | `src/` layout is incompatible across branches — merge will corrupt |

**Why this matters:**
- `main` has `src/backend/data/`, `src/backend/node_engine/`
- `orchestration-tools` has `src/context_control/`, `src/cli/commands/`
- `scientific` has ML/data analysis components
- A merge would pollute each branch with incompatible files

**Regression test:**
```bash
# Before any cross-branch work, verify you're using cherry-pick or file backport
# NEVER run:
#   git merge main              (from orchestration-tools)
#   git merge orchestration-tools (from main)
#   git merge scientific        (from main)
```

**Reference docs:** `BRANCH_ISOLATION_GUIDELINES.md`, `BRANCH_UPDATE_PROCEDURE.md`

---

### D5: `.gitignore` Branch-Specific Entries Must Be Preserved

**Decision:** Each branch has specific `.gitignore` entries that must not be removed during alignment.
**Branches affected:** All

| Branch | Required `.gitignore` entries |
|--------|------------------------------|
| All branches | `.taskmaster/`, `worktrees/` |
| `main` | `.orchestration-disabled` |
| `orchestration-tools` | `.orchestration-disabled`, `.context-control/`, `.merge-notes/` |
| All branches | `.env`, `*.db`, `credentials.json`, `token.json` |

| Invariant | Description |
|-----------|-------------|
| Never remove security entries | `.env`, `credentials.json`, `token.json`, `*.db` must always be ignored |
| Never remove `.taskmaster/` | Required for worktree isolation (see D2) |
| Never remove `worktrees/` | Other worktrees may exist locally |
| Preserve branch-specific entries | Don't overwrite `.gitignore` wholesale from another branch |

**Regression test:**
```bash
# Critical security entries must exist
for entry in ".env" "credentials.json" "token.json" ".taskmaster/"; do
  grep -q "$entry" .gitignore && echo "PASS: $entry" || echo "FAIL: $entry"
done
```

---

### D6: Orchestration Files Must Not Cross Branch Boundaries

**Decision:** IDE orchestration directories are branch-specific and must not be propagated.
**Branches affected:** All

| Invariant | Description |
|-----------|-------------|
| No orchestration on taskmaster | `.specify/`, `.gemini/`, `.qwen/`, `.kilo/`, `.roo/`, `.clinerules/` must NOT exist on taskmaster branch |
| No taskmaster files on other branches | `.taskmaster/` content must NOT be committed on `main`, `scientific`, or `orchestration-tools` |
| Agent configs are branch-local | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` content may differ per branch — don't overwrite |

**Reference docs:** `TASKMASTER_BRANCH_CONVENTIONS.md` (Section 1: Branch Isolation)

---

### D7: Documentation Propagation Must Be File-Level, Not Branch-Level

**Decision:** When propagating documentation updates across branches, use file-level backport, not merge or the bulk sync script.

| Invariant | Description |
|-----------|-------------|
| No bulk sync for docs | `scripts/update-all-branches.sh` is for infrastructure scripts only, not documentation migration |
| File-level backport | Use `git show source:file > file` to bring specific docs to target branch |
| Small commits | Each propagated change should be a small, isolated commit |
| Branch-specific edits | After backporting, verify content makes sense on the target branch |

**Safe propagation pattern:**
```bash
git checkout target-branch
git show source-branch:DOCUMENT.md > DOCUMENT.md
git add DOCUMENT.md
git commit -m "docs: backport DOCUMENT.md from source-branch"
```

---

### D8: `main` Branch — Submodule Cleanup Required

**Decision:** The `main` branch still has legacy submodule metadata that must be cleaned up during alignment.
**Status:** PENDING — must be done as part of branch alignment

| Cleanup item | Command |
|-------------|---------|
| Remove gitlink entry | `git rm --cached .taskmaster` |
| Remove `.gitmodules` | `rm .gitmodules && git add -A .gitmodules` |
| Verify clean index | `git ls-tree HEAD \| grep 160000` must return empty |

**⚠️ WARNING:** Simply deleting `.gitmodules` is NOT sufficient. The gitlink (mode `160000`) must also be removed from the index with `git rm --cached .taskmaster`.

---

### D9: `scientific` Branch — Missing `.taskmaster/` in `.gitignore`

**Decision:** The `scientific` branch currently lacks `.taskmaster/` in its `.gitignore` — this must be added during alignment.
**Status:** PENDING

```bash
git checkout scientific
echo '.taskmaster/' >> .gitignore
git add .gitignore
git commit -m "chore: ignore taskmaster worktree path"
```

---

### D10: Pre-Commit Hooks Missing on `main` and `scientific`

**Decision:** `main` and `scientific` branches lack `scripts/hooks/pre-commit` with the `.taskmaster/` isolation check. This must be added during alignment.
**Status:** PENDING

```bash
mkdir -p scripts/hooks
git show orchestration-tools:scripts/hooks/pre-commit > scripts/hooks/pre-commit
chmod +x scripts/hooks/pre-commit
git add scripts/hooks/pre-commit
git commit -m "chore: add pre-commit guard for taskmaster worktree files"
```

---

## Alignment Execution Order

When performing branch alignment, follow this order (lowest risk first):

```
1. orchestration-tools  (hooks already present, .gitignore correct — docs only)
2. scientific           (needs .gitignore fix + hooks + docs)
3. main                 (needs submodule removal + hooks + docs — highest risk)
```

---

## Pre-Alignment Checklist

Before starting any branch alignment work:

- [ ] Read this document completely
- [ ] Verify `.taskmaster` worktree exists: `git worktree list`
- [ ] Verify working tree is clean: `git status`
- [ ] Fetch latest: `git fetch origin`
- [ ] Confirm alignment method is cherry-pick or file-level backport (NEVER merge)
- [ ] Identify which decisions (D1–D10) are relevant to the work

## Post-Alignment Verification

After completing alignment on each branch:

- [ ] `.gitmodules` does NOT exist
- [ ] `git ls-tree HEAD | grep 160000` returns empty (no submodule entries)
- [ ] `.gitignore` contains `.taskmaster/`
- [ ] `.gitignore` does NOT contain `!.taskmaster/**`
- [ ] `scripts/hooks/pre-commit` exists and contains `.taskmaster/` check
- [ ] No orchestration files leaked across branches
- [ ] Security-sensitive entries still in `.gitignore` (`.env`, `credentials.json`, etc.)

---

## Violation Detection & Remediation

This section provides concrete commands to **search for commits that violated** each decision and **step-by-step remediation** for each violation type.

### General: Full Audit Script

Run this from the repo root to check all decisions at once against a given branch:

```bash
#!/bin/bash
# Usage: bash audit_branch.sh <branch-name>
BRANCH="${1:-HEAD}"
echo "=== Auditing branch: $BRANCH ==="
FAIL=0

# D1: No .gitmodules
if git show "$BRANCH":.gitmodules >/dev/null 2>&1; then
  echo "FAIL [D1]: .gitmodules exists on $BRANCH"
  FAIL=1
else
  echo "PASS [D1]: No .gitmodules"
fi

# D1: No gitlink 160000
if git ls-tree "$BRANCH" 2>/dev/null | grep -q "160000.*taskmaster"; then
  echo "FAIL [D1]: .taskmaster tracked as submodule (gitlink 160000) on $BRANCH"
  FAIL=1
else
  echo "PASS [D1]: No submodule gitlink"
fi

# D2: .taskmaster/ in .gitignore
if git show "$BRANCH":.gitignore 2>/dev/null | grep -q "^\.taskmaster/"; then
  echo "PASS [D2]: .taskmaster/ in .gitignore"
else
  echo "FAIL [D2]: .taskmaster/ NOT in .gitignore on $BRANCH"
  FAIL=1
fi

# D2: No whitelist
if git show "$BRANCH":.gitignore 2>/dev/null | grep -q '!\.taskmaster'; then
  echo "FAIL [D2]: !.taskmaster whitelist found in .gitignore on $BRANCH"
  FAIL=1
else
  echo "PASS [D2]: No .taskmaster whitelist"
fi

# D3: Pre-commit hook source
if git show "$BRANCH":scripts/hooks/pre-commit 2>/dev/null | grep -q '\.taskmaster/'; then
  echo "PASS [D3]: Pre-commit hook has .taskmaster/ check"
else
  echo "WARN [D3]: scripts/hooks/pre-commit missing or lacks .taskmaster/ check on $BRANCH"
fi

# D5: Security entries
for entry in ".env" "credentials.json" "token.json"; do
  if git show "$BRANCH":.gitignore 2>/dev/null | grep -q "$entry"; then
    echo "PASS [D5]: $entry in .gitignore"
  else
    echo "FAIL [D5]: $entry NOT in .gitignore on $BRANCH"
    FAIL=1
  fi
done

# D6: No orchestration dirs on taskmaster
if [[ "$BRANCH" == *"taskmaster"* ]]; then
  for dir in .specify .gemini .qwen .kilo .roo .clinerules; do
    if git ls-tree "$BRANCH" "$dir/" >/dev/null 2>&1; then
      echo "FAIL [D6]: $dir/ exists on taskmaster branch"
      FAIL=1
    fi
  done
fi

echo ""
if [[ $FAIL -eq 0 ]]; then
  echo "✅ All checks passed for $BRANCH"
else
  echo "❌ Violations detected — see above"
fi
```

---

### D1 Violations: Submodule Reintroduced

#### How to detect

```bash
# Find ALL commits across all branches that added/modified .gitmodules
git log --all --oneline --diff-filter=A -- .gitmodules
git log --all --oneline -- .gitmodules

# Find commits that added .taskmaster as a submodule (gitlink mode 160000)
git log --all --oneline --raw -- .taskmaster | grep "^:.*160000"

# Check which branches currently have .gitmodules
for b in main scientific orchestration-tools taskmaster; do
  echo -n "origin/$b: "
  git show "origin/$b":.gitmodules >/dev/null 2>&1 && echo "HAS .gitmodules ❌" || echo "clean ✅"
done

# Check which branches have gitlink entries
for b in main scientific orchestration-tools taskmaster; do
  echo -n "origin/$b: "
  git ls-tree "origin/$b" 2>/dev/null | grep -q "160000.*taskmaster" \
    && echo "HAS submodule gitlink ❌" || echo "clean ✅"
done
```

**Known historical violating commits:**
- `472db8f7` — "Add .taskmaster as submodule tracking taskmaster branch"
- `5af0da32` — "Add .taskmaster as submodule"
- `73679231` — "Add shared .taskmaster setup as submodule"

#### How to remediate

```bash
git checkout <affected-branch>

# Step 1: Remove the gitlink from the index (if tracked as submodule)
git ls-tree HEAD | grep "160000.*taskmaster"   # check if present
git rm --cached .taskmaster 2>/dev/null        # remove gitlink entry

# Step 2: Delete .gitmodules
rm -f .gitmodules
git add -A .gitmodules 2>/dev/null

# Step 3: Clean up submodule metadata in .git/
rm -rf .git/modules/.taskmaster 2>/dev/null

# Step 4: Commit
git commit -m "fix: remove legacy .taskmaster submodule metadata

Resolves D1 violation: .taskmaster must be a worktree, not a submodule.
Ref: BRANCH_ALIGNMENT_NON_REGRESSION_GUIDE.md"

# Step 5: Verify
test ! -f .gitmodules && echo "PASS" || echo "FAIL"
git ls-tree HEAD | grep -c "160000.*taskmaster"  # must be 0
```

---

### D2 Violations: `.taskmaster/` Missing from or Whitelisted in `.gitignore`

#### How to detect

```bash
# Find commits that removed .taskmaster/ from .gitignore
git log --all --oneline -S '.taskmaster/' -- .gitignore

# Find commits that added !.taskmaster whitelist
git log --all --oneline -S '!.taskmaster' -- .gitignore

# Find commits that created .taskmaster/.gitignore
git log --all --oneline --diff-filter=A -- .taskmaster/.gitignore

# Check current state per branch
for b in main scientific orchestration-tools; do
  echo -n "origin/$b .taskmaster/ in .gitignore: "
  git show "origin/$b":.gitignore 2>/dev/null | grep -q "^\.taskmaster/" \
    && echo "YES ✅" || echo "NO ❌"
  echo -n "origin/$b !.taskmaster whitelist: "
  git show "origin/$b":.gitignore 2>/dev/null | grep -q '!\.taskmaster' \
    && echo "FOUND ❌" || echo "clean ✅"
done
```

**Known historical violating commits:**
- `fd665c03` — "fix: use .git/info/exclude instead of .gitignore for taskmaster worktree"
- `a0400993` — "fix: correct .taskmaster worktree gitignore isolation"

#### How to remediate

**Missing `.taskmaster/` from `.gitignore`:**
```bash
git checkout <affected-branch>

# Add .taskmaster/ near other project-specific ignores
# Find the right location (near worktrees/)
grep -n "worktrees/" .gitignore
# Append after that line, or at end of project-specific section
echo '.taskmaster/' >> .gitignore

git add .gitignore
git commit -m "fix: add .taskmaster/ to .gitignore (D2 compliance)

Defense-in-depth: .gitignore prevents accidental staging,
pre-commit hook catches force-adds.
Ref: BRANCH_ALIGNMENT_NON_REGRESSION_GUIDE.md"
```

**Whitelist `!.taskmaster/**` found:**
```bash
git checkout <affected-branch>

# Remove the whitelist line
sed -i '/!\.taskmaster/d' .gitignore

git add .gitignore
git commit -m "fix: remove !.taskmaster whitelist from .gitignore (D2 compliance)

Whitelisting .taskmaster defeats worktree isolation.
Ref: BRANCH_ALIGNMENT_NON_REGRESSION_GUIDE.md"
```

**`.taskmaster/.gitignore` exists:**
```bash
git checkout <affected-branch>

git rm .taskmaster/.gitignore 2>/dev/null || rm -f .taskmaster/.gitignore
git add -A .taskmaster/.gitignore
git commit -m "fix: remove .taskmaster/.gitignore (D2 compliance)

Worktree directories must not have their own .gitignore.
Ref: BRANCH_ALIGNMENT_NON_REGRESSION_GUIDE.md"
```

---

### D3 Violations: Pre-Commit Hook Missing or Gutted

#### How to detect

```bash
# Check which branches have the hook source
for b in main scientific orchestration-tools; do
  echo -n "origin/$b scripts/hooks/pre-commit: "
  git show "origin/$b":scripts/hooks/pre-commit 2>/dev/null | grep -q '\.taskmaster/' \
    && echo "HAS check ✅" || echo "MISSING ❌"
done

# Find commits that deleted or modified the hook
git log --all --oneline -- scripts/hooks/pre-commit

# Find commits that removed the .taskmaster check from hooks
git log --all --oneline -S '\.taskmaster/' -- scripts/hooks/pre-commit

# Check if installed locally
test -f .git/hooks/pre-commit && grep -q '\.taskmaster/' .git/hooks/pre-commit \
  && echo "Installed ✅" || echo "NOT installed locally ❌"
```

#### How to remediate

```bash
git checkout <affected-branch>
mkdir -p scripts/hooks

# Backport from orchestration-tools (canonical source)
git show origin/orchestration-tools:scripts/hooks/pre-commit > scripts/hooks/pre-commit
chmod +x scripts/hooks/pre-commit

git add scripts/hooks/pre-commit
git commit -m "fix: restore pre-commit hook with .taskmaster/ guard (D3 compliance)

Ref: BRANCH_ALIGNMENT_NON_REGRESSION_GUIDE.md"

# Also install locally
cp scripts/hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

---

### D4 Violations: Direct Cross-Branch Merge Detected

#### How to detect

```bash
# Find merge commits on orchestration-tools that merged main
git log origin/orchestration-tools --oneline --merges --grep="[Mm]ain" | head -20

# Find merge commits on main that merged orchestration-tools
git log origin/main --oneline --merges --grep="[Oo]rchestration" | head -20

# Find merge commits on scientific that merged main or vice versa
git log origin/scientific --oneline --merges --grep="[Mm]ain" | head -20
git log origin/main --oneline --merges --grep="[Ss]cientific" | head -20

# More thorough: find ANY merge commits and inspect parents
git log origin/orchestration-tools --oneline --merges | head -20

# Check if a specific merge commit has a parent from another primary branch
# Replace <merge-hash> with actual hash
git log --oneline --ancestry-path origin/main..<merge-hash> 2>/dev/null | head -5

# Find all commits on orchestration-tools whose second parent is on main
git log origin/orchestration-tools --oneline --merges --format="%H %P %s" | while read hash p1 p2 rest; do
  if [ -n "$p2" ]; then
    if git merge-base --is-ancestor "$p2" origin/main 2>/dev/null; then
      echo "VIOLATION: $hash merged main into orchestration-tools: $rest"
    fi
  fi
done
```

**Known historical violating commits:**
- `421317c7` — "Merge main into orchestration-tools - complete merge with all files"

#### How to remediate

Direct merge violations are **the hardest to fix** because they pollute the branch history with incompatible files.

**Option A: Revert the merge (if recent, no subsequent work depends on it):**
```bash
git checkout <affected-branch>

# Find the merge commit
git log --oneline --merges | head -10

# Revert the merge (keeping the branch's own history as mainline)
git revert -m 1 <merge-commit-hash>
git commit -m "revert: undo direct merge from <source-branch> (D4 violation)

Direct merges between primary branches are prohibited.
Use cherry-pick or file-level backport instead.
Ref: BRANCH_ALIGNMENT_NON_REGRESSION_GUIDE.md"
```

**Option B: Identify and remove polluting files (if merge is old):**
```bash
git checkout <affected-branch>

# Find files that shouldn't be on this branch
# For orchestration-tools: should NOT have src/backend/data/, src/backend/node_engine/
git ls-files | grep -E "^src/backend/(data|node_engine)/" | head -20

# Remove polluting files
git rm -r src/backend/data/ src/backend/node_engine/ 2>/dev/null
git commit -m "fix: remove files from illegal merge (D4 cleanup)

These files belong on main, not orchestration-tools.
Ref: BRANCH_ALIGNMENT_NON_REGRESSION_GUIDE.md"
```

**Option C: Reset branch to before the merge (nuclear — use with extreme caution):**
```bash
# Only if no valuable work exists after the merge
git checkout <affected-branch>
git log --oneline | head -20    # find the commit before the merge
git reset --hard <commit-before-merge>
git push --force-with-lease origin <affected-branch>
```

---

### D5 Violations: Security Entries Removed from `.gitignore`

#### How to detect

```bash
# Find commits that modified .gitignore and may have removed security entries
git log --all --oneline -S '.env' -- .gitignore | head -10
git log --all --oneline -S 'credentials.json' -- .gitignore | head -10
git log --all --oneline -S 'token.json' -- .gitignore | head -10

# Check current state
for b in main scientific orchestration-tools; do
  echo "=== origin/$b ==="
  for entry in ".env" "credentials.json" "token.json" "*.db" ".taskmaster/" "worktrees/"; do
    echo -n "  $entry: "
    git show "origin/$b":.gitignore 2>/dev/null | grep -q "$entry" \
      && echo "✅" || echo "❌ MISSING"
  done
done

# Find commits that did wholesale .gitignore replacement
git log --all --oneline --format="%H %s" -- .gitignore | while read hash msg; do
  lines_changed=$(git show "$hash" -- .gitignore 2>/dev/null | grep -c "^[-+]" || echo 0)
  if [ "$lines_changed" -gt 50 ]; then
    echo "SUSPECT (${lines_changed} lines changed): $(echo $hash | cut -c1-8) $msg"
  fi
done
```

#### How to remediate

```bash
git checkout <affected-branch>

# Verify which entries are missing
for entry in ".env" "credentials.json" "token.json" "*.db" ".taskmaster/" "worktrees/"; do
  grep -q "$entry" .gitignore || echo "MISSING: $entry"
done

# Add missing entries (append to project-specific section)
cat >> .gitignore << 'EOF'

# Restored security entries (D5 compliance)
.env
credentials.json
token.json
EOF

git add .gitignore
git commit -m "fix: restore missing security entries in .gitignore (D5 compliance)

Ref: BRANCH_ALIGNMENT_NON_REGRESSION_GUIDE.md"

# IMPORTANT: Check if secrets were already committed
git log --all --oneline -- credentials.json token.json .env | head -5
# If any results: secrets may be in history — consider git-filter-repo
```

---

### D6 Violations: Orchestration Files Leaked Across Branches

#### How to detect

```bash
# Check for orchestration dirs on taskmaster branch
for dir in .specify .gemini .qwen .kilo .roo .clinerules .cursor/rules/orchestration-tools; do
  git ls-tree -d origin/taskmaster "$dir" 2>/dev/null | head -1 | \
    grep -q . && echo "VIOLATION [D6]: $dir/ exists on taskmaster ❌"
done

# Check for .taskmaster content committed on non-taskmaster branches
for b in main scientific orchestration-tools; do
  count=$(git ls-tree -r "origin/$b" 2>/dev/null | grep -c "\.taskmaster/" || echo 0)
  if [ "$count" -gt 0 ]; then
    echo "VIOLATION [D6]: $count .taskmaster/ files tracked on $b ❌"
  else
    echo "PASS [D6]: No .taskmaster/ files on $b ✅"
  fi
done

# Find commits that added orchestration files to taskmaster
git log origin/taskmaster --oneline --diff-filter=A -- ".specify/*" ".gemini/*" ".qwen/*" ".kilo/*" ".roo/*" ".clinerules/*"
```

#### How to remediate

```bash
git checkout <affected-branch>

# Remove files that don't belong (example: orchestration dirs on taskmaster)
git rm -r .specify/ .gemini/ .qwen/ .kilo/ .roo/ .clinerules/ 2>/dev/null
git commit -m "fix: remove orchestration files from taskmaster branch (D6 compliance)

These directories belong on orchestration-tools, not taskmaster.
Ref: BRANCH_ALIGNMENT_NON_REGRESSION_GUIDE.md"

# Remove .taskmaster/ content from non-taskmaster branch
git rm -r --cached .taskmaster/ 2>/dev/null
git commit -m "fix: untrack .taskmaster/ files (D6 compliance)

.taskmaster/ is a worktree and must not be committed on this branch.
Ref: BRANCH_ALIGNMENT_NON_REGRESSION_GUIDE.md"
```

---

### D7 Violations: Bulk Sync or Merge Used for Doc Propagation

#### How to detect

```bash
# Find commits that suggest bulk sync was used
git log --all --oneline --grep="sync infrastructure" | head -10
git log --all --oneline --grep="update-all-branches" | head -10

# Find commits with suspiciously many files changed (>20 docs at once)
for b in main scientific orchestration-tools; do
  echo "=== origin/$b: Large doc commits ==="
  git log "origin/$b" --oneline --format="%H %s" | while read hash msg; do
    md_count=$(git show "$hash" --stat 2>/dev/null | grep -c "\.md" || echo 0)
    if [ "$md_count" -gt 15 ]; then
      echo "  SUSPECT ($md_count .md files): $(echo $hash | cut -c1-8) $msg"
    fi
  done | head -5
done
```

#### How to remediate

If a bulk sync introduced wrong content, cherry-pick the correct file versions:

```bash
git checkout <affected-branch>

# Identify which files have wrong content
# Compare with the canonical source
diff <(git show origin/004-guided-workflow:SUBMODULE_CONFIGURATION.md) \
     <(git show HEAD:SUBMODULE_CONFIGURATION.md) | head -30

# Backport the correct version
git show origin/004-guided-workflow:SUBMODULE_CONFIGURATION.md > SUBMODULE_CONFIGURATION.md
git add SUBMODULE_CONFIGURATION.md
git commit -m "fix: backport correct SUBMODULE_CONFIGURATION.md (D7 compliance)

File-level backport from 004-guided-workflow, not bulk sync.
Ref: BRANCH_ALIGNMENT_NON_REGRESSION_GUIDE.md"
```

---

### D8 Violations: `main` Still Has Submodule Metadata

#### How to detect

```bash
# Check for .gitmodules on main
git show origin/main:.gitmodules 2>/dev/null && echo "VIOLATION: .gitmodules on main ❌" || echo "clean ✅"

# Check for gitlink entry
git ls-tree origin/main | grep "160000" && echo "VIOLATION: gitlink on main ❌" || echo "clean ✅"

# Find the original commit that added the submodule
git log origin/main --oneline -- .gitmodules | head -5

# Check .git/modules/ for stale submodule data
ls -la .git/modules/.taskmaster 2>/dev/null && echo "STALE: .git/modules/.taskmaster exists" || echo "clean"
```

**Known current state:** `main` has `.gitmodules` with submodule config (confirmed).

#### How to remediate

See D1 remediation above. For `main` specifically:

```bash
git checkout main

# Remove submodule fully
git rm --cached .taskmaster 2>/dev/null    # remove gitlink
rm -f .gitmodules                          # remove config file
git add -A .gitmodules
rm -rf .git/modules/.taskmaster 2>/dev/null  # clean metadata

git commit -m "chore: remove legacy .taskmaster submodule metadata

.taskmaster is now a git worktree, not a submodule.
Ref: BRANCH_ALIGNMENT_NON_REGRESSION_GUIDE.md (D1, D8)"

# Verify
test ! -f .gitmodules && echo "PASS" || echo "FAIL"
git ls-tree HEAD | grep -c "160000" | xargs test 0 -eq && echo "PASS" || echo "FAIL"
```

---

### D9 Violations: `scientific` Missing `.taskmaster/` in `.gitignore`

#### How to detect

```bash
git show origin/scientific:.gitignore 2>/dev/null | grep -q "^\.taskmaster/" \
  && echo "PASS: .taskmaster/ in scientific .gitignore ✅" \
  || echo "FAIL: .taskmaster/ NOT in scientific .gitignore ❌"
```

#### How to remediate

```bash
git checkout scientific

# Add .taskmaster/ near worktrees/ (which already exists)
sed -i '/^worktrees\/$/a .taskmaster/' .gitignore
# Or if sed is tricky, just append:
# echo '.taskmaster/' >> .gitignore

git add .gitignore
git commit -m "chore: add .taskmaster/ to .gitignore (D2/D9 compliance)

Prevents accidental staging of worktree files.
Ref: BRANCH_ALIGNMENT_NON_REGRESSION_GUIDE.md"
```

---

### D10 Violations: Hooks Missing on `main` / `scientific`

#### How to detect

```bash
for b in main scientific; do
  echo -n "origin/$b: "
  git show "origin/$b":scripts/hooks/pre-commit 2>/dev/null | grep -q '\.taskmaster/' \
    && echo "pre-commit hook with .taskmaster/ check ✅" \
    || echo "pre-commit hook MISSING ❌"
done
```

#### How to remediate

```bash
git checkout <main or scientific>
mkdir -p scripts/hooks

# Backport from orchestration-tools (canonical hook source)
git show origin/orchestration-tools:scripts/hooks/pre-commit > scripts/hooks/pre-commit
chmod +x scripts/hooks/pre-commit

git add scripts/hooks/pre-commit
git commit -m "chore: add pre-commit hook with .taskmaster/ isolation guard (D3/D10)

Backported from orchestration-tools.
Ref: BRANCH_ALIGNMENT_NON_REGRESSION_GUIDE.md"
```

---

### General: How to Find the Commit That Introduced a Violation

When you know a violation exists but don't know when it was introduced:

```bash
# Method 1: git log with pickaxe (-S) — finds commits that added/removed a string
git log --all --oneline -S '<search-string>' -- <file>
# Examples:
git log --all --oneline -S '!.taskmaster' -- .gitignore     # D2 whitelist violation
git log --all --oneline -S 'submodule ".taskmaster"' -- .gitmodules  # D1 submodule

# Method 2: git log with regex (-G) — finds commits where diff matches regex
git log --all --oneline -G '160000.*taskmaster' | head -10   # gitlink entries

# Method 3: git bisect — binary search for when a property changed
git bisect start
git bisect bad HEAD               # current state is bad (has violation)
git bisect good <known-good-hash> # a commit known to be clean
# Then test each bisect step with the regression test for that decision

# Method 4: Blame a specific line in .gitignore
git log --all --oneline -S '.taskmaster/' -- .gitignore  # find all touches
git blame .gitignore | grep taskmaster                    # who last changed it

# Method 5: Find all branches containing a violating commit
git branch -a --contains <violating-commit-hash>
```

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-03-28 | Initial creation with decisions D1–D10 | AI Agent (Amp) |
| 2026-03-29 | Added violation detection & remediation for all decisions (D1–D10), audit script, and general forensic methods | AI Agent (Amp) |

---

*This document is the canonical non-regression reference for branch alignment. Update it when new architectural decisions are made.*
