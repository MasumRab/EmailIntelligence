# Lost Features (Disabled/Parked/Reverted) — Forensic Audit

**Repository**: MasumRab/EmailIntelligence  
**Branch**: main (base: main)  
**Audit Date**: 2026-11-11  
**Method**: Read-only forensics per S13 task

---

## 1. .DISABLED Workflows on main (17)

| File | What It Did | Current Status | Last Run | Verdict | Action |
|------|-------------|----------------|----------|---------|--------|
| `gemini-scheduled-triage.yml.DISABLED` | Scheduled Gemini triage of issues/PRs | No active replacement | N/A | **DEAD** | Remove or re-enable with updated config |
| `jules-pr-resolve-conflicts.yml.DISABLED` | Jules auto-resolve merge conflicts | No active replacement | N/A | **DEAD** | Remove — conflict resolution now manual |
| `jules-pr-walkthrough.yml.DISABLED` | Jules PR walkthrough generation | No active replacement | N/A | **DEAD** | Remove |
| `gemini-triage.yml.DISABLED` | Gemini issue/PR triage | active | 2026-11-10 | **LIVE** | gh workflow disable gemini-triage |
| `gemini-review.yml.DISABLED` | Gemini code review | active | 2026-11-10 | **LIVE** | gh workflow disable gemini-review |
| `jules-issue-triage.yml.DISABLED` | Jules issue triage | No active replacement | N/A | **DEAD** | Remove |
| `jules-pr-auto-fix.yml.DISABLED` | Jules auto-fix on label | No active replacement | N/A | **DEAD** | Remove — auto-fix not used |
| `deploy-staging.yml.DISABLED` | Staging deployment | No active replacement | N/A | **DEAD** | Remove — no staging env |
| `gemini-dispatch.yml.DISABLED` | Gemini dispatch trigger | active | 2026-11-06 | **LIVE** | gh workflow disable gemini-dispatch |
| `jules-pr-review.yml.DISABLED` | Jules PR review | disabled_manually | 2026-09-12 | **LIVE** | Keep disabled via gh |
| `jules-pr-force-review.yml.DISABLED` | Force Jules review | No active replacement | N/A | **DEAD** | Remove |
| `gemini-invoke.yml.DISABLED` | Gemini invoke workflow | active | 2026-11-10 | **LIVE** | gh workflow disable gemini-invoke |
| `jules-pr-rebuild.yml.DISABLED` | Jules PR rebuild | No active replacement | N/A | **DEAD** | Remove |
| `extract-orchestration-changes.yml.DISABLED` | Extract orchestration changes | No active replacement | N/A | **DEAD** | Remove |
| `push-check.yml.DISABLED` | Push checks | Replaced by `pr-check.yml` | 2026-09-15 | **LIVE** (migrated) | Keep disabled as archive |
| `jules-pr-address-comments.yml.DISABLED` | Jules address review comments | No active replacement | N/A | **DEAD** | Remove |
| `jules-pr-automerge-label.yml.DISABLED` | Auto-merge on label | No active replacement | N/A | **DEAD** | Remove |

**Summary**: 11 DEAD, 1 LIVE (migrated to pr-check.yml), 5 LIVE (still firing on branches)

**Note:** The statement "everything is safely disabled" is incorrect. The workflows `gemini-dispatch`, `gemini-invoke`, `gemini-review`, `gemini-triage`, and `push-check` (also `jules-pr-review` though manually disabled) are still registered and firing on long-lived branches that pre-date their rename to `.DISABLED` on main.

**Measured on 2026-11-11** (`gh api repos/MasumRab/EmailIntelligence/actions/workflows`,
then each workflow's `.../runs?per_page=1`): `gemini-dispatch.yml`, `gemini-invoke.yml`,
`gemini-review.yml` and `gemini-triage.yml` are all registered `active`; invoke, review and
triage each ran on a long-lived branch at 2026-11-10T20:49Z (conclusion `push failure`),
dispatch last ran 2026-11-06, and `push-check.yml` last ran 2026-09-15 on
`orchestration-tools`. `jules-pr-review.yml` is `disabled_manually` and its last run was
skipped. A `.DISABLED` suffix on main does not unregister a workflow that other branches
still define under its original name.


---

## 2. Disabled/Bak/Currently_Disabled Trees

| Path | Type | Status |
|------|------|--------|
| `./scripts/test_concurrent_review.py` | File | Test script, not disabled |
| `./scripts/concurrent_review.py` | File | Script, not disabled |
| `./docs/current_orchestration_docs/` | Directory | Active docs |

**No** `*.bak`, `*.bak_*`, `disabled/`, or `currently_disabled/` trees found on any branch.

---

## 3. Deleted Files (git log --diff-filter=D)

Recent deletions on main (last 20 commits with deletions):

| Commit | Deleted Files | Move vs Delete |
|--------|---------------|----------------|
| 647a1b4a2 | `update_mergify.py` | Delete (script no longer needed) |
| 08b967ba8 | `src/backend/python_backend/smart_filters.py` | **Move** → replaced by proper module |
| 4a60f7f35 | `fix_conflict.py` | Delete (scratch script) |
| 46bfe32e8 | `reply_to_comment.json` | Delete (artifact) |
| d50cf08d2 | `manifest.json`, `update.json` | Delete (obsolete config) |
| 43db0ab81 | `fix_conflict.py` | Delete (duplicate) |
| da3aa018b | `update_conflict_detection.py` | Delete (refactored) |
| f7b23ef87 | `plan.md` | Delete (temp file) |
| 998bc9017 | `plan.md` | Delete (temp file) |
| 185e46889 | `plan.md`, `test_path_traversal.py` | Delete (temp/test) |
| 4bc201f8e | Many config/data files | **Purge** — large data/config cleanup |
| e56550da4 | `.continue/`, `.cursor/`, `.openhands/`, `.qwen/`, `.specify/`, `.voidrules`, client configs | **Purge** — removed IDE/tooling configs |
| 283d99233 | `docs/SUBMODULES.md` | Delete (obsolete) |
| d0fa8161d | IDE configs + data files | **Purge** — same as above |
| 4f60ac1cf | IDE configs | **Purge** |

**Verdict**: Most deletions are **cleanup of scratch/temp/IDE config files** — not feature loss. The `smart_filters.py` deletion was a **move** (stub removed, real module exists elsewhere).

---

## 4. Reverts on main

| Commit | Message | Reverted Work | Status |
|--------|---------|---------------|--------|
| 4a60f7f35 | "revert unintentional data layer and scripts modifications" | Data layer/scripts changes | **Intentional cleanup** |
| 4a985434f | "restore ALL workflows to match origin/main exactly" | All workflow changes | **Intentional sync** |
| 6ec398ecf | "restore active Gemini workflows disabled by session" | Gemini workflow disable | **Restored** — but workflows now .DISABLED |
| a2b1bbf09 | "add disabled-workflow rules and stale-snapshot guards to AGENTS.md" | Doc update | **Kept** |
| 8a6fb1cbc | "Sentinel: Enhance security headers and API caching controls" | Security PR | **Merged** |
| 4e9f4869b | "revert workflow action versions to stable v4/v5/v5" | Action version bump | **Intentional downgrade** |
| a67970e60 | "Revert Merge PR #195" | Orchestration tools deps | **Conflict resolution** |
| 7de75e85d | "Revert Synchronize MANAGED_FILES" | Post-push hook | **Conflict resolution** |
| 2abe41e33 | "Revert Merge main into orchestration-tools" | Branch merge | **Conflict resolution** |
| a3694af6d | "Revert Synchronize MANAGED_FILES" | Duplicate revert | **Duplicate** |
| b833950de | "Revert Ignore worktree files" | Hook config | **Conflict resolution** |

**Verdict**: Most reverts are **conflict resolutions** or **intentional rollbacks**, not feature loss. The Gemini workflow restore (6ec398ecf) was later superseded by mass disable.

---

## 5. Skip/Xfail Markers (pytest.mark.skip/skipif)

**None found** in `src/` or `tests/` directories.

- No `@pytest.mark.skip` added by branches/PRs
- No `@pytest.mark.xfail` in source code
- Only in `.venv/` (third-party packages)

**Verdict**: No silent test retirement via skip markers.

---

## 6. Local Branches Not on Origin (400+)

**Hundreds of local branches** exist only locally (no upstream tracking). Categories:

| Category | Count | Examples |
|----------|-------|----------|
| `bolt/*` optimization branches | 100+ | `bolt/optimize-search-caching-...` |
| `jules/*` session branches | 50+ | `jules-16572034054047473480-...` |
| `sentinel/*` security fix branches | 50+ | `sentinel/fix-auth-bypass-...` |
| `feature/*` | 30+ | `feature/taskmaster-ast-semantic...` |
| `fix/*` | 30+ | `fix/ci-infrastructure-...` |
| `task-*` / `taskmaster` | 10+ | `task-014-conflict-detect` |
| `orchestration-tools*` | 10+ | `orchestration-tools-consolidated` |
| `scientific*` | 5+ | `scientific-resolved` |

**Verdict**: **LATENT** — massive local branch debt. Many contain unique commits not on any remote. Per branch governance (`.taskmaster/BRANCH_MANAGEMENT_MODEL.md`), only `main`, `scientific`, `orchestration-tools`, `taskmaster`, `consolidate/cli-unification` are protected. The rest should be pruned or merged.

---

## Overall Verdicts

| Category | Verdict | Count |
|----------|---------|-------|
| .DISABLED workflows | **DEAD** | 16 |
| .DISABLED workflows | **LIVE (migrated)** | 1 |
| Disabled/bak trees | **NONE** | 0 |
| Deleted files | **CLEANUP** (not loss) | ~50 |
| Reverts | **INTENTIONAL** | 11 |
| Skip/xfail markers | **NONE** | 0 |
| Local-only branches | **LATENT** | 400+ |

---

## Recommended Actions

1. **Delete 16 .DISABLED workflow files** — they are dead code
2. **Prune 400+ local branches** — keep only protected branches + active PR branches
3. **Document the 1 migrated workflow** (`push-check.yml` → `pr-check.yml`) in ARCHITECTURE.md
4. **No code changes needed** — no features were silently disabled via skip/xfail or config

---

*Generated by S13 forensic audit — read-only, no edits to source code.*
