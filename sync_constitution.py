#!/usr/bin/env python3
"""
Constitution Synchronization Script

This script synchronizes the enhanced constitution file across all repositories
in the Email Intelligence Platform to ensure consistency in development practices.

The script copies the master constitution file from the EmailIntelligence repository
to all other repositories that contain constitution files.
"""

import os
import shutil
import sys
from pathlib import Path


def get_constitution_paths(base_dir):
    """Get all constitution file paths in the project."""
    constitution_files = []
    
    # Look for constitution files in all subdirectories
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.lower() == "constitution.md":
                constitution_files.append(os.path.join(root, file))
    
    return constitution_files


def sync_constitution_files(base_dir, master_constitution_path):
    """Synchronize constitution files across all repositories."""
    constitution_files = get_constitution_paths(base_dir)
    
    # Read the master constitution content
    with open(master_constitution_path, 'r', encoding='utf-8') as f:
        master_content = f.read()
    
    updated_files = []
    for constitution_path in constitution_files:
        # Skip the master file itself
        if os.path.abspath(constitution_path) == os.path.abspath(master_constitution_path):
            continue
        
        # Read current content to check if update is needed
        with open(constitution_path, 'r', encoding='utf-8') as f:
            current_content = f.read()
        
        # Only update if content is different
        if current_content != master_content:
            # Create backup
            backup_path = constitution_path + '.backup'
            shutil.copy2(constitution_path, backup_path)
            
            # Write new content
            with open(constitution_path, 'w', encoding='utf-8') as f:
                f.write(master_content)
            
            updated_files.append(constitution_path)
            print(f"Updated: {constitution_path}")
            print(f"  Backup created: {backup_path}")
        else:
            print(f"Already up to date: {constitution_path}")
    
    return updated_files


def main():
    """Main function to execute the synchronization."""
    if len(sys.argv) > 1:
        base_directory = sys.argv[1]
    else:
        base_directory = os.getcwd()
    
    # Define the master constitution file path
    # Using the one we created in the EmailIntelligence directory
    master_constitution = os.path.join(base_directory, "EmailIntelligence", "constitution.md")
    
    # Check if master constitution exists
    if not os.path.exists(master_constitution):
        print(f"Error: Master constitution file not found at {master_constitution}")
        # Try alternative location
        master_constitution = os.path.join(base_directory, "enhanced_constitution.md")
        if not os.path.exists(master_constitution):
            print(f"Error: Master constitution file not found at {master_constitution}")
            sys.exit(1)
        else:
            print(f"Using enhanced constitution file from: {master_constitution}")
    else:
        print(f"Using master constitution file from: {master_constitution}")
    
    print(f"Base directory: {base_directory}")
    
    # Synchronize all constitution files
    updated_files = sync_constitution_files(base_directory, master_constitution)
    
    if updated_files:
        print(f"\nSuccessfully updated {len(updated_files)} constitution files:")
        for file_path in updated_files:
            print(f"  - {file_path}")
        print("\nSynchronization completed with updates.")
    else:
        print("\nAll constitution files were already up to date.")
        print("Synchronization completed without updates.")


if __name__ == "__main__":
    main()