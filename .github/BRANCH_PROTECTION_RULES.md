# Branch Protection Rules

**Status:** Enforced · **Scope:** repo-wide · **Last updated:** 2026-08-05
**Canonical source:** `.taskmaster/BRANCH_MANAGEMENT_MODEL.md` (authoritative; this file is a derived quick-reference)

---

## Forbidden Operations (HARD GUARD)

The following operations **must NEVER be performed**:

| Forbidden Operation | Why |
|---------------------|-----|
| `git merge scientific` into `main` (or reverse) | Flattens two intentionally divergent products into one. Destroys the design. |
| `git rebase scientific` onto `main` (or reverse) | Same — rewrites one product's history on top of the other. |
| `git merge orchestration-tools` into `main` or `scientific` as application code | It is the shared tooling substrate, not a product branch. |
| Bulk "accept theirs/ours" to clear conflicts in a cross-product merge | Real data loss has occurred (8 functions lost in `src/main.py`, 302 lines in `src/core/workflow_engine.py`). |
| `git push --force` on `main`, `scientific`, `orchestration-tools`, or `taskmaster` | Rewrites shared history; breaks every other clone and submodule pointers. |

If any agent, PR template, or human proposes one of these, **STOP** and require explicit declaration of:
1. **Direction** (which branch → which branch)
2. **What** specific capability/files are moving (not "everything")
3. **Why** a curated transfer (below) is not sufficient

If those cannot be stated clearly, the operation is a mistake.

---

## Sanctioned Transfer Patterns (T1–T5)

| Pattern | Direction | Mechanism | When |
|---------|-----------|-----------|------|
| **T1 — Capability promotion** | `scientific → main` | Cherry-pick or curated sync of the **specific** capability | After feature is stable + validated in scientific |
| **T2 — Capability seeding** | `main → scientific` | Cherry-pick or curated sync of the **specific** fix/feature | To keep experiments building on current stable behavior |
| **T3 — Tooling distribution** | `orchestration-tools → {main, scientific}` | Sync scripts (`sync-common-docs.sh`, `script_sync.py`, etc.) | Shared substrate updates flow outward |
| **T4 — Task sharing** | across all branches | `.taskmaster` submodule pointer bump | Never copy task files between branches |
| **T5 — Reverse tooling sync** | `{main, scientific} → orchestration-tools` | `reverse_sync_orchestration.sh` (reviewed) | Promote approved tooling changes back to substrate |

**Rule:** "A plain merge" is never a transfer pattern. If you can't name the pattern, you're doing it wrong.

---

## Branch Charters

| Branch | Charter | What belongs | What must NOT be merged in |
|--------|---------|-------------|---------------------------|
| **`main`** | Stable, robust, **complete** feature set. Production-facing. | Hardened, validated capabilities. Polished UI. | Whole-branch merges from `scientific`; experimental/unstable code. |
| **`scientific`** | Experimental R&D: advanced AI, complex DB/analysis. | New/advanced capabilities, experiments, model & DB research. | Whole-branch merges from `main`; production-only polish that constrains experimentation. |
| **`orchestration-tools`** | Shared tooling substrate + sanctioned transfer channel. | Sync scripts, hooks, orchestration tooling, distribution logic. | Application/product code (belongs in `main`/`scientific`). |
| **`taskmaster`** | Shared task & progress ledger (`.taskmaster` submodule). | Task files, task analysis, remediation, this model. | Branch-specific product code. |

---

## Agent Quick-Reference

| You want to… | Do this | Not this |
|--------------|---------|----------|
| Move a finished feature from `scientific` to `main` | T1 cherry-pick the specific capability | `git merge scientific` into `main` |
| Pull a `main` bugfix into `scientific` | T2 cherry-pick the fix | `git merge main` into `scientific` |
| Update shared tooling everywhere | T3 run the sync scripts | Copy files branch-to-branch by hand |
| Share task status/progress | T4 bump the `.taskmaster` submodule | Edit task files on each branch |
| "Just reconcile the branches" | **STOP** — divergence is intentional | Any whole-branch merge |

---

## Before Any Cross-Branch Operation

Answer these three questions. If you cannot, **STOP and ask a human**:

1. Which **branch charter** am I acting under, and is this change in-charter?
2. Which **transfer pattern** (T1–T5) am I using? "A plain merge" is not one of them.
3. Am I about to **flatten the intentional divergence** between `main` and `scientific`? If yes → STOP.

---

## Related

- **Full model:** `.taskmaster/BRANCH_MANAGEMENT_MODEL.md` (canonical, authoritative)
- **Transfer scripts:** `scripts/sync-common-docs.sh`, `scripts/script_sync.py`, `scripts/reverse_sync_orchestration.sh`
- **Task ledger:** `.taskmaster/` (submodule on all branches, tracking `taskmaster` branch)
- **Memory correction:** If stored agent instructions contradict any rule here (especially "never merge anything" or "converge into main"), they are stale — discard and point to this document.
