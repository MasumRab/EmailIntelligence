#!/bin/bash

# Email Intelligence Platform - Backup and Recovery Script
# Handles automated backups and disaster recovery procedures

set -e

# Configuration
BACKUP_ROOT="./backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_NAME="email_intelligence_$TIMESTAMP"
BACKUP_DIR="$BACKUP_ROOT/$BACKUP_NAME"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

# Create backup
create_backup() {
    log_info "Starting backup: $BACKUP_NAME"

    # Create backup directory
    mkdir -p "$BACKUP_DIR"

    # Backup database
    if [[ -f "./data/production.db" ]]; then
        log_info "Backing up database..."
        cp "./data/production.db" "$BACKUP_DIR/database.db"
        log_success "Database backup completed"
    else
        log_warning "Database file not found, skipping database backup"
    fi

    # Backup application data
    if [[ -d "./data" ]]; then
        log_info "Backing up application data..."
        cp -r "./data" "$BACKUP_DIR/app_data"
        log_success "Application data backup completed"
    fi

    # Backup logs
    if [[ -d "./logs" ]]; then
        log_info "Backing up logs..."
        cp -r "./logs" "$BACKUP_DIR/logs"
        log_success "Logs backup completed"
    fi

    # Backup monitoring data
    if [[ -d "./monitoring/grafana/data" ]]; then
        log_info "Backing up Grafana data..."
        cp -r "./monitoring/grafana/data" "$BACKUP_DIR/grafana_data"
        log_success "Grafana data backup completed"
    fi

    # Create backup manifest
    cat > "$BACKUP_DIR/manifest.txt" << EOF
Email Intelligence Platform Backup
==================================

Backup Name: $BACKUP_NAME
Created: $(date)
Version: $(git rev-parse HEAD 2>/dev/null || echo "unknown")

Contents:
$(ls -la "$BACKUP_DIR")

System Information:
$(uname -a)

Docker Version:
$(docker --version 2>/dev/null || echo "Docker not available")

Docker Compose Version:
$(docker-compose --version 2>/dev/null || echo "Docker Compose not available")
EOF

    # Create compressed archive
    log_info "Creating compressed archive..."
    cd "$BACKUP_ROOT"
    tar -czf "${BACKUP_NAME}.tar.gz" "$BACKUP_NAME"
    cd - > /dev/null

    # Calculate backup size
    BACKUP_SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)
    ARCHIVE_SIZE=$(du -sh "$BACKUP_ROOT/${BACKUP_NAME}.tar.gz" | cut -f1)

    log_success "Backup completed successfully"
    log_info "Backup location: $BACKUP_ROOT/${BACKUP_NAME}.tar.gz"
    log_info "Uncompressed size: $BACKUP_SIZE"
    log_info "Compressed size: $ARCHIVE_SIZE"

    # Cleanup uncompressed backup
    rm -rf "$BACKUP_DIR"
}

# Restore from backup
restore_backup() {
    local backup_file="$1"

    if [[ -z "$backup_file" ]]; then
        log_error "Please specify a backup file to restore from"
        echo "Usage: $0 restore <backup_file.tar.gz>"
        exit 1
    fi

    if [[ ! -f "$backup_file" ]]; then
        log_error "Backup file not found: $backup_file"
        exit 1
    fi

    log_info "Starting restore from: $backup_file"

    # Create temporary directory for extraction
    local temp_dir=$(mktemp -d)
    trap "rm -rf $temp_dir" EXIT

    # Extract backup
    log_info "Extracting backup archive..."
    tar -xzf "$backup_file" -C "$temp_dir"

    # Find backup directory
    local backup_dir=$(find "$temp_dir" -mindepth 1 -maxdepth 1 -type d | head -1)

    if [[ -z "$backup_dir" ]]; then
        log_error "Invalid backup archive structure"
        exit 1
    fi

    log_info "Restoring from: $(basename "$backup_dir")"

    # Stop services before restore
    log_info "Stopping services..."
    docker-compose -f docker-compose.prod.yml down 2>/dev/null || true

    # Restore database
    if [[ -f "$backup_dir/database.db" ]]; then
        log_info "Restoring database..."
        mkdir -p "./data"
        cp "$backup_dir/database.db" "./data/production.db"
        log_success "Database restored"
    fi

    # Restore application data
    if [[ -d "$backup_dir/app_data" ]]; then
        log_info "Restoring application data..."
        cp -r "$backup_dir/app_data"/* "./data/" 2>/dev/null || true
        log_success "Application data restored"
    fi

    # Restore logs
    if [[ -d "$backup_dir/logs" ]]; then
        log_info "Restoring logs..."
        mkdir -p "./logs"
        cp -r "$backup_dir/logs"/* "./logs/" 2>/dev/null || true
        log_success "Logs restored"
    fi

    # Start services after restore
    log_info "Starting services..."
    docker-compose -f docker-compose.prod.yml up -d

    log_success "Restore completed successfully"
}

# List available backups
list_backups() {
    echo "Available backups in $BACKUP_ROOT:"
    echo "=================================="

    if [[ ! -d "$BACKUP_ROOT" ]]; then
        echo "No backups directory found"
        return
    fi

    local count=0
    for backup in "$BACKUP_ROOT"/*.tar.gz; do
        if [[ -f "$backup" ]]; then
            local size=$(du -sh "$backup" | cut -f1)
            local date=$(stat -c %y "$backup" 2>/dev/null | cut -d'.' -f1)
            echo "$(basename "$backup") - $size - $date"
            ((count++))
        fi
    done

    if [[ $count -eq 0 ]]; then
        echo "No backup files found"
    else
        echo ""
        echo "Total backups: $count"
    fi
}

# Cleanup old backups
cleanup_backups() {
    local keep_days="${1:-30}"
    local keep_count="${2:-10}"

    log_info "Cleaning up backups older than $keep_days days, keeping $keep_count most recent"

    if [[ ! -d "$BACKUP_ROOT" ]]; then
        log_warning "No backups directory found"
        return
    fi

    # Remove old backups by date
    find "$BACKUP_ROOT" -name "*.tar.gz" -mtime +$keep_days -delete

    # Keep only most recent backups by count
    local backup_count=$(ls -1 "$BACKUP_ROOT"/*.tar.gz 2>/dev/null | wc -l)
    if [[ $backup_count -gt $keep_count ]]; then
        ls -1t "$BACKUP_ROOT"/*.tar.gz | tail -n +$((keep_count + 1)) | xargs rm -f
        log_success "Cleaned up old backups, kept $keep_count most recent"
    fi
}

# Verify backup integrity
verify_backup() {
    local backup_file="$1"

    if [[ -z "$backup_file" ]]; then
        log_error "Please specify a backup file to verify"
        echo "Usage: $0 verify <backup_file.tar.gz>"
        exit 1
    fi

    if [[ ! -f "$backup_file" ]]; then
        log_error "Backup file not found: $backup_file"
        exit 1
    fi

    log_info "Verifying backup integrity: $backup_file"

    # Check if archive is valid
    if ! tar -tzf "$backup_file" > /dev/null 2>&1; then
        log_error "Backup archive is corrupted"
        exit 1
    fi

    # Extract and verify manifest
    local temp_dir=$(mktemp -d)
    trap "rm -rf $temp_dir" EXIT

    tar -xzf "$backup_file" -C "$temp_dir"

    local backup_dir=$(find "$temp_dir" -mindepth 1 -maxdepth 1 -type d | head -1)

    if [[ ! -f "$backup_dir/manifest.txt" ]]; then
        log_warning "Backup manifest not found"
    else
        log_info "Backup manifest found"
        echo "Manifest contents:"
        echo "---"
        cat "$backup_dir/manifest.txt"
        echo "---"
    fi

    # Check for essential files
    local essential_files=("database.db")
    local missing_files=()

    for file in "${essential_files[@]}"; do
        if [[ ! -f "$backup_dir/$file" ]]; then
            missing_files+=("$file")
        fi
    done

    if [[ ${#missing_files[@]} -gt 0 ]]; then
        log_warning "Missing essential files: ${missing_files[*]}"
    else
        log_success "All essential files present"
    fi

    log_success "Backup verification completed"
}

# Show usage
usage() {
    echo "Email Intelligence Platform - Backup & Recovery Tool"
    echo ""
    echo "Usage: $0 <command> [options]"
    echo ""
    echo "Commands:"
    echo "  backup           Create a new backup"
    echo "  restore <file>   Restore from backup file"
    echo "  list             List available backups"
    echo "  cleanup [days] [count]  Clean up old backups (default: 30 days, keep 10)"
    echo "  verify <file>    Verify backup integrity"
    echo "  help             Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 backup"
    echo "  $0 restore backups/email_intelligence_20231201_120000.tar.gz"
    echo "  $0 cleanup 7 5"
    echo "  $0 verify backups/email_intelligence_20231201_120000.tar.gz"
}

# Main script logic
case "${1:-help}" in
    "backup")
        create_backup
        ;;
    "restore")
        restore_backup "$2"
        ;;
    "list")
        list_backups
        ;;
    "cleanup")
        cleanup_backups "$2" "$3"
        ;;
    "verify")
        verify_backup "$2"
        ;;
    "help"|*)
        usage
        ;;
esac</content>
</xai:function_call: <parameter name="path">/home/masum/github/EmailIntelligence/backup.sh
