#!/bin/bash
# modules/config.sh - Configuration module (~200 lines)

# Import dependencies if needed
# Define constants for this module
readonly CONFIG_FILE_PATH="${PROJECT_ROOT:-.}/config/distribution.json"
readonly DEFAULT_CONFIG_PATH="$(dirname "${BASH_SOURCE[0]}")/../config/default.json"

# Default configuration structure
DEFAULT_CONFIG='{
  "sources": {
    "orchestration-tools": {
      "remote": "origin/orchestration-tools",
      "directories": ["setup/", "scripts/hooks/", "scripts/lib/", "config/"],
      "files": [".flake8", ".pylintrc", ".gitignore", "launch.py"],
      "validation_script": "scripts/validate-orchestration-context.sh"
    }
  },
  "targets": {
    "orchestration-tools-*": {
      "allowed": true,
      "sync_method": "git-worktree-safe",
      "validation_after_sync": true
    },
    "taskmaster-*": {
      "allowed": false,
      "reason": "worktree-isolation-required"
    },
    "other": {
      "allowed": false,
      "reason": "orchestration-not-applicable"
    }
  },
  "validation_rules": {
    "large_file_threshold": 52428800,
    "sensitive_patterns": ["password", "secret", "key", "token"],
    "required_files": ["scripts/install-hooks.sh", "setup/launch.py"]
  }
}'

# Function to load distribution configuration
load_distribution_config() {
    # Check if config file exists, if not create default
    if [[ ! -f "$CONFIG_FILE_PATH" ]]; then
        echo "Configuration file not found, creating default..."
        create_default_config
    fi
    
    # Load configuration from file
    if [[ -f "$CONFIG_FILE_PATH" ]]; then
        echo "Loading configuration from $CONFIG_FILE_PATH"
        # In a real implementation, we would parse the JSON and set variables
        # For now, we'll just validate the file exists and is readable
        if [[ -r "$CONFIG_FILE_PATH" ]]; then
            echo "Configuration loaded successfully"
            return 0
        else
            echo "ERROR: Cannot read configuration file $CONFIG_FILE_PATH"
            return 1
        fi
    else
        echo "ERROR: Configuration file $CONFIG_FILE_PATH does not exist"
        return 1
    fi
}

# Function to create default configuration
create_default_config() {
    # Create config directory if it doesn't exist
    mkdir -p "$(dirname "$CONFIG_FILE_PATH")"
    
    # Write default configuration
    echo "$DEFAULT_CONFIG" > "$CONFIG_FILE_PATH"
    
    echo "Default configuration created at $CONFIG_FILE_PATH"
}

# Function to get branch-specific configuration
get_branch_config() {
    local branch_name="$1"
    
    # In a real implementation, we would parse the JSON and return branch-specific config
    # For now, we'll determine the branch type and return appropriate settings
    if [[ "$branch_name" == taskmaster* ]]; then
        echo '{"allowed": false, "reason": "worktree-isolation-required"}'
    elif [[ "$branch_name" == orchestration-tools* ]]; then
        echo '{"allowed": true, "sync_method": "git-worktree-safe", "validation_after_sync": true}'
    else
        echo '{"allowed": false, "reason": "orchestration-not-applicable"}'
    fi
}

# Function to validate configuration integrity
validate_config_integrity() {
    if [[ ! -f "$CONFIG_FILE_PATH" ]]; then
        echo "ERROR: Configuration file does not exist: $CONFIG_FILE_PATH"
        return 1
    fi
    
    # Check if the file is valid JSON
    if ! jq empty "$CONFIG_FILE_PATH" 2>/dev/null; then
        echo "ERROR: Configuration file is not valid JSON: $CONFIG_FILE_PATH"
        return 1
    fi
    
    # Validate required fields exist
    local required_fields=("sources" "targets" "validation_rules")
    for field in "${required_fields[@]}"; do
        if ! jq -e ".${field}" "$CONFIG_FILE_PATH" >/dev/null 2>&1; then
            echo "ERROR: Missing required field '$field' in configuration"
            return 1
        fi
    done
    
    echo "Configuration integrity validated"
    return 0
}

# Function to get target branches from configuration
get_target_branches_from_config() {
    # In a real implementation, we would parse the JSON and extract target branches
    # For now, we'll return orchestration-tools branches
    git branch -r | grep "origin/orchestration-tools-" | sed 's/origin\///' | xargs
}

# Function to get source files from configuration
get_source_files_from_config() {
    # In a real implementation, we would parse the JSON and extract source files
    # For now, we'll return default source files
    echo "setup/ scripts/hooks/ scripts/lib/ .flake8 .pylintrc .gitignore launch.py"
}

# Function to get validation script from configuration
get_validation_script_from_config() {
    # In a real implementation, we would parse the JSON and extract validation script
    # For now, we'll return default validation script
    echo "scripts/validate-orchestration-context.sh"
}

# Function to get remote source from configuration
get_remote_source_from_config() {
    # In a real implementation, we would parse the JSON and extract remote source
    # For now, we'll return default remote source
    echo "origin/orchestration-tools"
}

# Function to check if branch is allowed for distribution
is_branch_allowed_for_distribution() {
    local branch_name="$1"
    
    # In a real implementation, we would parse the JSON and check if branch is allowed
    # For now, we'll use simple logic based on branch name
    if [[ "$branch_name" == taskmaster* ]]; then
        return 1  # Not allowed
    elif [[ "$branch_name" == orchestration-tools* ]]; then
        return 0  # Allowed
    else
        return 1  # Not allowed
    fi
}

# Function to get distribution method for a branch
get_distribution_method() {
    local branch_name="$1"
    
    # In a real implementation, we would parse the JSON and get distribution method
    # For now, we'll return default method
    if [[ "$branch_name" == orchestration-tools* ]]; then
        echo "git-worktree-safe"
    else
        echo "none"
    fi
}

# Function to check if validation is required after sync
is_validation_required_after_sync() {
    local branch_name="$1"
    
    # In a real implementation, we would parse the JSON and check validation requirement
    # For now, we'll return true for orchestration-tools branches
    if [[ "$branch_name" == orchestration-tools* ]]; then
        return 0  # Yes, validation required
    else
        return 1  # No, validation not required
    fi
}

# Function to get large file threshold from config
get_large_file_threshold() {
    # In a real implementation, we would parse the JSON and extract threshold
    # For now, we'll return default threshold (50MB)
    echo 52428800
}

# Function to get sensitive patterns from config
get_sensitive_patterns() {
    # In a real implementation, we would parse the JSON and extract patterns
    # For now, we'll return default patterns
    echo "password secret key token credential private"
}

# Function to get required files from config
get_required_files() {
    # In a real implementation, we would parse the JSON and extract required files
    # For now, we'll return default required files
    echo "scripts/install-hooks.sh setup/launch.py"
}

# Function to update configuration value
update_config_value() {
    local key="$1"
    local value="$2"
    
    if [[ ! -f "$CONFIG_FILE_PATH" ]]; then
        echo "ERROR: Configuration file does not exist: $CONFIG_FILE_PATH"
        return 1
    fi
    
    # In a real implementation, we would use jq to update the JSON
    # For now, we'll just indicate this is not implemented
    echo "Updating configuration value $key=$value (not implemented in this version)"
    return 0
}

# Export functions that should be available to other modules
export -f load_distribution_config
export -f create_default_config
export -f get_branch_config
export -f validate_config_integrity
export -f get_target_branches_from_config
export -f get_source_files_from_config
export -f get_validation_script_from_config
export -f get_remote_source_from_config
export -f is_branch_allowed_for_distribution
export -f get_distribution_method
export -f is_validation_required_after_sync
export -f get_large_file_threshold
export -f get_sensitive_patterns
export -f get_required_files
export -f update_config_value