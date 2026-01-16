#!/bin/bash
# Logging utility functions for orchestration scripts

# Log levels
LOG_LEVEL=${LOG_LEVEL:-INFO}
LOG_LEVELS=(DEBUG INFO WARN ERROR)

# Default log level mapping
declare -A LOG_LEVEL_MAP
LOG_LEVEL_MAP[DEBUG]=0
LOG_LEVEL_MAP[INFO]=1
LOG_LEVEL_MAP[WARN]=2
LOG_LEVEL_MAP[ERROR]=3

# Setup logging
setup_logging() {
    # Set log level if specified
    if [[ -n "$LOG_LEVEL" ]]; then
        for level in "${LOG_LEVELS[@]}"; do
            if [[ "$level" == "$LOG_LEVEL" ]]; then
                CURRENT_LOG_LEVEL=$level
                break
            fi
        done
    fi
    CURRENT_LOG_LEVEL=${CURRENT_LOG_LEVEL:-INFO}
}

# Check if log level should be shown
should_log() {
    local level=$1
    local current_level_num=${LOG_LEVEL_MAP[$CURRENT_LOG_LEVEL]}
    local message_level_num=${LOG_LEVEL_MAP[$level]}

    [[ $message_level_num -ge $current_level_num ]]
}

# Logging functions
log_debug() {
    should_log "DEBUG" && echo "[DEBUG] $*" >&2
}

log_info() {
    should_log "INFO" && echo "[INFO] $*" >&2
}

log_warn() {
    should_log "WARN" && echo "[WARN] $*" >&2
}

log_error() {
    should_log "ERROR" && echo "[ERROR] $*" >&2
}