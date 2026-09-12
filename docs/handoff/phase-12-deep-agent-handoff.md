# Phase 12: Deep Agent Handoff for Corrected Phase 5/6/9 Execution

## Purpose

This document is a ready-to-run deep-agent handoff for completing the corrected:

- Phase 5: File Cleanup
- Phase 6: Deduplication
- Phase 9: Verification

It is designed for use on the `orchestration-tools` branch after Phases 1-4 were completed and after the handoff plan itself was corrected to use a Tier 1 shared-content / Tier 2 root-file model.

This handoff is intentionally strict. It assumes the next agent must preserve meaningful tool-specific behavior, avoid destructive git operations, and update [docs/handoff/STATE.md](file:///home/masum/github/EmailIntelligenceAider/docs/handoff/STATE.md) as the authoritative execution log.

If the goal is broader autonomous completion across all remaining relevant phases with explicit prior-thread ingestion and off-root archive evidence, use [Phase 13](file:///home/masum/github/EmailIntelligenceAider/docs/handoff/phase-13-smart-amp-deep-agent-autonomous-handoff.md) instead.

---

## Verified Live State at Handoff Creation

These facts were verified live on this branch before writing this handoff.

- Repository: `/home/masum/github/EmailIntelligenceAider`
- Branch: `orchestration-tools`
- [docs/handoff/STATE.md](file:///home/masum/github/EmailIntelligenceAider/docs/handoff/STATE.md) shows Phases 1-4 complete and Phase 5 pending.
- Root Tier 2 file state at time of handoff creation:
  - `GEMINI.md`: missing
  - `QWEN.md`: missing
  - `IFLOW.md`: exists
  - `CRUSH.md`: exists
  - `LLXPRT.md`: missing
- Runtime config facts at time of handoff creation:
  - [`.gemini/settings.json`](file:///home/masum/github/EmailIntelligenceAider/.gemini/settings.json) uses `"contextFileName": "AGENTS.md"`
  - [`.qwen/settings.json`](file:///home/masum/github/EmailIntelligenceAider/.qwen/settings.json) uses `"contextFileName": "AGENTS.md"`
- Manifest drift is present in [`.github/instructions/tools-manifest.json`](file:///home/masum/github/EmailIntelligenceAider/.github/instructions/tools-manifest.json)
  - It still describes `GEMINI.md` and `QWEN.md` as tool contexts while those files are currently absent.
  - It still treats `qwen` in a partly placeholder/stale way.
  - It does not cleanly reconcile runtime behavior with corrected Tier 2 policy.
- Live content nuance at time of handoff creation:
  - [IFLOW.md](file:///home/masum/github/EmailIntelligenceAider/IFLOW.md) exists and contains meaningful iFlow-specific integration/workflow content.
  - [CRUSH.md](file:///home/masum/github/EmailIntelligenceAider/CRUSH.md) exists but appears to be generated/shared AGENTS-style content rather than clearly unique Crush-specific Tier 2 guidance.

These facts are inputs, not conclusions. The next agent must still re-check live state before editing.

---

## Source Hierarchy

The next agent must use evidence in this order.

### 1. Live Repo State First

Primary truth is current branch reality.

- [docs/handoff/STATE.md](file:///home/masum/github/EmailIntelligenceAider/docs/handoff/STATE.md)
- [docs/handoff/phase-05-file-cleanup.md](file:///home/masum/github/EmailIntelligenceAider/docs/handoff/phase-05-file-cleanup.md)
- [docs/handoff/phase-06-deduplication.md](file:///home/masum/github/EmailIntelligenceAider/docs/handoff/phase-06-deduplication.md)
- [docs/handoff/phase-09-verification.md](file:///home/masum/github/EmailIntelligenceAider/docs/handoff/phase-09-verification.md)
- [docs/handoff/README.md](file:///home/masum/github/EmailIntelligenceAider/docs/handoff/README.md)
- [docs/handoff/MULTI_HANDOFF_EXECUTION_PROCESS.md](file:///home/masum/github/EmailIntelligenceAider/docs/handoff/MULTI_HANDOFF_EXECUTION_PROCESS.md)
- [docs/AGENT_RULES_IMPLEMENTATION_HANDOFF.md](file:///home/masum/github/EmailIntelligenceAider/docs/AGENT_RULES_IMPLEMENTATION_HANDOFF.md)
- [docs/AGENT_RULES_GAP_ANALYSIS_AND_CONTENT_MAP.md](file:///home/masum/github/EmailIntelligenceAider/docs/AGENT_RULES_GAP_ANALYSIS_AND_CONTENT_MAP.md)
- [docs/handoff/content-archive/COLLATED_AGENT_FILES_ANALYSIS.md](file:///home/masum/github/EmailIntelligenceAider/docs/handoff/content-archive/COLLATED_AGENT_FILES_ANALYSIS.md)
- [`.gemini/settings.json`](file:///home/masum/github/EmailIntelligenceAider/.gemini/settings.json)
- [`.qwen/settings.json`](file:///home/masum/github/EmailIntelligenceAider/.qwen/settings.json)
- [`.github/instructions/tools-manifest.json`](file:///home/masum/github/EmailIntelligenceAider/.github/instructions/tools-manifest.json)
- Existing live root Tier 2 files if present

### 2. Corrected Handoff Docs Second

Use the corrected docs as execution guidance where older handoff text is stale or incomplete.

Key principle: the plan now follows a Tier 1 shared-content / Tier 2 root-file model. Do not silently drop root Tier 2 files just because Gemini and Qwen currently load shared context through settings that reference `AGENTS.md`.

### 3. Archive Snapshots and Histories Third

Use these as evidence to reconstruct or justify restore-versus-not_on_branch decisions.

- `/home/masum/github/agents/EmailIntelligenceGem/GEMINI__consolidate-cli-unification.md`
- `/home/masum/github/agents/EmailIntelligenceGem/QWEN__consolidate-cli-unification.md`
- `/home/masum/github/agents/EmailIntelligenceGem/IFLOW__consolidate-cli-unification.md`
- `/home/masum/github/agents/EmailIntelligenceGem/CRUSH__consolidate-cli-unification.md`
- `/home/masum/github/agents/EmailIntelligenceGem/LLXPRT__consolidate-cli-unification.md`
- `/home/masum/github/agents/EmailIntelligenceAuto/GEMINI__auto-sync-20260405.md`
- `/home/masum/github/agents/EmailIntelligenceAuto/QWEN__auto-sync-20260405.md`
- `/home/masum/github/agents/EmailIntelligenceAuto/IFLOW__auto-sync-20260405.md`
- `/home/masum/github/agents/EmailIntelligenceAuto/CRUSH__auto-sync-20260405.md`
- `/home/masum/github/agents/EmailIntelligenceAider/IFLOW__orchestration-tools.md`
- `/home/masum/github/agents/history/EmailIntelligenceGem/GEMINI_history.md`
- `/home/masum/github/agents/history/EmailIntelligenceGem/QWEN_history.md`
- `/home/masum/github/agents/history/EmailIntelligenceGem/IFLOW_history.md`
- `/home/masum/github/agents/history/EmailIntelligenceGem/CRUSH_history.md`
- `/home/masum/github/agents/history/EmailIntelligenceGem/LLXPRT_history.md`
- `/home/masum/github/agents/history/EmailIntelligenceAuto/GEMINI_history.md`
- `/home/masum/github/agents/history/EmailIntelligenceAuto/QWEN_history.md`
- `/home/masum/github/agents/history/EmailIntelligenceAuto/IFLOW_history.md`
- `/home/masum/github/agents/history/EmailIntelligenceAuto/CRUSH_history.md`
- `/home/masum/github/agents/history/EmailIntelligenceAuto/LLXPRT_history.md`
- `/home/masum/github/agents/history/EmailIntelligenceAider/IFLOW_history.md`
- `/home/masum/github/agents/history/EmailIntelligence/GEMINI_history.md`
- `/home/masum/github/agents/history/EmailIntelligence/QWEN_history.md`

### 4. Remote Git Evidence Fourth

Use these refs as concrete upstream evidence.

- `git show origin/001-agent-context-control:IFLOW.md`
- `git show origin/consolidate/cli-unification:CRUSH.md`
- `git show origin/consolidate/cli-unification:LLXPRT.md`
- `git show origin/004-guided-workflow:GEMINI.md`
- `git show origin/004-guided-workflow:QWEN.md`

---

## Deep Agent Prompt

Use the following prompt verbatim or with only minimal path corrections if needed.

```text
You are the next deep agent continuing the Agent Rules cleanup on the `orchestration-tools` branch in:

/home/masum/github/EmailIntelligenceAider

Your job is to finish the corrected Phase 5 and Phase 6 work, then run the corrected Phase 9 verification, while preserving any meaningful tool-specific behavior and documenting explicit branch-policy decisions.

Mission
- Execute the corrected handoff plan, not the stale Phase 1-oriented “Next Agent Instructions” in docs/handoff/STATE.md.
- Preserve unique Tier 2 root context behavior for Gemini, Qwen, iFlow, Crush, and LLxPRT where warranted.
- Keep shared content centralized where appropriate, but do not silently collapse Tier 2 files into AGENTS.md.
- Reconcile docs, manifest, and runtime behavior so the repo is internally consistent.
- Update docs/handoff/STATE.md with what you actually did, what policy decisions you made, and what verification passed or failed.

Hard Constraints
- No merges, no rebases, no resets, no destructive git commands.
- Never use `git add -A` or `git add .`.
- Do not revert unrelated user/worktree changes.
- Use docs/handoff/STATE.md as the execution log.
- Treat the corrected phase docs under docs/handoff/ as authoritative where they differ from older handoff text.
- Before editing anything, build a live-versus-archive-versus-remote comparison matrix for:
  - GEMINI.md
  - QWEN.md
  - IFLOW.md
  - CRUSH.md
  - LLXPRT.md
- If you need earlier conversation context, use `read_thread` on:
  - T-019d82c6-0385-73f7-8f20-f626d5ab49f5

Current Verified Live State
- Branch: `orchestration-tools`
- docs/handoff/STATE.md shows Phases 1-4 complete and Phase 5 pending.
- Current root Tier 2 file state:
  - GEMINI.md: missing
  - QWEN.md: missing
  - IFLOW.md: exists
  - CRUSH.md: exists
  - LLXPRT.md: missing
- Current runtime config facts:
  - .gemini/settings.json uses `contextFileName: "AGENTS.md"`
  - .qwen/settings.json uses `contextFileName: "AGENTS.md"`
- Current manifest is stale/inconsistent:
  - model_context entries do not fully reflect branch reality
  - tool `qwen` still reads like a placeholder in places
  - Gemini/Qwen discovery notes do not fully match runtime + corrected Tier 2 policy
- Current live file nuance:
  - IFLOW.md exists and appears to be a 104-line iFlow integration guide
  - CRUSH.md exists but currently looks like generated/shared AGENTS-style content, not obviously meaningful Crush-specific Tier 2 behavior
- Do not assume prior narrative about “missing IFLOW.md” is still true. Verify live state first and base decisions on that.

Source Hierarchy
Use this evidence hierarchy in order:

1. Live repo state first
- Current files in this branch
- Current runtime config in .gemini/settings.json and .qwen/settings.json
- Current tools-manifest.json
- Current docs/handoff plan files

2. Corrected handoff docs second
- docs/handoff/phase-05-file-cleanup.md
- docs/handoff/phase-06-deduplication.md
- docs/handoff/phase-09-verification.md
- docs/handoff/README.md
- docs/handoff/MULTI_HANDOFF_EXECUTION_PROCESS.md
- docs/AGENT_RULES_IMPLEMENTATION_HANDOFF.md
- docs/AGENT_RULES_GAP_ANALYSIS_AND_CONTENT_MAP.md
- docs/handoff/content-archive/COLLATED_AGENT_FILES_ANALYSIS.md

3. ~/github/agents archive snapshots and histories third
Use these as concrete evidence for reconstruction and policy decisions:
- /home/masum/github/agents/EmailIntelligenceGem/GEMINI__consolidate-cli-unification.md
- /home/masum/github/agents/EmailIntelligenceGem/QWEN__consolidate-cli-unification.md
- /home/masum/github/agents/EmailIntelligenceGem/IFLOW__consolidate-cli-unification.md
- /home/masum/github/agents/EmailIntelligenceGem/CRUSH__consolidate-cli-unification.md
- /home/masum/github/agents/EmailIntelligenceGem/LLXPRT__consolidate-cli-unification.md
- /home/masum/github/agents/EmailIntelligenceAuto/GEMINI__auto-sync-20260405.md
- /home/masum/github/agents/EmailIntelligenceAuto/QWEN__auto-sync-20260405.md
- /home/masum/github/agents/EmailIntelligenceAuto/IFLOW__auto-sync-20260405.md
- /home/masum/github/agents/EmailIntelligenceAuto/CRUSH__auto-sync-20260405.md
- /home/masum/github/agents/EmailIntelligenceAider/IFLOW__orchestration-tools.md
- /home/masum/github/agents/history/EmailIntelligenceGem/GEMINI_history.md
- /home/masum/github/agents/history/EmailIntelligenceGem/QWEN_history.md
- /home/masum/github/agents/history/EmailIntelligenceGem/IFLOW_history.md
- /home/masum/github/agents/history/EmailIntelligenceGem/CRUSH_history.md
- /home/masum/github/agents/history/EmailIntelligenceGem/LLXPRT_history.md
- /home/masum/github/agents/history/EmailIntelligenceAuto/GEMINI_history.md
- /home/masum/github/agents/history/EmailIntelligenceAuto/QWEN_history.md
- /home/masum/github/agents/history/EmailIntelligenceAuto/IFLOW_history.md
- /home/masum/github/agents/history/EmailIntelligenceAuto/CRUSH_history.md
- /home/masum/github/agents/history/EmailIntelligenceAuto/LLXPRT_history.md
- /home/masum/github/agents/history/EmailIntelligenceAider/IFLOW_history.md
- /home/masum/github/agents/history/EmailIntelligence/GEMINI_history.md
- /home/masum/github/agents/history/EmailIntelligence/QWEN_history.md

4. Remote git evidence fourth
Validate and use these refs as source material:
- `git show origin/001-agent-context-control:IFLOW.md`
- `git show origin/consolidate/cli-unification:CRUSH.md`
- `git show origin/consolidate/cli-unification:LLXPRT.md`
- `git show origin/004-guided-workflow:GEMINI.md`
- `git show origin/004-guided-workflow:QWEN.md`

Execution Plan

Step 1: Re-read the state and corrected plan
Read at minimum:
- docs/handoff/STATE.md
- docs/handoff/phase-05-file-cleanup.md
- docs/handoff/phase-06-deduplication.md
- docs/handoff/phase-09-verification.md
- docs/handoff/README.md
- docs/handoff/MULTI_HANDOFF_EXECUTION_PROCESS.md
- docs/AGENT_RULES_IMPLEMENTATION_HANDOFF.md
- docs/AGENT_RULES_GAP_ANALYSIS_AND_CONTENT_MAP.md
- docs/handoff/content-archive/COLLATED_AGENT_FILES_ANALYSIS.md

Step 2: Build the comparison matrix before editing
Create a working matrix in your notes/output with columns like:
- File
- Live branch status
- Live runtime references
- Live content classification
- Archive snapshot evidence
- History evidence
- Remote git evidence
- Unique tool-specific behavior present?
- Generated duplicate vs real Tier 2?
- Recommended branch action
- Required manifest status
- Notes/risk

You must answer these questions for each of the five Tier 2 root files:
- Should this file exist on this branch?
- If yes, should it be restored, replaced, split, or kept as-is?
- If a live file exists, is it a real Tier 2 file or just generated shared boilerplate?
- What should tools-manifest say after the decision?
- Does runtime currently load it directly, indirectly, or not at all?

Step 3: Execute corrected Phase 5
Use the corrected phase docs, but apply them against live reality rather than stale assumptions.

Required outcomes:
- GEMINI.md:
  - Root GEMINI.md must exist as a Tier 2 file if the corrected plan still calls for it.
  - Split out Jules template content to `.gemini/JULES_TEMPLATE.md`.
  - Keep Gemini-specific instructions at the root.
  - Do not collapse Gemini-specific behavior into AGENTS.md.
- QWEN.md:
  - Preserve any scientific/session-manager content before replacement.
  - Create `docs/SCIENTIFIC_BRANCH_DOCS.md` if needed.
  - Restore/replace root QWEN.md with reviewed Tier 2 Qwen instructions.
  - Keep QWEN.md at root.
- IFLOW.md:
  - Do not assume the current 104-line file is final.
  - Compare current live IFLOW.md against archive/remote richer versions.
  - Preserve meaningful iFlow-specific workflow/model/setup behavior if iFlow is active on this branch.
  - If iFlow is truly not used on this branch, set manifest to `not_on_branch` instead of silently dropping it.
- CRUSH.md:
  - Current live CRUSH.md looks like generated shared content; do not treat that as conclusive evidence of meaningful Tier 2 coverage.
  - Decide explicitly whether Crush is active on this branch.
  - If active, restore or replace with real Crush-specific Tier 2 content from evidence sources.
  - If not active, remove/leave absent as appropriate and mark `not_on_branch`.
- LLXPRT.md:
  - Determine whether LLxPRT is active on this branch.
  - Restore only if active; otherwise mark `not_on_branch`.
- Run the Phase 5 verification/gate checks from the corrected docs.

Step 4: Execute corrected Phase 6
Complete the deduplication and manifest reconciliation work.

Required areas:
- `.kilo/mcp.json`
  - Ensure it is populated correctly if still empty/broken/stale.
- `.github/instructions/*.md`
  - Remove Prisma references.
  - Fix TypeScript-only guidance to match Python backend + TypeScript frontend reality.
- `.clinerules/*.md` and `.cursor/rules/*.md` / `.mdc`
  - Fix any remaining TypeScript-only or stale references as specified by Phase 6.
  - Remove `cerebras-mcp` references where still present.
- `*_deep.md`
  - Delete the duplicate `_deep` files listed in Phase 6 if they still exist.
- `.github/instructions/tools-manifest.json`
  - Reconcile manifest entries with actual Phase 5 outcomes.
  - Reconcile discovery/config notes with actual runtime in:
    - .gemini/settings.json
    - .qwen/settings.json
  - Fix Gemini/Qwen contradictions so docs do not claim one thing while runtime does another.
  - Ensure Tier 2 statuses for IFLOW/CRUSH/LLXPRT are explicit: `configured` or `not_on_branch`.
  - Ensure GEMINI.md and QWEN.md are treated as root Tier 2 files when present.
  - Resolve the stale Qwen tool/manifest mismatch as part of this reconciliation.
- Also inspect and resolve the known stale guidance areas that were already identified:
  - `.github/instructions/GEMINI.instructions.md`
  - `.qwen/PROJECT_SUMMARY.md`
  If one of these is clearly in scope and contradicts the corrected runtime model, fix it. If not fixed, document it explicitly as residual follow-up and explain why it was left out.

Step 5: Run corrected Phase 9 verification
Run the updated multi-loop verification after implementation.

Important:
- Use the corrected docs/handoff/phase-09-verification.md as the basis.
- If a command in the docs is stale but the intent is clear, execute the intent and document the exact correction.
- For RuleZ verification, account for the known `rulez 2.3.0` caveat:
  - a raw `grep -c "Blocked"` may return `2` because “Blocked” appears in both JSON reason and summary output
  - evaluate semantic pass/fail, not just that raw count
  - record the caveat in STATE if it still applies

Success Criteria
You are done only when all of the following are true:
- You built and used a comparison matrix before editing.
- Phase 5 decisions are explicit for all five Tier 2 root files.
- tools-manifest matches branch reality and runtime behavior.
- GEMINI/QWEN/IFLOW/CRUSH/LLXPRT are either intentionally present with justified content or intentionally absent with `not_on_branch`.
- Duplicate `_deep` files are removed if present.
- Prisma / TypeScript-only / cerebras-mcp leftovers are resolved in the Phase 6 target areas.
- Phase 5 gate checks run.
- Phase 6 gate checks run.
- Phase 9 verification loops run.
- docs/handoff/STATE.md is updated with:
  - your agent name
  - start/completion timestamps
  - Phase 5 completion details
  - Phase 6 completion details
  - Phase 9 verification result
  - explicit branch-policy decisions for GEMINI/QWEN/IFLOW/CRUSH/LLXPRT
  - files modified
  - issues/caveats/blockers
- If anything remains unresolved, document it clearly in STATE and stop rather than hand-waving it.

State File Update Requirements
Update docs/handoff/STATE.md so it reflects reality now, not the stale generic starter text.
At minimum:
- Mark Phase 5 as in progress, then complete/fail.
- Add Phase 6 and Phase 9 entries if needed.
- Record branch-policy decisions for:
  - GEMINI.md
  - QWEN.md
  - IFLOW.md
  - CRUSH.md
  - LLXPRT.md
- Record the RuleZ grep-count caveat again only if it materially affected verification.
- Replace stale “Next Agent Instructions” with instructions appropriate to the new stopping point.

Working Style
- Search first, then edit.
- Prefer small correct changes over broad refactors.
- Use live repo state as the primary truth.
- If a live file was generated from Ruler/shared content, classify it as such instead of assuming it satisfies Tier 2 requirements.
- Preserve meaningful tool-specific workflow layers; do not erase value-bearing behavior in the name of deduplication.

Final Response Format
When you finish, report back with:
1. The comparison-matrix conclusions for the five Tier 2 root files.
2. The concrete changes made.
3. Manifest/runtime reconciliation details.
4. Verification results for Phase 5, Phase 6, and Phase 9.
5. Any remaining blockers or residual risks.

Do not stop after analysis. Implement the changes, verify them, and update docs/handoff/STATE.md before returning.
```

---

## Detailed Execution Checklist

This checklist is intentionally extensive. The next agent should work through it in order and check off each item while executing.

### A. Session Start Checklist

- [ ] Confirm working directory is `/home/masum/github/EmailIntelligenceAider`.
- [ ] Confirm current branch is `orchestration-tools`.
- [ ] Confirm no destructive git operations will be used.
- [ ] Re-open [docs/handoff/STATE.md](file:///home/masum/github/EmailIntelligenceAider/docs/handoff/STATE.md).
- [ ] Record agent name in STATE.
- [ ] Record Phase 5 start timestamp in STATE.
- [ ] Note in STATE that execution is following the corrected Phase 5/6/9 plan, not stale Phase 1 starter text.
- [ ] If needed, read prior thread context from `T-019d82c6-0385-73f7-8f20-f626d5ab49f5`.

### B. Required Reading Checklist

- [ ] Read [docs/handoff/phase-05-file-cleanup.md](file:///home/masum/github/EmailIntelligenceAider/docs/handoff/phase-05-file-cleanup.md).
- [ ] Read [docs/handoff/phase-06-deduplication.md](file:///home/masum/github/EmailIntelligenceAider/docs/handoff/phase-06-deduplication.md).
- [ ] Read [docs/handoff/phase-09-verification.md](file:///home/masum/github/EmailIntelligenceAider/docs/handoff/phase-09-verification.md).
- [ ] Read [docs/handoff/README.md](file:///home/masum/github/EmailIntelligenceAider/docs/handoff/README.md).
- [ ] Read [docs/handoff/MULTI_HANDOFF_EXECUTION_PROCESS.md](file:///home/masum/github/EmailIntelligenceAider/docs/handoff/MULTI_HANDOFF_EXECUTION_PROCESS.md).
- [ ] Read [docs/AGENT_RULES_IMPLEMENTATION_HANDOFF.md](file:///home/masum/github/EmailIntelligenceAider/docs/AGENT_RULES_IMPLEMENTATION_HANDOFF.md).
- [ ] Read [docs/AGENT_RULES_GAP_ANALYSIS_AND_CONTENT_MAP.md](file:///home/masum/github/EmailIntelligenceAider/docs/AGENT_RULES_GAP_ANALYSIS_AND_CONTENT_MAP.md).
- [ ] Read [docs/handoff/content-archive/COLLATED_AGENT_FILES_ANALYSIS.md](file:///home/masum/github/EmailIntelligenceAider/docs/handoff/content-archive/COLLATED_AGENT_FILES_ANALYSIS.md).

### C. Live State Re-Validation Checklist

- [ ] Re-check whether `GEMINI.md` exists.
- [ ] Re-check whether `QWEN.md` exists.
- [ ] Re-check whether `IFLOW.md` exists.
- [ ] Re-check whether `CRUSH.md` exists.
- [ ] Re-check whether `LLXPRT.md` exists.
- [ ] Re-read [`.gemini/settings.json`](file:///home/masum/github/EmailIntelligenceAider/.gemini/settings.json).
- [ ] Re-read [`.qwen/settings.json`](file:///home/masum/github/EmailIntelligenceAider/.qwen/settings.json).
- [ ] Re-read [`.github/instructions/tools-manifest.json`](file:///home/masum/github/EmailIntelligenceAider/.github/instructions/tools-manifest.json).
- [ ] Inspect live [IFLOW.md](file:///home/masum/github/EmailIntelligenceAider/IFLOW.md) content if still present.
- [ ] Inspect live [CRUSH.md](file:///home/masum/github/EmailIntelligenceAider/CRUSH.md) content if still present.
- [ ] Note any live-state drift since this handoff document was created.

### D. Evidence Gathering Checklist

- [ ] Read Gemini archive snapshot(s).
- [ ] Read Qwen archive snapshot(s).
- [ ] Read IFLOW archive snapshot(s).
- [ ] Read CRUSH archive snapshot(s).
- [ ] Read LLXPRT archive snapshot(s).
- [ ] Read relevant Gemini history files.
- [ ] Read relevant Qwen history files.
- [ ] Read relevant IFLOW history files.
- [ ] Read relevant CRUSH history files.
- [ ] Read relevant LLXPRT history files.
- [ ] Run `git show origin/001-agent-context-control:IFLOW.md`.
- [ ] Run `git show origin/consolidate/cli-unification:CRUSH.md`.
- [ ] Run `git show origin/consolidate/cli-unification:LLXPRT.md`.
- [ ] Run `git show origin/004-guided-workflow:GEMINI.md`.
- [ ] Run `git show origin/004-guided-workflow:QWEN.md`.
- [ ] Capture short evidence notes for each file rather than relying on memory.

### E. Comparison Matrix Checklist

- [ ] Build a matrix row for `GEMINI.md`.
- [ ] Build a matrix row for `QWEN.md`.
- [ ] Build a matrix row for `IFLOW.md`.
- [ ] Build a matrix row for `CRUSH.md`.
- [ ] Build a matrix row for `LLXPRT.md`.
- [ ] Mark current live status for each file.
- [ ] Mark whether runtime currently loads it directly, indirectly, or not at all.
- [ ] Mark whether current live content is unique Tier 2 or shared/generated boilerplate.
- [ ] Mark whether archive evidence shows meaningful unique tool-specific behavior.
- [ ] Mark whether remote evidence supports restoration.
- [ ] Mark recommended branch action for each file.
- [ ] Mark required manifest status for each file.
- [ ] Confirm the matrix is complete before any edits begin.

### F. Phase 5 Execution Checklist

#### GEMINI.md

- [ ] Decide whether `GEMINI.md` must exist on this branch.
- [ ] If yes, reconstruct Gemini-specific root content from live/archive/remote evidence.
- [ ] Separate any Jules-template content into `.gemini/JULES_TEMPLATE.md`.
- [ ] Keep Gemini-specific instructions in root `GEMINI.md`.
- [ ] Confirm `GEMINI.md` is not just duplicated AGENTS content.
- [ ] Confirm Gemini-specific behavior is preserved.

#### QWEN.md

- [ ] Decide whether `QWEN.md` must exist on this branch.
- [ ] Preserve any scientific/session-manager content before replacement.
- [ ] Create `docs/SCIENTIFIC_BRANCH_DOCS.md` if that content needs a dedicated preservation target.
- [ ] Rebuild reviewed root `QWEN.md` Tier 2 instructions.
- [ ] Confirm `QWEN.md` is not just duplicated AGENTS content.
- [ ] Confirm scientific/session-manager material was not lost.

#### IFLOW.md

- [ ] Compare live `IFLOW.md` with archive and remote IFLOW evidence.
- [ ] Decide whether current live IFLOW content is sufficient, partial, or stale.
- [ ] If iFlow is active, preserve meaningful model/setup/workflow instructions.
- [ ] If iFlow is not active, explicitly choose `not_on_branch` rather than silent deletion.
- [ ] Confirm final `IFLOW.md` state matches the branch-policy decision.

#### CRUSH.md

- [ ] Determine whether Crush is active on this branch.
- [ ] Confirm whether live `CRUSH.md` is merely generated/shared content.
- [ ] If Crush is active, replace/restore with real Crush-specific Tier 2 instructions.
- [ ] If Crush is not active, explicitly classify it as `not_on_branch`.
- [ ] Confirm final `CRUSH.md` state matches that decision.

#### LLXPRT.md

- [ ] Determine whether LLxPRT is active on this branch.
- [ ] If active, restore `LLXPRT.md` from evidence.
- [ ] If not active, explicitly classify LLxPRT as `not_on_branch`.
- [ ] Confirm final `LLXPRT.md` state matches that decision.

#### Phase 5 Verification

- [ ] Run all corrected Phase 5 verification/gate checks.
- [ ] Record any deviations from stale commands and why they were corrected.
- [ ] Update STATE with Phase 5 completion or blocker details.

### G. Phase 6 Execution Checklist

#### Manifest Reconciliation

- [ ] Reconcile model-context entries in [`.github/instructions/tools-manifest.json`](file:///home/masum/github/EmailIntelligenceAider/.github/instructions/tools-manifest.json).
- [ ] Reconcile the Gemini tool entry with actual runtime and root-file policy.
- [ ] Reconcile the Qwen tool entry with actual runtime and root-file policy.
- [ ] Ensure IFLOW status is explicit.
- [ ] Ensure CRUSH status is explicit.
- [ ] Ensure LLXPRT status is explicit.
- [ ] Use `configured` or `not_on_branch` explicitly where appropriate.
- [ ] Ensure manifest discovery notes match `.gemini/settings.json`.
- [ ] Ensure manifest discovery notes match `.qwen/settings.json`.

#### Instruction Cleanup

- [ ] Inspect `.github/instructions/*.md` for Prisma references.
- [ ] Remove Prisma references where stale.
- [ ] Inspect `.github/instructions/*.md` for TypeScript-first or TypeScript-only guidance.
- [ ] Fix guidance to reflect Python/FastAPI backend plus TypeScript frontend reality.
- [ ] Inspect `.github/instructions/GEMINI.instructions.md` specifically.
- [ ] Fix `.github/instructions/GEMINI.instructions.md` if still wrong.

#### Rule/Config Cleanup

- [ ] Inspect `.clinerules/*.md` for stale TypeScript-only guidance.
- [ ] Inspect `.cursor/rules/*.md` or `.mdc` for stale TypeScript-only guidance.
- [ ] Remove stale `cerebras-mcp` references wherever Phase 6 requires.
- [ ] Inspect `.kilo/mcp.json`.
- [ ] Repair or populate `.kilo/mcp.json` if still broken/empty/stale.
- [ ] Inspect `.qwen/PROJECT_SUMMARY.md`.
- [ ] Fix or explicitly defer `.qwen/PROJECT_SUMMARY.md` with a recorded reason.

#### Duplicate File Cleanup

- [ ] Search for duplicate `*_deep.md` files named by Phase 6.
- [ ] Delete the duplicate `_deep` files that are in scope.
- [ ] Re-check that only intended files were deleted.

#### Phase 6 Verification

- [ ] Run all corrected Phase 6 verification/gate checks.
- [ ] Update STATE with Phase 6 results.

### H. Phase 9 Verification Checklist

- [ ] Re-read [docs/handoff/phase-09-verification.md](file:///home/masum/github/EmailIntelligenceAider/docs/handoff/phase-09-verification.md) immediately before verification.
- [ ] Run the corrected verification loops, not just one-off spot checks.
- [ ] Verify manifest/runtime consistency.
- [ ] Verify root Tier 2 file decisions match branch reality.
- [ ] Verify deleted/retained file outcomes match explicit policy.
- [ ] Verify Ruler-generated/shared files are not being mistaken for Tier 2 coverage.
- [ ] Verify no meaningful tool-specific behavior was lost.
- [ ] Verify any preservation documents such as `docs/SCIENTIFIC_BRANCH_DOCS.md` if created.
- [ ] Re-run RuleZ validation.
- [ ] Apply the known RuleZ 2.3.0 caveat when interpreting `grep -c "Blocked"`.
- [ ] Record semantic RuleZ pass/fail, not only raw grep output.
- [ ] Capture verification command outputs or summaries for STATE.

### I. STATE.md Update Checklist

- [ ] Mark Phase 5 as complete, blocked, or failed.
- [ ] Add a Phase 6 section if not already present.
- [ ] Add a Phase 9 section if not already present.
- [ ] Record agent name.
- [ ] Record timestamps for Phase 5, Phase 6, and Phase 9 work.
- [ ] Record files modified.
- [ ] Record branch-policy decision for `GEMINI.md`.
- [ ] Record branch-policy decision for `QWEN.md`.
- [ ] Record branch-policy decision for `IFLOW.md`.
- [ ] Record branch-policy decision for `CRUSH.md`.
- [ ] Record branch-policy decision for `LLXPRT.md`.
- [ ] Record tools-manifest reconciliation results.
- [ ] Record runtime reconciliation results for Gemini and Qwen settings.
- [ ] Record verification outcomes.
- [ ] Record caveats, residual risks, or blockers.
- [ ] Replace stale next-step instructions with instructions appropriate to the actual stopping point.

### J. Final Completion Checklist

- [ ] Confirm comparison matrix existed before edits.
- [ ] Confirm every Tier 2 file now has an explicit policy outcome.
- [ ] Confirm manifest matches final branch state.
- [ ] Confirm runtime notes and docs no longer contradict each other.
- [ ] Confirm no meaningful agentic workflow or tool-specific prompt layer was lost.
- [ ] Confirm Phase 5 verification passed or that failures are explicitly documented.
- [ ] Confirm Phase 6 verification passed or that failures are explicitly documented.
- [ ] Confirm Phase 9 verification passed or that failures are explicitly documented.
- [ ] Confirm STATE is accurate enough for another agent to resume without re-discovering the same planning gap.

---

## Notes for the Next Agent

- Do not assume earlier narrative is still accurate if live branch state has changed.
- Gemini and Qwen currently load shared context indirectly through settings that point at `AGENTS.md`, but that does not automatically eliminate the need for reviewed root `GEMINI.md` and `QWEN.md` Tier 2 files under the corrected plan.
- The current presence of [CRUSH.md](file:///home/masum/github/EmailIntelligenceAider/CRUSH.md) is not enough by itself. You must determine whether it is a meaningful tool-specific file or only generated shared content.
- The current presence of [IFLOW.md](file:///home/masum/github/EmailIntelligenceAider/IFLOW.md) is meaningful evidence, but it still needs archive/remote comparison before being accepted as final.
- The goal is not maximum file retention. The goal is explicit, justified, loss-avoiding policy.
