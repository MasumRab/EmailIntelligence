# Progress File Compression System

**Created:** 2026-01-04  
**Purpose:** Robust compression for progress tracking files without data loss

---

## Overview

This compression system is designed specifically for progress tracking files in the Branch Alignment Project. It provides:

- **Lossless compression** - All data is preserved with SHA-256 verification
- **Selective compression** - Essential files can be preserved separately
- **Integrity verification** - Checksums ensure no data corruption
- **Flexible formats** - Support for gzip, bzip2, and xz compression

---

## Compression Tools

### 1. Bash Script (Recommended for Quick Use)

**Location:** `scripts/compress_progress.sh`

**Usage:**
```bash
# Show help
bash scripts/compress_progress.sh --help

# Compress all progress files
bash scripts/compress_progress.sh compress --source . --backup backups/

# Compress only essential files
bash scripts/compress_progress.sh compress --essential

# List available archives
bash scripts/compress_progress.sh list

# Verify archive integrity
bash scripts/compress_progress.sh verify progress_20260104_120000.tar.xz

# Decompress an archive
bash scripts/compress_progress.sh decompress progress_20260104_120000.tar.xz

# Show current status
bash scripts/compress_progress.sh status
```

### 2. Python Script (Advanced Features)

**Location:** `scripts/compress_progress.py`

**Usage:**
```bash
# Compress with custom settings
python scripts/compress_progress.py --compress --source . --destination backups/ --format xz

# Decompress with verification
python scripts/compress_progress.py --decompress --archive progress.tar.xz --restore-to ./restore/

# List archive contents
python scripts/compress_progress.py --list --archive progress.tar.xz

# Verify integrity
python scripts/compress_progress.py --verify --archive progress.tar.xz

# Query all archives
python scripts/compress_progress.py --stats
```

---

## Compression Format Comparison

| Format | Compression Ratio | Speed | Use Case |
|--------|------------------|-------|----------|
| **gzip (.gz)** | Good (60-70%) | Fast | Quick backups, frequent access |
| **bzip2 (.bz2)** | Better (65-75%) | Medium | Balanced size/speed |
| **xz (.xz)** | Best (70-80%) | Slow | Long-term storage, maximum compression |

**Recommendation:** Use `xz` for maximum compression when speed is not critical.

---

## File Selection Strategy

### Files Always Included (Essential)

```python
ESSENTIAL_FILES = {
    'PROJECT_REFERENCE.md',
    'ENHANCED_VALIDATION_PLAN.md',
    'LOGGING_SYSTEM_PLAN.md',
    'LOGGING_GUIDE.md',
    'CLEAN_TASK_INDEX.md',
    'README.md',
    'AGENTS.md',
    'CLAUDE.md',
}
```

### Files Selected by Extension

| Extension | Compression Level | Priority |
|-----------|------------------|----------|
| `.json` | 6 (Moderate) | High |
| `.md` | 3 (Light) | Medium |
| `.txt` | 6 (Moderate) | Medium |
| `.log` | 9 (Maximum) | Low |
| `.py` | 6 (Moderate) | Low |
| `.sh` | 3 (Light) | Low |

### Files Selected by Name

Files containing these keywords are automatically included:
- `progress`, `tracking`, `status`, `summary`
- `index`, `reference`, `plan`, `guide`
- `task`, `logging`, `findings`

---

## Compression Workflow

### Step 1: Before Major Changes

```bash
# Create backup of current state
bash scripts/compress_progress.sh compress --source . --backup backups/
```

**Output:**
```
[INFO] Compressing progress files...
[INFO] Source: .
[INFO] Destination: backups/
[INFO] Format: xz
[INFO] Creating archive: backups/progress_20260104_120000.tar.xz
[INFO] Compression complete!
[INFO]   Files: 54
[INFO]   Original: 2.5 MB
[INFO]   Compressed: 0.8 MB
[INFO]   Ratio: 68.0%
```

### Step 2: During Development

```bash
# Compress essential files only (faster)
bash scripts/compress_progress.sh compress --essential --format xz
```

### Step 3: After Major Milestone

```bash
# Full compression with verification
python scripts/compress_progress.py --compress --source . --destination backups/ --format xz
python scripts/compress_progress.py --verify --archive backups/progress_20260104_120000.tar.xz
```

### Step 4: Restore When Needed

```bash
# Decompress specific archive
bash scripts/compress_progress.sh decompress backups/progress_20260104_120000.tar.xz

# Or with Python (more control)
python scripts/compress_progress.py --decompress \
    --archive backups/progress_20260104_120000.tar.xz \
    --restore-to ./restore/
```

---

## Archive Structure

Each archive contains:

```
progress_20260104_120000.tar.xz/
├── manifest.json          # Metadata and checksums
├── PROJECT_REFERENCE.md   # Progress reference
├── ENHANCED_VALIDATION_PLAN.md
├── LOGGING_SYSTEM_PLAN.md
├── LOGGING_GUIDE.md
├── CLEAN_TASK_INDEX.md
├── ... (other selected files)
└── *.md, *.json, *.txt   # Progress tracking files
```

### Manifest Format

```json
{
  "created": "2026-01-04T12:00:00+00:00",
  "source": ".",
  "files": {
    "PROJECT_REFERENCE.md": {
      "size": 17614,
      "mtime": "2026-01-04T12:00:00+00:00",
      "sha256": "abc123..."
    }
  },
  "totals": {
    "file_count": 54,
    "original_size": 2621440,
    "compressed_size": 840000
  }
}
```

---

## Verification Process

### Automated Verification

1. **During compression:**
   - Calculate SHA-256 hash for each file
   - Store hashes in manifest

2. **During decompression:**
   - Extract files
   - Recalculate SHA-256 hash
   - Compare with manifest

3. **Manual verification:**
   ```bash
   # Verify archive integrity
   bash scripts/compress_progress.sh verify progress_20260104_120000.tar.xz
   
   # Or with Python
   python scripts/compress_progress.py --verify --archive progress.tar.xz
   ```

---

## Best Practices

### 1. Before Major Changes

```bash
# Always backup before making changes
bash scripts/compress_progress.sh compress --source . --backup backups/
```

### 2. After Milestones

```bash
# Create milestone snapshots
python scripts/compress_progress.py \
    --compress \
    --source . \
    --destination backups/milestones/ \
    --format xz
```

### 3. Regular Maintenance

```bash
# Check archive status
bash scripts/compress_progress.sh status

# Verify oldest archives
bash scripts/compress_progress.sh verify backups/progress_20260101_000000.tar.xz
```

### 4. Cleanup Old Archives

```bash
# List archives by date
ls -la backups/progress_*.tar.xz | head -10

# Remove old archives (keep last 5)
ls -t backups/progress_*.tar.xz | tail -n +6 | xargs rm -f

# Remove associated manifests
ls -t backups/progress_*.tar.xz.manifest.json | tail -n +6 | xargs rm -f
```

---

## Quick Reference Commands

```bash
# Quick backup
bash scripts/compress_progress.sh compress --essential

# Full backup
bash scripts/compress_progress.sh compress --format xz

# Check status
bash scripts/compress_progress.sh status

# List archives
bash scripts/compress_progress.sh list

# Verify latest archive
bash scripts/compress_progress.sh verify $(ls -t backups/progress_*.tar.xz | head -1)

# Decompress
bash scripts/compress_progress.sh decompress backups/progress_20260104_120000.tar.xz
```

---

## Troubleshooting

### Issue: "Archive not found"

```bash
# Check archive location
ls -la backups/

# List available archives
bash scripts/compress_progress.sh list
```

### Issue: "Checksum mismatch"

```bash
# Re-verify archive
bash scripts/compress_progress.sh verify <archive_name>

# If verification fails, decompress manually
mkdir -p restore
tar -xf backups/<archive_name> -C restore/
```

### Issue: "Permission denied"

```bash
# Make scripts executable
chmod +x scripts/compress_progress.sh
chmod +x scripts/compress_progress.py
```

---

## File Locations

| File | Location |
|------|----------|
| Bash script | `/home/masum/github/PR/.taskmaster/scripts/compress_progress.sh` |
| Python script | `/home/masum/github/PR/.taskmaster/scripts/compress_progress.py` |
| Backups | `/home/masum/github/PR/.taskmaster/backups/` |
| This guide | `/home/masum/github/PR/.taskmaster/COMPRESSION_GUIDE.md` |

---

**End of Compression Guide**
