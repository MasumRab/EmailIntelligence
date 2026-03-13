# Task 004: Tuned Recommendations for EmailIntelligence Repo

**Date:** 2026-03-13
**Purpose:** Reality-adjusted branch protection recommendations based on actual repo analysis.

---

## Repo Reality Snapshot

| Fact | Data |
|---|---|
| Total unique branches | ~370 |
| Top naming patterns | `bolt` (212), `sentinel` (31), `users/` (31), `feature` (26), `orchestration-tools` (15) |
| Unprefixed branches | ~75 (taskmaster, develop, release, scientific, main, beads-sync, task-ID branches) |
| GitHub protection on `main` | **Disabled** (`enforcement_level: off`) |
| Existing hooks | `pre-commit` (bd sync), `post-commit` (roborev), `post-merge` (bd import) |
| Primary branches | `main`, `scientific`, `orchestration-tools` |
| Key long-lived branches | `taskmaster`, `develop`, `release` |

---

## Must-Do Recommendations

### 1. Expand Protected Branch List Beyond the Original 3

Task 004 spec only lists `main`, `scientific`, `orchestration-tools`. Expand to:

```python
PROTECTED_BRANCHES = [
    "main",
    "scientific",
    "orchestration-tools",
    "develop",
    "release",
    "master",        # Legacy, still exists on remote
]
```

**Rationale:** `develop` and `release` are local long-lived branches that should never receive accidental direct commits. `master` exists on the remote as a legacy artifact.

---

### 2. Match Actual Branch Naming Prefixes (13 patterns, not 4)

Task 004 spec says `feature/`, `docs/`, `fix/`, `enhancement/`. The repo actually uses 13 distinct prefix patterns:

```python
ALLOWED_PREFIXES = [
    # Original spec (keep)
    "feature/", "feature-",    # 26 branches
    "docs/", "docs-",          # 8 branches
    "fix/", "fix-",            # 8 branches
    # Must add — heavily used in this repo
    "bolt/", "bolt-",          # 212 branches (AI-generated optimization)
    "sentinel/", "sentinel-",  # 31 branches (security fixes)
    "perf/", "perf-",          # 6 branches
    "feat/", "feat-",          # 5 branches
    "refactor-", "refactor/",  # 4 branches
    "bugfix/",                 # 1 branch
    # Organizational
    "users/",                  # 31 branches (user workspace)
    "backup/",                 # Safety backups
    "archive/",                # Historical
    "consolidate/",            # Consolidation work
    # Tool-generated (whitelist)
    "mergify/",                # Mergify bot
    "cto/",                    # CTO audit branches
    "align-",                  # Alignment operation branches
    # Enhancement
    "enhancement/", "enhance-", # 2 branches
]
```

**Critical:** With 75 unprefixed branches already existing, this check **must remain a warning, not a block**.

---

### 3. Hook Chaining — Don't Overwrite Existing Hooks

`pre-commit` already runs `bd sync --flush-only`. Must **chain**, not replace.

**Recommended approach — hook dispatcher:**

```bash
# .git/hooks/pre-commit becomes a dispatcher:
#!/bin/sh
for hook in .githooks/pre-commit.d/*; do
    [ -x "$hook" ] && "$hook" "$@" || exit $?
done
```

Then:
- Move existing bd hook → `.githooks/pre-commit.d/01-bd-sync.sh`
- Add alignment hook → `.githooks/pre-commit.d/02-branch-protection.py`
- `pre-push` has no custom hook yet — safe to add directly

---

### 4. Enable GitHub Branch Protection on `main` and `scientific`

Currently **disabled** (`enforcement_level: off`).

| Rule | Recommended | Rationale |
|---|---|---|
| Block force pushes to `main` | ✅ MUST | `backup/scientific-*` and `diverged-*` branches = evidence of past destructive ops |
| Block branch deletion on `main` | ✅ MUST | Prevent accidental deletion |
| Block force pushes to `scientific` | ✅ MUST | Has backup branches proving past instability |
| Require PR for `main` | ❌ Skip | Single developer — too much friction |
| Require status checks | ❌ Skip for now | No CI pipeline yet; add when Task 008 delivers |

```bash
# Enable via gh CLI
gh api repos/MasumRab/EmailIntelligence/branches/main/protection \
  -X PUT \
  -f required_status_checks='null' \
  -f enforce_admins=false \
  -f required_pull_request_reviews='null' \
  -f restrictions='null' \
  -F allow_force_pushes=false \
  -F allow_deletions=false
```

---

### 5. Start Pre-push Lightweight — Wire Validation Later

Tasks 003 and 008 don't exist yet. Start with what's actionable:

```python
def pre_push_checks():
    branch = get_current_branch()

    # HARD BLOCK: never push directly from protected branch
    if is_protected_branch(branch):
        print("ERROR: Cannot push from protected branch directly")
        sys.exit(1)

    # SOFT WARN: naming convention
    if not is_allowed_prefix(branch):
        print(f"WARNING: '{branch}' doesn't follow naming convention")

    # PLACEHOLDER: wire in when Tasks 003/008 deliver
    # run_validation()
```

---

### 6. Detached HEAD and Rebase-in-Progress Guards

The repo does extensive rebasing (Tasks 009/010 are rebase-based). Hooks must not interfere:

```python
def is_detached_head():
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True, text=True
    )
    return result.stdout.strip() == "HEAD"

def is_rebase_in_progress():
    git_dir = Path(subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        capture_output=True, text=True
    ).stdout.strip())
    return (git_dir / "rebase-merge").exists() or (git_dir / "rebase-apply").exists()

# In hook entry point:
if is_detached_head() or is_rebase_in_progress():
    sys.exit(0)  # Skip all branch checks silently
```

---

### 7. Bolt/Sentinel Branch Awareness

243 AI-generated branches (`bolt-*`, `sentinel-*`) exist. The orchestrator should:
- Recognize as a distinct category (auto-generated, likely stale)
- Not warn about their naming (they're valid)
- Flag for cleanup consideration in Task 007's categorization tool

---

## Summary Checklist

| # | Recommendation | Priority |
|---|---|---|
| 1 | Expand protected branches to include `develop`, `release`, `master` | 🔴 Must |
| 2 | Expand allowed prefixes to match actual 13 repo patterns | 🔴 Must |
| 3 | Implement hook chaining (preserve `bd` pre-commit hook) | 🔴 Must |
| 4 | Enable GitHub force-push/deletion protection on `main` and `scientific` | 🔴 Must |
| 5 | Start pre-push with branch checks only; wire validation later | 🟡 Should |
| 6 | Add detached HEAD / rebase-in-progress guards | 🔴 Must |
| 7 | Whitelist `bolt-*` and `sentinel-*` as known AI-generated prefixes | 🟡 Should |

---

## Open Questions

1. Should `taskmaster` branch itself be added to protected list? (It's the current primary working branch)
2. Cleanup strategy for 212 stale `bolt-*` branches — defer to Task 007 or handle separately?
3. Should `users/masum/*` branches (31) be auto-cleaned on a schedule?

---

*Analysis based on actual `git branch -a` output and `gh api` protection status query from 2026-03-13.*
