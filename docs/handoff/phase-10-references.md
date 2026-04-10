# Phase 10: External Reference Lookup

**Purpose:** Reference guide for agentrulegen.com and extended tool documentation.
**Usage:** Lookup when implementing content for specific tools.

---

## ⚠️ CRITICAL: AgentsMdAgent Pattern (Ruler Built-in)

**Discovery:** Most AI CLI tools read `AGENTS.md` from project root via `settings.json contextFileName`.

### AgentsMdAgent Base Class (Ruler)

These agents extend `AgentsMdAgent` and **natively read AGENTS.md** — they DON'T need custom `output_path`:

| Agent | Base Class | Default Output | Custom output_path Needed? |
|-------|------------|----------------|---------------------------|
| `gemini-cli` | AgentsMdAgent | `AGENTS.md` | ❌ NO |
| `qwen` | AgentsMdAgent | `AGENTS.md` | ❌ NO |
| `opencode` | AgentsMdAgent | `AGENTS.md` | ❌ NO |
| `amp` | AgentsMdAgent | `AGENTS.md` | ❌ NO |
| `kilocode` | AgentsMdAgent | `AGENTS.md` | ❌ NO |
| `cursor` | AgentsMdAgent | `AGENTS.md` | ⚠️ Optional (reads .cursor/rules/ too) |
| `windsurf` | AgentsMdAgent | `AGENTS.md` | ⚠️ Optional (reads .windsurf/rules/ too) |
| `roo` | AgentsMdAgent | `AGENTS.md` | ⚠️ Optional (reads .roo/rules/ too) |

### Non-AgentsMdAgent Agents (Need Custom Paths)

| Agent | Default Output | Custom output_path Required? |
|-------|----------------|------------------------------|
| `claude` | `CLAUDE.md` | ✅ YES — unique file |
| `cline` | `.clinerules/` | ✅ YES — directory-based |
| `kiro` | `.kiro/steering/` | ✅ YES — unique path |
| `trae` | `.trae/rules/` | ✅ YES — unique path |

### settings.json Schema (Gemini CLI, Qwen)

```json
{
  "contextFileName": "AGENTS.md",
  "mcpServers": { ... },
  "permissions": { "allow": [...], "deny": [...] }
}
```

### Decision Implemented

- **Removed agent sections from ruler.toml** for: `amp`, `qwen`, `opencode`, `kilocode` (pure CLI tools)
- **Kept `output_path` for IDE tools**: `claude`, `cline`, `kiro`, `trae` (non-AgentsMdAgent)
- **Kept `output_path` for hybrid tools**: `cursor`, `windsurf`, `roo` (optional secondary context)
- **Redundant `system.md` files DELETED** (6 files, ~1,020 tokens/sessions saved):
  - `.qwen/system.md`, `.agents/system.md`, `.opencode/system.md`, `.kilo/rules/system.md` (pure CLI)
  - `.cursor/rules/system.md`, `.windsurf/rules/system.md`, `.roo/rules/system.md` (hybrid, using root AGENTS.md only)

---

## Extended Tool Ecosystem

### Additional AI Coding Agents

| Tool | Source | Config File | Key Feature |
|------|--------|-------------|-------------|
| **Hermes Agent** | `github.com/NousResearch/hermes-agent` | `~/.hermes/config.yaml`, `SOUL.md` | Self-improving, skills from experience |
| **Nanocoder** | `github.com/Nano-Collective/nanocoder` | `docs.nanocollective.org` | Local-first, community-driven |
| **Oh-My-Pi** | `github.com/can1357/oh-my-pi` | `omp` CLI | Feature-rich fork of pi |
| **Pi-Mono** | `github.com/badlogic/pi-mono` | `@mariozechner/pi-coding-agent` | Minimal, "Bash is all you need" |
| **Crush** | `github.com/charmbracelet/crush` | `.goosehints` | Terminal-native, Charm ecosystem |
| **Goose** | `github.com/block/goose` | `.goosehints`, recipes YAML | Recipes = reusable workflows |
| **Mistral Vibe** | `mistral.ai/vibe` | CLI-native | Devstral 2, 256k context |
| **Kilo Code** | `kilo.ai`, `github.com/Kilo-Org/kilocode` | `AGENTS.md`, `kilo.jsonc` | Memory bank → AGENTS.md |
| **Every Code** | `github.com/just-every/code` | `AGENTS.md`, `CLAUDE.md` | Auto Drive, multi-agent orchestration |

---

## Detailed Tool Documentation

### Hermes Agent (NousResearch)

| Aspect | Details |
|--------|---------|
| **Config Dir** | `~/.hermes/` |
| **Config File** | `config.yaml` |
| **API Keys** | `.env` |
| **Persona** | `SOUL.md` — primary agent identity |
| **Memory** | `MEMORY.md`, `USER.md` |
| **Skills** | `~/.hermes/skills/` |
| **Key Feature** | Self-improving loop — creates skills from experience |
| **Providers** | OpenRouter, Anthropic, Copilot, custom endpoints |

### Nanocoder (Nano Collective)

| Aspect | Details |
|--------|---------|
| **Install** | `npm install -g @nanocollective/nanocoder` |
| **Docs** | `docs.nanocollective.org` |
| **Key Feature** | Local-first, community-driven, open |
| **Providers** | Local models, OpenRouter, Ollama |

### Pi-Mono / Pi Coding Agent (badlogic)

| Aspect | Details |
|--------|---------|
| **Install** | `npm install -g @mariozechner/pi-coding-agent` |
| **Config** | Project-level, minimal |
| **Philosophy** | "Bash is all you need" |
| **Extensions** | TypeScript extensions, skills, prompt templates |
| **Modes** | Interactive, print/JSON, RPC, SDK |
| **Tools** | `read`, `write`, `edit`, `bash` |

### Oh-My-Pi (can1357)

| Aspect | Details |
|--------|---------|
| **CLI** | `omp` |
| **Base** | Fork of pi-mono with more features |
| **Key Feature** | Power-user version with orchestration |
| **Config** | Same as pi-mono |

### Crush (Charmbracelet)

| Aspect | Details |
|--------|---------|
| **Install** | `github.com/charmbracelet/crush` |
| **Config** | `.goosehints` |
| **Key Feature** | Terminal-native TUI, Charm ecosystem |
| **Providers** | Model-agnostic |
| **Commands** | `crush`, `crush run`, `crush session` |

### Goose (Block)

| Aspect | Details |
|--------|---------|
| **Config** | `.goosehints`, recipes YAML |
| **Key Feature** | Recipes = reusable workflows with parameters |
| **Extension** | `.goose/extensions/` |
| **MCP** | First-class MCP support |
| **Docs** | `block.github.io/goose` |
| **Standard** | Linux Foundation AI Agent Interoperability |

### Mistral Vibe (Mistral AI)

| Aspect | Details |
|--------|---------|
| **Model** | Devstral 2 (123B) |
| **Context** | 256k tokens |
| **Key Feature** | Multi-file orchestration, local or cloud |
| **Local** | Devstral Small 2 (24B) via Ollama/vLLM |
| **Install** | `pip install mistral-vibe` |
| **Pricing** | Le Chat Pro ($14.99/mo) or API |

### Kilo Code (Kilo.ai)

| Aspect | Details |
|--------|---------|
| **Config** | `AGENTS.md`, `kilo.jsonc` |
| **Global Config** | `~/.config/kilo/opencode.json` |
| **Key Feature** | Memory bank deprecated → AGENTS.md |
| **Commands** | `/init`, `/model`, `/mcp` |
| **Install** | `npm install -g @kilocode/cli` |
| **Fork Of** | OpenCode |

### Every Code (just-every)

| Aspect | Details |
|--------|---------|
| **Config** | `AGENTS.md`, `CLAUDE.md` |
| **Key Feature** | Auto Drive orchestration, multi-agent |
| **Commands** | `/plan`, `/code`, `/solve`, `/auto` |
| **Install** | `npx -y @just-every/code` |
| **Fork Of** | OpenAI Codex CLI |
| **Feature** | Code Bridge (error streaming), theming |

---

**Purpose:** Reference guide for agentrulegen.com and extended tool documentation.
**Usage:** Lookup when implementing content for specific tools.

---

## agentrulegen.com Guides

| URL | Key Content | Usage |
|-----|-------------|-------|
| `/guides/what-are-ai-coding-rules` | Tool file locations, 40-60% correction reduction | Foundational setup |
| `/guides/how-to-set-up-cursor-rules` | `.cursor/rules/*.mdc`, YAML frontmatter (`globs`, `alwaysApply`) | Cursor structure |
| `/guides/claude-code-guide` | Hierarchy, `@path` imports, `.claude/rules/` | Claude structure |
| `/guides/github-copilot-instructions` | `.github/copilot-instructions.md`, `applyTo:` frontmatter | Copilot setup |
| `/guides/cursorrules-vs-claude-md` | 8-tool comparison, nesting support matrix | Cross-tool equivalence |
| `/guides/convert-cursor-rules-to-claude-md` | Migration paths, 90%+ content identical | Format conversion |
| `/guides/how-to-code-faster-with-ai` | Spec-first dev, multi-tool orchestration | Workflow patterns |
| `/guides/agent-rules-for-monorepos` | 3 strategies, import boundary rules | Monorepo patterns |
| `/guides/debugging-ai-generated-code` | Common pitfalls, prevention rules | Debugging rules |

---

## agentrulegen.com Templates

| URL | Key Content | Usage |
|-----|-------------|-------|
| `/templates/python-fastapi` | SQLAlchemy 2.0 async, Pydantic v2, error handling | Python/FastAPI rules |
| `/templates/ai-agent-workflow` | Plan mode, subagent strategy, self-improvement loop | Agent workflow |
| `/templates/git-workflow` | Conventional commits, branch strategy, git hooks | Git rules |
| `/templates/code-review` | Checklists, comment prefixes, approval workflow | Code review |
| `/templates/linear-workflow` | Magic words, priority SLA, triage workflow | Task management |

---

## Extended Tool Documentation

### Roo Code

| Aspect | Details |
|--------|---------|
| **Modes File** | `.roomodes` (YAML) at project root |
| **New Structure** | `.roo/modes/{slug}/.roomode` |
| **Per-Mode Rules** | `.roo/rules-{mode-slug}/` |
| **Precedence** | Project `.roo/modes` > `.roomodes` > Global |
| **Groups** | `read`, `edit`, `command`, `mcp` |
| **Schema** | `schemastore.org/roomodes.json` |

### Kiro

| Aspect | Details |
|--------|---------|
| **Steering Files** | `.kiro/steering/*.md` |
| **Foundation Files** | `product.md`, `tech.md`, `structure.md` |
| **Inclusion Modes** | `always`, `fileMatch`, `manual`, `auto` |
| **Frontmatter** | `inclusion: fileMatch` with `fileMatchPattern` |
| **Hooks** | `.kiro/hooks/` |
| **MCP Config** | `.kiro/settings/mcp.json` |

### Trae

| Aspect | Details |
|--------|---------|
| **Rules Location** | AI Management > Rules panel |
| **Personal Rules** | `user_rules.md` |
| **Project Rules** | `project_rules.md` |
| **Builder Mode** | Autonomous project scaffolding |
| **MCP Support** | Yes |

### Letta Code

| Aspect | Details |
|--------|---------|
| **Memory Dir** | `$MEMORY_DIR/` |
| **System Memory** | `system/` (always in context) |
| **External Memory** | `reference/`, `history/` |
| **Commands** | `/init`, `/remember`, `/doctor` |

---

## Cross-Tool Equivalence

### File Locations

| Tool | Rules File | MCP Config |
|------|-----------|------------|
| Cursor | `.cursor/rules/*.mdc` | `.cursor/mcp.json` |
| Claude Code | `CLAUDE.md`, `.claude/rules/` | `.claude/mcp.json` |
| Copilot | `.github/copilot-instructions.md` | — |
| Roo | `.roo/rules-{mode}/` | `.roo/mcp.json` |
| Kiro | `.kiro/steering/*.md` | `.kiro/settings/mcp.json` |
| Trae | `.trae/rules/` | `.trae/mcp.json` |
| Letta Code | `$MEMORY_DIR/system/` | — |

### Frontmatter Syntax

| Tool | Path Scoping | Inclusion |
|------|-------------|-----------|
| Cursor | `globs: "src/**/*.ts"` | `alwaysApply: true` |
| Claude Code | `paths: ["src/**/*.ts"]` | N/A |
| Copilot | `applyTo: "**/*.ts"` | N/A |
| Kiro | `fileMatchPattern: "**/*.ts"` | `inclusion: fileMatch` |

### Nesting Support

| Tool | Hierarchical | Import |
|------|-------------|--------|
| Cursor | Yes | `.cursor/rules/` subdirs |
| Claude Code | Yes | `@path` imports |
| Copilot | No | Root only |
| Windsurf | No | Root only |
| Roo | Partial | `.roo/rules-{mode}/` |
| Kiro | Yes | `.kiro/steering/` subdirs |
| Letta Code | Yes | `[[path]]` refs |

---

## Validation via /analyze (Manual Workflow)

**URL:** https://agentrulegen.com/analyze  
**Limit:** 10,000 characters per analysis (3 free, 10/day with sign in)

### IMPORTANT: No API Available

This is a **manual web interface only**. No API endpoints exist.

## Validation via /analyze (Playwright Browser Automation)

**URL:** https://agentrulegen.com/analyze  
**Limit:** 10,000 characters per analysis (3 free, 10/day with sign in)

### IMPORTANT: No API — Use Browser Automation

No official API exists. Use Playwright to automate:

```bash
# Option A: Node.js version (recommended — playwright already installed)
node scripts/analyze_agent_rules.mjs .ruler/AGENTS.md

# Option B: Python version
pip install playwright && playwright install chromium
python3 scripts/analyze_agent_rules.py .ruler/AGENTS.md

# Batch analysis (multiple configs)
node scripts/analyze_agent_rules.mjs .ruler/AGENTS.md .claude/hooks.yaml rulesync.jsonc
```

### Automation Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│  BROWSER AUTOMATION (scripts/analyze_agent_rules.mjs)           │
├─────────────────────────────────────────────────────────────────┤
│  Step 1: READ — Read config file content                        │
│  Step 2: NAVIGATE — Go to agentrulegen.com/analyze             │
│  Step 3: FILL — Paste content into textarea                     │
│  Step 4: CLICK — Click "Analyze Rules" button                  │
│  Step 5: WAIT — Wait for AI-generated results (60s timeout)     │
│  Step 6: SCRAPE — Extract redundant/essential/improvable rules  │
│  Step 7: SAVE — Output to agent_rules_analysis.json            │
└─────────────────────────────────────────────────────────────────┘
```

### Output Format

```json
{
  "file": ".ruler/AGENTS.md",
  "charCount": 4823,
  "redundant": ["Duplicate type hints rule"],
  "essential": ["No eval() rule", "No secrets rule"],
  "improvable": ["Add specific framework patterns"],
  "missing": ["Error handling patterns", "Testing conventions"]
}
```

### Manual Workflow Steps (Alternative)

If automation fails, use manual workflow:

```bash
# Step 1: Read config file content
cat .ruler/AGENTS.md

# Step 2: CUT — Copy entire content to clipboard
# (Use terminal copy or mouse selection)

# Step 3: PASTE — Visit https://agentrulegen.com/analyze
# - Paste content into text area (max 10,000 chars)
# - Click "Analyze Rules" button
# - Wait for AI-generated results

# Step 4: SCRAPE — Copy analysis results
# - Results show: redundant, essential, improvable rules
# - Copy relevant suggestions to improve rules
# - No API to retrieve results programmatically

# Step 5: UPDATE — Apply suggestions to .ruler/AGENTS.md
# - Manually incorporate feedback
# - Re-run analysis if needed
```

### Character Limits

| File | Typical Size | Fits? |
|------|-------------|-------|
| `.ruler/AGENTS.md` | ~200-400 lines (~5,000 chars) | ✅ YES |
| `.claude/hooks.yaml` | ~50-100 lines (~1,500 chars) | ✅ YES |
| `rulesync.jsonc` | ~200 lines (~4,000 chars) | ✅ YES |

### Session Limits

| Account Type | Analyses | Notes |
|---------------|----------|-------|
| Anonymous | 3 total | Then must sign in |
| Signed in | 10/day | Resets daily |

### What Gets Analyzed

| Category | Description |
|----------|-------------|
| **Redundant** | Duplicate or overlapping rules |
| **Essential** | Must-keep rules |
| **Improvable** | Rules that need refinement |
| **Missing** | Common patterns not covered |

### Automation Note

⚠️ **Cannot be automated** — no API exists. Must be done manually per session.

If automation is needed, consider:
- Using `agent-rules-kit` CLI for offline validation
- Running Ruler dry-run for syntax check
- Using CI `rulesync generate --check` for drift detection

### Files to Validate

After implementation, validate these configs:
1. `.ruler/AGENTS.md` — main rules content
2. `.claude/hooks.yaml` — runtime enforcement rules
3. `rulesync.jsonc` — sync target configuration

---

## Agent Rules Kit (tecnomanu)

**Repository:** https://github.com/tecnomanu/agent-rules-kit  
**MCP Server:** https://github.com/tecnomanu/agent-rules-kit-mcp  
**Related:** PAMPA - Protocol for Augmented Memory of Project Artifacts

| Aspect | Details |
|--------|---------|
| **Version** | v3.8.1 (52 releases) |
| **Type** | CLI tool (`npx agent-rules-kit`) |
| **Purpose** | Bootstrap AI agent rules for 9+ IDEs |
| **IDEs** | Cursor, VS Code/Copilot, Windsurf, Continue, Claude Code, Gemini CLI, OpenAI Codex, Cline, Zed |
| **Stacks** | Laravel, Next.js, React, Angular, Vue, NestJS, Svelte, Astro, React Native, MCP SDKs |
| **MCP Tools** | PAMPA (semantic search), GitHub, Memory, Filesystem, Git |
| **License** | ISC |

### Usage Patterns

**Content Generation (SAFE for Ruler integration):**
```bash
# Generate stack-specific rules
npx agent-rules-kit --stack=python --global

# View generated content
cat .cursor/rules/*.mdc

# Copy relevant sections to .ruler/AGENTS.md
# Then run: ruler apply --project-root .
```

**Direct Installation (CAUTION - may conflict with Ruler):**
```bash
# Generates directly to tool directories
npx agent-rules-kit install --target=cursor
npx agent-rules-kit install --target=windsurf
```

**CRITICAL:** When using with Ruler, use as **content source only** — do NOT use `install` command directly.

### PAMPA Semantic Code Search

| Aspect | Details |
|--------|---------|
| **Purpose** | AI-powered semantic code search for agents |
| **MCP Support** | Yes (`npx pampa mcp`) |
| **Languages** | Python, TypeScript, Java, Go, PHP, and more |
| **Feature** | Semantic understanding of code meaning |
| **Use Case** | Large codebase navigation for AI agents |

**Note:** PAMPA is optional. Prefer **existing AST tools** installed via mise:

### AST-Based Code Search (Already Installed)

| Tool | Version | Purpose | Location |
|------|---------|---------|----------|
| **ast-grep** | 0.42.0 | AST pattern search/rewrite | `pipx:ast-grep-cli` |
| **semgrep** | 1.157.0 | Security/linting with AST | `pipx:semgrep` |
| **ck** (ck-search) | 0.7.0 | Semantic code search | `npm:@beaconbay/ck-search` |

**Usage Examples:**

```bash
# ast-grep — Search code using AST patterns
ast-grep run 'console.log($VAR)' --lang typescript
ast-grep run 'if ($COND) { $BODY }' --lang python
ast-grep scan --config sgrep.yml

# semgrep — Security analysis with AST patterns
semgrep --config=auto .
semgrep --config p/python
semgrep --config p/security-audit

# grep-ast — AST-aware grep (npx)
npx grep-ast "function $NAME($PARAMS)" --lang typescript
```

**Comparison:**

| Feature | ast-grep | semgrep | pampa |
|---------|----------|---------|-------|
| **AST Search** | ✅ | ✅ | ⚠️ Semantic |
| **Rewrite** | ✅ | ✅ | ❌ |
| **Security** | ⚠️ | ✅ | ❌ |
| **MCP Integration** | ❌ | ❌ | ✅ |
| **Installed** | ✅ | ✅ | ❌ |

### MCP Tools Integration

Agent Rules Kit includes multi-select MCP tool rules:

| Tool | Purpose | Best For |
|------|---------|----------|
| PAMPA | Semantic Code Search | Understanding large codebases |
| GitHub | Repository Management | GitHub API integration |
| Memory | Persistent Knowledge | Learning from conversations |
| Filesystem | File Operations | Project organization |
| Git | Version Control | Commit management, branch ops |

### Integration Guidelines

**With Ruler (Current Handoff):**
1. Use `npx agent-rules-kit --stack=...` for content generation
2. Copy generated rules to `.ruler/AGENTS.md`
3. Run `ruler apply` to distribute to all tools
4. **NEVER** use `install` command directly — causes sync drift

**Standalone:**
1. Run `npx agent-rules-kit install --target=...` for each IDE
2. Rules written directly to tool directories
3. No central synchronization

### Compatibility Notes

| Aspect | Compatible? | Notes |
|--------|-------------|-------|
| Content generation | ✅ YES | Use as alternative to agentrulegen.com |
| `install` command | ❌ NO | Conflicts with Ruler sync model |
| Front matter (`.mdc`) | ⚠️ CAUTION | Remove frontmatter before Ruler sync |
| MCP tool rules | ✅ YES | Can generate separately |
| PAMPA integration | ✅ YES | Independent capability |
