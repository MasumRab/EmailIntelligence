# Tool Ecosystem Compatibility Analysis

**Purpose:** Analyze integration of `tecnomanu/agent-rules-kit` into current handoff
**Created:** 2026-04-09

---

## Current Handoff Tool Stack

| Tool | Type | Phase | Config | Coverage |
|------|------|-------|--------|----------|
| **agentrulegen.com** | Web UI templates | 0 | `.ruler/AGENTS.md` | 10,000+ rules, 41 languages |
| **Ruler** | TOML static sync | 3 | `.ruler/ruler.toml` | 13 agents |
| **RuleSync** | CI drift detection | 2/8 | `rulesync.jsonc` | 28+ targets |
| **Agent RuleZ** | Runtime enforcement | 4 | `.claude/hooks.yaml` | 7 active rules |

---

## Agent Rules Kit (tecnomanu)

| Aspect | Details |
|--------|---------|
| **Repository** | https://github.com/tecnomanu/agent-rules-kit |
| **Type** | CLI tool (`npx agent-rules-kit`) |
| **Purpose** | Bootstrap AI agent rules for multiple IDEs |
| **IDEs Supported** | 9+ (Cursor, VS Code/Copilot, Windsurf, Continue, Claude, Gemini, OpenAI Codex, Cline, Zed) |
| **Stack Support** | Laravel, Next.js, React, Angular, Vue, NestJS, Svelte, Astro, React Native, MCP SDKs |
| **MCP Tools** | PAMPA, GitHub, Memory, Filesystem, Git (multi-select) |
| **Latest Version** | v3.8.1 (52 releases) |

---

## Compatibility Matrix

| Feature | agentrulegen.com | agent-rules-kit | Ruler | Conflict Risk |
|---------|------------------|-----------------|-------|---------------|
| **Source** | Web UI | CLI | CLI | LOW |
| **Output Format** | Markdown blocks | `.mdc` + `.md` mirror | Syncs `.ruler/AGENTS.md` | **HIGH** |
| **IDE Targets** | 8 tools | 9+ IDEs | 13 agents | MEDIUM |
| **Path Structure** | Custom paste | Tool-specific paths | `.ruler/` → root | **HIGH** |
| **Versioning** | Manual | Auto-detection | Manual | LOW |
| **MCP Integration** | None | 5 MCP tools | None | LOW |
| **Front Matter** | No | Yes (for `.mdc`) | No | MEDIUM |

---

## Why It May Have Been Omitted

### 1. Philosophy Mismatch

**Current approach:** Single source of truth (`.ruler/AGENTS.md`) → distributed via Ruler
```bash
.ruler/AGENTS.md  →  CLAUDE.md
                   →  .cursor/rules/AGENTS.md
                   →  .roo/rules/AGENTS.md
                   →  ...
```

**agent-rules-kit approach:** Generate tool-specific files directly
```bash
npx agent-rules-kit --stack=react --ide=cursor
  → .cursor/rules/react-architecture.mdc
  → .cursor/rules/react-testing.mdc
  → .cursor/rules/react-best-practices.mdc
```

### 2. Path Conflict Risk

| Tool | Target Path | agent-rules-kit Path |
|------|-------------|---------------------|
| Ruler | `CLAUDE.md` | `CLAUDE.md` (same!) |
| Ruler | `.cursor/rules/CLAUDE.md` | `.cursor/rules/*.mdc` (different format) |
| agent-rules-kit | — | `.windsurf/rules/*.md` (same rule dir!) |

**Risk:** `agent-rules-kit install --target=windsurf` may overwrite `.windsurf/rules/` content created by Ruler.

### 3. Format Incompatibility

**Ruler generates:** Plain markdown files (`.md`)
```markdown
# EmailIntelligence Agent Rules

## Code Style
- Use type hints on all functions
...
```

**agent-rules-kit generates:** Cursor rules with frontmatter (`.mdc`)
```markdown
---
description: React architecture patterns
globs: ["**/*.tsx", "**/*.ts"]
---

# React Architecture

Keep components under 20 lines...
```

### 4. Process Flow Conflict

| Step | Current Handoff | With agent-rules-kit |
|------|-----------------|---------------------|
| 1 | Phase 0: agentrulegen.com | `npx agent-rules-kit --stack=...` |
| 2 | Copy to `.ruler/AGENTS.md` | Generates directly to tool dirs |
| 3 | Phase 3: `ruler apply` | Creates files in `.cursor/rules/` |
| 4 | — | **CONFLICT:** Ruler may not sync properly |

---

## Integration Approaches

### Option A: Replace Phase 0 (Not Recommended)

Replace `agentrulegen.com` with `agent-rules-kit`:

```bash
# Phase 0 (new)
npx agent-rules-kit --stack=fastapi --global --ide=claude
```

**PROBLEMS:**
- Bypasses `.ruler/AGENTS.md` single source of truth
- Ruler would need reconfiguration
- agent-rules-kit doesn't support all current tools (Roo, Kiro, Trae)

### Option B: Add as Alternative Phase 0a (Recommended)

Add as parallel option for template generation:

```markdown
## Phase 0: Content Bootstrap

**Option A: agentrulegen.com (Web-based)**
- Visit https://agentrulegen.com
- Select languages, frameworks
- Copy-paste to `.ruler/AGENTS.md`

**Option B: agent-rules-kit (CLI)**
npx agent-rules-kit --stack=python --global --mcp-tools=pampa,github

# Then COPY generated rules to `.ruler/AGENTS.md` (DO NOT use install command)
cat .cursor/rules/*.mdc > .ruler/AGENTS.md
```

**Key:** NEVER use `agent-rules-kit install` directly - use as content source only.

### Option C: MCP Tools Integration Only

Add agent-rules-kit for MCP tool rules:

```bash
# Phase 0 MCP Tools
npx agent-rules-kit --mcp-tools=pampa,github,memory
```

This generates MCP-specific rules that complement (not conflict with) Ruler.

### Option D: Reference Only (Safest)

Document in Phase 10 references, not in execution flow.

---

## Recommended Integration

**DO NOT use agent-rules-kit's `install` command** — it conflicts with Ruler's distribution model.

**SAFE usage:**
1. Use for **content generation only** (Phase 0 alternative)
2. Copy generated content to `.ruler/AGENTS.md`
3. Let Ruler distribute to all tools
4. Use **PAMPA MCP server** for semantic code search (separate concern)

**CLI Command:**
```bash
# Safe: Generate content only
npx agent-rules-kit --stack=python --global

# View generated rules
cat .cursor/rules/*.mdc

# Copy to Ruler source (manual)
# Then run: ruler apply --project-root .
```

**UNSAFE:**
```bash
# DANGEROUS: This bypasses Ruler and may cause sync drift
npx agent-rules-kit install --target=cursor
npx agent-rules-kit install --target=windsurf
```

---

## Summary Table

| Aspect | Safe Integration? | Notes |
|--------|-------------------|-------|
| Content generation | ✅ YES | Use as alternative to agentrulegen.com |
| `install` command | ❌ NO | Conflicts with Ruler distribution |
| MCP tools rules | ⚠️ CAUTION | Generate separately, merge manually |
| PAMPA semantic search | ✅ YES | Independent capability |
| Version detection | ✅ YES | Copy detected versions to AGENTS.md |
| Front matter | ⚠️ CAUTION | Remove before Ruler sync |

---

## Proposed Phase 0 Update

Add agent-rules-kit as Option B:

```markdown
## Phase 0: Content Bootstrap

**Purpose:** Generate framework-specific rules before Ruler sync.

**Option A: agentrulegen.com (Web UI)**
1. Visit https://agentrulegen.com
2. Select: Python, TypeScript, FastAPI, React
3. Export: `.ruler/AGENTS.md`

**Option B: agent-rules-kit (CLI)** 
1. Run: `npx agent-rules-kit --stack=python --global`
2. View: `cat .cursor/rules/*.mdc`
3. Copy: relevant sections to `.ruler/AGENTS.md`
4. DO NOT run: `install` command

**CRITICAL:** Both options feed `.ruler/AGENTS.md` → Ruler distributes.
```
