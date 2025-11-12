#!/bin/bash

# Email Intelligence Aider - JSON Data Store Backup Script
# This script creates compressed backups of data/processed/email_data.json
# with timestamped filenames and implements a retention policy.

set -euo pipefail

# Configuration
SOURCE_FILE="data/processed/email_data.json"
BACKUP_DIR="${HOME}/email_intelligence_backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
GIT_COMMIT=$(git rev-parse --short HEAD 2>/dev/null || echo "nogit")
BACKUP_FILENAME="email_data_${TIMESTAMP}_${GIT_COMMIT}.json.gz"

# Retention policy (in days)
DAILY_RETENTION=7
WEEKLY_RETENTION=28  # 4 weeks
MONTHLY_RETENTION=365  # 12 months

# Enhanced retention for recent backups (hours)
HOURLY_RETENTION_HOURS=48

# Logging
LOG_FILE="${HOME}/.email_intelligence_backup.log"
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $*" | tee -a "$LOG_FILE"
}

# Ensure backup directory exists
ensure_backup_dir() {
    if [[ ! -d "$BACKUP_DIR" ]]; then
        log "Creating backup directory: $BACKUP_DIR"
        mkdir -p "$BACKUP_DIR"
    fi
}

# Create backup with enhanced integrity checks
create_backup() {
    local source_path="$1"
    local backup_path="$2"

    if [[ ! -f "$source_path" ]]; then
        log "ERROR: Source file does not exist: $source_path"
        exit 1
    fi

    log "Creating backup: $backup_path"

    # Calculate SHA256 checksum of original file
    local checksum_file="${backup_path}.sha256"
    sha256sum "$source_path" > "$checksum_file"

    # Create compressed backup
    gzip -c "$source_path" > "$backup_path"

    # Verify backup integrity
    if gzip -t "$backup_path"; then
        log "Backup created successfully: $backup_path"
        log "Backup size: $(du -h "$backup_path" | cut -f1)"
        log "SHA256 checksum saved: $checksum_file"
    else
        log "ERROR: Backup verification failed for: $backup_path"
        rm -f "$backup_path" "$checksum_file"
        exit 1
    fi
}

# Clean up old backups based on enhanced retention policy
cleanup_old_backups() {
    local backup_dir="$1"
    log "Cleaning up old backups in: $backup_dir"

    # Get all backup files sorted by modification time (newest first)
    local all_backups=($(find "$backup_dir" -name "email_data_*.json.gz" -type f -printf '%T@ %p\n' | sort -nr | cut -d' ' -f2-))

    if [[ ${#all_backups[@]} -eq 0 ]]; then
        log "No backup files found for cleanup"
        return
    fi

    # Keep all backups from the last HOURLY_RETENTION_HOURS hours
    local hourly_cutoff=$(date -d "$HOURLY_RETENTION_HOURS hours ago" +%s)
    local hourly_backups=()

    # Keep all backups from the last DAILY_RETENTION days
    local daily_cutoff=$(date -d "$DAILY_RETENTION days ago" +%s)
    local daily_backups=()

    # Keep one backup per week for the last WEEKLY_RETENTION days
    local weekly_cutoff=$(date -d "$WEEKLY_RETENTION days ago" +%s)
    local weekly_backups=()

    # Keep one backup per month for the last MONTHLY_RETENTION days
    local monthly_cutoff=$(date -d "$MONTHLY_RETENTION days ago" +%s)
    local monthly_backups=()

    # Process each backup file
    for backup in "${all_backups[@]}"; do
        local mtime=$(stat -c %Y "$backup")
        local filename=$(basename "$backup")

        # Always keep hourly backups within retention period
        if [[ $mtime -gt $hourly_cutoff ]]; then
            hourly_backups+=("$backup")
            continue
        fi

        # Always keep daily backups within retention period
        if [[ $mtime -gt $daily_cutoff ]]; then
            daily_backups+=("$backup")
            continue
        fi

        # For weekly backups: keep one per week
        if [[ $mtime -gt $weekly_cutoff ]]; then
            local week_num=$(date -d "@$mtime" +%Y%U)
            local found_weekly=false
            for wb in "${weekly_backups[@]}"; do
                if [[ "$(date -d "@$(stat -c %Y "$wb")" +%Y%U)" == "$week_num" ]]; then
                    found_weekly=true
                    break
                fi
            done
            if [[ $found_weekly == false ]]; then
                weekly_backups+=("$backup")
                continue
            fi
        fi

        # For monthly backups: keep one per month
        if [[ $mtime -gt $monthly_cutoff ]]; then
            local month_num=$(date -d "@$mtime" +%Y%m)
            local found_monthly=false
            for mb in "${monthly_backups[@]}"; do
                if [[ "$(date -d "@$(stat -c %Y "$mb")" +%Y%m)" == "$month_num" ]]; then
                    found_monthly=true
                    break
                fi
            done
            if [[ $found_monthly == false ]]; then
                monthly_backups+=("$backup")
                continue
            fi
        fi

        # Delete backups that don't fall into retention categories
        log "Deleting old backup: $filename and checksum file"
        rm -f "$backup" "${backup}.sha256"
    done

    log "Retention summary:"
    log "  Hourly backups kept: ${#hourly_backups[@]}"
    log "  Daily backups kept: ${#daily_backups[@]}"
    log "  Weekly backups kept: ${#weekly_backups[@]}"
    log "  Monthly backups kept: ${#monthly_backups[@]}"
    log "  Total backups kept: $((${#hourly_backups[@]} + ${#daily_backups[@]} + ${#weekly_backups[@]} + ${#monthly_backups[@]}))"
}

# Main execution
main() {
    log "Starting Email Intelligence Aider backup process"

    # Ensure we're in the project root
    if [[ ! -f "$SOURCE_FILE" ]]; then
        log "ERROR: Not in project root directory. Expected to find: $SOURCE_FILE"
        exit 1
    fi

    ensure_backup_dir

    local backup_path="$BACKUP_DIR/$BACKUP_FILENAME"
    create_backup "$SOURCE_FILE" "$backup_path"

    cleanup_old_backups "$BACKUP_DIR"

    log "Backup process completed successfully"
}

# Run main function
main "$@"