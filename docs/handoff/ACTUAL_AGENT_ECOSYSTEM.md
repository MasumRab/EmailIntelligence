# EmailIntelligence — Actual Agent Ecosystem (CLI-First)

**Generated:** 2026-04-10  
**Status:** Phase 4 COMPLETE, PHASE 0 REQUIREMENTS MISALIGNED  
**Priority:** HIGH — Major restructuring needed for Phases 0-5

---

## CRITICAL FINDING: CLI-First Workflow, Not IDE-First

### What Phase 0-4 Assumed
```
IDE-First Model:
  Claude Code (primary) → Cursor/Windsurf/Cline (secondary) → CLI tools (tertiary)
  
Result: CLAUDE.md emphasized, Cursor/Windsurf rules synced, CLI tools ignored
```

### Actual Workflow (User Input)
```
CLI-First Model:
  PRIMARY CLI (heavy rotation) → SECONDARY CLI (waiting for routing) → IDE agents (rare)
  
Gemini/Qwen/OpenCode/AMP/Kilo/iFlow → Aider/Ra-aid/Goose/Letta → Cursor/Claude/Cline/Roo
```

**Impact:** Everything from Phase 1-4 is **backwards prioritization**.

---

## Part 1: Actual Agent Ecosystem (Complete Map)

### TIER 1: PRIMARY CLI TOOLS (Heavy Rotation, Last 2 Months)

**Decision Implemented (2026-04-10):** CLI tools (amp, qwen, opencode, kilocode) extend `AgentsMdAgent` and read root `AGENTS.md` via `settings.json` `contextFileName`. NO custom `output_path` sections in `.ruler/ruler.toml` — uses Ruler built-in defaults.

#### 1. Gemini CLI ✅ ALIGNED (AgentsMdAgent)
- **Status:** ✅ Primary coding tool
- **Context Loading:** `settings.json` with `contextFileName: "AGENTS.md"`
  - **Tool reads:** Root `AGENTS.md`
  - **Ruler syncs:** Root `AGENTS.md` via `agentsmd` agent
  - **ALIGNED:** Tool reads what Ruler writes!
- **settings.json Location:** `.gemini/settings.json`
- **Hook Status:** ❌ NO HOOKS
- **Decision:** NO `output_path` section needed — uses Ruler's built-in `agentsmd`

#### 2. Qwen Code ✅ ALIGNED (AgentsMdAgent)
- **Status:** ✅ Primary coding tool
- **Context Loading:** `settings.json` with `contextFileName: "AGENTS.md"`
  - **Tool reads:** Root `AGENTS.md`
  - **Ruler syncs:** Root `AGENTS.md` via `agentsmd` agent
  - **ALIGNED:** Tool reads what Ruler writes!
- **settings.json Location:** `.qwen/settings.json`
- **Hook Status:** ❌ NO HOOKS
- **Decision:** NO `output_path` section needed — uses Ruler's built-in `agentsmd`

#### 3. OpenCode (OpenAI) ✅ ALIGNED (AgentsMdAgent)
- **Status:** ✅ Primary coding tool
- **Context Loading:** `settings.json` with `contextFileName: "AGENTS.md"`
  - **Tool reads:** Root `AGENTS.md`
  - **Ruler syncs:** Root `AGENTS.md` via `agentsmd` agent
  - **ALIGNED:** Tool reads what Ruler writes!
- **Hook Status:** ❌ NO HOOKS
- **Decision:** NO `output_path` section needed — uses Ruler's built-in `agentsmd`

#### 4. AMP (Amp CLI) ✅ ALIGNED (AgentsMdAgent)
- **Status:** ✅ Primary coding tool (this session using AMP)
- **Context Loading:** Reads root `AGENTS.md` via `settings.json` contextFileName
  - **Tool reads:** Root `AGENTS.md`
  - **Ruler syncs:** Root `AGENTS.md` via `agentsmd` agent
  - **ALIGNED:** Tool reads what Ruler writes!
- **Hook Status:** ❌ NO HOOKS
- **Decision:** NO `output_path` section needed — uses Ruler's built-in `agentsmd`

#### 5. Kilo (Kilo Code) ✅ ALIGNED (AgentsMdAgent)
- **Status:** ✅ Primary coding tool
- **Context Loading:** Reads root `AGENTS.md` via `settings.json` contextFileName
  - **Tool reads:** Root `AGENTS.md`
  - **Ruler syncs:** Root `AGENTS.md` via `agentsmd` agent
  - **ALIGNED:** Tool reads what Ruler writes!
- **Hook Status:** ❌ NO HOOKS
- **Decision:** NO `output_path` section needed — uses Ruler's built-in `agentsmd`

#### 6. iFlow
- **Status:** ✅ Primary coding tool
- **Current Config:** NOT FOUND
- **Hook Status:** ❌ NO CONFIG, NO HOOKS
- **Recommendation:**
  - Determine iFlow config location
  - Add to ruler.toml
  - Create rules + hooks
  - CRITICAL PRIORITY — missing entirely

---

### TIER 2: SECONDARY CLI TOOLS (Waiting for API/Provider Routing)

#### 7. Aider
- **Status:** 🟢 In queue (awaiting routing framework)
- **Current Config:** Variant exists (`EmailIntelligenceAider` branch)
- **Hook Status:** ❌ NO HOOKS
- **Recommendation:**
  - Create `.aider/system.md`
  - Create `.aider/hooks.yaml` (once routing ready)
  - MEDIUM PRIORITY — deferred to Phase 5

#### 8. Ra-aid (Ra.aid)
- **Status:** 🟢 In queue
- **Current Config:** NOT FOUND
- **Hook Status:** ❌ NO CONFIG
- **Recommendation:**
  - Research ra.aid CLI structure
  - Create `.ra-aid/system.md`
  - MEDIUM PRIORITY

#### 9. Goose CLI
- **Status:** 🟢 In queue
- **Current Config:** NOT FOUND
- **Hook Status:** ❌ NO CONFIG
- **Recommendation:**
  - Create `.goose/system.md`
  - MEDIUM PRIORITY

#### 10. Oh-My-Pi (OMP)
- **Status:** 🟢 In queue
- **Current Config:** NOT FOUND
- **Hook Status:** ❌ NO CONFIG
- **Recommendation:**
  - Create `.omp/system.md`
  - MEDIUM PRIORITY

#### 11. Letta
- **Status:** 🟢 In queue (memory-augmented agent framework)
- **Current Config:** `.letta/` directory exists (but unconfigured)
- **Hook Status:** ❌ NO HOOKS
- **Recommendation:**
  - Create `.letta/system.md`
  - Create `.letta/hooks.yaml`
  - MEDIUM PRIORITY

#### 12. OpenHands
- **Status:** 🟢 In queue
- **Current Config:** NOT FOUND
- **Hook Status:** ❌ NO CONFIG
- **Recommendation:**
  - Create `.openhands/system.md`
  - MEDIUM PRIORITY

---

### TIER 3: TERTIARY CLI TOOLS (Limited Ecosystem, Low Priority)

#### 13-19. Crush, LLXPRT, Pi, Shai, Parallel-AI, Mistral-Vibe, Agent-Deck
- **Status:** ⚠️ Not recommended for config routing
- **Current Config:** NOT FOUND (mostly)
- **Recommendation:**
  - **DO NOT** add to ruler.toml or rulesync unless explicitly needed
  - Create minimal configs only if user explicitly requests
  - LOW PRIORITY — backlog only

---

## Part 2: IDE Browser Preference (Secondary)

### Used Relatively Commonly

#### 1. ANTIGRAVITY (Browser-based IDE)
- **Status:** ✅ Actively used
- **Current Config:** NOT FOUND
- **Recommendation:**
  - Add `.antigravity/system.md` if it has agent config support
  - MEDIUM PRIORITY — but CLI-first means lower urgency

#### 2. KIRO (IDE)
- **Status:** ✅ Actively used
- **Current Config:** `.kiro/steering/system.md` ✅ (in ruler.toml)
- **Hook Status:** ❌ NO HOOKS
- **Recommendation:**
  - Create `.kiro/steering/hooks.yaml`
  - MEDIUM PRIORITY (IDE is secondary tier)

#### 3. VSCode (with extensions)
- **Status:** ✅ Actively used via extensions
  - **kilo-code** — maps to Kilo (Tier 1 CLI)
  - **cline** — maps to Cline (Tier 4, not recommended for routing)
  - **github-copilot** — maps to Copilot (Tier 4)
- **Current Config:** VSCode configs scattered
- **Recommendation:**
  - Config in `.vscode/settings.json` (not part of ruler)
  - Extension rules inherit from respective agent directories
  - MEDIUM PRIORITY

#### 4. Zed (Editor with builtin CLI extensions)
- **Status:** ✅ Actively used
- **Current Config:** `.zed/` directory (might exist)
- **Hook Status:** Unknown
- **Recommendation:**
  - Create `.zed/system.md` if extensible
  - MEDIUM PRIORITY

#### 5. Trae (IDE)
- **Status:** ✅ Actively used
- **Current Config:** `.trae/rules/system.md` ✅ (in ruler.toml)
- **Hook Status:** ❌ NO HOOKS
- **Recommendation:**
  - Create `.trae/rules/hooks.yaml`
  - MEDIUM PRIORITY

#### 6. Windsurf (IDE)
- **Status:** ✅ Actively used
- **Current Config:** `.windsurf/rules/system.md` ✅ (in ruler.toml)
- **Hook Status:** ❌ NO HOOKS
- **Recommendation:**
  - Create `.windsurf/rules/hooks.yaml`
  - MEDIUM PRIORITY

---

### Used Rarely But Useful

#### 7. Cursor IDE
- **Status:** 🟡 Rarely used (despite having full config)
- **Current Config:** `.cursor/rules/system.md` ✅ (in ruler.toml)
- **Hook Status:** ❌ NO HOOKS
- **Recommendation:**
  - Create `.cursor/rules/hooks.yaml` only if usage increases
  - LOW PRIORITY

#### 8. Amazon-Q (VSCode extension)
- **Status:** 🟡 Rarely used
- **Current Config:** Not applicable (VSCode extension)
- **Recommendation:**
  - Configure via VSCode settings, not in ruler
  - LOW PRIORITY

---

## Part 3: Current Configuration Gaps

**Decision Implemented (2026-04-10):** CLI tools (amp, qwen, opencode, kilocode) extend AgentsMdAgent — NO output_path needed.

### CRITICAL GAPS (Block Phase 5 until fixed)

| Agent | Tier | Config | Hooks | Status | Priority |
|-------|------|--------|-------|--------|----------|
| **Gemini** | 1 | ✅ ALIGNED (AgentsMdAgent) | ❌ | WORKING | 🟢 RESOLVED |
| **Qwen** | 1 | ✅ ALIGNED (AgentsMdAgent) | ❌ | WORKING | 🟢 RESOLVED |
| **OpenCode** | 1 | ✅ ALIGNED (AgentsMdAgent) | ❌ | WORKING | 🟢 RESOLVED |
| **AMP** | 1 | ✅ ALIGNED (AgentsMdAgent) | ❌ | WORKING | 🟢 RESOLVED |
| **Kilo** | 1 | ✅ ALIGNED (AgentsMdAgent) | ❌ | WORKING | 🟢 RESOLVED |
| **iFlow** | 1 | ❌ Missing | ❌ | UNCONFIGURED | 🔴 CRITICAL |

### MEDIUM GAPS (Phase 4.5)

| Agent | Tier | Config | Hooks | Status | Priority |
|-------|------|--------|-------|--------|----------|
| **Aider** | 2 | ⚠️ Variant exists | ❌ | PARTIAL | 🟡 MEDIUM |
| **Ra-aid** | 2 | ❌ Missing | ❌ | UNCONFIGURED | 🟡 MEDIUM |
| **Goose** | 2 | ❌ Missing | ❌ | UNCONFIGURED | 🟡 MEDIUM |
| **Letta** | 2 | ⚠️ Dir exists | ❌ | PARTIAL | 🟡 MEDIUM |
| **Kiro (IDE)** | Secondary | ✅ | ❌ | PARTIAL | 🟡 MEDIUM |
| **Trae (IDE)** | Secondary | ✅ | ❌ | PARTIAL | 🟡 MEDIUM |
| **Windsurf (IDE)** | Secondary | ✅ (output_path OPTIONAL) | ❌ | PARTIAL | 🟡 MEDIUM |

---

## Part 4: Recommendations for Phase 0-5 Restructuring

**Decision Implemented (2026-04-10):**
- Removed `[agents.amp]`, `[agents.qwen]`, `[agents.opencode]`, `[agents.kilocode]` from ruler.toml
- Deleted files: `.qwen/system.md`, `.agents/system.md`, `.opencode/system.md`, `.kilo/rules/system.md`
- CLI tools (amp, qwen, opencode, kilocode) extend AgentsMdAgent — NO output_path needed

### IMMEDIATE (Phase 4.5 — New)

**Create Phase 4.5: CLI-First Hook Enforcement**

```
Phase 4.5 Steps:
1. CLI Tools Already Configured (AgentsMdAgent - DECISION COMPLETE)
   ✅ amp, qwen, opencode, kilocode — Read root AGENTS.md
   ✅ NO output_path sections needed — uses Ruler built-in defaults
   ✅ Deleted orphaned system.md files

2. Create hooks for PRIMARY CLI tools:
   - .gemini/hooks.yaml
   - .qwen/hooks.yaml
   - .opencode/hooks.yaml
   - .agents/hooks.yaml (AMP)

3. Hybrid tools (cursor, windsurf, roo):
   - output_path is OPTIONAL — may read from both locations
   - NO changes required

4. IDE tools (claude, cline, kiro, trae):
   - KEEP output_path (non-AgentsMdAgent)
   - NO changes required

5. Update rulesync.jsonc targets to CLI-first priority
```

### SHORT TERM (Phase 5 — Revised)

**Phase 5: Secondary CLI Tool Preparation**

```
For agents awaiting API/provider routing:
1. Create .aider/system.md (from variant branch)
2. Create .ra-aid/system.md
3. Create .goose/system.md
4. Create .omp/system.md
5. Create .letta/system.md (activate existing dir)
6. Create .openhands/system.md

Don't create hooks yet (routing framework not ready)
```

### MEDIUM TERM (Phase 6 — New)

**Phase 6: Secondary CLI Tool Hooks (Once Routing Ready)**

```
Once API/provider routing framework implemented:
1. Add hooks to: aider, ra-aid, goose, letta, openhands
2. Implement provider routing enforcement hooks
3. Add credential/API key safety rules
4. Test route selection + fallback behavior
```

### IDE AGENTS (Phase 7 — New, Lower Priority)

**Phase 7: IDE-First Hardening (Optional)**

```
For IDE agents (lower usage priority):
1. Create hooks for: Kiro, Trae, Windsurf (commonly used)
2. Defer hooks for: Cursor, Cline, Roo (rarely used, not recommended)
3. Ignore: Claude, Copilot in IDE context
```

---

## Part 5: Changes to Phases 0-4

### Phase 0 (Requirements) — NEEDS REWRITE
**Current Problem:** Assumed IDE-first, Claude-centric workflow  
**Action:** Rebase on CLI-first, Gemini/Qwen primary workflow

**Revised Phase 0 should document:**
```
✅ Primary workflow: gemini > qwen > opencode > amp > kilo > iflow
✅ Secondary workflow: aider > ra-aid > goose > letta (once routing ready)
✅ Tertiary: IDE agents for context-switching only (Kiro, Windsurf, Trae)
❌ Do NOT emphasize: Claude Code (not primary), Cursor (rarely used)
❌ Do NOT prioritize: IDE-first configuration (CLI-first instead)
```

### Phase 1 (Emergency Fixes) — PARTIALLY CORRECT
**Status:** ✅ MCP configs added (good)  
**Issue:** Focused on all agent dirs equally, should prioritize Tier 1

**Revised Phase 1 should:**
```
✅ Fix MCP for PRIMARY tools: gemini, qwen, opencode, amp
⚠️ Fix MCP for SECONDARY tools: aider, letta, etc. (can be later)
❌ Don't spend time on: Claude, Cursor, Cline MCP (rarely used)
```

### Phase 2 (Content Fixes) — CORRECT APPROACH
**Status:** ✅ Tool rules were updated across all agents  
**Good:** Removed Prisma refs, added launch.py examples  
**Could improve:** Prioritize Tier 1 examples in docs

### Phase 3 (Ruler Setup) — BACKWARDS PRIORITY
**Current Problem:** 
```
ruler.toml default_agents = [
  "claude",        ← WRONG: Rarely used
  "cursor",        ← WRONG: Rarely used
  "cline",         ← WRONG: Not recommended
  ...
  "gemini-cli",    ← CORRECT: Primary, but config wrong
  "qwen",          ← CORRECT: Primary
  "opencode",      ← CORRECT: Primary
  ...
]
```

**Revised ruler.toml should:**
```toml
# CLI-First Priority Order
default_agents = [
  "gemini",        # Primary Tier 1
  "qwen",          # Primary Tier 1
  "opencode",      # Primary Tier 1
  "amp",           # Primary Tier 1
  "kilo",          # Primary Tier 1
  "iflow",         # Primary Tier 1
  "aider",         # Secondary Tier 2
  "letta",         # Secondary Tier 2
  "kiro",          # IDE, Secondary
  "trae",          # IDE, Secondary
  "windsurf",      # IDE, Secondary
  # Lower priority (defer or remove)
  # "claude",
  # "cursor",
  # "cline",
  # "roo",
]
```

### Phase 4 (Agent RuleZ) — WRONG TARGET
**Current Problem:** Hooks only created for `.claude/hooks.yaml`  
**Should be:** `.gemini/hooks.yaml`, `.qwen/hooks.yaml`, `.opencode/hooks.yaml`, `.agents/hooks.yaml`

**Revised Phase 4 should:**
```
Step 4.1: Install rulez ✅ (correct)
Step 4.2-6: Create hooks for PRIMARY tools instead of Claude:
  1. .gemini/hooks.yaml (4 rules)
  2. .qwen/hooks.yaml (4 rules)
  3. .opencode/hooks.yaml (4 rules)
  4. .agents/hooks.yaml (4 rules)
  5. Test all 4 enforcements
```

---

## Part 6: New Phase Architecture (0-7)

### Revised Phase Timeline

```
Phase 0: Requirements & Planning
  ✏️ REWRITE to reflect CLI-first workflow
  
Phase 1: Emergency Fixes (DONE ✅)
  ✅ MCP configs
  
Phase 2: Content Fixes (DONE ✅)
  ✅ Tool rules update
  
Phase 3: Ruler Setup (DONE ✅, but needs reorder)
  ✅ Configured, needs priority reorder
  
Phase 4: Hook Enforcement — REDO
  ❌ Current: Claude only
  ✏️ Revised: Gemini, Qwen, OpenCode, AMP (Tier 1)
  
Phase 4.5: Additional CLI Configs (NEW)
  🆕 Kilo, iFlow setup (Tier 1 completion)
  🆕 Separate Gemini from Qwen
  
Phase 5: Secondary CLI Tools (revised Phase 5)
  🆕 Aider, Ra-aid, Goose, Letta, OpenHands setup
  
Phase 6: Provider Routing Hooks (NEW, deferred)
  🆕 Once routing framework ready
  
Phase 7: IDE Hardening (NEW, optional)
  🆕 Kiro, Trae, Windsurf hooks if needed
```

---

## Part 7: Specific Action Items

### URGENT (Block Phase 5)

- [ ] **Fix Gemini/Qwen split:** Create `.gemini/system.md`, separate from `.qwen/system.md`
- [ ] **Add Kilo to ruler.toml:** 
  ```toml
  [agents.kilo]
  enabled = true
  output_path = ".kilo/system.md"
  ```
- [ ] **Add iFlow to ruler.toml:**
  ```toml
  [agents.iflow]
  enabled = true
  output_path = ".iflow/system.md"
  ```
- [ ] **Update rulesync.jsonc targets** to reorder by tier (CLI Tier 1 first)
- [ ] **Locate iFlow config location** (research where it expects system.md)

### HIGH PRIORITY (Phase 4.5)

- [ ] **Create Phase 4.5 hooks for PRIMARY CLI:**
  - `.gemini/hooks.yaml` (4 rules: block-force-push, block-secrets, etc.)
  - `.qwen/hooks.yaml` (same 4 rules)
  - `.opencode/hooks.yaml` (same 4 rules)
  - `.agents/hooks.yaml` (same 4 rules for AMP)

- [ ] **Test each hook enforcement:**
  - `rulez debug PreToolUse -t Bash -c "git push --force origin main"` for each
  - Verify force-push blocked on Gemini, Qwen, OpenCode, AMP

- [ ] **Create system.md for Tier 1 missing agents:**
  - `.kilo/system.md` (pull from source or create new)
  - `.iflow/system.md` (create appropriate content)

### MEDIUM PRIORITY (Phase 5)

- [ ] **Create Secondary CLI configs:**
  - `.aider/system.md`
  - `.ra-aid/system.md`
  - `.goose/system.md`
  - `.letta/system.md` (activate existing)
  - `.openhands/system.md`

- [ ] **Create IDE agent hooks** (if usage increases):
  - `.kiro/steering/hooks.yaml`
  - `.trae/rules/hooks.yaml`
  - `.windsurf/rules/hooks.yaml`

### LOW PRIORITY (Phase 6+)

- [ ] **Tertiary CLI tools** (crush, llxprt, pi, shai, etc.)
  - Do not configure unless explicitly requested
  - Document in backlog

- [ ] **Deprecated agents** (Claude Code, Cursor in IDE, Cline)
  - Keep existing configs but deprioritize
  - Consider deprecation notices in Phase 7

---

## Part 8: Key Recommendations for User Review

### Strategic Questions

1. **Should Phase 4 be re-executed for Tier 1 CLI tools?**
   - Current: Hooks only on Claude (wrong)
   - Recommended: Redo Phase 4 for Gemini, Qwen, OpenCode, AMP
   
2. **How urgent is Kilo + iFlow setup?**
   - Both are Tier 1 (heavy rotation)
   - Should be completed in Phase 4.5
   
3. **When should Secondary CLI tools get hooks?**
   - Can be deferred until API/provider routing framework ready
   - Or create configs now, hooks later
   
4. **Should IDE agents get hooks?**
   - Kiro, Trae, Windsurf are used relatively commonly
   - Recommend: Create hooks if you want IDE-level enforcement
   - Safe to defer if CLI tools are primary enforcement points

5. **What about Tertiary tools?**
   - Recommend: Do NOT configure (low priority, limited ecosystem)
   - Revisit if usage pattern changes

---

## Summary Table: What Needs to Change

**Decision Implemented (2026-04-10):**

| Component | Previous | Now (Decision Implemented) | Status |
|-----------|----------|---------------------------|--------|
| **CLI Tool output_path** | Required per tool ❌ | NONE needed (AgentsMdAgent) ✅ | COMPLETE |
| **Gemini Config** | Mismatch with Ruler ❌ | ALIGNED (root AGENTS.md) ✅ | RESOLVED |
| **Qwen Config** | Mismatch with Ruler ❌ | ALIGNED (root AGENTS.md) ✅ | RESOLVED |
| **OpenCode Config** | Verify needed ❓ | ALIGNED (root AGENTS.md) ✅ | RESOLVED |
| **AMP Config** | In `.agents/` ❓ | ALIGNED (root AGENTS.md) ✅ | RESOLVED |
| **Kilo Config** | Missing ❌ | ALIGNED (root AGENTS.md) ✅ | RESOLVED |
| **Hybrid Tools (cursor, windsurf, roo)** | Required output_path | OPTIONAL — may read both | NO CHANGE |
| **IDE Tools (claude, cline, kiro, trae)** | Required output_path | KEEP output_path | NO CHANGE |

**Files Deleted:**
- `.qwen/system.md`
- `.agents/system.md`
- `.opencode/system.md`
- `.kilo/rules/system.md`

**ruler.toml Sections Removed:**
- `[agents.amp]`
- `[agents.qwen]`
- `[agents.opencode]`
- `[agents.kilocode]`

---

**Status:** Decision implemented, ready for verification
**Recommendation:** Run `ruler apply` to sync root AGENTS.md

