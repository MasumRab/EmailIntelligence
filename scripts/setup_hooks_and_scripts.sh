#!/bin/bash
# Setup hooks and scripts after pull

# Install hooks
cp scripts/hooks/* .git/hooks/ 2>/dev/null
chmod +x .git/hooks/* 2>/dev/null

# Ensure scripts are installed
bash scripts/install_branch_scripts.sh 2>/dev/null

echo "Hooks and scripts setup complete."
