# Task 006.2: Extend Backups to Primary Branches

**Status:** specified
**Priority:** high
**Effort:** 4-5 hours
**Complexity:** 6/10
**Dependencies:** 006.1

---

## Overview/Purpose

Extend backup mechanism for primary branches with comprehensive backup options.

## Success Criteria

- [ ] Mirror backup working
- [ ] Remote backup working
- [ ] Integrity verification implemented
- [ ] Critical branches can be backed up

## Prerequisites & Dependencies

### Required Before Starting
- [ ] No external prerequisites

### Blocks (What This Task Unblocks)
- [ ] No specific blocks defined

### External Dependencies
- [ ] No external dependencies

## Sub-subtasks Breakdown


## Specification Details

### Task Interface
- **ID**: 006.2
- **Title**: Extend Backups to Primary Branches
- **Status**: specified
- **Priority**: high
- **Effort**: 4-5 hours
- **Complexity**: 6/10

### Requirements
1. Primary branches (`main`, `scientific`, `orchestration-tools`) can be backed up by the same command
   as feature branches, with no special case in the caller.
2. The backup ref for a primary branch is distinguishable from a feature-branch backup by name alone.
3. The command refuses to back up a branch whose SHA is unchanged since the last backup, unless
   `--always` is passed, so a scheduled run does not create one ref per hour.
4. Retention is explicit: a documented number of backups per branch, with the pruning command.
5. Pruning never removes the oldest surviving backup for a branch.

## Implementation Guide

Extend `scripts/branch_ref_backup.py` with `--include-primary` and `--retain N`. Verify the prune path
on a scratch branch before documenting it:

```bash
python scripts/branch_ref_backup.py --include-primary --retain 5
git for-each-ref --format='%(refname)' | grep -c backup
```


## Purpose

Extend backup mechanism for primary branches with comprehensive backup options.

---

## Details

Implement git clone --mirror and remote backup options for critical branches.

### Steps

1. **Implement mirror backup**
   ```bash
   git clone --mirror <repo_url> backup-mirror-<timestamp>.git
   ```

2. **Implement remote backup**
   ```bash
   git push origin backup-<name>:refs/heads/backup-<name>
   ```

3. **Implement integrity verification**
   ```python
   def verify_backup_integrity(original, backup):
       original_hash = subprocess.run(
           ["git", "rev-parse", original],
           capture_output=True, text=True
       ).stdout.strip()
       
       backup_hash = subprocess.run(
           ["git", "rev-parse", backup],
           capture_output=True, text=True
       ).stdout.strip()
       
       return original_hash == backup_hash
   ```

4. **Test comprehensive backup**

---

## Test Strategy

- Test mirror clone (should create .git directory)
- Test remote push backup (should create remote branch)
- Test integrity check (should match commits)

---

## Implementation Notes

### Mirror Backup

```python
def create_mirror_backup(repo_path, backup_dir):
    """Create mirror clone for comprehensive backup."""
    from pathlib import Path
    import shutil
    
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    mirror_path = Path(backup_dir) / f"backup-mirror-{timestamp}.git"
    
    if mirror_path.exists():
        shutil.rmtree(mirror_path)
    
    result = subprocess.run(
        ["git", "clone", "--mirror", repo_path, str(mirror_path)],
        capture_output=True, text=True
    )
    
    if result.returncode == 0:
        print(f"Mirror backup created: {mirror_path}")
        return str(mirror_path)
    else:
        print(f"Mirror backup failed: {result.stderr}")
        return None
```

### Remote Backup

```python
def create_remote_backup(branch_name, remote="origin"):
    """Create backup on remote repository."""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_name = f"backup-{branch_name}-{timestamp}"
    
    result = subprocess.run(
        ["git", "push", remote, f"{branch_name}:refs/heads/{backup_name}"],
        capture_output=True, text=True
    )
    
    if result.returncode == 0:
        print(f"Remote backup created: {backup_name}")
        return backup_name
    else:
        print(f"Remote backup failed: {result.stderr}")
        return None
```

### Integrity Verification

```python
def verify_backup_integrity(branch_name, backup_ref):
    """Verify backup matches original branch."""
    original = subprocess.run(
        ["git", "rev-parse", branch_name],
        capture_output=True, text=True
    ).stdout.strip()
    
    backup = subprocess.run(
        ["git", "rev-parse", backup_ref],
        capture_output=True, text=True
    ).stdout.strip()
    
    if original == backup:
        print(f"Integrity verified: {branch_name} == {backup_ref}")
        return True
    else:
        print(f"Integrity mismatch: {branch_name} != {backup_ref}")
        return False
```

---

## Progress Log

### 2026-01-06
- Subtask file created
- Ready for implementation

---

## Next Steps

After completion, proceed to **Task 006.3**: Integrate into Automated Workflow
**Priority:** high
**Effort:** 4-5 hours
**Complexity:** 6/10
**Dependencies:** 006.1
**Created:** 2026-01-06
**Parent:** Task 006: Implement Robust Branch Backup and Restore Mechanism

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

### Unit Tests
- [ ] Tests cover core functionality
- [ ] Edge cases handled appropriately
- [ ] Performance benchmarks met

### Integration Tests
- [ ] Integration with dependent components verified
- [ ] End-to-end workflow tested
- [ ] Error handling verified

### Test Strategy Notes
- Test mirror clone (should create .git directory)
- Test remote push backup (should create remote branch)
- Test integrity check (should match commits)

## Common Gotchas & Solutions

- [ ] [Common issues and solutions to be documented]

## Integration Checkpoint

### Criteria for Moving Forward
- [ ] All success criteria met
- [ ] Code reviewed and approved
- [ ] Tests passing
- [ ] Documentation updated
- [ ] No critical or high severity issues

## Done Definition

### Completion Criteria
- [ ] All success criteria checkboxes marked complete
- [ ] Code quality standards met (PEP 8, documentation)
- [ ] Performance targets achieved
- [ ] All subtasks completed
- [ ] Integration checkpoint criteria satisfied
