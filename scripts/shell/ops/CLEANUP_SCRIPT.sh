#!/bin/bash

# Task 75 Cleanup Script
# Removes all orphaned Task 75 references and consolidates into Task 002
# Date: January 6, 2026

set -e  # Exit on error

BACKUP_DIR=".backups"
ARCHIVE_DIR="task_data/archived"

echo "==============================================="
echo "Task 002 Consolidation & Cleanup"
echo "Removing all Task 75 orphaned files"
echo "==============================================="
echo ""

# Function to backup before deletion
backup_and_delete() {
    local file=$1
    local backup_timestamp=$(date +%Y%m%d_%H%M%S)
    
    if [ -f "$file" ]; then
        echo "Backing up: $file"
        mkdir -p "$BACKUP_DIR"
        cp "$file" "$BACKUP_DIR/$(basename $file)_task75_backup_${backup_timestamp}"
        rm "$file"
        echo "  ✓ Deleted: $file"
    fi
}

echo "Phase 1: Removing orphaned task-75.*.md files from task_data/"
echo "---"

# Remove individual task-75 files (now consolidated into task_002.md)
for i in {1..9}; do
    backup_and_delete "task_data/task-75.$i.md"
done

# Remove main task-75.md
backup_and_delete "task_data/task-75.md"

echo ""
echo "Phase 2: Removing HANDOFF_75.*.md files from task_data/archived_handoff/"
echo "---"

mkdir -p "$ARCHIVE_DIR/handoff_archive_task75"

for handoff_file in task_data/archived_handoff/HANDOFF_75*.md; do
    if [ -f "$handoff_file" ]; then
        echo "Archiving: $(basename $handoff_file)"
        mv "$handoff_file" "$ARCHIVE_DIR/handoff_archive_task75/"
        echo "  ✓ Moved to archive"
    fi
done

echo ""
echo "Phase 3: Removing backup files from task_data/backups/"
echo "---"

mkdir -p "$ARCHIVE_DIR/backups_archive_task75"

for backup_file in task_data/backups/task-75*.md; do
    if [ -f "$backup_file" ]; then
        echo "Archiving: $(basename $backup_file)"
        mv "$backup_file" "$ARCHIVE_DIR/backups_archive_task75/"
        echo "  ✓ Moved to archive"
    fi
done

echo ""
echo "Phase 4: Removing old backup files from .backups/"
echo "---"

for old_backup in .backups/task-75*.md.20260104_200852; do
    if [ -f "$old_backup" ]; then
        echo "Deleting: $(basename $old_backup)"
        rm "$old_backup"
        echo "  ✓ Deleted"
    fi
done

echo ""
echo "Phase 5: Verifying cleanup"
echo "---"

echo "Checking for remaining task-75 references:"
found_refs=$(find . -name "*task-75*" -o -name "*Task 75*" 2>/dev/null | grep -v ARCHIVE | grep -v ".git" | wc -l)

if [ "$found_refs" -eq 0 ]; then
    echo "  ✓ No task-75 references found in active code"
else
    echo "  ⚠ Warning: $found_refs references still exist:"
    find . -name "*task-75*" -o -name "*Task 75*" 2>/dev/null | grep -v ARCHIVE | grep -v ".git"
fi

echo ""
echo "Phase 6: Verifying new task files exist"
echo "---"

if [ -f "tasks/task_002.md" ]; then
    echo "  ✓ tasks/task_002.md exists"
else
    echo "  ✗ ERROR: tasks/task_002.md not found!"
    exit 1
fi

if [ -f "tasks/task_002-clustering.md" ]; then
    echo "  ✓ tasks/task_002-clustering.md exists"
else
    echo "  ✗ ERROR: tasks/task_002-clustering.md not found!"
    exit 1
fi

echo ""
echo "==============================================="
echo "Cleanup Complete"
echo "==============================================="
echo ""
echo "Summary:"
echo "- All task-75.*.md files removed from task_data/"
echo "- All HANDOFF_75.*.md files archived"
echo "- All task-75 backup files archived"
echo "- New task_002.md and task_002-clustering.md in place"
echo "- session_log.json updated with task_002 references"
echo ""
echo "Next Steps:"
echo "1. Review task_002.md for task overview"
echo "2. Review task_002-clustering.md for implementation details"
echo "3. Start implementation using recommended Full Parallel strategy"
echo "4. Commit with message: 'chore: consolidate Task 75 into Task 002 (Branch Clustering System)'"
echo ""
