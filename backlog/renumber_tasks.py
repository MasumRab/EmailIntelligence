"""
Task Renumbering Script

Renumbers all consolidated tasks with consistent sequential numbering.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple
import yaml


class TaskRenumberer:
    """Renumbers consolidated tasks with consistent sequential IDs."""

    def __init__(self, consolidated_dir: Path):
        self.consolidated_dir = consolidated_dir
        self.task_files = []
        self.task_mapping = {}  # old_id -> new_id

    def collect_all_tasks(self) -> List[Tuple[str, Path]]:
        """Collect all task files with their current IDs."""
        tasks = []

        # Find all .md files that are tasks (not READMEs or category files)
        for md_file in self.consolidated_dir.rglob("*.md"):
            if md_file.name == "README.md":
                continue
            if "categories/" in str(md_file):
                continue
            if md_file.name in ["master_backlog.md", "statistics_report.md", "consolidation_report.md", "CONSOLIDATION_SUMMARY.md"]:
                continue

            # Extract current task ID from filename
            filename = md_file.name

            # Skip files that are already properly numbered (task-1, task-2, etc.)
            # Only process files that need renumbering
            if filename.startswith("task-"):
                # Check if it's already a simple sequential number
                parts = filename.split(" - ", 1)
                if len(parts) == 2:
                    task_id_part = parts[0]  # e.g., "task-123"
                    try:
                        num = int(task_id_part.replace("task-", ""))
                        # If it's a simple number 1-999, assume it's already correctly numbered
                        # Only reprocess if it has complex patterns
                        if "-" not in task_id_part.replace("task-", "") and "." not in task_id_part.replace("task-", ""):
                            continue  # Skip already correctly numbered files
                    except ValueError:
                        pass  # Not a simple number, process it

            if filename.startswith("task-"):
                # Regular task format: task-123 - Title.md
                task_id = filename.split(" - ")[0]
            elif filename.startswith("prd-"):
                # PRD task format: prd-fr-001 - Title.md
                task_id = filename.split(" - ")[0]
            elif filename.startswith("epic-"):
                # Epic format: epic-name - Title.md
                task_id = filename.split(" - ")[0]
            else:
                # Skip files that don't match expected patterns
                continue

            tasks.append((task_id, md_file))

        # Sort tasks by category priority, then by original ID
        category_priority = {
            "consolidation_migration": 1,
            "branch_management": 2,
            "validation_testing": 3,
            "documentation_research": 4,
            "development_implementation": 5,
            "security_hardening": 6,
            "uncategorized": 7
        }

        def sort_key(task_tuple):
            task_id, file_path = task_tuple
            # Extract category from path
            path_parts = file_path.relative_to(self.consolidated_dir).parts
            category = path_parts[0] if len(path_parts) > 0 else "uncategorized"
            category_num = category_priority.get(category, 8)

            # Extract numeric part for sorting
            if task_id.startswith("task-"):
                num_part = task_id.replace("task-", "")
            elif task_id.startswith("prd-"):
                num_part = task_id.replace("prd-", "").replace("-", "")
            else:
                num_part = task_id

            # Handle sub-numbers like 18.1, 115.1
            try:
                if "." in num_part:
                    major, minor = num_part.split(".", 1)
                    return (category_num, int(major), float(minor))
                else:
                    return (category_num, int(num_part), 0)
            except ValueError:
                return (category_num, 9999, 0)  # Put unparseable IDs at end

        tasks.sort(key=sort_key)
        return tasks

    def generate_new_ids(self, tasks: List[Tuple[str, Path]]) -> Dict[str, str]:
        """Generate new sequential task IDs."""
        mapping = {}
        counter = 1

        for old_id, file_path in tasks:
            new_id = f"task-{counter}"
            mapping[old_id] = new_id
            counter += 1

        return mapping

    def update_task_file(self, file_path: Path, old_id: str, new_id: str):
        """Update a task file with new ID and references."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Update frontmatter ID if it exists
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    try:
                        frontmatter = yaml.safe_load(parts[1]) or {}
                        if 'id' in frontmatter and frontmatter['id'] == old_id:
                            frontmatter['id'] = new_id
                            new_frontmatter = yaml.dump(frontmatter, default_flow_style=False).strip()
                            content = f"---\n{new_frontmatter}\n---{parts[2]}"
                    except:
                        pass  # Keep original content if YAML parsing fails

            # Update filename
            directory = file_path.parent
            filename_parts = file_path.name.split(" - ", 1)
            if len(filename_parts) == 2:
                title_part = filename_parts[1]
                new_filename = f"{new_id} - {title_part}"
                new_file_path = directory / new_filename

                # Write updated content
                with open(new_file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                # Remove old file
                file_path.unlink()

                print(f"✅ Renamed: {old_id} -> {new_id}")
                print(f"   File: {file_path} -> {new_file_path}")

        except Exception as e:
            print(f"❌ Error updating {file_path}: {e}")

    def update_references_in_files(self, mapping: Dict[str, str]):
        """Update references to old task IDs in all files."""
        print("🔄 Updating task ID references in all files...")

        for md_file in self.consolidated_dir.rglob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                updated = False
                for old_id, new_id in mapping.items():
                    # Update references in content (but not in filenames)
                    if old_id in content:
                        # Be careful not to update IDs in frontmatter or other structured data
                        # Just update plain text references
                        content = re.sub(r'\b' + re.escape(old_id) + r'\b', new_id, content)
                        updated = True

                if updated:
                    with open(md_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"   Updated references in: {md_file.name}")

            except Exception as e:
                print(f"❌ Error updating references in {md_file}: {e}")

    def renumber_all_tasks(self):
        """Main renumbering process."""
        print("🔢 Starting task renumbering process...")

        # Collect all tasks
        tasks = self.collect_all_tasks()
        print(f"📋 Found {len(tasks)} tasks to renumber")

        # Generate new IDs
        self.task_mapping = self.generate_new_ids(tasks)
        print(f"🆔 Generated {len(self.task_mapping)} new task IDs")

        # Show mapping preview
        print("\n📋 ID Mapping Preview (first 10):")
        for i, (old_id, new_id) in enumerate(list(self.task_mapping.items())[:10]):
            print(f"   {old_id} -> {new_id}")
        if len(self.task_mapping) > 10:
            print(f"   ... and {len(self.task_mapping) - 10} more")

        # Update task files
        print("\n📝 Updating task files...")
        for old_id, file_path in tasks:
            new_id = self.task_mapping[old_id]
            self.update_task_file(file_path, old_id, new_id)

        # Update references
        self.update_references_in_files(self.task_mapping)

        print("\n✅ Task renumbering complete!")
        print(f"📊 Total tasks renumbered: {len(self.task_mapping)}")
        print(f"🆔 New ID range: task-1 to task-{len(self.task_mapping)}")


if __name__ == "__main__":
    consolidated_dir = Path("/home/masum/github/backlog/consolidated")
    renumberer = TaskRenumberer(consolidated_dir)
    renumberer.renumber_all_tasks()