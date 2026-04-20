# AMP Session Creation

**Purpose:** Start an Amp agent session for the Agent Rules handoff on any branch.
**Updated:** 2026-04-14

---

## Quick Start — Fresh Run (Any Branch)

```
You are executing the Agent Rules Implementation Handoff.

**Project:** (auto-detected — run from project root)
**Branch:** `<BRANCH>` (replace with target branch)
**Handoff Index:** `docs/handoff/README.md`
**State File:** `docs/handoff/STATE_<BRANCH>.md`

**Task:** Execute all phases of the Agent Rules handoff on this branch.

**Setup:**
1. If `docs/handoff/STATE_<BRANCH>.md` does not exist, create it from `docs/handoff/STATE_TEMPLATE.md`
2. Source `docs/handoff/context-guard.sh` to auto-detect environment
3. Read `docs/handoff/README.md` for phase order and mode guidance

**Execution:**
1. Read the next pending phase doc from `docs/handoff/phase-NN-*.md`
2. Execute all steps with verification after each
3. Run the gate check at the end of each phase
4. Update `docs/handoff/STATE_<BRANCH>.md` with status, decisions, files modified
5. Proceed to next phase or handoff if context is full

**Rules:**
1. Run VERIFY after EVERY step — do not skip
2. Do NOT proceed if verification fails
3. Copy strings EXACTLY from phase documents
4. NEVER use `git add -A` or `git add .`
5. No merges, rebases, resets, or destructive git commands
```

---

## Mode Selection

Use the mode that matches the phases you're executing:

| Mode | Phases | Why |
|------|--------|-----|
| **Rush** | 1–4 | Mechanical edits with bash verification — no judgment needed |
| **Deep** | 5–9 | Tier 2 file decisions require reading live state and making branch-policy calls |
| **Smart** | 11 | Shell script refactoring — analysis-heavy, self-contained |

### Rush Prompt (Phases 1–4)

```
Execute Phases 1–4 of the Agent Rules handoff on `<BRANCH>`.

**Project:** (auto-detected — run from project root)
**Phase docs:** `docs/handoff/phase-01-emergency-fixes.md` through `phase-04-agent-rulez.md`
**State:** `docs/handoff/STATE_<BRANCH>.md`

Execute each step, verify, run gate check, update state. Do not explain — just execute and verify.
```

### Deep Prompt (Phases 5–10)

```
Execute Phases 5–10 of the Agent Rules handoff on `<BRANCH>`.

**Project:** (auto-detected — run from project root)
**Phase docs:** `docs/handoff/phase-05-file-cleanup.md` through `phase-10-rule-quality.md`
**State:** `docs/handoff/STATE_<BRANCH>.md`

Phase 5 requires branch-policy decisions for Tier 2 root files (GEMINI.md, QWEN.md, IFLOW.md, CRUSH.md, LLXPRT.md). Check live state first, then decide keep/restore/not_on_branch for each. Record decisions in STATE.
Phase 10 requires manual evaluation at agentrulegen.com/analyze — paste .ruler/AGENTS.md and record the quality score.
```

### Smart Prompt (Phase 11)

```
Execute Phase 11 (Smart Workflow Remediation) on `<BRANCH>`.

**Project:** (auto-detected — run from project root)
**Phase doc:** `docs/handoff/phase-11-smart-remediation.md`
**State:** `docs/handoff/STATE_<BRANCH>.md`

This phase is independent of Phases 5–10. It addresses shell script hardening findings.
```

---

## Resume — Continuing a Partial Run

```
Resume the Agent Rules handoff on `<BRANCH>`.

**Project:** (auto-detected — run from project root)
**State:** `docs/handoff/STATE_<BRANCH>.md`

1. Read the state file to find the last completed phase
2. Read the next pending phase doc
3. Continue from the first unchecked step
4. Update state after each phase
```

For `orchestration-tools` branch specifically, additional resume context exists in:
- `docs/handoff/phase-12-deep-agent-handoff.md` — corrected Phase 5/6/9 resume with evidence hierarchy
- `docs/handoff/phase-13-smart-amp-deep-agent-autonomous-handoff.md` — full remaining-phase closure with thread ingestion

---

## Pre-Session Checklist

```bash
# First: source docs/handoff/context-guard.sh
# Verify environment before starting
test -d "$PROJECT_ROOT" && echo "PROJECT: EXISTS" || echo "PROJECT: MISSING"
cd "$PROJECT_ROOT" && git branch --show-current
ls docs/handoff/phase-*.md docs/handoff/STATE.md docs/handoff/README.md
```

---

## Error Recovery

1. **Verification fails** → Re-read the step, re-execute with exact strings, re-verify
2. **Gate check fails** → Document failing check in STATE under "Issues", do not proceed
3. **Context full** → Update STATE with current progress, handoff to fresh agent with resume prompt
4. **File missing** → Use `context-agnostic-gates.sh` helpers which report `⚪ NOT PRESENT` instead of failing
