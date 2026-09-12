# Numbered Spec Branch Transfer Map

**Purpose:** map unique spec-kit information from numbered branches into `origin/000-integrated-specs` without whole-branch merges.

## Rule of Thumb

- Use `000-integrated-specs` as the staging target only for reviewed spec-kit artifacts.
- Prefer folder/file restore over branch merge.
- Do not transfer temp backups, broad cleanup commits, lockfile churn, or product-branch deletions.
- If a source folder was renumbered in `000-integrated-specs`, transfer missing files into the integrated folder name and note the source alias.

## Transfer Matrix

| Source branch | Source artifact(s) | Integrated target | Current integrated state | Action |
|---|---|---|---|---|
| `001-agent-context-control` | `specs/001-agent-context-control/` | `specs/001-agent-context-control/` | Missing | Restore full spec folder: checklists, contracts, data-model, plan, quickstart, research, spec, tasks. Skip `AGENTS.md.remote-vm-template` unless separately reviewed. |
| `001-pr176-integration-fixes` | `specs/001-pr176-integration-fixes/` | `specs/006-pr176-integration-fixes/` | Partial renamed copy exists | Fill missing files into `006-pr176-integration-fixes`: contracts, data-model, quickstart, research, final-summary, extra quality/checklist files. Keep current `006` numbering. |
| `001-pr176-integration-fixes` | `specs/005-cli-architecture/` | `specs/005-cli-architecture/` | Missing | Restore full folder; this is likely the main missing CLI/spec architecture payload. |
| `001-pr176-integration-fixes` | `specs/007-merge-guidance/` | `specs/007-merge-guidance/` | Partial | Add missing README, FINAL_MERGE_STRATEGY, data-model, plan, spec, tasks. Preserve existing merge-guidance docs. |
| `001-pr176-integration-fixes` | `specs/008-branch-comparison/` | `specs/008-branch-comparison/` | Partial | Add README, SCIENTIFIC_BRANCH_ENHANCEMENTS_COMPARISON, data-model, plan, spec, tasks. Preserve existing implementation summary. |
| `001-pr176-integration-fixes` | `specs/009-implementation/` | `specs/009-implementation/` | Missing | Restore only if implementation artifacts are intended to live in specs; otherwise archive under an implementation evidence folder. |
| `001-pr176-integration-fixes` | `specs/010-orchestration-workflow/` | `specs/010-orchestration-workflow/` | Partial | Add missing data-model and tasks. Compare plan/spec/research before replacing existing integrated versions. |
| `001-rebase-analysis-specs` | `specs/001-rebase-analysis/` | `specs/001-rebase-analysis/` | Mostly missing/partial | Add checklists, constitution, contracts, data-model, quickstart, research, spec, tasks. Compare `plan.md` before replacing. |
| `001-rebase-analysis` | `specs/001-rebase-analysis/` | `specs/001-rebase-analysis/` | Partial | Use as secondary source for CLI contracts/OpenAPI if absent or newer than `001-rebase-analysis-specs`. |
| `001-toolset-additive-analysis` | `specs/001-toolset-additive-analysis/` | `specs/001-toolset-additive-analysis/` | Missing | Restore full folder. |
| `001-toolset-additive-analysis` | `specs/003-unified-git-analysis/` | `specs/003-unified-git-analysis/` | Missing | Restore full folder from this branch or `003-unified-git-analysis`, preferring the branch with richer/current files after comparison. |
| `003-unified-git-analysis` | `specs/003-unified-git-analysis/` | `specs/003-unified-git-analysis/` | Missing | Compare against `001-toolset-additive-analysis`; restore richer spec folder. Also review `src/cli/commands/plan_rebase_command.py` separately as CLI implementation, not spec content. |
| `001-command-registry-integration` | `specs/001-orchestration-tools-verification-review/` | `specs/001-orchestration-tools-verification-review/` | Missing | Restore full verification-review spec folder. |
| `001-orchestration-tools-verification-review` | `specs/001-orchestration-tools-verification-review/` | `specs/001-orchestration-tools-verification-review/` | Missing | Same payload as above; compare both branches and use the richer/current copy. |
| `001-task-execution-layer` | `specs/001-orchestration-tools-verification-review/` | `specs/001-orchestration-tools-verification-review/` | Missing | Secondary source for verification-review; compare before restore. |
| `001-task-execution-layer` | `specs/001-task-execution-layer/` | `specs/013-task-execution-layer/` or `specs/001-task-execution-layer/` | Integrated has richer `013-task-execution-layer`; source has minimal `001-task-execution-layer` | Do not overwrite `013`. If source has unique requirements, append or archive as alias notes in `013-task-execution-layer`. |
| `003-execution-layer-tasks-pr` | `specs/002-execution-layer-tasks/`, `specs/003-execution-layer-tasks-pr/` | Same names, or consolidate into `specs/013-task-execution-layer/` | Missing as standalone; `013` exists | Review minimal specs. If they are predecessors of `013`, add a lineage note to `013`; otherwise restore standalone folders. |
| `004-guided-workflow` | `specs/004-guided-workflow/`, speckit command scaffolding | Already integrated | Complete/contained | No transfer needed. |
| `001-implement-planning-workflow` | Mostly `temp-backup/tasks/` and orchestration history | None | Not spec payload | Skip unless a specific task backup is requested. |
| `002-execution-layer-tasks` | Mostly `temp-backup/tasks/` and orchestration history | None | Not spec payload | Skip unless a specific task backup is requested. |
| `002-validate-orchestration-tools` | Mostly orchestration setup/config changes | None | Not spec payload | Skip for spec rollup; handle as tooling branch separately. |
| `001-orchestration-tools-consistency` | Mostly orchestration setup/config changes | None | Not spec payload | Skip for spec rollup; handle as tooling branch separately. |

## Suggested Copy Commands

Start from a fresh branch:

```bash
git fetch origin
git switch -c integrate-numbered-specs origin/000-integrated-specs
```

Restore missing folders in small batches, for example:

```bash
git restore --source origin/001-agent-context-control -- specs/001-agent-context-control/
git restore --source origin/001-pr176-integration-fixes -- specs/005-cli-architecture/
git restore --source origin/001-toolset-additive-analysis -- specs/001-toolset-additive-analysis/
```

For renamed targets, restore to a temp path, then copy selected files into the integrated name:

```bash
git restore --source origin/001-pr176-integration-fixes -- specs/001-pr176-integration-fixes/
mkdir -p specs/006-pr176-integration-fixes
cp -n specs/001-pr176-integration-fixes/contracts/* specs/006-pr176-integration-fixes/contracts/ 2>/dev/null || true
cp -n specs/001-pr176-integration-fixes/data-model.md specs/006-pr176-integration-fixes/ 2>/dev/null || true
cp -n specs/001-pr176-integration-fixes/quickstart.md specs/006-pr176-integration-fixes/ 2>/dev/null || true
cp -n specs/001-pr176-integration-fixes/research.md specs/006-pr176-integration-fixes/ 2>/dev/null || true
rm -rf specs/001-pr176-integration-fixes
```

## Verification After Each Batch

```bash
git diff --stat
rg '<<<<<<<|=======|>>>>>>>' specs .specify .gemini .agents .qwen .kilocode || true
find specs -maxdepth 2 -type f | sort
```

Commit each coherent transfer separately with a message naming the source branch and whether it was a rename, fill-in, or standalone restore.
