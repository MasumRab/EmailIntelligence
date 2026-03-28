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

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-03-28 | Initial creation with decisions D1–D10 | AI Agent (Amp) |

---

*This document is the canonical non-regression reference for branch alignment. Update it when new architectural decisions are made.*
