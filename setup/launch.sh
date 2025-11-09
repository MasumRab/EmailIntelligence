#!/bin/bash
# EmailIntelligence Launcher for Linux/macOS
# This script is a wrapper that forwards to the actual launch.sh in the setup subtree
# It maintains backward compatibility for references to launch.sh in the root directory

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Execute the actual launch.sh in the setup subtree with all arguments
exec "$SCRIPT_DIR/setup/launch.sh" "$@"# Test push
# Another test line
