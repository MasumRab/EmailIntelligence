#!/usr/bin/env python3
"""
Micro-task Decomposition System
Breaks large documentation tasks into micro-tasks completable in <15 minutes.
"""

import re
import json
from pathlib import Path
from typing import List, Dict
from datetime import timedelta


class TaskDecomposer:
    """Breaks documentation tasks into micro-tasks."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.max_task_time = timedelta(minutes=15)  # 15 minutes max per task

    def decompose_documentation_task(self, doc_file: Path) -> List[Dict]:
        """Decompose a documentation file into micro-tasks."""
        if not doc_file.exists():
            return []

        with open(doc_file, "r") as f:
            content = f.read()

        tasks = []
        sections = self._split_into_sections(content, doc_file.name)

        for i, section in enumerate(sections):
            task = self._create_micro_task(section, doc_file, i)
            if task:
                tasks.append(task)

        return tasks

    def _split_into_sections(self, content: str, filename: str) -> List[Dict]:
        """Split content into logical sections."""
        sections = []

        # Split by markdown headers
        header_pattern = r"(#{1,6})\s+(.*?)(?=\n#{1,6}|\Z)"
        matches = list(re.finditer(header_pattern, content, re.DOTALL))

        if not matches:
            # If no headers, treat as single section
            return [
                {
                    "title": f"{filename} - Complete Document",
                    "content": content,
                    "type": "document",
                }
            ]

        # Process each section
        for i, match in enumerate(matches):
            header_level = len(match.group(1))
            header_title = match.group(2).strip()

            # Get content until next header or end of file
            start_pos = match.end()
            if i < len(matches) - 1:
                end_pos = matches[i + 1].start()
            else:
                end_pos = len(content)

            section_content = content[start_pos:end_pos].strip()

            sections.append(
                {
                    "title": header_title,
                    "content": section_content,
                    "type": f"header-{header_level}",
                    "estimated_time": self._estimate_time(section_content),
                }
            )

        return sections

    def _estimate_time(self, content: str) -> timedelta:
        """Estimate time needed to complete a section."""
        # Simple estimation based on word count
        word_count = len(content.split())

        # Assume 100 words per minute reading/writing speed
        minutes = max(2, word_count / 100)  # Minimum 2 minutes

        return timedelta(minutes=minutes)

    def _create_micro_task(self, section: Dict, source_file: Path, index: int) -> Dict:
        """Create a micro-task from a section."""
        estimated_time = section.get("estimated_time", timedelta(minutes=5))

        # If section is too large, split it further
        if estimated_time > self.max_task_time:
            sub_sections = self._split_large_section(section)
            tasks = []
            for i, sub_section in enumerate(sub_sections):
                task = self._create_micro_task(
                    sub_section, source_file, index * 100 + i
                )
                if task:
                    tasks.append(task)
            return tasks[0] if tasks else None

        # Create single task
        task = {
            "id": f"{source_file.stem}-{index}",
            "title": f"Process section: {section['title']}",
            "description": section["content"][:200] + "..."
            if len(section["content"]) > 200
            else section["content"],
            "source_file": str(source_file.relative_to(self.project_root)),
            "section_title": section["title"],
            "type": section["type"],
            "estimated_time": int(estimated_time.total_seconds() / 60),  # in minutes
            "status": "pending",
            "dependencies": [],
            "priority": "normal",
        }

        return task

    def _split_large_section(self, section: Dict) -> List[Dict]:
        """Split a large section into smaller parts."""
        content = section["content"]
        paragraphs = content.split("\n\n")

        # If we have paragraphs, split by them
        if len(paragraphs) > 1:
            # Group paragraphs into chunks
            chunk_size = max(1, len(paragraphs) // 3)  # Aim for 3 chunks
            chunks = []
            for i in range(0, len(paragraphs), chunk_size):
                chunk_paragraphs = paragraphs[i : i + chunk_size]
                chunk_content = "\n\n".join(chunk_paragraphs)
                chunks.append(
                    {
                        "title": f"{section['title']} (part {i // chunk_size + 1})",
                        "content": chunk_content,
                        "type": section["type"],
                        "estimated_time": self._estimate_time(chunk_content),
                    }
                )
            return chunks

        # If no paragraphs or single paragraph, split by sentences
        sentences = re.split(r"[.!?]+", content)
        if len(sentences) > 3:
            chunk_size = max(1, len(sentences) // 3)
            chunks = []
            for i in range(0, len(sentences), chunk_size):
                chunk_sentences = sentences[i : i + chunk_size]
                chunk_content = (
                    ". ".join(s.strip() for s in chunk_sentences if s.strip()) + "."
                )
                chunks.append(
                    {
                        "title": f"{section['title']} (part {i // chunk_size + 1})",
                        "content": chunk_content,
                        "type": section["type"],
                        "estimated_time": self._estimate_time(chunk_content),
                    }
                )
            return chunks

        # If still too large, split by characters
        char_limit = len(content) // 3
        chunks = []
        for i in range(0, len(content), char_limit):
            chunk_content = content[i : i + char_limit]
            chunks.append(
                {
                    "title": f"{section['title']} (part {i // char_limit + 1})",
                    "content": chunk_content,
                    "type": section["type"],
                    "estimated_time": self._estimate_time(chunk_content),
                }
            )
        return chunks

    def save_tasks(self, tasks: List[Dict], output_dir: Path):
        """Save tasks to JSON files."""
        output_dir.mkdir(parents=True, exist_ok=True)

        if isinstance(tasks, list) and len(tasks) > 0 and isinstance(tasks[0], list):
            # Handle nested task lists
            flat_tasks = []
            for task_group in tasks:
                if isinstance(task_group, list):
                    flat_tasks.extend(task_group)
                else:
                    flat_tasks.append(task_group)
            tasks = flat_tasks

        for task in tasks:
            task_file = output_dir / f"task-{task['id']}.json"
            with open(task_file, "w") as f:
                json.dump(task, f, indent=2)

    def process_directory(self, docs_dir: Path, output_dir: Path):
        """Process all documentation files in a directory."""
        all_tasks = []

        for doc_file in docs_dir.rglob("*.md"):
            if doc_file.is_file():
                tasks = self.decompose_documentation_task(doc_file)
                if tasks:
                    if (
                        isinstance(tasks, list)
                        and len(tasks) > 0
                        and isinstance(tasks[0], list)
                    ):
                        # Flatten nested task lists
                        flat_tasks = []
                        for task_group in tasks:
                            if isinstance(task_group, list):
                                flat_tasks.extend(task_group)
                            else:
                                flat_tasks.append(task_group)
                        tasks = flat_tasks
                    all_tasks.extend(tasks)

        self.save_tasks(all_tasks, output_dir)
        return all_tasks


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Micro-task Decomposition System")
    parser.add_argument("input_dir", help="Directory containing documentation files")
    parser.add_argument("output_dir", help="Directory to save decomposed tasks")
    parser.add_argument("--project-root", default=".", help="Project root directory")

    args = parser.parse_args()

    project_root = Path(args.project_root)
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)

    decomposer = TaskDecomposer(project_root)
    tasks = decomposer.process_directory(input_dir, output_dir)

    print(f"Decomposed {len(tasks)} micro-tasks from documentation in {input_dir}")
    print(f"Tasks saved to {output_dir}")


if __name__ == "__main__":
    main()
