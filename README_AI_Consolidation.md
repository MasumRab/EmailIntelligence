# AI Tools Configurations Centralization and Syncing Plan

## Overview
The AI tools configurations are now centralized in `~/.aiglobal` repository for unified management. Using rulesync, configurations are generated and synced to individual EmailIntelligence project directories. This ensures consistency, version control, and easy maintenance across all projects. The centralization eliminates duplicates, resolves conflicts, and provides seamless AI tool switching.

## Text Diagram of Rulesync Process
```
+-------------------+     +-------------------+     +-------------------+
| 1. Centralize     | --> | 2. Define Rules   | --> | 3. Branch for     |
| Configs in        |     | in .rulesync/     |     | Variants          |
| ~/aiglobal       |     | rules/            |     | (auto, gem, etc.) |
+-------------------+     +-------------------+     +-------------------+
         |                         |                         |
         v                         v                         v
+-------------------+     +-------------------+     +-------------------+
| 4. Generate via   | --> | 5. Validate       | --> | 6. Sync to        |
| Rulesync in       |     | Configs (JSON     |     | Projects          |
| Projects          |     | syntax, files)    |     | (Copy/Merge)      |
+-------------------+     +-------------------+     +-------------------+
         |                         |                         |
         v                         v                         v
+-------------------+     +-------------------+     +-------------------+
| 7. Monitor Drift  | --> | 8. Update Rules   | --> | 9. Push Remote    |
| & Refine Scripts  |     | & Regenerate      |     | for Sharing       |
+-------------------+     +-------------------+     +-------------------+
         |                         |                         |
         +-------------------------+-------------------------+
                                   |
                                   v
                        +-------------------+
                        | Final: Centralized|
                        | AI Config Mgmt    |
                        +-------------------+
```

## Step-by-Step Rulesync Process
1. **Centralize Configs**: Store all AI tool configs in `~/.aiglobal` git repository.
2. **Define Rules**: Create rules in `~/.aiglobal/.rulesync/rules/` for generating configs.
3. **Branch for Variants**: Create git branches for project-specific variants (auto, gem, qwen, aider).
4. **Generate via Rulesync**: Add temporary `.rulesync` to projects, run rulesync to generate configs from centralized rules.
5. **Validate Configs**: Check JSON syntax, file existence, and tool loading capability.
6. **Sync to Projects**: Copy generated configs to all EmailIntelligence project directories.
7. **Monitor Drift**: Use scripts to detect config drift and refine syncing processes.
8. **Update Rules**: Modify rules as needed and regenerate configs across projects.
9. **Push Remote**: Share `~/.aiglobal` repository remotely for team access.

## Key Components
- **Central Repo**: `~/.aiglobal` - Git repository for centralized configs.
- **Rules**: `~/.aiglobal/.rulesync/rules/` - Rules for generating project configs.
- **Branches**: Git branches for project variants.
- **Tools**: rulesync (config generation), bash scripts (syncing), git (version control).
- **Outputs**: Generated .claude/, .cursor/, .mcp.json, AGENTS.md in projects.
- **Constraints**: Rulesync installed, API keys in .env, git access.

## Usage Instructions
1. **Setup**: Ensure `~/.aiglobal` repo exists with rules and configs.
2. **Generate Configs**: Add `.rulesync` to project, run `rulesync` to generate configs.
3. **Validate**: Run validation scripts to check JSON syntax and file existence.
4. **Sync**: Use sync scripts for non-rulesync files (LLMs CLI, TUI, MCPs).
5. **Monitor**: Use `change_report.sh` for traceability, pre-commit hooks for validation.

## Notes
- Configs are version-controlled in `~/.aiglobal` for traceability.
- Temporary `.rulesync` dirs are removed after generation.
- Validation ensures configs are functional before syncing.
- See CONFIG_TRACKING.md for detailed config management.
