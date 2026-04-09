# Agent Rules Gap Analysis & Content Map

**Date:** 2026-04-06  
**Scope:** All AI agent configurations across 8 tool directories, 8 root files, and 3 orchestration docs  
**Method:** Exhaustive file-by-file audit with content classification, hash comparison, and cross-reference validation

---

## 1. Executive Summary

| Metric | Count |
|--------|-------|
| Original issues (stress test) | 13 |
| **Additional gaps found** | **17** |
| Total issues | **30** |
| Tool directories audited | 8 |
| Root agent files audited | 8 |
| Total duplicated lines | **11,092** |
| Unique tool-specific content | ~47,000 lines (Roo mode rules) |
| Files with wrong content | 15 |
| Empty/broken MCP configs | 5 |
| Tools with placeholder API keys | 2 (Windsurf, Kilo) |

The original 5-phase handoff addressed 13 issues but missed `.kilo/`, `.github/instructions/`, cerebras-MCP override files, TypeScript-only content in 9+ files, `_deep` duplicates (1,960 lines), dead manifest references, and had no plan for content deduplication, hierarchical structuring, or multi-loop verification.

---

## 2. Complete File Inventory

### 2.1 Root-Level Agent Files

| File | Lines | Purpose | Classification | Disposition |
|------|-------|---------|----------------|-------------|
| `AGENTS.md` | 883 | Universal foundation: Taskmaster, build/test, architecture | Tier 1 — Shared | ✅ KEEP |
| `CLAUDE.md` | 143 | Claude-specific features + MCP config | Tier 2 — Tool-specific | 🔴 FIX merge conflict |
| `GEMINI.md` | 353 | **DUAL-PURPOSE**: Lines 1-185 = Jules template, Lines 186-353 = Gemini CLI agent instructions (Tier 2) | ⚠️ SPLIT — NOT relocate | 🟡 SPLIT: keep Gemini CLI section at root (Gemini CLI auto-loads `GEMINI.md`), extract Jules template to `.gemini/JULES_TEMPLATE.md` |
| `QWEN.md` | 229 | Scientific branch project docs BUT `.taskmaster/.qwen/session_manager.py` reads it from root | ⚠️ KEEP AT ROOT | 🟡 REPLACE content with proper Tier 2 Qwen agent instructions (session_manager.py reads from root — moving breaks Qwen) |
| `AGENT.md` | 5 | Amp import stub for .taskmaster/ | Tier 2 — Amp-specific | ✅ KEEP |
| `IFLOW.md` | N/A | Deleted from current branch, exists on 516 remote branches as Iflow Cursor integration guide (Tier 2) | Missing on current branch | 🟠 RESTORE from remote or mark as branch-specific |
| `CRUSH.md` | N/A | **Gitignored** (`.gitignore:232`), exists on 504 remote branches as Crush IDE agent instructions (Tier 2) | Gitignored — intentionally excluded | 🟠 Gitignored by design — restore only if Crush is used on this branch |
| `LLXPRT.md` | N/A | **Gitignored** (`.gitignore:233`), exists on 504 remote branches as LLxPRT reasoning guide (Tier 2) | Gitignored — intentionally excluded | 🟠 Same as CRUSH.md |
| `.rules` | 417 | Stale gitignored subset of AGENTS.md | Obsolete | 🔴 DELETE |
| `MODEL_CONTEXT_STRATEGY.md` | 320 | Three-tier context distribution strategy | Reference architecture | ✅ KEEP |
| `AGENTS_orchestration-tools.md` | varies | Orchestration branch instructions | Branch-specific | ✅ KEEP |

### 2.2 Tool Directory Files

#### .clinerules/ (CANONICAL source) — 9 files, 2,163 lines

| File | Lines | Content Type | Status |
|------|-------|-------------|--------|
| `cline_rules.md` | 52 | Meta-rules (Prisma refs) | ❌ FIX Prisma |
| `self_improve.md` | 72 | Self-improvement (Prisma code) | ❌ FIX Prisma |
| `dev_workflow.md` | 423 | Taskmaster workflow | ✅ Canonical |
| `taskmaster.md` | 557 | Taskmaster full guide | ✅ Canonical |
| `dev_workflow_deep.md` | 423 | EXACT DUPLICATE | 🔴 DELETE |
| `taskmaster_deep.md` | 557 | EXACT DUPLICATE | 🔴 DELETE |
| `logic_preservation.md` | 32 | CLI porting workflow | ✅ UNIQUE — distribute to all |
| `copilot-instructions.md` | 36 | TypeScript-only content | ❌ FIX language |
| `CLAUDE.md` | 11 | cerebras-mcp override | 🟡 EDIT — remove dangerous content |

#### .cursor/rules/ — 14+ files, 2,195 lines

| File | Lines | Content Type | Status |
|------|-------|-------------|--------|
| `overview.mdc` | 29 | TypeScript-only guidelines | ❌ FIX language |
| `CLAUDE.md` | 11 | cerebras-mcp override | 🟡 EDIT — remove dangerous content |
| `CLAUDE.mdc` | 29 | TypeScript-only guidelines | ❌ FIX language |
| `GEMINI.mdc` | 33 | TypeScript-only guidelines | ❌ FIX language |
| `copilot-instructions.md` | 36 | TypeScript-only guidelines | ❌ FIX language |
| `copilot-instructions.mdc` | 33 | TypeScript-only guidelines | ❌ FIX language |
| `logic_preservation.md` | 1,624 | Copy from .clinerules | ⚠️ Large copy |
| `dev_workflow_deep.md` | 423 | DUPLICATE | 🔴 DELETE |
| `dev_workflow_deep.mdc` | 423 | DUPLICATE | 🔴 DELETE |
| `taskmaster_deep.md` | 557 | DUPLICATE | 🔴 DELETE |
| `taskmaster_deep.mdc` | 557 | DUPLICATE | 🔴 DELETE |
| `taskmaster/` | varies | Cursor-specific Taskmaster | ✅ UNIQUE |

#### .windsurf/rules/ — 4 files, 1,104 lines

| File | Lines | Content Type | Status |
|------|-------|-------------|--------|
| `windsurf_rules.md` | 52 | Meta-rules (Prisma refs) | ❌ FIX Prisma |
| `self_improve.md` | 72 | Self-improvement (Prisma code) | ❌ FIX Prisma |
| `dev_workflow.md` | 423 | Has `--rules windsurf,windsurf` BUG | ❌ FIX bug |
| `taskmaster.md` | 557 | Name-swapped copy | ⚠️ Duplicate |

#### .roo/rules/ — 6+ files, 1,104+ lines (+ 46,571 mode rules)

| File | Lines | Content Type | Status |
|------|-------|-------------|--------|
| `roo_rules.md` | 52 | Meta-rules (Prisma refs) | ❌ FIX Prisma |
| `self_improve.md` | 72 | Self-improvement (Prisma code) | ❌ FIX Prisma |
| `dev_workflow.md` | 423 | Name-swapped copy | ⚠️ Duplicate |
| `taskmaster.md` | 557 | Name-swapped copy | ⚠️ Duplicate |
| `.roomodes` | 62 | 5 custom modes | ✅ UNIQUE — Roo only |
| `.roo/rules-*/` | ~46,571 | 6 mode-specific rule sets | ✅ UNIQUE — Roo only |

#### .trae/rules/ — 4 files, 1,104 lines

| File | Lines | Content Type | Status |
|------|-------|-------------|--------|
| `trae_rules.md` | 52 | Meta-rules (Prisma refs) | ❌ FIX Prisma |
| `self_improve.md` | 72 | Self-improvement (Prisma code) | ❌ FIX Prisma |
| `dev_workflow.md` | 423 | Name-swapped copy | ⚠️ Duplicate |
| `taskmaster.md` | 557 | Name-swapped copy | ⚠️ Duplicate |

#### .kiro/steering/ — 6 files, 1,154 lines (+ 7 hooks)

| File | Lines | Content Type | Status |
|------|-------|-------------|--------|
| `kiro_rules.md` | 50 | Meta-rules (`inclusion: always` format) | ❌ FIX Prisma |
| `self_improve.md` | 70 | Self-improvement (Prisma code) | ❌ FIX Prisma |
| `dev_workflow.md` | 421 | Name-swapped copy | ⚠️ Duplicate |
| `taskmaster.md` | 555 | Name-swapped copy | ⚠️ Duplicate |
| `taskmaster_hooks_workflow.md` | 58 | Hook-driven task workflow | ✅ UNIQUE — Kiro only |
| `.kiro/hooks/` | 7 hooks | Kiro automation hooks | ✅ UNIQUE — Kiro only |

#### .kilo/rules/ — 5 files + modes, 1,104+ lines

| File | Lines | Content Type | Status |
|------|-------|-------------|--------|
| `kilo_rules.md` | 52 | Meta-rules (Prisma refs) | ❌ FIX Prisma |
| `self_improve.md` | 72 | Self-improvement (Prisma code) | ❌ FIX Prisma |
| `dev_workflow.md` | 423 | Name-swapped copy | ⚠️ Duplicate |
| `taskmaster.md` | 557 | Name-swapped copy | ⚠️ Duplicate |
| `.kilocodemodes` | 62 | 5 custom modes (Kilo-branded) | ✅ UNIQUE — Kilo only |

#### .github/instructions/ — 7 files, 1,164 lines

| File | Lines | Content Type | Status |
|------|-------|-------------|--------|
| `taskmaster.instructions.md` | ~557 | Name-swapped copy | ⚠️ Duplicate |
| `dev_workflow.instructions.md` | ~423 | Name-swapped copy | ⚠️ Duplicate |
| `self_improve.instructions.md` | ~72 | Prisma code | ❌ FIX Prisma |
| `vscode_rules.instructions.md` | ~52 | Prisma refs | ❌ FIX Prisma |
| `copilot-instructions.instructions.md` | ~36 | TypeScript-only | ❌ FIX language |
| `GEMINI.instructions.md` | ~33 | TypeScript-only | ❌ FIX language |
| `tools-manifest.json` | 279 | Tool registry | ✅ UNIQUE — dead refs ❌ |

---

## 3. Content Classification by Intent

### 3.1 Universal Shared Content (Tier 1 — belongs in `.ruler/AGENTS.md`)

| Content | Total Duplicated Lines | Source | Recommendation |
|---------|----------------------|--------|----------------|
| Taskmaster workflow guide | 3,899 (557 × 7) | `.clinerules/taskmaster.md` | Single canonical in `.ruler/` |
| Development workflow | 2,961 (423 × 7) | `.clinerules/dev_workflow.md` | Single canonical in `.ruler/` |
| `_deep` exact duplicates | 1,960 (2 × .clinerules + 4 × .cursor) | Various | DELETE all |
| Self-improvement patterns | 500 (72 × 7) | `.clinerules/self_improve.md` | Single canonical (fix Prisma) |
| Logic preservation workflow | 32 | `.clinerules/logic_preservation.md` | Distribute to all tools |
| **Subtotal** | **9,352 lines** | | |

### 3.2 Tool-Specific Meta-Rules (Tier 2 — generated per-tool by Ruler)

| Content | Lines × Tools | Differences | Recommendation |
|---------|--------------|-------------|----------------|
| `*_rules.md` meta-rules | 52 × 7 = 364 | Tool name, path prefix, frontmatter format | Ruler generates with path rewriting |
| Copilot instructions | 36 × 3 = 108 | None (identical wrong content) | Fix language, let Ruler distribute |
| **Subtotal** | **472 lines** | | |

### 3.3 Tool-Unique Content (Tier 3 — stays in tool directory)

| Content | Location | Lines | Scope |
|---------|----------|-------|-------|
| Roo custom modes | `.roo/rules/.roomodes` | 62 | Roo Code only |
| Roo mode-specific rules | `.roo/rules/.roo/rules-*` | ~46,571 | Roo Code only |
| Kilo custom modes | `.kilo/rules/.kilocodemodes` | 62 | Kilo Code only |
| Kiro hooks | `.kiro/steering/.kiro/hooks/` | 7 files | Kiro only |
| Kiro hooks workflow | `.kiro/steering/taskmaster_hooks_workflow.md` | 58 | Kiro only |
| Cursor taskmaster subdir | `.cursor/rules/taskmaster/` | varies | Cursor only |
| tools-manifest.json | `.github/instructions/` | 279 | GitHub/VS Code only |
| Agent RuleZ hooks | `.claude/hooks.yaml` | ~60 | Claude Code only (runtime) |
| **Subtotal** | **~47,100 lines** | | |

### 3.4 Wrong/Broken Content (DELETE or FIX)

| # | Content | Locations | Problem | Fix |
|---|---------|-----------|---------|-----|
| W1 | `<<<<<<< HEAD` markers | `CLAUDE.md` | Merge conflict | OVERWRITE (Phase 1) |
| W2 | Prisma references | 26 occurrences in 8 dirs | Project doesn't use Prisma | Replace with Python/SQLAlchemy |
| W3 | `--rules windsurf,windsurf` | `.windsurf/rules/dev_workflow.md` L36,303 | Naive find-replace bug | Fix to `cline,windsurf` |
| W4 | "Use TypeScript for all new code" | 9 files across .cursor, .clinerules, .github | Python-primary project | Fix to dual-language |
| W5 | cerebras-mcp write tool | `.clinerules/CLAUDE.md`, `.cursor/rules/CLAUDE.md` | Forces non-existent tool | EDIT — remove dangerous content |
| W6 | Placeholder API keys | `.windsurf/mcp.json`, `.kilo/mcp.json` | `YOUR_*_HERE` | Replace with `${ENV_VAR}` |
| W7 | Empty MCP configs | `.roo/`, `.cursor/`, `.claude/` | 0 bytes | Populate from canonical |
| W8 | Missing MCP config | `.trae/` | No mcp.json | Create from canonical |
| W9 | Agent file references to missing files | `tools-manifest.json` | CRUSH.md, LLXPRT.md, IFLOW.md don't exist **on current branch** (gitignored/deleted) but exist on 500+ remote branches as real Tier 2 agent files | Set `status: "not_on_branch"` with note about remote branch availability |
| W10 | Stale `.rules` file | Root | 417-line gitignored duplicate | DELETE |

### 3.5 Misplaced/Dual-Purpose Content (CAREFUL — Tool Conventions Apply)

> ⚠️ **CRITICAL SAFETY NOTE:** These files are auto-loaded by their respective tools via filename convention. Moving or renaming them **WILL** break tool context injection. An exhaustive impact search of git history, ignore rules, session managers, and orchestration docs was performed before these recommendations.

| File | Current Location | Tool Convention | Impact of Moving | Correct Action |
|------|-----------------|----------------|------------------|----------------|
| `GEMINI.md` | Root (353 lines) | **Gemini CLI auto-loads `GEMINI.md` from project root** (line 218 confirms) | ❌ Moving BREAKS Gemini CLI context injection | **SPLIT**: Extract Jules template (L1-185) → `.gemini/JULES_TEMPLATE.md`, keep Gemini CLI instructions (L186-353) at root as `GEMINI.md` |
| `QWEN.md` | Root (229 lines) | **`.taskmaster/.qwen/session_manager.py` reads `QWEN.md` from project root** (line 172-176) | ❌ Moving BREAKS Qwen session manager | **REPLACE** content: keep file at root, replace scientific branch docs with proper Tier 2 Qwen agent instructions. Move current content to `docs/SCIENTIFIC_BRANCH_DOCS.md` as a COPY |
| `.github/copilot-instructions.md` | `.github/` | **Copilot auto-loads from `.github/copilot-instructions.md`** (GitHub convention) | ❌ Moving BREAKS Copilot context injection | **FIX content** only (TypeScript→Python), do NOT move |
| `IFLOW.md` | MISSING on current branch | **Iflow Cursor loads from root** (per recovered content from origin/001-agent-context-control) | File is deleted — Iflow has no context | 🟠 RESTORE from `git show origin/001-agent-context-control:IFLOW.md` if Iflow is used |
| `CRUSH.md` | MISSING (gitignored: `.gitignore:232`) | **Crush IDE loads from root** (per recovered content: "auto-loaded in Crush workspace context") | File is gitignored — Crush has no context on this branch | 🟠 RESTORE from remote branch if Crush is used. `.gitignore` entry was intentional |
| `LLXPRT.md` | MISSING (gitignored: `.gitignore:233`) | **LLxPRT loads from root** (per recovered content: "auto-loaded in LLxPRT context") | File is gitignored — LLxPRT has no context on this branch | 🟠 Same as CRUSH.md |

### 3.6 Git History Findings for Deleted Agent Files

| File | Remote Branches | Added By | Deleted By | Content Type |
|------|----------------|----------|------------|--------------|
| `IFLOW.md` | 516 branches | `bb13d6c76` ("iflow md") | `2b17d13a` (orchestration cleanup) | Tier 2: Iflow Cursor integration guide with MCP config, inline AI features |
| `CRUSH.md` | 504 branches | `563608e8f` ("iflow") | `136c12457` (untrack + gitignore) | Tier 2: Crush IDE instructions with workspace integration, MCP config |
| `LLXPRT.md` | 504 branches | `136c12457` | `136c12457` (same commit: untracked + gitignored) | Tier 2: LLxPRT reasoning/planning guide with multi-step verification |

### 3.7 Gitignore Rules Affecting Agent Files

| File | `.gitignore` Line | Effect | Implication |
|------|-------------------|--------|-------------|
| `GEMINI.md` | 230 | Listed BUT currently tracked (git tracks overrides gitignore) | Safe to edit; if `git rm` is run, it would become ignored |
| `QWEN.md` | 231 | Listed BUT currently tracked | Same as GEMINI.md |
| `CRUSH.md` | 232 | Listed AND NOT tracked | **Ignored** — cannot be committed without `git add -f` |
| `LLXPRT.md` | 233 | Listed AND NOT tracked | **Ignored** — same as CRUSH.md |
| `CLAUDE.md` | N/A (comment says "MUST be tracked") | NOT ignored | ✅ Correctly tracked |
| `IFLOW.md` | N/A | NOT ignored but deleted | Could be re-added normally |
| `.rules` | 193 | Listed AND tracked | Stale — should be `git rm` |

### 3.8 Sibling Worktrees Agent Files (NOT in Main Repo)

> **Full analysis:** `docs/SIBLING_WORKTREES_AGENT_FILES_ANALYSIS.md`
> **Agents archive:** `~/github/agents/` (280 versioned files + 57 git history files)

Three sibling worktrees contain agent files not available on the main branch:

| Worktree | Branch | Files NOT in Main |
|----------|--------|-------------------|
| `EmailIntelligenceAider` | `orchestration-tools` | IFLOW.md (104 lines) |
| `EmailIntelligenceAuto` | `auto-sync-20260405` | IFLOW.md (41 lines, truncated), CRUSH.md (5 lines, stub), LLXPRT.md (0 lines, empty) |
| `EmailIntelligenceGem` | `consolidate/cli-unification` | IFLOW.md (330 lines, best), CRUSH.md (52 lines), LLXPRT.md (37 lines) |

**Best Source for Restoration:**

| File | Best Worktree | Lines | Content |
|------|---------------|-------|---------|
| IFLOW.md | EmailIntelligenceGem | 330 | Full iFlow CLI integration + project overview |
| CRUSH.md | EmailIntelligenceGem | 52 | Build/lint/test commands, code style guidelines |
| LLXPRT.md | EmailIntelligenceGem | 37 | Project overview with architecture TOC |

**Differing Files (in main but different content):**

| File | Worktree | Lines | Main Lines | Status |
|------|----------|-------|------------|--------|
| AGENTS.md | EmailIntelligenceAider | 76 | 883 | Truncated |
| AGENTS.md | EmailIntelligenceAuto | 11 | 883 | Severely truncated |
| AGENTS.md | EmailIntelligenceGem | 910 | 883 | Extended (+27 lines) |
| CLAUDE.md | EmailIntelligenceAider | 112 | 143 | Missing sections |
| CLAUDE.md | EmailIntelligenceAuto | 0 | 143 | Empty file |
| GEMINI.md | EmailIntelligenceAuto | 329 | 353 | Missing Gemini CLI section |
| GEMINI.md | EmailIntelligenceGem | 288 | 353 | Missing Gemini CLI section |

---

## 4. MCP Configuration Audit

| Location | Bytes | Command | Key Pattern | Env Keys | Status |
|----------|-------|---------|-------------|----------|--------|
| `.mcp.json` (root) | 289 | `npm exec` | `${ENV_VAR}` | 7 keys | ✅ CANONICAL |
| `.kiro/settings/mcp.json` | 431 | `npm exec` | `${ENV_VAR}` | 7 keys | ✅ Matches |
| `.windsurf/mcp.json` | 517 | `npx -y` | `YOUR_*_HERE` | 8 keys (different set) | ❌ Placeholder + wrong command |
| `.kilo/mcp.json` | 517 | `npx -y` | `YOUR_*_HERE` | 8 keys (different set) | ❌ Same as Windsurf |
| `.vscode/mcp.json` | 537 | varies | varies | varies | ⚠️ Unaudited |
| `.roo/mcp.json` | 0 | — | — | — | ❌ Empty |
| `.cursor/mcp.json` | 0 | — | — | — | ❌ Empty |
| `.claude/mcp.json` | 0 | — | — | — | ❌ Empty |
| `.trae/mcp.json` | N/A | — | — | — | ❌ Missing |

**Canonical standard:** `npm exec` command, `${ENV_VAR}` references, 7 keys (GOOGLE_API_KEY, GEMINI_API_KEY, XAI_API_KEY, OPENROUTER_API_KEY, MISTRAL_API_KEY, OLLAMA_API_KEY, GITHUB_API_KEY).

---

## 5. Gaps in Existing Handoff (17 Additional Issues)

| # | Gap | Severity | Phase Added |
|---|-----|----------|-------------|
| G1 | `.kilo/` entirely omitted (MCP + Prisma + duplicates) | 🔴 Critical | Phase 6.1 |
| G2 | `.github/instructions/` Prisma refs (2 files) | 🟡 Major | Phase 6.2 |
| G3 | `.github/` TypeScript-only content (3 files) | 🟡 Major | Phase 6.2 |
| G4 | cerebras-MCP override CLAUDE.md (2 files) | 🟡 Major | Phase 6.3 (EDIT) |
| G5 | Cursor TypeScript-only .mdc files (5 files) | 🟡 Major | Phase 6.4 |
| G6 | `_deep` duplicate files (6 files, 1,960 lines) | 🟡 Major | Phase 6.5 |
| G7 | Dead refs in tools-manifest.json (3 missing files) | 🟠 Moderate | Phase 6.6 |
| G8 | No content deduplication plan (11,092 lines) | 🔴 Critical | Phase 7 |
| G9 | No oh-my-openagent hierarchy | 🟠 Moderate | Phase 7 |
| G10 | No Ruler/RuleSync orchestration strategy | 🟡 Major | Phase 8 |
| G11 | No agentrulegen.com analysis integration | 🟠 Moderate | Phase 10 |
| G12 | No multi-loop verification process | 🟡 Major | Phase 9 |
| G13 | `.vscode/mcp.json` not audited | 🟠 Moderate | Future |
| G14 | `.clinerules/copilot-instructions.md` TypeScript-only | 🟡 Major | Phase 6.4 |
| G15 | `.github/copilot-instructions.md` TypeScript-only | 🟡 Major | Phase 6.2 |
| G16 | logic_preservation.md only in 2 dirs (useful for all) | 🟠 Moderate | Phase 7 |
| G17 | Kiro hooks workflow contradicts shared rules (never acknowledged) | 🟠 Moderate | Documentation |

---

## 6. oh-my-openagent Hierarchical Structure Plan

Following the 4-phase `init-deep` model from [oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent):

### Phase 1: Discovery + Analysis

| Agent | Focus |
|-------|-------|
| Project structure | Root is Python/FastAPI + React. Deviations: dual-language, no monorepo |
| Entry points | `launch.py`, `src/main.py`, `emailintelligence_cli.py` |
| Conventions | Black, flake8, mypy, pytest (Python); Vite, Tailwind (TypeScript) |
| Anti-patterns | Circular deps (AIEngine ↔ DatabaseManager), no eval/exec, no hardcoded paths |
| Build/CI | pytest, npm run build, `.github/workflows/` |
| Test patterns | pytest with conftest.py, tests/ directory |

### Phase 2: Scoring & Location Decision

| Directory | File Count | Centrality | Module Boundary | Score | Action |
|-----------|-----------|------------|-----------------|-------|--------|
| `.` (root) | 100+ | — | — | — | **Always create** |
| `src/core/` | 10+ | High (AI engine, DB) | ✅ `__init__.py` | ~18 | **Create AGENTS.md** |
| `backend/python_backend/` | 15+ | High (FastAPI API) | ✅ `__init__.py` | ~16 | **Create AGENTS.md** |
| `client/` | 30+ | Medium | ✅ `package.json` | ~14 | Skip (root covers) |
| `modules/` | 5+ | Medium | ✅ `__init__.py` | ~12 | Skip |
| `server/` | 10+ | Medium | ✅ `package.json` | ~11 | Skip |
| Other dirs | <10 | Low | — | <8 | Skip |

### Phase 3: Generate

**Root `.ruler/AGENTS.md`** (50-150 lines): Project overview, build commands, key directories, task management, critical rules. Already created in Phase 3 of handoff.

**Subdirectory files** (30-80 lines each, telegraphic style):
- `src/core/AGENTS.md` — AI engine, DB manager, workflow engines. Anti-patterns: circular deps.
- `backend/python_backend/AGENTS.md` — FastAPI routes, middleware. Conventions: Pydantic models.

### Phase 4: Deduplicate

- Child files NEVER repeat root content (build commands, task management, code style)
- Remove generic advice (anything true of all Python projects)
- Verify telegraphic style (no prose paragraphs)

---

## 7. Ruler/RuleSync/RuleZ Orchestration Strategy

### 7.1 Ruler — Primary Distribution (32 agents)

| Responsibility | Details |
|---------------|---------|
| Rule distribution | `.ruler/AGENTS.md` → all 32 agent targets |
| Trae AI support | Only tool that supports Trae |
| MCP propagation | `[mcp_servers]` in `ruler.toml` → merge to all tools |
| Backup + revert | `--backup` creates `.bak`, `ruler revert` undoes |
| Nested rules | `src/.ruler/AGENTS.md` for subdirectory-specific rules |

### 7.2 RuleSync — CI Drift Detection

| Responsibility | Details |
|---------------|---------|
| Drift detection | `npx rulesync generate --check` in CI pipeline |
| Permissions sync | `.rulesync/permissions.json` → unified allow/deny |
| Skills lockfile | `rulesync install --frozen` for CI safety |
| Import | `rulesync import --targets cline` (one-time bootstrap) |

### 7.3 Agent RuleZ — Runtime Enforcement

| Responsibility | Details |
|---------------|---------|
| Policy enforcement | `.claude/hooks.yaml` blocks dangerous operations |
| Validation | `rulez validate` + `rulez lint` in CI |
| Debug testing | `rulez debug` simulates events against rules |
| Skills sync | `rulez skills sync` across claude/opencode/gemini/codex |

### 7.4 Tool Responsibility Matrix

| Task | Primary | Fallback | CI Check |
|------|---------|----------|----------|
| Distribute shared rules | Ruler | Manual | `ruler apply --dry-run` |
| Distribute MCP configs | Ruler | Manual | Diff against canonical |
| Detect rule drift | RuleSync | Hash compare | `rulesync --check` |
| Block dangerous git ops | Agent RuleZ | None | `rulez debug` |
| Trae AI rules | Ruler | Manual | `ruler apply --dry-run` |
| Kiro hooks | Manual | N/A | File existence check |
| Roo modes | Manual | N/A | JSON validation |

---

## 8. agentrulegen.com Integration Plan

### 8.1 Reference Guides (for enhancing documentation)

| Guide URL | Relevant To |
|-----------|------------|
| `/guides/what-are-ai-coding-rules` | Foundational concepts for AGENTS.md |
| `/guides/how-to-set-up-cursor-rules` | `.cursor/rules/` config |
| `/guides/claude-code-guide` | CLAUDE.md best practices |
| `/guides/github-copilot-instructions` | `.github/copilot-instructions.md` format |
| `/guides/cursorrules-vs-claude-md` | Format comparison for consolidation |
| `/guides/convert-cursor-rules-to-claude-md` | Migration reference |
| `/guides/how-to-code-faster-with-ai` | Efficiency patterns |
| `/guides/agent-rules-for-monorepos` | Multi-dir structure patterns |
| `/guides/debugging-ai-generated-code` | Debug strategy rules |

### 8.2 Templates (for content enhancement)

| Template URL | Priority | Use Case |
|-------------|----------|----------|
| `/templates/python-fastapi` | **HIGH** | Replace Prisma boilerplate with Python/FastAPI patterns |
| `/templates/ai-agent-workflow` | Medium | Agent workflow standardization |
| `/templates/git-workflow` | Medium | Git rules for Agent RuleZ |
| `/templates/code-review` | Medium | Code review standards |
| `/templates/linear-workflow` | Low | Task management integration |

### 8.3 Validation via /analyze

After all phases complete, upload configs to `agentrulegen.com/analyze`:
1. `.ruler/AGENTS.md` — Validate shared rules quality
2. `.claude/hooks.yaml` — Validate policy rules
3. `rulesync.jsonc` — Validate sync config
4. Individual tool rules — Validate per-tool configs

> **NOTE:** Use these URLs with the intelligent extraction approach: fetch full content, extract key sections, and extend search for equivalent tool documentation (Roo, Kiro, Trae, Letta Code) when gaps identified.

---

## 9. Multi-Loop Verification Process

### 9.1 Loop 1: File Existence & Size

Verify all required files exist and are non-empty.

```bash
echo "=== LOOP 1: FILE EXISTENCE ==="
for f in AGENTS.md CLAUDE.md AGENT.md .ruler/AGENTS.md .ruler/ruler.toml .claude/hooks.yaml rulesync.jsonc; do
  echo -n "$f: "; test -f "$f" && echo "EXISTS ($(wc -c < "$f") bytes)" || echo "MISSING"
done
for d in .roo .cursor .windsurf .trae .kiro .kilo .claude; do
  echo -n "$d/mcp.json: "; test -s "$d/mcp.json" && echo "OK" || echo "EMPTY/MISSING"
done
```

### 9.2 Loop 2: Content Correctness

Verify no wrong content remains.

```bash
echo "=== LOOP 2: CONTENT CORRECTNESS ==="
echo -n "Conflict markers: "; grep -rc '<<<<<<\|======\|>>>>>>' CLAUDE.md 2>/dev/null || echo "0"
echo -n "Prisma refs: "; grep -rl "prisma" .clinerules/ .windsurf/rules/ .roo/rules/ .trae/rules/ .kiro/steering/ .kilo/rules/ .github/instructions/ 2>/dev/null | wc -l
echo -n "TypeScript-only: "; grep -rl "Use TypeScript for all new code" .cursor/rules/ .clinerules/ .github/ 2>/dev/null | wc -l
echo -n "cerebras-mcp: "; grep -rl "cerebras-mcp" .clinerules/ .cursor/rules/ 2>/dev/null | wc -l
echo -n "windsurf,windsurf: "; grep -c "windsurf,windsurf" .windsurf/rules/dev_workflow.md 2>/dev/null || echo "0"
echo -n "Placeholder keys: "; grep -rl "YOUR_.*_HERE" .windsurf/mcp.json .kilo/mcp.json 2>/dev/null | wc -l
```

### 9.3 Loop 3: MCP Config Consistency

Verify all MCP configs match canonical pattern.

```bash
echo "=== LOOP 3: MCP CONSISTENCY ==="
canonical=$(python3 -c "import json; d=json.load(open('.mcp.json')); print(d['mcpServers']['task-master-ai']['command'])")
for f in .roo/mcp.json .cursor/mcp.json .claude/mcp.json .windsurf/mcp.json .trae/mcp.json .kilo/mcp.json; do
  cmd=$(python3 -c "import json; d=json.load(open('$f')); print(d['mcpServers']['task-master-ai']['command'])" 2>/dev/null)
  echo -n "$f command: "; [ "$cmd" = "$canonical" ] && echo "MATCH" || echo "MISMATCH ($cmd)"
done
```

### 9.4 Loop 4: Tool-Specific Context Injection Test

Simulate what each tool loads on startup.

```bash
echo "=== LOOP 4: CONTEXT INJECTION ==="
echo -n "Claude: "; test -s CLAUDE.md && test -s AGENTS.md && test -s .claude/mcp.json && echo "PASS" || echo "FAIL"
echo -n "Amp: "; test -s AGENT.md && test -s AGENTS.md && echo "PASS" || echo "FAIL"
echo -n "Cursor: "; test -s .cursor/mcp.json && ls .cursor/rules/*.mdc >/dev/null 2>&1 && echo "PASS" || echo "FAIL"
echo -n "Cline: "; ls .clinerules/cline_rules.md >/dev/null 2>&1 && echo "PASS" || echo "FAIL"
echo -n "Windsurf: "; test -s .windsurf/mcp.json && ls .windsurf/rules/*.md >/dev/null 2>&1 && echo "PASS" || echo "FAIL"
echo -n "Roo: "; test -s .roo/mcp.json && test -f .roo/rules/.roomodes && echo "PASS" || echo "FAIL"
echo -n "Trae: "; test -s .trae/mcp.json && ls .trae/rules/*.md >/dev/null 2>&1 && echo "PASS" || echo "FAIL"
echo -n "Kiro: "; test -s .kiro/settings/mcp.json && ls .kiro/steering/*.md >/dev/null 2>&1 && echo "PASS" || echo "FAIL"
echo -n "Kilo: "; test -s .kilo/mcp.json && ls .kilo/rules/*.md >/dev/null 2>&1 && echo "PASS" || echo "FAIL"
echo -n "Copilot: "; test -s .github/copilot-instructions.md && echo "PASS" || echo "FAIL"
echo -n "VS Code: "; ls .github/instructions/*.instructions.md >/dev/null 2>&1 && echo "PASS" || echo "FAIL"
```

### 9.5 Loop 5: Cross-Tool Parity (Hash Comparison)

```bash
echo "=== LOOP 5: HASH PARITY ==="
for base in taskmaster.md dev_workflow.md self_improve.md; do
  echo "--- $base ---"
  md5sum .clinerules/$base .windsurf/rules/$base .roo/rules/$base .trae/rules/$base .kiro/steering/$base .kilo/rules/$base 2>/dev/null
done
```

### 9.6 Loop 6: Ruler Dry-Run

```bash
echo "=== LOOP 6: RULER DRY-RUN ==="
ruler apply --project-root . --dry-run 2>&1 | head -20
```

### 9.7 Loop 7: RuleSync --check CI

```bash
echo "=== LOOP 7: RULESYNC CHECK ==="
npx rulesync generate --check --targets cline,cursor,roo,kiro,windsurf --features rules 2>&1 | tail -5
```

### 9.8 Loop 8: Agent RuleZ Debug Scenarios

```bash
echo "=== LOOP 8: RULEZ SCENARIOS ==="
rulez debug PreToolUse --tool Bash --command "git push --force origin main" 2>&1 | grep -o "Blocked\|Allowed"
rulez debug PreToolUse --tool Bash --command "git commit -m 'feat: test'" 2>&1 | grep -o "Blocked\|Allowed"
rulez debug PreToolUse --tool Bash --command "cat .env" 2>&1 | grep -o "Blocked\|Allowed"
rulez debug PreToolUse --tool Bash --command "git add -A" 2>&1 | grep -o "Blocked\|Allowed"
rulez debug PreToolUse --tool Bash --command "git add src/main.py" 2>&1 | grep -o "Blocked\|Allowed"
```

**Expected results:** `Blocked, Allowed, Blocked, Blocked, Allowed`

---

## 10. Recommended Tasks (for backlog tracking)

### 🔴 Priority 0 — Critical (Block tool usage)

| # | Task | Files Affected | Est. |
|---|------|---------------|------|
| T1 | Resolve CLAUDE.md merge conflict | `CLAUDE.md` | 5 min |
| T2 | Populate empty MCP configs (.roo, .cursor, .claude) | 3 files | 10 min |
| T3 | Create .trae/mcp.json | 1 file | 5 min |
| T4 | Fix Windsurf MCP placeholder keys | `.windsurf/mcp.json` | 5 min |
| T5 | Fix Kilo MCP placeholder keys | `.kilo/mcp.json` | 5 min |
| T6 | Fix cerebras-MCP override files | `.clinerules/CLAUDE.md`, `.cursor/rules/CLAUDE.md` | 2 min |

### 🟡 Priority 1 — Major (Wrong content)

| # | Task | Files Affected | Est. |
|---|------|---------------|------|
| T7 | Fix Prisma references (all 8 dirs) | 16 files | 30 min |
| T8 | Fix `--rules windsurf,windsurf` bug | `.windsurf/rules/dev_workflow.md` | 5 min |
| T9 | Fix TypeScript-only content (9 files) | 9 files across .cursor, .clinerules, .github | 20 min |
| T10 | Delete `_deep` duplicate files | 6 files (1,960 lines) | 5 min |
| T11 | Update rulesync.jsonc targets | `rulesync.jsonc` | 5 min |
| T12 | Delete stale `.rules` file | `.rules` | 2 min |

### 🟠 Priority 2 — Moderate (Organization/infrastructure)

| # | Task | Files Affected | Est. |
|---|------|---------------|------|
| T13 | SPLIT GEMINI.md — extract Jules template, keep Gemini CLI at root | `GEMINI.md` → split, `.gemini/JULES_TEMPLATE.md` | 15 min |
| T14 | REPLACE QWEN.md content — copy to docs, write Tier 2 instructions | `QWEN.md`, `docs/SCIENTIFIC_BRANCH_DOCS.md` | 20 min |
| T15 | Fix refs in tools-manifest.json (status: not_on_branch) | 1 file | 10 min |
| T16 | Create .ruler/ canonical config | 2 files | 15 min |
| T17 | Create .claude/hooks.yaml policy | 1 file | 10 min |
| T18 | Create subdirectory AGENTS.md (src/core/, backend/) | 2 files | 30 min |
| T19 | Distribute logic_preservation.md to all tools | 7 files | 15 min |
| T20 | Document Kiro hooks workflow contradiction | 1 file | 10 min |

### ⚪ Priority 3 — Enhancement (Future)

| # | Task | Description | Est. |
|---|------|-------------|------|
| T21 | Configure Ruler for canonical distribution | Full `ruler apply` run | 30 min |
| T22 | Set up RuleSync CI pipeline | `.github/workflows/` | 30 min |
| T23 | Fetch agentrulegen.com Python/FastAPI template | Content enhancement | 1 hr |
| T24 | Upload configs to agentrulegen.com/analyze | Validation | 30 min |
| T25 | Audit `.vscode/mcp.json` | Unaudited config | 10 min |
| T26 | Content deduplication with Ruler | Reduce 11,092 → ~1,200 lines | 2-4 hrs |

---

*Total estimated effort: ~8-10 hours across all priorities.*  
*See `docs/AGENT_RULES_IMPLEMENTATION_HANDOFF.md` for step-by-step execution instructions (Phases 1-10).*
