# Orchestration Files Change Monitoring Checklist

## Purpose
Monitor changes to key orchestration files during the alignment process to prevent:
- Deletions of critical orchestration functionality
- Removal of important information
- Breaking changes to orchestration systems

Allow safe additions that can be reviewed later.

## Key Orchestration Files to Monitor

### Core Launch System
- `setup/launch.py` - Primary orchestration launch script
- `launch.py` - Wrapper script for launch functionality
- `launch.sh` - Shell launch script
- `launch.bat` - Windows batch launch script

### Configuration Management
- `pyproject.toml` - Project configuration and dependencies
- `Dockerfile` - Container orchestration
- `docker-compose.yml` - Multi-container orchestration
- `uv.lock` - Dependency lock file

### Agent Context Control
- `src/agents/` - Entire agents directory
- `src/core/context_control/` - Context isolation modules
- `src/context_control/` - Legacy context control (if exists)

### Branch Management & Hooks
- `.git/hooks/` - Git hook scripts
- `.taskmaster/` - Taskmaster orchestration system
- `scripts/` - Orchestration scripts

### Database & Environment Configuration
- `src/core/database.py` - Database orchestration
- `.env` files and environment config
- Configuration files in `config/` directory

## Change Alerting Criteria

### CRITICAL: BLOCK THESE CHANGES
- [ ] **Complete file deletion** of any key orchestration files
- [ ] **Function/method deletion** in orchestration modules
- [ ] **Class deletion** in orchestration modules
- [ ] **Import statement removal** that affects orchestration functionality
- [ ] **Configuration removal** (database URLs, API keys, environment vars)
- [ ] **Dependency removal** critical to orchestration
- [ ] **Launch/entry point deletion** (main functions, CLI entry points)
- [ ] **Critical module import changes** that break orchestration dependencies
- [ ] **Security/permission lowering** in orchestration components
- [ ] **Hook script removal** that affects branch operations

### HIGH PRIORITY: FLAG FOR REVIEW
- [ ] **Function signature changes** in orchestration modules
- [ ] **Parameter list changes** in orchestration functions
- [ ] **Return type changes** in orchestration functions
- [ ] **Configuration value changes** that might affect stability
- [ ] **Dependency version downgrades** for orchestration modules
- [ ] **Permission changes** in orchestration files
- [ ] **Error handling removal** from orchestration components
- [ ] **Logging removal** from orchestration system
- [ ] **Thread/process management changes** in orchestration

### STANDARD REVIEW: DOCUMENT BUT ALLOW
- [ ] **New configuration options** (should be added gradually)
- [ ] **New dependency additions** (review for necessity)
- [ ] **New function implementations** in orchestration modules
- [ ] **New class additions** to orchestration system
- [ ] **Documentation improvements** in orchestration files
- [ ] **Comment additions** to orchestration code
- [ ] **Performance improvements** to orchestration components

## Pre-Alignment Verification Checklist

### Before Starting Any Alignment Task:
- [ ] **Backup orchestration files** before any merge/rebase operations
- [ ] **Document current state** of key orchestration files
- [ ] **Verify launch functionality** works with current codebase
- [ ] **Check agent context control** is functional
- [ ] **Confirm database connectivity** is operational
- [ ] **Test basic orchestration** flows still work

## During Alignment Process Monitoring

### At Each Major Merge/Rebase:
- [ ] **Verify no critical files were deleted**
- [ ] **Check that import statements still work**
- [ ] **Validate launch script functionality**
- [ ] **Confirm orchestration dependencies still exist**
- [ ] **Test basic functionality after each major change**

### Conflict Resolution:
- [ ] **Never delete orchestration functionality during conflict resolution**
- [ ] **When resolving conflicts in orchestration files, favor stability over features**
- [ ] **Always test orchestration functionality after conflict resolution**
- [ ] **Make note of any orchestration-related conflicts for post-alignment review**

## Post-Alignment Validation

### After Each Alignment Operation:
- [ ] **Test launch script**: `python launch.py --system-info`
- [ ] **Verify agent functionality** is still working
- [ ] **Confirm database connections** are still valid
- [ ] **Check that all required dependencies** are still present
- [ ] **Validate branch management hooks** still work correctly
- [ ] **Ensure taskmaster functionality** is preserved

### Final Validation:
- [ ] **Run smoke tests** on orchestration functionality
- [ ] **Verify all critical entry points** still work
- [ ] **Confirm context isolation** is maintained
- [ ] **Test configuration loading** functionality

## Red Flags That Require Immediate Action

### STOP ALIGNMENT PROCESS IF YOU SEE:
- [ ] **Any launch script stops working**
- [ ] **Agent context control functionality broken**
- [ ] **Database connectivity issues**
- [ ] **Critical configuration files deleted**
- [ ] **Dependency management broken**
- [ ] **Git hook scripts removed or broken**
- [ ] **Import errors in orchestration modules**

## Documentation Requirements

### Record Any Changes To:
- [ ] **Orchestration file modification** with reason and impact
- [ ] **Critical functionality changes** with testing results
- [ ] **New orchestration features** for future review
- [ ] **Removed functionality** and justification
- [ ] **Configuration changes** that affect orchestration

## Escalation Process

### If Critical Orchestration Changes Are Detected:
1. **STOP** the current alignment operation
2. **REVERT** to last known good state
3. **DOCUMENT** the issue with specific file and change
4. **INVESTIGATE** the reason for the change
5. **APPLY** appropriate fix with proper testing
6. **CONTINUE** alignment only after validation

This checklist ensures that critical orchestration functionality is preserved during the alignment process while allowing beneficial additions to be incorporated safely.