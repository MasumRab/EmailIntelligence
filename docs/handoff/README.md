# Agent Rules Implementation Handoff

## Overview

This directory contains granular, execution-ready task files for implementing agent rules infrastructure across EmailIntelligence branches.

## Tool Coverage Matrix

| Tool | Rules Dir | MCP Config | Source |
|------|-----------|------------|--------|
| **Cursor** | `.cursor/rules/` | `.cursor/mcp.json` | cursor.sh |
| **Claude Code** | `CLAUDE.md`, `.claude/rules/` | `.claude/mcp.json` | anthropic.com |
| **GitHub Copilot** | `.github/copilot-instructions.md` | — | github.com |
| **Cline** | `.clinerules/` | — | cline.bot |
| **Windsurf** | `.windsurf/rules/` | `.windsurf/mcp.json` | codeium.com |
| **Roo** | `.roo/rules-{mode}/` | `.roo/mcp.json` | roocode.com |
| **Trae** | `.trae/rules/` | `.trae/mcp.json` | trae.ai |
| **Kiro** | `.kiro/steering/` | `.kiro/settings/mcp.json` | kiro.dev |
| **Kilo** | `.kilo/rules/` | `.kilo/mcp.json` | kilo.ai |
| **Gemini CLI** | `GEMINI.md` | — | google.com |
| **Qwen Code** | `QWEN.md` | — | alibaba.com |
| **OpenAI Codex** | `AGENTS.md` | — | openai.com |
| **Letta Code** | `$MEMORY_DIR/` | — | letta.com |
| **Hermes Agent** | `SOUL.md`, `~/.hermes/` | `~/.hermes/config.yaml` | nousresearch.com |
| **Nanocoder** | `AGENTS.md` | — | nanocollective.org |
| **Pi-Mono** | Project-level | — | badlogic/pi-mono |
| **Oh-My-Pi** | Same as Pi | — | can1357/oh-my-pi |
| **Crush** | `.goosehints` | — | charmbracelet/crush |
| **Goose** | `.goosehints`, recipes | — | block/goose |
| **Mistral Vibe** | CLI-native | — | mistral.ai |
| **Every Code** | `AGENTS.md`, `CLAUDE.md` | — | just-every/code |

## External Tools

| Tool | Config File | Purpose |
|------|--------------|---------|
| **RuleSync** | `rulesync.jsonc` | Multi-target sync |
| **Ruler** | `.ruler/ruler.toml` | TOML-based sync |
| **Agent RuleZ** | `.claude/hooks.yaml` | Runtime enforcement |
| **Task Master AI** | `.mcp.json` | Task management MCP |

## Phase Files

| Phase | File | Steps | Focus |
|-------|------|-------|-------|
| 0 | `phase-00-content-bootstrap.md` | 4 | agentrulegen.com templates (NEW) |
| 1 | `phase-01-emergency-fixes.md` | 13 | MCP configs, merge conflicts |
| 2 | `phase-02-content-fixes.md` | 8 | Prisma refs, TypeScript-only, RuleSync (UPDATED) |
| 3 | `phase-03-ruler-setup.md` | 6 | TOML sync configuration |
| 4 | `phase-04-agent-rulez.md` | 6 | Runtime hooks setup |
| 5 | `phase-05-file-cleanup.md` | 4 | GEMINI.md, QWEN.md split |
| 6 | `phase-06-deduplication.md` | 6 | Remove duplicate content |
| 7 | `phase-07-hierarchy.md` | 3 | Directory AGENTS.md files |
| 8 | `phase-08-orchestration.md` | 4 | Tool responsibility matrix |
| 9 | `phase-09-verification.md` | 8 | Multi-loop verification |
| 10 | `phase-10-references.md` | 3 | External reference lookup |
| 11 | `phase-11-token-analysis.md` | 5 | Token optimization (NEW) |

## Execution Order

1. **Phase 0 (NEW):** Use agentrulegen.com to bootstrap content
2. **Phases 1-4 (REQUIRED):** Fix 13 core issues
3. **Phase 5 (OPTIONAL):** GEMINI.md/QWEN.md cleanup
4. **Phases 6-8 (EXTENDED):** Can run in parallel after phase 5
5. **Phase 9:** Multi-loop verification
6. **Phase 10:** Reference material (use as needed)
7. **Phase 11 (NEW):** Token usage analysis and optimization

## Reference Documents

- `AGENT_RULES_GAP_ANALYSIS_AND_CONTENT_MAP.md` — Issue inventory
- `AGENT_RULES_TOOLS_VERIFIED_TEST_RESULTS.md` — Tool capabilities
- `AGENT_RULES_TOOL_INTEGRATION_PLAN.md` — Feasibility analysis
