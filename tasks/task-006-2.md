# Task 006.2: Enhance Backup for Primary/Complex Branches

**Status:** pending
**Priority:** high
**Effort:** 4-5 hours
**Complexity:** 6/10
**Dependencies:** 006.1
**Created:** 2026-01-06
**Parent:** Task 006: Implement Robust Branch Backup and Restore Mechanism

---

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

## Success Criteria

- [ ] Mirror backup working
- [ ] Remote backup working
- [ ] Integrity verification implemented
- [ ] Critical branches can be backed up

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
