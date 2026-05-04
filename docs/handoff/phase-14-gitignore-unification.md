# Phase 14: .gitignore Unification (Branch-Aware)

**Purpose:** Eliminate `.gitignore` drift across branches while preserving branch-specific patterns. Enforce a security-critical baseline (credentials, env files, backups) on every branch.
**Steps:** 6
**Dependencies:** Phase 9 (verification) recommended; can run independently.
**Mode:** Deep (requires per-branch judgment)
**Created:** 2026-04-28

---

## Background

Audit revealed four divergent `.gitignore` versions across the canonical branches:

| Branch | Lines | SHA |
|---|---|---|
| `main` | 108 | 9d08f03c61a7 |
| `scientific` | 94 | 6ce8578b1d24 |
| `orchestration-tools` | 324 | 7c045ac55ae9 |
| `taskmaster` | 149 | b7d30e94a021 |

Critical drift: `main` ignores `token.json`, `credentials.json`, `apikey.json`, `jsons/`; `orchestration-tools` and `taskmaster` do **not**. `taskmaster` over-ignores env files (`.env*.example`, `.env*.template` …) which would hide intentionally-tracked `.env.example`. `orchestration-tools` lacks `*.bak`/`*~` ignores despite many backup files at the repo root.

Goal: one canonical baseline (`scripts/unified.gitignore`) plus an explicit, documented branch-tail block for branch-specific concerns.

---

## Inputs

| File | Purpose |
|------|---------|
| `scripts/unified.gitignore` | Canonical baseline (superset of safe patterns) |
| `scripts/apply-unified-gitignore.sh` | Audit + apply tool (read-only by default) |
| `docs/handoff/context-guard.sh` | Project-root + branch detection (any CWD) |
| `docs/handoff/STATE_<branch>.md` | Per-branch tracker for completion |

---

## Steps

### Step 1 — Setup (context-agnostic)

```bash
# From any directory in the repo:
source docs/handoff/context-guard.sh   # sets PROJECT_ROOT, CURRENT_BRANCH
echo "Operating on: $CURRENT_BRANCH (root: $PROJECT_ROOT)"
```

Pre-flight:

- `git -C "$PROJECT_ROOT" status --porcelain` must be empty.
- `git -C "$PROJECT_ROOT" fetch --all --prune` to refresh remote refs.

### Step 2 — Read-only audit across ALL branches

```bash
bash "$PROJECT_ROOT/scripts/apply-unified-gitignore.sh" --audit \
  > "$PROJECT_ROOT/docs/handoff/gitignore-audit-$(date +%Y%m%d).txt"
```

Review the audit file. For each branch the script reports:

- ✓ no conflicts → safe to apply baseline.
- ⚠ tracked files that the unified ignore would hide → **decision required** (Step 3).

### Step 3 — Per-branch decision matrix

For each ⚠ file in the audit, choose exactly one:

| Decision | Action | When |
|----------|--------|------|
| **Drop** | `git rm --cached <file>` then commit | File is genuinely a build artifact / secret / scratch leak |
| **Keep (branch-specific)** | Add `!<pattern>` to a `# === Branch-specific exceptions ===` block appended to `.gitignore` on that branch only | File is intentional for that branch (e.g. spec branches, backup branches) |
| **Keep (universal)** | Promote to `scripts/unified.gitignore` as a `!<pattern>` and re-audit | The file is intentional on multiple branches |

Document each decision in `docs/handoff/STATE_<branch>.md` under a new "## Phase 14 decisions" heading.

### Step 4 — Apply baseline to canonical branches

```bash
bash "$PROJECT_ROOT/scripts/apply-unified-gitignore.sh" --apply-main-set
```

This commits (locally only) on `main`, `scientific`, `orchestration-tools`, `taskmaster`. **Does not push.**

For non-canonical branches with audit conflicts resolved, apply individually:

```bash
bash "$PROJECT_ROOT/scripts/apply-unified-gitignore.sh" --apply <branch> [<branch>...]
```

### Step 5 — Append branch-specific tail (where required)

After the baseline is committed, on any branch that needs unique exceptions, append the documented tail:

```bash
git checkout <branch>
cat >> "$PROJECT_ROOT/.gitignore" <<'EOF'

# === Branch-specific exceptions (Phase 14) ===
# Document each entry: who added, why, when.
# Example:
# !specs/branch-001/output.json   # Required by spec freeze (2026-04-28)
EOF
git add .gitignore
git commit -m "chore(<branch>): add branch-specific .gitignore exceptions"
```

The `# === Branch-specific exceptions ===` marker is the contract: future re-runs of this phase preserve everything below it and only refresh the section above.

### Step 6 — Verify and push

For each touched branch:

```bash
git checkout <branch>
git status                          # must be clean
git ls-files | xargs -I{} git check-ignore -v {} | head     # spot-check
bash scripts/verify-agent-content.sh                         # AGENTS.md audit (optional)
git push origin <branch>
```

Update `docs/handoff/STATE_<branch>.md`: tick Phase 14 complete, paste the audit summary.

---

## Acceptance Criteria

- [ ] `gitignore-audit-YYYYMMDD.txt` exists in `docs/handoff/`.
- [ ] Every ⚠ entry has a documented decision in the relevant `STATE_<branch>.md`.
- [ ] `main`, `scientific`, `orchestration-tools`, `taskmaster` all have `.gitignore` content where the section **above** the `# === Branch-specific exceptions ===` marker matches `scripts/unified.gitignore` byte-for-byte.
- [ ] No tracked file matching a baseline ignore pattern remains tracked unless protected by a documented `!exception`.
- [ ] No new merge conflicts introduced (re-run `grep -rln '^<<<<<<< ' docs/`).

---

## Rollback

The script never force-pushes and only commits one file per branch. To revert:

```bash
git checkout <branch>
git revert <commit-sha-of-gitignore-update>
git push origin <branch>
```

---

## Notes / Risks

- **Spec branches (`001-*`, `002-*`, `003-*`)** may track `dist/`, `*.bak`, or `jsons/` payloads intentionally. Always audit before applying.
- **Remote-only branches** require `git fetch` and a local tracking branch before `--apply` works.
- **Submodules** (e.g. `taskmaster`) inherit their own `.gitignore`; this phase does not touch them.
- **Pre-commit hooks** that re-write `.gitignore` (e.g. `ruler` sync) must be paused for the duration of this phase, or they'll fight the apply step.
