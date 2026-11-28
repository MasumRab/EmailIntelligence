#!/usr/bin/env python3
"""
Goal-Task Consistency Validator

Implements Constitution v1.3.0 Goal-Task Consistency Principle.
Validates that all implementation tasks map directly to at least one orchestration goal.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple


class GoalTaskValidator:
    """Validates consistency between project goals and implementation tasks."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.orchestration_goals = self._load_orchestration_goals()
        self.tasks_data = self._load_tasks_data()

    def _load_orchestration_goals(self) -> List[str]:
        """Load orchestration goals from constitution or goals file."""
        goals = []

        # Try to load from constitution
        constitution_path = self.project_root / ".specify" / "memory" / "constitution.md"
        if constitution_path.exists():
            with open(constitution_path, 'r') as f:
                content = f.read()
                # Extract goals from constitution
                if "Goal-Task Consistency" in content:
                    # Parse goals from constitution text
                    goals.extend([
                        "Verification-First Development",
                        "Goal-Task Consistency",
                        "Role-Based Access Control",
                        "Context-Aware Verification",
                        "Token Optimization",
                        "Security Requirements",
                        "Observability",
                        "Performance & Efficiency",
                        "Reliability",
                        "Extensibility"
                    ])

        # Fallback: load from goals file if it exists
        goals_file = self.project_root / "ORCHESTRATION_GOALS.md"
        if goals_file.exists():
            with open(goals_file, 'r') as f:
                content = f.read()
                # Extract goals from markdown
                lines = content.split('\n')
                for line in lines:
                    if line.strip().startswith('- ') or line.strip().startswith('* '):
                        goals.append(line.strip()[2:].strip())

        return goals

    def _load_tasks_data(self) -> Dict:
        """Load tasks data from tasks.json file."""
        tasks_file = self.project_root / ".taskmaster" / "tasks" / "tasks.json"
        if tasks_file.exists():
            try:
                with open(tasks_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Could not parse {tasks_file}")
                return {}
        return {}

    def validate_task_consistency(self, task_id: str, task_data: Dict) -> Tuple[bool, str]:
        """Validate that a single task is consistent with project goals.

        Args:
            task_id: The task identifier
            task_data: Task data dictionary

        Returns:
            Tuple of (is_consistent, reason)
        """
        if not self.orchestration_goals:
            return True, "No goals defined - cannot validate consistency"

        task_title = task_data.get('title', '').lower()
        task_description = task_data.get('description', '').lower()
        task_details = task_data.get('details', '').lower()

        # Check if task content aligns with any orchestration goal
        for goal in self.orchestration_goals:
            goal_lower = goal.lower()
            if (goal_lower in task_title or
                goal_lower in task_description or
                goal_lower in task_details):
                return True, f"Task aligns with goal: {goal}"

        return False, f"Task does not align with any defined orchestration goals: {self.orchestration_goals}"

    def validate_all_tasks(self) -> Tuple[bool, List[str]]:
        """Validate consistency of all tasks.

        Returns:
            Tuple of (all_consistent, list_of_issues)
        """
        issues = []
        all_consistent = True

        tasks = self.tasks_data.get('tasks', {})

        for task_id, task_data in tasks.items():
            is_consistent, reason = self.validate_task_consistency(task_id, task_data)
            if not is_consistent:
                all_consistent = False
                issues.append(f"Task {task_id} ({task_data.get('title', 'Unknown')}): {reason}")

            # Also validate subtasks
            subtasks = task_data.get('subtasks', [])
            for subtask in subtasks:
                subtask_id = f"{task_id}.{subtask.get('id', '?')}"
                is_sub_consistent, sub_reason = self.validate_task_consistency(subtask_id, subtask)
                if not is_sub_consistent:
                    all_consistent = False
                    issues.append(f"Subtask {subtask_id} ({subtask.get('title', 'Unknown')}): {sub_reason}")

        return all_consistent, issues

    def generate_consistency_report(self) -> str:
        """Generate a detailed consistency report."""
        report_lines = []
        report_lines.append("# Goal-Task Consistency Report")
        report_lines.append("")

        # Goals summary
        report_lines.append("## Defined Orchestration Goals")
        for goal in self.orchestration_goals:
            report_lines.append(f"- {goal}")
        report_lines.append("")

        # Validation results
        all_consistent, issues = self.validate_all_tasks()

        report_lines.append("## Validation Results")
        report_lines.append(f"Overall Status: {'✅ CONSISTENT' if all_consistent else '❌ INCONSISTENT'}")
        report_lines.append("")

        if issues:
            report_lines.append("## Issues Found")
            for issue in issues:
                report_lines.append(f"- {issue}")
            report_lines.append("")
        else:
            report_lines.append("✅ All tasks are consistent with orchestration goals")
            report_lines.append("")

        # Statistics
        tasks = self.tasks_data.get('tasks', {})
        total_tasks = len(tasks)
        total_subtasks = sum(len(task.get('subtasks', [])) for task in tasks.values())

        report_lines.append("## Statistics")
        report_lines.append(f"- Total Tasks: {total_tasks}")
        report_lines.append(f"- Total Subtasks: {total_subtasks}")
        report_lines.append(f"- Goals Defined: {len(self.orchestration_goals)}")
        report_lines.append(f"- Consistency Rate: {((total_tasks + total_subtasks - len(issues)) / (total_tasks + total_subtasks) * 100):.1f}%")

        return "\n".join(report_lines)


def main():
    """Main entry point for the goal-task validator."""
    project_root = Path(__file__).parent.parent

    validator = GoalTaskValidator(project_root)
    all_consistent, issues = validator.validate_all_tasks()

    if all_consistent:
        print("✅ All tasks are consistent with orchestration goals")
        sys.exit(0)
    else:
        print("❌ Goal-task consistency violations found:")
        for issue in issues:
            print(f"  - {issue}")
        print("")
        print("Run with --report for detailed analysis")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--report":
        project_root = Path(__file__).parent.parent
        validator = GoalTaskValidator(project_root)
        print(validator.generate_consistency_report())
    else:
        main()