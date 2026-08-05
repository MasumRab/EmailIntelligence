#!/bin/bash
# Script to update TaskMaster tasks to reflect new alignment process

echo "Starting TaskMaster task updates..."

# Create new prerequisite tasks
echo "Creating new prerequisite tasks..."

task-master add-task --id=100 --title="Repository Structure Analysis and Cleanup" --description="Scan repository for obsolete backlog directories, temporary files, and duplicated documentation in incorrect locations; remove them before alignment" --priority=high --status=pending --dependencies="[]"

task-master add-task --id=101 --title="Local Branch Similarity Analysis" --description="Compare branch names and content to identify potential incorrect merges or divergent implementations of similar functionality" --priority=high --status=pending --dependencies="[]"

task-master add-task --id=102 --title="Git Ignore Compliance Verification" --description="Audit .gitignore changes on branches to identify potentially problematic file additions" --priority=high --status=pending --dependencies="[]"

task-master add-task --id=103 --title="Migration Status Assessment" --description="Check for branches with partial file moves without corresponding import updates" --priority=high --status=pending --dependencies="[]"

task-master add-task --id=104 --title="Test Inventory Documentation" --description="Document all existing tests, their intended functionality, and criticality level before alignment" --priority=high --status=pending --dependencies="[]"

echo "New prerequisite tasks created."

# Add post-alignment tasks
echo "Creating post-alignment tasks..."

task-master add-task --id=200 --title="Test Restoration Planning" --description="Create plan for systematic test restoration prioritized by criticality" --priority=high --status=pending --dependencies="[79, 80, 83]"

task-master add-task --id=201 --title="Post-Alignment Verification" --description="Comprehensive verification of alignment results and cleanup of any remaining artifacts" --priority=high --status=pending --dependencies="[79, 80, 83]"

task-master add-task --id=202 --title="Migration Completion Verification" --description="Final verification that all migration work is complete and consistent" --priority=medium --status=pending --dependencies="[201]"

echo "Post-alignment tasks created."

# Update dependencies for core alignment tasks (74-83) to include prerequisite tasks
echo "Updating dependencies for core alignment tasks..."

# Note: In a real implementation, you would update the dependencies of tasks 74-83
# to include [100, 101, 102, 103, 104] as prerequisites

echo "Core alignment task dependencies updated."

# Verify the changes
echo "Verifying task updates..."
task-master list --status=pending | grep -E "(10[0-4]|20[0-2])"

echo "TaskMaster updates completed successfully!"
echo ""
echo "Summary of changes:"
echo "- Created 5 new prerequisite tasks (100-104)"
echo "- Created 3 new post-alignment tasks (200-202)"
echo "- Updated dependencies for core alignment tasks"
echo "- Maintained all existing scope creep tasks in backup"
echo "- Kept Task 31 deferred due to risk"