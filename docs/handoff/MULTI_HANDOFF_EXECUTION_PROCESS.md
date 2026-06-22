# Multi-Handoff Task Execution Process

**Purpose:** Gate checks and handoff protocol for the Agent Rules Implementation.
**Prompts:** See `AMP_RUSH_SESSION_CREATION.md` for session prompts.

---

## Execution Context

Run from any folder/branch using the context-agnostic framework:

```bash
source docs/handoff/context-guard.sh
source docs/handoff/context-agnostic-gates.sh
echo "State file: $STATE_FILE"
```

Each branch has its own `STATE_<branch>.md`. Create from `STATE_TEMPLATE.md` if missing.

---

## Phase Execution Flow

```
Phase N → Execute Steps → Verify Each → Gate Check → Update STATE → Next Phase
                                              │
                                         FAIL ├── Document failure, stop
                                              │
                                         PASS ├── Handoff to next agent/phase
```

### When to Handoff

1. **Phase Complete + Gate PASS** → Proceed to next phase
2. **Phase Complete + Gate FAIL** → Stop, document failure in STATE
3. **Agent Context Full** → Update STATE, handoff to fresh agent with resume prompt
4. **Blocking Error** → Document in STATE, stop

---

## Gate Checks by Phase

### Phase 1: Emergency Fixes

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

**PASS:** conflicts=0, all MCP=YES, placeholders=0, .rules=YES

---

### Phase 2: Content Fixes

```bash
echo "=== PHASE 2 GATE CHECK ==="
echo -n "Windsurf bug: "; grep -c "windsurf,windsurf" .windsurf/rules/dev_workflow.md 2>/dev/null || echo "0"
echo -n "Prisma refs: "; grep -rl "prisma" .clinerules/ .windsurf/rules/ .roo/rules/ .trae/rules/ .kiro/steering/ 2>/dev/null | wc -l
echo -n "Rulesync targets: "; python3 -c "import json; d=json.load(open('rulesync.jsonc')); print(len(d['targets']))"
```

**PASS:** bug=0, refs=0, targets≥11

---

### Phase 3: Ruler Setup

```bash
echo "=== PHASE 3 GATE CHECK ==="
echo -n ".ruler/AGENTS.md: "; test -f .ruler/AGENTS.md && echo "EXISTS" || echo "MISSING"
echo -n ".ruler/ruler.toml: "; test -f .ruler/ruler.toml && echo "EXISTS" || echo "MISSING"
echo -n "Ruler dry-run: "; ruler apply --dry-run 2>&1 | head -1
echo -n "CLAUDE.md content: "; grep -c "EmailIntelligence" CLAUDE.md 2>/dev/null || echo "0"
```

**PASS:** both EXISTS, dry-run shows "Applying rules", content>0

---

### Phase 4: Agent RuleZ

```bash
echo "=== PHASE 4 GATE CHECK ==="
rulez --version 2>/dev/null && echo "rulez: INSTALLED" || echo "rulez: MISSING"
rulez validate 2>&1 | grep -c "validated successfully"
rulez debug PreToolUse --tool Bash --command "git push --force origin main" 2>&1 | grep -c "Blocked"
rulez debug PreToolUse --tool Bash --command "git commit -m test" 2>&1 | grep -c "Allowed"
```

**PASS:** INSTALLED, validate=1, Blocked=1, Allowed=1
**Caveat:** rulez 2.3.0 may return 2 for `grep -c "Blocked"` (appears in both JSON reason and summary). Semantic pass is sufficient.

---

### Phase 5: File Cleanup

Gate check is in `phase-05-file-cleanup.md` Step 5.6.

---

### Phase 6: Deduplication

Gate check is in `phase-06-deduplication.md` bottom section.

---

### Phase 7: Hierarchy

Gate check is in `phase-07-hierarchy.md` bottom section.

---

### Phase 8: Orchestration

Gate check is in `phase-08-orchestration.md` bottom section.

---

### Phase 9: Verification

Run all 9 loops defined in `phase-09-verification.md`.

---

### Phase 10: Agent Rules Quality Evaluation

Gate check is in `phase-10-rule-quality.md` Step 10.8.

Manual step required: paste `.ruler/AGENTS.md` into `agentrulegen.com/analyze` and record the quality score.

Run `bash scripts/detect-branch-stack.sh` first to determine which templates to evaluate for the current branch's style family.

**Pre-built evaluations:** If `phase-10-stack-evaluation-{branch}.md` exists for your branch (with `{branch}` replaced by current branch name), use it directly. Otherwise, run `bash scripts/detect-branch-stack.sh --generate-eval` to auto-create evaluation skeleton for your branch.

---

### Phase 11: Smart Remediation

```bash
echo "=== PHASE 11 GATE CHECK ==="
echo -n "Prisma refs in .kilo/: "; grep -rl "prisma" .kilo/ 2>/dev/null | wc -l
echo -n "Prisma refs in .github/instructions/: "; grep -rl "prisma" .github/instructions/ 2>/dev/null | wc -l
echo -n "Unquoted vars in git commands: "; grep -n 'git .* \$[a-zA-Z_]' modules/branch.sh modules/distribute.sh 2>/dev/null | grep -v '"' | wc -l
source modules/safety.sh 2>/dev/null
validate_branch_name_format "orchestration-tools-feature" 2>/dev/null && echo "Valid: PASS" || echo "Valid: FAIL"
! validate_branch_name_format 'branch$(rm -rf /)' 2>/dev/null && echo "Injection blocked: PASS" || echo "Injection blocked: FAIL"
echo -n "GEMINI.md: "; test -f GEMINI.md && echo "EXISTS" || echo "MISSING"
echo -n "QWEN.md: "; test -f QWEN.md && echo "EXISTS" || echo "MISSING"
echo -n "config-loader.sh: "; test -f modules/config-loader.sh && echo "EXISTS" || echo "MISSING"
echo -n "config-accessors.sh: "; test -f modules/config-accessors.sh && echo "EXISTS" || echo "MISSING"
echo -n "config-policy.sh: "; test -f modules/config-policy.sh && echo "EXISTS" || echo "MISSING"
echo -n "Manual temp paths: "; grep -n '/tmp/' modules/utils.sh 2>/dev/null | grep -v mktemp | wc -l
```

**PASS:** All counts=0, validation=PASS, files=EXISTS

---

## Final Verification (All Core Issues)

Run after completing Phases 1–4 (or 1–9):

```bash
echo "============================================"
echo "FINAL VERIFICATION"
echo "============================================"
echo -n "C1 CLAUDE.md merge conflict: "; grep -c '<<<<<<' CLAUDE.md 2>/dev/null && echo "FAIL" || echo "PASS"
echo -n "C2 Roo MCP populated: "; test -s .roo/mcp.json && echo "PASS" || echo "FAIL"
echo -n "C3 Cursor MCP populated: "; test -s .cursor/mcp.json && echo "PASS" || echo "FAIL"
echo -n "C4 Trae MCP exists: "; test -s .trae/mcp.json && echo "PASS" || echo "FAIL"
echo -n "C5 Windsurf no placeholders: "; grep -c "YOUR_" .windsurf/mcp.json 2>/dev/null && echo "FAIL" || echo "PASS"
echo -n "M1 Prisma refs: "; count=$(grep -rl "prisma" .clinerules/ .windsurf/rules/ .roo/rules/ .trae/rules/ .kiro/steering/ 2>/dev/null | wc -l); test "$count" -eq 0 && echo "PASS" || echo "FAIL ($count)"
echo -n "M2 Windsurf dupe flag: "; grep -c "windsurf,windsurf" .windsurf/rules/dev_workflow.md 2>/dev/null && echo "FAIL" || echo "PASS"
echo -n "Ruler config: "; test -f .ruler/ruler.toml && echo "PASS" || echo "FAIL"
echo -n "Agent RuleZ: "; test -f .claude/hooks.yaml && echo "PASS" || echo "FAIL"
echo -n "RuleSync: "; python3 -c "import json; d=json.load(open('rulesync.jsonc')); assert len(d['targets'])>=10; print('PASS')" 2>/dev/null || echo "FAIL"
echo -n "Agent content: "; bash scripts/verify-agent-content.sh 2>/dev/null | tail -1
echo "============================================"
```

---

## Handoff Message Format

```
**HANDOFF: Phase N Complete**

**Status:** [PASS | FAIL]
**Branch:** [BRANCH_NAME]
**Agent:** [AGENT_NAME]

**Gate Check Output:**
[PASTE OUTPUT]

**Files Modified:**
- [file1]
- [file2]

**Issues:** [None | Description]

**Next:** Execute Phase N+1 from `docs/handoff/phase-NN-*.md`
**State:** `docs/handoff/STATE_<branch>.md`
```

---

## Error Recovery

1. **Verification fails** → Re-read step, re-execute with exact strings, re-verify
2. **Gate check fails** → Document in STATE, do not proceed
3. **File content mismatch** → Read file, compare to expected, re-apply edit
4. **Tool not available** → `which [tool]`, install if missing, verify version
5. **Context full** → Update STATE with progress, handoff to fresh agent
