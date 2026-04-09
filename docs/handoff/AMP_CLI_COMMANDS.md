# AMP CLI Commands for Agent Rules Implementation

**Purpose:** Ready-to-use AMP CLI command strings with correct tool configurations based on actual usage patterns.

**Critical Insight:** Tools like Gemini CLI and Qwen Code use `settings.json` with `contextFileName: "AGENTS.md"` — they may NOT read what Ruler writes (`system.md`)!

**AMP Modes:**
- `rush` — Fast execution, minimal verification
- `deep` — Thorough analysis, comprehensive verification
- `large` — Extended context for complex tasks
- `smart` — Balanced approach (default)

---

## Tool Configuration Matrix

### Tier 1: CLI Tools with settings.json

| Tool | Context Loading | contextFileName | Ruler Output | Status |
|------|-----------------|-----------------|--------------|--------|
| **Gemini CLI** | Hierarchical (AGENTS.md + GEMINI.md) | `AGENTS.md` | `.gemini/system.md` | ⚠️ MISMATCH |
| **Qwen Code** | Hierarchical (AGENTS.md + QWEN.md) | `AGENTS.md` | `.qwen/system.md` | ⚠️ MISMATCH |
| **OpenCode** | `.opencode/OPENCODE.md` | - | `.opencode/system.md` | ❓ VERIFY |
| **Claude Code** | Root `CLAUDE.md` | N/A | `CLAUDE.md` | ✅ ALIGNED |

### Tier 2: IDE Agents (Ruler Aligned)

| Tool | Context Directory | Config Pattern | Status |
|------|-------------------|----------------|--------|
| **Cursor** | `.cursor/rules/` | system.md + rules/*.md | ✅ Working |
| **Roo (Cline)** | `.roo/rules/` | system.md + roo_rules.md | ✅ Working |
| **Windsurf** | `.windsurf/rules/` | system.md + workflows/ | ✅ Working |
| **Trae** | `.trae/rules/` | system.md + trae_rules.md | ✅ Working |
| **Kiro** | `.kiro/steering/` | system.md + kiro_rules.md | ✅ Working |

---

## CRITICAL: contextFileName Mismatch

**Problem**: Gemini and Qwen are configured via `settings.json`:

```json
{
  "contextFileName": "AGENTS.md",
  "mcpServers": { ... },
  "permissions": { "allow": [...], "deny": [...] }
}
```

This means:
- Tool loads `AGENTS.md` from project root or tool directory
- Ruler writes to `{tool}/system.md`
- **MISMATCH**: Tool may NOT read what Ruler writes!

**Solution**: Either:
1. Update `settings.json`: `"contextFileName": "system.md"`
2. Update Ruler: `output_path = ".{tool}/AGENTS.md"`
3. Create symlink: `ln -s system.md .{tool}/AGENTS.md`

---

## amp_phase_0_5: Configuration Audit (NEW - Deep Mode)

**Run BEFORE any other phases to verify correct tool configurations.**

```bash
amp threads new --mode deep --execute "You are auditing AI coding agent tool configurations.

**Critical Document:** docs/handoff/REAL_CONFIGURATION_AUDIT.md

**Tasks:**
0.5.1: Check all settings.json files for contextFileName
0.5.2: Verify context file alignment with Ruler outputs
0.5.3: Check for missing context files in tool directories
0.5.4: Verify MCP server configurations in settings.json
0.5.5: Fix any mismatches found

**Discovery:**
Both Gemini CLI and Qwen Code use contextFileName: 'AGENTS.md' in settings.json.

**Check:**
for f in .gemini/settings.json .qwen/settings.json .claude/settings.json; do
  if [ -f \"\$f\" ]; then
    echo \"=== \$f ===\"
    python3 -c \"import json; d=json.load(open('\$f')); print('contextFileName:', d.get('contextFileName', 'NOT SET'))\"
  fi
done

**Fix Mismatches:**
# Option A: Update settings.json
python3 -c \"import json; d=json.load(open('.qwen/settings.json')); d['contextFileName']='system.md'; json.dump(d, open('.qwen/settings.json','w'), indent=2)\"

# Option B: Create symlink
ln -s system.md .qwen/AGENTS.md

**VERIFY:**
grep 'contextFileName' ./*/settings.json"
```

---

## amp_phase_0: Content Bootstrap (Rush Mode)

```bash
amp threads new --mode rush --execute "You are bootstrapping Agent Rules content from templates.

**Option A: agentrulegen.com (Web UI)**
- URL: https://agentrulegen.com
- Select: Python, FastAPI, React, SQLAlchemy, Pydantic
- Export to: .ruler/AGENTS.md

**Option B: agent-rules-kit (CLI)**
```bash
agent-rules-kit --stack=react --ide=claude --global --auto-install
# Copy generated CLAUDE.md to .ruler/AGENTS.md
cat CLAUDE.md >> .ruler/AGENTS.md && rm CLAUDE.md
```

**CRITICAL for Gemini/Qwen:**
Both tools load AGENTS.md by default (contextFileName: 'AGENTS.md').
Ensure .ruler/AGENTS.md exists at project root before running Ruler.

**VERIFY:**
test -f AGENTS.md && echo 'AGENTS.md: ROOT EXISTS' || echo 'MISSING'
test -f .ruler/AGENTS.md && echo '.ruler/AGENTS.md: EXISTS' || echo 'MISSING'"
```

---

## amp_phase_1: Emergency Fixes (Rush Mode)

```bash
amp threads new --mode rush --execute "You are executing Phase 1 Emergency Fixes.

**Phase Document:** docs/handoff/phase-01-emergency-fixes.md

**Tasks (13 steps):**
1.1-1.2: Resolve CLAUDE.md merge conflict
1.3-1.4: Fix .roo/mcp.json (empty → populated)
1.5-1.6: Fix .cursor/mcp.json (empty → populated)
1.7-1.8: Fix .claude/mcp.json (empty → populated)
1.9-1.10: Fix .windsurf/mcp.json (placeholder keys → env vars)
1.11-1.12: Create .trae/mcp.json
1.13: Delete .rules file

**settings.json Pattern (for Gemini/Qwen):**
```json
{
  \"contextFileName\": \"AGENTS.md\",
  \"mcpServers\": {
    \"task-master-ai\": {
      \"command\": \"npm\",
      \"args\": [\"exec\", \"task-master-ai\"],
      \"env\": {
        \"GOOGLE_API_KEY\": \"\${GOOGLE_API_KEY}\",
        \"GITHUB_API_KEY\": \"\${GITHUB_API_KEY}\"
      }
    }
  },
  \"permissions\": {
    \"allow\": [\"Bash(git *)\"],
    \"deny\": [\"Read(credentials/)\"]
  }
}
```

**Critical Rules:**
1. Run VERIFY after EVERY step
2. Copy strings EXACTLY from phase document
3. NEVER use git add -A

**Start:** Read docs/handoff/phase-01-emergency-fixes.md"
```

---

## amp_phase_2: Content Fixes (Rush Mode)

```bash
amp threads new --mode rush --execute "You are executing Phase 2 Content Fixes.

**Phase Document:** docs/handoff/phase-02-content-fixes.md

**Tasks (8 steps):**
2.1-2.3: Fix Windsurf dev_workflow.md bugs
2.4-2.6: Fix Prisma references (project doesn't use Prisma)
2.7: Update rulesync.jsonc targets
2.8: Verify all content fixes

**Critical Rules:**
1. Run VERIFY after EVERY step
2. Copy strings EXACTLY from phase document
3. NEVER use git add -A

**Start:** Read docs/handoff/phase-02-content-fixes.md"
```

---

## amp_phase_3: Ruler Setup (Rush Mode)

```bash
amp threads new --mode rush --execute "You are executing Phase 3 Ruler Setup.

**Phase Document:** docs/handoff/phase-03-ruler-setup.md
**Config File:** .ruler/ruler.toml
**Source File:** .ruler/AGENTS.md

**CRITICAL: Align Ruler outputs with tool expectations!**

For tools with settings.json (Gemini, Qwen):
- They read contextFileName from settings.json
- Default: contextFileName: 'AGENTS.md'
- Ruler must write to matching path

**Fix: Option A** — Update Ruler output_path:
```toml
[agents.qwen]
output_path = \".qwen/AGENTS.md\"  # Match settings.json contextFileName
```

**Fix: Option B** — Update settings.json:
```json
{ \"contextFileName\": \"system.md\" }
```

**Tasks (6 steps):**
3.1: Verify .ruler/ exists
3.2: Create .ruler/AGENTS.md
3.3: Create .ruler/ruler.toml with correct output_paths
3.4: Verify Ruler config (dry-run)
3.5: Apply Ruler
3.6: Verify each tool reads the correct file

**Commands:**
ruler apply --project-root . --dry-run 2>&1 | head -10
ruler apply --project-root . --backup

**VERIFY for each tool:**
# Check settings.json contextFileName
grep contextFileName .gemini/settings.json .qwen/settings.json

# Check Ruler output
grep 'output_path' .ruler/ruler.toml

# Check alignment
python3 -c \"
import json
for tool in ['gemini', 'qwen']:
    s = json.load(open(f'.{tool}/settings.json'))
    ctx = s.get('contextFileName', 'NOT SET')
    print(f'{tool}: reads {ctx}')
\"

**Start:** Read docs/handoff/phase-03-ruler-setup.md"
```

---

## amp_phase_4: Agent RuleZ Setup (Rush Mode)

```bash
amp threads new --mode rush --execute "You are executing Phase 4 Agent RuleZ Setup.

**Phase Document:** docs/handoff/phase-04-agent-rulez.md

**STATUS:** rulez binary already installed (v2.3.0 at ~/.local/bin/rulez)

**Tasks (5 steps — Step 4.1 COMPLETE):**
4.1: ✅ Install rulez binary (ALREADY DONE)
4.2: Create .claude/hooks.yaml
4.3: Validate hooks.yaml
4.4: Lint hooks.yaml
4.5: Debug test: force push blocked
4.6: Debug test: normal commit allowed

**Commands:**
which rulez  # → ~/.local/bin/rulez
rulez --version  # → rulez 2.3.0
rulez validate --config .claude/hooks.yaml
rulez debug --event 'Bash:git push --force origin main'

**Start with Step 4.2:** Read docs/handoff/phase-04-agent-rulez.md"
```

---

## amp_phase_5: Context File Alignment (Deep Mode)

**NEW PHASE — Critical for Gemini/Qwen**

```bash
amp threads new --mode deep --execute "You are fixing context file mismatches.

**Discovery:**
- Gemini CLI: contextFileName = 'AGENTS.md' in .gemini/settings.json
- Qwen Code: contextFileName = 'AGENTS.md' in .qwen/settings.json
- But Ruler writes to: .gemini/system.md and .qwen/system.md

**Tasks:**
5.1: Check current contextFileName values
5.2: Decide fix strategy per tool (update settings.json OR Ruler)
5.3: Apply fixes
5.4: Verify tool reads correct file
5.5: Test with actual tool invocation

**Check:**
bash ~/.letta/skills/agent-rules-handoff/scripts/audit_tool_configs.sh

**Fix Example (update settings.json):**
python3 -c \"
import json
d = json.load(open('.qwen/settings.json'))
d['contextFileName'] = 'system.md'
json.dump(d, open('.qwen/settings.json', 'w'), indent=2)
\"

**VERIFY:**
cat .qwen/settings.json | grep contextFileName
# Should show: 'contextFileName': 'system.md'

**Alternative: Update Ruler:**
# Edit .ruler/ruler.toml
[agents.qwen]
output_path = \".qwen/AGENTS.md\"

ruler apply --project-root . --dry-run
ruler apply --project-root ."
```

---

## amp_gate_check: Run Gate Check (Deep Mode)

```bash
amp threads new --mode deep --execute "You are running a Phase Gate Check.

**Phase:** [PHASE_NUMBER]

**Gate Check Commands:**
echo '=== PHASE [N] GATE CHECK ==='

# File existence checks
for f in [FILES_TO_CHECK]; do
  test -f \"\$f\" && echo '✅ '\$f': EXISTS' || echo '❌ '\$f': MISSING'
done

# contextFileName alignment check
for tool in gemini qwen opencode; do
  settings=\".\$tool/settings.json\"
  if [ -f \"\$settings\" ]; then
    ctx=\$(python3 -c \"import json; print(json.load(open('\$settings')).get('contextFileName', 'NOT SET'))\")
    echo \"\$tool: reads \$ctx\"
  fi
done

**Report results in format:**
## Phase [N] Gate Check Results
- File X: PASS/FAIL
- Overall: PASS/FAIL"
```

---

## Mode Usage Guidelines

| Phase | Recommended Mode | Reason |
|-------|------------------|--------|
| **Phase 0.5** (NEW) | `deep` | Configuration audit requires thoroughness |
| Phase 0 | `rush` | Quick template generation |
| Phase 1 | `rush` | Fast fixes, clear verification |
| Phase 2 | `rush` | Content edits, fast execution |
| Phase 3 | `rush` | Ruler apply is straightforward |
| Phase 4 | `rush` | RuleZ debug is fast |
| **Phase 5** (NEW) | `deep` | Context alignment critical |
| Phase 9 | `deep` | Comprehensive verification |

---

## Quick Reference

```bash
# Create Rush mode session
amp threads new --mode rush --execute "[PROMPT]"

# Create Deep mode session
amp threads new --mode deep --execute "[PROMPT]"

# Continue last thread
amp threads continue --last

# List threads
amp threads list
```

---

## Tool-Specific CLI Commands

### Claude Code
```bash
claude --version  # Check version
cat CLAUDE.md      # Verify context file at root
```

### Gemini CLI
```bash
gemini  # Runs in interactive mode
# Check settings.json for:
# - contextFileName: "AGENTS.md" (hierarchical loading)
# - mcpServers: MCP server configs
cat .gemini/settings.json
```

### Qwen Code
```bash
qwen  # Runs in interactive mode
# Check settings.json for:
# - contextFileName: "AGENTS.md"
# - permissions: allow/deny lists
# - mcpServers: MCP configs
cat .qwen/settings.json
```

### Ruler (Distribution)
```bash
ruler apply --project-root . --dry-run
ruler apply --project-root . --backup
ruler --version
```

### Agent RuleZ (Runtime Hooks)
```bash
rulez --version      # Check installed version
rulez validate        # Validate hooks.yaml
rulez lint           # Check for rule overlaps
rulez debug --event 'Bash:git push --force origin main'
```
