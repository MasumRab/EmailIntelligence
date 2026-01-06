#!/bin/bash

# Determine the project root (by finding the .git directory)
# This script assumes it's run from within a git repository.
PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)

if [ -z "$PROJECT_ROOT" ]; then
    echo "Error: Not in a git repository. Cannot determine project root." >&2
    echo "Please run this script from within your project's git repository." >&2
    return 1 # Use 'return' for sourcing, 'exit' for direct execution
fi

echo "Setting up agent environment for project: $PROJECT_ROOT" >&2

# Path to the config_manager.py script
CONFIG_MANAGER_SCRIPT="$PROJECT_ROOT/scripts/config_manager.py"

if [ ! -f "$CONFIG_MANAGER_SCRIPT" ]; then
    echo "Error: config_manager.py not found at $CONFIG_MANAGER_SCRIPT" >&2
    echo "Please ensure config_manager.py exists in your project's scripts/ directory." >&2
    return 1
fi

# Execute config_manager.py to get environment variables and generate tool-specific configs
# 'eval' is used to apply the 'export' commands to the current shell session.
eval "$(python3 "$CONFIG_MANAGER_SCRIPT" --project-root "$PROJECT_ROOT" --output-env)"

# Generate tool-specific configuration files
python3 "$CONFIG_MANAGER_SCRIPT" --project-root "$PROJECT_ROOT" --generate-tool-configs >&2

echo "Agent environment setup complete. Environment variables exported and tool configs generated." >&2
echo "To verify, you can run 'env | grep API_KEY' or check your .gemini/config.json file." >&2
