#!/bin/bash

# Email Intelligence Aider - JSON Data Recovery Script
# This script restores data/processed/email_data.json from a backup file.

set -euo pipefail

# Configuration
TARGET_FILE="data/processed/email_data.json"
BACKUP_DIR="${HOME}/email_intelligence_backups"
LOG_FILE="${HOME}/.email_intelligence_restore.log"

# Logging
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $*" | tee -a "$LOG_FILE"
}

# Show available backups
show_available_backups() {
    local backup_dir="$1"
    log "Available backups in: $backup_dir"

    if [[ ! -d "$backup_dir" ]]; then
        log "ERROR: Backup directory does not exist: $backup_dir"
        exit 1
    fi

    local backups=($(find "$backup_dir" -name "email_data_*.json.gz" -type f -printf '%T@ %p\n' | sort -nr | cut -d' ' -f2-))

    if [[ ${#backups[@]} -eq 0 ]]; then
        log "No backup files found in: $backup_dir"
        exit 1
    fi

    echo "Available backups (newest first):"
    echo "=================================="
    local i=1
    for backup in "${backups[@]}"; do
        local filename=$(basename "$backup")
        local size=$(du -h "$backup" | cut -f1)
        local mtime=$(stat -c '%y' "$backup" | cut -d'.' -f1)
        echo "$i) $filename (Size: $size, Created: $mtime)"
        ((i++))
    done
    echo ""
}

# Select backup file
select_backup() {
    local backup_dir="$1"
    local backups=($(find "$backup_dir" -name "email_data_*.json.gz" -type f -printf '%T@ %p\n' | sort -nr | cut -d' ' -f2-))

    if [[ ${#backups[@]} -eq 0 ]]; then
        log "No backup files available"
        exit 1
    fi

    # If only one backup, use it automatically
    if [[ ${#backups[@]} -eq 1 ]]; then
        echo "${backups[0]}"
        return
    fi

    # Otherwise, let user choose
    while true; do
        echo "Enter the number of the backup to restore (1-${#backups[@]}), or 'q' to quit:"
        read -r choice

        if [[ "$choice" == "q" ]]; then
            log "Restore cancelled by user"
            exit 0
        fi

        if [[ "$choice" =~ ^[0-9]+$ ]] && [[ "$choice" -ge 1 ]] && [[ "$choice" -le ${#backups[@]} ]]; then
            echo "${backups[$((choice-1))]}"
            return
        else
            echo "Invalid choice. Please enter a number between 1 and ${#backups[@]}."
        fi
    done
}

# Create backup of current file
backup_current_file() {
    local target_file="$1"

    if [[ -f "$target_file" ]]; then
        local backup_name="${target_file}.backup.$(date +%Y%m%d_%H%M%S)"
        log "Creating backup of current file: $backup_name"
        cp "$target_file" "$backup_name"
        echo "$backup_name"
    else
        log "No current file to backup: $target_file"
        echo ""
    fi
}

# Restore from backup with enhanced integrity verification
restore_from_backup() {
    local backup_file="$1"
    local target_file="$2"

    log "Restoring from backup: $backup_file"

    # Check for SHA256 checksum file
    local checksum_file="${backup_file}.sha256"
    local has_checksum=false
    if [[ -f "$checksum_file" ]]; then
        has_checksum=true
        log "Found SHA256 checksum file: $checksum_file"
    else
        log "WARNING: No SHA256 checksum file found for: $backup_file"
    fi

    # Verify backup integrity
    if ! gzip -t "$backup_file"; then
        log "ERROR: Backup file is corrupted: $backup_file"
        exit 1
    fi

    # Create target directory if it doesn't exist
    local target_dir=$(dirname "$target_file")
    mkdir -p "$target_dir"

    # Restore the file
    log "Decompressing backup to: $target_file"
    gzip -dc "$backup_file" > "$target_file"

    # Verify the restored file
    if [[ ! -f "$target_file" ]]; then
        log "ERROR: Failed to create target file: $target_file"
        exit 1
    fi

    # Verify SHA256 checksum if available
    if [[ "$has_checksum" == true ]]; then
        log "Verifying SHA256 checksum..."
        if sha256sum -c "$checksum_file" --quiet; then
            log "SHA256 checksum verification passed"
        else
            log "ERROR: SHA256 checksum verification failed for restored file"
            exit 1
        fi
    fi

    # Basic JSON validation
    if ! python3 -m json.tool "$target_file" > /dev/null 2>&1; then
        log "WARNING: Restored file does not appear to be valid JSON"
    else
        log "Restored file validated as proper JSON"
    fi

    local restored_size=$(du -h "$target_file" | cut -f1)
    log "Restoration completed successfully. File size: $restored_size"
}

# Verify restoration
verify_restoration() {
    local target_file="$1"
    local audit_script="scripts/audit_migration.py"

    log "Verifying restored data integrity"

    if [[ -f "$audit_script" ]]; then
        log "Running audit script to verify data integrity..."
        if python3 "$audit_script" 2>&1; then
            log "Audit completed successfully - data integrity verified"
        else
            log "WARNING: Audit script reported issues with restored data"
        fi
    else
        log "Audit script not found: $audit_script"
        log "Manual verification recommended"
    fi
}

# Interactive restore mode
interactive_restore() {
    log "Starting interactive restore process"

    show_available_backups "$BACKUP_DIR"

    local selected_backup=$(select_backup "$BACKUP_DIR")
    if [[ -z "$selected_backup" ]]; then
        exit 0
    fi

    log "Selected backup: $(basename "$selected_backup")"

    echo ""
    echo "WARNING: This will replace the current data file with the backup."
    echo "Current file: $TARGET_FILE"
    echo "Backup file: $(basename "$selected_backup")"
    echo ""
    read -p "Are you sure you want to proceed? (yes/no): " -r confirm

    if [[ "$confirm" != "yes" ]]; then
        log "Restore cancelled by user"
        exit 0
    fi

    # Backup current file
    local current_backup=$(backup_current_file "$TARGET_FILE")

    # Restore from backup
    restore_from_backup "$selected_backup" "$TARGET_FILE"

    # Verify restoration
    verify_restoration "$TARGET_FILE"

    echo ""
    echo "Restore completed successfully!"
    echo "Original file backed up as: $current_backup"
    echo "You may want to run the application to verify it works with the restored data."
}

# Automated restore mode (for scripts/cron)
automated_restore() {
    local backup_file="$1"

    if [[ ! -f "$backup_file" ]]; then
        log "ERROR: Specified backup file does not exist: $backup_file"
        exit 1
    fi

    log "Starting automated restore from: $backup_file"

    # Backup current file
    backup_current_file "$TARGET_FILE" > /dev/null

    # Restore from backup
    restore_from_backup "$backup_file" "$TARGET_FILE"

    # Verify restoration
    verify_restoration "$TARGET_FILE"
}

# Main execution
main() {
    log "Email Intelligence Aider data restoration process started"

    # Ensure we're in the project root
    if [[ ! -f "data/processed/email_data.json" ]] && [[ ! -f "data/processed/email_data.json" ]]; then
        # Try to find the file
        if [[ -f "email_data.json" ]]; then
            TARGET_FILE="email_data.json"
        else
            log "ERROR: Not in project root directory. Expected to find data/processed/email_data.json"
            exit 1
        fi
    fi

    # Check if backup file specified as argument (automated mode)
    if [[ $# -eq 1 ]]; then
        automated_restore "$1"
    else
        interactive_restore
    fi

    log "Restoration process completed"
}

# Show usage if requested
if [[ "${1:-}" == "--help" ]] || [[ "${1:-}" == "-h" ]]; then
    echo "Email Intelligence Aider - JSON Data Recovery Script"
    echo ""
    echo "Usage:"
    echo "  $0                    # Interactive mode - select backup interactively"
    echo "  $0 <backup_file>      # Automated mode - restore from specific backup file"
    echo "  $0 --help             # Show this help"
    echo ""
    echo "Examples:"
    echo "  $0"
    echo "  $0 ~/email_intelligence_backups/email_data_20251113_053758.json.gz"
    exit 0
fi

# Run main function
main "$@"