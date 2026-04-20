# Phase 10: External Reference Lookup

**Purpose:** Reference guide for agentrulegen.com and extended tool documentation.
**Usage:** Lookup when implementing content for specific tools.

---

## Extended Tool Ecosystem

### Tier 2 Root File Source Map

| File | Best Source | Fallback | Notes |
|------|-------------|----------|-------|
| `GEMINI.md` | Current tracked root file/history | Reconstruct from current branch history | Split out Jules template, keep Gemini CLI content at root |
| `QWEN.md` | Current tracked root file/history | Preserve current content in `docs/SCIENTIFIC_BRANCH_DOCS.md`, then rewrite root file | Must remain at root if Qwen loader depends on it |
| `IFLOW.md` | `~/github/EmailIntelligenceGem/IFLOW.md` | `docs/handoff/content-archive/ARCHIVED_IFLOW_WORKFLOW.md` + `ARCHIVED_AI_MODELS_SETUP.md` | Unique content worth preserving |
| `CRUSH.md` | `~/github/EmailIntelligenceGem/CRUSH.md` | Leave absent and mark `not_on_branch` | Mostly duplicated by `AGENTS.md` |
| `LLXPRT.md` | `~/github/EmailIntelligenceGem/LLXPRT.md` | Leave absent and mark `not_on_branch` | Mostly duplicated by `AGENTS.md` |

---

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

## Validation via /analyze

After implementation, validate configs at `agentrulegen.com/analyze`:
1. `.ruler/AGENTS.md`
2. `.claude/hooks.yaml`
3. `rulesync.jsonc`
