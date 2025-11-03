#!/bin/bash
# Install essential scripts to code worktrees
# Run from launch-setup-fixes

# List of scripts to install
scripts=("validate_setup.sh" "organize_docs.sh" "sync_setup_worktrees.sh")

for repo in ../EmailIntelligenceGem ../EmailIntelligenceAuto ../EmailIntelligenceQwen; do
  if [[ -d "$repo" ]]; then
    echo "Installing scripts to $repo"
    mkdir -p "$repo/scripts"
    for script in "${scripts[@]}"; do
      cp "scripts/$script" "$repo/scripts/"
      chmod +x "$repo/scripts/$script"
    done
  fi
done

echo "Script installation complete."
