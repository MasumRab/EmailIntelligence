# Modular Orchestration System - Quick Reference Guide

## System Overview

The Modular Orchestration Distribution System is a centralized, SOLID-principles-based system for distributing orchestration files across branches.

## Architecture

- **Main Script**: `scripts/distribute-orchestration-files.sh` (~50 lines)
- **Modules** (~200 lines each):
  - `modules/config.sh` - Configuration management
  - `modules/validate.sh` - Validation checks
  - `modules/distribute.sh` - File distribution
  - `modules/logging.sh` - Logging and reporting
  - `modules/branch.sh` - Branch operations
  - `modules/safety.sh` - Safety checks
  - `modules/utils.sh` - Utility functions

## Common Commands

### Distribution
```bash
# Dry run (preview changes)
./scripts/distribute-orchestration-files.sh --dry-run

# Sync from remote and distribute
./scripts/distribute-orchestration-files.sh --sync-from-remote --with-validation

# Distribute only setup files
./scripts/distribute-orchestration-files.sh --setup-only

# Distribute only hooks
./scripts/distribute-orchestration-files.sh --hooks-only

# Verify without distributing
./scripts/distribute-orchestration-files.sh --verify
```

### Safety Checks
```bash
# Check for uncommitted files before distribution
./scripts/distribute-orchestration-files.sh --dry-run

# Interactive mode for confirmation
./scripts/distribute-orchestration-files.sh --interactive
```

## Key Safety Features

- ✅ Preserves `.taskmaster/` worktree isolation
- ✅ Preserves `scripts/` and `setup/` directories
- ✅ Warns about uncommitted files
- ✅ Validates before distribution
- ✅ Requires confirmation for destructive actions

## Configuration

Configuration files:
- `config/distribution.json` - Main distribution configuration
- `config/default.json` - Default settings

## Testing

Run comprehensive tests:
```bash
bash tests/modules/run_all_module_tests.sh
```

Individual module tests:
- `bash tests/modules/test_config_module.sh`
- `bash tests/modules/test_validate_module.sh`
- `bash tests/modules/test_distribute_module.sh`
- `bash tests/modules/test_safety_module.sh`

## Troubleshooting

### Common Issues
- **Remote sync fails**: Check internet connection and git remote configuration
- **Permission errors**: Ensure proper file permissions on scripts
- **Configuration errors**: Verify JSON syntax in config files
- **Safety warnings**: Review and confirm before proceeding

### Quick Fixes
```bash
# Make scripts executable
chmod +x scripts/*.sh
chmod +x modules/*.sh

# Check configuration validity
jq . config/distribution.json

# Verify git remote
git remote -v
```

## Best Practices

1. **Always use dry-run first** to preview changes
2. **Check for uncommitted files** before distribution
3. **Validate configuration** before running distribution
4. **Use interactive mode** for important distributions
5. **Review safety warnings** carefully
6. **Test changes** with the test suite before deployment

## Migration Notes

- Distribution logic moved from git hooks to centralized script
- All validation functions preserved and enhanced
- Safety checks strengthened
- Configuration-driven approach implemented