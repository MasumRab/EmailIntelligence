# EmailIntelligence — Real Configuration Audit

**Generated:** 2026-04-10  
**Status:** Pre-Phase 5, CRITICAL GAP ANALYSIS  
**Severity:** HIGH — Default configs used instead of tool-specific analysis

---

## Executive Summary

**The Problem:** Phases 1-4 relied on Ruler defaults and template assumptions instead of auditing what was ACTUALLY configured on this system.

**Result:** Configuration mismatches between:
- What Ruler **expects** to write
- What tools **actually expect** to read
- What's **actually on disk**

**Examples:**
- Ruler writes to `.qwen/system.md` but you said `.qwen/QWEN.md` is correct
- `.gemini-cli` in ruler.toml but `.gemini` directory exists
- `geminicli` in rulesync.jsonc but no config created yet
- Kilo has `.kilo/mcp.json` but no rules synced

---

## Part 1: What Actually Exists on Disk (REAL Inventory)

### TIER 1 CLI TOOLS (Heavy Rotation, Per User)

#### ✅ Gemini CLI
**Status:** Minimally configured  
**Current Config:**
```
.gemini/
  ├── settings.json (MCP/runtime config)
  └── NO context files
```
**Missing:** `.gemini/GEMINI.md` (context/instructions)  
**Ruler expects:** `gemini-cli` agent → `.gemini/system.md` (WRONG PATH)  
**Action:** Create `.gemini/GEMINI.md` with proper context

#### ✅ Qwen Code
**Status:** Partially configured  
**Current Config:**
```
.qwen/
  ├── settings.json (runtime config)
  ├── system.md (22KB, auto-generated/synced)
  ├── PROJECT_SUMMARY.md (documentation)
  └── commands/ (extension commands)
```
**Issue:** Has `.qwen/system.md` but user says `.qwen/QWEN.md` is correct  
**Ruler expects:** `qwen` agent → `.qwen/system.md` (MATCHES current)  
**Question:** Should `.qwen/system.md` be renamed to `.qwen/QWEN.md`?  
**Action:** Clarify if system.md should be QWEN.md

#### ✅ OpenCode
**Status:** Minimally configured  
**Current Config:**
```
.opencode/
  ├── package.json (npm metadata)
  └── NO rules or context
```
**Missing:** `.opencode/OPENCODE.md` (context/instructions)  
**Ruler expects:** `opencode` agent → `.opencode/system.md`  
**Action:** Create `.opencode/OPENCODE.md` with proper context

#### ⚠️ AMP (Amp CLI)
**Status:** NOT CONFIGURED  
**Current Config:**
```
.agents/
  └── system.md (synced, no other config)
```
**Context:** User mentioned AMP as primary (in heavy rotation)  
**Ruler expects:** `amp` agent → `.agents/system.md` (EXISTS)  
**Note:** AMP likely uses Claude context, verify if `.agents/` is correct root  
**Action:** Confirm if AMP needs separate `.amp/` directory

#### ❌ Kilo Code
**Status:** PARTIALLY CONFIGURED, NOT IN RULER  
**Current Config:**
```
.kilo/
  ├── mcp.json (MCP server config)
  ├── package.json (npm metadata)
  └── NO rules or context
```
**Issue:** Not in `ruler.toml` default_agents  
**Missing:** `.kilo/system.md` or `.kilo/KILO.md`  
**Ruler Status:** Has `[agents.kilo]` section commented out or missing  
**Action:** Add Kilo to ruler.toml, create context file

#### ❌ iFlow
**Status:** ORPHANED CONFIGURATION  
**Current Config:**
```
IFLOW.md (104 lines at root)
└── NO agent directory (.iflow/)
```
**Issue:** Context exists at root but no agent directory  
**Ruler Status:** Not in ruler.toml, not in rulesync  
**Action:** Determine iFlow's expected directory, create `.iflow/` with config

---

### TIER 2 CLI TOOLS (Awaiting API/Provider Routing)

#### ✅ Letta (Memory-Augmented Agent)
**Status:** Minimally configured  
**Current Config:**
```
.letta/
  ├── settings.json
  ├── settings.local.json
  └── NO rules or context
```
**Ruler Status:** Not in ruler.toml  
**Action:** Add to ruler.toml, create `.letta/LETTA.md`

#### ❌ Aider
**Status:** NOT CONFIGURED (variant exists in EmailIntelligenceAider branch)  
**Current Config:** None in this repo  
**Ruler Status:** Not in ruler.toml  
**Action:** Determine if needed, create `.aider/AIDER.md` if so

#### ❌ Ra-aid
**Status:** NOT CONFIGURED  
**Current Config:** None  
**Ruler Status:** Not in ruler.toml  
**Action:** Research expected config, create if needed

#### ❌ Goose CLI
**Status:** NOT CONFIGURED  
**Current Config:** None  
**Ruler Status:** Not in ruler.toml  
**Action:** Research expected config, create if needed

#### ❌ OpenHands
**Status:** NOT CONFIGURED  
**Current Config:** None  
**Ruler Status:** Not in ruler.toml  
**Action:** Research expected config, create if needed

---

### IDE AGENTS (Secondary Priority)

#### ✅ Cursor IDE
**Status:** CONFIGURED  
**Current Config:**
```
.cursor/
  ├── mcp.json (MCP servers)
  └── rules/system.md (synced from Ruler)
```
**Ruler Status:** In ruler.toml → `.cursor/rules/system.md`  
**Status:** ✅ Working as configured

#### ✅ Cline (Previously Claude in IDE)
**Status:** FULLY CONFIGURED (Most complex)  
**Current Config:**
```
.clinerules/
  ├── cline_rules.md
  ├── dev_workflow.md
  ├── self_improve.md
  ├── system.md (synced)
  └── taskmaster.md
```
**Ruler Status:** In ruler.toml → `.clinerules/system.md`  
**Status:** ✅ Working as configured

#### ✅ RooCoder
**Status:** FULLY CONFIGURED  
**Current Config:**
```
.roo/
  ├── mcp.json
  ├── commands/ (Speckit workflows)
  ├── rules/ (5 markdown files)
  │   ├── dev_workflow.md
  │   ├── roo_rules.md
  │   ├── system.md (synced)
  │   ├── taskmaster.md
  │   └── self_improve.md
```
**Ruler Status:** In ruler.toml → `.roo/rules/system.md`  
**Status:** ✅ Working as configured

#### ✅ Windsurf IDE
**Status:** FULLY CONFIGURED  
**Current Config:**
```
.windsurf/
  ├── mcp.json
  ├── mcp_config.json
  ├── workflows/ (Speckit workflows, 9 files)
  └── rules/ (5 markdown files)
      ├── dev_workflow.md
      ├── system.md (synced)
      ├── taskmaster.md
      ├── windsurf_rules.md
      └── self_improve.md
```
**Ruler Status:** In ruler.toml → `.windsurf/rules/system.md`  
**Status:** ✅ Working as configured

#### ✅ Trae AI
**Status:** FULLY CONFIGURED  
**Current Config:**
```
.trae/
  ├── mcp.json
  └── rules/ (5 markdown files)
      ├── dev_workflow.md
      ├── system.md (synced)
      ├── taskmaster.md
      ├── trae_rules.md
      └── self_improve.md
```
**Ruler Status:** In ruler.toml → `.trae/rules/system.md`  
**Status:** ✅ Working as configured

#### ✅ Kiro
**Status:** FULLY CONFIGURED  
**Current Config:**
```
.kiro/
  ├── steering/ (direction/control files)
  │   ├── dev_workflow.md
  │   ├── kiro_rules.md
  │   ├── system.md (synced)
  │   ├── taskmaster.md
  │   ├── taskmaster_hooks_workflow.md
  │   └── self_improve.md
  └── settings/ (runtime config)
      └── mcp.json
```
**Ruler Status:** In ruler.toml → `.kiro/steering/system.md`  
**Status:** ✅ Working as configured

#### ❌ Claude Code (NOT IDE)
**Status:** Root-level config  
**Current Config:**
```
CLAUDE.md (at repository root, auto-generated)
```
**Ruler expects:** `claude` agent → `CLAUDE.md` (ROOT)  
**Status:** ✅ Synced correctly

#### ⚠️ Copilot/GitHub
**Status:** Uses Claude config  
**Note:** Shares `.claude/` context with Claude Code  
**Status:** ⚠️ Inherits from Claude

---

## Part 2: What Ruler Thinks It Should Do

### Ruler.toml Analysis

**Configured Agents (13 total):**
```toml
[agents.claude]           → CLAUDE.md (root)
[agents.cursor]           → .cursor/rules/system.md
[agents.cline]            → .clinerules/system.md
[agents.roo]              → .roo/rules/system.md
[agents.kiro]             → .kiro/steering/system.md
[agents.trae]             → .trae/rules/system.md
[agents.windsurf]         → .windsurf/rules/system.md
[agents.amp]              → .agents/system.md
[agents.qwen]             → .qwen/system.md ← MISMATCH?
[agents.opencode]         → .opencode/system.md
(MISSING)                 → .gemini/system.md ← NOT IN CONFIG
(MISSING)                 → .kilo/system.md ← NOT IN CONFIG
(MISSING)                 → .agents/AGENTS.md ← NOT FOR AMP
```

**Issues:**
1. **`gemini-cli` in default_agents** but NO `[agents.gemini-cli]` section
2. **`amp` maps to `.agents/system.md`** — Is this correct for AMP or generic?
3. **`qwen` maps to `.qwen/system.md`** — You said `.qwen/QWEN.md` is correct
4. **`codex` in default_agents** but NO `[agents.codex]` section

---

### Rulesync.jsonc Analysis

**Targets (11 specified):**
```jsonc
"claudecode"      ✅ Maps to ruler: claude
"cursor"          ✅ Maps to ruler: cursor
"cline"           ✅ Maps to ruler: cline
"roo"             ✅ Maps to ruler: roo
"kiro"            ✅ Maps to ruler: kiro
"windsurf"        ✅ Maps to ruler: windsurf
"qwencode"        ❓ Maps to ruler: qwen (name mismatch)
"opencode"        ✅ Maps to ruler: opencode
"geminicli"       ❌ NOT in ruler.toml
"agentsmd"        ❓ Maps to ruler: amp (unclear)
"codexcli"        ❌ NOT in ruler.toml
```

**Issues:**
1. **Name mismatches:** `geminicli` vs Ruler's `gemini-cli`
2. **Missing configs:** `geminicli` and `codexcli` not in ruler.toml
3. **Unclear purpose:** `agentsmd` — Is it for AMP or generic AGENTS.md?

---

## Part 3: Gap Analysis — Actual vs. Expected

| Tool | Tier | Disk Status | Ruler Status | Rulesync | Context File | MCP Config | Action |
|------|------|------------|--------------|----------|--------------|-----------|--------|
| **Gemini** | 1 | ⚠️ Minimal | ❌ `gemini-cli` wrong name | ❌ `geminicli` orphaned | ❌ Missing | ✅ settings.json | CREATE `.gemini/GEMINI.md` |
| **Qwen** | 1 | ✅ Configured | ✅ `qwen` | ✅ `qwencode` | ⚠️ system.md vs QWEN.md? | ✅ settings.json | VERIFY naming, rename if needed |
| **OpenCode** | 1 | ⚠️ Minimal | ✅ `opencode` | ✅ `opencode` | ❌ Missing | ❌ No config | CREATE `.opencode/OPENCODE.md` |
| **AMP** | 1 | ⚠️ Minimal | ✅ `amp` | ✅ `agentsmd` | ⚠️ Inherited | ❌ In `.agents/` | CLARIFY if `.amp/` needed |
| **Kilo** | 1 | ⚠️ Minimal | ❌ Not in ruler | ❌ Not in rulesync | ❌ Missing | ✅ .kilo/mcp.json | ADD to ruler, CREATE context |
| **iFlow** | 1 | ❌ Orphaned | ❌ Not in ruler | ❌ Not in rulesync | ✅ IFLOW.md (root) | ❌ No config | RESEARCH, CREATE directory |
| **Letta** | 2 | ⚠️ Minimal | ❌ Not in ruler | ❌ Not in rulesync | ❌ Missing | ✅ .letta/settings | ADD to ruler, CREATE context |
| **Aider** | 2 | ❌ None | ❌ Not in ruler | ❌ Not in rulesync | ❌ Missing | ❌ No config | RESEARCH, add if needed |
| **Cursor** | IDE | ✅ Configured | ✅ cursor | ✅ cursor | ✅ system.md | ✅ mcp.json | ✅ No action |
| **Cline** | IDE | ✅ Configured | ✅ cline | ✅ cline | ✅ system.md | ❌ No MCP | ✅ Mostly good |
| **Roo** | IDE | ✅ Configured | ✅ roo | ✅ roo | ✅ system.md | ✅ mcp.json | ✅ No action |
| **Windsurf** | IDE | ✅ Configured | ✅ windsurf | ✅ windsurf | ✅ system.md | ✅ mcp.json | ✅ No action |
| **Trae** | IDE | ✅ Configured | ✅ trae | ✅ trae | ✅ system.md | ✅ mcp.json | ✅ No action |
| **Kiro** | IDE | ✅ Configured | ✅ kiro | ✅ kiro | ✅ system.md | ✅ mcp.json | ✅ No action |
| **Claude** | IDE | ✅ Configured | ✅ claude | ✅ claudecode | ✅ CLAUDE.md | ✅ mcp.json | ✅ + hooks.yaml (Phase 4) |

---

## Part 4: Specific Corrections Needed

### CRITICAL (Block Phase 5)

1. **Gemini CLI Configuration**
   - Add to ruler.toml: `[agents.gemini]` (fix name: not `gemini-cli`)
   - Update rulesync.jsonc: Change `geminicli` → `gemini`
   - Create `.gemini/GEMINI.md`
   - Question: Should also create `.gemini/system.md` (override) or just GEMINI.md?

2. **Qwen Configuration Naming**
   - Clarify: Is `.qwen/system.md` correct or should it be `.qwen/QWEN.md`?
   - If renaming needed: system.md → QWEN.md
   - Update ruler.toml output_path accordingly

3. **Kilo Configuration**
   - Add to ruler.toml:
     ```toml
     [agents.kilo]
     enabled = true
     output_path = ".kilo/KILO.md"
     ```
   - Add to rulesync.jsonc targets: `"kilo"`
   - Create `.kilo/KILO.md`

4. **iFlow Configuration**
   - Research iFlow's expected config directory
   - Determine if `.iflow/` or other path
   - Move `IFLOW.md` from root if needed
   - Create proper directory structure
   - Add to ruler.toml and rulesync.jsonc

### HIGH PRIORITY (Phase 5)

5. **OpenCode Configuration**
   - Create `.opencode/OPENCODE.md`
   - Verify settings.json for runtime config

6. **AMP Configuration**
   - Clarify: Is `.agents/` correct or should `.amp/` be used?
   - Create `.agents/AMP.md` or `.amp/AMP.md`

7. **Codex CLI Configuration**
   - Verify if Codex is actually used
   - If yes: Add to ruler.toml and create config
   - If no: Remove from default_agents and rulesync

8. **Secondary CLI Tools** (Letta, Aider, Ra-aid, Goose, OpenHands)
   - Add to ruler.toml (for Letta at minimum)
   - Create context files when routing framework ready

---

## Part 5: Pattern Discovery — What the System Actually Expects

### Context File Naming Pattern

Based on what exists on disk:

**IDE Agents (Configured):**
- Pattern: `{Agent}/system.md` (Ruler syncs here)
- Examples: `.cursor/rules/system.md`, `.roo/rules/system.md`
- Status: Working

**Root-level Agent (Claude):**
- Pattern: `{AGENT}.md` (at repository root)
- Example: `CLAUDE.md`
- Status: Working

**CLI Tools (Partial):**
- Gemini expects: `.gemini/GEMINI.md` (hierarchical context loading)
- Qwen expects: `.qwen/QWEN.md` (or system.md?)
- OpenCode expects: `.opencode/OPENCODE.md`
- iFlow expects: `IFLOW.md` or `.iflow/IFLOW.md`?

**Ruler Output Pattern Inconsistency:**
- Ruler writes to: `.{agent}/system.md` (generic)
- But tools expect: `.{AGENT}/{AGENT}.md` or custom names
- **This is the core mismatch**

---

## Part 6: Recommended Action Plan

### Phase 0.5 (NEW) — Configuration Audit & Alignment

**Before touching any more phases, execute:**

1. **User Input Required:**
   - [ ] Confirm correct context filenames:
     - `.gemini/GEMINI.md` or `.gemini/system.md`?
     - `.qwen/QWEN.md` or `.qwen/system.md`?
     - `.kilo/KILO.md` or `.kilo/system.md`?
     - `.opencode/OPENCODE.md` or `.opencode/system.md`?
     - `.amp/AMP.md` or `.agents/AMP.md`?
   
   - [ ] Is iFlow critical or backlog?
   - [ ] Is Codex actually used?
   - [ ] Is AMP primary or inherited from Claude?

2. **Update Ruler Configuration:**
   - Fix agent names in ruler.toml
   - Fix output_path to match actual tool expectations
   - Add missing agents (Kilo, iFlow, Letta, etc.)

3. **Fix Rulesync Configuration:**
   - Update target names to match ruler.toml agent names
   - Remove orphaned targets (geminicli if no config, codexcli if unused)
   - Add Kilo, iFlow, Letta targets

4. **Create Missing Context Files:**
   - `.gemini/GEMINI.md`
   - `.opencode/OPENCODE.md`
   - `.kilo/KILO.md`
   - `.iflow/IFLOW.md` (pending clarification)
   - Update AMP context (`.agents/AMP.md` or `.amp/AMP.md`)

5. **Verify & Test:**
   - Run `ruler apply --dry-run` to preview changes
   - Verify all output_paths exist
   - Test with each tool

---

## Part 7: User Review Checklist

Before proceeding, please confirm:

- [ ] **Gemini:** Should context be `.gemini/GEMINI.md` or Ruler's `.gemini/system.md`?
- [ ] **Qwen:** Rename `.qwen/system.md` to `.qwen/QWEN.md`? Or keep as is?
- [ ] **Kilo:** Is it a Tier 1 primary tool requiring full config?
- [ ] **iFlow:** Is this active? Expected directory path?
- [ ] **AMP:** Is `.agents/` the correct location or should `.amp/` be used?
- [ ] **Codex:** Is this actually used or should it be removed from defaults?
- [ ] **Letta:** Should be added to Tier 2 configuration?
- [ ] **Naming Pattern:** Should all CLI tools use `{TOOL}/{TOOL}.md` or accept Ruler's `{tool}/system.md`?

---

**Status:** Awaiting user clarification  
**Next Step:** Phase 0.5 execution based on answers above

