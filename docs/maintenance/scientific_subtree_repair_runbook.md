# Scientific Subtree Repair Runbook: Git Subtree Management

This runbook provides a structured approach for repairing and maintaining the Git subtree integration in the `scientific` branch. It ensures that shared setup and launch files remain synchronized while preserving specialized scientific development.

---

## 1. Subtree Infrastructure Core

The `scientific` branch uses the `setup/` prefix to manage shared launch and setup files from the central `launch-setup-fixes` branch (or equivalent).

### Prefix Integrity
The standard prefix for the setup subtree is `setup`. All subtree commands must use this exact prefix:
```bash
--prefix=setup
```
**Warning:** Never manually move files into or out of the `setup/` directory using standard `git mv` if you intend to continue using subtree commands, as it will break the subtree's tracking.

### Remote Tracking
Ensure you have the correct remote configured for the source of the subtree:
```bash
git remote add origin <repository-url>  # Usually already exists
```

---

## 2. Recovery & Sync Guide

### Pulling Updates (The Most Common Operation)
If the `setup/` directory is out of sync with the central setup:
```bash
git subtree pull --prefix=setup origin launch-setup-fixes --squash
```
**If conflicts occur during pull:**
1. Resolve the conflicts manually in the `setup/` directory.
2. `git add` the resolved files.
3. `git commit` to complete the merge.
4. **Note:** Treat the `setup/` directory as a "protected zone" during conflict resolution—favor the changes from `origin/launch-setup-fixes` for infrastructure logic unless they explicitly break scientific-specific features.

### Re-initializing a Broken Subtree
If the subtree relationship is completely lost (e.g., the directory exists but `git subtree pull` fails with "can't find a common ancestor"):
1. **Backup your changes:** `cp -r setup/ ../setup_backup`
2. **Remove the directory:** `git rm -r setup && git commit -m "chore: remove broken setup subtree"`
3. **Re-add the subtree:**
   ```bash
   git subtree add --prefix=setup origin launch-setup-fixes --squash
   ```
4. **Restore local scientific changes:** Manually merge scientific-specific logic back from `../setup_backup` if necessary.

---

## 3. Scientific Context Preservation

The `scientific` branch often requires additional dependencies.

### Dependency Merging
When `setup/requirements.txt` is updated via subtree pull:
1. Check if scientific-specific requirements (e.g., `scipy`, `pandas`, or specialized ML libs) were overwritten.
2. If the scientific branch uses a separate `requirements-scientific.txt`, ensure it is still referenced correctly in the launch scripts.
3. If dependencies are merged into the main `requirements.txt`, verify that the union of both branches' needs is met.

### Local Overrides
Scientific-specific launch logic should ideally reside in files *outside* the `setup/` subtree prefix if possible, or be clearly guarded with conditional logic within the subtree files to simplify future merges.

---

## 4. Validation Shield

After any subtree operation, verify the integrity of the setup:

### Syntax Check
Run the automated syntax check for all setup files:
```bash
python3 -m py_compile setup/*.py
```

### Functional Test
Verify that the launcher still correctly identifies the scientific context:
```bash
python3 setup/launch.py --system-info
```

### Post-Repair Checklist
- [ ] Subtree prefix `setup/` contains the latest shared infrastructure.
- [ ] Scientific-specific dependencies are present in `venv` or `requirements.txt`.
- [ ] `git subtree pull` command executes without "no common ancestor" errors.
- [ ] All setup scripts pass the `py_compile` check.
