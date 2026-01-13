# Branch Merge Task: taskmaster (EmailIntelligenceQwen)

**Repository:** /home/masum/github/EmailIntelligenceQwen
**Branch:** taskmaster
**Status:** behind origin by 21
**Priority:** MEDIUM
**Guide Version:** 1.0

---

## Current State

```
Local:  taskmaster @ ffb78701
Remote: origin/taskmaster @ 4258e068
Ahead:  0 commits
Behind: 21 commits
```

## Merge Strategy: Rebase

```bash
cd /home/masum/github/EmailIntelligenceQwen

git fetch origin
git checkout taskmaster
git rebase origin/taskmaster

git push origin taskmaster --force-with-lease
```

## Testing

```bash
# Verify .taskmaster integrity
ls -la .taskmaster/

# Check task file syntax
python -c "
import yaml
import os

for root, dirs, files in os.walk('.taskmaster'):
    for f in files:
        if f.endswith('.yml') or f.endswith('.yaml'):
            with open(os.path.join(root, f)) as file:
                try:
                    yaml.safe_load(file)
                    print(f'{f}: Valid')
                except Exception as e:
                    print(f'{f}: ERROR - {e}')
"
```

## Rollback

```bash
git reset --hard origin/taskmaster
```

## Time Estimate

10-15 minutes

---

*Task created: 2025-01-13*


---

## Enhanced Process Guide (v2.0)

This section provides access to advanced merge tools and processes for preserving changes and handling structural differences.

### Phase 2b: Intelligent Change Integration

**Purpose:** Systematically preserve changes from both branches where possible.

**Step 1: Analyze Change Overlap**

```bash
cd /home/masum/github/home

# Analyze overlap for key files
python3 /home/masum/github/home/scripts/intelligent_merge_analyzer.py \
  src/core/security.py \
  origin/taskmaster..HEAD \
  origin/taskmaster~10..origin/taskmaster

# Analyze other critical files
python3 /home/masum/github/home/scripts/intelligent_merge_analyzer.py \
  src/core/main.py \
  origin/taskmaster..HEAD \
  origin/taskmaster~10..origin/taskmaster
```

**Interpretation:**
- **< 20% overlap:** Safe to auto-merge
- **20-50% overlap:** Use intelligent merger
- **> 50% overlap:** Manual resolution required

**Step 2: Intelligent Combination (if overlap 20-50%)**

```bash
# For files with moderate overlap
python3 /home/masum/github/home/scripts/intelligent_merger.py \
  src/core/main.py \
  HEAD \
  origin/taskmaster

# Review and resolve conflicts in .merged file
${EDITOR:-vi} src/core/main.py.merged

# If acceptable, replace original
mv src/core/main.py.merged src/core/main.py
git add src/core/main.py
```

### Phase 2c: Import & Path Sweep

**Purpose:** Detect and fix structural changes between branches.

**Step 1: Detect Path Changes**

```bash
# Run path change detector
python3 /home/masum/github/home/scripts/path_change_detector.py \
  HEAD \
  origin/taskmaster

# View report
cat PATH_CHANGE_REPORT.md
```

**Step 2: Audit Import Statements**

```bash
# Run comprehensive import audit
python3 /home/masum/github/home/scripts/import_audit.py /home/masum/github/home

# View issues
cat IMPORT_AUDIT_REPORT.md

# Auto-fix simple issues
python3 /home/masum/github/home/scripts/import_audit.py /home/masum/github/home --auto-fix
```

**Step 3: Update References (if path changes detected)**

```bash
# Update references for detected path changes
python3 /home/masum/github/home/scripts/update_references.py \
  "OLD_PATTERN" \
  "NEW_PATTERN" \
  "src/**/*.py"
```

### Master Audit (Recommended)

```bash
# Run all audits together
cd /home/masum/github/home
./scripts/master_audit.sh /home/masum/github/home taskmaster-merge-audit-$(date +%Y%m%d)

# Review all reports
cat taskmaster-merge-audit-$(date +%Y%m%d)_summary.md
cat taskmaster-merge-audit-$(date +%Y%m%d)_path_changes.md
cat taskmaster-merge-audit-$(date +%Y%m%d)_import_audit.md
```

### Branch-Specific Considerations

**taskmaster branch specific:**
- Task management branch
- May have task definition changes
- Verify .taskmaster/ directory integrity
- Check task file syntax after merge

### Updated Time Estimate (v2.0)

- Backup: 2 minutes
- **Master audit (new): 5-10 minutes**
- **Path/import analysis (new): 5-10 minutes**
- Fetch/Reset/Merge: 10-30 minutes (depends on conflicts)
- **Intelligent merge if needed (new): 10-20 minutes**
- Testing: 10 minutes
- Push: 1 minute

**Total: 45-80 minutes** (with new enhanced process)
**With major conflicts: 1.5-3 hours**

### Updated Decision Log

| Date | Decision | Rationale | Owner |
|------|----------|-----------|-------|
| 2025-01-14 | Added enhanced process guide | Include intelligent change integration and import/path sweep tools | Git Workflow |
| | | | |

---

*Task created: 2025-01-13*
*Last updated: 2025-01-14*
*Enhanced with Phase 2b and 2c processes*
