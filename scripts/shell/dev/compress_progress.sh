#!/usr/bin/env bash
#===============================================================================
# Simple Progress File Compression Script
# 
# Compresses progress tracking files with checksums for verification.
# Run from project root.
#===============================================================================

set -euo pipefail

# Configuration
SOURCE_DIR="${1:-.}"
BACKUP_DIR="${2:-backups}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
ARCHIVE_NAME="progress_${TIMESTAMP}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

#===============================================================================
# FUNCTIONS
#===============================================================================

show_help() {
    cat << EOF
Progress File Compression Tool

Usage: $0 [COMMAND] [OPTIONS]

Commands:
    compress    Compress progress files
    decompress  Decompress an archive
    list        List available archives
    verify      Verify archive integrity
    status      Show current compression status

Options:
    --source DIR      Source directory (default: .)
    --backup DIR      Backup directory (default: backups)
    --essential       Only compress essential files
    --format FORMAT   Compression format: gz, bz2, xz (default: xz)

Examples:
    $0 compress --source . --backup backups
    $0 compress --essential --format xz
    $0 decompress backups/progress_20260104_120000.tar.xz
    $0 list
    $0 verify backups/progress_20260104_120000.tar.xz

EOF
}

# Create backup directory if it doesn't exist
init_backup_dir() {
    mkdir -p "$BACKUP_DIR"
}

# Calculate SHA-256 checksum
checksum() {
    sha256sum "$1" | awk '{print $1}'
}

# Compress progress files
do_compress() {
    local format="${1:-xz}"
    local essential_only=false
    
    # Parse remaining arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --essential) essential_only=true; shift ;;
            --format) format=$2; shift 2 ;;
            *) shift ;;
        esac
    done
    
    init_backup_dir
    
    log_info "Compressing progress files..."
    log_info "Source: $SOURCE_DIR"
    log_info "Destination: $BACKUP_DIR"
    log_info "Format: $format"
    
    # Create temporary directory for staging
    local temp_dir=$(mktemp -d)
    local stage_dir="$temp_dir/stage"
    mkdir -p "$stage_dir"
    
    # Create manifest
    local manifest_file="$stage_dir/manifest.json"
    echo "{" > "$manifest_file"
    echo "  \"created\": \"$(date -Iseconds)\"," >> "$manifest_file"
    echo "  \"source\": \"$SOURCE_DIR\"," >> "$manifest_file"
    echo "  \"files\": {" >> "$manifest_file"
    
    # Find and add files
    local file_count=0
    local total_size=0
    local first=true
    
    # Essential files (always include)
    if $essential_only; then
        for file in PROJECT_REFERENCE.md ENHANCED_VALIDATION_PLAN.md LOGGING_SYSTEM_PLAN.md \
                    LOGGING_GUIDE.md CLEAN_TASK_INDEX.md README.md AGENTS.md CLAUDE.md; do
            if [[ -f "$SOURCE_DIR/$file" ]]; then
                cp "$SOURCE_DIR/$file" "$stage_dir/"
                local size=$(stat -c%s "$SOURCE_DIR/$file")
                local hash=$(checksum "$SOURCE_DIR/$file")
                echo "  \"$file\": {\"size\": $size, \"sha256\": \"$hash\"}," >> "$manifest_file"
                ((file_count++))
                ((total_size+=size))
            fi
        done
    else
        # Find progress-related files
        while IFS= read -r -d '' file; do
            local rel_path="${file#$SOURCE_DIR/}"
            local size=$(stat -c%s "$file")
            local hash=$(checksum "$file")
            
            if [ "$first" = true ]; then
                first=false
            else
                echo "," >> "$manifest_file"
            fi
            echo -n "  \"$rel_path\": {\"size\": $size, \"sha256\": \"$hash\"}" >> "$manifest_file"
            
            cp "$file" "$stage_dir/$rel_path"
            ((file_count++))
            ((total_size+=size))
        done < <(find "$SOURCE_DIR" -type f \( \
            -name "*.md" -o -name "*.json" -o -name "*.txt" -o -name "*.log" \
            \) -print0 2>/dev/null)
    fi
    
    echo "" >> "$manifest_file"
    echo "  }," >> "$manifest_file"
    echo "  \"totals\": {" >> "$manifest_file"
    echo "    \"file_count\": $file_count," >> "$manifest_file"
    echo "    \"original_size\": $total_size" >> "$manifest_file"
    echo "  }" >> "$manifest_file"
    echo "}" >> "$manifest_file"
    
    # Create archive
    local archive_path="$BACKUP_DIR/${ARCHIVE_NAME}.tar.${format}"
    log_info "Creating archive: $archive_path"
    
    case $format in
        gz)  tar -czf "$archive_path" -C "$temp_dir" stage ;;
        bz2) tar -cjf "$archive_path" -C "$temp_dir" stage ;;
        xz)  tar -cJf "$archive_path" -C "$temp_dir" stage ;;
        *)   log_error "Unknown format: $format"; rm -rf "$temp_dir"; exit 1 ;;
    esac
    
    # Calculate compressed size
    local compressed_size=$(stat -c%s "$archive_path")
    local ratio=$(echo "scale=1; (1 - $compressed_size / $total_size) * 100" | bc)
    
    log_info "Compression complete!"
    log_info "  Files: $file_count"
    log_info "  Original: $(echo "scale=2; $total_size / 1024 / 1024" | bc) MB"
    log_info "  Compressed: $(echo "scale=2; $compressed_size / 1024 / 1024" | bc) MB"
    log_info "  Ratio: ${ratio}%"
    
    # Cleanup
    rm -rf "$temp_dir"
}

# Decompress an archive
do_decompress() {
    local archive="${1:-}"
    
    if [[ -z "$archive" ]]; then
        log_error "Archive name required"
        echo "Usage: $0 decompress <archive.tar.xz>"
        exit 1
    fi
    
    local archive_path="$BACKUP_DIR/$archive"
    
    if [[ ! -f "$archive_path" ]]; then
        log_error "Archive not found: $archive_path"
        exit 1
    fi
    
    init_backup_dir
    
    log_info "Decompressing: $archive"
    log_info "To: $SOURCE_DIR"
    
    # Create restore directory
    local restore_dir="$SOURCE_DIR/restore_$TIMESTAMP"
    mkdir -p "$restore_dir"
    
    # Extract to restore directory first
    tar -xf "$archive_path" -C "$restore_dir"
    
    # Verify checksums
    if [[ -f "$restore_dir/manifest.json" ]]; then
        log_info "Verifying checksums..."
        
        # Verify each file
        while IFS= read -r line; do
            local file=$(echo "$line" | cut -d: -f1)
            local expected_hash=$(echo "$line" | cut -d: -f2)
            
            if [[ -f "$restore_dir/$file" ]]; then
                local actual_hash=$(checksum "$restore_dir/$file")
                if [[ "$expected_hash" != "$actual_hash" ]]; then
                    log_error "Checksum mismatch: $file"
                    log_error "  Expected: $expected_hash"
                    log_error "  Actual: $actual_hash"
                    exit 1
                fi
            fi
        done < <(grep -o '"[^"]*": {"size": [0-9]*, "sha256": "[^"]*"}' "$restore_dir/manifest.json" | \
              sed 's/: {"size": /:/; s/, "sha256": /:/; s/}//' | tr -d '"')
        
        log_info "All checksums verified"
    fi
    
    # Move files to source
    log_info "Restoring files..."
    find "$restore_dir" -maxdepth 1 -type f -name "*.md" -o -name "*.json" -o -name "*.txt" | \
        while read -r file; do
            local filename=$(basename "$file")
            cp -n "$file" "$SOURCE_DIR/"
            log_info "  Restored: $filename"
        done
    
    # Cleanup restore directory
    rm -rf "$restore_dir"
    
    log_info "Decompression complete!"
}

# List available archives
do_list() {
    init_backup_dir
    
    echo "Available archives in $BACKUP_DIR:"
    echo ""
    
    local count=0
    for archive in "$BACKUP_DIR"/progress_*.tar.*; do
        if [[ -f "$archive" ]]; then
            local size=$(stat -c%s "$archive")
            local size_mb=$(echo "scale=2; $size / 1024 / 1024" | bc)
            local date_str=$(basename "$archive" | grep -oP '\d{8}_\d{6}')
            local date_formatted=$(date -d "${date_str:0:8} ${date_str:9:2}:${date_str:11:2}:${date_str:13:2}" 2>/dev/null || echo "$date_str")
            
            # Get file count from manifest if exists
            local manifest="${archive}.manifest.json"
            local files="?"
            if [[ -f "$manifest" ]]; then
                files=$(grep -o '"file_count"' "$manifest" | wc -l)
            fi
            
            printf "  %-50s %8s MB  [%s files]\n" "$(basename "$archive")" "$size_mb" "$files"
            ((count++))
        fi
    done
    
    if [[ $count -eq 0 ]]; then
        echo "  No archives found"
    fi
    
    echo ""
    echo "Total: $count archives"
}

# Verify archive integrity
do_verify() {
    local archive="${1:-}"
    
    if [[ -z "$archive" ]]; then
        log_error "Archive name required"
        exit 1
    fi
    
    local archive_path="$BACKUP_DIR/$archive"
    
    if [[ ! -f "$archive_path" ]]; then
        log_error "Archive not found: $archive_path"
        exit 1
    fi
    
    log_info "Verifying: $archive"
    
    # Check archive is readable
    if tar -tf "$archive_path" > /dev/null 2>&1; then
        log_info "  Archive readable: OK"
    else
        log_error "  Archive readable: FAILED"
        exit 1
    fi
    
    # Check manifest
    local manifest="${archive_path}.manifest.json"
    if [[ -f "$manifest" ]]; then
        if python3 -c "import json; json.load(open('$manifest'))" 2>/dev/null; then
            log_info "  Manifest valid: OK"
        else
            log_error "  Manifest valid: FAILED"
            exit 1
        fi
    else
        log_warn "  Manifest not found (optional)"
    fi
    
    log_info "Verification complete: PASSED"
}

# Show compression status
do_status() {
    init_backup_dir
    
    echo "Compression Status"
    echo "=================="
    echo ""
    
    # Count files
    local md_files=$(find "$SOURCE_DIR" -name "*.md" 2>/dev/null | wc -l)
    local json_files=$(find "$SOURCE_DIR" -name "*.json" 2>/dev/null | wc -l)
    local total_size=$(du -sh "$SOURCE_DIR" 2>/dev/null | cut -f1)
    
    echo "Source Directory: $SOURCE_DIR"
    echo "  Markdown files: $md_files"
    echo "  JSON files: $json_files"
    echo "  Total size: $total_size"
    echo ""
    
    echo "Backup Directory: $BACKUP_DIR"
    local archive_count=$(find "$BACKUP_DIR" -name "progress_*.tar.*" 2>/dev/null | wc -l)
    local backup_size=$(du -sh "$BACKUP_DIR" 2>/dev/null | cut -f1)
    echo "  Archives: $archive_count"
    echo "  Total size: $backup_size"
    echo ""
    
    if [[ $archive_count -gt 0 ]]; then
        echo "Latest Archive:"
        latest=$(find "$BACKUP_DIR" -name "progress_*.tar.*" -printf "%T@ %p\n" 2>/dev/null | sort -rn | head -1 | cut -d' ' -f2-)
        if [[ -n "$latest" ]]; then
            latest_size=$(stat -c%s "$latest" 2>/dev/null || echo 0)
            latest_mb=$(echo "scale=2; $latest_size / 1024 / 1024" | bc)
            echo "  $(basename "$latest"): ${latest_mb} MB"
        fi
    fi
}

#===============================================================================
# MAIN
#===============================================================================

main() {
    local command="${1:-status}"
    shift 2>/dev/null || true
    
    case $command in
        compress|decompress|list|verify|status|--help|-h)
            "do_${command}" "$@"
            ;;
        *)
            log_error "Unknown command: $command"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
