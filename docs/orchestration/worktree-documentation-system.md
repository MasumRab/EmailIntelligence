# Worktree Documentation Inheritance System

## Overview

The Worktree Documentation Inheritance System provides automated synchronization of common documentation across multiple Git worktrees while maintaining branch-specific documentation independence.

## Architecture

### Directory Structure

```
project/
├── docs/                          # Inheritance base (common docs)
├── worktrees/
│   ├── docs-main/
│   │   ├── docs/
│   │   │   ├── common/docs/      # Inherited from inheritance base
│   │   │   └── main/             # Main branch specific docs
│   │   └── backlog/              # Branch-specific tasks
│   └── docs-scientific/
│       ├── docs/
│       │   ├── common/docs/      # Inherited from inheritance base
│       │   └── scientific/       # Scientific branch specific docs
│       └── backlog/              # Branch-specific tasks
├── scripts/
│   ├── sync_common_docs.py       # Python sync script with conflict resolution
│   ├── sync-common-docs.sh       # Shell sync script
│   ├── auto_sync_docs.py         # Automated sync system
│   ├── maintenance_docs.py       # Maintenance and health checks
│   └── sync_config.json          # Configuration file
└── logs/                         # Sync logs and metrics
```

## Key Features

### 1. Conflict Resolution
- **overwrite**: Replace target files with source (default)
- **backup**: Create timestamped backups before overwriting
- **skip**: Skip conflicting files
- **newer**: Overwrite only if source file is newer

### 2. Automated Synchronization
- Git post-commit hooks for automatic sync on documentation changes
- Scheduled sync via cron/systemd
- CI/CD integration with GitHub Actions

### 3. Monitoring and Maintenance
- Comprehensive health checks
- Automated cleanup of old backups and temp files
- Integrity validation
- Performance metrics and logging

## Usage

### Manual Sync

```bash
# Sync from inheritance base to all worktrees
python scripts/auto_sync_docs.py --run-once

# Sync between specific worktrees
python scripts/sync_common_docs.py --sync-between docs-main docs-scientific

# Use different conflict resolution
python scripts/sync_common_docs.py --sync-from-base --conflict-strategy backup
```

### Automated Setup

```bash
# Run setup script to install hooks and scheduling
./scripts/setup_automation.sh
```

### Maintenance

```bash
# Run full maintenance suite
python scripts/maintenance_docs.py --full

# Check system health only
python scripts/maintenance_docs.py --health

# Perform cleanup only
python scripts/maintenance_docs.py --cleanup
```

## Configuration

The system is configured via `scripts/sync_config.json`:

```json
{
  "sync_rules": {
    "inheritance_base": "docs/clean-inheritance-base",
    "worktrees": ["docs-main", "docs-scientific"],
    "common_docs_path": "docs/common/docs",
    "branch_docs_paths": {
      "docs-main": "docs/main",
      "docs-scientific": "docs/scientific"
    }
  },
  "conflict_resolution": {
    "default_strategy": "backup",
    "auto_backup": true,
    "backup_retention_days": 30
  },
  "automation": {
    "auto_sync_on_commit": false,
    "sync_schedule": "daily",
    "sync_time": "02:00"
  }
}
```

## Workflows

### Development Workflow

1. **Make changes** to documentation in any worktree
2. **Commit changes** - post-commit hook triggers sync
3. **System automatically** syncs common docs across worktrees
4. **Branch-specific docs** remain independent

### Conflict Resolution Workflow

1. **System detects** file conflicts during sync
2. **Applies configured** conflict resolution strategy
3. **Creates backups** if backup strategy is used
4. **Logs conflicts** for review
5. **Maintains data integrity** across all worktrees

### Maintenance Workflow

1. **Scheduled maintenance** runs daily/weekly
2. **Health checks** verify system integrity
3. **Cleanup tasks** remove old backups and temp files
4. **Reports generated** for monitoring and troubleshooting

## Monitoring

### Logs
- `logs/docs_sync.log`: Sync operations and conflicts
- `logs/docs_sync_metrics.json`: Performance metrics
- `logs/maintenance_report_*.json`: Maintenance results

### Metrics
- Sync success/failure rates
- Conflict frequency
- File counts per worktree
- Performance timings

## Troubleshooting

### Common Issues

1. **Worktree not found**
   ```bash
   git worktree list
   git worktree add worktrees/docs-main main
   ```

2. **Permission errors**
   ```bash
   chmod +x scripts/*.sh scripts/*.py
   ```

3. **Sync conflicts**
   - Check `logs/docs_sync.log` for details
   - Use `--conflict-strategy backup` to preserve originals
   - Manually resolve and re-sync

4. **Missing dependencies**
   ```bash
   pip install schedule
   ```

5. **Misplaced documentation files**
   - **Detection**: Run `python scripts/maintenance_docs.py --integrity`
   - **Automatic fix**: Run `python scripts/maintenance_docs.py --fix-misplaced`
   - **Prevention**: Pre-commit hooks prevent committing misplaced files
   - **Manual cleanup**: Move files to correct locations:
     - Task files → `backlog/tasks/`
     - Branch docs → `docs/{branch}/`
     - Common docs → `docs/`

### Handling Misplaced Files

The system includes multiple layers of protection against misplaced documentation:

#### Prevention (Pre-commit Hooks)
- Automatically installed via `setup_automation.sh`
- Prevents committing `.md` files to forbidden locations
- Provides suggestions for correct locations

#### Detection (Maintenance Scripts)
```bash
# Check for misplaced files
python scripts/maintenance_docs.py --integrity

# Automatically fix misplaced files
python scripts/maintenance_docs.py --fix-misplaced
```

#### Automatic Correction
The system intelligently moves misplaced files based on content analysis:
- **Task files** (containing `id: task-` or `status:`) → appropriate backlog
- **Documentation** (containing headers like `#`, `##`) → branch-specific docs
- **Other files** → inheritance base or branch-specific directories

#### Forbidden Locations
Documentation files should NOT be in:
- `src/`, `backend/`, `client/`, `modules/`
- `tests/`, `scripts/`, `deployment/`, `config/`
- `data/`, `models/`, `plugins/`, `shared/`
- `venv/`, `node_modules/`, `__pycache__/`
- `.git/`, `.github/`, `logs/`

### Health Checks

```bash
# Quick health check
python scripts/maintenance_docs.py --health

# Full diagnostic
python scripts/maintenance_docs.py --full
```

## Best Practices

1. **Regular commits** trigger automatic sync
2. **Use backup strategy** for important changes
3. **Monitor logs** for sync issues
4. **Run maintenance** regularly
5. **Keep config updated** with new worktrees

## Integration

### CI/CD
- GitHub Actions workflow automatically syncs on pushes to documentation
- Scheduled runs ensure consistency
- Failure notifications for manual intervention

### Git Hooks
- Post-commit hook syncs on documentation changes
- Pre-commit hooks can validate documentation

### External Tools
- Integrates with documentation generators
- Supports various markdown processors
- Compatible with static site generators