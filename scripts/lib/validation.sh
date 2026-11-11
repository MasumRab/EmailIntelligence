#!/bin/bash
# Validation utility functions for orchestration scripts

# Error codes
ERROR_NONE=0
ERROR_GIT=1
ERROR_FILESYSTEM=2
ERROR_VALIDATION=3
ERROR_CONFIG=4
ERROR_UNEXPECTED=99

# Validate git repository
validate_git_repo() {
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        log_error "Not in a git repository"
        return $ERROR_GIT
    fi

    log_debug "Git repository validated"
    return $ERROR_NONE
}

# Validate orchestration-tools branch exists
validate_orchestration_branch() {
    if ! git show-ref --verify --quiet refs/heads/orchestration-tools && \
       ! git show-ref --verify --quiet refs/remotes/origin/orchestration-tools; then
        log_error "orchestration-tools branch not found"
        return $ERROR_GIT
    fi

    log_debug "orchestration-tools branch validated"
    return $ERROR_NONE
}

# Validate hooks directory exists
validate_hooks_directory() {
    local hooks_dir="${HOOKS_DIR:-scripts/hooks}"

    if [[ ! -d "$hooks_dir" ]]; then
        log_error "Hooks directory not found: $hooks_dir"
        return $ERROR_FILESYSTEM
    fi

    log_debug "Hooks directory validated: $hooks_dir"
    return $ERROR_NONE
}

# Validate git hooks directory
validate_git_hooks_directory() {
    local git_hooks_dir="${GIT_HOOKS_DIR:-.git/hooks}"

    if [[ ! -d "$git_hooks_dir" ]]; then
        log_error "Git hooks directory not found: $git_hooks_dir"
        return $ERROR_FILESYSTEM
    fi

    log_debug "Git hooks directory validated: $git_hooks_dir"
    return $ERROR_NONE
}

# Comprehensive environment validation
validate_environment() {
    local errors=0

    validate_git_repo || ((errors++))
    validate_orchestration_branch || ((errors++))
    validate_hooks_directory || ((errors++))
    validate_git_hooks_directory || ((errors++))

    if [[ $errors -gt 0 ]]; then
        log_error "Environment validation failed with $errors errors"
        return $ERROR_VALIDATION
    fi

    log_info "Environment validation passed"
    return $ERROR_NONE
}