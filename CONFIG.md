# Configuration Strategy and Details

This document outlines the robust, three-tiered configuration strategy for this project, ensuring consistency, flexibility, and security across all environments.

## Three-Tiered Configuration Hierarchy

The configuration is loaded and merged from three distinct levels, with each subsequent level overriding settings from the previous one:

1.  **Global Configuration (`~/.config/email-intelligence/config.json`)**
    *   **Location:** In your user's home directory, under `.config/email-intelligence/`.
    *   **Purpose:** Stores default settings and API keys that apply to all `EmailIntelligence` projects for the current user. This file is not version-controlled.
    *   **Example:** Default Gemini model, common API keys (which can be overridden).

2.  **Project Configuration (`./agent-config.json`)**
    *   **Location:** In the root directory of each `EmailIntelligence` project.
    *   **Purpose:** Contains project-specific settings. It overrides global settings and defines configurations unique to that project. This file *is* version-controlled.
    *   **Example:** Specific model versions for a project, tool allowlists for Claude, MCP server definitions.

3.  **Local Overrides (`./agent-config.local.json`)**
    *   **Location:** In the root directory of each `EmailIntelligence` project.
    *   **Purpose:** For local development overrides. This file is *git-ignored* and should contain sensitive information or temporary settings that should not be committed to the repository.
    *   **Example:** Local API endpoints, developer-specific API keys, debugging flags.

## Configuration Loading and Merging

The configuration is loaded by a `config_manager.py` script (or similar utility) which performs a "deep merge" operation. This means that nested objects are merged intelligently, allowing you to override specific keys without replacing entire sections.

**Order of Precedence:** Global -> Project -> Local (Local overrides Project, Project overrides Global).

## `agent-config.json` Structure

This file is the primary machine-readable configuration for your agents.

```json
{
  "api_keys": {
    "_comment": "For development, you can place keys here. However, for security, it is STRONGLY recommended to use environment variables (e.g., GEMINI_API_KEY). The loading script will always prioritize environment variables over values in this file.",
    "google": "YOUR_GOOGLE_API_KEY_HERE_OR_LEAVE_EMPTY",
    "anthropic": "YOUR_ANTHROPIC_API_KEY_HERE_OR_LEAVE_EMPTY",
    "perplexity": "YOUR_PERPLEXITY_API_KEY_HERE_OR_LEAVE_EMPTY",
    "openai": "YOUR_OPENAI_API_KEY_HERE_OR_LEAVE_EMPTY"
  },
  "models": {
    "_comment": "Define the default models for different roles across all agents.",
    "main": "claude-3-5-sonnet-20241022",
    "research": "perplexity-llama-3.1-sonar-large-128k-online",
    "fallback": "gpt-4o-mini"
  },
  "agents": {
    "_comment": "Agent-specific configurations. These settings will be used to generate the tool-specific config files (e.g., .claude/settings.json).",
    "gemini": {
      "model": "gemini-1.5-pro-latest",
      "tools": ["file_io", "shell", "google_search"]
    },
    "claude": {
      "model": "claude-3-opus-20240229",
      "allowed_tools": [
        "Edit",
        "Bash(task-master *)",
        "Bash(git *)",
        "mcp__task_master_ai__*"
      ]
    }
  },
  "mcp_servers": {
    "_comment": "Configuration for MCP (Multi-Code-Pilot) servers.",
    "task-master-ai": {
      "command": "npx",
      "args": ["-y", "task-master-ai"]
    }
  }
}
```

## How Agents Access Configuration

In a CLI-centric environment, a `setup_agent_env.sh` script orchestrates the environment setup. This script:

1.  Executes `config_manager.py` to read and merge the configuration files.
2.  `config_manager.py` then:
    *   Exports environment variables (e.g., `GOOGLE_API_KEY`) based on the merged configuration.
    *   Generates or updates tool-specific configuration files (e.g., `.gemini/config.json`, `.claude/settings.json`) in the project directory, which are then read by the respective CLI tools.

This ensures that each CLI agent process starts with a consistent and correctly merged configuration.

---
[Link back to AGENTS.md for general agent overview.](AGENTS.md)
