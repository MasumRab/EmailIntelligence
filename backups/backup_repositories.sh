#!/bin/bash
# Backup script for all repositories

echo "Starting backup of all repositories..."

# Create timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# List of repositories to backup
REPOS=(
    "../EmailIntelligence"
    "../EmailIntelligenceAider"
    "../EmailIntelligenceAuto"
    "../EmailIntelligenceGem"
    "../EmailIntelligenceQwen"
    "../PR/EmailIntelligence"
    "../rulesync"
)

for repo in "${REPOS[@]}"; do
    if [ -d "$repo" ]; then
        echo "Backing up $repo..."
        cd "$repo"
        
        # Create a tar archive of the repository
        tar -czf "../../backups/$(basename $(pwd))_$TIMESTAMP.tar.gz" . --exclude=".git"
        
        cd - > /dev/null
    fi
done

echo "Backup completed at $(date)"