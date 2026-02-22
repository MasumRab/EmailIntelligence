#!/usr/bin/env python3
"""Audit task markdown files against the 14-section standard.

Checks all tasks/task_*.md files for compliance with TASK_STRUCTURE_STANDARD.md.
Parent tasks (no dot in ID) only require Purpose and Success Criteria.
Subtask files (dot in ID) require all 14 sections.

Usage:
    python scripts/check_section_compliance.py          # Show failures only
    python scripts/check_section_compliance.py --all     # Show all results
    python scripts/check_section_compliance.py --fix     # Add missing section stubs
"""

import argparse
import glob
import os
import re
import sys

TASKS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tasks")

# Section definitions: (section_number, canonical_name, list_of_accepted_heading_patterns)
# Section 1 (header) is checked separately via the # line.
# Sections 2-14 are ## headings.
SECTIONS = [
    (2, "Overview/Purpose", [
        "## Overview/Purpose",
        "## Purpose",
        "## Overview",
    ]),
    (3, "Success Criteria", [
        "## Success Criteria",
    ]),
    (4, "Prerequisites & Dependencies", [
        "## Prerequisites & Dependencies",
        "## Prerequisites",
    ]),
    (5, "Sub-subtasks Breakdown", [
        "## Sub-subtasks Breakdown",
        "## Sub-subtasks",
        "## Subtasks Breakdown",
        "## Subtasks",
    ]),
    (6, "Specification Details", [
        "## Specification Details",
        "## Specification",
    ]),
    (7, "Implementation Guide", [
        "## Implementation Guide",
        "## Implementation",
    ]),
    (8, "Configuration Parameters", [
        "## Configuration Parameters",
        "## Configuration & Defaults",
        "## Configuration",
    ]),
    (9, "Performance Targets", [
        "## Performance Targets",
    ]),
    (10, "Testing Strategy", [
        "## Testing Strategy",
        "## Test Strategy",
    ]),
    (11, "Common Gotchas & Solutions", [
        "## Common Gotchas & Solutions",
        "## Common Gotchas",
    ]),
    (12, "Integration Checkpoint", [
        "## Integration Checkpoint",
    ]),
    (13, "Done Definition", [
        "## Done Definition",
    ]),
    (14, "Next Steps", [
        "## Next Steps",
    ]),
]

# Bonus sections that should not be flagged as extra
BONUS_SECTIONS = [
    "## Provenance",
    "## Typical Development Workflow",
]

HEADER_METADATA_FIELDS = ["Status", "Priority", "Effort", "Complexity", "Dependencies"]

# Parent tasks only require these sections (by number)
PARENT_REQUIRED = {2, 3}  # Purpose and Success Criteria

# Stub templates for --fix
SECTION_STUBS = {
    2: "\n## Overview/Purpose\n\n[Overview to be defined]\n",
    3: "\n## Success Criteria\n\n- [ ] [Success criteria to be defined]\n",
    4: "\n## Prerequisites & Dependencies\n\n### Required Before Starting\n- [ ] None\n\n### Blocks (What This Task Unblocks)\n- [ ] To be defined\n\n### External Dependencies\n- [ ] No external dependencies\n",
    5: "\n## Sub-subtasks Breakdown\n\n[Sub-subtasks to be defined]\n",
    6: "\n## Specification Details\n\n[Specification to be defined]\n",
    7: "\n## Implementation Guide\n\n[Implementation guide to be defined]\n",
    8: "\n## Configuration Parameters\n\n[Configuration parameters to be defined]\n",
    9: "\n## Performance Targets\n\n[Performance targets to be defined]\n",
    10: "\n## Testing Strategy\n\n[Testing strategy to be defined]\n",
    11: "\n## Common Gotchas & Solutions\n\n[Common gotchas to be defined]\n",
    12: "\n## Integration Checkpoint\n\n- [ ] [Integration checkpoint to be defined]\n",
    13: "\n## Done Definition\n\n- [ ] [Done definition to be defined]\n",
    14: "\n## Next Steps\n\n[Next steps to be defined]\n",
}


def extract_task_id(filepath):
    """Extract task ID from filename like task_001.md or task_001.1.md."""
    basename = os.path.basename(filepath)
    # Match task_NNN.md (parent) or task_NNN.N.md / task_NNN.NN.md (subtask)
    m = re.match(r"task_(\d+(?:\.\d+)?)\.md$", basename)
    if m:
        return m.group(1)
    return None


def is_subtask(task_id):
    """Return True if task_id contains a dot (e.g., '001.1')."""
    return "." in task_id


def check_file(filepath):
    """Check a single task file for section compliance.

    Returns dict with:
        task_id, filepath, is_subtask, has_header, header_metadata_issues,
        present_sections (set of section numbers), missing_sections (list),
        passed (bool)
    """
    task_id = extract_task_id(filepath)
    if task_id is None:
        return None

    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    lines = content.split("\n")
    subtask = is_subtask(task_id)

    # --- Section 1: Header check ---
    has_header = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# ") and not stripped.startswith("## "):
            has_header = True
            break

    # --- Header metadata check ---
    header_metadata_issues = []
    for field in HEADER_METADATA_FIELDS:
        pattern = re.compile(rf"^\*\*{re.escape(field)}:\*\*\s*(.*)", re.MULTILINE)
        m = pattern.search(content)
        if not m:
            header_metadata_issues.append(f"{field}: missing")
        else:
            val = m.group(1).strip()
            if not val or val.upper() == "TBD":
                header_metadata_issues.append(f"{field}: TBD")

    # --- Sections 2-14 check ---
    # Collect all ## headings present in the file
    headings_in_file = set()
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## ") and not stripped.startswith("### "):
            headings_in_file.add(stripped)

    present_sections = set()
    for sec_num, _canonical, patterns in SECTIONS:
        for pat in patterns:
            if pat in headings_in_file:
                present_sections.add(sec_num)
                break

    # Determine required sections
    if subtask:
        required = set(range(2, 15))  # sections 2-14
    else:
        required = PARENT_REQUIRED

    # Also check header for subtasks
    missing_sections = []
    if subtask and not has_header:
        missing_sections.append("1: Task Header")

    for sec_num in sorted(required):
        if sec_num not in present_sections:
            # Find canonical name
            for sn, canonical, _ in SECTIONS:
                if sn == sec_num:
                    missing_sections.append(f"{sec_num}: {canonical}")
                    break

    passed = len(missing_sections) == 0

    return {
        "task_id": task_id,
        "filepath": filepath,
        "is_subtask": subtask,
        "has_header": has_header,
        "header_metadata_issues": header_metadata_issues,
        "present_sections": present_sections,
        "missing_sections": missing_sections,
        "passed": passed,
    }


def fix_file(filepath, result):
    """Append missing section stubs to a file."""
    if not result["missing_sections"]:
        return False

    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    additions = []
    for entry in result["missing_sections"]:
        sec_num = int(entry.split(":")[0])
        if sec_num == 1:
            # Can't easily fix a missing header — skip
            continue
        if sec_num in SECTION_STUBS:
            additions.append(SECTION_STUBS[sec_num])

    if not additions:
        return False

    # Ensure file ends with newline before appending
    if not content.endswith("\n"):
        content += "\n"

    content += "\n".join(additions)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return True


def main():
    parser = argparse.ArgumentParser(description="Audit task files against 14-section standard")
    parser.add_argument("--all", action="store_true", help="Show all files, not just failures")
    parser.add_argument("--fix", action="store_true", help="Add missing section stubs to failing files")
    parser.add_argument("--tasks-dir", default=TASKS_DIR, help="Path to tasks directory")
    args = parser.parse_args()

    task_files = sorted(glob.glob(os.path.join(args.tasks_dir, "task_*.md")))
    if not task_files:
        print(f"No task files found in {args.tasks_dir}")
        sys.exit(1)

    results = []
    skipped = 0
    for fp in task_files:
        r = check_file(fp)
        if r is None:
            skipped += 1
            continue
        results.append(r)

    pass_count = sum(1 for r in results if r["passed"])
    fail_count = sum(1 for r in results if not r["passed"])
    parent_count = sum(1 for r in results if not r["is_subtask"])
    subtask_count = sum(1 for r in results if r["is_subtask"])
    fixed_count = 0

    # Fix mode
    if args.fix:
        for r in results:
            if not r["passed"]:
                if fix_file(r["filepath"], r):
                    fixed_count += 1

    # Print summary
    print("=" * 70)
    print("TASK SECTION COMPLIANCE REPORT")
    print("=" * 70)
    print(f"Total files scanned: {len(results)}  (parents: {parent_count}, subtasks: {subtask_count})")
    if skipped:
        print(f"Skipped (unrecognized naming): {skipped}")
    print(f"PASS: {pass_count}   FAIL: {fail_count}")
    if args.fix:
        print(f"FIXED: {fixed_count} files had stubs appended")
    print("=" * 70)
    print()

    # Per-file details
    for r in results:
        if not args.all and r["passed"]:
            continue

        kind = "SUBTASK" if r["is_subtask"] else "PARENT"
        status = "PASS" if r["passed"] else "FAIL"
        basename = os.path.basename(r["filepath"])
        print(f"[{status}] {basename}  ({kind})")

        if r["missing_sections"]:
            for ms in r["missing_sections"]:
                print(f"       ✗ Missing: {ms}")

        if r["header_metadata_issues"]:
            for issue in r["header_metadata_issues"]:
                print(f"       ⚠ Metadata: {issue}")

        print()

    # Exit code
    if fail_count > 0 and not args.fix:
        sys.exit(1)
    elif args.fix:
        # Re-check after fix
        recheck_fails = 0
        for r in results:
            if not r["passed"]:
                r2 = check_file(r["filepath"])
                if r2 and not r2["passed"]:
                    recheck_fails += 1
        if recheck_fails > 0:
            sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
