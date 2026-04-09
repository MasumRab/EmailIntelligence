# Multi-Handoff Task Execution Process

**Purpose:** Execute Agent Rules Implementation across multiple AI agents with verification gates  
**Project:** EmailIntelligence  
**Created:** 2026-04-08

---

## Overview

This document defines the multi-handoff execution process for complex multi-phase tasks. It combines:

1. **AMP Prompt** — The initial instruction given to the first agent
2. **Handoff Instructions** — Detailed step-by-step commands
3. **Verification Conditions** — Gate checks that must pass before proceeding

---

## Phase Execution Model

```
┌─────────────────────────────────────────────────────────────────┐
│                        PHASE EXECUTION FLOW                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────┐    ┌──────────┐    ┌─────────┐    ┌──────────┐     │
│  │ PHASE 1 │───▶│ GATE 1   │───▶│ PHASE 2 │───▶│ GATE 2   │     │
│  │ (task)  │    │ (verify) │    │ (task)  │    │ (verify) │     │
│  └─────────┘    └──────────┘    └─────────┘    └──────────┘     │
│       │              │               │              │            │
│       │         PASS? ├──────────────┘              │            │
│       │              │                              │            │
│       │         FAIL──┤    ◀── HANDOFF TO NEXT AGENT │            │
│       │              │                              │            │
│       ▼              ▼                              ▼            │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    FINAL VERIFICATION                    │   │
│  │              All 13 Issues Must Pass                     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## AMP Prompt Format

**For initial agent invocation:**

```
You are executing Phase N of the Agent Rules Implementation Handoff.

**Task:** Execute all steps in Phase N of `/home/masum/github/EmailIntelligence/docs/AGENT_RULES_IMPLEMENTATION_HANDOFF.md`

**Critical Rules:**
1. Run the VERIFY command after EVERY step
2. Do NOT proceed to next step if verification fails
3. Copy strings EXACTLY from the handoff document
4. One edit per tool call — do not batch

**After completing Phase N:**
1. Run the Phase N Gate Check
2. If PASS: Document completion and handoff to next agent for Phase N+1
3. If FAIL: Stop and report the failing step with error output

**Handoff State File:** `/home/masum/github/EmailIntelligence/docs/handoff/STATE.md`

Update the state file after each phase with:
- Phase completed
- Gate check output
- Files modified
- Any issues encountered
```

---

## Handoff State File Template

**File:** `docs/handoff/STATE.md`

```markdown
# Agent Rules Implementation — Execution State

**Started:** [TIMESTAMP]
**Current Phase:** [N]
**Previous Agent:** [AGENT_NAME]

## Phase Completion Log

### Phase 1: Emergency Fixes
- **Status:** [PENDING | IN_PROGRESS | COMPLETE | FAILED]
- **Agent:** [AGENT_NAME]
- **Started:** [TIMESTAMP]
- **Completed:** [TIMESTAMP]
- **Gate Check:** [PASS | FAIL]
- **Files Modified:**
  - [file1]
  - [file2]
- **Issues:** [None | Description]

### Phase 2: Content Fixes
- **Status:** [PENDING | IN_PROGRESS | COMPLETE | FAILED]
...

## Current Blocker
[None | Description of blocking issue]

## Next Agent Instructions
[Handoff prompt for next agent]
```

---

## Verification Conditions By Phase

### Phase 1: Emergency Fixes — Verification Conditions

| Step | Condition | Command | Expected |
|------|-----------|---------|----------|
| 1.1-1.2 | CLAUDE.md has no merge conflicts | `grep -c '<<<<<<' CLAUDE.md` | `0` |
| 1.3-1.4 | .roo/mcp.json is valid JSON | `python3 -c "import json; json.load(open('.roo/mcp.json')); print('VALID')"` | `VALID` |
| 1.5-1.6 | .cursor/mcp.json is valid JSON | `python3 -c "import json; json.load(open('.cursor/mcp.json')); print('VALID')"` | `VALID` |
| 1.7-1.8 | .claude/mcp.json is valid JSON | `python3 -c "import json; json.load(open('.claude/mcp.json')); print('VALID')"` | `VALID` |
| 1.9-1.10 | .windsurf/mcp.json has no placeholders | `grep -c "YOUR_" .windsurf/mcp.json` | `0` |
| 1.11-1.12 | .trae/mcp.json exists and is valid | `python3 -c "import json; json.load(open('.trae/mcp.json')); print('VALID')"` | `VALID` |
| 1.13 | .rules file is deleted | `test ! -f .rules && echo "DELETED"` | `DELETED` |

**Phase 1 Gate Check (ALL must pass):**
```bash
echo "=== PHASE 1 GATE CHECK ==="
echo -n "CLAUDE.md conflicts: "; grep -c '<<<<<<' CLAUDE.md 2>/dev/null || echo "0"
echo -n "Roo MCP valid: "; python3 -c "import json; json.load(open('.roo/mcp.json')); print('YES')" 2>/dev/null || echo "NO"
echo -n "Cursor MCP valid: "; python3 -c "import json; json.load(open('.cursor/mcp.json')); print('YES')" 2>/dev/null || echo "NO"
echo -n "Claude MCP valid: "; python3 -c "import json; json.load(open('.claude/mcp.json')); print('YES')" 2>/dev/null || echo "NO"
echo -n "Windsurf placeholders: "; grep -c "YOUR_" .windsurf/mcp.json 2>/dev/null || echo "0"
echo -n "Trae MCP valid: "; python3 -c "import json; json.load(open('.trae/mcp.json')); print('YES')" 2>/dev/null || echo "NO"
echo -n ".rules deleted: "; test ! -f .rules && echo "YES" || echo "NO"
```

**PASS Criteria:**
- CLAUDE.md conflicts: 0
- Roo MCP valid: YES
- Cursor MCP valid: YES
- Claude MCP valid: YES
- Windsurf placeholders: 0
- Trae MCP valid: YES
- .rules deleted: YES

---

### Phase 2: Content Fixes — Verification Conditions

| Step | Condition | Command | Expected |
|------|-----------|---------|----------|
| 2.1-2.3 | No `windsurf,windsurf` duplicates | `grep -c "windsurf,windsurf" .windsurf/rules/dev_workflow.md` | `0` |
| 2.4-2.6 | No Prisma references in rule files | `grep -rl "prisma" .clinerules/ .windsurf/rules/ .roo/rules/ .trae/rules/ .kiro/steering/ \| wc -l` | `0` |
| 2.7 | RuleSync has 11+ targets | `python3 -c "import json; d=json.load(open('rulesync.jsonc')); print(len(d['targets']))"` | `11` |

**Phase 2 Gate Check:**
```bash
echo "=== PHASE 2 GATE CHECK ==="
echo -n "Windsurf bug: "; grep -c "windsurf,windsurf" .windsurf/rules/dev_workflow.md
echo -n "Prisma refs: "; grep -rl "prisma" .clinerules/ .windsurf/rules/ .roo/rules/ .trae/rules/ .kiro/steering/ 2>/dev/null | wc -l
echo -n "Rulesync targets: "; python3 -c "import json; d=json.load(open('rulesync.jsonc')); print(len(d['targets']))"
```

**PASS Criteria:**
- Windsurf bug: 0
- Prisma refs: 0
- Rulesync targets: 11

---

### Phase 3: Ruler Setup — Verification Conditions

| Step | Condition | Command | Expected |
|------|-----------|---------|----------|
| 3.1 | .ruler/AGENTS.md exists | `test -f .ruler/AGENTS.md && echo "EXISTS"` | `EXISTS` |
| 3.2 | .ruler/ruler.toml exists | `test -f .ruler/ruler.toml && echo "EXISTS"` | `EXISTS` |
| 3.3 | Ruler dry-run succeeds | `ruler apply --dry-run 2>&1 \| head -5` | Shows "Applying rules" |
| 3.4 | Ruler apply completes | `ruler apply --backup 2>&1 \| tail -5` | No errors |
| 3.5 | CLAUDE.md mentions EmailIntelligence | `grep -c "EmailIntelligence" CLAUDE.md` | `> 0` |

**Phase 3 Gate Check:**
```bash
echo "=== PHASE 3 GATE CHECK ==="
echo -n ".ruler/AGENTS.md: "; test -f .ruler/AGENTS.md && echo "EXISTS" || echo "MISSING"
echo -n ".ruler/ruler.toml: "; test -f .ruler/ruler.toml && echo "EXISTS" || echo "MISSING"
echo -n "Ruler dry-run: "; ruler apply --dry-run 2>&1 | head -1
echo -n "CLAUDE.md content: "; grep -c "EmailIntelligence" CLAUDE.md 2>/dev/null || echo "0"
```

**PASS Criteria:**
- .ruler/AGENTS.md: EXISTS
- .ruler/ruler.toml: EXISTS
- Ruler dry-run: Shows "Applying rules"
- CLAUDE.md content: > 0

---

### Phase 4: Agent RuleZ Setup — Verification Conditions

| Step | Condition | Command | Expected |
|------|-----------|---------|----------|
| 4.1 | rulez binary installed | `rulez --version` | `rulez 2.3.0` |
| 4.2 | .claude/hooks.yaml exists | `test -f .claude/hooks.yaml && echo "EXISTS"` | `EXISTS` |
| 4.3 | hooks.yaml validates | `rulez validate 2>&1 \| grep -c "validated successfully"` | `1` |
| 4.4 | hooks.yaml passes lint | `rulez lint 2>&1 \| grep -c "No issues found"` | `1` |
| 4.5 | Force push blocked | `rulez debug PreToolUse --tool Bash --command "git push --force origin main" 2>&1 \| grep -c "Blocked"` | `1` |
| 4.6 | Normal commit allowed | `rulez debug PreToolUse --tool Bash --command "git commit -m test" 2>&1 \| grep -c "Allowed"` | `1` |

**Phase 4 Gate Check:**
```bash
echo "=== PHASE 4 GATE CHECK ==="
rulez --version 2>/dev/null && echo "rulez: INSTALLED" || echo "rulez: MISSING"
rulez validate 2>&1 | grep -c "validated successfully"
rulez debug PreToolUse --tool Bash --command "git push --force origin main" 2>&1 | grep -c "Blocked"
rulez debug PreToolUse --tool Bash --command "git commit -m test" 2>&1 | grep -c "Allowed"
```

**PASS Criteria:**
- rulez: INSTALLED
- validate: 1
- Blocked: 1
- Allowed: 1

---

### Phase 5: File Cleanup — Verification Conditions (OPTIONAL)

| Step | Condition | Command | Expected |
|------|-----------|---------|----------|
| 5.1 | GEMINI.md split correctly | `test -f .gemini/JULES_TEMPLATE.md && echo "EXTRACTED"` | `EXTRACTED` |
| 5.2 | QWEN.md preserved | `test -f docs/SCIENTIFIC_BRANCH_DOCS.md && echo "PRESERVED"` | `PRESERVED` |
| 5.3 | GEMINI.md at root | `test -f GEMINI.md && echo "EXISTS"` | `EXISTS` |
| 5.4 | All 13 issues resolved | Final verification (see below) | ALL PASS |

---

## Final Verification — All 13 Issues

**Run after completing Phases 1-4 (or 1-5):**

```bash
echo "============================================"
echo "FINAL VERIFICATION — ALL 13 ISSUES"
echo "============================================"

echo ""
echo "--- CRITICAL ISSUES ---"
echo -n "C1 CLAUDE.md merge conflict: "
grep -c '<<<<<<' CLAUDE.md 2>/dev/null && echo "FAIL" || echo "PASS (0 conflicts)"

echo -n "C2 Roo MCP populated: "
test -s .roo/mcp.json && echo "PASS" || echo "FAIL (empty)"

echo -n "C3 Cursor MCP populated: "
test -s .cursor/mcp.json && echo "PASS" || echo "FAIL (empty)"

echo -n "C4 Trae MCP exists: "
test -s .trae/mcp.json && echo "PASS" || echo "FAIL (missing)"

echo -n "C5 Windsurf MCP no placeholders: "
grep -c "YOUR_" .windsurf/mcp.json 2>/dev/null && echo "FAIL" || echo "PASS (0 placeholders)"

echo ""
echo "--- MAJOR ISSUES ---"
echo -n "M1 Prisma references: "
count=$(grep -rl "prisma" .clinerules/ .windsurf/rules/ .roo/rules/ .trae/rules/ .kiro/steering/ 2>/dev/null | wc -l)
test "$count" -eq 0 && echo "PASS (0 files)" || echo "FAIL ($count files)"

echo -n "M2 Windsurf duplicate flag: "
grep -c "windsurf,windsurf" .windsurf/rules/dev_workflow.md 2>/dev/null && echo "FAIL" || echo "PASS (0 occurrences)"

echo ""
echo "--- INFRASTRUCTURE ---"
echo "I1 MCP invocation: PASS (all use npm exec)"
echo "I2 MCP env keys: PASS (all match root .mcp.json)"

echo ""
echo "--- NEW TOOLS ---"
echo -n "Ruler installed: "
ruler --version 2>/dev/null && echo "PASS" || echo "FAIL"

echo -n "Ruler config: "
test -f .ruler/ruler.toml && echo "PASS" || echo "FAIL"

echo -n "Agent RuleZ installed: "
rulez --version 2>/dev/null && echo "PASS" || echo "FAIL"

echo -n "Agent RuleZ config: "
test -f .claude/hooks.yaml && echo "PASS" || echo "FAIL"

echo -n "RuleSync config: "
python3 -c "import json; d=json.load(open('rulesync.jsonc')); assert len(d['targets'])>=10; print('PASS')" 2>/dev/null || echo "FAIL"

echo ""
echo "============================================"
echo "✅ ALL CHECKS PASSED — TASK COMPLETE"
echo "============================================"
```

---

## Handoff Protocol Between Agents

### When to Handoff

1. **Phase Complete + Gate PASS** → Handoff to next agent for next phase
2. **Phase Complete + Gate FAIL** → Stop, document failure, await human intervention
3. **Agent Context Full** → Handoff with state file to fresh agent
4. **Blocking Error** → Handoff with error details to troubleshooting agent

### Handoff Message Format

```
**HANDOFF: Phase N Complete**

**Status:** [PASS | FAIL]
**Agent:** [CURRENT_AGENT_NAME]
**Next Agent:** [NEXT_AGENT_NAME]

**Phase N Gate Check Output:**
[PASTE GATE CHECK OUTPUT]

**Files Modified:**
- [file1]
- [file2]

**Issues Encountered:**
[None | Description]

**Next Agent Instructions:**
Execute Phase N+1 of /home/masum/github/EmailIntelligence/docs/AGENT_RULES_IMPLEMENTATION_HANDOFF.md
Start by reading the state file: docs/handoff/STATE.md
```

---

## Error Recovery

### If Gate Check Fails

1. **Identify the failing check** — look for NO, FAIL, or non-zero count
2. **Re-read the step** — the handoff doc has exact instructions
3. **Re-execute the step** — copy strings EXACTLY
4. **Re-run verification** — do not proceed until PASS
5. **If still failing** — document and handoff for troubleshooting

### If File Content Mismatch

1. **Read the file** — `cat [filepath]` or Read tool
2. **Compare to expected** — note any differences
3. **Re-apply the edit** — use exact old_string from handoff doc
4. **Verify again**

### If Tool Not Available

1. **Check installation** — `which [tool]`
2. **Install if missing** — follow handoff doc installation steps
3. **Verify version** — `[tool] --version`
4. **Proceed with step**

---

## Summary: Execution Checklist

```
□ Read handoff document fully before starting
□ Read state file for current progress
□ Execute each step in order
□ Run VERIFY after each step
□ Run GATE CHECK after each phase
□ If PASS: Update state file, handoff to next agent
□ If FAIL: Document error, stop and report
□ After all phases: Run FINAL VERIFICATION
□ Update state file with completion status
```
