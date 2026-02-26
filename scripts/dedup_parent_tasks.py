#!/usr/bin/env python3
"""Clean up parent task files by removing trailing junk after the 14-section standard.

This script:
1. Identifies the 14 canonical sections in each parent task file
2. Removes everything after the "## Next Steps" section that isn't part of the standard
3. Strips trailing metadata duplicates, Progress Log, DEPENDENCY GRAPH, etc.
4. Removes empty EXTENDED_METADATA blocks
5. Cleans up trailing blank lines and horizontal rules

Usage:
    python scripts/dedup_parent_tasks.py --dry-run     # Preview changes
    python scripts/dedup_parent_tasks.py                # Apply changes
"""

import argparse
import glob
import os
import re
import sys

TASKS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tasks")

# The 14 canonical section headings (## level)
CANONICAL_SECTIONS = [
    "## Overview/Purpose",
    "## Purpose",
    "## Overview",
    "## Success Criteria",
    "## Prerequisites & Dependencies",
    "## Prerequisites",
    "## Sub-subtasks Breakdown",
    "## Sub-subtasks",
    "## Subtasks Breakdown",
    "## Subtasks",
    "## Specification Details",
    "## Specification",
    "## Implementation Guide",
    "## Implementation",
    "## Configuration Parameters",
    "## Configuration & Defaults",
    "## Configuration",
    "## Performance Targets",
    "## Testing Strategy",
    "## Test Strategy",
    "## Common Gotchas & Solutions",
    "## Common Gotchas",
    "## Integration Checkpoint",
    "## Done Definition",
    "## Next Steps",
]

# Sections that should be REMOVED (non-canonical trailing junk)
JUNK_SECTIONS = [
    "## Progress Log",
    "## DEPENDENCY GRAPH",
    "## Architecture Overview",
    "## Integration with Task",
    "## Checklist",
    "## What to Build",
    "## 3 Execution Options",
    "## 5-Step Implementation Plan",
    "## Task-Specific Quick References",
    "## Key Success Metrics",
    "## Documentation Resources",
    "## Get Started Now",
    "## Getting Help",
    "## Executive Summary",
    "## What Was Done",
    "## New Task Structure",
    "## Quick Start for Implementation",
    "## File Mapping Reference",
    "## Verification Checklist",
    "## Key Metrics",
    "## Deferred Tasks",
    "## Troubleshooting This Migration",
    "## Success Definition",
    "## Document References",
    "## Guidance & Standards",
    "## Typical Development Workflow",
]


def is_canonical(heading):
    """Check if a ## heading is a canonical section."""
    heading_stripped = heading.strip()
    for canonical in CANONICAL_SECTIONS:
        if heading_stripped == canonical or heading_stripped.startswith(canonical):
            return True
    return False


def is_junk(heading):
    """Check if a ## heading is a known junk section."""
    heading_stripped = heading.strip()
    for junk in JUNK_SECTIONS:
        if heading_stripped == junk or heading_stripped.startswith(junk):
            return True
    return False


def extract_task_id(filepath):
    """Extract task ID from filename like task_001.md."""
    basename = os.path.basename(filepath)
    m = re.match(r"task_(\d+)\.md$", basename)
    if m:
        return m.group(1)
    return None


def find_next_steps_end(lines):
    """Find where the ## Next Steps section ends (before any trailing junk)."""
    in_next_steps = False
    next_steps_start = -1
    next_steps_end = -1

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == "## Next Steps":
            in_next_steps = True
            next_steps_start = i
            continue
        if in_next_steps and stripped.startswith("## "):
            # Found the next section after Next Steps
            next_steps_end = i
            break

    if in_next_steps and next_steps_end == -1:
        # Next Steps is the last section - find the content end
        # Walk backwards from end to find last non-blank, non-hr line
        for i in range(len(lines) - 1, next_steps_start, -1):
            stripped = lines[i].strip()
            if stripped and stripped != "---":
                next_steps_end = i + 1
                break

    return next_steps_start, next_steps_end


def clean_file(filepath, dry_run=False):
    """Clean a parent task file by removing trailing junk sections."""
    task_id = extract_task_id(filepath)
    if task_id is None:
        return None

    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    lines = content.split("\n")
    original_line_count = len(lines)

    # Find all ## headings and their line numbers
    headings = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("## ") and not stripped.startswith("### "):
            headings.append((i, stripped))

    # Find which headings are junk (after Next Steps or not canonical)
    next_steps_idx = None
    for i, (line_num, heading) in enumerate(headings):
        if heading == "## Next Steps":
            next_steps_idx = i
            break

    if next_steps_idx is None:
        return {"task_id": task_id, "filepath": filepath, "action": "skip", "reason": "no Next Steps section"}

    # Everything after Next Steps that isn't canonical is junk
    junk_ranges = []
    for i in range(next_steps_idx + 1, len(headings)):
        line_num, heading = headings[i]
        if is_junk(heading) or not is_canonical(heading):
            # Find end of this junk section
            if i + 1 < len(headings):
                end_line = headings[i + 1][0]
            else:
                end_line = len(lines)
            junk_ranges.append((line_num, end_line, heading))

    # Also check for trailing metadata duplicates (lines starting with **Status:** etc after Next Steps)
    next_steps_line = headings[next_steps_idx][0]

    # Find end of Next Steps content (before junk)
    if junk_ranges:
        first_junk_line = junk_ranges[0][0]
    else:
        first_junk_line = len(lines)

    # Find actual Next Steps content end
    content_end = first_junk_line
    # Walk backwards to remove trailing blank lines and --- before junk
    while content_end > next_steps_line and lines[content_end - 1].strip() in ("", "---"):
        content_end -= 1
    content_end += 1  # Keep one blank line

    # Also remove EXTENDED_METADATA empty blocks anywhere in the file
    cleaned_lines = lines[:content_end]

    # Remove empty EXTENDED_METADATA blocks
    new_lines = []
    skip_until_end = False
    for line in cleaned_lines:
        if "<!-- EXTENDED_METADATA" in line:
            skip_until_end = True
            continue
        if skip_until_end and "END_EXTENDED_METADATA -->" in line:
            skip_until_end = False
            continue
        if skip_until_end:
            continue
        new_lines.append(line)

    # Find the Next Steps heading and trim trailing junk WITHIN the Next Steps section
    # (### Blocks, ### External Dependencies, orphaned metadata lines)
    final_lines = []
    in_next_steps = False
    next_steps_content_ended = False
    for i, line in enumerate(new_lines):
        stripped = line.strip()

        if stripped == "## Next Steps":
            in_next_steps = True
            next_steps_content_ended = False
            final_lines.append(line)
            continue

        if in_next_steps:
            # Detect orphaned metadata fields (Status, Priority, etc.)
            if re.match(r"^-?\s*\*\*(Status|Priority|Effort|Complexity|Dependencies)\*\*:", stripped):
                continue  # Skip orphaned metadata
            # Detect trailing ### subsections that don't belong
            if stripped.startswith("### Blocks") or stripped.startswith("### External Dependencies"):
                next_steps_content_ended = True
                continue
            if next_steps_content_ended:
                # Skip everything after we've seen trailing subsections
                if stripped and not stripped.startswith("## "):
                    continue
                if stripped == "---":
                    continue
            # Detect **Reference:** lines as end of real content
            if stripped.startswith("**Reference:**"):
                # Include this line but mark content as ended after it
                final_lines.append(line)
                next_steps_content_ended = True
                continue

        final_lines.append(line)

    # Ensure file ends with a newline and ---
    while final_lines and final_lines[-1].strip() == "":
        final_lines.pop()
    if final_lines and final_lines[-1].strip() != "---":
        final_lines.append("")
        final_lines.append("---")
    final_lines.append("")

    new_content = "\n".join(final_lines)
    new_line_count = len(final_lines)
    reduction = original_line_count - new_line_count

    result = {
        "task_id": task_id,
        "filepath": filepath,
        "original_lines": original_line_count,
        "new_lines": new_line_count,
        "reduction": reduction,
        "junk_sections": [h for _, _, h in junk_ranges],
        "action": "cleaned" if reduction > 0 else "no_change",
    }

    if not dry_run and reduction > 0:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

    return result


def main():
    parser = argparse.ArgumentParser(description="Clean up parent task files")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing")
    parser.add_argument("--tasks-dir", default=TASKS_DIR, help="Path to tasks directory")
    parser.add_argument("--file", help="Process a single file instead of all")
    args = parser.parse_args()

    if args.file:
        task_files = [args.file]
    else:
        # Only process parent task files (no dot in the number part)
        task_files = sorted(glob.glob(os.path.join(args.tasks_dir, "task_0*.md")))
        # Filter to parent tasks only (task_NNN.md, not task_NNN.N.md)
        task_files = [f for f in task_files if re.match(r"task_\d+\.md$", os.path.basename(f))]

    if not task_files:
        print(f"No parent task files found in {args.tasks_dir}")
        sys.exit(1)

    total_reduction = 0
    cleaned_count = 0

    print("=" * 70)
    if args.dry_run:
        print("PARENT TASK CLEANUP - DRY RUN")
    else:
        print("PARENT TASK CLEANUP - APPLYING CHANGES")
    print("=" * 70)

    for fp in task_files:
        result = clean_file(fp, dry_run=args.dry_run)
        if result is None:
            continue

        if result["action"] == "cleaned":
            cleaned_count += 1
            total_reduction += result["reduction"]
            basename = os.path.basename(result["filepath"])
            print(f"  [{basename}] {result['original_lines']} → {result['new_lines']} lines (-{result['reduction']})")
            if result["junk_sections"]:
                for junk in result["junk_sections"]:
                    print(f"    ✗ Removed: {junk}")
        elif result["action"] == "skip":
            print(f"  [task_{result['task_id']}.md] SKIPPED: {result['reason']}")

    print()
    print(f"Files cleaned: {cleaned_count}")
    print(f"Total lines removed: {total_reduction}")
    if args.dry_run:
        print("\nRe-run without --dry-run to apply changes.")


if __name__ == "__main__":
    main()
