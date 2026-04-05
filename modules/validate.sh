#!/bin/bash
# modules/validate.sh - Validation module (~200 lines)

# Import dependencies if needed
# Define constants for this module
readonly VALIDATION_CONFIG_PATH="${PROJECT_ROOT:-.}/config/validation.json"

# Function to validate branch type
validate_branch_type() {
    local branch="$1"
    
    if [[ "$branch" == orchestration-tools* ]]; then
        echo "Branch $branch identified as orchestration-tools branch"
        return 0
    elif [[ "$branch" == taskmaster* ]]; then
        echo "Branch $branch identified as taskmaster branch"
        return 0
    elif [[ "$branch" == main ]] || [[ "$branch" == scientific* ]]; then
        echo "Branch $branch identified as main/scientific branch"
        return 0
    else
        echo "Branch $branch identified as generic branch"
        return 0
    fi
}

# Function to validate remote synchronization status
validate_remote_sync() {
    local source_branch="$1"
    
    # Fetch latest from remote
    git fetch origin "$source_branch" 2>/dev/null || { 
        echo "ERROR: Could not fetch from origin/$source_branch"
        return 1
    }
    
    # Compare local and remote
    local local_hash=$(git rev-parse HEAD)
    local remote_hash=$(git rev-parse "origin/$source_branch")
    
    if [[ "$local_hash" == "$remote_hash" ]]; then
        echo "Local branch is up to date with remote"
        return 0
    else
        echo "Local branch is behind remote by $(git rev-list --count HEAD..origin/$source_branch) commits"
        return 1
    fi
}

# Function to validate file integrity
validate_file_integrity() {
    local source_file="$1"
    local target_file="$2"
    
    if [[ ! -f "$source_file" ]]; then
        echo "ERROR: Source file $source_file does not exist"
        return 1
    fi
    
    if [[ -f "$target_file" ]]; then
        # Compare file checksums
        local source_checksum=$(sha256sum "$source_file" | cut -d' ' -f1)
        local target_checksum=$(sha256sum "$target_file" | cut -d' ' -f1)
        
        if [[ "$source_checksum" == "$target_checksum" ]]; then
            echo "File integrity: $target_file matches $source_file"
            return 0
        else
            echo "WARNING: $target_file differs from $source_file"
            return 1
        fi
    else
        echo "INFO: $target_file does not exist yet"
        return 0
    fi
}

# Function to validate file permissions
validate_permissions() {
    local file_path="$1"
    
    if [[ ! -e "$file_path" ]]; then
        echo "ERROR: File $file_path does not exist"
        return 1
    fi
    
    # Check if it's a script file that should be executable
    if [[ "$file_path" == *.sh ]] || [[ "$file_path" == scripts/* ]] || [[ "$file_path" == scripts/hooks/* ]]; then
        if [[ -x "$file_path" ]]; then
            echo "Permissions OK: $file_path is executable"
            return 0
        else
            echo "WARNING: $file_path should be executable"
            return 1
        fi
    fi
    
    return 0
}

# Function to validate large files (check for files >50MB)
validate_large_files() {
    local directory="$1"
    local threshold=${2:-52428800}  # 50MB in bytes
    
    if [[ ! -d "$directory" ]]; then
        echo "ERROR: Directory $directory does not exist"
        return 1
    fi
    
    local large_files=()
    while IFS= read -r -d '' file; do
        local size=$(stat -c%s "$file")
        if [[ $size -gt $threshold ]]; then
            large_files+=("$file ($(( size / 1024 / 1024 ))MB)")
        fi
    done < <(find "$directory" -type f -print0)
    
    if [[ ${#large_files[@]} -gt 0 ]]; then
        echo "WARNING: Large files detected (>50MB):"
        for large_file in "${large_files[@]}"; do
            echo "  - $large_file"
        done
        return 1
    else
        echo "No large files detected in $directory"
        return 0
    fi
}

# Function to scan for sensitive data
validate_sensitive_data() {
    local file_path="$1"
    local sensitive_patterns=("password" "secret" "key" "token" "credential" "private")
    
    if [[ ! -f "$file_path" ]]; then
        echo "ERROR: File $file_path does not exist"
        return 1
    fi
    
    local found_sensitive=()
    for pattern in "${sensitive_patterns[@]}"; do
        if grep -i -n "$pattern" "$file_path" >/dev/null 2>&1; then
            local matches=$(grep -i -n "$pattern" "$file_path" | head -3 | tr '\n' ';')
            found_sensitive+=("$pattern in $file_path: $matches")
        fi
    done
    
    if [[ ${#found_sensitive[@]} -gt 0 ]]; then
        echo "WARNING: Potential sensitive data detected in $file_path:"
        for sensitive in "${found_sensitive[@]}"; do
            echo "  - $sensitive"
        done
        return 1
    else
        echo "No sensitive data patterns found in $file_path"
        return 0
    fi
}

# Function to validate required files exist
validate_required_files() {
    local required_files=("$@")
    local missing_files=()
    
    for file in "${required_files[@]}"; do
        if [[ ! -f "$file" ]]; then
            missing_files+=("$file")
        fi
    done
    
    if [[ ${#missing_files[@]} -gt 0 ]]; then
        echo "ERROR: Required files missing:"
        for missing in "${missing_files[@]}"; do
            echo "  - $missing"
        done
        return 1
    else
        echo "All required files present"
        return 0
    fi
}

# Function to validate distribution targets
validate_distribution_targets() {
    echo "Validating distribution targets..."
    
    # Validate configuration integrity
    validate_config_integrity
    
    # Validate required orchestration files
    validate_required_files "scripts/install-hooks.sh" "setup/launch.py"
    
    # Validate permissions for scripts
    find "scripts/" -type f -name "*.sh" | while read -r script; do
        validate_permissions "$script"
    done
    
    # Validate hooks are executable
    find "scripts/hooks/" -type f | while read -r hook; do
        validate_permissions "$hook"
    done
    
    return 0
}

# Function to validate commit size
validate_commit_size() {
    local max_size=${1:-104857600}  # 100MB default
    
    # Get the size of the current commit
    local commit_size=$(git diff --cached --numstat | awk '{ sum += $1 + $2 } END { print sum }')
    
    if [[ -z "$commit_size" ]]; then
        commit_size=0
    fi
    
    if [[ $commit_size -gt $max_size ]]; then
        echo "WARNING: Commit size ($(( commit_size / 1024 / 1024 ))MB) exceeds recommended limit ($(( max_size / 1024 / 1024 ))MB)"
        return 1
    else
        echo "Commit size OK: $(( commit_size / 1024 / 1024 ))MB"
        return 0
    fi
}

# Function to validate merge conflicts
validate_merge_conflicts() {
    local conflict_files=()
    
    # Check for files with conflict markers
    while IFS= read -r -d '' file; do
        if [[ -f "$file" ]] && grep -q "^[<=>]\{7,\}" "$file"; then
            conflict_files+=("$file")
        fi
    done < <(git ls-files -u | cut -f2 | sort -u | tr '\n' '\0')
    
    if [[ ${#conflict_files[@]} -gt 0 ]]; then
        echo "ERROR: Unresolved merge conflicts detected:"
        for conflict in "${conflict_files[@]}"; do
            echo "  - $conflict"
        done
        return 1
    else
        echo "No merge conflicts detected"
        return 0
    fi
}

# Export functions that should be available to other modules
export -f validate_branch_type
export -f validate_remote_sync
export -f validate_file_integrity
export -f validate_permissions
export -f validate_large_files
export -f validate_sensitive_data
export -f validate_required_files
export -f validate_distribution_targets
export -f validate_commit_size
export -f validate_merge_conflicts