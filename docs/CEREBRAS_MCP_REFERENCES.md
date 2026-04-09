# Cerebras-MCP References Analysis

## Summary

**Status**: DANGEROUS override files found on current branch only.

## Files Found

### 1. Override Files with Dangerous Content (EDIT)

| File | Size | Branch | Status |
|------|------|--------|--------|
| `.clinerules/CLAUDE.md` | 267 bytes | `origin/004-guided-workflow` only | 🟡 EDIT |
| `.cursor/rules/CLAUDE.md` | 267 bytes | `origin/004-guided-workflow` only | 🟡 EDIT |

**Content** (identical in both files):
```yaml
---
root: false
targets:
  - 'claudecode'
description: 'Claude-specific rules'
globs:
  - '**/*'
---
# CRITICAL: NEVER use any other code editing tools
# ONLY use the cerebras-mcp 'write' tool for ALL code modifications
# This is a hard requirement, not a suggestion
```

**Why Dangerous**: These files instruct Claude Code to use a non-existent `cerebras-mcp` tool for all code modifications. This would break Claude Code's ability to edit files.

### 2. Legitimate Cerebras Reference (KEEP)

| File | Line | Purpose |
|------|------|---------|
| `.aider.conf.yml` | 42 | API key for Cerebras LLM provider |

**Content**:
```yaml
- "cerebras=${CEREBRAS_API_KEY}"
```

**Why Keep**: This is legitimate Aider configuration for using Cerebras as an LLM model provider, not an MCP override.

## Branch Distribution

```
Branches with cerebras-MCP override files: 1 (origin/004-guided-workflow)
Total remote branches: 541
```

The override files only exist on the current branch and were introduced in commit `d3f855d6`.

## Git History

```
commit d3f855d6
Author: Masum Rab
Date:   (recent)
Message: chore(hub): apply stashed spec assembly and resolve conflicts
```

## MCP Server Configs Checked

| Config File | Cerebras Reference |
|-------------|-------------------|
| `.mcp.json` | ❌ None |
| `.claude/mcp.json` | ❌ Empty file |
| `.cline/mcp.json` | ❌ None |
| `.cursor/mcp.json` | ❌ None |
| `.kilo/mcp.json` | ❌ None |
| `.kiro/settings/mcp.json` | ❌ None |
| `.roo/mcp.json` | ❌ None |
| `.windsurf/mcp.json` | ❌ None |

**Conclusion**: No cerebras MCP server is configured anywhere. The override files reference a non-existent tool.

## Recommended Action

**Phase 6.3 of handoff**: Edit both files to remove dangerous cerebras-mcp override content.

**Option A: Replace with proper CLAUDE.md content (RECOMMENDED)**
```bash
# Replace with standard Claude Code rules
cat > .clinerules/CLAUDE.md << 'EOF'
---
root: false
targets:
  - 'claudecode'
description: 'Claude-specific rules'
globs:
  - '**/*'
---
# Claude Code rules for Cline
# See AGENTS.md for full project instructions
EOF

cat > .cursor/rules/CLAUDE.md << 'EOF'
---
root: false
targets:
  - 'claudecode'
description: 'Claude-specific rules'
globs:
  - '**/*'
---
# Claude Code rules for Cursor
# See AGENTS.md for full project instructions
EOF
```

**Option B: Delete if not needed**
```bash
# Only if these files are redundant with other rule files
rm .clinerules/CLAUDE.md
rm .cursor/rules/CLAUDE.md
```

**Note**: The files have valid frontmatter and correct `targets: ['claudecode']`. Only the dangerous comment lines (9-11) need removal.

## Verification Commands

```bash
# Check if files exist
ls -la .clinerules/CLAUDE.md .cursor/rules/CLAUDE.md

# Count occurrences across branches
git branch -r | while read b; do git show "$b:.clinerules/CLAUDE.md" 2>/dev/null && echo "=== $b ==="; done

# Search for cerebras in MCP configs
grep -r "cerebras" ./*/mcp.json .mcp.json 2>/dev/null
```

## Related Documentation

- `docs/AGENT_RULES_GAP_ANALYSIS_AND_CONTENT_MAP.md` - Section W5, G4
- `docs/AGENT_RULES_IMPLEMENTATION_HANDOFF.md` - Step 6.3
