# Orchestration Workflow Complete Guide

## Overview

This comprehensive guide covers all aspects of the EmailIntelligence orchestration workflow, from initial setup to advanced maintenance operations. The orchestration system ensures consistent development environments across all branches and worktrees.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Core Concepts](#core-concepts)
3. [Branch Management](#branch-management)
4. [File Synchronization](#file-synchronization)
5. [Hook Management](#hook-management)
6. [Troubleshooting](#troubleshooting)
7. [Advanced Operations](#advanced-operations)
8. [Maintenance Procedures](#maintenance-procedures)

## Quick Start

### For New Developers

```bash
# 1. Clone the repository
git clone https://github.com/MasumRab/EmailIntelligence.git
cd EmailIntelligence

# 2. Install orchestration hooks
bash scripts/install-hooks.sh

# 3. Set up development environment
python setup/launch.py setup

# 4. Start development
python setup/launch.py run --dev
```

### For Existing Contributors

```bash
# Update to latest orchestration
git pull origin main
# Hooks will auto-sync during checkout
```

## Core Concepts

### Orchestration-Tools Branch
The `orchestration-tools` branch serves as the **single source of truth** for:
- Development environment setup
- Shared configuration files
- Git hooks and automation scripts
- Environment synchronization logic

### File Ownership Matrix

| File Type | Owned By | Synced To | Purpose |
|-----------|----------|-----------|---------|
| `setup/*.py` | orchestration-tools | All branches | Environment setup |
| `scripts/hooks/*` | orchestration-tools | All branches | Git automation |
| `.flake8`, `.gitignore` | orchestration-tools | All branches | Code quality |
| `src/`, `modules/` | feature branches | N/A | Application code |
| `tsconfig.json` | feature branches | N/A | Build configuration |

## Branch Management

### Creating Feature Branches

```bash
# From main branch
git checkout main
git pull origin main
git checkout -b feature/my-feature

# Orchestration hooks will automatically:
# - Sync setup files from orchestration-tools
# - Install consistent Git hooks
# - Validate environment setup
```

## Troubleshooting

### Common Issues

#### "Changes to setup/ files blocked"
```
Error: Changes to setup/ files should only be made in the 'orchestration-tools' branch
```
**Solution:**
```bash
# Move changes to orchestration-tools branch
git stash
git checkout orchestration-tools
git stash pop
# Make changes and commit
git push origin orchestration-tools
```

#### "Hook installation failed"
**Symptoms:** Hooks not working, commands failing
**Solution:**
```bash
# Check permissions
ls -la .git/hooks/

# Reinstall hooks
bash scripts/install-hooks.sh --force

# Verify hook executability
chmod +x .git/hooks/*
```

## Advanced Operations

### Reverse Synchronization

When feature branches have approved orchestration improvements:

```bash
# Switch to orchestration-tools
git checkout orchestration-tools

# Run reverse sync
bash scripts/reverse_sync_orchestration.sh feature/branch abc123

# Or use dry-run first
bash scripts/reverse_sync_orchestration.sh feature/branch abc123 --dry-run
```

## Maintenance Procedures

### Regular Maintenance

#### Weekly Tasks
- [ ] Review open orchestration PRs
- [ ] Update dependencies in `orchestration-tools`
- [ ] Test hook functionality across branches
- [ ] Clean up old worktrees

#### Monthly Tasks
- [ ] Audit orchestration-managed files
- [ ] Review hook performance
- [ ] Update documentation
- [ ] Test recovery procedures

This guide provides comprehensive coverage of the orchestration workflow. For specific command references, see individual script documentation or use `--help` flags.
