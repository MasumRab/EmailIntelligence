# Orchestration IDE Agent Distribution Plan

**Status:** Active  
**Branch:** orchestration-tools  
**Last Updated:** 2025-11-17  
**Commit:** 60bc0f0d

---

## Overview

This document outlines the distribution strategy for IDE-specific agent instruction files and configurations from the orchestration-tools branch to secondary branches (main, scientific).

---

## Distribution Architecture

### Source Branch: orchestration-tools
Primary repository for all orchestration and IDE agent configurations.

**Contains:**
- Core AGENTS.md (Task Master baseline)
- IDE-specific agent files (CRUSH.md, LLXPRT.md, IFLOW.md, QWEN.md, CLAUDE.md, etc.)
- IDE configuration directories (.claude, .cursor, .windsurf, .roo, .kilo)
- MCP server configuration (.mcp.json)
- GitHub instructions (.github/instructions/**)
- Orchestration control modules

### Target Branches

#### main
- **Purpose:** Stable release branch
- **Distribution:** Full IDE agent files + core orchestration
- **Schedule:** On-demand, synchronized with orchestration-tools changes

#### scientific
- **Purpose:** Scientific computing focus
- **Distribution:** IDE agent files only (excludes orchestration-specific modules)
- **Schedule:** On-demand, with scientific branch policy compliance

---

## File Distribution Matrix

### Always Distributed to All Branches

| Files | Rationale |
|-------|-----------|
| AGENTS.md | Core agent guidance (variant per branch) |
| CRUSH.md, LLXPRT.md, IFLOW.md | IDE-specific extensions |
| QWEN.md, CLAUDE.md | Model-specific guidance |
| terminal-jarvis_AGENTS.md, cognee-AGENTS.md | Additional agent support |
| .mcp.json | MCP configuration (standardized) |
| .env.example | Environment setup template |

### Conditionally Distributed

| Files | main | scientific | Rationale |
|-------|------|-----------|-----------|
| .claude/, .cursor/, .windsurf/ | ✅ | ✅ | IDE configurations |
| .roo/, .kilo/ | ✅ | ✅ | IDE configurations |
| .github/instructions/** | ✅ | ✅ | Shared instructions |
| Orchestration modules | ✅ | ❌ | Orchestration-only |

### Never Distributed

| Files | Rationale |
|-------|-----------|
| .git-rewrite/ | Maintenance directory |
| .taskmaster/ | Project-specific tasks |
| .specify/, .context-control/ | Branch-specific profiles |
| Resolution-workspace/ | Temporary resolution work |

---

## Distribution Procedure

### Step 1: Verify Inclusion in orchestration-tools

```bash
# Run validation script
bash scripts/validate-ide-agent-inclusion.sh

# Expected output: ✅ All IDE agent files are properly included!
```

### Step 2: Create Distribution Branch

```bash
# From orchestration-tools
git checkout orchestration-tools
git pull origin orchestration-tools

# Create distribution branch
git checkout -b dist/ide-agents-$(date +%Y%m%d) orchestration-tools
```

### Step 3: Distribute to main

```bash
# Merge IDE agent files to main
git checkout main
git pull origin main

# Merge specific files from distribution branch
git merge --no-commit --no-ff dist/ide-agents-20251117

# Remove orchestration-only files if present
git reset HEAD orchestration/*.py  # Example: remove orchestration modules
git rm --cached orchestration/*.py

# Commit distribution
git commit -m "chore: distribute IDE agent files from orchestration-tools

- Add/update IDE-specific agent instruction files
- Include CRUSH.md, LLXPRT.md, IFLOW.md, QWEN.md, CLAUDE.md
- Distribute IDE configurations: .claude, .cursor, .windsurf, .roo, .kilo
- Update .mcp.json and .env.example
- Validate via validate-ide-agent-inclusion.sh"
```

### Step 4: Distribute to scientific

```bash
# Checkout scientific branch
git checkout scientific
git pull origin scientific

# Merge IDE agent files (excluding orchestration modules)
git merge --no-commit --no-ff dist/ide-agents-20251117

# Remove orchestration-specific modules
git reset HEAD orchestration/modules/  # Example path
git rm --cached orchestration/modules/

# Verify scientific branch compliance
git log --oneline -5 | head -5

# Commit
git commit -m "chore: distribute IDE agent files to scientific branch

- Add/update IDE-specific agent instruction files
- Include IDE configurations (.claude, .cursor, .windsurf, .roo, .kilo)
- Maintain scientific branch policy (no orchestration modules)
- Pass validate-ide-agent-inclusion.sh checks"
```

### Step 5: Validation

```bash
# On each branch, validate inclusion
git checkout main && bash scripts/validate-ide-agent-inclusion.sh
git checkout scientific && bash scripts/validate-ide-agent-inclusion.sh
git checkout orchestration-tools && bash scripts/validate-ide-agent-inclusion.sh
```

### Step 6: Push to Remote

```bash
# Push all branches
git push origin main main
git push origin scientific scientific
git push origin orchestration-tools orchestration-tools

# Clean up distribution branch
git branch -d dist/ide-agents-20251117
```

---

## Automated Distribution (Future)

### GitHub Actions Workflow

Create `.github/workflows/distribute-ide-agents.yml`:

```yaml
name: Distribute IDE Agents

on:
  push:
    branches:
      - orchestration-tools
    paths:
      - 'AGENTS.md'
      - 'CRUSH.md'
      - 'LLXPRT.md'
      - 'IFLOW.md'
      - 'QWEN.md'
      - 'CLAUDE.md'
      - '.claude/**'
      - '.cursor/**'
      - '.windsurf/**'
      - '.roo/**'
      - '.kilo/**'
      - '.mcp.json'
      - '.env.example'

jobs:
  distribute:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
          
      - name: Validate inclusion
        run: bash scripts/validate-ide-agent-inclusion.sh
        
      - name: Distribute to main
        run: |
          git config user.name "Distribution Bot"
          git config user.email "bot@example.com"
          git checkout main
          git merge orchestration-tools --no-commit --no-ff
          git commit -m "chore: distribute IDE agents from orchestration-tools"
          
      - name: Distribute to scientific
        run: |
          git checkout scientific
          git merge orchestration-tools --no-commit --no-ff
          # Remove orchestration-only files
          git reset HEAD orchestration/
          git commit -m "chore: distribute IDE agents to scientific"
          
      - name: Push changes
        run: |
          git push origin main
          git push origin scientific
```

---

## Integration with CRUSH, LLXPRT, IFLOW

### File Relationships

```
orchestration-tools/
├── AGENTS.md (core baseline)
├── CRUSH.md (extends AGENTS.md for Crush IDE)
├── LLXPRT.md (extends AGENTS.md for extended reasoning)
├── IFLOW.md (extends AGENTS.md for Cursor inline workflows)
├── QWEN.md (Qwen-specific configuration)
├── CLAUDE.md (Claude Code integration)
├── .claude/ (Claude Code configurations)
├── .cursor/ (Cursor IDE rules)
├── .windsurf/ (Windsurf IDE rules)
├── .roo/ (Roo IDE rules)
└── .kilo/ (Kilo Code rules)
```

### Cross-References

All IDE-specific files reference AGENTS.md for core functionality:
- "See AGENTS.md for complete Task Master commands..."
- Links to core AGENTS.md in footer
- Cross-references to other IDE files where applicable

---

## Validation & Quality Assurance

### Pre-Distribution Checklist

- [ ] Run `validate-ide-agent-inclusion.sh` on orchestration-tools
- [ ] Verify all agent files are tracked in git
- [ ] Check .gitignore doesn't exclude IDE configs
- [ ] Review IDE config directories for sensitive data
- [ ] Validate MCP configuration (.mcp.json)
- [ ] Test links and references in markdown files

### Post-Distribution Checklist

- [ ] Run validation on main branch
- [ ] Run validation on scientific branch
- [ ] Verify no orchestration-only files in scientific
- [ ] Spot-check key agent files for completeness
- [ ] Verify .mcp.json is identical across branches
- [ ] Test file references work correctly

---

## Troubleshooting

### Issue: Validation script fails on secondary branch

**Cause:** IDE config directories not properly merged  
**Solution:**
```bash
git checkout branch-name
git merge orchestration-tools --no-commit
git add .claude .cursor .windsurf .roo .kilo
git commit -m "fix: ensure IDE configs merged"
```

### Issue: orchestration-only files leaked to scientific

**Cause:** Merge not properly filtered  
**Solution:**
```bash
git checkout scientific
git log --oneline -1  # Find the merge commit
git revert -m 1 <commit-hash>
# OR manually remove files
git rm --cached orchestration/modules/
git commit -m "fix: remove orchestration modules from scientific"
```

### Issue: .mcp.json diverges between branches

**Cause:** Independent changes in branches  
**Solution:**
1. Update orchestration-tools .mcp.json first
2. Re-run full distribution to synchronize
3. Add .mcp.json to protected patterns in CI

---

## References

- `ORCHESTRATION_IDE_AGENT_INCLUSION.md` - File inclusion manifest
- `AGENTS.md` - Core agent guidance
- `CRUSH.md`, `LLXPRT.md`, `IFLOW.md` - IDE-specific extensions
- `.github/BRANCH_PROPAGATION_POLICY.md` - Branch management policy
- `scripts/validate-ide-agent-inclusion.sh` - Validation script

---

## Contact & Updates

For questions about IDE agent distribution:
1. Check this document first
2. Review `AGENTS.md` for core guidance
3. Review specific IDE file (CRUSH.md, LLXPRT.md, etc.)
4. Consult `ORCHESTRATION_IDE_AGENT_INCLUSION.md` for file tracking

---

*Last validated: 2025-11-17 | Distribution ready for manual or automated deployment*
