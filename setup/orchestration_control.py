"""
Centralized Orchestration Control Module

This module provides a single point of control for enabling/disabling orchestration.
Other code should NOT check for ORCHESTRATION_DISABLED directly.
Instead, import is_orchestration_enabled() and call it.

This keeps all orchestration control logic localized and allows other branches
to remain agnostic to the disable/enable mechanism.

Design:
- Checks multiple disable signals (env var, marker file, config file)
- Caches result for performance
- Single source of truth for orchestration status
- Branch code only imports is_orchestration_enabled()
"""

import os
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# Cache for orchestration status (None = not checked yet)
_orchestration_enabled: Optional[bool] = None


def _check_environment_variable() -> bool:
    """Check if orchestration is disabled via environment variable."""
    return os.getenv('ORCHESTRATION_DISABLED', '').lower() != 'true'


def _check_marker_file() -> bool:
    """Check if orchestration is disabled via marker file."""
    marker_path = Path('.orchestration-disabled')
    return not marker_path.exists()


def _check_config_file() -> bool:
    """Check if orchestration is disabled via config file."""
    config_path = Path('config/orchestration-config.json')
    
    if not config_path.exists():
        return True  # Default: enabled if no config
    
    try:
        import json
        with open(config_path) as f:
            config = json.load(f)
            return config.get('enabled', True)
    except Exception as e:
        logger.warning(f"Error reading orchestration config: {e}")
        return True  # Default: enabled on error


def is_orchestration_enabled() -> bool:
    """
    Check if orchestration workflows are enabled.
    
    This is the ONLY function other code should use to check orchestration status.
    
    Checks three disable signals in order:
    1. Environment variable ORCHESTRATION_DISABLED=true
    2. Marker file .orchestration-disabled exists
    3. Configuration file config/orchestration-config.json enabled=false
    
    Returns:
        bool: True if orchestration is enabled, False if disabled
    
    Examples:
        >>> if is_orchestration_enabled():
        ...     run_orchestration_workflows()
        >>> else:
        ...     logger.info("Orchestration disabled, skipping workflows")
    """
    global _orchestration_enabled
    
    # Return cached value if already checked
    if _orchestration_enabled is not None:
        return _orchestration_enabled
    
    # Check all disable signals
    env_enabled = _check_environment_variable()
    marker_enabled = _check_marker_file()
    config_enabled = _check_config_file()
    
    # All must be true for orchestration to be enabled
    # (any "disabled" signal disables orchestration)
    _orchestration_enabled = env_enabled and marker_enabled and config_enabled
    
    if not _orchestration_enabled:
        logger.info("Orchestration is DISABLED")
        if not env_enabled:
            logger.debug("  Reason: ORCHESTRATION_DISABLED environment variable")
        if not marker_enabled:
            logger.debug("  Reason: .orchestration-disabled marker file exists")
        if not config_enabled:
            logger.debug("  Reason: orchestration disabled in config file")
    
    return _orchestration_enabled


def reset_cache():
    """
    Reset the orchestration status cache.
    
    Useful for testing or if the disable status changes at runtime.
    """
    global _orchestration_enabled
    _orchestration_enabled = None


def get_orchestration_status_summary() -> dict:
    """
    Get detailed status of all orchestration disable signals.
    
    Returns:
        dict: Status of each disable signal
    
    Example:
        >>> status = get_orchestration_status_summary()
        >>> print(f"Orchestration enabled: {status['enabled']}")
        >>> for signal, active in status['signals'].items():
        ...     print(f"  {signal}: {'DISABLED' if not active else 'enabled'}")
    """
    return {
        'enabled': is_orchestration_enabled(),
        'signals': {
            'environment_variable': _check_environment_variable(),
            'marker_file': _check_marker_file(),
            'config_file': _check_config_file(),
        }
    }


# Utility functions for the control scripts

def enable_orchestration():
    """
    Enable orchestration by clearing all disable signals.
    
    Called by enable-all-orchestration.sh
    """
    reset_cache()
    # Note: Actual enable logic is in the shell scripts
    # This is just for documentation and potential Python-based enable
    logger.info("Orchestration enable requested (actual setup in shell scripts)")


def disable_orchestration():
    """
    Disable orchestration by setting disable signals.
    
    Called by disable-all-orchestration.sh
    """
    reset_cache()
    # Note: Actual disable logic is in the shell scripts
    # This is just for documentation and potential Python-based disable
    logger.info("Orchestration disable requested (actual setup in shell scripts)")


if __name__ == '__main__':
    # Test this module
    print("Orchestration Control Module Test")
    print("=" * 50)
    
    status = get_orchestration_status_summary()
    print(f"Orchestration Enabled: {status['enabled']}")
    print("\nSignals:")
    for signal, active in status['signals'].items():
        state = "✓ ACTIVE" if active else "✗ DISABLED"
        print(f"  {signal}: {state}")
    
    print("\nUsage in code:")
    print("  from setup.orchestration_control import is_orchestration_enabled")
    print("  if is_orchestration_enabled():")
    print("      run_orchestration()")
