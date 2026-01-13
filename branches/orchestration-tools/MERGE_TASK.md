# Branch Merge Task: orchestration-tools (EmailIntelligenceQwen)

**Repository:** /home/masum/github/EmailIntelligenceQwen
**Branch:** orchestration-tools
**Status:** behind origin by 3
**Priority:** LOW
**Guide Version:** 1.0

---

## Current State

```
Local:  orchestration-tools @ fbe73039
Remote: origin/orchestration-tools @ c5243dd2
Ahead:  0 commits
Behind: 3 commits
```

## Merge Strategy: Simple Rebase

```bash
cd /home/masum/github/EmailIntelligenceQwen

git fetch origin
git checkout orchestration-tools
git rebase origin/orchestration-tools

git push origin orchestration-tools --force-with-lease
```

## Testing

```bash
cd setup
python -m pytest tests/ -v --tb=short 2>&1 | head -20
```

## Rollback

```bash
git reset --hard origin/orchestration-tools
```

## Time Estimate

5-10 minutes

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
  origin/orchestration-tools..HEAD \
  origin/orchestration-tools~10..origin/orchestration-tools

# Analyze other critical files
python3 /home/masum/github/home/scripts/intelligent_merge_analyzer.py \
  src/core/main.py \
  origin/orchestration-tools..HEAD \
  origin/orchestration-tools~10..origin/orchestration-tools
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
  origin/orchestration-tools

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
  origin/orchestration-tools

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
./scripts/master_audit.sh /home/masum/github/home orchestration-tools-merge-audit-$(date +%Y%m%d)

# Review all reports
cat orchestration-tools-merge-audit-$(date +%Y%m%d)_summary.md
cat orchestration-tools-merge-audit-$(date +%Y%m%d)_path_changes.md
cat orchestration-tools-merge-audit-$(date +%Y%m%d)_import_audit.md
```

### Branch-Specific Considerations

**orchestration-tools branch specific:**
- ✅ Infrastructure/hooks branch
- Minimal changes
- Focus on hooks and infrastructure
- Verify orchestration works after merge

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
