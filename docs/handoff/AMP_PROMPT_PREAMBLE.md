# AMP Prompt Preamble — Completion + Token Efficiency Contract

**Purpose:** Canonical block to prepend to every `amp threads new --execute "..."` prompt across the handoff workflow.
**Scope:** Large, unstructured, multi-phase tasks (Phases 0–14, gate checks, error recovery, review).
**Updated:** 2026-04-28

---

## How to use

Every amp prompt in `docs/handoff/AMP_*.md` and `commands/workflows/*.toml` MUST start with the directive block below (verbatim or by reference). When invoking via CLI, prepend the block; when invoking from a TOML prompt, include `{{PREAMBLE}}` and substitute at render time.

---

## The Preamble (verbatim)

```text
# === AMP COMPLETION + TOKEN-EFFICIENCY CONTRACT ===
# Read once. Apply throughout this thread.

## Completion contract (do not stop early)
1. Persist until the user's stated goal is fully done end-to-end:
   implement → verify → report. Do not stop at analysis or partial fixes.
2. If a step is blocked, resolve it yourself before asking the user.
   Only escalate after exhausting available tools and documenting the
   attempts in the execution journal.
3. Mark a phase "done" ONLY after its acceptance criteria pass and
   STATE_<branch>.md is updated. Never claim done without verification.
4. If the task is unstructured, decompose it into a numbered checklist
   in your first message; check off each item as you complete it.

## Token-efficiency rules (large unstructured tasks)
T1. NEVER read entire files when a range or grep will do.
    Prefer: rg / ast-grep / serena symbol tools / Read with read_range.
T2. Use Task subagents for INDEPENDENT fan-out work (frontend/backend/
    docs). Each subagent loses context, so put the plan + paths in its
    prompt. Do NOT spawn a subagent for single-file edits.
T3. Prefer summary outputs over raw dumps:
    - run `wc -l` / `head` / `tail` before `cat`
    - pipe through `head -<N>` for greps that may be large
    - emit diffs, not full file contents, in status reports.
T4. Cache discovery once; do not re-list directories or re-read AGENTS.md
    files repeatedly within the same thread.
T5. For multi-branch work: source `docs/handoff/context-guard.sh` once;
    reuse $PROJECT_ROOT and $CURRENT_BRANCH instead of re-detecting.
T6. Skip the oracle for mechanical tasks. Use it only for
    architecture-level decisions or when stuck after 2 failed attempts.
T7. Skip librarian for local repo work. Local code → ck/serena/Grep.
T8. When summarising for the user, target ≤ 4 lines of prose unless
    asked for detail. Tables and bullet lists count as structured data,
    not prose, and are preferred for status reports.
T9. Tool-call batching: issue independent reads/searches in parallel
    inside a single response. Sequential calls only when there is a
    real data dependency.
T10. Stop generating prose when the work is done. No filler,
     no recap of what was already shown in tool output.

## Context-agnostic requirements (any branch, any CWD)
C1. Source `docs/handoff/context-guard.sh` at thread start.
C2. Reference `$PROJECT_ROOT` for absolute paths; never `cd`.
C3. Read STATE_${CURRENT_BRANCH}.md before deciding the next step;
    create from STATE_TEMPLATE.md if missing.
C4. Log non-trivial decisions via `docs/handoff/execution-journal.sh`.

## Verification gates
V1. Run `bash scripts/verify-agent-content.sh` after content changes.
V2. Run `bash docs/handoff/context-agnostic-gates.sh` between phases.
V3. For .gitignore work, run
    `bash scripts/apply-unified-gitignore.sh --audit` before --apply.
V4. Never `git push --force`, `git reset --hard`, or `--no-verify`.

## Failure handling
F1. On any tool error: read the error, check assumptions, try a focused
    fix. Don't retry identical commands; don't abandon viable approaches
    after one failure.
F2. If three consecutive attempts on the same problem fail, log to the
    journal and consult oracle with the failing files attached.

# === END CONTRACT ===
```

---

## Reference table — which prompts include the preamble

| Artifact | Inclusion mode |
|---|---|
| `docs/handoff/AMP_CLI_COMMANDS.md` | Prepend block above each `amp threads new` invocation |
| `docs/handoff/AMP_COMMANDS.md` | Linked at top; each phase command refers back |
| `docs/handoff/AMP_RUSH_SESSION_CREATION.md` | Prepend before any `--mode rush` execute string |
| `docs/handoff/phase-12-deep-agent-handoff.md` | Already implicit; add explicit reference |
| `docs/handoff/phase-13-smart-amp-deep-agent-autonomous-handoff.md` | Add explicit reference |
| `docs/handoff/phase-14-gitignore-unification.md` | Add explicit reference |
| `commands/workflows/start-handoff.toml` | `{{PREAMBLE}}` substitution |

---

## Rationale (why this exists)

Prior amp prompts in this repo are 50–300 lines each, repeat boilerplate, and lack explicit completion + token guards. For large unstructured handoff tasks (e.g. running 14 phases across 4+ branches), the preamble:

1. Eliminates per-prompt drift on completion semantics.
2. Sets explicit token rules so agents don't burn context on whole-file reads.
3. Makes the workflow context-agnostic by contract, not just convention.
4. Centralises one place to update — change here, propagate everywhere.
