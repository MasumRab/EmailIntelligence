# Jules Actions Traceability: EmailIntelligence

Date: 2026-07-25 (updated from 2026-07-21, originally 2026-07-08)
Repo: `MasumRab/EmailIntelligence`
Status: **workflows installed and active** (8-workflow stack deployed).

## Existing local evidence

Relevant existing files found locally:

- `JULES_ACTION_REPORT.md` — session/action report, not a GitHub Actions setup plan.
- `docs/JULES_OPERATIONS.md` — Jules REST/session operations.
- `.jules/session_analysis/` — retrieved session data and workflow definitions.
- `jules_sessions/README.md` and `scripts/jules_sync_all.sh` — session archive/sync support.
- `skills/jules-*.skill` — local Jules API/CLI/scheduling/session/workflow skills (archived `.skill` zips; live skills in `~/.letta/skills/` and `~/.agents/skills/`).
- `.github/BRANCH_PROPAGATION_POLICY.md`, `.github/PROPAGATION_SETUP_CHECKLIST.md` on relevant remote branches — branch ownership/contamination rules that should feed Jules review rules.

## Suitability assessment

EmailIntelligence is the strongest fit for the full Jules Actions stack because it has:

- a large PR/branch backlog,
- stale and overlapping branches,
- separate `main`, `scientific`, `orchestration-tools`, and `taskmaster` concerns,
- multiple competing CLI/tool integration branches,
- existing Jules session history that should be linked back to PRs.

## Installed Jules Actions workflows

All 8 workflows are deployed in `.github/workflows/`:

| Workflow file | Trigger | Session type | Purpose |
|---|---|---|---|
| `jules-pr-review.yml` | `pull_request` (auto) | Analytical | Automatic PR review on every PR. Posts review comment + `jules/review` status. |
| `jules-pr-force-review.yml` | `jules-force-review` label / `/jules-force-review` slash | Analytical | Manual re-review on demand. Same logic as auto-review. |
| `jules-pr-walkthrough.yml` | `jules-walkthrough` label / `/jules-walkthrough` slash | Analytical | Narrative walkthrough comment for PR understanding. |
| `jules-pr-auto-fix.yml` | `jules-fix` label / `/jules-fix` slash | Mutating | Creates session, pushes repair commit to PR branch. |
| `jules-pr-resolve-conflicts.yml` | `jules-resolve` label / `/jules-resolve` slash | Mutating | Resolves merge conflicts and pushes to PR branch. |
| `jules-pr-rebuild.yml` | `jules-rebuild` label / `/jules-rebuild` slash | 2 sessions (analysis + rebuild) | Cleans messy PRs in-place: analysis session identifies valuable vs noise, rebuild session cleans up. |
| `jules-pr-address-comments.yml` | `pull_request_review_comment` (auto) | No session | Posts `@jules` comment with unresolved review thread context. Only on Jules-authored PRs. |
| `jules-pr-automerge-label.yml` | Hourly cron | No session | Labels Jules-created PRs with `automerge`. Relies on Mergify (`.mergify.yml`) to complete the merge. |

## Auto-merge configuration

This repo uses **Mergify** (`.mergify.yml`) for auto-merge. The `automerge` label is consumed by a Mergify rule that merges when CI passes.

## Review rules to encode

Seed `.github/jules-review-rules.md` with these project-specific rules:

- `main` owns application/distribution code.
- `orchestration-tools` owns hooks, validation scripts, setup/orchestration infra, and internal orchestration docs.
- `scientific` may receive compatible application changes but must not receive a wholesale orchestration-tools merge.
- `taskmaster` is planning/process context; do not distribute internal state unless explicitly approved.
- Do not introduce new competing CLI entry points.
- Prefer canonical public CLI direction: `eai`.
- Treat `dev.py` as orchestration/developer tooling unless a final alignment doc says otherwise.
- Treat shell scripts as low-level implementation details unless the change is explicitly orchestration-only.
- Review stale PRs for: mergeability, rebase path, branch contamination, CLI conflicts, test risk, and close-candidate status.

## Backlog review output contract

A Jules backlog review comment should use this compact shape:

```md
## Jules Backlog Review

Status: mergeable | needs-small-fixes | needs-rebase | stale-salvageable | close-candidate | blocked

Summary:
...

Branch / CLI / orchestration risk:
...

Blocking issues:
...

Suggested next action:
...

Existing Jules session found: yes/no
```

## Safeguards

- Use `pull_request`, not `pull_request_target`, for Jules review.
- Skip forks by default.
- Use `fail_on: blocking` rather than `any` (applies to third-party `jules-pr-reviewer` action only; custom self-hosted workflows use commit statuses).
- Feedback allowlist not needed: the address-comments workflow only triggers on Jules-authored PRs, so Jules-author ownership is the complete safeguard. No `feedback_users` allowlist is required.
- Label/manual-gate Jules Invoke.
- Do not run destructive branch sync, stash mutation, hook toggles, or auto-resolution commands unless explicitly requested.

## Implementation status

All 8 workflows are installed and active. The `JULES_API_KEY` secret is configured. Mergify handles auto-merge for the `automerge` label.

## Resolved questions

- **Which branch should own the GitHub Actions rollout?** — `main` owns the workflow files.
- **Should backlog sweep review all open PRs or only those with a `jules-backlog` label?** — Not yet implemented; backlog sweep is a future enhancement.
- **Which users are allowed in `feedback_users`?** — The address-comments workflow skips non-Jules PRs; feedback allowlist is not needed.
- **Should branch protection require `jules/review` immediately or start advisory-only?** — Currently advisory; `jules/review` status is posted but not required by branch protection.
