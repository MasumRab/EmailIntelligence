#!/usr/bin/env python3

import os
import re
import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class TaskMigrator:
    def __init__(self, tasks_dir: str = "tasks", task_data_dir: str = "task_data"):
        self.tasks_dir = Path(tasks_dir)
        self.task_data_dir = Path(task_data_dir)
        self.backup_dir = Path(f"task_data/migration_backup_{self.get_datestamp()}")

    def get_datestamp(self) -> str:
        from datetime import datetime

        return datetime.now().strftime("%Y%m%d")

    def read_task_file(self, file_path: Path) -> str:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return ""

    def extract_handoff_patterns(self, enhanced_content: str) -> Dict[str, str]:
        patterns = {}
        dev_ref_match = re.search(
            r"## Developer Quick Reference\n(.*?)(?=\n## |\n---|$)",
            enhanced_content,
            re.DOTALL,
        )
        if dev_ref_match:
            patterns["developer_quick_reference"] = dev_ref_match.group(1).strip()

        impl_check_match = re.search(
            r"## Implementation Checklist\n(.*?)(?=\n## |\n---|$)",
            enhanced_content,
            re.DOTALL,
        )
        if impl_check_match:
            patterns["implementation_checklist"] = impl_check_match.group(1).strip()

        test_cases_match = re.search(
            r"## Test Case Examples\n(.*?)(?=\n## |\n---|$)",
            enhanced_content,
            re.DOTALL,
        )
        if test_cases_match:
            patterns["test_case_examples"] = test_cases_match.group(1).strip()

        config_match = re.search(
            r"## Configuration Parameters\n(.*?)(?=\n## |\n---|$)",
            enhanced_content,
            re.DOTALL,
        )
        if config_match:
            patterns["configuration_parameters"] = config_match.group(1).strip()

        return patterns

    def merge_task_content(self, current_content: str, enhanced_content: str) -> str:
        patterns = self.extract_handoff_patterns(enhanced_content)
        merged_parts = []
        merged_parts.append(current_content)
        merged_parts.append("\n\n---\n## HANDOFF Enhanced Implementation Guidance\n")

        if patterns.get("developer_quick_reference"):
            merged_parts.append("### Developer Quick Reference\n")
            merged_parts.append(patterns["developer_quick_reference"])
            merged_parts.append("\n\n")

        if patterns.get("implementation_checklist"):
            merged_parts.append("### Implementation Checklist\n")
            merged_parts.append(patterns["implementation_checklist"])
            merged_parts.append("\n\n")

        if patterns.get("test_case_examples"):
            merged_parts.append("### Test Case Examples\n")
            merged_parts.append(patterns["test_case_examples"])
            merged_parts.append("\n\n")

        if patterns.get("configuration_parameters"):
            merged_parts.append("### Configuration Parameters\n")
            merged_parts.append(patterns["configuration_parameters"])
            merged_parts.append("\n\n")

        return "".join(merged_parts)

    def migrate_task_002(self):
        current_path = self.tasks_dir / "task-002.md"
        enhanced_path = (
            self.task_data_dir / "archived" / "task_002_consolidated_v1" / "task_002.md"
        )
        output_path = self.tasks_dir / "task_002.md"

        if not current_path.exists():
            print(f"Current task-002.md not found at {current_path}")
            return False

        if not enhanced_path.exists():
            print(f"Enhanced task_002.md not found at {enhanced_path}")
            return False

        current_content = self.read_task_file(current_path)
        enhanced_content = self.read_task_file(enhanced_path)

        if not current_content or not enhanced_content:
            print(f"Failed to read task files for migration")
            return False

        merged_content = self.merge_task_content(current_content, enhanced_content)

        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(merged_content)
            print(f"Successfully migrated Task 002 to {output_path}")
            return True
        except Exception as e:
            print(f"Error writing migrated Task 002: {e}")
            return False

    def add_handoff_patterns_to_task(self, task_number: str):
        current_path = self.tasks_dir / f"task-{task_number}.md"
        output_path = self.tasks_dir / f"task_{task_number}.md"

        if not current_path.exists():
            print(f"Task {task_number} not found at {current_path}")
            return False

        current_content = self.read_task_file(current_path)
        if not current_content:
            print(f"Failed to read task {task_number}")
            return False

        enhanced_content = self.create_enhanced_template(task_number)
        merged_content = self.merge_task_content(current_content, enhanced_content)

        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(merged_content)
            print(f"Successfully enhanced Task {task_number}")
            return True
        except Exception as e:
            print(f"Error enhancing Task {task_number}: {e}")
            return False

    def create_enhanced_template(self, task_number: str) -> str:
        template = f"""
 ## Developer Quick Reference

### Key Classes & Functions
- Task{task_number}Processor: Main processing class
- analyze_{task_number}_data(): Core analysis function
- validate_{task_number}_config(): Configuration validation

### Performance Metrics
- Processing time: < 5 seconds per batch
- Memory usage: < 100MB peak
- Accuracy target: > 95%

### Dependencies
- pandas >= 1.3.0
- numpy >= 1.21.0
- Custom framework modules

## Implementation Checklist

- [ ] Set up basic class structure
- [ ] Implement core processing logic
- [ ] Add error handling and validation
- [ ] Create unit tests
- [ ] Add integration tests
- [ ] Performance optimization
- [ ] Documentation updates

## Test Case Examples

### Test Case 1: Basic Processing
```python
processor = Task{task_number}Processor()
result = processor.process(test_data)
assert result.success == True
```

### Test Case 2: Error Handling
```python
processor = Task{task_number}Processor()
result = processor.process(invalid_data)
assert result.error is not None
```

## Configuration Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| batch_size | 100 | Processing batch size |
| timeout | 30 | Operation timeout in seconds |
| max_retries | 3 | Maximum retry attempts |
| log_level | INFO | Logging level |
"""
        return template.strip()

    def archive_old_task_file(self, task_number: str):
        old_path = self.tasks_dir / f"task-{task_number}.md"
        archive_path = self.backup_dir / "archived_tasks" / f"task-{task_number}.md"

        if old_path.exists():
            archive_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(old_path), str(archive_path))
            print(f"Archived old task-{task_number}.md to {archive_path}")

    def run_migration(self):
        print("Starting task migration...")

        if self.migrate_task_002():
            self.archive_old_task_file("002")

        key_tasks = ["001", "007", "015", "020", "025"]
        for task_num in key_tasks:
            if self.add_handoff_patterns_to_task(task_num):
                self.archive_old_task_file(task_num)

        print("\nMigration Summary:")
        print(f"Backup directory: {self.backup_dir}")
        print("Enhanced tasks created with HANDOFF patterns")
        print("Original improvements preserved")


if __name__ == "__main__":
    migrator = TaskMigrator()
    migrator.run_migration()
