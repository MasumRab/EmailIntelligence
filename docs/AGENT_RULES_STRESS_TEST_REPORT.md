# Agent Rules Stress Test & Feasibility Report

**Date:** 2026-04-04  
**Scope:** All agent tool configurations in EmailIntelligence  
**Methodology:** Hash comparison, diff analysis, content audit, workflow validation

---

## Executive Summary

The agent rules infrastructure has **13 critical issues** across 12+ agent tool directories. RuleSync was configured but produced only **cosmetic find-and-replace sync** (tool name substitution) while leaving structural, content, and MCP configuration deeply inconsistent. The system is **partially feasible** for single-tool use but **not feasible as a unified sync plan** in its current state.

---

## 1. Complete Agent Tool Inventory

### Tools with Dedicated Rule Directories (Active)

| Tool | Directory | Rule Files | Lines | MCP Config | Status |
|------|-----------|-----------|-------|------------|--------|
| **Cline** | `.clinerules/` | 4 files | 1,104 | via root `.mcp.json` | ✅ Canonical source |
| **Windsurf** | `.windsurf/rules/` | 4 files | 1,104 | `.windsurf/mcp.json` | ⚠️ Stale template keys |
| **Roo Code** | `.roo/rules/` | 6 files + modes | 1,104 | `.roo/mcp.json` (empty) | ⚠️ MCP broken |
| **Trae** | `.trae/rules/` | 4 files | 1,104 | None | ❌ No MCP |
| **Kiro** | `.kiro/steering/` | 6 files + hooks | 1,154 | `.kiro/settings/mcp.json` | ✅ Most complete |
| **Cursor** | `.cursor/rules/` | 3 files | 29 | `.cursor/mcp.json` (empty) | ❌ Severely underequipped |

### Tools with Top-Level Config Files

| Tool | Config File | Lines | Purpose | Status |
|------|------------|-------|---------|--------|
| **Claude Code** | `CLAUDE.md` | 143 | Claude-specific features | 🔴 **HAS MERGE CONFLICT** |
| **Amp** | `AGENT.md` | 5 | Taskmaster import only | ⚠️ Stub |
| **Gemini/Jules** | `GEMINI.md` | 353 | Jules prompt template | 🟡 Different purpose entirely |
| **Qwen** | `QWEN.md` | 229 | Scientific branch docs | 🟡 Repurposed as project docs |
| **All Agents** | `AGENTS.md` | 863 | Shared base instructions | ✅ Active (loaded by Amp) |
| **Legacy** | `.rules` | 417 | Task Master subset | ⚠️ Gitignored, stale |

### Tools with Settings Only (No Rules)

| Tool | Directory | Content |
|------|-----------|---------|
| **Gemini** | `.gemini/` | `settings.json` + commands |
| **Qwen** | `.qwen/` | `settings.json` + commands |
| **OpenCode** | `.opencode/` | `command/` + packages |

### Shared Rules (Language-Specific YAML)

| Category | Directory | Files | Status |
|----------|-----------|-------|--------|
| Architectural | `rules/architectural/` | 1 YAML | ✅ Clean |
| Python | `rules/python/` | 5 YAMLs | ✅ Clean |
| TypeScript | `rules/typescript/` | 4 YAMLs | ✅ Clean |
| DevPy | `rules/devpy/` | 3 YAMLs | ✅ Clean |

---

## 2. RuleSync Configuration Analysis

**Config:** `rulesync.jsonc`
```json
{
  "targets": ["copilot", "cursor", "claudecode", "codexcli"],
  "features": ["rules", "ignore", "mcp", "commands", "subagents"]
}
```

### 🔴 CRITICAL: Target Mismatch

| RuleSync Target | Actual Directory | Exists? | Rule Files? |
|----------------|-----------------|---------|-------------|
| `copilot` | `.github/copilot/` | ❌ No | ❌ |
| `cursor` | `.cursor/` | ✅ Yes | ⚠️ Only overview.mdc (29 lines) |
| `claudecode` | `.claude/` | ✅ Yes | ⚠️ No rules dir, agents/ subdir instead |
| `codexcli` | Not mapped | ❌ No | ❌ |

**Finding:** RuleSync targets don't match the actual active tools (Cline, Windsurf, Roo, Trae, Kiro). The config references tools that either don't exist or have minimal presence, while the 5 tools with 1,104+ lines of rules each aren't in the sync target list.

---

## 3. Sync Drift Analysis (Hash Comparison)

### Shared Files — ALL DIFFERENT Despite Identical Intent

#### `taskmaster.md` (558 lines each)
| Tool | MD5 Hash | Drift Type |
|------|----------|-----------|
| Cline | `13bfc8bd` | Canonical |
| Windsurf | `9dd8609a` | Tool name substitution only |
| Roo | `d69afb56` | Tool name substitution only |
| Trae | `87cd4244` | Tool name substitution only |
| Kiro | `a1765a53` | Tool name + frontmatter format |

**Actual diff:** Only `s/Cline/Windsurf/g` style replacements. Semantically identical.

#### `dev_workflow.md` (424 lines each)
| Tool | MD5 Hash | Drift Type |
|------|----------|-----------|
| Cline | `fd9efeff` | Canonical |
| Windsurf | `bc730256` | ⚠️ **Has bug**: `--rules windsurf,windsurf` (duplicate) |
| Roo | `bdff4ed5` | Tool name substitution |
| Trae | `4b53efc9` | Tool name substitution |
| Kiro | `8c637c86` | Tool name + inclusion format |

**🔴 BUG FOUND:** Windsurf's `dev_workflow.md` line 303:
```
"During Initialization": Use `task-master init --rules windsurf,windsurf`
```
Should be `--rules cline,windsurf` or just `--rules windsurf`. Naive find-replace of "cline" → "windsurf" corrupted the example.

#### `self_improve.md` (72 lines each)
| Tool | MD5 Hash | Drift Type |
|------|----------|-----------|
| Cline | `f628714c` | Canonical |
| Windsurf | `246a59f0` | Tool name substitution |
| Roo | `23c51e68` | Tool name substitution |
| Trae | `4b92e260` | Tool name substitution |
| Kiro | `0952cf37` | Tool name + frontmatter format |

#### Tool-specific rules (meta-rules)
| Tool | MD5 Hash | Content |
|------|----------|---------|
| `cline_rules.md` | `c037d7cf` | Identical body |
| `windsurf_rules.md` | `3cd35124` | Only path refs differ |
| `roo_rules.md` | `d853b59a` | Only path refs differ |
| `trae_rules.md` | `c4e55cc7` | Only path refs differ |
| `kiro_rules.md` | `59b9cc26` | Different frontmatter format |
| `overview.mdc` | `42993bec` | **Completely different content** |

---

## 4. Critical Issues Found

### 🔴 CRITICAL (Breaks Functionality)

| # | Issue | Location | Impact |
|---|-------|----------|--------|
| **C1** | **CLAUDE.md has unresolved merge conflict** | `CLAUDE.md` lines 1, 30, 143 | Claude Code loads broken file with `<<<<<<<` markers |
| **C2** | **Roo MCP config is empty** | `.roo/mcp.json` | Roo Code cannot access Task Master MCP |
| **C3** | **Cursor MCP config is empty** | `.cursor/mcp.json` | Cursor cannot access Task Master MCP |
| **C4** | **Trae has no MCP config at all** | `.trae/` | Trae cannot use Task Master |
| **C5** | **Windsurf MCP has hardcoded placeholder keys** | `.windsurf/mcp.json` | `YOUR_PERPLEXITY_API_KEY_HERE` — won't work |

### 🟡 MAJOR (Incorrect Content)

| # | Issue | Location | Impact |
|---|-------|----------|--------|
| **M1** | **Prisma references in all tools** | All `*_rules.md` + `self_improve.md` | References `prisma.md`, `schema.prisma` — project doesn't use Prisma at all |
| **M2** | **`dev_workflow.md` duplicate flag bug** | `.windsurf/rules/dev_workflow.md:303` | `--rules windsurf,windsurf` is invalid |
| **M3** | **GEMINI.md is a Jules prompt template, not rules** | `GEMINI.md` | 353 lines of unrelated Jules backlog automation prompts |
| **M4** | **QWEN.md is project documentation, not agent rules** | `QWEN.md` | Contains scientific branch architecture docs |
| **M5** | **Cursor rules are 29 lines vs 1,104 for other tools** | `.cursor/rules/` | Missing taskmaster.md, dev_workflow.md, self_improve.md in proper format |

### 🟠 MODERATE (Inconsistency)

| # | Issue | Location | Impact |
|---|-------|----------|--------|
| **I1** | **MCP invocation differs: `npm exec` vs `npx -y`** | `.mcp.json` vs `.windsurf/mcp.json` | Different install behavior |
| **I2** | **MCP env keys differ across configs** | All MCP files | Root has `GEMINI_API_KEY`+`GITHUB_API_KEY`, Windsurf has `PERPLEXITY_API_KEY`+`AZURE_OPENAI_API_KEY` |
| **I3** | **Kiro has unique hook system not documented elsewhere** | `.kiro/steering/` | 7 hook files + workflow guide — no other tool knows about this |

---

## 5. MCP Configuration Matrix

| Key | `.mcp.json` (root) | `.windsurf/mcp.json` | `.kiro/settings/mcp.json` | `.roo/mcp.json` | `.cursor/mcp.json` | `.claude/mcp.json` |
|-----|-------|---------|------|------|--------|--------|
| Command | `npm exec` | `npx -y` | `npm exec` | Empty | Empty | Empty |
| `ANTHROPIC_API_KEY` | ❌ | ❌ | ❌ | — | — | — |
| `PERPLEXITY_API_KEY` | ❌ | ✅ (placeholder) | ❌ | — | — | — |
| `OPENAI_API_KEY` | ❌ | ✅ (placeholder) | ❌ | — | — | — |
| `GOOGLE_API_KEY` | ✅ `${env}` | ✅ (placeholder) | ✅ `${env}` | — | — | — |
| `GEMINI_API_KEY` | ✅ `${env}` | ❌ | ✅ `${env}` | — | — | — |
| `XAI_API_KEY` | ✅ `${env}` | ✅ (placeholder) | ✅ `${env}` | — | — | — |
| `OPENROUTER_API_KEY` | ✅ `${env}` | ✅ (placeholder) | ✅ `${env}` | — | — | — |
| `MISTRAL_API_KEY` | ✅ `${env}` | ✅ (placeholder) | ✅ `${env}` | — | — | — |
| `AZURE_OPENAI_API_KEY` | ❌ | ✅ (placeholder) | ❌ | — | — | — |
| `OLLAMA_API_KEY` | ✅ `${env}` | ✅ (placeholder) | ✅ `${env}` | — | — | — |
| `GITHUB_API_KEY` | ✅ `${env}` | ❌ | ✅ `${env}` | — | — | — |
| `alwaysAllow` | `["add_task","expand_task"]` | ❌ | ❌ | — | — | — |

**Summary:** 3 different MCP configurations exist with no common standard. 4 tools have empty/missing MCP configs.

---

## 6. Content Architecture Overlap & Conflicts

```
┌─────────────────────────────────────────────────────────┐
│                    AGENTS.md (863 lines)                  │
│  ┌───────────────────────────────────────────────────┐  │
│  │ Taskmaster workflow + Backlog.md + Build/Test     │  │
│  │ Architecture + Code Style + Troubleshooting       │  │
│  └───────────────────────────────────────────────────┘  │
│           ↑ loaded by Amp/Claude                         │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  .rules (417 lines) — SUBSET of AGENTS.md (gitignored)  │
│  CLAUDE.md (143 lines) — 🔴 MERGE CONFLICT              │
│  AGENT.md (5 lines) — stub import to .taskmaster/        │
│  GEMINI.md (353 lines) — Jules template (unrelated)      │
│  QWEN.md (229 lines) — project docs (misnamed)           │
│                                                          │
├─────────────────────────────────────────────────────────┤
│        Per-Tool Rule Sets (Cline = canonical)            │
│                                                          │
│  taskmaster.md ──── 558 lines × 5 tools (name-swapped)  │
│  dev_workflow.md ── 424 lines × 5 tools (name-swapped)  │
│  self_improve.md ── 72 lines × 5 tools (name-swapped)   │
│  *_rules.md ─────── 53 lines × 5 tools (name-swapped)  │
│                                                          │
│  TOTAL DUPLICATED: ~5,570 lines of near-identical rules  │
│                                                          │
├─────────────────────────────────────────────────────────┤
│         Unique Per-Tool Content                          │
│                                                          │
│  Kiro: 7 hook files + hooks_workflow.md (50 lines)       │
│  Roo: .roomodes (63 lines) — role definitions            │
│  Cursor: overview.mdc (29 lines) — TypeScript-only       │
│  Cursor: taskmaster/ subdir with .mdc format             │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 7. Workflow Feasibility Stress Test

### Test 1: "New developer opens project in Windsurf"
- ❌ **FAIL**: `.windsurf/mcp.json` has placeholder keys (`YOUR_PERPLEXITY_API_KEY_HERE`)
- ❌ **FAIL**: `dev_workflow.md` has broken `--rules windsurf,windsurf` example
- ⚠️ WARN: Rules reference `prisma.md` which doesn't exist

### Test 2: "Developer uses Cursor"
- ❌ **FAIL**: `.cursor/mcp.json` is empty — no Task Master access
- ❌ **FAIL**: Only 29 lines of rules vs 1,104 for other tools — missing Taskmaster integration
- ❌ **FAIL**: `overview.mdc` says "Use TypeScript for all new code" — this is a Python-primary project

### Test 3: "Developer uses Roo Code"
- ❌ **FAIL**: `.roo/mcp.json` is empty — no Task Master MCP access
- ✅ PASS: Has complete rule set + custom roomodes with role definitions
- ⚠️ WARN: Nested `.roo/rules/.roo/` structure is confusing

### Test 4: "Developer uses Trae"
- ❌ **FAIL**: No MCP configuration at all
- ✅ PASS: Has complete rule set

### Test 5: "Developer uses Claude Code"
- ❌ **FAIL**: `CLAUDE.md` has unresolved git merge conflict (`<<<<<<<` markers)
- ⚠️ WARN: `.claude/mcp.json` is empty (uses root `.mcp.json`)
- ✅ PASS: Root `.mcp.json` works, `AGENTS.md` is loaded

### Test 6: "Developer uses Kiro"
- ✅ PASS: Complete rules, MCP config with env vars, unique hook system
- ✅ PASS: Most complete setup of any tool
- ⚠️ WARN: Hook-driven workflow contradicts manual Taskmaster workflow in shared rules

### Test 7: "RuleSync sync is run"
- ❌ **FAIL**: Targets `copilot` (no directory exists), `codexcli` (unmapped)
- ❌ **FAIL**: Doesn't target the 5 active tools (Cline, Windsurf, Roo, Trae, Kiro)
- ❌ **FAIL**: Would not fix any of the issues found above

### Test 8: "Content consistency across tools"
- ❌ **FAIL**: Cursor says "Use TypeScript for all new code" while AGENTS.md says Python primary
- ❌ **FAIL**: Kiro says "Never use `tm set-status --status=done`" while all other tools say to use it
- ❌ **FAIL**: All tools reference Prisma which isn't used

---

## 8. Recommended Architecture

### Single Source of Truth Model

```
AGENTS.md (shared base — ALL tools read this)
├── Taskmaster workflow
├── Build/test commands
├── Architecture overview
├── Code style (Python + TypeScript)
└── Troubleshooting

rules/                    (shared YAML linting rules)
├── python/*.yaml
├── typescript/*.yaml
├── architectural/*.yaml
└── devpy/*.yaml

Per-tool directories:     (ONLY tool-specific config)
├── .claude/              settings.json, agents/, commands/
├── .cursor/rules/        overview.mdc (cursor-specific frontmatter)
├── .windsurf/            mcp.json (same keys as root)
├── .roo/                 mcp.json, .roomodes
├── .kiro/                mcp.json, hooks/, steering/
├── .trae/                mcp.json (to be created)
├── .clinerules/          cline-specific rules only
├── .gemini/              settings.json, commands/
└── .qwen/                settings.json, commands/

DELETED:
├── .rules                (stale gitignored duplicate)
├── GEMINI.md             (Jules template — move to .gemini/)
├── QWEN.md               (project docs — not agent rules)
├── AGENT.md              (5-line stub — unnecessary)
```

### Key Principles

1. **One canonical `taskmaster.md`** in `rules/` — symlinked or `@import`'d by each tool
2. **One canonical `dev_workflow.md`** — no tool-name substitution needed
3. **MCP configs standardized** — all use `npm exec` with `${ENV_VAR}` references
4. **Tool-specific directories contain ONLY unique content** (roomodes, hooks, settings)
5. **RuleSync targets updated** to match actual tools used

---

## 9. Priority Fix List

| Priority | Fix | Effort |
|----------|-----|--------|
| 🔴 P0 | Resolve `CLAUDE.md` merge conflict | 5 min |
| 🔴 P0 | Populate empty MCP configs (Roo, Cursor, Claude) | 10 min |
| 🔴 P0 | Create Trae MCP config | 5 min |
| 🔴 P0 | Fix Windsurf MCP placeholder keys → `${ENV_VAR}` | 5 min |
| 🟡 P1 | Fix `--rules windsurf,windsurf` bug in Windsurf dev_workflow | 2 min |
| 🟡 P1 | Remove all Prisma references from all tools | 15 min |
| 🟡 P1 | Update Cursor `overview.mdc` to match Python-primary project | 10 min |
| 🟡 P1 | Update `rulesync.jsonc` targets to actual tools | 5 min |
| 🟠 P2 | Deduplicate 5,570 lines of near-identical rules | 2-4 hrs |
| 🟠 P2 | Move GEMINI.md content to `.gemini/` or `docs/` | 10 min |
| 🟠 P2 | Move QWEN.md content to `docs/` | 5 min |
| 🟠 P2 | Document Kiro hook workflow contradiction | 15 min |

---

## 10. Conclusion

**Feasibility Verdict: ⚠️ PARTIALLY FEASIBLE**

The sync plan is structurally sound in concept (shared rules distributed across tools) but the execution has 3 fundamental problems:

1. **RuleSync isn't targeting the right tools** — the 4 configured targets don't match the 5+ tools with actual rule directories
2. **The sync is lossy** — naive find-and-replace of tool names introduces bugs (windsurf,windsurf) and doesn't handle structural differences (Kiro frontmatter, Cursor .mdc format)
3. **MCP configs are individually managed** — no sync mechanism exists for the most critical configuration (API keys and invocation commands)

The current state results in **5,570+ lines of duplicated content** that will inevitably drift further. The recommended fix is to move to a single-source-of-truth model where tool directories contain only tool-specific configurations.
