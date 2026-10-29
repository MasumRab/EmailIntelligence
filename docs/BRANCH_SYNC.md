# Branch Sync Architecture

**Last updated:** 2026-06-26
**Maintained on:** `main` until the branch-sync policy is copied/cherry-picked to the branch that owns orchestration documentation
**Referenced from:** `AGENTS.md`

## Intended Architecture

| Branch | Purpose | Should Contain | Should NOT Contain |
|---|---|---|---|
| `main` | Application code | `src/core/`, `modules/`, `setup/`, `client/`, `backend/`, `tests/`, `.github/workflows/` | Orchestration scripts, agent configs, NLP models |
| `scientific` | Application + research | Everything in `main` + `models/`, NLP-specific modules, research features | Orchestration scripts, agent configs |
| `orchestration-tools` | Shared orchestration tooling | `scripts/`, `setup/`, selected `docs/`, lint/config files, git hooks, agent/tool configs, and reviewed CLI/orchestration support modules | Product application modules, product data files, NLP models |

### Sync Flow

```
orchestration-tools (shared orchestration/tooling source)
    ↓ reviewed copy / cherry-pick / sync scripts for managed files
main (application baseline) ←→ scientific (application + research)

taskmaster branch (submodule, orphan history)
    ↕ pinned as .taskmaster gitlink in parent branches
```

- `orchestration-tools` is the reviewed source for shared orchestration/tooling files. Current scripts implement manual or hook-assisted copy/cherry-pick flows, not guaranteed automatic remote propagation.
- `main` and `scientific` share application code; `scientific` adds NLP/research scope on top.
- `taskmaster` is a separate submodule branch with unrelated/orphan history. Parent branches should update only the `.taskmaster` gitlink when taking Taskmaster changes.
- Avoid whole-branch merges between these long-diverged branches unless a branch-specific integration plan says otherwise; prefer file-scoped cherry-picks or scripted sync for managed files.

## Current Drift Status

### Last Cross-Branch Merges

| Merge | Date | Gap |
|---|---|---|
| main → scientific | Nov 1, 2025 | **7 months** |
| main → orchestration-tools | Nov 8, 2025 | **7 months** |
| scientific → orchestration-tools | Oct 27, 2025 | **7+ months** |

No cross-branch merges in the last 30 days.

### Divergence Metrics (as of 2026-06-26)

| Metric | main ↔ scientific | main ↔ orchestration-tools |
|---|---|---|
| Commits branch is ahead of `main` | 1,404 | 817 |
| Commits branch is behind `main` | 18 | 41 |
| `.taskmaster` gitlink | `9eaea69f` | `9eaea69f` |
| `.gitmodules` branch | `taskmaster` | `taskmaster` |

`main` currently pins `.taskmaster` to `a81f3119`.

### Known Drift Issues

| Issue | Branches | Severity | Notes |
|---|---|---|---|
| `src/cli/commands/` deleted | scientific | CRITICAL | 8 CLI command files missing |
| `src/context_control/` deleted | scientific | CRITICAL | 12+ context control files missing |
| `modules/new_ui/` deleted | both | HIGH | 6 new UI files missing |
| `modules/auth/`, `dashboard/`, `email/` etc. deleted | orchestration-tools | HIGH | 35 module files missing (expected per scope) |
| `src/backend/data/` deleted | orchestration-tools | MEDIUM | Data files missing |
| CI workflows diverged | both | MEDIUM | Branch-specific workflows are allowed, but shared checkout/submodule behavior should stay aligned. `deploy-staging.yml` currently lacks `submodules: recursive`. |
| `src/` content present | orchestration-tools | REVIEW | Historical `validate-orchestration-context.sh` treats all `src/` as contamination, but newer CLI/orchestration branches use selected `src/cli`, `src/analysis`, `src/git`, `src/core`, and `src/resolution` modules. Resolve by replacing blanket path rules with an allowlist/denylist. |

### Justifiable Differences

| Difference | Branch | Justification |
|---|---|---|
| `models/` (topic model, tokenizer, vocab) | scientific | NLP research models — scientific-only |
| `src/analysis/`, `src/git/`, `src/resolution/`, selected `src/core/` and `src/cli/` | orchestration-tools | Shared CLI/orchestration support modules when reviewed as tooling, not product app code |
| `.agents/`, `.claude/`, `.cline/`, `.codex/`, `.cursor/` | orchestration-tools | Agent configs — correct home |
| `modules/*.sh` (branch.sh, config.sh, safety.sh) | orchestration-tools | Orchestration shell scripts — correct home |

## Sync Rules

### Must Stay Aligned Across main ↔ scientific

- `src/core/` — shared engine code
- `src/backend/python_backend/` — shared API backend
- `modules/auth/`, `modules/email/`, `modules/dashboard/` — shared app modules
- `setup/` — shared launch and config
- Shared `.github/workflows/` behavior — especially checkout, submodule, test, and security gates. Branch-specific workflows may differ when documented.
- `.gitignore`, `.gitattributes` — repo config

### Managed from orchestration-tools → main/scientific

- `setup/launch.py`, `setup/launch.sh` — shared launcher
- `setup/pyproject.toml`, `setup/requirements*.txt` — shared deps
- Reviewed orchestration scripts such as `sync_setup_worktrees.sh`, `reverse_sync_orchestration.sh`, and validation/context scripts
- `.flake8`, `.pylintrc`, `.pre-commit-config.yaml` — lint configs
- Shared CI behavior and reusable workflow patterns. Branch-specific workflows may differ when documented.

### Allowed to Drift

- `models/` — scientific-only NLP models
- Reviewed CLI/orchestration support modules under `src/cli/`, `src/analysis/`, `src/git/`, `src/resolution/`, and selected `src/core/` — orchestration/tooling scope only
- Agent config directories (`.agents/`, `.claude/`, etc.) — orchestration-tools-only
- Branch-specific docs and reports

## Outstanding Task List

1. **Fix shared CI checkout/submodule behavior.** Add `submodules: recursive` to any active `actions/checkout` step that must see `.taskmaster`, starting with `.github/workflows/deploy-staging.yml` on `main` and `scientific`. Decide separately whether pinned checkout actions such as `gemini-review.yml` need submodules.

2. **Align `.taskmaster` pins across active branches.** `main` pins `.taskmaster` to `a81f3119`, while `scientific` and `orchestration-tools` still pin `9eaea69f`. Update the latter branches if they should share the completed remediation/doc-map work.

3. **Publish this branch-sync policy to its intended home.** This file was created locally on `main`, while the policy says orchestration docs are maintained on `orchestration-tools`. Commit it where it will be authoritative, then copy/sync it to branches that reference it.

4. **Resolve branch-sync documentation freshness.** Refresh merge dates and divergence metrics before treating this document as current. The existing metrics are from 2026-06-08 and are stale after the June dependency and submodule work.

5. **Fix orchestration context validation policy.** `scripts/validate-orchestration-context.sh` currently flags all `src/` as contamination, which conflicts with implemented CLI/orchestration support modules. Replace that blanket rule with an allowlist for tooling modules and a denylist for product app modules (`client/`, product `modules/`, data/model directories, etc.).

6. **Close Task 015 identity conflict in `.taskmaster`.** Choose one outcome from `.taskmaster/REMEDIATION_PLAN.md`: keep Task 015 as validation and move orchestration content into/near Task 012, or explicitly split the task. Do not edit `tasks.json` manually.

7. **Reassign misplaced Task 007 subtasks.** Move error-detection subtasks toward Task 005 and migration-analysis content toward Task 022, then write replacement subtasks for branch identification/categorization.

8. **Resolve backup/safety and validation overlap boundaries.** Define Task 006 vs 013 and Task 011 vs 017 boundaries before changing dependencies. Prefer keeping distinct tasks only when each has an exclusive responsibility.

9. **Create validation layer boundary documentation.** Define the ownership chain for Tasks 003 → 008 → 011 → 017 so new validation checks have one clear home.

10. **Reconnect the task dependency graph after decisions.** Apply Phase C from `.taskmaster/REMEDIATION_PLAN.md`: reconnect Task 002, Task 001, validation chain dependencies, and collapse the fake sequential tail for Tasks 019–025.

11. **Run Task Master sync only after Markdown task edits.** For `.taskmaster/tasks/*.md`, follow the submodule AGENTS rule: edit Markdown first, then run `python taskmaster_cli.py parse-prd --input tasks/` or the repo-approved equivalent. Do not manually edit `tasks.json`.

12. **Verify outstanding tool setup items outside this repo only if still needed.** `hermes-hud` runtime verification and Fabric/OpenRouter live-call verification were left open in a home-directory mise thread; they are not branch-sync blockers.

## Resolved Contradictions

1. **“No `src/` on orchestration-tools” vs implemented CLI/orchestration modules under `src/`.** Resolution: blanket `src/` bans are wrong. Tooling modules under `src/cli`, `src/analysis`, `src/git`, `src/resolution`, and selected `src/core` may be valid after review; product application modules remain out of scope.

2. **“All `.github/workflows/` must stay aligned” vs branch-specific CI needs.** Resolution: shared CI behavior must align, but branch-specific workflows may differ when documented.

3. **“All parent branches pin the same `.taskmaster` commit” vs current branch state.** Resolution: treat equal pins as the target state, not the current state, until `scientific` and `orchestration-tools` are updated.

4. **Task 015 validation title vs orchestration subtasks.** Resolution: unresolved by policy; it is an explicit decision task and must be settled before dependency rewiring.

## Update Process

When making changes that affect branch alignment:
1. Update the drift status table above
2. Update the last merge dates if a merge occurs
3. Add new justifiable differences if intentional drift is introduced
4. Run `git diff --stat origin/main origin/scientific -- src/ modules/ setup/ .github/` to refresh metrics
