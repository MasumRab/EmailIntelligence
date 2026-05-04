# Phase 13: Smart Amp Deep Agent Autonomous Completion Handoff

## Purpose

This is the highest-context handoff for completing the remaining Agent Rules work on the `orchestration-tools` branch with an Amp deep agent operating autonomously and, when useful, delegating focused analysis to subagents/background threads.

This document supersedes Phase 12 when the goal is not only to finish corrected Phase 5, Phase 6, and Phase 9, but to close out all remaining relevant handoff work from Phase 5 onward, including explicit resolution of whether Phases 7, 8, 10, and 11 are complete, still needed, or should be deferred.

The next agent should use this document when it needs the fullest possible context from:

- live repo state
- corrected handoff docs
- previous Amp thread conversations
- off-root evidence under `~/github/agents`
- remote git evidence

---

## Autonomous Completion Goal

The next Amp deep agent should drive the handoff to a real stopping point, not just another intermediate handoff.

That means:

- completing the corrected Phase 5 work
- completing the corrected Phase 6 work
- deciding whether Phase 7 and Phase 8 still require action
- using Phase 10 reference material where needed
- deciding whether any validated Phase 11 remediation remains after the corrected Phase 5/6 work
- running Phase 9 verification as the final verification layer
- updating [docs/handoff/STATE.md](file:///home/masum/github/EmailIntelligenceAider/docs/handoff/STATE.md) so another agent does not need to rediscover the same planning gap

The agent must explicitly classify each remaining phase from 5 onward as one of:

- `complete`
- `completed during this run`
- `not needed after later corrections`
- `deferred with reason`
- `blocked with reason`

---

## Required Conversation Sources

The next agent must ingest the previous Amp conversations, not just the docs.

### Thread 1: Corrected Plan / Runtime Findings

- Thread ID: `T-019d82c6-0385-73f7-8f20-f626d5ab49f5`
- Recommended `read_thread` goal:

```text
Extract the implementation history, completed phases, major runtime findings, corrected plan decisions, source hierarchy, and explicit next steps for finishing Phase 5, Phase 6, and Phase 9.
```

### Thread 2: Phase 12 + Resume Wiring

- Thread ID: `T-019d82e2-1c91-75ea-99f8-7c7d322bfae9`
- Recommended `read_thread` goal:

```text
Extract the work done in this thread: the creation of phase-12, README/process/state/session-creation updates, and the intended deep-agent autonomous resume flow.
```

### Conversation-Derived Facts To Carry Forward

From Thread 1:

- Phases 1-4 were completed and recorded in STATE.
- A real Ruler compatibility issue was found and fixed by giving Cline a file-specific output path in `.ruler/ruler.toml`.
- The deleted `.rules` file did not contain unique agent/subagent definitions; meaningful Task Master workflow content was preserved in `.ruler/AGENTS.md`.
- The original cleanup plan over-focused on AGENTS/CLAUDE propagation and under-modeled Tier 2 root files.
- Gemini and Qwen currently load shared context via `.gemini/settings.json` and `.qwen/settings.json`, but root `GEMINI.md` and `QWEN.md` must still be treated as real Tier 2 files.
- `IFLOW.md`, `CRUSH.md`, and `LLXPRT.md` require explicit branch-policy decisions rather than silent deletion.
- `.github/instructions/GEMINI.instructions.md` was previously identified as stale and Python/FastAPI-inconsistent.
- `.qwen/PROJECT_SUMMARY.md` was previously identified as stale side-channel content.
- The RuleZ 2.3.0 grep-count caveat is real: semantic pass/fail matters more than raw `grep -c "Blocked"`.

From Thread 2:

- [docs/handoff/phase-12-deep-agent-handoff.md](file:///home/masum/github/EmailIntelligenceAider/docs/handoff/phase-12-deep-agent-handoff.md) was created as a corrected deep-agent handoff for Phase 5/6/9.
- [docs/handoff/README.md](file:///home/masum/github/EmailIntelligenceAider/docs/handoff/README.md), [docs/handoff/MULTI_HANDOFF_EXECUTION_PROCESS.md](file:///home/masum/github/EmailIntelligenceAider/docs/handoff/MULTI_HANDOFF_EXECUTION_PROCESS.md), [docs/handoff/AMP_RUSH_SESSION_CREATION.md](file:///home/masum/github/EmailIntelligenceAider/docs/handoff/AMP_RUSH_SESSION_CREATION.md), and [docs/handoff/STATE.md](file:///home/masum/github/EmailIntelligenceAider/docs/handoff/STATE.md) were updated to point future agents at the deep-agent resume path.
- Phase 12 is already the preferred deep-agent resume handoff for corrected Phase 5/6/9 execution.
- This Phase 13 handoff is meant to extend that into full remaining-phase closure with autonomous orchestration and conversation-aware execution.

---

## Source Hierarchy

The next agent must use sources in this order.

### 1. Live Repo State First

Primary truth is the current branch reality under:

- [docs/handoff/STATE.md](file:///home/masum/github/EmailIntelligenceAider/docs/handoff/STATE.md)
- [docs/handoff/README.md](file:///home/masum/github/EmailIntelligenceAider/docs/handoff/README.md)
- [docs/handoff/phase-05-file-cleanup.md](file:///home/masum/github/EmailIntelligenceAider/docs/handoff/phase-05-file-cleanup.md)
- [docs/handoff/phase-06-deduplication.md](file:///home/masum/github/EmailIntelligenceAider/docs/handoff/phase-06-deduplication.md)
- [docs/handoff/phase-07-hierarchy.md](file:///home/masum/github/EmailIntelligenceAider/docs/handoff/phase-07-hierarchy.md)
- [docs/handoff/phase-08-orchestration.md](file:///home/masum/github/EmailIntelligenceAider/docs/handoff/phase-08-orchestration.md)
- [docs/handoff/phase-09-verification.md](file:///home/masum/github/EmailIntelligenceAider/docs/handoff/phase-09-verification.md)
- [docs/handoff/phase-10-references.md](file:///home/masum/github/EmailIntelligenceAider/docs/handoff/phase-10-references.md)
- [docs/handoff/phase-11-smart-remediation.md](file:///home/masum/github/EmailIntelligenceAider/docs/handoff/phase-11-smart-remediation.md)
- [docs/handoff/phase-12-deep-agent-handoff.md](file:///home/masum/github/EmailIntelligenceAider/docs/handoff/phase-12-deep-agent-handoff.md)
- [docs/AGENT_RULES_IMPLEMENTATION_HANDOFF.md](file:///home/masum/github/EmailIntelligenceAider/docs/AGENT_RULES_IMPLEMENTATION_HANDOFF.md)
- [docs/AGENT_RULES_GAP_ANALYSIS_AND_CONTENT_MAP.md](file:///home/masum/github/EmailIntelligenceAider/docs/AGENT_RULES_GAP_ANALYSIS_AND_CONTENT_MAP.md)
- [docs/handoff/content-archive/COLLATED_AGENT_FILES_ANALYSIS.md](file:///home/masum/github/EmailIntelligenceAider/docs/handoff/content-archive/COLLATED_AGENT_FILES_ANALYSIS.md)
- [`.gemini/settings.json`](file:///home/masum/github/EmailIntelligenceAider/.gemini/settings.json)
- [`.qwen/settings.json`](file:///home/masum/github/EmailIntelligenceAider/.qwen/settings.json)
- [`.github/instructions/tools-manifest.json`](file:///home/masum/github/EmailIntelligenceAider/.github/instructions/tools-manifest.json)

### 2. Previous Thread Conversations Second

Use `read_thread` on:

- `T-019d82c6-0385-73f7-8f20-f626d5ab49f5`
- `T-019d82e2-1c91-75ea-99f8-7c7d322bfae9`

These are required sources, not optional nice-to-haves.

### 3. Corrected Handoff Docs Third

Use the corrected docs to drive execution decisions where earlier text or stale state-file prompts disagree.

### 4. Off-Root Local Archive Evidence Fourth

Use the `~/github/agents` evidence set to reconstruct or justify Tier 2 root-file decisions.

### 5. Remote Git Evidence Fifth

Use `git show origin/<branch>:<file>` evidence after live repo state, threads, docs, and local archive evidence.

---

## Off-Root Evidence Links

These are outside the repo root and should be treated as explicit evidence sources.

### Snapshot Files

- [EmailIntelligenceGem/GEMINI__consolidate-cli-unification.md](file:///home/masum/github/agents/EmailIntelligenceGem/GEMINI__consolidate-cli-unification.md)
- [EmailIntelligenceGem/QWEN__consolidate-cli-unification.md](file:///home/masum/github/agents/EmailIntelligenceGem/QWEN__consolidate-cli-unification.md)
- [EmailIntelligenceGem/IFLOW__consolidate-cli-unification.md](file:///home/masum/github/agents/EmailIntelligenceGem/IFLOW__consolidate-cli-unification.md)
- [EmailIntelligenceGem/CRUSH__consolidate-cli-unification.md](file:///home/masum/github/agents/EmailIntelligenceGem/CRUSH__consolidate-cli-unification.md)
- [EmailIntelligenceGem/LLXPRT__consolidate-cli-unification.md](file:///home/masum/github/agents/EmailIntelligenceGem/LLXPRT__consolidate-cli-unification.md)
- [EmailIntelligenceAuto/GEMINI__auto-sync-20260405.md](file:///home/masum/github/agents/EmailIntelligenceAuto/GEMINI__auto-sync-20260405.md)
- [EmailIntelligenceAuto/QWEN__auto-sync-20260405.md](file:///home/masum/github/agents/EmailIntelligenceAuto/QWEN__auto-sync-20260405.md)
- [EmailIntelligenceAuto/IFLOW__auto-sync-20260405.md](file:///home/masum/github/agents/EmailIntelligenceAuto/IFLOW__auto-sync-20260405.md)
- [EmailIntelligenceAuto/CRUSH__auto-sync-20260405.md](file:///home/masum/github/agents/EmailIntelligenceAuto/CRUSH__auto-sync-20260405.md)
- [EmailIntelligenceAider/IFLOW__orchestration-tools.md](file:///home/masum/github/agents/EmailIntelligenceAider/IFLOW__orchestration-tools.md)

### History Files

- [EmailIntelligenceAider/cursor_rules_GEMINI_history.md](file:///home/masum/github/agents/history/EmailIntelligenceAider/cursor_rules_GEMINI_history.md)
- [EmailIntelligenceAider/IFLOW_history.md](file:///home/masum/github/agents/history/EmailIntelligenceAider/IFLOW_history.md)
- [EmailIntelligence/GEMINI_history.md](file:///home/masum/github/agents/history/EmailIntelligence/GEMINI_history.md)
- [EmailIntelligence/QWEN_history.md](file:///home/masum/github/agents/history/EmailIntelligence/QWEN_history.md)
- [EmailIntelligenceGem/GEMINI_history.md](file:///home/masum/github/agents/history/EmailIntelligenceGem/GEMINI_history.md)
- [EmailIntelligenceGem/QWEN_history.md](file:///home/masum/github/agents/history/EmailIntelligenceGem/QWEN_history.md)
- [EmailIntelligenceGem/IFLOW_history.md](file:///home/masum/github/agents/history/EmailIntelligenceGem/IFLOW_history.md)
- [EmailIntelligenceGem/CRUSH_history.md](file:///home/masum/github/agents/history/EmailIntelligenceGem/CRUSH_history.md)
- [EmailIntelligenceGem/LLXPRT_history.md](file:///home/masum/github/agents/history/EmailIntelligenceGem/LLXPRT_history.md)
- [EmailIntelligenceAuto/GEMINI_history.md](file:///home/masum/github/agents/history/EmailIntelligenceAuto/GEMINI_history.md)
- [EmailIntelligenceAuto/QWEN_history.md](file:///home/masum/github/agents/history/EmailIntelligenceAuto/QWEN_history.md)
- [EmailIntelligenceAuto/IFLOW_history.md](file:///home/masum/github/agents/history/EmailIntelligenceAuto/IFLOW_history.md)
- [EmailIntelligenceAuto/CRUSH_history.md](file:///home/masum/github/agents/history/EmailIntelligenceAuto/CRUSH_history.md)
- [EmailIntelligenceAuto/LLXPRT_history.md](file:///home/masum/github/agents/history/EmailIntelligenceAuto/LLXPRT_history.md)

### Remote Git Evidence Targets

- `git show origin/001-agent-context-control:IFLOW.md`
- `git show origin/consolidate/cli-unification:CRUSH.md`
- `git show origin/consolidate/cli-unification:LLXPRT.md`
- `git show origin/004-guided-workflow:GEMINI.md`
- `git show origin/004-guided-workflow:QWEN.md`

---

## Autonomous Operation Model

The next agent should behave as the primary orchestrator and use subagents/background threads only to reduce context pressure and accelerate evidence gathering.

### Main Agent Responsibilities

The main Amp deep agent owns:

- final branch-policy decisions
- all code and docs edits that land in the repo
- all verification runs
- the final update to [docs/handoff/STATE.md](file:///home/masum/github/EmailIntelligenceAider/docs/handoff/STATE.md)

### Suggested Subagent Work Packets

If context grows or evidence gathering becomes wide, the main agent should spin off focused background threads with `handoff` for one narrow goal each.

Suggested packets:

1. Tier 2 Evidence Matrix Packet
- Goal: compare live, archive, history, and remote evidence for `GEMINI.md`, `QWEN.md`, `IFLOW.md`, `CRUSH.md`, and `LLXPRT.md`
- Deliverable: a restore/replace/keep/not_on_branch recommendation table with citations

2. Manifest + Runtime Reconciliation Packet
- Goal: audit `.github/instructions/tools-manifest.json`, `.gemini/settings.json`, `.qwen/settings.json`, `.github/instructions/*.md`, `.qwen/PROJECT_SUMMARY.md`, and Phase 6 targets
- Deliverable: a concrete edit list and contradictions matrix

3. Remaining Phase Triage Packet
- Goal: determine whether Phases 7, 8, and 11 still require execution after Phase 5/6 edits
- Deliverable: per-phase status of `complete`, `needs_execution`, `verification_only`, `not_needed`, or `defer`

4. Verification Packet
- Goal: assemble and/or dry-run the commands needed for Phase 5 gates, Phase 6 gates, Phase 8 checks if relevant, and Phase 9 multi-loop verification
- Deliverable: command list, expected outcomes, and caveats including RuleZ 2.3.0 behavior

### Rules For Autonomous Delegation

- Subagents are for analysis, evidence gathering, and narrow audits.
- The main agent must integrate conclusions rather than copy them blindly.
- The main agent must not stop after receiving subagent results.
- The run is only complete when edits, verification, and STATE updates are finished.

---

## Remaining Phase Completion Strategy

The next agent must not assume that only Phase 5, Phase 6, and Phase 9 matter.

It must explicitly classify all remaining phases:

- Phase 5
- Phase 6
- Phase 7
- Phase 8
- Phase 9
- Phase 10
- Phase 11

### Expected Treatment By Phase

#### Phase 5

Must be executed using the corrected Tier 1 / Tier 2 model.

#### Phase 6

Must be executed with tools-manifest and runtime reconciliation.

#### Phase 7

Do not assume this phase is mandatory. Decide whether directory-level `AGENTS.md` work is still needed after Phase 6 or whether it should be left unexecuted and explicitly marked deferred/not needed.

#### Phase 8

Do not assume Phase 8 is already satisfied just because Ruler, RuleSync, and RuleZ exist. Confirm whether the tool responsibility matrix and branch-policy boundaries are already adequately represented after Phase 5/6 reconciliation.

#### Phase 9

Must be run as the final verification layer after all remaining relevant edits are complete.

#### Phase 10

Reference-only. Use it as evidence support. Mark it as reference-used rather than execution-pending if no standalone edits are required.

#### Phase 11

Do not blindly execute every remediation item. Reassess which validated findings remain after corrected Phase 5/6/7/8 work.

Possible Phase 11 outcomes:

- fully satisfied by corrected work
- partially remaining and executed during this run
- deferred with reason

---

## Smart Deep-Agent Prompt

Use the following prompt verbatim or with only minimal path corrections.

```text
You are an Amp deep agent resuming the Agent Rules cleanup on the `orchestration-tools` branch in:

/home/masum/github/EmailIntelligenceAider

Your job is to complete all remaining relevant handoff work autonomously, using subagents/background threads only when helpful for focused evidence gathering, and to stop only when the repo reaches a real documented stopping point.

Primary Handoff
- docs/handoff/phase-13-smart-amp-deep-agent-autonomous-handoff.md

Required Conversation Sources
- read_thread T-019d82c6-0385-73f7-8f20-f626d5ab49f5
- read_thread T-019d82e2-1c91-75ea-99f8-7c7d322bfae9

Mission
- Complete corrected Phase 5 and Phase 6.
- Decide and resolve the remaining status of Phases 7, 8, 10, and 11.
- Run Phase 9 verification after all relevant implementation work is complete.
- Reconcile docs, runtime behavior, and tools-manifest with actual branch reality.
- Preserve meaningful tool-specific behavior and prevent loss of Tier 2 root-file value.
- Update docs/handoff/STATE.md so the next agent does not need to rediscover the same context.

Hard Constraints
- No merges, no rebases, no resets, and no destructive git commands.
- Never use git add -A or git add .
- Do not revert unrelated worktree changes.
- Use live repo state first, previous threads second, corrected docs third, ~/github/agents evidence fourth, and remote git evidence fifth.
- Do not stop at analysis.
- If you delegate to subagents/background threads, you still own integration, edits, verification, and state updates.

Required First Actions
1. Read docs/handoff/STATE.md.
2. Read docs/handoff/phase-13-smart-amp-deep-agent-autonomous-handoff.md.
3. Use read_thread on both required prior threads.
4. Re-establish live state for GEMINI.md, QWEN.md, IFLOW.md, CRUSH.md, LLXPRT.md, .gemini/settings.json, .qwen/settings.json, and .github/instructions/tools-manifest.json.
5. Build two matrices before editing:
   - a Tier 2 root-file comparison matrix
   - a remaining-phases status matrix for phases 5-11

Autonomous Work Model
- Use subagents/background threads only for narrow evidence-gathering packets.
- Main agent keeps the final integrated plan and final implementation responsibility.
- Main agent decides whether Phase 7, Phase 8, and Phase 11 still need execution after Phase 5/6 work.

Minimum Deliverables
1. Tier 2 comparison matrix for GEMINI/QWEN/IFLOW/CRUSH/LLXPRT.
2. Remaining-phase status matrix for phases 5-11.
3. Corrected Phase 5 implementation.
4. Corrected Phase 6 implementation.
5. Explicit status resolution for Phase 7, Phase 8, Phase 10, and Phase 11.
6. Corrected Phase 9 verification run.
7. Updated docs/handoff/STATE.md with timestamps, files modified, branch-policy decisions, phase statuses, verification results, and blockers/caveats.

Success Condition
The run is only complete when every remaining phase from 5 onward has an explicit outcome recorded in STATE and all relevant edits and verification have been completed or clearly deferred with reason.
```

---

## Detailed Execution Checklist

### A. Thread Ingestion Checklist

- [ ] Read `T-019d82c6-0385-73f7-8f20-f626d5ab49f5` with a goal focused on completed phases, corrected plan decisions, runtime findings, and explicit next steps.
- [ ] Read `T-019d82e2-1c91-75ea-99f8-7c7d322bfae9` with a goal focused on Phase 12 creation and autonomous resume flow.
- [ ] Capture the key decisions from both threads in working notes.
- [ ] Confirm that thread-derived decisions do not conflict with live repo state.

### B. Live State Checklist

- [ ] Re-check branch and working directory.
- [ ] Re-read [docs/handoff/STATE.md](file:///home/masum/github/EmailIntelligenceAider/docs/handoff/STATE.md).
- [ ] Re-read [docs/handoff/phase-12-deep-agent-handoff.md](file:///home/masum/github/EmailIntelligenceAider/docs/handoff/phase-12-deep-agent-handoff.md).
- [ ] Re-check existence and content of `GEMINI.md`.
- [ ] Re-check existence and content of `QWEN.md`.
- [ ] Re-check existence and content of `IFLOW.md`.
- [ ] Re-check existence and content of `CRUSH.md`.
- [ ] Re-check existence and content of `LLXPRT.md`.
- [ ] Re-read `.gemini/settings.json`.
- [ ] Re-read `.qwen/settings.json`.
- [ ] Re-read `.github/instructions/tools-manifest.json`.

### C. Matrix Checklist

- [ ] Build the Tier 2 comparison matrix before editing.
- [ ] Build the remaining-phase status matrix before editing.
- [ ] Classify each phase from 5 through 11.
- [ ] Classify each Tier 2 root file as keep/restore/replace/split/not_on_branch.

### D. Subagent Checklist

- [ ] Decide whether subagents/background threads are needed.
- [ ] If used, keep each delegated goal narrow and evidence-focused.
- [ ] Collect subagent outputs without treating them as final truth.
- [ ] Integrate results into a single main-agent plan.

### E. Implementation Checklist

- [ ] Execute corrected Phase 5.
- [ ] Execute corrected Phase 6.
- [ ] Reassess whether Phase 7 requires action.
- [ ] Reassess whether Phase 8 requires action.
- [ ] Use Phase 10 references where needed.
- [ ] Reassess whether any Phase 11 validated findings remain.
- [ ] Execute only the Phase 11 residuals that are still real and still in scope.

### F. Verification Checklist

- [ ] Run Phase 5 gates.
- [ ] Run Phase 6 gates.
- [ ] Run any Phase 7/8 checks if those phases were executed.
- [ ] Run corrected Phase 9 multi-loop verification.
- [ ] Apply the RuleZ 2.3.0 semantic caveat.

### G. State Finalization Checklist

- [ ] Update STATE with actual start/completion timestamps.
- [ ] Record files modified.
- [ ] Record branch-policy decisions for all Tier 2 root files.
- [ ] Record explicit outcome for every phase from 5 onward.
- [ ] Record verification results.
- [ ] Record any deferred items or blockers.
- [ ] Replace stale next-step text with the true remaining state.

---

## Success Criteria

The next agent is done only if all of the following are true:

- both required prior threads were read and their decisions were incorporated
- off-root `~/github/agents` evidence was explicitly used where relevant
- the Tier 2 comparison matrix was created before edits
- the remaining-phase status matrix was created before edits
- corrected Phase 5 and Phase 6 were executed
- Phase 7, Phase 8, Phase 10, and Phase 11 each have explicit final status
- corrected Phase 9 verification was run after implementation
- `.github/instructions/tools-manifest.json` matches actual runtime and branch policy
- [docs/handoff/STATE.md](file:///home/masum/github/EmailIntelligenceAider/docs/handoff/STATE.md) records a real stopping point rather than another generic placeholder handoff

---

## Relationship To Phase 12

[Phase 12](file:///home/masum/github/EmailIntelligenceAider/docs/handoff/phase-12-deep-agent-handoff.md) remains the focused corrected handoff for Phase 5/6/9 execution.

This Phase 13 handoff extends that work by adding:

- mandatory prior-thread ingestion
- explicit off-root archive links
- remaining-phase closure from Phase 5 onward
- subagent-oriented autonomous execution guidance
- a requirement to resolve whether later phases are complete, unnecessary, deferred, or blocked
