#!/bin/bash
# Script to demonstrate proper subtree integration for main branch

# This script shows the proper way to integrate the setup subtree into the main branch
# It assumes that the setup directory exists as a separate branch or repository

# Step 1: Add the setup subtree from launch-setup-fixes branch
# git subtree add --prefix=setup origin/launch-setup-fixes --squash

# Step 2: After the subtree is established, to pull updates from the setup branch:
# git subtree pull --prefix=setup origin/launch-setup-fixes --squash

# Step 3: If you want to push changes from the main branch back to the setup branch:
# git subtree push --prefix=setup origin launch-setup-fixes

echo "This script documents the proper git subtree process for main branch integration."
echo ""
echo "The setup directory contains the launch and setup files that should be shared across branches."
echo "This allows the main and scientific branches to diverge while still sharing common launch infrastructure."