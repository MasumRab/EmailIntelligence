# Email Intelligence Aider - Backup Procedure

This document describes the automated backup system for the Email Intelligence Aider JSON data store.

## Overview

The backup system automatically creates compressed backups of `data/processed/email_data.json` with timestamped filenames and implements a retention policy to manage backup storage.

## Backup Script

### Location
`scripts/backup_json_data.sh`

### Features
- Compresses JSON data using gzip
- Creates timestamped backup files: `email_data_YYYYMMDD_HHMMSS.json.gz`
- Implements retention policy: 7 daily, 4 weekly, 12 monthly backups
- Logs all operations to `~/.email_intelligence_backup.log`
- Verifies backup integrity after creation

### Backup Location
Backups are stored in: `~/email_intelligence_backups/`

## Scheduling Options

### Option 1: Cron Job (Recommended)

The script is configured to run daily at 2 AM via cron:

```bash
# View current cron jobs
crontab -l

# The backup job is scheduled as:
0 2 * * * /home/masum/github/EmailIntelligenceAider/scripts/backup_json_data.sh
```

### Option 2: Systemd Timer (Alternative)

Systemd service and timer files are provided for systems that prefer systemd:

- `scripts/email_backup.service` - Defines the backup service
- `scripts/email_backup.timer` - Schedules daily execution

To install the systemd timer:

```bash
# Copy service files to systemd directory
sudo cp scripts/email_backup.service /etc/systemd/system/
sudo cp scripts/email_backup.timer /etc/systemd/system/

# Reload systemd and enable timer
sudo systemctl daemon-reload
sudo systemctl enable email_backup.timer
sudo systemctl start email_backup.timer

# Check timer status
sudo systemctl list-timers | grep email_backup
```

## Manual Testing

To test the backup script manually:

```bash
cd /home/masum/github/EmailIntelligenceAider
./scripts/backup_json_data.sh
```

Verify the backup was created:
```bash
ls -la ~/email_intelligence_backups/
```

Test backup integrity:
```bash
gunzip -c ~/email_intelligence_backups/email_data_*.json.gz | head -5
```

## Retention Policy

The script maintains the following retention policy:

- **Daily backups**: Keep last 7 days
- **Weekly backups**: Keep one per week for last 4 weeks
- **Monthly backups**: Keep one per month for last 12 months

Old backups are automatically deleted when the script runs.

## Log Files

Backup operations are logged to: `~/.email_intelligence_backup.log`

View recent logs:
```bash
tail -20 ~/.email_intelligence_backup.log
```

## Recovery

To restore from a backup:

1. Identify the backup file to restore from:
   ```bash
   ls -la ~/email_intelligence_backups/
   ```

2. Decompress and restore:
   ```bash
   gunzip -c ~/email_intelligence_backups/email_data_YYYYMMDD_HHMMSS.json.gz > data/processed/email_data.json
   ```

3. Verify the restored data:
   ```bash
   python scripts/audit_migration.py  # Run the audit script to verify integrity
   ```

## Configuration

To modify backup settings, edit the variables at the top of `scripts/backup_json_data.sh`:

```bash
SOURCE_FILE="data/processed/email_data.json"
BACKUP_DIR="${HOME}/email_intelligence_backups"
DAILY_RETENTION=7
WEEKLY_RETENTION=28  # 4 weeks
MONTHLY_RETENTION=365  # 12 months
```

## Troubleshooting

### Permission Issues
If the script cannot write to the backup directory, ensure the user has write permissions:
```bash
mkdir -p ~/email_intelligence_backups
chmod 755 ~/email_intelligence_backups
```

### Cron Job Not Running
Check cron logs:
```bash
grep CRON /var/log/syslog
```

Verify the script path in crontab is absolute and executable.

### Large Backup Files
Monitor backup sizes:
```bash
du -sh ~/email_intelligence_backups/*
```

If backups are too large, consider adjusting the retention policy or implementing incremental backups.

## Security Notes

- Backup files contain sensitive email data
- Ensure backup directory has appropriate permissions (readable only by owner)
- Consider encrypting backups for additional security
- Regularly audit backup integrity and recovery procedures