#!/bin/bash

################################################################################
# Orchestration Control Module - Shell Implementation
#
# Provides centralized orchestration enable/disable checking.
# This module should be sourced by shell scripts that need to check
# orchestration status.
#
# Usage:
#   source scripts/lib/orchestration-control.sh
#   if is_orchestration_enabled; then
#     # Run orchestration code
#   else
#     echo "Orchestration disabled"
#   fi
#
# For more information, see ORCHESTRATION_CONTROL_MODULE.md
################################################################################

set -euo pipefail

# Color codes for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color

# Cache variables
_ORCHESTRATION_ENABLED_CACHE=""
_ORCHESTRATION_CACHE_SET=false

# Debug flag - export _ORCHESTRATION_DEBUG=1 to enable debug output
_ORCHESTRATION_DEBUG="${_ORCHESTRATION_DEBUG:-0}"

################################################################################
# Private Helper Functions
################################################################################

# Check if environment variable disables orchestration
_check_environment_variable() {
    if [[ "${ORCHESTRATION_DISABLED:-}" == "true" ]]; then
        [[ $_ORCHESTRATION_DEBUG == "1" ]] && echo "Orchestration disabled by environment variable ORCHESTRATION_DISABLED" >&2
        return 1  # Disabled
    fi
    return 0  # Enabled
}

# Check if marker file exists to disable orchestration
_check_marker_file() {
    if [[ -f ".orchestration-disabled" ]]; then
        [[ $_ORCHESTRATION_DEBUG == "1" ]] && echo "Orchestration disabled by marker file .orchestration-disabled" >&2
        return 1  # Disabled
    fi
    return 0  # Enabled
}

# Check if config file sets enabled=false
_check_config_file() {
    local config_file="config/orchestration-config.json"
    
    if [[ -f "$config_file" ]]; then
        # Use grep as a fallback in case jq is not available
        if grep -q '"enabled"[[:space:]]*:[[:space:]]*false' "$config_file" 2>/dev/null; then
            [[ $_ORCHESTRATION_DEBUG == "1" ]] && echo "Orchestration disabled by config file $config_file" >&2
            return 1  # Disabled
        fi
    fi
    return 0  # Enabled
}

# Internal function to check all disable signals
_check_all_signals() {
    # If ANY signal disables orchestration, return 1 (disabled)
    if ! _check_environment_variable || ! _check_marker_file || ! _check_config_file; then
        return 1  # Disabled
    fi
    
    # All checks passed - orchestration is enabled
    return 0
}

# Show debug information for all signals
_show_all_signals() {
    echo "${BLUE}[DEBUG]${NC} Orchestration Control Signal Status:"
    
    if _check_environment_variable; then
        echo "  Environment Variable: ${GREEN}ENABLED${NC}"
    else
        echo "  Environment Variable: ${RED}DISABLED${NC}"
    fi
    
    if _check_marker_file; then
        echo "  Marker File: ${GREEN}ENABLED${NC}"
    else
        echo "  Marker File: ${RED}DISABLED${NC}"
    fi
    
    if _check_config_file; then
        echo "  Config File: ${GREEN}ENABLED${NC}"
    else
        echo "  Config File: ${RED}DISABLED${NC}"
    fi
}

################################################################################
# Public API Functions
################################################################################

# Main function to check if orchestration is enabled
# Returns 0 (success) if enabled, 1 (failure) if disabled
is_orchestration_enabled() {
    # Use cached value if available
    if [[ "$_ORCHESTRATION_CACHE_SET" == "true" ]]; then
        if [[ "$_ORCHESTRATION_ENABLED_CACHE" == "true" ]]; then
            return 0  # Enabled
        else
            return 1  # Disabled
        fi
    fi
    
    # Check all signals and cache the result
    if _check_all_signals; then
        _ORCHESTRATION_ENABLED_CACHE="true"
        _ORCHESTRATION_CACHE_SET=true
        return 0  # Enabled
    else
        _ORCHESTRATION_ENABLED_CACHE="false"
        _ORCHESTRATION_CACHE_SET=true
        return 1  # Disabled
    fi
}

# Get orchestration status as a message
get_orchestration_status() {
    if is_orchestration_enabled; then
        echo "Orchestration: ${GREEN}ENABLED ✓${NC}"
    else
        echo "Orchestration: ${RED}DISABLED ✗${NC}"
    fi
}

# Assert orchestration is enabled (returns 1 if disabled)
assert_orchestration_enabled() {
    if is_orchestration_enabled; then
        return 0  # Enabled, continue
    else
        echo "Error: Orchestration is required but disabled" >&2
        return 1  # Disabled
    fi
}

# Skip if orchestration is disabled (returns 0 if disabled)
skip_if_orchestration_disabled() {
    if is_orchestration_enabled; then
        return 0  # Enabled, don't skip
    else
        return 1  # Disabled, skip
    fi
}

# Reset the orchestration status cache
reset_orchestration_cache() {
    _ORCHESTRATION_ENABLED_CACHE=""
    _ORCHESTRATION_CACHE_SET=false
}

# Function to run as script (for testing)
_run_as_script() {
    if [[ $_ORCHESTRATION_DEBUG == "1" ]]; then
        _show_all_signals
    fi
    
    if is_orchestration_enabled; then
        echo "true"
        return 0
    else
        echo "false"
        return 1
    fi
}

# Export functions for use in other scripts
export -f is_orchestration_enabled
export -f get_orchestration_status
export -f assert_orchestration_enabled
export -f skip_if_orchestration_disabled
export -f reset_orchestration_cache

################################################################################
# Run if called as script (for testing)
################################################################################
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    _run_as_script
fi