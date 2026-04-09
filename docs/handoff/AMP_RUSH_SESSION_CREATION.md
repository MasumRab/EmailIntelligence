# AMP Rush Model Session Creation

**Purpose:** Define the session creation protocol for Rush-level AMP execution  
**Use:** Start a new LLM agent session with this prompt  
**Updated:** 2026-04-09

---

## Quick Start

### Option 1: Full Task Execution

```
You are a Rush-level AMP agent executing the Agent Rules Implementation.

**Project:** `/home/masum/github/EmailIntelligenceAider`  
**Branch:** `orchestration-tools`  
**Task:** Fix 13 identified issues in AI coding agent configurations

**Handoff Documents:**
- Master: `docs/AGENT_RULES_IMPLEMENTATION_HANDOFF.md`
- Phases: `docs/handoff/phase-01-emergency-fixes.md` through `phase-04-agent-rulez.md`
- State: `docs/handoff/STATE.md`
- Process: `docs/handoff/MULTI_HANDOFF_EXECUTION_PROCESS.md`

**Critical Rules:**
1. Run VERIFY after EVERY step — do not skip
2. Do NOT proceed if verification fails
3. Copy strings EXACTLY — do not paraphrase
4. One edit per tool call — do not batch
5. NEVER use `git add -A` or `git add .`

**Execution Protocol:**
1. Read `docs/handoff/STATE.md` for current progress
2. Execute phase steps with verification
3. Run gate check after phase completion
4. Update STATE.md with results
5. Handoff to next agent if phase complete

**Start with Phase 1:** Read `docs/handoff/phase-01-emergency-fixes.md`
```

### Option 2: Phase-Specific Execution

```
You are executing Phase [N] of the Agent Rules Implementation Handoff.

**Phase Document:** `docs/handoff/phase-0[N]-[name].md`
**State File:** `docs/handoff/STATE.md`

**Task:** Execute all steps in Phase [N] with verification after each step.

**Critical Rules:**
1. Run VERIFY command after EVERY step
2. Do NOT proceed to next step if verification fails
3. Copy strings EXACTLY from phase document
4. One edit per tool call — do not batch

**After Phase [N] Completion:**
1. Run Phase [N] Gate Check
2. Update `docs/handoff/STATE.md` with:
   - Status: COMPLETE or FAILED
   - Gate Check output
   - Files modified
   - Issues encountered (if any)
3. If PASS: Document handoff instructions for next agent
4. If FAIL: Document blocker and stop

**If blocked:** Read `docs/handoff/MULTI_HANDOFF_EXECUTION_PROCESS.md` section "Error Recovery"
```

---

## Session Creation Checklist

Before starting agent execution, verify:

```bash
# 1. Project exists
test -d /home/masum/github/EmailIntelligenceAider && echo "PROJECT: EXISTS" || echo "PROJECT: MISSING"

# 2. Branch correct  
cd /home/masum/github/EmailIntelligenceAider && git branch --show-current

# 3. Handoff documents exist
ls docs/handoff/phase-*.md docs/handoff/STATE.md docs/handoff/README.md

# 4. Current state readable
cat docs/handoff/STATE.md | head -20
```

---

## Rush-Level Execution Guidelines

### Speed Priorities

| Priority | Action | Example |
|----------|--------|---------|
| 1 | Execute step | Write file, edit file |
| 2 | Verify step | Run verify command |
| 3 | Update state | Mark step done in STATE.md |
| 4 | Next step | Proceed if verify passes |

### What to Skip (for Speed)

- Do NOT explain what you're doing — just do it
- Do NOT show file contents unless verification fails
- Do NOT ask for confirmation — execute and verify
- Do NOT comment on code quality — this is infrastructure setup

### What to NEVER Skip

- **VERIFY commands** — always run after each step
- **Gate checks** — always run after phase completion
- **State updates** — always update STATE.md
- **Error reporting** — always document failures

---

## Verification Quick Reference

### Phase 1 Verify Commands

| Step | Verify Command | Expected |
|------|----------------|----------|
| 1.1-1.2 | `grep -c '<<<<<<' CLAUDE.md` | `0` |
| 1.3-1.4 | `python3 -c "import json; json.load(open('.roo/mcp.json')); print('VALID')"` | `VALID` |
| 1.5-1.6 | `python3 -c "import json; json.load(open('.cursor/mcp.json')); print('VALID')"` | `VALID` |
| 1.7-1.8 | `python3 -c "import json; json.load(open('.claude/mcp.json')); print('VALID')"` | `VALID` |
| 1.9-1.10 | `grep -c "YOUR_" .windsurf/mcp.json` | `0` |
| 1.11-1.12 | `python3 -c "import json; json.load(open('.trae/mcp.json')); print('VALID')"` | `VALID` |
| 1.13 | `test ! -f .rules && echo "DELETED"` | `DELETED` |

### Phase 1 Gate Check

```bash
echo "=== PHASE 1 GATE ==="
echo -n "CLAUDE.md: "; grep -c '<<<<<<' CLAUDE.md || echo "0"
echo -n ".roo/mcp.json: "; python3 -c "import json; json.load(open('.roo/mcp.json')); print('YES')" 2>/dev/null || echo "NO"
echo -n ".cursor/mcp.json: "; python3 -c "import json; json.load(open('.cursor/mcp.json')); print('YES')" 2>/dev/null || echo "NO"
echo -n ".claude/mcp.json: "; python3 -c "import json; json.load(open('.claude/mcp.json')); print('YES')" 2>/dev/null || echo "NO"
echo -n ".windsurf/mcp.json: "; grep -c "YOUR_" .windsurf/mcp.json || echo "0"
echo -n ".trae/mcp.json: "; python3 -c "import json; json.load(open('.trae/mcp.json')); print('YES')" 2>/dev/null || echo "NO"
echo -n ".rules: "; test ! -f .rules && echo "DELETED" || echo "EXISTS"
```

---

## Handoff Prompts by Phase

### Phase 1 → Phase 2 Handoff

```
**HANDOFF: Phase 1 COMPLETE**

**Status:** PASS
**Agent:** [AGENT_NAME]
**Next Phase:** 2

**Phase 1 Gate Output:**
[PASTE GATE CHECK OUTPUT]

**Files Modified:**
- `.roo/mcp.json` — populated
- `.cursor/mcp.json` — populated  
- `.claude/mcp.json` — populated
- `.windsurf/mcp.json` — placeholders replaced
- `.trae/mcp.json` — created
- `.rules` — deleted

**Next Agent Task:**
Execute Phase 2 of `docs/handoff/phase-02-content-fixes.md`
```

---

## Error Recovery Protocol

### If Verification Fails

1. **Re-read the step** — check phase document for exact instructions
2. **Re-read the file** — use Read tool, compare to expected
3. **Re-execute the step** — copy strings EXACTLY from phase document
4. **Re-verify** — run verify command again
5. **If still failing** — document in STATE.md under "Current Blocker"

---

## Related Documents

| Document | Purpose |
|----------|---------|
| `docs/handoff/README.md` | Tool coverage matrix |
| `docs/handoff/STATE.md` | Execution state tracker |
| `docs/handoff/MULTI_HANDOFF_EXECUTION_PROCESS.md` | Detailed process |
| `docs/handoff/phase-*.md` | Granular task specifications |
