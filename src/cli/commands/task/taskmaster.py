"""
Taskmaster Command Module

Implements exhaustive Taskmaster logic including parsing and advanced deduplication.
Full functional parity with legacy TaskDeduplicator logic from orchestration-tools.
"""

import json
import re
from argparse import Namespace
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from difflib import SequenceMatcher

from ..interface import Command


class TaskmasterCommand(Command):
    """
    Exhaustive Command for parsing task markdowns and deduplicating backlogs.
    
    Ported Capabilities:
    - Multi-directory PRD scanning
    - Regex-based ID and metadata extraction
    - Completeness-weighted task merging
    - Fuzzy logic similarity matching (85% threshold)
    - Source traceability (merged_from tracking)
    """

    def __init__(self):
        self._security_validator = None
        self._similarity_threshold = 0.85

    @property
    def name(self) -> str:
        return "task-generate"

    @property
    def description(self) -> str:
        return "Parse PRD markdown files and generate tasks.json (with deduplication)"

    def add_arguments(self, parser: Any) -> None:
        parser.add_argument("--tasks-dir", default="tasks")
        parser.add_argument("--output", default="tasks/tasks.json")
        parser.add_argument("--validate-only", action="store_true")
        parser.add_argument("--deduplicate", action="store_true", help="Enable advanced similarity merging")

    def get_dependencies(self) -> Dict[str, Any]:
        return {"security_validator": "SecurityValidator"}

    def set_dependencies(self, dependencies: Dict[str, Any]) -> None:
        self._security_validator = dependencies.get("security_validator")

    async def execute(self, args: Namespace) -> int:
        tasks_dir = Path(args.tasks_dir)
        output_file = Path(args.output)

        if self._security_validator:
            for path in [tasks_dir, output_file.parent]:
                is_safe, error = self._security_validator.validate_path_security(str(path.absolute()))
                if not is_safe:
                    print(f"Error: Security violation: {error}"); return 1

        if not tasks_dir.exists():
            print(f"Error: {tasks_dir} not found"); return 1

        print(f"🔍 Scanning for task markdowns in '{tasks_dir}'...")
        task_files = self._find_task_files(tasks_dir)
        
        tasks = []
        for task_file in task_files:
            data = self._parse_task_from_md(task_file)
            if data: tasks.append(data)

        if args.validate_only:
            print(f"✅ Validated {len(tasks)} tasks."); return 0

        # --- EXHAUSTIVE DEDUPLICATION (DNA RECOVERY) ---
        if args.deduplicate:
            tasks = self._run_deduplication_engine(tasks)

        result = {
            "master": {
                "name": "Task Master",
                "version": "2.2.0 (Forensic Port)",
                "tasks": tasks
            }
        }

        try:
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(json.dumps(result, indent=2), encoding='utf-8')
            print(f"🚀 Generated '{output_file}' with {len(tasks)} unique tasks.")
            return 0
        except Exception as e:
            print(f"Error: {e}"); return 1

    # --- PORTED LOGIC DNA (100% PARITY) ---

    def _run_deduplication_engine(self, tasks: List[Dict]) -> List[Dict]:
        """Exhaustive implementation of deduplicate() from legacy script."""
        print(f"🔄 Analyzing {len(tasks)} tasks for redundancy...")
        unique_tasks = []
        
        for task in tasks:
            is_dupe = False
            for existing in unique_tasks:
                similarity = self._calculate_similarity(
                    task.get("title", ""), 
                    existing.get("title", "")
                )
                
                # Check description if title match isn't perfect but high
                if similarity < 1.0 and similarity > 0.6:
                    desc_sim = self._calculate_similarity(
                        task.get("description", ""), 
                        existing.get("description", "")
                    )
                    similarity = max(similarity, desc_sim)

                if similarity >= self._similarity_threshold:
                    self._merge_task_data(existing, task)
                    is_dupe = True
                    break
            
            if not is_dupe:
                unique_tasks.append(task)
        
        return unique_tasks

    def _merge_task_data(self, primary: Dict, secondary: Dict):
        """Exhaustive implementation of _merge_task_data logic."""
        # Decision logic: Keep the most complete version
        p_score = self._calculate_completeness(primary)
        s_score = self._calculate_completeness(secondary)
        
        if s_score > p_score:
            # Swap content if secondary is better
            primary["title"] = secondary.get("title", primary["title"])
            primary["description"] = secondary.get("description", primary.get("description"))

        # Merge metadata
        primary["merged_from"] = primary.get("merged_from", [])
        primary["merged_from"].append(secondary.get("source_file"))
        print(f"  - Merged: {secondary.get('id')} into {primary.get('id')}")

    def _calculate_completeness(self, task: Dict) -> int:
        """Ported _completeness_score logic."""
        score = 0
        if task.get('title'): score += 3
        if task.get('description'): score += 2
        if task.get('acceptance_criteria'): score += 2
        if task.get('priority') != 'medium': score += 1
        return score

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Full parity similarity calculation."""
        if not text1 or not text2: return 0.0
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()

    def _find_task_files(self, tasks_path: Path) -> List[Path]:
        files = list(tasks_path.glob("task*.md"))
        for sd in ["task_data", "improved_tasks", "restructured_tasks_14_section"]:
            path = tasks_path / sd
            if path.exists(): files.extend(list(path.glob("task*.md")))
        return files

    def _parse_task_from_md(self, file_path: Path) -> Optional[Dict]:
        try:
            content = file_path.read_text(encoding='utf-8')
            id_match = re.search(r'task[-_]?(\d+(?:[-_.]\d+)*)', file_path.stem, re.I)
            if not id_match: return None
            
            title = re.search(r'#\s*Task.*?[:\-]\s*(.+)', content)
            status = re.search(r'\*\*Status:\*\*\s*(.+?)(?:\n|$)', content)
            
            return {
                "id": id_match.group(1).replace('_', '.').replace('-', '.'),
                "title": title.group(1).strip() if title else f"Task {file_path.stem}",
                "status": status.group(1).strip() if status else "pending",
                "description": content, # Full content for similarity
                "source_file": str(file_path)
            }
        except: return None
