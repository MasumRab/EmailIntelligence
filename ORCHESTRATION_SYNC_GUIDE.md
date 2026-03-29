# Orchestration Files Sync - Quick Guide

**Status**: Phase 2 Complete  
**Last Updated**: 2025-11-18 17:25

---

## Quick Start

### For orchestration-tools* Branches

```bash
# Preview what would be synced
./scripts/sync_orchestration_files.sh --dry-run

# Verify current state
./scripts/sync_orchestration_files.sh --verify

# Sync all files
./scripts/sync_orchestration_files.sh
```

### Common Tasks

**Sync only setup directory:**
```bash
./scripts/sync_orchestration_files.sh --setup-only
```

**Sync only hooks:**
```bash
./scripts/sync_orchestration_files.sh --hooks-only
```

**Sync only config files:**
```bash
./scripts/sync_orchestration_files.sh --config-only
```

**Force overwrite (experimental):**
```bash
./scripts/sync_orchestration_files.sh --force
```

---

## What Gets Synced?

### Setup Directory (10 files)
- `launch.py` - Main launcher script
- `validation.py` - Environment validation
- `services.py` - Service management
- `environment.py` - Environment setup
- `utils.py` - Utility functions
- `project_config.py` - Project config
- `test_stages.py` - Test management
- `pyproject.toml` - Project metadata
- `requirements.txt` - Dependencies
- `requirements-dev.txt` - Dev dependencies

### Git Hooks (6 files)
- `pre-commit` - Prevents bad commits
- `post-commit` - Logs commits (coming soon: simplified)
- `post-merge` - Handles merges
- `post-checkout` - Detects branch switches
- `post-push` - Post-push actions
- `post-commit-setup-sync` - Setup sync hook

### Configuration Files (4 files)
- `.flake8` - Linting rules
- `.pylintrc` - Python linter config
- `.gitignore` - Git ignore rules
- `.gitattributes` - Git attributes

### Root Scripts (1 file)
- `launch.py` - Root wrapper

---

## Branch Support

### ✓ Supported
- `orchestration-tools` (main branch)
- `orchestration-tools-*` (variant branches)

### ✗ Unsupported (Auto-Skip)
- `taskmaster*` branches
- `main` branch
- `scientific` branch
- Feature branches

---

## Features

### Dry-Run Mode
```bash
./scripts/sync_orchestration_files.sh --dry-run
```
Shows exactly what would be synced **without making changes**.

### Verification Mode
```bash
./scripts/sync_orchestration_files.sh --verify
```
Checks:
- All critical files present
- Python syntax valid
- Git hooks executable
- Config files accessible

### Selective Sync
Sync individual components:
```bash
--setup-only     # Only setup/ directory
--hooks-only     # Only git hooks
--config-only    # Only config files
```

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error (missing files, syntax error, etc.) |

---

## Integration with launch.py

```bash
# Coming soon in Phase 4
python3 launch.py sync              # Full sync
python3 launch.py sync --dry-run    # Preview
python3 launch.py sync --verify     # Verify
```

---

## Troubleshooting

### Issue: "Not on orchestration-tools* branch"
**Reason**: Script only runs on orchestration-tools* branches  
**Solution**: Switch to orchestration-tools branch:
```bash
git checkout orchestration-tools
./scripts/sync_orchestration_files.sh
```

### Issue: "Python syntax error"
**Reason**: One of the synced files has invalid Python  
**Solution**: Check error message and verify file integrity:
```bash
./scripts/sync_orchestration_files.sh --verify
```

### Issue: "Missing critical files"
**Reason**: Some files couldn't be found for syncing  
**Solution**: Verify repository is not corrupted:
```bash
git status
git log --oneline -5
```

---

## Advanced Options

### Dry-Run with Detailed Output
```bash
DEBUG=1 ./scripts/sync_orchestration_files.sh --dry-run
```

### Force Mode (Use with Caution!)
```bash
./scripts/sync_orchestration_files.sh --force
```
Overwrites all local changes. **Warning**: Use only if you know what you're doing.

---

## Design Philosophy (SOLID)

The sync script follows SOLID principles:

- **Single Responsibility** - Each function does one thing
- **Open/Closed** - Easy to extend with new sync types
- **Liskov Substitution** - Sync functions are interchangeable
- **Interface Segregation** - Clear, focused command interface
- **Dependency Inversion** - Modular, independent components

This makes the script:
- ✓ Easy to understand
- ✓ Safe to modify
- ✓ Simple to test
- ✓ Maintainable long-term

---

## Next Steps

### Phase 3: Hook Simplification (In Progress)
Hooks will be simplified to focus on **safety only**:
- Remove file distribution logic
- Remove complex branching
- Keep only essential validation

### Phase 4: Integration (Planned)
- Add `launch.py sync` command
- CI/CD integration
- Automated testing

### Phase 5: Deployment (Planned)
- Full rollout to all branches
- Comprehensive documentation
- User training

---

## Quick Reference

| Task | Command |
|------|---------|
| Show help | `./scripts/sync_orchestration_files.sh --help` |
| Preview changes | `./scripts/sync_orchestration_files.sh --dry-run` |
| Verify files | `./scripts/sync_orchestration_files.sh --verify` |
| Sync all | `./scripts/sync_orchestration_files.sh` |
| Sync setup only | `./scripts/sync_orchestration_files.sh --setup-only` |
| Sync hooks only | `./scripts/sync_orchestration_files.sh --hooks-only` |
| Sync config only | `./scripts/sync_orchestration_files.sh --config-only` |

---

## Related Documentation

- `ORCHESTRATION_TOOLS_REDESIGN.md` - Full redesign plan and tracking
- `.taskmaster/AGENTS.md` - Agent integration guide
- `scripts/sync_orchestration_files.sh` - Script implementation
- `scripts/hooks/` - Git hook implementations

---

**For more details**: See `ORCHESTRATION_TOOLS_REDESIGN.md`
