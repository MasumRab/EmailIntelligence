#!/usr/bin/env python3
"""Remove duplicate ## sections from subtask files.

Subtask files have repeated blocks (Progress Log, Next Steps, etc.) that
were copied during template expansion. This script keeps only the FIRST
occurrence of each ## heading and removes all subsequent duplicates.

Usage:
    python scripts/dedup_subtask_sections.py --dry-run   # Preview
    python scripts/dedup_subtask_sections.py              # Apply
"""

import argparse
import glob
import os
import re
import sys

TASKS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tasks")


def dedup_file(filepath, dry_run=False):
    """Remove duplicate ## sections, keeping only the first of each."""
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    original_count = len(lines)

    # Parse into sections: (heading_text, [lines including heading])
    sections = []
    current_heading = None
    current_lines = []

    for line in lines:
        stripped = line.rstrip("\n")
        if stripped.startswith("## ") and not stripped.startswith("### "):
            if current_heading is not None or current_lines:
                sections.append((current_heading, current_lines))
            current_heading = stripped
            current_lines = [line]
        else:
            current_lines.append(line)

    if current_heading is not None or current_lines:
        sections.append((current_heading, current_lines))

    # Keep only first occurrence of each ## heading
    seen_headings = set()
    kept_sections = []
    removed_headings = []

    for heading, section_lines in sections:
        if heading is None:
            # Preamble (before first ## heading) — always keep
            kept_sections.append(section_lines)
        elif heading not in seen_headings:
            seen_headings.add(heading)
            kept_sections.append(section_lines)
        else:
            removed_headings.append(heading)

    # Flatten
    new_lines = []
    for section_lines in kept_sections:
        new_lines.extend(section_lines)

    # Clean up trailing blank lines and ensure file ends with newline
    while new_lines and new_lines[-1].strip() == "":
        new_lines.pop()
    if new_lines and not new_lines[-1].endswith("\n"):
        new_lines[-1] += "\n"

    new_count = len(new_lines)
    reduction = original_count - new_count

    if not dry_run and reduction > 0:
        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

    return {
        "filepath": filepath,
        "original": original_count,
        "new": new_count,
        "reduction": reduction,
        "removed": removed_headings,
    }


def main():
    parser = argparse.ArgumentParser(description="Deduplicate ## sections in subtask files")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes")
    parser.add_argument("--tasks-dir", default=TASKS_DIR)
    args = parser.parse_args()

    # Only subtask files (have a dot in task ID: task_NNN.N.md)
    all_files = sorted(glob.glob(os.path.join(args.tasks_dir, "task_*.md")))
    subtask_files = [f for f in all_files if re.match(r"task_\d+\.\d+\.md$", os.path.basename(f))]

    if not subtask_files:
        print(f"No subtask files found in {args.tasks_dir}")
        sys.exit(1)

    total_reduction = 0
    cleaned = 0

    print("=" * 60)
    print("SUBTASK SECTION DEDUPLICATION" + (" — DRY RUN" if args.dry_run else ""))
    print("=" * 60)

    for fp in subtask_files:
        r = dedup_file(fp, dry_run=args.dry_run)
        if r["reduction"] > 0:
            cleaned += 1
            total_reduction += r["reduction"]
            basename = os.path.basename(r["filepath"])
            print(f"  [{basename}] {r['original']} → {r['new']} lines (-{r['reduction']})")

    print()
    print(f"Files cleaned: {cleaned}/{len(subtask_files)}")
    print(f"Total lines removed: {total_reduction}")
    if args.dry_run:
        print("\nRe-run without --dry-run to apply.")


if __name__ == "__main__":
    main()
