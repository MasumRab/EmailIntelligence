#!/bin/bash
# modules/utils.sh - Utility module (~200 lines)

# Import dependencies if needed
# Define constants for this module
readonly TEMP_DIR="${TEMP_DIR:-${PROJECT_ROOT:-.}/temp}"
readonly BACKUP_DIR="${BACKUP_DIR:-${PROJECT_ROOT:-.}/backups}"

# Function to get git repository information
get_git_info() {
    local info_type="$1"
    
    case "$info_type" in
        "branch")
            git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown"
            ;;
        "commit-hash")
            git rev-parse HEAD 2>/dev/null || echo "unknown"
            ;;
        "repo-root")
            git rev-parse --show-toplevel 2>/dev/null || pwd
            ;;
        "current-status")
            git status --porcelain 2>/dev/null || echo "error"
            ;;
        "remote-urls")
            git remote -v 2>/dev/null | awk '{print $2}' | sort -u
            ;;
        *)
            echo "unknown"
            ;;
    esac
}

# Function to check remote repository status
check_remote_status() {
    local remote_name="${1:-origin}"
    local branch_name="${2:-$(get_git_info "branch")}"
    
    # Fetch latest information from remote
    if ! git fetch "$remote_name" "$branch_name" 2>/dev/null; then
        echo "ERROR: Could not fetch from $remote_name/$branch_name"
        return 1
    fi
    
    # Get local and remote commit hashes
    local local_hash=$(git rev-parse HEAD 2>/dev/null)
    local remote_hash=$(git rev-parse "$remote_name/$branch_name" 2>/dev/null)
    
    if [[ -z "$remote_hash" ]]; then
        echo "INFO: Remote branch $remote_name/$branch_name does not exist"
        return 0
    fi
    
    # Compare hashes
    if [[ "$local_hash" == "$remote_hash" ]]; then
        echo "up-to-date"
    else
        local ahead_count=$(git rev-list --count "$remote_hash..$local_hash" 2>/dev/null)
        local behind_count=$(git rev-list --count "$local_hash..$remote_hash" 2>/dev/null)
        
        if [[ $ahead_count -gt 0 ]] && [[ $behind_count -gt 0 ]]; then
            echo "diverged ahead:$ahead_count behind:$behind_count"
        elif [[ $ahead_count -gt 0 ]]; then
            echo "ahead by $ahead_count commits"
        elif [[ $behind_count -gt 0 ]]; then
            echo "behind by $behind_count commits"
        else
            echo "unknown state"
        fi
    fi
}

# Function to fix file permissions
fix_permissions() {
    local target_path="$1"
    
    if [[ -z "$target_path" ]]; then
        echo "ERROR: No target path specified"
        return 1
    fi
    
    if [[ ! -e "$target_path" ]]; then
        echo "ERROR: Path does not exist: $target_path"
        return 1
    fi
    
    # Make shell scripts executable
    if [[ -f "$target_path" ]] && [[ "$target_path" == *.sh ]]; then
        chmod +x "$target_path"
        echo "Made executable: $target_path"
    elif [[ -d "$target_path" ]]; then
        # Recursively make shell scripts executable in directory
        find "$target_path" -type f -name "*.sh" -exec chmod +x {} \;
        echo "Fixed permissions for shell scripts in: $target_path"
        
        # Also make hook scripts executable
        find "$target_path" -path "*/hooks/*" -type f -exec chmod +x {} \;
        echo "Fixed permissions for hook scripts in: $target_path"
    fi
    
    return 0
}

# Function to create backup of files/directory
create_backup() {
    local source_path="$1"
    local backup_name="${2:-$(date +%Y%m%d_%H%M%S)}"
    
    if [[ -z "$source_path" ]]; then
        echo "ERROR: No source path specified"
        return 1
    fi
    
    if [[ ! -e "$source_path" ]]; then
        echo "ERROR: Source path does not exist: $source_path"
        return 1
    fi
    
    # Create backup directory if it doesn't exist
    mkdir -p "$BACKUP_DIR"
    
    # Create backup with timestamp
    local backup_path="$BACKUP_DIR/$(basename "$source_path")_backup_$backup_name"
    
    if [[ -d "$source_path" ]]; then
        cp -r "$source_path" "$backup_path"
    else
        cp "$source_path" "$backup_path"
    fi
    
    if [[ $? -eq 0 ]]; then
        echo "Backup created: $backup_path"
        return 0
    else
        echo "ERROR: Failed to create backup of $source_path"
        return 1
    fi
}

# Function to restore from backup
restore_from_backup() {
    local backup_path="$1"
    local target_path="$2"
    
    if [[ -z "$backup_path" ]] || [[ -z "$target_path" ]]; then
        echo "ERROR: Both backup path and target path must be specified"
        return 1
    fi
    
    if [[ ! -e "$backup_path" ]]; then
        echo "ERROR: Backup path does not exist: $backup_path"
        return 1
    fi
    
    # Create target directory if needed
    mkdir -p "$(dirname "$target_path")"
    
    # Remove existing target if it exists
    if [[ -e "$target_path" ]]; then
        rm -rf "$target_path"
    fi
    
    # Restore from backup
    if [[ -d "$backup_path" ]]; then
        cp -r "$backup_path" "$target_path"
    else
        cp "$backup_path" "$target_path"
    fi
    
    if [[ $? -eq 0 ]]; then
        echo "Restored from backup: $backup_path to $target_path"
        return 0
    else
        echo "ERROR: Failed to restore from backup $backup_path to $target_path"
        return 1
    fi
}

# Function to validate JSON file
validate_json() {
    local json_file="$1"
    
    if [[ ! -f "$json_file" ]]; then
        echo "ERROR: File does not exist: $json_file"
        return 1
    fi
    
    if ! command -v jq >/dev/null 2>&1; then
        echo "WARNING: jq command not found, skipping JSON validation"
        return 0
    fi
    
    if jq empty "$json_file" 2>/dev/null; then
        echo "JSON is valid: $json_file"
        return 0
    else
        echo "ERROR: Invalid JSON in file: $json_file"
        return 1
    fi
}

# Function to wait for file lock
wait_for_file_lock() {
    local file_path="$1"
    local timeout="${2:-30}"  # Default 30 seconds timeout
    
    local count=0
    while [[ $count -lt $timeout ]]; do
        if [[ ! -f "$file_path.lock" ]]; then
            # Create lock file
            touch "$file_path.lock"
            echo "Acquired lock for: $file_path"
            return 0
        fi
        sleep 1
        ((count++))
    done
    
    echo "ERROR: Timeout waiting for lock on: $file_path"
    return 1
}

# Function to release file lock
release_file_lock() {
    local file_path="$1"
    
    local lock_file="$file_path.lock"
    if [[ -f "$lock_file" ]]; then
        rm -f "$lock_file"
        echo "Released lock for: $file_path"
    fi
}

# Function to calculate file/directory size
calculate_size() {
    local path="$1"
    
    if [[ ! -e "$path" ]]; then
        echo "0"
        return 0
    fi
    
    if [[ -f "$path" ]]; then
        stat -c%s "$path" 2>/dev/null || echo "0"
    elif [[ -d "$path" ]]; then
        du -sb "$path" 2>/dev/null | cut -f1 || echo "0"
    else
        echo "0"
    fi
}

# Function to check if command exists
command_exists() {
    local cmd="$1"
    
    if command -v "$cmd" >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Function to create temporary directory
create_temp_dir() {
    local suffix="${1:-$$}"
    
    local temp_dir="$TEMP_DIR/temp_$suffix"
    mkdir -p "$temp_dir"
    
    echo "$temp_dir"
    return 0
}

# Function to clean up temporary files
cleanup_temp_files() {
    local days_old="${1:-1}"  # Default to cleaning files older than 1 day
    
    if [[ -d "$TEMP_DIR" ]]; then
        find "$TEMP_DIR" -type f -mtime +$days_old -delete 2>/dev/null
        find "$TEMP_DIR" -type d -empty -delete 2>/dev/null
        echo "Cleaned up temporary files older than $days_old day(s)"
    fi
}

# Function to read configuration value from file
read_config_value() {
    local config_file="$1"
    local key="$2"
    
    if [[ ! -f "$config_file" ]]; then
        echo ""
        return 1
    fi
    
    if command_exists jq; then
        # Use jq if available for JSON files
        jq -r ".${key}" "$config_file" 2>/dev/null || echo ""
    else
        # Fallback method for simple key=value files
        grep "^$key=" "$config_file" 2>/dev/null | cut -d'=' -f2- || echo ""
    fi
}

# Function to write configuration value to file
write_config_value() {
    local config_file="$1"
    local key="$2"
    local value="$3"
    
    # Create config directory if it doesn't exist
    mkdir -p "$(dirname "$config_file")"
    
    if [[ -f "$config_file" ]] && command_exists jq; then
        # Use jq if available for JSON files
        jq --arg key "$key" --arg val "$value" '.[$key]=$val' "$config_file" > "${config_file}.tmp" && mv "${config_file}.tmp" "$config_file"
    else
        # Fallback method for simple key=value files
        if grep -q "^$key=" "$config_file" 2>/dev/null; then
            sed -i "s/^$key=.*/$key=$value/" "$config_file"
        else
            echo "$key=$value" >> "$config_file"
        fi
    fi
}

# Export functions that should be available to other modules
export -f get_git_info
export -f check_remote_status
export -f fix_permissions
export -f create_backup
export -f restore_from_backup
export -f validate_json
export -f wait_for_file_lock
export -f release_file_lock
export -f calculate_size
export -f command_exists
export -f create_temp_dir
export -f cleanup_temp_files
export -f read_config_value
export -f write_config_value