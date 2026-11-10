# Task 013.7: Implement Configuration and Externalization

**Status:** specified
**Priority:** high
**Effort:** TBD
**Complexity:** TBD
**Dependencies:** 013.6

---

## Overview/Purpose

Retention counts, backup directory and the verify-on-restore policy are decisions, not constants. This
task moves them where they can be changed without editing the module.

## Success Criteria

- [ ] [Success criteria to be defined]

## Prerequisites & Dependencies

### Required Before Starting
- [ ] 013.6

### Blocks (What This Task Unblocks)
- [ ] To be defined

### External Dependencies
- [ ] No external dependencies

## Sub-subtasks Breakdown


## Specification Details

### Task Interface
- **ID**: 013.7
- **Title**: Implement Configuration and Externalization
- **Status**: pending
- **Priority**: high
- **Effort**: TBD
- **Complexity**: TBD

### Requirements
1. Settings live in one file (`config/alignment.yaml` or `scripts/alignment/config.py` with defaults
   read from the environment), and no retention number appears inline in `branch_ref_backup.py`.
2. Every setting has a stated default and a stated valid range; an out-of-range value fails at load,
   not at the moment it is used.
3. The backup directory stays confined to the repository even when configured: `_resolve_backup_path`
   already flattens a path to its basename, and the configuration must not imply otherwise.
4. The effective configuration is printed at run start and recorded in the run state.

## Implementation Guide

Read the current defaults before moving them: `BACKUP_DIR = pathlib.Path(".backups")` and
`BACKUP_FILE_DEFAULT = ".branch_backup.json"` at the top of `scripts/branch_ref_backup.py`.

```bash
python -c "import scripts.branch_ref_backup as b; print(b.BACKUP_DIR, b.BACKUP_FILE_DEFAULT)"
```

Keep the module importable without the config file present; a missing config must fall back to the
defaults above, not raise.


### 013.7. Implement Configuration and Externalization

**Effort:** 4-6 hours
**Depends on:** 013.6

**Steps:**
1. Create configuration file for backup settings
2. Implement configuration validation
3. Add external parameter support
4. Create default configuration values
5. Implement configuration loading and validation

**Success Criteria:**
- [ ] Configuration file for backup settings created
- [ ] Configuration validation implemented
- [ ] External parameter support operational
- [ ] Default configuration values defined
- [ ] Configuration loading and validation implemented

---


## Configuration Parameters

- **Owner**: TBD
- **Initiative**: TBD
- **Scope**: TBD
- **Focus**: TBD

## Performance Targets

- **Effort Range**: TBD
- **Complexity Level**: TBD

## Testing Strategy

Test strategy to be defined

## Common Gotchas & Solutions

- [ ] No common gotchas identified

## Integration Checkpoint

### Criteria for Moving Forward
- [ ] All success criteria met
- [ ] Code reviewed and approved
- [ ] Tests passing
- [ ] Documentation updated
- [ ] No critical or high severity issues

## Done Definition

### Completion Criteria
- [ ] All success criteria met
- [ ] Code reviewed and approved
- [ ] Tests passing
- [ ] Documentation updated

## Next Steps

- [ ] Next steps to be defined
