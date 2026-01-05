#!/bin/bash
# Centralized Orchestration Control Module (Shell Version)
#
# This library provides a single point of control for enabling/disabling orchestration.
# Other scripts should NOT check for ORCHESTRATION_DISABLED directly.
# Instead, source this file and use is_orchestration_enabled()
#
# This keeps all orchestration control logic localized and allows other branches
# to remain agnostic to the disable/enable mechanism.

# Source common utilities if available
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f "$SCRIPT_DIR/common.sh" ]]; then
    source "$SCRIPT_DIR/common.sh"
fi

# Cache variable (unset = not checked yet)
_ORCHESTRATION_ENABLED_CACHE=""

# ============================================================================
# PUBLIC API - Scripts should only use these functions
# ============================================================================

#
# is_orchestration_enabled()
#
# Check if orchestration workflows are enabled.
# This is the ONLY function other scripts should use.
#
# Returns: 0 if enabled, 1 if disabled
#
# Usage:
#   if is_orchestration_enabled; then
#       run_orchestration_workflows
#   else
#       echo "Orchestration disabled"
#   fi
#
is_orchestration_enabled() {
    # Return cached value if already checked
    if [[ -n "$_ORCHESTRATION_ENABLED_CACHE" ]]; then
        [[ "$_ORCHESTRATION_ENABLED_CACHE" == "true" ]]
        return $?
    fi
    
    # Check all disable signals
    local env_enabled=true
    local marker_enabled=true
    local config_enabled=true
    
    # Check environment variable
    if [[ "${ORCHESTRATION_DISABLED}" == "true" ]]; then
        env_enabled=false
    fi
    
    # Check marker file
    if [[ -f ".orchestration-disabled" ]]; then
        marker_enabled=false
    fi
    
    # Check config file (basic check, requires jq for full parsing)
    if [[ -f "config/orchestration-config.json" ]]; then
        if command -v jq &> /dev/null; then
            local config_value
            config_value=$(jq -r '.enabled' config/orchestration-config.json 2>/dev/null)
            if [[ "$config_value" != "true" ]]; then
                config_enabled=false
            fi
        fi
    fi
    
    # All must be true for orchestration to be enabled
    if [[ "$env_enabled" == "true" && "$marker_enabled" == "true" && "$config_enabled" == "true" ]]; then
        _ORCHESTRATION_ENABLED_CACHE="true"
        return 0  # Enabled
    else
        _ORCHESTRATION_ENABLED_CACHE="false"
        
        # Log why it's disabled
        if [[ "$env_enabled" == "false" ]]; then
            [[ -n "$_ORCHESTRATION_DEBUG" ]] && echo "[ORCH-CONTROL] Disabled: ORCHESTRATION_DISABLED env var" >&2
        fi
        if [[ "$marker_enabled" == "false" ]]; then
            [[ -n "$_ORCHESTRATION_DEBUG" ]] && echo "[ORCH-CONTROL] Disabled: .orchestration-disabled marker file" >&2
        fi
        if [[ "$config_enabled" == "false" ]]; then
            [[ -n "$_ORCHESTRATION_DEBUG" ]] && echo "[ORCH-CONTROL] Disabled: config file setting" >&2
        fi
        
        return 1  # Disabled
    fi
}

#
# reset_orchestration_cache()
#
# Reset the orchestration status cache.
# Useful for testing or if disable status changes at runtime.
#
reset_orchestration_cache() {
    _ORCHESTRATION_ENABLED_CACHE=""
}

#
# get_orchestration_status()
#
# Get human-readable status of orchestration.
#
# Usage:
#   get_orchestration_status
#   # Outputs: "Orchestration: ENABLED" or "Orchestration: DISABLED"
#
get_orchestration_status() {
    if is_orchestration_enabled; then
        echo "Orchestration: ENABLED ✓"
        return 0
    else
        echo "Orchestration: DISABLED ✗"
        return 1
    fi
}

#
# assert_orchestration_enabled()
#
# Assert that orchestration is enabled, exit if not.
# Used by orchestration-dependent scripts.
#
# Usage:
#   assert_orchestration_enabled || return 1  # Soft fail
#   assert_orchestration_enabled             # Hard exit
#
assert_orchestration_enabled() {
    if ! is_orchestration_enabled; then
        echo "ERROR: Orchestration is disabled" >&2
        echo "To enable, run: ./scripts/enable-all-orchestration.sh" >&2
        return 1
    fi
    return 0
}

#
# skip_if_orchestration_disabled()
#
# Early return if orchestration is disabled.
# Cleaner syntax for optional orchestration features.
#
# Usage:
#   skip_if_orchestration_disabled || return 0
#   # Rest of orchestration code
#
skip_if_orchestration_disabled() {
    if ! is_orchestration_enabled; then
        return 1  # True = skip
    fi
    return 0  # False = continue
}

# ============================================================================
# TESTING & DEBUGGING
# ============================================================================

#
# Internal function: Show all disable signals
# Only used for debugging (set _ORCHESTRATION_DEBUG=1)
#
_show_all_signals() {
    echo "[ORCH-CONTROL] Status check:"
    
    # Environment variable
    if [[ "${ORCHESTRATION_DISABLED}" == "true" ]]; then
        echo "  ORCHESTRATION_DISABLED: true (DISABLED)"
    else
        echo "  ORCHESTRATION_DISABLED: not set (enabled)"
    fi
    
    # Marker file
    if [[ -f ".orchestration-disabled" ]]; then
        echo "  .orchestration-disabled: EXISTS (DISABLED)"
    else
        echo "  .orchestration-disabled: not found (enabled)"
    fi
    
    # Config file
    if [[ -f "config/orchestration-config.json" ]]; then
        echo "  config/orchestration-config.json: EXISTS"
        if command -v jq &> /dev/null; then
            jq '.enabled' config/orchestration-config.json 2>/dev/null || echo "    (parse error)"
        else
            echo "    (jq not available to parse)"
        fi
    else
        echo "  config/orchestration-config.json: not found (enabled by default)"
    fi
    
    # Overall status
    if is_orchestration_enabled; then
        echo "  OVERALL: ENABLED ✓"
    else
        echo "  OVERALL: DISABLED ✗"
    fi
}

# ============================================================================
# SELF-TEST
# ============================================================================

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    # Script is being run directly (not sourced)
    echo "Orchestration Control Module (Shell) - Self Test"
    echo "=================================================="
    echo ""
    
    export _ORCHESTRATION_DEBUG=1
    
    if is_orchestration_enabled; then
        echo "✓ Orchestration is ENABLED"
    else
        echo "✗ Orchestration is DISABLED"
    fi
    
    echo ""
    echo "Details:"
    _show_all_signals
    
    echo ""
    echo "Usage in scripts:"
    echo '  source scripts/lib/orchestration-control.sh'
    echo "  if is_orchestration_enabled; then"
    echo "      echo 'Running orchestration'"
    echo "  fi"
fi
