# Email Intelligence Aider - Data Recovery Procedure

This document outlines the procedures for recovering `data/processed/email_data.json` from backups in case of data loss or corruption.

## Overview

The recovery process uses automated scripts to safely restore data from compressed timestamped backups. The system includes safeguards to prevent accidental data loss during recovery operations.

## Recovery Script

### Location
`scripts/restore_json_data.sh`

### Usage

#### Interactive Mode (Recommended for manual recovery)
```bash
cd /path/to/email_intelligence_aider
./scripts/restore_json_data.sh
```

This mode will:
1. Display all available backups with timestamps and sizes
2. Allow you to select which backup to restore from
3. Create a backup of the current file before restoration
4. Restore the selected backup
5. Validate the restored data

#### Automated Mode (For scripts/cron jobs)
```bash
./scripts/restore_json_data.sh /path/to/backup/email_data_YYYYMMDD_HHMMSS.json.gz
```

This mode will automatically restore from the specified backup file.

## Recovery Steps

### Step 1: Assess the Situation
Before starting recovery, determine:
- Is the data file missing or corrupted?
- When was the last known good state?
- Are there recent backups available?

Check current status:
```bash
ls -la data/processed/email_data.json
ls -la ~/email_intelligence_backups/
```

### Step 2: Choose Recovery Method

#### Option A: Interactive Recovery (Safest)
```bash
cd /path/to/email_intelligence_aider
./scripts/restore_json_data.sh
```

Follow the prompts to select the appropriate backup.

#### Option B: Direct Restoration
If you know the exact backup file to use:
```bash
./scripts/restore_json_data.sh ~/email_intelligence_backups/email_data_20251113_053853.json.gz
```

### Step 3: Verify Recovery

After restoration, verify the data integrity:

1. **Check file integrity:**
   ```bash
   ls -la data/processed/email_data.json
   head -5 data/processed/email_data.json
   ```

2. **Validate JSON structure:**
   ```bash
   python3 -m json.tool data/processed/email_data.json > /dev/null && echo "JSON is valid"
   ```

3. **Test application functionality:**
   Start the application and verify it can read the restored data properly.

### Step 4: Clean Up (Optional)
The recovery script automatically creates backups of the original file before restoration. These are named with timestamps:
```
data/processed/email_data.json.backup.YYYYMMDD_HHMMSS
```

Remove old backup files if no longer needed:
```bash
ls -la data/processed/email_data.json.backup.*
rm data/processed/email_data.json.backup.YYYYMMDD_HHMMSS
```

## Safety Features

### Automatic Backup Creation
Before any restoration, the script creates a timestamped backup of the current file:
```
data/processed/email_data.json.backup.YYYYMMDD_HHMMSS
```

### Data Validation
- Verifies backup file integrity using `gzip -t`
- Validates restored JSON structure
- Runs audit script if available

### Confirmation Prompts
Interactive mode requires explicit confirmation before proceeding with restoration.

## Troubleshooting

### No Backups Available
If `ls ~/email_intelligence_backups/` shows no files:
- Check if backup script is running: `crontab -l | grep backup`
- Run backup manually: `./scripts/backup_json_data.sh`
- Check backup script logs: `tail ~/.email_intelligence_backup.log`

### Backup File Corrupted
If restoration fails with "Backup file is corrupted":
- Try a different backup file
- Check available backups: `ls -la ~/email_intelligence_backups/`
- Verify backup integrity: `gzip -t ~/email_intelligence_backups/filename.json.gz`

### Permission Issues
If you get permission errors:
```bash
chmod +x scripts/restore_json_data.sh
ls -la ~/email_intelligence_backups/
```

### Application Won't Start After Recovery
If the application fails to read restored data:
- Check JSON syntax: `python3 -c "import json; json.load(open('data/processed/email_data.json'))"`
- Compare with a known good backup
- Check application logs for specific error messages

## Emergency Recovery (Without Scripts)

If the recovery script is unavailable, manual recovery can be performed:

1. **Locate backup:**
   ```bash
   ls -la ~/email_intelligence_backups/
   ```

2. **Backup current file (if it exists):**
   ```bash
   cp data/processed/email_data.json data/processed/email_data.json.emergency_backup
   ```

3. **Restore from backup:**
   ```bash
   gzip -dc ~/email_intelligence_backups/email_data_YYYYMMDD_HHMMSS.json.gz > data/processed/email_data.json
   ```

4. **Verify:**
   ```bash
   python3 -m json.tool data/processed/email_data.json > /dev/null && echo "Recovery successful"
   ```

## Prevention

To minimize recovery needs:
- Ensure backup script runs regularly via cron
- Monitor backup logs: `tail ~/.email_intelligence_backup.log`
- Test recovery procedures periodically
- Keep multiple backup locations if possible

## Related Documentation

- [Backup Procedure](scripts/README_backup.md) - Automated backup system documentation
- [Migration Audit](scripts/audit_migration.py) - Data integrity verification script
- [System Administration Guide](../../docs/) - General system maintenance procedures

---

**Last Updated:** November 13, 2025
**Version:** 1.0