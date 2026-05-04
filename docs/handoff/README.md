# Agent Rules Implementation Handoff

## Overview

Execution-ready task files for implementing agent rules infrastructure across EmailIntelligence branches.

## Fresh Start (Any Branch)

1. Copy `STATE_TEMPLATE.md` → `STATE_<branch>.md` (track per-phase completion)
2. Source `context-guard.sh` (auto-detects project root, branch, CWD, tools)
3. Execute phases 0→11 in order (see Execution Order below)

## Phase Files

| Phase | File | Steps | Focus |
|-------|------|-------|-------|
| 0 | `phase-00-content-bootstrap.md` | 4 | agentrulegen.com templates (bootstrap) |
| 1 | `phase-01-emergency-fixes.md` | 13 | MCP configs, merge conflicts |
| 2 | `phase-02-content-fixes.md` | 8 | Prisma refs, TypeScript-only, RuleSync |
| 3 | `phase-03-ruler-setup.md` | 6 | TOML sync configuration |
| 4 | `phase-04-agent-rulez.md` | 6 | Runtime hooks setup |
| 5 | `phase-05-file-cleanup.md` | 6 | Tier 2 root files: GEMINI, QWEN, IFLOW, CRUSH, LLXPRT |
| 6 | `phase-06-deduplication.md` | 6 | Remove duplicate content |
| 7 | `phase-07-hierarchy.md` | 3 | Directory AGENTS.md files |
| 8 | `phase-08-orchestration.md` | 4 | Tool responsibility matrix |
| 9 | `phase-09-verification.md` | 9 | Multi-loop verification |
| 10a | `phase-10-references.md` | 3 | External reference lookup |
| 10b | `phase-10-rule-quality.md` | 8 | Branch-dependent quality evaluation (detect-branch-stack.sh + agentrulegen.com) |
| 10c | `phase-10-stack-evaluation.md` | — | Pre-built rule-by-rule gap analysis for `orchestration-tools` |
| 11a | `phase-11-smart-remediation.md` | 8 | Independent — shell hardening |
| 11b | `phase-11-token-analysis.md` | 5 | Token usage analysis and optimization |
| 12 | `phase-12-deep-agent-handoff.md` | — | Resume-only — `orchestration-tools` deep agent handoff |
| 13 | `phase-13-smart-amp-deep-agent-autonomous-handoff.md` | — | Resume-only — autonomous smart/amp/deep agent handoff |
| 14 | `phase-14-gitignore-unification.md` | 6 | Branch-aware `.gitignore` consolidation (audit → apply → branch-specific tail) |

## Execution Order

1. **Phase 0:** Use agentrulegen.com to bootstrap content (optional, fresh repos)
2. **Phases 1–5:** Sequential (dependencies exist) — required core fixes
3. **Phases 6–8:** Parallel after Phase 5
4. **Phase 9:** Multi-loop verification, after all implementation phases
5. **Phase 10:** Reference + quality evaluation (a/b/c, post-9)
6. **Phase 11:** Independent — shell hardening (a) and token optimization (b)
7. **Phases 12–13:** Resume-only handoffs for specific branches (see "Resume on Existing Branch")
8. **Phase 14:** `.gitignore` unification — independent, run after Phase 9 or any time the working tree is clean

## Mode Selection Guide

| Mode | Phases | Rationale |
|------|--------|-----------|
| Rush | 1–4 | Mechanical edits, no judgment needed |
| Deep | 5–10 | Requires branch-policy judgment and quality review |
| Smart | 11 | Shell script refactoring + token analysis |

## Resume on Existing Branch

1. Open the branch's `STATE_<branch>.md` to find the last completed phase
2. Read the incomplete phase doc and continue from the next unchecked step
3. For `orchestration-tools` resume specifically, use `phase-12-deep-agent-handoff.md` and `phase-13-smart-amp-deep-agent-autonomous-handoff.md`

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

## Reference Documents

- `docs/AGENT_RULES_GAP_ANALYSIS_AND_CONTENT_MAP.md` — Issue inventory
- `docs/handoff/AGENTS_REVIEW_PROCESS.md` — Review workflow (if present)
- `docs/handoff/TOOL_ECOSYSTEM_COMPATIBILITY.md` — Tool capabilities (if present)
- `docs/handoff/AGENT_TOOLS_HIERARCHY.md` — Tool layering (if present)
