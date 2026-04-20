# Agent Rules Implementation Handoff

## Overview

Execution-ready task files for implementing agent rules infrastructure across EmailIntelligence branches.

## Fresh Start (Any Branch)

1. Copy `STATE_TEMPLATE.md` → `STATE_<branch>.md` (track per-phase completion)
2. Source `context-guard.sh` (auto-detects project root, branch, CWD, tools)
3. Execute phases 1→9 in order (see Execution Order below)

## Phase Files

| Phase | File | Steps | Focus |
|-------|------|-------|-------|
| 1 | `phase-01-emergency-fixes.md` | 13 | MCP configs, merge conflicts |
| 2 | `phase-02-content-fixes.md` | 7 | Prisma refs, TypeScript-only |
| 3 | `phase-03-ruler-setup.md` | 6 | TOML sync configuration |
| 4 | `phase-04-agent-rulez.md` | 6 | Runtime hooks setup |
| 5 | `phase-05-file-cleanup.md` | 6 | Tier 2 root files: GEMINI, QWEN, IFLOW, CRUSH, LLXPRT |
| 6 | `phase-06-deduplication.md` | 6 | Remove duplicate content |
| 7 | `phase-07-hierarchy.md` | 3 | Directory AGENTS.md files |
| 8 | `phase-08-orchestration.md` | 4 | Tool responsibility matrix |
| 9 | `phase-09-verification.md` | 9 | Multi-loop verification |
| 10 | `phase-10-rule-quality.md` | 8 | Branch-dependent quality evaluation (detect-branch-stack.sh + agentrulegen.com) |
| 11 | `phase-11-smart-remediation.md` | 8 | Independent — shell hardening |

## Execution Order

1. Phases 1–5 sequential (dependencies exist)
2. Phases 6–8 parallel after Phase 5
3. Phase 9 after all implementation phases
4. Phase 10 after Phase 9 (quality evaluation)
5. Phase 11 independent (no dependency on 5–10)

## Mode Selection Guide

| Mode | Phases | Rationale |
|------|--------|-----------|
| Rush | 1–4 | Mechanical edits, no judgment needed |
| Deep | 5–10 | Requires branch-policy judgment and quality review |
| Smart | 11 | Shell script refactoring |

## Resume on Existing Branch

1. Open the branch's `STATE_<branch>.md` to find the last completed phase
2. Read the incomplete phase doc and continue from the next unchecked step
3. For `orchestration-tools` resume specifically, `phase-12-deep-agent-handoff.md` and `phase-13-smart-amp-deep-agent-autonomous-handoff.md` exist in this directory

## Context-Agnostic Framework

| File | Purpose |
|------|---------|
| [context-guard.sh](context-guard.sh) | Auto-detects project root, branch, CWD, discovered tools |
| [context-agnostic-gates.sh](context-agnostic-gates.sh) | Gate check functions that work from any CWD/branch |
| [execution-journal.sh](execution-journal.sh) | Structured decision logging helpers |
| [CONTEXT_AGNOSTIC_GUIDE.md](CONTEXT_AGNOSTIC_GUIDE.md) | Full framework documentation |
| [STATE_TEMPLATE.md](STATE_TEMPLATE.md) | Template for creating new branch state files |
| `scripts/detect-branch-stack.sh` | Auto-detects tech stack and recommends agentrulegen.com templates per branch |
| `scripts/verify-agent-content.sh` | Audits .ruler/AGENTS.md claims against live branch state |
| [phase-10-stack-evaluation.md](phase-10-stack-evaluation.md) | Pre-built rule-by-rule gap analysis for `orchestration-tools` |

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
| **iFlow** | `IFLOW.md` | — | branch-specific |
| **Letta Code** | `$MEMORY_DIR/` | — | letta.com |
| **Hermes Agent** | `SOUL.md`, `~/.hermes/` | `~/.hermes/config.yaml` | nousresearch.com |
| **Nanocoder** | `AGENTS.md` | — | nanocollective.org |
| **Pi-Mono** | Project-level | — | badlogic/pi-mono |
| **Oh-My-Pi** | Same as Pi | — | can1357/oh-my-pi |
| **Crush** | `CRUSH.md`, `.goosehints` | — | charmbracelet/crush |
| **Goose** | `.goosehints`, recipes | — | block/goose |
| **LLxPRT** | `LLXPRT.md` | — | branch-specific |
| **Mistral Vibe** | CLI-native | — | mistral.ai |
| **Every Code** | `AGENTS.md`, `CLAUDE.md` | — | just-every/code |

## External Tools

| Tool | Config File | Purpose |
|------|--------------|---------|
| **RuleSync** | `rulesync.jsonc` | Multi-target sync |
| **Ruler** | `.ruler/ruler.toml` | TOML-based sync |
| **Agent RuleZ** | `.claude/hooks.yaml` | Runtime enforcement |
| **Task Master AI** | `.mcp.json` | Task management MCP |
