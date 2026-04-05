#!/bin/bash
# modules/safety.sh - Safety module (~200 lines)

# Import dependencies if needed
# Define constants for this module
readonly SAFETY_BACKUP_DIR="${SAFETY_BACKUP_DIR:-${PROJECT_ROOT:-.}/backups}"

# Function to check for uncommitted files
check_uncommitted_files() {
    local warning_only="${1:-false}"
    
    # Check for uncommitted changes in the working directory
    if ! git diff-index --quiet HEAD -- 2>/dev/null; then
        local uncommitted_files=$(git diff --name-only)
        local uncommitted_count=$(echo "$uncommitted_files" | wc -l)
        
        echo "WARNING: You have $uncommitted_count uncommitted file(s) that might be affected by distribution:"
        echo "$uncommitted_files" | sed 's/^/  - /'
        
        if [[ "$warning_only" == "false" ]]; then
            read -p "Continue with distribution? (y/N): " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                echo "Distribution cancelled by user due to uncommitted files"
                return 1
            fi
        fi
    else
        echo "No uncommitted files detected"
    fi
    
    return 0
}

# Function to confirm destructive action
confirm_destructive_action() {
    local action_description="$1"
    local additional_warning="${2:-""}"
    
    echo "⚠️  WARNING: This action is potentially destructive:"
    echo "  - $action_description"
    
    if [[ -n "$additional_warning" ]]; then
        echo "  - $additional_warning"
    fi
    
    read -p "Are you sure you want to proceed? Type 'YES' to confirm: " -r
    echo
    
    if [[ "$REPLY" == "YES" ]]; then
        return 0
    else
        echo "Action cancelled by user"
        return 1
    fi
}

# Function to preserve orchestration files
preserve_orchestration_files() {
    # Ensure critical orchestration infrastructure is not removed
    local protected_paths=(
        "scripts/"
        "setup/"
        ".taskmaster/"
    )
    
    for path in "${protected_paths[@]}"; do
        if [[ -d "$path" ]]; then
            echo "INFO: Preserving directory: $path"
        elif [[ -f "$path" ]]; then
            echo "INFO: Preserving file: $path"
        fi
    done
    
    # Verify that these directories exist and are not empty (unless explicitly allowed)
    for path in "${protected_paths[@]}"; do
        if [[ -d "$path" ]] && [[ ! "$(ls -A "$path" 2>/dev/null)" ]]; then
            echo "WARNING: Protected directory $path is empty"
        fi
    done
}

# Function to check file overwrite risks
check_file_overwrite_risks() {
    local source_files=("$@")
    local risky_files=()
    
    for file in "${source_files[@]}"; do
        if [[ -f "$file" ]] && [[ ! -w "$file" ]]; then
            risky_files+=("$file (read-only)")
        elif [[ -d "$file" ]] && [[ ! -w "$file" ]]; then
            risky_files+=("$file/ (directory read-only)")
        fi
    done
    
    if [[ ${#risky_files[@]} -gt 0 ]]; then
        echo "WARNING: The following files/directories may pose overwrite risks:"
        for risky_file in "${risky_files[@]}"; do
            echo "  - $risky_file"
        done
        return 1
    else
        echo "No file overwrite risks detected"
        return 0
    fi
}

# Function to validate taskmaster isolation
validate_taskmaster_isolation() {
    # Check that .taskmaster directory exists and is properly isolated
    if [[ ! -d ".taskmaster" ]]; then
        echo "WARNING: .taskmaster directory does not exist - Task Master isolation may not be properly configured"
        return 1
    fi
    
    # Check for any orchestration files that might interfere with Task Master
    local tm_conflicts=()
    while IFS= read -r -d '' file; do
        if [[ "$file" == .taskmaster/* ]]; then
            continue  # Skip files already in .taskmaster
        fi
        
        # Check if any orchestration files exist in places that might conflict with Task Master
        case "$file" in
            "taskmaster"*|*"taskmaster"*)
                tm_conflicts+=("$file")
                ;;
        esac
    done < <(find . -maxdepth 1 -type f -not -path "./.*" -print0 2>/dev/null)
    
    if [[ ${#tm_conflicts[@]} -gt 0 ]]; then
        echo "WARNING: Potential Task Master conflicts detected:"
        for conflict in "${tm_conflicts[@]}"; do
            echo "  - $conflict"
        done
        return 1
    fi
    
    echo "Task Master isolation validated"
    return 0
}

# Function to create safety backup
create_safety_backup() {
    local backup_name="${1:-$(date +%Y%m%d_%H%M%S)}"
    local backup_path="$SAFETY_BACKUP_DIR/backup_$backup_name"
    
    # Create backup directory
    mkdir -p "$backup_path"
    
    # Backup critical directories
    local critical_dirs=("scripts" "setup" "config")
    for dir in "${critical_dirs[@]}"; do
        if [[ -d "$dir" ]]; then
            cp -r "$dir" "$backup_path/" 2>/dev/null || echo "Warning: Could not backup $dir"
        fi
    done
    
    # Backup critical files
    local critical_files=(".flake8" ".pylintrc" ".gitignore" "launch.py")
    for file in "${critical_files[@]}"; do
        if [[ -f "$file" ]]; then
            cp "$file" "$backup_path/" 2>/dev/null || echo "Warning: Could not backup $file"
        fi
    done
    
    echo "Safety backup created at: $backup_path"
    return 0
}

# Function to validate distribution safety
validate_distribution_safety() {
    local target_branch="$1"
    
    # Check if target branch is a taskmaster branch (should not be modified)
    if [[ "$target_branch" == taskmaster* ]]; then
        echo "ERROR: Cannot distribute to taskmaster branches (worktree isolation required)"
        return 1
    fi
    
    # Check if we're on the same branch we're trying to modify
    local current_branch=$(git rev-parse --abbrev-ref HEAD)
    if [[ "$current_branch" == "$target_branch" ]]; then
        echo "WARNING: You are currently on the target branch $target_branch"
        read -p "Continue with distribution? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Distribution cancelled by user"
            return 1
        fi
    fi
    
    # Check for uncommitted changes
    check_uncommitted_files "true"  # Just warn, don't force confirmation here
    
    # Validate taskmaster isolation
    validate_taskmaster_isolation
    
    echo "Distribution safety validated for branch: $target_branch"
    return 0
}

# Function to check for destructive operations
check_for_destructive_operations() {
    local operation_type="$1"
    local target="$2"
    
    case "$operation_type" in
        "delete")
            if [[ "$target" == "scripts/" ]] || [[ "$target" == "setup/" ]] || [[ "$target" == ".taskmaster/" ]]; then
                echo "ERROR: Attempting to delete protected directory: $target"
                confirm_destructive_action "Delete protected directory $target" "This will remove critical orchestration infrastructure"
                return $?
            fi
            ;;
        "overwrite")
            if [[ -f "$target" ]] && [[ "$target" == *".taskmaster/"* ]]; then
                echo "WARNING: Attempting to overwrite Task Master file: $target"
                confirm_destructive_action "Overwrite Task Master file $target" "This may affect Task Master functionality"
                return $?
            fi
            ;;
        "modify")
            if [[ "$target" == "scripts/" ]] || [[ "$target" == "setup/" ]]; then
                echo "INFO: Modifying orchestration directory: $target"
                # This is typically allowed, but we log it
            fi
            ;;
    esac
    
    return 0
}

# Function to validate file permissions before operations
validate_file_permissions() {
    local file_path="$1"
    local operation="$2"  # read, write, execute
    
    case "$operation" in
        "read")
            if [[ ! -r "$file_path" ]]; then
                echo "ERROR: Cannot read file $file_path - insufficient permissions"
                return 1
            fi
            ;;
        "write")
            if [[ ! -w "$file_path" ]]; then
                echo "ERROR: Cannot write to file $file_path - insufficient permissions"
                return 1
            fi
            ;;
        "execute")
            if [[ ! -x "$file_path" ]] && [[ "$file_path" == *.sh ]]; then
                echo "WARNING: File $file_path is not executable but appears to be a script"
            fi
            ;;
    esac
    
    return 0
}

# Function to check disk space availability
check_disk_space() {
    local required_space_mb="${1:-100}"  # Default 100MB required
    
    # Get available disk space in MB
    local available_space_mb=$(df . | awk 'NR==2 {print int($4/1024)}')
    
    if [[ $available_space_mb -lt $required_space_mb ]]; then
        echo "ERROR: Insufficient disk space. Required: ${required_space_mb}MB, Available: ${available_space_mb}MB"
        return 1
    else
        echo "Sufficient disk space available: ${available_space_mb}MB"
        return 0
    fi
}

# Function to validate git repository state
validate_git_repository_state() {
    # Check if we're in a git repository
    if ! git rev-parse --git-dir >/dev/null 2>&1; then
        echo "ERROR: Not in a git repository"
        return 1
    fi
    
    # Check if git directory is corrupted
    if ! git fsck --no-progress >/dev/null 2>&1; then
        echo "ERROR: Git repository appears to be corrupted"
        return 1
    fi
    
    # Check if we're in the middle of a merge, rebase, etc.
    local git_dir=$(git rev-parse --git-dir)
    if [[ -f "$git_dir/MERGE_HEAD" ]]; then
        echo "WARNING: Repository is in the middle of a merge"
    fi
    if [[ -d "$git_dir/rebase-apply" ]] || [[ -d "$git_dir/rebase-merge" ]]; then
        echo "WARNING: Repository is in the middle of a rebase"
    fi
    
    echo "Git repository state validated"
    return 0
}

# Function to validate remote connectivity
validate_remote_connectivity() {
    local remote_name="${1:-origin}"
    
    if ! git remote -v | grep -q "^$remote_name "; then
        echo "ERROR: Remote $remote_name does not exist"
        return 1
    fi
    
    # Test connectivity to remote
    if ! git ls-remote "$remote_name" >/dev/null 2>&1; then
        echo "ERROR: Cannot connect to remote $remote_name - check network connection and credentials"
        return 1
    fi
    
    echo "Remote connectivity to $remote_name validated"
    return 0
}

# Export functions that should be available to other modules
export -f check_uncommitted_files
export -f confirm_destructive_action
export -f preserve_orchestration_files
export -f check_file_overwrite_risks
export -f validate_taskmaster_isolation
export -f create_safety_backup
export -f validate_distribution_safety
export -f check_for_destructive_operations
export -f validate_file_permissions
export -f check_disk_space
export -f validate_git_repository_state
export -f validate_remote_connectivity