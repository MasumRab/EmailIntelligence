#!/usr/bin/env python3
"""
Search Across All Remote Branches for Backlog Tasks

Systematically searches all remote branches for task files and consolidates them.
"""

import subprocess
import os
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict
import re
try:
    import yaml
except ImportError:
    yaml = None


class RemoteBranchTaskSearcher:
    """Searches remote branches for task files and consolidates them."""

    def __init__(self, repo_path: Path, output_dir: Path):
        self.repo_path = repo_path
        self.output_dir = output_dir
        self.found_tasks = defaultdict(dict)  # branch -> {task_id: task_data}
        self.task_patterns = [
            r"task-\d+.*\.md$",           # task-123.md, task-123-description.md
            r"task-\d+\.\d+.*\.md$",      # task-123.1.md, task-123.1-description.md
        ]

    def run_git_command(self, cmd: List[str]) -> str:
        """Run a git command and return output."""
        try:
            result = subprocess.run(
                ["git"] + cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Git command failed: {' '.join(cmd)}")
            print(f"Error: {e}")
            return ""

    def get_remote_branches(self) -> List[str]:
        """Get all remote branches."""
        output = self.run_git_command(["branch", "-r"])
        branches = []
        for line in output.split('\n'):
            branch = line.strip()
            if branch and not branch.endswith('-> origin/HEAD'):
                # Remove 'origin/' prefix
                branch_name = branch.replace('origin/', '')
                branches.append(branch_name)
        return sorted(branches)

    def find_task_files_in_branch(self, branch: str) -> List[str]:
        """Find task files in a specific branch."""
        # Use git ls-tree to list files without checking out
        output = self.run_git_command(["ls-tree", "-r", "--name-only", f"origin/{branch}"])

        task_files = []
        for line in output.split('\n'):
            file_path = line.strip()
            if file_path:
                # Check if it matches our task patterns
                for pattern in self.task_patterns:
                    if re.search(pattern, file_path, re.IGNORECASE):
                        task_files.append(file_path)
                        break

        return task_files

    def extract_task_from_branch(self, branch: str, file_path: str) -> Optional[Dict]:
        """Extract task content from a specific branch and file."""
        try:
            # Use git show to get file content from specific branch
            output = self.run_git_command(["show", f"origin/{branch}:{file_path}"])

            if not output:
                return None

            # Parse frontmatter and content
            task_data = self.parse_task_content(output, file_path)
            if task_data:
                task_data['branch'] = branch
                task_data['source_path'] = file_path
                task_data['git_ref'] = f"origin/{branch}"

            return task_data

        except Exception as e:
            print(f"Error extracting {file_path} from {branch}: {e}")
            return None

    def parse_task_content(self, content: str, file_path: str) -> Optional[Dict]:
        """Parse task content and extract metadata."""
        try:
            # Extract frontmatter
            frontmatter = {}
            body = content

            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    try:
                        if yaml:
                            frontmatter = yaml.safe_load(parts[1]) or {}
                        else:
                            frontmatter = {}
                        body = parts[2].strip()
                    except Exception:
                        body = content

            # Extract task ID from filename or frontmatter
            task_id = frontmatter.get('id')
            if not task_id:
                # Extract from filename
                filename = Path(file_path).name
                match = re.search(r'(task-\d+(?:\.\d+)?)', filename, re.IGNORECASE)
                if match:
                    task_id = match.group(1)

            if not task_id:
                return None

            return {
                'task_id': task_id,
                'title': frontmatter.get('title', ''),
                'status': frontmatter.get('status', 'Unknown'),
                'content': body,
                'frontmatter': frontmatter,
                'filename': Path(file_path).name,
                'full_content': content
            }

        except Exception as e:
            print(f"Error parsing task content: {e}")
            return None

    def search_all_branches(self) -> Dict:
        """Search all remote branches for tasks."""
        print("🔍 Starting comprehensive remote branch search...")

        branches = self.get_remote_branches()
        print(f"📋 Found {len(branches)} remote branches to search")

        # Prioritize branches by likelihood of having tasks
        priority_branches = [
            'main', 'scientific', 'orchestration-tools', 'taskmaster'
        ]

        # Add branches that start with task- or feature-
        task_branches = [b for b in branches if b.startswith(('task-', 'feature-'))]
        other_branches = [b for b in branches if b not in priority_branches and b not in task_branches]

        search_order = priority_branches + task_branches + other_branches

        total_tasks_found = 0
        branch_stats = {}

        for branch in search_order:
            print(f"🔎 Searching branch: {branch}")
            task_files = self.find_task_files_in_branch(branch)

            if task_files:
                print(f"  📄 Found {len(task_files)} task files")
                branch_tasks = {}

                for file_path in task_files:
                    task_data = self.extract_task_from_branch(branch, file_path)
                    if task_data:
                        task_id = task_data['task_id']
                        branch_tasks[task_id] = task_data
                        self.found_tasks[task_id][branch] = task_data

                branch_stats[branch] = {
                    'task_count': len(branch_tasks),
                    'task_files': task_files
                }
                total_tasks_found += len(branch_tasks)
            else:
                branch_stats[branch] = {'task_count': 0, 'task_files': []}

        print(f"\n✅ Search complete! Found {total_tasks_found} total tasks across {len(branches)} branches")

        return {
            'branch_stats': branch_stats,
            'total_tasks': total_tasks_found,
            'branches_searched': len(branches),
            'tasks_by_id': dict(self.found_tasks)
        }

    def save_results(self, results: Dict):
        """Save search results to files."""
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Save summary
        summary_file = self.output_dir / "remote_branch_search_summary.json"
        with open(summary_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)

        # Save detailed task data
        tasks_file = self.output_dir / "all_remote_tasks.json"
        with open(tasks_file, 'w') as f:
            json.dump(results['tasks_by_id'], f, indent=2, default=str)

        # Generate human-readable report
        self.generate_report(results)

        print(f"💾 Results saved to {self.output_dir}")

    def generate_report(self, results: Dict):
        """Generate a human-readable report."""
        report_file = self.output_dir / "remote_branch_search_report.md"

        with open(report_file, 'w') as f:
            f.write("# Remote Branch Task Search Report\n\n")
            f.write(f"**Generated:** {os.popen('date').read().strip()}\n\n")

            f.write("## Executive Summary\n\n")
            f.write(f"- **Branches searched:** {results['branches_searched']}\n")
            f.write(f"- **Total tasks found:** {results['total_tasks']}\n")
            f.write(f"- **Unique task IDs:** {len(results['tasks_by_id'])}\n\n")

            # Branch statistics
            f.write("## Branch Statistics\n\n")
            f.write("| Branch | Tasks Found | Sample Files |\n")
            f.write("|--------|-------------|--------------|\n")

            for branch, stats in results['branch_stats'].items():
                task_count = stats['task_count']
                sample_files = ", ".join(stats['task_files'][:2]) if stats['task_files'] else "None"
                if len(sample_files) > 50:
                    sample_files = sample_files[:47] + "..."
                f.write(f"| {branch} | {task_count} | {sample_files} |\n")

            f.write("\n")

            # Task distribution analysis
            f.write("## Task Distribution Analysis\n\n")

            # Tasks by branch count
            branch_counts = defaultdict(int)
            for task_id, branches in results['tasks_by_id'].items():
                branch_count = len(branches)
                branch_counts[branch_count] += 1

            f.write("### Tasks by Branch Distribution\n\n")
            for branch_count, task_count in sorted(branch_counts.items()):
                f.write(f"- **{task_count} tasks** appear in {branch_count} branch(es)\n")

            f.write("\n")

            # Most common tasks across branches
            multi_branch_tasks = {
                task_id: branches
                for task_id, branches in results['tasks_by_id'].items()
                if len(branches) > 1
            }

            if multi_branch_tasks:
                f.write("### Tasks Appearing in Multiple Branches\n\n")
                f.write(f"Found {len(multi_branch_tasks)} tasks that appear in multiple branches:\n\n")

                for task_id, branches in list(multi_branch_tasks.items())[:10]:  # Top 10
                    branch_names = list(branches.keys())
                    f.write(f"- **{task_id}**: {', '.join(branch_names)}\n")

                if len(multi_branch_tasks) > 10:
                    f.write(f"- ... and {len(multi_branch_tasks) - 10} more\n")

            f.write("\n## Recommendations\n\n")
            f.write("1. **Review multi-branch tasks** for consolidation opportunities\n")
            f.write("2. **Identify branch-specific tasks** that may need merging\n")
            f.write("3. **Check for task evolution** across different branches\n")
            f.write("4. **Consolidate duplicate efforts** found across branches\n")


def main():
    """Main execution function."""
    repo_path = Path("/home/masum/github/EmailIntelligence")
    output_dir = Path("/home/masum/github/backlog/remote_branch_search")

    searcher = RemoteBranchTaskSearcher(repo_path, output_dir)
    results = searcher.search_all_branches()
    searcher.save_results(results)

    print("\n🎉 Remote branch search complete!")
    print(f"📊 Results saved to: {output_dir}")
    print(f"📈 Found {results['total_tasks']} tasks across {results['branches_searched']} branches")


if __name__ == "__main__":
    main()