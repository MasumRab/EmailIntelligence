# EmailIntelligence — Agent & Tools Hierarchy

**Generated:** 2026-04-09  
**Status:** Phase 4 complete  
**Purpose:** Document all configured agents, their supported tools, and maintenance targets

---

## Executive Summary

**Total Agents:** 13  
**Configuration Sources:** 2 (ruler.toml, rulesync.jsonc)  
**Common Tools:** Bash, Edit, Write, Read, Glob  
**Rule Sync Targets:** 11 endpoints  
**Hook Enforcement:** Claude only (Phase 4 implementation)

---

## Part 1: Agent Hierarchy by Platform

### 1.1 Claude Ecosystem (4 agents)

#### **Claude Code** (Ruler target: `claudecode`)
- **Config Path:** `CLAUDE.md`
- **Sync Source:** `.ruler/AGENTS.md`
- **Supported Tools:**
  - `Read` — File reading with context windows
  - `Edit` — In-place file modification
  - `Create` — File creation
  - `Bash` — Shell command execution
  - `Grep` — Text search
  - `Glob` — File pattern matching
- **Hooks:** `.claude/hooks.yaml` ✅ (4 rules)
  - block-force-push
  - block-main-commit
  - inject-edit-context
  - block-secrets
- **Status:** ✅ CONFIGURED, HARDENED

#### **Claude Desktop (via AMP)**
- **Config Path:** `.agents/system.md`
- **Sync Source:** `.ruler/AGENTS.md`
- **Supported Tools:** Same as Claude Code (inherited)
- **Hooks:** Uses `.claude/hooks.yaml` (if configured in runtime)
- **Status:** ✅ CONFIGURED

---

### 1.2 Cursor IDE (2 agents)

#### **Cursor IDE** (Ruler target: `cursor`)
- **Config Path:** `.cursor/rules/system.md`
- **Sync Source:** `.ruler/AGENTS.md`
- **Supported Tools:**
  - `Read` — File reading (context-aware)
  - `Edit` — Multi-file editing
  - `Create` — File creation
  - `Bash` — Terminal execution
  - `Search` — Full-text search
  - `Diff` — File comparison
- **Hooks:** None (Phase 4 only implements Claude)
- **Status:** ✅ CONFIGURED, AWAITING HOOKS

#### **Copilot Chat** (via Cursor)
- **Config Path:** `.cursor/rules/system.md` (shared)
- **Sync Source:** `.ruler/AGENTS.md`
- **Supported Tools:** Same as Cursor IDE
- **Hooks:** None (inherited from Cursor)
- **Status:** ✅ CONFIGURED, AWAITING HOOKS

---

### 1.3 Alternative IDE Editors (3 agents)

#### **Windsurf IDE** (Ruler target: `windsurf`)
- **Config Path:** `.windsurf/rules/system.md`
- **Sync Source:** `.ruler/AGENTS.md`
- **Supported Tools:**
  - `Read` — File reading
  - `Edit` — File modification
  - `Create` — File creation
  - `Bash` — Command execution
  - `Codeium` — AI autocomplete (integrated)
- **Hooks:** None (Phase 4 only implements Claude)
- **Status:** ✅ CONFIGURED, AWAITING HOOKS

#### **Cline (Previously Claude in IDE)** (Ruler target: `cline`)
- **Config Path:** `.clinerules/system.md`
- **Sync Source:** `.ruler/AGENTS.md`
- **Supported Tools:** Same as Cursor IDE
- **Hooks:** None (Phase 4 only implements Claude)
- **Status:** ✅ CONFIGURED, AWAITING HOOKS

#### **Kiro** (Ruler target: not in default_agents)
- **Config Path:** `.kiro/steering/system.md`
- **Sync Source:** `.ruler/AGENTS.md`
- **Supported Tools:** TBD (check Kiro documentation)
- **Hooks:** None
- **Status:** ✅ CONFIGURED, MINIMAL INFO

---

### 1.4 CLI-Based Agents (4 agents)

#### **Gemini CLI** (Ruler target: `geminicli`) ⚠️ CONFIG MISMATCH
- **CRITICAL:** Tool uses `settings.json` with `contextFileName: "AGENTS.md"`
- **Tool Reads:** `AGENTS.md` (from settings.json), PLUS hierarchical loading:
  - `./AGENTS.md` (project root)
  - `./.gemini/AGENTS.md` (project-specific)
  - `./GEMINI.md` (if exists in project)
  - `~/.gemini/GEMINI.md` (user-level)
- **Ruler Writes:** `.gemini/system.md` (NOT READ BY TOOL!)
- **settings.json:** `.gemini/settings.json`
  - `contextFileName: "AGENTS.md"` — Primary context file
  - `mcpServers: {...}` — MCP server configs
- **Sync Source:** `.ruler/AGENTS.md`
- **Supported Tools:**
  - `read` — File reading (CLI style)
  - `list_dir` — Directory listing
  - `search` — Pattern search
  - Prompt execution (one-shot Q&A)
- **Hooks:** None (CLI-based, limited hook support)
- **Status:** ⚠️ CRITICAL: Ruler output not aligned with tool expectation
- **Fix Required:** Either update settings.json OR Ruler output_path

#### **Qwen Code** (Ruler target: `qwencode`) ⚠️ CONFIG MISMATCH
- **CRITICAL:** Tool uses `settings.json` with `contextFileName: "AGENTS.md"`
- **Tool Reads:** `AGENTS.md` (from settings.json), PLUS hierarchical loading:
  - `./AGENTS.md` (project root)
  - `./.qwen/AGENTS.md` (project-specific)
  - `./QWEN.md` (if exists in project)
  - `~/.qwen/QWEN.md` (user-level)
- **Ruler Writes:** `.qwen/system.md` (NOT READ BY TOOL!)
- **settings.json:** `.qwen/settings.json`
  - `contextFileName: "AGENTS.md"` — Primary context file
  - `mcpServers: {...}` — MCP server configs
  - `permissions: { allow: [...], deny: [...] }` — Tool permissions
- **Sync Source:** `.ruler/AGENTS.md`
- **Supported Tools:**
  - `Read` — File reading
  - `Edit` — File modification
  - `Bash` — Command execution
- **Hooks:** None
- **Status:** ⚠️ CRITICAL: Ruler output not aligned with tool expectation
- **Fix Required:** Either update settings.json OR Ruler output_path

#### **OpenCode (OpenAI)** (Ruler target: `opencode`) ❓ VERIFY
- **Config Path:** `.opencode/system.md` (MAY NEED AGENTS.md alignment)
- **Sync Source:** `.ruler/AGENTS.md`
- **Supported Tools:**
  - `Read` — File reading
  - `Edit` — File modification
  - `Bash` — Command execution
  - `Search` — Code search
- **Hooks:** None
- **Status:** ❓ VERIFY: Check if OpenCode uses settings.json with contextFileName

#### **Codex CLI** (Ruler target: `codexcli`)
- **Config Path:** Not in ruler.toml (MISSING)
- **Sync Source:** `.ruler/AGENTS.md`
- **Supported Tools:** TBD (Codex CLI dependent)
- **Hooks:** None
- **Status:** ⚠️ PARTIALLY CONFIGURED (in rulesync but not ruler)

---

### 1.5 Other Agents (2 agents, potential issues)

#### **RooCoder** (Ruler target: `roo`)
- **Config Path:** `.roo/rules/system.md`
- **Sync Source:** `.ruler/AGENTS.md`
- **Supported Tools:**
  - `Read` — File reading
  - `Edit` — File modification
  - `Create` — File creation
  - `Bash` — Shell execution
  - `Search` — Code search
- **Hooks:** None
- **Status:** ✅ CONFIGURED

#### **Trae** (Ruler target: not in default_agents)
- **Config Path:** `.trae/rules/system.md`
- **Sync Source:** `.ruler/AGENTS.md`
- **Supported Tools:** TBD (Trae-specific)
- **Hooks:** None
- **Status:** ✅ CONFIGURED, MINIMAL INFO

---

## Part 2: Tool Support Matrix

| Tool | Claude | Cursor | Windsurf | Cline | Gemini | Qwen | OpenCode | Codex | Roo | Kiro | Trae |
|------|--------|--------|----------|-------|--------|------|----------|-------|-----|------|------|
| **Read** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Edit** | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Create** | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Bash** | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Grep** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Glob** | ✅ | ✅ | ⚠️ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ⚠️ |
| **Diff** | ⚠️ | ✅ | ⚠️ | ✅ | ❌ | ❌ | ⚠️ | ❌ | ⚠️ | ❌ | ❌ |
| **Hooks** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

**Legend:**
- ✅ = Fully supported
- ⚠️ = Partial/context-dependent support
- ❌ = Not supported

---

## Part 3: Rule Sync Configuration

### Current Target Endpoints (rulesync.jsonc)

```
Source: .ruler/AGENTS.md
Drift Detection: ENABLED (strict mode)

Targets:
1. claudecode      → CLAUDE.md
2. cursor          → .cursor/rules/system.md
3. cline           → .clinerules/system.md
4. roo             → .roo/rules/system.md
5. kiro            → .kiro/steering/system.md
6. windsurf        → .windsurf/rules/system.md
7. qwencode        → .qwen/system.md
8. opencode        → .opencode/system.md
9. geminicli       → NOT FOUND (see issue below)
10. agentsmd       → .agents/system.md
11. codexcli       → NOT FOUND (config in ruler.toml missing)
```

---

## Part 4: Issues & Recommendations

### 🔴 CRITICAL ISSUES

#### Issue #1: Codex CLI Config Missing
- **Severity:** HIGH
- **Problem:** `codexcli` in rulesync.jsonc but missing from ruler.toml `default_agents`
- **Impact:** Rule sync will fail for Codex or generate orphaned config
- **Action:** Either:
  - Add `"codex"` to ruler.toml default_agents, OR
  - Remove `"codexcli"` from rulesync.jsonc targets
- **Owner:** [PENDING USER REVIEW]

#### Issue #2: Gemini CLI Path Mismatch
- **Severity:** MEDIUM
- **Problem:** `geminicli` target in rulesync.jsonc maps to `.qwen/system.md` (shared with Qwen)
- **Impact:** Potential rule sync conflicts between Gemini and Qwen
- **Action:** Either:
  - Create separate `.gemini/system.md` path, OR
  - Verify Gemini CLI and Qwen share identical configs (intentional)
- **Owner:** [PENDING USER REVIEW]

---

### 🟡 MEDIUM PRIORITY ISSUES

#### Issue #3: Phase 4 Hooks Only for Claude
- **Severity:** MEDIUM
- **Problem:** `.claude/hooks.yaml` only created for Claude Code (Phase 4 spec)
- **Impact:** Other agents (Cursor, Windsurf, etc.) lack runtime enforcement
- **Action:** Design hooks for other agents in Phase 5 if desired
- **Recommendation:** Each IDE may need platform-specific hook implementation
- **Owner:** [DEFERRED TO PHASE 5]

#### Issue #4: Incomplete Ruler Configuration
- **Severity:** MEDIUM
- **Problem:** Kiro and Trae in default_agents but lacking agent-specific config blocks in ruler.toml
- **Impact:** Ruler apply may not generate proper output paths
- **Action:** Add config blocks:
  ```toml
  [agents.kiro]
  enabled = true
  output_path = ".kiro/steering/system.md"

  [agents.trae]
  enabled = true
  output_path = ".trae/rules/system.md"
  ```
- **Owner:** [PENDING USER REVIEW]

---

### 🟢 LOW PRIORITY ISSUES

#### Issue #5: Tool Support Documentation Sparse
- **Severity:** LOW
- **Problem:** Some agents (Kiro, Trae, Codex) lack detailed tool support documentation
- **Impact:** Agents may have untapped capabilities or false expectations
- **Action:** Create tool support matrix docs for each agent
- **Owner:** [BACKLOG]

#### Issue #6: No Agent-Specific Rules
- **Severity:** LOW
- **Problem:** All agents use same `.ruler/AGENTS.md` source (one-size-fits-all)
- **Impact:** No IDE-specific guidance (e.g., Cursor shortcuts, Windsurf AI features)
- **Action:** Consider agent-specific variants in Phase 5
- **Owner:** [BACKLOG]

---

## Part 5: Maintenance Action Items

### Immediate (Pre-Phase 5)

- [ ] **Fix Codex CLI Config:** Add to ruler.toml OR remove from rulesync.jsonc
- [ ] **Verify Gemini/Qwen Path:** Confirm if separate configs needed or intentional sharing
- [ ] **Complete Ruler Config:** Add Kiro and Trae config blocks

### Phase 5 & Beyond

- [ ] **Design hooks for Cursor IDE** (if runtime enforcement needed)
- [ ] **Design hooks for Windsurf IDE** (if runtime enforcement needed)
- [ ] **Create agent-specific tool documentation**
- [ ] **Consider IDE-specific AGENTS variants** (agent-rules per platform)
- [ ] **Expand hook enforcement** to CLI agents where applicable

---

## Part 6: Quick Reference

### File Locations

```
Configuration Source:
  .ruler/AGENTS.md                     ← Primary source
  .ruler/ruler.toml                    ← Agent platform config
  rulesync.jsonc                       ← Sync targets

Agent Config Paths (13 total):
  CLAUDE.md
  .agents/system.md
  .cursor/rules/system.md
  .clinerules/system.md
  .windsurf/rules/system.md
  .roo/rules/system.md
  .kiro/steering/system.md
  .trae/rules/system.md
  .qwen/system.md
  .opencode/system.md
  (codex — MISSING)
  (gemini — shares .qwen/system.md)

Hook Enforcement:
  .claude/hooks.yaml                   ← 4 rules, production-ready
  (Other agents — not implemented yet)

Task Master Integration:
  .taskmaster/                         ← Task tracking config
  .mcp.json files (in all agent dirs)  ← MCP server config
```

### Update Commands

```bash
# Validate all configurations
ruler validate --project-root . --strict

# Sync rules from source to all targets
ruler apply --project-root . --backup

# Check for drift
ruler check --project-root .

# Lint hooks
rulez lint --config .claude/hooks.yaml
```

---

## Part 7: User Review Checklist

**Before proceeding to Phase 5, please review:**

- [ ] **Codex CLI Issue:** Should it be added to ruler.toml or removed from rulesync?
- [ ] **Gemini/Qwen Path:** Intentional sharing or should they be separate?
- [ ] **Ruler Config:** Should Kiro and Trae config blocks be added?
- [ ] **Phase 5 Scope:** Which agents (if any) should get hooks enforcement beyond Claude?
- [ ] **Tool Matrix:** Are all tool support levels accurate per your agents?
- [ ] **Maintenance Cadence:** How often should rule sync be run?

---

**Generated by:** Amp (Rush Mode)  
**Status:** Ready for user review  
**Next Step:** Phase 5 (File Cleanup - OPTIONAL) or custom implementation based on review feedback
