#!/usr/bin/env python3
"""
Enhance clean task files with detailed content from archived task files.
"""

import re
from pathlib import Path

# Mapping from clean IDs to archived file numbers
ID_MAP = {
    "002": "009",
    "003": "019",
    "004": "054",
    "005": "055",
    "006": "056",
    "007": "057",
    "008": "058",
    "010": "059",
    "011": "060",
    "012": "061",
    "013": "062",
    "015": "063",
    "016": "023",
    "018": "027",
    "019": "031",
    "020": "040",
}


def parse_archived_task(filepath: Path) -> dict:
    """Parse an archived task file for detailed information."""
    content = filepath.read_text()

    task = {
        "title": "",
        "description": "",
        "details": "",
        "test_strategy": "",
        "subtasks": {},
        "tags": [],
    }

    # Extract title
    title_match = re.search(r"\*\*Title:\*\*\s*(.+)", content)
    if title_match:
        task["title"] = title_match.group(1).strip()

    # Extract description
    desc_match = re.search(r"\*\*Description:\*\*\s*(.+?)(?=\*\*Details:|\*\*)", content, re.DOTALL)
    if desc_match:
        task["description"] = desc_match.group(1).strip()

    # Extract details section
    details_match = re.search(
        r"\*\*Details:\*\*\s*(.+?)(?=\*\*Test Strategy:|\*\*)", content, re.DOTALL
    )
    if details_match:
        task["details"] = details_match.group(1).strip()

    # Extract test strategy
    test_match = re.search(r"\*\*Test Strategy:\*\*\s*(.+?)(?=## Subtasks|\Z)", content, re.DOTALL)
    if test_match:
        task["test_strategy"] = test_match.group(1).strip()

    # Extract tags
    tags_match = re.search(r"### Tags:(.+?)(?=\*\*)", content, re.DOTALL)
    if tags_match:
        tags = re.findall(r"- `([^`]+)`", tags_match.group(1))
        task["tags"] = tags

    # Extract subtasks - format is "### 23.1. Title"
    subtask_matches = re.findall(r"### (\d+\.\d+)\. (.+?)\n\n\*\*Status:", content)

    for subtask_id, subtask_title in subtask_matches:
        # Get details for this subtask
        details_pattern = rf"### {subtask_id}\. {re.escape(subtask_title)}\n\n\*\*Status:[^\n]*\n\n(.+?)(?=\n### |\n## |\Z)"
        details_match = re.search(details_pattern, content, re.DOTALL)

        subtask_details = ""
        if details_match:
            subtask_details = details_match.group(1).strip()
            # Extract key commands
            commands = re.findall(r"`([^`]+)`", subtask_details)
            subtask_details = (
                subtask_details
                + "\n\n**Key Commands:**\n"
                + "\n".join(f"- `{c}`" for c in commands[:3])
            )

        task["subtasks"][subtask_id] = {
            "title": subtask_title,
            "details": subtask_details,
        }

    return task


def enhance_task_file(clean_id: str, archived_id: str):
    """Enhance a clean task file with archived details."""
    clean_path = Path(f"new_task_plan/task_files/task-{clean_id}.md")
    archived_path = Path(f"tasks/archive/task_{archived_id.zfill(3)}.md")

    if not archived_path.exists():
        return False

    if not clean_path.exists():
        return False

    archived = parse_archived_task(archived_path)
    content = clean_path.read_text()

    # Add archived description to purpose
    if archived["description"]:
        content = re.sub(r"(## Purpose\n\n)", r"\1" + archived["description"] + "\n\n", content)

    # Add implementation details
    if archived["details"]:
        details_section = f"""

## Detailed Implementation

{archived["details"]}
"""
        content = re.sub(r"(## Success Criteria\n)", details_section + r"\1", content)

    # Add test strategy
    if archived["test_strategy"]:
        test_section = f"""

## Test Strategy

{archived["test_strategy"]}
"""
        content = re.sub(r"(## Subtasks\n)", test_section + r"\1", content)

    # Add tags
    if archived["tags"]:
        tags_str = ", ".join(f"`{t}`" for t in archived["tags"])
        content = re.sub(r"(\*\*Original Task:.+?\n)", r"\1**Tags:** " + tags_str + "\n", content)

    # Replace placeholder subtask details with archived content
    for subtask_id, subtask_data in archived["subtasks"].items():
        old_pattern = rf"(### {subtask_id}: .+?\n\n\*\*Purpose:\*\*.+?\n)(---)"
        if re.search(old_pattern, content):
            replacement = rf"\1\n{subtask_data['details']}\n\2"
            content = re.sub(old_pattern, replacement, content, flags=re.DOTALL)

    clean_path.write_text(content)
    print(f"Enhanced: task-{clean_id}.md ({len(archived['subtasks'])} subtasks)")
    return True


def main():
    print("Enhancing clean task files with archived content...\n")

    enhanced = []
    for clean_id, archived_id in sorted(ID_MAP.items()):
        if enhance_task_file(clean_id, archived_id):
            enhanced.append(clean_id)

    print(f"\nEnhanced {len(enhanced)} task files")
    for e in enhanced:
        print(f"  - task-{e}.md")


if __name__ == "__main__":
    main()
