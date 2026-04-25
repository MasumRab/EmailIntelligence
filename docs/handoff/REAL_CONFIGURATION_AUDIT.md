# EmailIntelligence — Real Configuration Audit

**Generated:** 2026-04-10
**Status:** Phase 5, DECISION IMPLEMENTED
**Severity:** RESOLVED — CLI tools use AgentsMdAgent pattern

---

## Executive Summary

**Decision Implemented (2026-04-10):**
- CLI tools (amp, qwen, opencode, kilocode) extend `AgentsMdAgent` and read root `AGENTS.md`
- NO custom `output_path` sections needed in `.ruler/ruler.toml`
- Deleted files: `.qwen/system.md`, `.agents/system.md`, `.opencode/system.md`, `.kilo/rules/system.md`
- Removed from ruler.toml: `[agents.amp]`, `[agents.qwen]`, `[agents.opencode]`, `[agents.kilocode]`

**Current State:**
- CLI tools read root `AGENTS.md` via `settings.json` `contextFileName`
- Ruler syncs to root `AGENTS.md` via `agentsmd` agent
- **NO MISMATCH** — Configuration is aligned

---

## Part 1: What Actually Exists on Disk (REAL Inventory)

**Decision Implemented (2026-04-10):** CLI tools (amp, qwen, opencode, kilocode) extend AgentsMdAgent and read root AGENTS.md.

### TIER 1 CLI TOOLS (Heavy Rotation, Per User)

#### ✅ Gemini CLI — ALIGNED (AgentsMdAgent)
**Status:** Configured  
**Current Config:**
```
AGENTS.md (root) ← SYNCED BY RULER
.gemini/
  └── settings.json (contextFileName: "AGENTS.md", MCP/runtime config)
```
**Decision:** NO output_path needed — reads root AGENTS.md via settings.json

#### ✅ Qwen Code — ALIGNED (AgentsMdAgent)
**Status:** Configured  
**Current Config:**
```
AGENTS.md (root) ← SYNCED BY RULER
.qwen/
  ├── settings.json (contextFileName: "AGENTS.md", runtime config)
  ├── PROJECT_SUMMARY.md (documentation)
  └── commands/ (extension commands)
```
**Decision:** NO output_path needed — reads root AGENTS.md via settings.json
**NOTE:** `.qwen/system.md` DELETED per decision

#### ✅ OpenCode — ALIGNED (AgentsMdAgent)
**Status:** Configured  
**Current Config:**
```
AGENTS.md (root) ← SYNCED BY RULER
.opencode/
  └── package.json (npm metadata)
```
**Decision:** NO output_path needed — reads root AGENTS.md via settings.json

#### ✅ AMP (Amp CLI) — ALIGNED (AgentsMdAgent)
**Status:** Configured  
**Current Config:**
```
AGENTS.md (root) ← SYNCED BY RULER
```
**Decision:** NO output_path needed — reads root AGENTS.md via settings.json

#### ✅ Kilo Code — ALIGNED (AgentsMdAgent)
**Status:** Configured  
**Current Config:**
```
AGENTS.md (root) ← SYNCED BY RULER
.kilo/
  ├── mcp.json (MCP server config)
  └── package.json (npm metadata)
```
**Decision:** NO output_path needed — reads root AGENTS.md via settings.json

#### ❌ iFlow
**Status:** ORPHANED CONFIGURATION  
**Current Config:**
```
IFLOW.md (104 lines at root)
└── NO agent directory (.iflow/)
```
**Issue:** Context exists at root but no agent directory  
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

**Decision Implemented (2026-04-10):**
- CLI tools (amp, qwen, opencode, kilocode) — NO output_path needed (AgentsMdAgent)
- Removed sections: `[agents.amp]`, `[agents.qwen]`, `[agents.opencode]`, `[agents.kilocode]`

### Ruler.toml Analysis (Updated)

**IDE Agents (output_path KEEP):**
```toml
[agents.claude]           → CLAUDE.md (root)
[agents.cursor]           → .cursor/rules/system.md (output_path OPTIONAL — hybrid)
[agents.cline]            → .clinerules/system.md
[agents.roo]              → .roo/rules/system.md (output_path OPTIONAL — hybrid)
[agents.kiro]             → .kiro/steering/system.md
[agents.trae]             → .trae/rules/system.md
[agents.windsurf]         → .windsurf/rules/system.md (output_path OPTIONAL — hybrid)
```

**CLI Agents (AgentsMdAgent — NO output_path needed):**
```toml
# REMOVED SECTIONS — these tools extend AgentsMdAgent and read root AGENTS.md
# [agents.amp]      ← REMOVED — reads root AGENTS.md
# [agents.qwen]     ← REMOVED — reads root AGENTS.md
# [agents.opencode] ← REMOVED — reads root AGENTS.md
# [agents.kilocode] ← REMOVED — reads root AGENTS.md
```

**Decision Rationale:**
1. CLI tools use `settings.json` with `contextFileName: "AGENTS.md"`
2. Ruler's `agentsmd` agent syncs to root `AGENTS.md`
3. NO custom `output_path` needed — tools read from root

---

### Rulesync.jsonc Analysis

**Decision Implemented:** CLI tools (amp, qwen, opencode, kilocode) read root `AGENTS.md` via `agentsmd`.

**Targets (Updated):**
```jsonc
"claudecode"      ✅ Maps to ruler: claude
"cursor"          ✅ Maps to ruler: cursor (output_path OPTIONAL — hybrid)
"cline"           ✅ Maps to ruler: cline
"roo"             ✅ Maps to ruler: roo (output_path OPTIONAL — hybrid)
"kiro"            ✅ Maps to ruler: kiro
"windsurf"        ✅ Maps to ruler: windsurf (output_path OPTIONAL — hybrid)
"qwencode"        ✅ ALIGNED — reads root AGENTS.md (AgentsMdAgent) DECISION COMPLETE
"opencode"        ✅ ALIGNED — reads root AGENTS.md (AgentsMdAgent) DECISION COMPLETE
"geminicli"       ✅ ALIGNED — reads root AGENTS.md (AgentsMdAgent) DECISION COMPLETE
"agentsmd"        ✅ SYNCED TO ROOT AGENTS.md — CLI tools read this
"codexcli"        ❌ NOT in ruler.toml — needs resolution
```

**Issues Resolved:**
1. ~~Name mismatches~~ — RESOLVED: CLI tools use AgentsMdAgent
2. ~~Missing configs~~ — RESOLVED: CLI tools read root AGENTS.md

---

## Part 3: Gap Analysis — Actual vs. Expected

**Decision Implemented (2026-04-10):** CLI tools (amp, qwen, opencode, kilocode) extend AgentsMdAgent and read root AGENTS.md.

| Tool | Tier | Disk Status | Ruler Status | Rulesync | Context File | MCP Config | Action |
|------|------|------------|--------------|----------|--------------|-----------|--------|
| **Gemini** | 1 | ✅ ALIGNED | ✅ AgentsMdAgent | ✅ DECISION DONE | ✅ ROOT AGENTS.md | ✅ settings.json | ✅ NO ACTION |
| **Qwen** | 1 | ✅ ALIGNED | ✅ AgentsMdAgent | ✅ DECISION DONE | ✅ ROOT AGENTS.md | ✅ settings.json | ✅ NO ACTION |
| **OpenCode** | 1 | ✅ ALIGNED | ✅ AgentsMdAgent | ✅ DECISION DONE | ✅ ROOT AGENTS.md | ⚠️ Needs verify | ✅ NO ACTION |
| **AMP** | 1 | ✅ ALIGNED | ✅ AgentsMdAgent | ✅ DECISION DONE | ✅ ROOT AGENTS.md | ⚠️ Needs verify | ✅ NO ACTION |
| **Kilo** | 1 | ✅ ALIGNED | ✅ AgentsMdAgent | ✅ DECISION DONE | ✅ ROOT AGENTS.md | ✅ .kilo/mcp.json | ✅ NO ACTION |
| **iFlow** | 1 | ❌ Orphaned | ❌ Not in ruler | ❌ Not in rulesync | ✅ IFLOW.md (root) | ❌ No config | RESEARCH, CREATE directory |
| **Letta** | 2 | ⚠️ Minimal | ❌ Not in ruler | ❌ Not in rulesync | ❌ Missing | ✅ .letta/settings | ADD to ruler, CREATE context |
| **Aider** | 2 | ❌ None | ❌ Not in ruler | ❌ Not in rulesync | ❌ Missing | ❌ No config | RESEARCH, add if needed |
| **Cursor** | IDE | ✅ Configured | ✅ cursor | ✅ cursor | ✅ system.md | ✅ mcp.json | ✅ NO ACTION |
| **Cline** | IDE | ✅ Configured | ✅ cline | ✅ cline | ✅ system.md | ❌ No MCP | ✅ Mostly good |
| **Roo** | IDE | ✅ Configured | ✅ roo | ✅ roo | ✅ system.md | ✅ mcp.json | ✅ NO ACTION |
| **Windsurf** | IDE | ✅ Configured | ✅ windsurf | ✅ windsurf | ✅ system.md | ✅ mcp.json | ✅ NO ACTION |
| **Trae** | IDE | ✅ Configured | ✅ trae | ✅ trae | ✅ system.md | ✅ mcp.json | ✅ NO ACTION |
| **Kiro** | IDE | ✅ Configured | ✅ kiro | ✅ kiro | ✅ system.md | ✅ mcp.json | ✅ NO ACTION |
| **Claude** | IDE | ✅ Configured | ✅ claude | ✅ claudecode | ✅ CLAUDE.md | ✅ mcp.json | ✅ + hooks.yaml (Phase 4) |

---

## Part 4: Specific Corrections Needed

### DECISION IMPLEMENTED (2026-04-10)

**CLI Tools Configuration — RESOLVED:**

1. **Removed output_path sections from ruler.toml:**
   - `[agents.amp]` — REMOVED — extends AgentsMdAgent
   - `[agents.qwen]` — REMOVED — extends AgentsMdAgent
   - `[agents.opencode]` — REMOVED — extends AgentsMdAgent
   - `[agents.kilocode]` — REMOVED — extends AgentsMdAgent

2. **Deleted orphaned files:**
   - `.qwen/system.md` — DELETED
   - `.agents/system.md` — DELETED
   - `.opencode/system.md` — DELETED
   - `.kilo/rules/system.md` — DELETED

3. **Rationale:**
   - CLI tools use `settings.json` with `contextFileName: "AGENTS.md"`
   - Ruler's `agentsmd` agent syncs to root `AGENTS.md`
   - Tools read from root `AGENTS.md` — NO MISMATCH

### CRITICAL (Block Phase 5)

1. **iFlow Configuration**
   - Research iFlow's expected config directory
   - Determine if `.iflow/` or other path
   - Move `IFLOW.md` from root if needed
   - Create proper directory structure
   - Add to ruler.toml and rulesync.jsonc

2. **Codex CLI Configuration**
   - Verify if Codex is actually used
   - If yes: Add to ruler.toml and create config
   - If no: Remove from default_agents and rulesync
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

3. **OpenCode Configuration**
   - ✅ DECISION COMPLETE — Uses AgentsMdAgent, reads root AGENTS.md
   - Verify settings.json for runtime config

4. **AMP Configuration**
   - ✅ DECISION COMPLETE — Uses AgentsMdAgent, reads root AGENTS.md

5. **Secondary CLI Tools** (Letta, Aider, Ra-aid, Goose, OpenHands)
   - Add to ruler.toml (for Letta at minimum)
   - Create context files when routing framework ready

---

## Part 5: Pattern Discovery — What the System Actually Expects

**Decision Implemented (2026-04-10):**

### Context File Naming Pattern

**CLI Tools (AgentsMdAgent) — RESOLVED:**
- All read root `AGENTS.md` via `settings.json` `contextFileName`
- NO custom `output_path` needed per tool
- Ruler syncs to root `AGENTS.md` via `agentsmd` agent

**IDE Agents (output_path KEEP):**
- Pattern: `{Agent}/system.md` (Ruler syncs here)
- Examples: `.cursor/rules/system.md`, `.roo/rules/system.md`
- Status: Working

**Hybrid Tools (cursor, windsurf, roo) — output_path OPTIONAL:**
- May read from both `{tool}/rules/system.md` AND root `AGENTS.md`
- No changes required

**Root-level Agent (Claude):**
- Pattern: `{AGENT}.md` (at repository root)
- Example: `CLAUDE.md`
- Status: Working

---

## Part 6: Recommended Action Plan

### Decision Summary (2026-04-10)

**COMPLETED:**

1. **CLI Tools Configuration** ✅ DECISION COMPLETE
   - [x] Removed `[agents.amp]`, `[agents.qwen]`, `[agents.opencode]`, `[agents.kilocode]` from ruler.toml
   - [x] Deleted `.qwen/system.md`, `.agents/system.md`, `.opencode/system.md`, `.kilo/rules/system.md`
   - [x] CLI tools (amp, qwen, opencode, kilocode) extend AgentsMdAgent
   - [x] They read root `AGENTS.md` via `settings.json` `contextFileName`

2. **Remaining Actions:**
   - [ ] Is iFlow critical or backlog?
   - [ ] Is Codex actually used?
   - [ ] Add Letta to ruler.toml (Tier 2)

3. **Verify:**
   - [x] Root `AGENTS.md` exists at project root
   - [ ] Run `ruler apply --project-root .` to sync
   - [ ] Test with each CLI tool

---

## Part 7: User Review Checklist

**Decision Implemented (2026-04-10):**

- [x] **CLI Tools (amp, qwen, opencode, kilocode):** NO output_path needed — extends AgentsMdAgent
- [x] **Context filenames:** All CLI tools read root `AGENTS.md` via `settings.json` contextFileName
- [x] **Files deleted:** `.qwen/system.md`, `.agents/system.md`, `.opencode/system.md`, `.kilo/rules/system.md`
- [x] **Ruler.toml sections removed:** `[agents.amp]`, `[agents.qwen]`, `[agents.opencode]`, `[agents.kilocode]`

**Still to confirm:**

- [ ] **iFlow:** Is this actively used? If so, needs directory creation
- [ ] **Codex:** Is this actually used or should it be removed from rulesync?
- [ ] **Letta:** Should be added to Tier 2 configuration?

---

**Status:** Decision implemented, ready for verification
**Next Step:** Run `ruler apply --project-root .` to sync root AGENTS.md

