# Orchestration User Guide

**Complete guide for managing EmailIntelligence orchestration workflows, hooks, and agent integration.**

---

## Quick Start (5 minutes)

### For New Users
1. **Read this guide** - You're here! ✓
2. **Check current status** - Run: `./scripts/disable-all-orchestration-with-branch-sync.sh --skip-push`
3. **Understand branches** - See [Branch Management](#branch-management) below
4. **Get help** - See [Troubleshooting](#troubleshooting) section

### For Developers
```bash
# Check if orchestration is active
cat .env.local | grep ORCHESTRATION_DISABLED

# See available commands
./scripts/disable-all-orchestration-with-branch-sync.sh --help

# Preview sync changes
./scripts/sync_orchestration_files.sh --dry-run
```

---

## Core Concepts

### What is Orchestration?
EmailIntelligence uses **orchestration** to manage:
- **Git hooks** - Automated validation and syncing
- **Agent integration** - IDE and tool configurations
- **Branch safety** - Preventing conflicts and contamination
- **File distribution** - Keeping tools and configs in sync

### When Orchestration Matters
- **Working on orchestration-tools branches** - Full orchestration active
- **Developing features** - May need to disable for testing
- **Merging to main** - Orchestration ensures clean deployments
- **Using IDE agents** - Orchestration provides agent configurations

---

## Common Workflows

### 1. Disable Orchestration (For Local Development)

**When:** Testing without hooks, debugging, offline work

```bash
# Disable with branch sync (recommended)
./scripts/disable-all-orchestration-with-branch-sync.sh

# Or disable without pushing (for review)
./scripts/disable-all-orchestration-with-branch-sync.sh --skip-push
```

**What happens:**
- ✅ Git hooks disabled (moved to *.disabled)
- ✅ `ORCHESTRATION_DISABLED=true` set in .env.local
- ✅ Branch profiles updated
- ✅ Changes pushed to scientific and main branches

### 2. Re-enable Orchestration

**When:** Done testing, ready to collaborate

```bash
# Re-enable with branch sync
./scripts/enable-all-orchestration-with-branch-sync.sh

# Or re-enable without pushing
./scripts/enable-all-orchestration-with-branch-sync.sh --skip-push
```

**What happens:**
- ✅ Git hooks restored
- ✅ `ORCHESTRATION_DISABLED` cleared
- ✅ Branch profiles updated
- ✅ Changes pushed to scientific and main branches

### 3. Sync Orchestration Files

**When:** On orchestration-tools* branches, need latest tools/configs

```bash
# Preview what will sync
./scripts/sync_orchestration_files.sh --dry-run

# Sync all files
./scripts/sync_orchestration_files.sh

# Sync specific components
./scripts/sync_orchestration_files.sh --setup-only    # Only setup/ directory
./scripts/sync_orchestration_files.sh --hooks-only    # Only git hooks
./scripts/sync_orchestration_files.sh --config-only   # Only config files
```

**What gets synced:**
- Setup directory (launch.py, validation.py, etc.)
- Git hooks (pre-commit, post-commit, etc.)
- Configuration files (.flake8, .pylintrc, etc.)

### 4. Branch Management

#### Working Branches
- **orchestration-tools** - Main orchestration branch (full hooks active)
- **orchestration-tools-* variants** - Feature branches (sync available)
- **main/scientific** - Application branches (orchestration disabled)
- **taskmaster** - Isolated task management (no orchestration)

#### Safe Branch Switching
```bash
# Switch to orchestration branch
git checkout orchestration-tools
./scripts/sync_orchestration_files.sh  # Get latest tools

# Switch to development branch
git checkout main
# Orchestration automatically disabled
```

### 5. IDE Integration

**Agent configurations are automatically included:**
- **AGENTS.md** - Core Task Master guidance
- **CRUSH.md, LLXPRT.md, IFLOW.md** - IDE-specific extensions
- **.claude/, .cursor/, .windsurf/** - IDE configurations
- **.mcp.json** - MCP server configuration

**Validate inclusion:**
```bash
# Check all IDE files are present
bash scripts/validate-ide-agent-inclusion.sh

# List IDE-specific files
git ls-files | grep -E '^(\.(claude|cursor|windsurf)|AGENTS|CRUSH|LLXPRT|IFLOW)'
```

---

## Status Checking

### Check Orchestration Status
```bash
# Is orchestration disabled?
cat .env.local | grep ORCHESTRATION_DISABLED

# Are hooks disabled?
ls .git/hooks/*.disabled

# Check branch profile
cat .context-control/profiles/main.json | grep orchestration_disabled

# Check marker file
ls -la .orchestration-disabled
```

### Check Sync Status
```bash
# Verify files are in sync
./scripts/sync_orchestration_files.sh --verify

# Check for missing files
./scripts/sync_orchestration_files.sh --dry-run
```

### Check Branch Status
```bash
# Current branch
git branch --show-current

# Available orchestration branches
git branch -a | grep orchestration

# Check if on supported branch
./scripts/sync_orchestration_files.sh --help | grep "orchestration-tools"
```

---

## Troubleshooting

### "Command not found" Errors
**Problem:** Scripts not executable or missing
```bash
# Make scripts executable
chmod +x scripts/disable-all-orchestration-with-branch-sync.sh
chmod +x scripts/enable-all-orchestration-with-branch-sync.sh
chmod +x scripts/sync_orchestration_files.sh

# Check scripts exist
ls -la scripts/disable* scripts/enable* scripts/sync*
```

### Push Failed
**Problem:** Cannot push to scientific/main branches
```bash
# Check branch permissions
git remote -v

# Try pushing individually
git push origin scientific
git push origin main

# Or skip push and push manually later
./scripts/disable-all-orchestration-with-branch-sync.sh --skip-push
```

### Hooks Won't Restore
**Problem:** Enable script fails to restore hooks
```bash
# Check backup exists
ls -d .git/hooks.backup-*

# Restore manually
git checkout HEAD -- .git/hooks/
chmod +x .git/hooks/*

# Then re-run enable
./scripts/enable-all-orchestration-with-branch-sync.sh
```

### Sync Fails on Wrong Branch
**Problem:** "Not on orchestration-tools* branch"
```bash
# Switch to correct branch
git checkout orchestration-tools

# Then sync
./scripts/sync_orchestration_files.sh
```

### Python Syntax Errors
**Problem:** Synced files have invalid Python
```bash
# Run verification
./scripts/sync_orchestration_files.sh --verify

# Check error messages for specific files
# Fix the problematic file, then re-sync
```

### IDE Agent Files Missing
**Problem:** Agent configurations not available
```bash
# Validate inclusion
bash scripts/validate-ide-agent-inclusion.sh

# Check specific directories
git ls-files | grep "^\.claude/"
git ls-files | grep "^AGENTS"
```

### Profile Files Corrupted
**Problem:** JSON branch profile files invalid
```bash
# Restore from git
git checkout HEAD -- .context-control/profiles/

# Re-run the orchestration script
./scripts/disable-all-orchestration-with-branch-sync.sh --skip-push
```

---

## Command Reference

### Orchestration Control
```bash
# Disable orchestration
./scripts/disable-all-orchestration-with-branch-sync.sh [--skip-push]

# Enable orchestration
./scripts/enable-all-orchestration-with-branch-sync.sh [--skip-push]

# Check status
cat .env.local | grep ORCHESTRATION_DISABLED
ls .git/hooks/*.disabled 2>/dev/null || echo "Hooks active"
```

### File Synchronization
```bash
# Preview sync
./scripts/sync_orchestration_files.sh --dry-run

# Full sync
./scripts/sync_orchestration_files.sh

# Selective sync
./scripts/sync_orchestration_files.sh --setup-only
./scripts/sync_orchestration_files.sh --hooks-only
./scripts/sync_orchestration_files.sh --config-only

# Verify sync
./scripts/sync_orchestration_files.sh --verify
```

### IDE Integration
```bash
# Validate agent files
bash scripts/validate-ide-agent-inclusion.sh

# List IDE files
git ls-files | grep -E '^(\.(claude|cursor|windsurf)|AGENTS|CRUSH|LLXPRT|IFLOW)'

# Check specific IDE
git ls-files | grep "^\.claude/"
```

### Branch Operations
```bash
# Switch with sync
git checkout orchestration-tools && ./scripts/sync_orchestration_files.sh

# Check current branch
git branch --show-current

# List orchestration branches
git branch -a | grep orchestration
```

### Recovery Commands
```bash
# Restore hooks manually
git checkout HEAD -- .git/hooks/
chmod +x .git/hooks/*

# Restore environment
git checkout HEAD -- .env.local

# Restore profiles
git checkout HEAD -- .context-control/profiles/

# Remove marker
rm -f .orchestration-disabled
```

---

## Branch-Specific Guidance

### orchestration-tools Branch
- **Full orchestration active** - All hooks and validations
- **Use for:** Tool development, hook testing, infrastructure changes
- **Commands:** Use sync scripts, full orchestration control

### orchestration-tools-* Variants
- **Sync available** - Can pull latest tools from main orchestration-tools
- **Use for:** Feature development with orchestration tools
- **Commands:** Use sync scripts, orchestration control works

### main/scientific Branches
- **Orchestration disabled** - Clean application branches
- **Use for:** Application development, user deployments
- **Commands:** Orchestration control available but typically disabled

### taskmaster Branch
- **Isolated** - No orchestration, separate worktree
- **Use for:** Task management, planning
- **Commands:** Standard git, no orchestration scripts

---

## Integration Points

### With Task Master (.taskmaster/)
- **Automatic isolation** - Git worktree prevents staging task files
- **Agent access** - Task files readable by agents but not committable
- **Branch safety** - Pre-commit hooks block accidental commits

### With IDE Agents
- **Configuration sync** - Agent files distributed via orchestration
- **Branch awareness** - Different guidance per branch type
- **Tool integration** - MCP servers and agent tools configured

### With Git Workflows
- **Hook management** - Orchestration controls hook activation
- **Branch protection** - Prevents contamination and conflicts
- **PR automation** - Clean merges between orchestration branches

---

## Advanced Usage

### Custom Sync Operations
```bash
# Force overwrite (use carefully)
./scripts/sync_orchestration_files.sh --force

# Debug output
DEBUG=1 ./scripts/sync_orchestration_files.sh --dry-run
```

### Batch Operations
```bash
# Disable across multiple sessions
for session in {1..3}; do
  ./scripts/disable-all-orchestration-with-branch-sync.sh --skip-push
  echo "Session $session disabled"
done
```

### Monitoring
```bash
# Watch for changes
watch -n 30 './scripts/sync_orchestration_files.sh --verify'

# Log orchestration activity
tail -f logs/orchestration.log 2>/dev/null || echo "No log file"
```

---

## Getting Help

### Documentation Hierarchy
1. **ORCHESTRATION_GUIDE.md** ← This file (user workflows)
2. **ORCHESTRATION_REFERENCE.md** ← Technical details and APIs
3. **ORCHESTRATION_DOCS_AUDIT.md** ← Documentation consolidation audit

### Common Issues
- **Scripts not working?** Check file permissions with `ls -la scripts/`
- **Hooks interfering?** Disable orchestration temporarily
- **Files out of sync?** Run sync script on orchestration-tools branches
- **Agent issues?** Validate IDE inclusion

### Emergency Recovery
If everything breaks:
```bash
# Quick reset
git checkout main
git reset --hard origin/main

# Re-enable basic functionality
./scripts/enable-all-orchestration-with-branch-sync.sh
```

---

## Related Documentation

- **ORCHESTRATION_REFERENCE.md** - Technical implementation details
- **AGENTS.md** - Task Master and agent integration
- **TASKMASTER_BRANCH_CONVENTIONS.md** - .taskmaster/ isolation rules
- **README.md** - Project overview and setup

---

**Last Updated:** November 24, 2025
**Consolidated from:** 4 source documents
**Status:** Ready for use