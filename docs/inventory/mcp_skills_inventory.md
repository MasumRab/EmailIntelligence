# MCP and Agent Skill Fragments Inventory

This document maps the scattered Model Context Protocol (MCP) configurations and Agent Skill instructions across the repository's remote branches for future consolidation into the unified CLI.

## 1. MCP Configurations (`mcp.json`)

| Source Branch | Path | Purpose |
| :--- | :--- | :--- |
| `orchestration-tools` | `.claude/mcp.json` | Claude-specific tool configuration. |
| `orchestration-tools` | `.cline/mcp.json` | Cline-specific tool configuration. |
| `orchestration-tools` | `.cursor/mcp.json` | Cursor-specific tool configuration. |
| `orchestration-tools` | `.mcp.json` (root) | Default MCP configuration. |
| `orchestration-tools` | `jules_mcp_schedule.json` | Task-specific MCP scheduling logic. |
| `local` | `.rulesync/.mcp.json` | Rulesync integration tools. |

## 2. Agent Skills & Instructions

| Source Branch | Path | Description |
| :--- | :--- | :--- |
| `000-integrated-specs` | `.github/instructions/dev_workflow.instructions.md` | Core developer workflow persona. |
| `000-integrated-specs` | `.github/instructions/taskmaster.instructions.md` | Taskmaster automation persona. |
| `000-integrated-specs` | `.github/instructions/tools-manifest.json` | Registry of available CLI tools. |
| `orchestration-tools` | `orchestration_prompts.md` | Prompts for branch synchronization and merge management. |
| `orchestration-tools` | `.agents/commands/speckit.*` | Markdown-based agent command definitions. |

## 3. Context & Strategy Documents

| Source Branch | Path | Description |
| :--- | :--- | :--- |
| `000-integrated-specs` | `MODEL_CONTEXT_STRATEGY.md` | Strategy for managing LLM context window efficiency. |
| `000-integrated-specs` | `agent-config.json` | High-level agent parameter configuration. |
| `scientific` | `docs/LLM_DOCUMENTATION_DISCOVERY.md` | Logic for how agents should discover project docs. |

## Consolidation Target
All identified fragments are scheduled for consolidation into the `src/cli/commands/automation/` (for MCP syncing) and `docs/guides/` (for skill instructions) domains.
