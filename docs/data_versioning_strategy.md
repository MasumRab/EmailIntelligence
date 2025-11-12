# JSON Data File Versioning Strategy

## Overview

This document outlines the versioning strategy for `data/processed/email_data.json`, the primary JSON data store for the Email Intelligence Aider application. After evaluating multiple versioning approaches, we have implemented an enhanced backup and integrity verification system that leverages the existing Git-based workflow while providing robust data protection.

## Current Data Characteristics

- **File Size**: ~1.7KB (small dataset)
- **Content**: Array of email records with metadata (sentiment, categories, timestamps)
- **Update Frequency**: Infrequent but critical when changed
- **Git Tracking**: Currently tracked directly in Git repository

## Evaluation of Versioning Options

### 1. Direct Git Tracking (Chosen Approach)
**Status**: ✅ **Implemented and Recommended**

**Rationale**:
- Optimal for small files (< 10MB)
- Provides complete change history with `git log`
- Enables easy rollback with `git checkout`
- Integrates seamlessly with development workflow
- No additional complexity or tools required

**Implementation**:
- File remains tracked in Git
- Enhanced commit practices recommended for data changes
- Git commit hash included in backup metadata

### 2. Git Large File Storage (Git LFS)
**Status**: ❌ **Not Recommended**

**Rationale**:
- Designed for large binary files (>10MB)
- Current file size (1.7KB) makes it unnecessary overhead
- Would complicate the repository structure
- Better suited for future growth scenarios

**When to Consider**: If `email_data.json` grows to >100MB

### 3. Document Store/Database Solutions
**Status**: ❌ **Not Recommended**

**Rationale**:
- Significant architectural change required
- Overkill for current data volume and access patterns
- Would require migration effort and maintenance overhead
- Better suited for applications with complex querying needs

**When to Consider**: If data complexity or access patterns require database features

### 4. Enhanced Backup Retention (Implemented Enhancement)
**Status**: ✅ **Implemented**

**Rationale**:
- Provides point-in-time recovery beyond Git history
- Protects against accidental data loss
- Enables recovery from corrupted states
- Complements Git versioning

## Implemented Versioning Strategy

### Multi-Tier Backup Retention Policy

```
Hourly: 48 hours (recent changes protection)
Daily:  7 days   (recent history)
Weekly: 4 weeks  (medium-term history)
Monthly: 12 months (long-term archive)
```

### Enhanced Integrity Verification

- **SHA256 Checksums**: Cryptographic verification of backup integrity
- **Gzip Compression**: Space-efficient storage with integrity checking
- **JSON Validation**: Ensures restored data is valid JSON
- **Git Integration**: Backup filenames include Git commit hash

### Backup File Naming Convention

```
email_data_YYYYMMDD_HHMMSS_GITCOMMITHASH.json.gz
email_data_YYYYMMDD_HHMMSS_GITCOMMITHASH.json.gz.sha256
```

Example:
```
email_data_20251113_054200_a1b2c3d.json.gz
email_data_20251113_054200_a1b2c3d.json.gz.sha256
```

## Usage Instructions

### Creating Backups

```bash
# Manual backup
./scripts/backup_json_data.sh

# Automated (via cron/systemd timer)
# Runs daily at 2:00 AM
```

### Restoring from Backup

```bash
# Interactive restoration
./scripts/restore_json_data.sh

# Automated restoration from specific backup
./scripts/restore_json_data.sh /path/to/backup/email_data_20251113_054200_a1b2c3d.json.gz
```

### Verifying Backup Integrity

```bash
# Check gzip integrity
gzip -t ~/email_intelligence_backups/email_data_*.json.gz

# Verify SHA256 checksum (if available)
cd ~/email_intelligence_backups
sha256sum -c email_data_20251113_054200_a1b2c3d.json.gz.sha256
```

## Git Integration Best Practices

### Commit Data Changes Properly

```bash
# When email_data.json is modified
git add data/processed/email_data.json
git commit -m "feat: update email data - add category filtering

- Added sentiment analysis metadata
- Updated category assignments
- Verified data integrity with audit script"
```

### Data Change Workflow

1. **Backup before changes**:
   ```bash
   ./scripts/backup_json_data.sh
   ```

2. **Make data changes** (via application or scripts)

3. **Validate changes**:
   ```bash
   python3 -m json.tool data/processed/email_data.json
   python3 scripts/audit_migration.py
   ```

4. **Commit with descriptive message**:
   ```bash
   git add data/processed/email_data.json
   git commit -m "feat: [description of data changes]"
   ```

## Monitoring and Maintenance

### Backup Health Checks

```bash
# Check backup directory
ls -la ~/email_intelligence_backups/

# Verify recent backups exist
find ~/email_intelligence_backups/ -name "email_data_*.json.gz" -mtime -1

# Check log for issues
tail -20 ~/.email_intelligence_backup.log
```

### Storage Management

- Monitor backup directory size: `du -sh ~/email_intelligence_backups/`
- Automatic cleanup runs with each backup
- Retention policy prevents unlimited growth

## Future Considerations

### Scaling Triggers

- **File Size > 10MB**: Consider Git LFS evaluation
- **Complex Queries**: Evaluate document store migration
- **Multi-user Editing**: Consider collaborative editing solutions
- **High Availability**: Implement off-site/cloud replication

### Enhancement Opportunities

- **Automated Testing**: Regular restore testing in staging
- **Cloud Integration**: AWS S3/Glacier for long-term archival
- **Change Tracking**: Detailed audit logs of data modifications
- **Version Pinning**: Tag specific data versions for releases

## Integration Points

### Related Systems

- **Audit Migration Script**: `scripts/audit_migration.py`
- **Recovery Procedures**: `docs/recovery_procedure.md`
- **Backup Documentation**: `scripts/README_backup.md`

### Dependencies

- Git (for commit hash integration)
- gzip (compression and integrity checking)
- sha256sum (cryptographic verification)
- Python 3 (JSON validation)

## Conclusion

The implemented strategy provides robust versioning for `email_data.json` through:

1. **Git-based versioning** for development workflow integration
2. **Enhanced backup system** with multi-tier retention
3. **Cryptographic integrity verification** for data protection
4. **Automated maintenance** to prevent storage bloat

This approach balances simplicity, reliability, and scalability while avoiding unnecessary complexity for the current data characteristics.</content>
</xai:function_call"> 

<xai:function_call name="task-master-ai_update_subtask">
<parameter name="id">15.5