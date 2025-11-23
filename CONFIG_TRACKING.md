# Config Tracking

## Overview
This document tracks the AI tool configurations across the EmailIntelligence project ecosystem. Configurations are centralized in `~/.aiglobal` and synced to individual project directories using rulesync.

## Centralized Repository Structure (~/.aiglobal)
- **Git Repository**: Manages version control for all configs
- **Branch Structure**:
  - `master`: Base configurations
  - `emailintelligenceauto`: Auto-specific variants
  - `emailintelligencegem`: Gemini-specific variants
  - `emailintelligenceqwen`: Qwen-specific variants
  - `emailintelligenceaider`: Aider-specific variants

## Configuration Files

### Claude Code (.claude/)
- **Location**: `~/.aiglobal/.claude/`
- **Contents**:
  - `settings.json`: Main settings (permissions, env vars)
  - `agents/`: Agent definitions
  - `commands/`: Custom commands
  - `memories/`: Context memories
- **Sync**: Generated in projects via rulesync

### Cursor IDE (.cursor/)
- **Location**: `~/.aiglobal/.cursor/`
- **Contents**:
  - `rules/`: IDE rules
  - `commands/`: Custom commands
  - `mcp.json`: MCP configuration
- **Sync**: Generated in projects via rulesync

### MCP Servers (.mcp.json)
- **Location**: `~/.aiglobal/.mcp.json`
- **Contents**: Server configurations for serena, context7, etc.
- **Sync**: Copied to projects

### Agent Instructions (AGENTS.md)
- **Location**: `~/.aiglobal/AGENTS.md`
- **Contents**: Instructions for AI agents
- **Sync**: Generated in projects via rulesync

### Opencode Settings (opencode.json)
- **Location**: `~/.aiglobal/opencode.json`
- **Contents**: Opencode CLI configuration
- **Sync**: Generated in projects

## Sync Process
1. **Centralized Rules**: Rules defined in `~/.aiglobal/.rulesync/rules/`
2. **Generation**: Temporary `.rulesync` added to projects to generate configs
3. **Validation**: JSON syntax checks, file existence verification
4. **Cleanup**: Temporary dirs removed, generated files committed

## Validation Checks
- JSON syntax validation for `.mcp.json`
- File existence for `.claude/settings.json`, `.cursor/`, etc.
- Tool loading capability verification

## Maintenance
- **Change Detection**: Pre-commit hooks validate changes
- **API Keys**: Managed in `~/.aiglobal/.env` with validation script
- **Traceability**: `change_report.sh` for git history analysis
- **Non-Rulesync Sync**: `sync_non_rulesync.sh` for LLMs CLI, TUI, MCPs

## Project Directories
Configs synced to:
- `/home/masum/github/EmailIntelligence`
- `/home/masum/github/EmailIntelligenceAuto`
- `/home/masum/github/EmailIntelligenceGem`
- `/home/masum/github/EmailIntelligenceQwen`
- `/home/masum/github/EmailIntelligenceAider`