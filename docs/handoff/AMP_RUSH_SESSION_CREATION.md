# AMP Session Creation

**Purpose:** Start an Amp agent session for the Agent Rules handoff on any branch, from any folder.
**Updated:** 2026-04-24

---

## Quick Start — Fresh Run (Any Branch, Any Folder)

```
You are executing the Agent Rules Implementation Handoff.

**Setup — auto-detect everything:**
1. Run `source docs/handoff/context-guard.sh` to detect project root, branch, and agent tools
2. The branch name and state file path are now in $CURRENT_BRANCH and $STATE_FILE
   - STATE_FILE is auto-set to: `docs/handoff/STATE_$(git branch --show-current).md`
3. If $STATE_FILE does not exist, create it: `cp docs/handoff/STATE_TEMPLATE.md "$STATE_FILE"`
4. Read `docs/handoff/README.md` for phase order and mode guidance

**Pre-flight — check for merge conflicts across the repo:**
   grep -rn '<<<<<<< ' . --include='*.md' --include='*.toml' --include='*.json' --include='*.sh' --include='*.yaml' | grep -v '.git/' | head -20
If any conflicts exist in handoff-relevant files (.ruler/ruler.toml, AGENTS.md, CLAUDE.md, docs/handoff/*), resolve them FIRST and record the resolution in $STATE_FILE.

**Execution:**
1. Read the next pending phase doc from `docs/handoff/phase-NN-*.md`
2. Execute all steps with verification after each
3. Run the gate check at the end of each phase
4. Update $STATE_FILE with status, decisions, files modified
5. Proceed to next phase or handoff if context is full

**Rules:**
1. Run VERIFY after EVERY step — do not skip
2. Do NOT proceed if verification fails
3. NEVER use `git add -A` or `git add .`
4. No merges, rebases, resets, or destructive git commands
5. Before editing ANY file, check it for merge conflict markers — resolve first if found
```

---

## Mode Selection

| Mode | Phases | Why |
|------|--------|-----|
| **Rush** | 1–4 | Mechanical edits with bash verification — no judgment needed |
| **Deep** | 5–10 | Tier 2 file decisions, stack evaluation — requires branch-policy judgment |
| **Smart** | 11 | Shell script refactoring — analysis-heavy, self-contained |

### Prompt 1 — Rush (Phases 1–4)

```
Execute Phases 1–4 of the Agent Rules handoff.

**Setup:**
1. Run: source docs/handoff/context-guard.sh
2. If $STATE_FILE doesn't exist, create it from STATE_TEMPLATE.md

**Pre-flight — merge conflict scan:**
   grep -rn '<<<<<<< ' .ruler/ AGENTS.md CLAUDE.md docs/handoff/ --include='*.md' --include='*.toml' 2>/dev/null | head -10
Resolve any conflicts BEFORE starting. Phase 1 Step 1.1 checks CLAUDE.md specifically — but check all files you touch.

**Phase docs:** `docs/handoff/phase-01-emergency-fixes.md` through `phase-04-agent-rulez.md`

Execute each step, verify, run gate check, update $STATE_FILE. Do not explain — just execute and verify.
```

### Prompt 2 — Deep (Phases 5–9)

```
Execute Phases 5–9 of the Agent Rules handoff.

**Setup:**
1. Run: source docs/handoff/context-guard.sh
2. Read $STATE_FILE to confirm Phases 1–4 are complete

**Pre-flight — merge conflict scan:**
   grep -rn '<<<<<<< ' . --include='*.md' --include='*.toml' --include='*.json' | grep -v .git/ | head -20
Resolve any conflicts in files you need to edit. Record resolutions in $STATE_FILE decision log.

**Phase docs:** `docs/handoff/phase-05-file-cleanup.md` through `phase-09-verification.md`

Phase 5 requires branch-policy decisions for Tier 2 root files (GEMINI.md, QWEN.md, IFLOW.md, CRUSH.md, LLXPRT.md). Check live state first, then decide keep/restore/not_on_branch for each. Record decisions in STATE.
```

### Prompt 3 — Deep (Phase 10)

```
Execute Phase 10 (Agent Rules Quality Evaluation).

**Setup:**
1. Run: source docs/handoff/context-guard.sh
2. Read $STATE_FILE to confirm Phase 9 is complete

**Pre-flight — merge conflict check on ruler config:**
   grep '<<<<<<< ' .ruler/ruler.toml 2>/dev/null && echo "RESOLVE FIRST" || echo "Clean"
If .ruler/ruler.toml has conflicts, resolve before running ruler apply.

**Phase doc:** `docs/handoff/phase-10-rule-quality.md`

Steps:
1. Run `bash scripts/detect-branch-stack.sh` — note branch style and template recommendations
2. Run `bash scripts/verify-agent-content.sh` — confirm structural accuracy
3. Run `bash scripts/detect-branch-stack.sh --generate-eval` — generate evaluation skeleton
4. For each recommended template, fetch rules from agentrulegen.com/templates/<name>
   Use the PERMISSIVE model: INCLUDE by default, only HARD CONFLICT excludes
5. Distill INCLUDE rules into one-liner additions for .ruler/AGENTS.md (stay under 80 lines)
6. Apply: `ruler apply` then re-run verify-agent-content.sh
7. Paste .ruler/AGENTS.md into agentrulegen.com/analyze and record quality score in $STATE_FILE
8. Run gate check
```

### Prompt 4 — Smart (Phase 11, independent)

```
Execute Phase 11 (Smart Workflow Remediation).

**Setup:**
1. Run: source docs/handoff/context-guard.sh

**Phase doc:** `docs/handoff/phase-11-smart-remediation.md`

This phase is independent of Phases 5–10. It addresses shell script hardening findings.
Before editing any shell script, check for merge conflict markers and resolve first.
Update $STATE_FILE when complete.
```

---

## Resume — Continuing a Partial Run

```
Resume the Agent Rules handoff.

**Setup:**
1. Run: source docs/handoff/context-guard.sh
2. Read $STATE_FILE to find the last completed phase
3. Run: grep -rn '<<<<<<< ' . --include='*.md' --include='*.toml' --include='*.json' | grep -v .git/ | head -20
4. If merge conflicts exist in any handoff-relevant files, resolve them first
5. Read the next pending phase doc
6. Continue from the first unchecked step
7. Update $STATE_FILE after each phase
```

---

## Pre-Session Checklist

```bash
source docs/handoff/context-guard.sh
# Output shows: Project Root, Branch, Agent Tools, State File
# If state file doesn't exist, create it:
# cp docs/handoff/STATE_TEMPLATE.md "$STATE_FILE"
```

---

## Cross-Variant Usage

To run the handoff on a different EmailIntelligence variant:

```bash
bash ~/github/scripts/handoff/run-handoff.sh EmailIntelligenceGem
# or
bash ~/github/scripts/handoff/run-handoff.sh EmailIntelligenceAuto
```

This copies the framework into the variant, creates the state file, and prints all prompts.

---

## Error Recovery

1. **Merge conflicts found** → Resolve, record resolution in $STATE_FILE decision log, then continue
2. **Verification fails** → Re-read the step, re-execute with exact strings, re-verify
3. **Gate check fails** → Document failing check in $STATE_FILE under "Issues", do not proceed
4. **Context full** → Update $STATE_FILE with current progress, handoff to fresh agent with Resume prompt
5. **File missing** → Use `context-agnostic-gates.sh` helpers which report `⚪ NOT PRESENT` instead of failing
