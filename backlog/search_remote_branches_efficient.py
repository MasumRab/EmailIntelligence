#!/usr/bin/env python3
"""
Efficient Remote Branch Task Search

Optimized search focusing on high-priority branches first.
"""

import subprocess
import os
import json
from pathlib import Path
from typing import Dict, List, Optional
from collections import defaultdict
import re


class EfficientBranchSearcher:
    """Efficiently searches remote branches for tasks."""

    def __init__(self, repo_path: Path, output_dir: Path):
        self.repo_path = repo_path
        self.output_dir = output_dir
        self.found_tasks = defaultdict(dict)

    def run_git_command(self, cmd: List[str], timeout: int = 30) -> Optional[str]:
        """Run git command with timeout."""
        try:
            result = subprocess.run(
                ["git"] + cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return result.stdout.strip() if result.returncode == 0 else None
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
            return None

    def get_priority_branches(self) -> List[str]:
        """Get high-priority branches to search first."""
        # Get all remote branches
        output = self.run_git_command(["branch", "-r"])
        if not output:
            return []

        all_branches = []
        for line in output.split('\n'):
            branch = line.strip()
            if branch and not branch.endswith('-> origin/HEAD'):
                branch_name = branch.replace('origin/', '')
                all_branches.append(branch_name)

        # Prioritize branches
        priority_patterns = [
            r'^main$', r'^master$',
            r'^scientific', r'^orchestration-tools',
            r'^taskmaster', r'^task-\d+',
            r'^feature-', r'^feat-',
            r'^pr-\d+'
        ]

        priority_branches = []
        other_branches = []

        for branch in all_branches:
            is_priority = False
            for pattern in priority_patterns:
                if re.search(pattern, branch, re.IGNORECASE):
                    priority_branches.append(branch)
                    is_priority = True
                    break
            if not is_priority:
                other_branches.append(branch)

        return priority_branches + other_branches[:20]  # Limit to top 20 priority + 20 others

    def quick_task_check(self, branch: str) -> int:
        """Quick check for number of task files in branch."""
        # Use git ls-tree to count task files quickly
        output = self.run_git_command([
            "ls-tree", "-r", "--name-only", f"origin/{branch}"
        ], timeout=10)

        if not output:
            return 0

        task_count = 0
        for line in output.split('\n'):
            if line.strip() and re.search(r'task-\d+.*\.md$', line, re.IGNORECASE):
                task_count += 1

        return task_count

    def extract_task_sample(self, branch: str, limit: int = 5) -> List[Dict]:
        """Extract a sample of tasks from a branch."""
        # Get list of task files
        output = self.run_git_command([
            "ls-tree", "-r", "--name-only", f"origin/{branch}"
        ], timeout=15)

        if not output:
            return []

        task_files = []
        for line in output.split('\n'):
            if line.strip() and re.search(r'task-\d+.*\.md$', line, re.IGNORECASE):
                task_files.append(line.strip())
                if len(task_files) >= limit:
                    break

        # Extract content for sample files
        samples = []
        for file_path in task_files[:limit]:
            content = self.run_git_command([
                "show", f"origin/{branch}:{file_path}"
            ], timeout=10)

            if content:
                # Quick parse
                task_id = "unknown"
                title = file_path

                # Extract task ID from filename
                match = re.search(r'(task-\d+(?:\.\d+)?)', file_path, re.IGNORECASE)
                if match:
                    task_id = match.group(1)

                # Extract title from content if possible
                lines = content.split('\n', 10)
                for line in lines[:5]:
                    if line.startswith('title:'):
                        title = line.replace('title:', '').strip().strip('"\'')
                        break

                samples.append({
                    'task_id': task_id,
                    'title': title,
                    'branch': branch,
                    'file_path': file_path,
                    'content_preview': content[:200] + '...' if len(content) > 200 else content
                })

        return samples

    def comprehensive_search(self) -> Dict:
        """Perform comprehensive but efficient search."""
        print("🔍 Starting efficient remote branch task search...")

        branches = self.get_priority_branches()
        print(f"📋 Prioritized {len(branches)} branches for searching")

        results = {
            'branch_summary': {},
            'task_samples': [],
            'total_tasks_estimated': 0,
            'branches_with_tasks': 0,
            'high_priority_branches': [],
            'search_stats': {}
        }

        for i, branch in enumerate(branches):
            print(f"🔎 [{i+1}/{len(branches)}] Checking branch: {branch}")

            # Quick count
            task_count = self.quick_task_check(branch)

            if task_count > 0:
                print(f"  📄 Found {task_count} task files")
                results['branches_with_tasks'] += 1
                results['total_tasks_estimated'] += task_count

                # Mark as high priority if it has many tasks
                if task_count > 10:
                    results['high_priority_branches'].append(branch)

                # Extract samples
                samples = self.extract_task_sample(branch, limit=3)
                results['task_samples'].extend(samples)

                results['branch_summary'][branch] = {
                    'task_count': task_count,
                    'has_samples': len(samples) > 0,
                    'samples': samples
                }
            else:
                results['branch_summary'][branch] = {
                    'task_count': 0,
                    'has_samples': False,
                    'samples': []
                }

        results['search_stats'] = {
            'branches_searched': len(branches),
            'branches_with_tasks': results['branches_with_tasks'],
            'total_tasks_estimated': results['total_tasks_estimated'],
            'samples_collected': len(results['task_samples'])
        }

        print("\n✅ Efficient search complete!")
        print(f"📊 Found tasks in {results['branches_with_tasks']} branches")
        print(f"📈 Estimated total tasks: {results['total_tasks_estimated']}")
        print(f"🧪 Collected {len(results['task_samples'])} task samples")

        return results

    def save_results(self, results: Dict):
        """Save search results."""
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Save full results
        results_file = self.output_dir / "efficient_branch_search.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)

        # Save summary report
        self.generate_summary_report(results)

        print(f"💾 Results saved to {self.output_dir}")

    def generate_summary_report(self, results: Dict):
        """Generate a summary report."""
        report_file = self.output_dir / "efficient_search_summary.md"

        with open(report_file, 'w') as f:
            f.write("# Efficient Remote Branch Task Search Summary\n\n")
            f.write(f"**Generated:** {os.popen('date').read().strip()}\n\n")

            stats = results['search_stats']
            f.write("## Executive Summary\n\n")
            f.write(f"- **Branches searched:** {stats['branches_searched']}\n")
            f.write(f"- **Branches with tasks:** {stats['branches_with_tasks']}\n")
            f.write(f"- **Estimated total tasks:** {stats['total_tasks_estimated']}\n")
            f.write(f"- **Task samples collected:** {stats['samples_collected']}\n\n")

            if results['high_priority_branches']:
                f.write("## High Priority Branches\n\n")
                f.write("Branches with significant task counts (>10 tasks):\n\n")
                for branch in results['high_priority_branches']:
                    count = results['branch_summary'][branch]['task_count']
                    f.write(f"- **{branch}**: {count} tasks\n")
                f.write("\n")

            f.write("## Branch Task Distribution\n\n")
            f.write("| Branch | Tasks | Status |\n")
            f.write("|--------|-------|--------|\n")

            for branch, info in results['branch_summary'].items():
                status = "✅ Has tasks" if info['task_count'] > 0 else "❌ No tasks"
                f.write(f"| {branch} | {info['task_count']} | {status} |\n")

            f.write("\n## Task Samples\n\n")
            f.write("Sample tasks from branches with content:\n\n")

            for sample in results['task_samples'][:10]:  # Show first 10 samples
                f.write(f"### {sample['task_id']}: {sample['title']}\n")
                f.write(f"**Branch:** {sample['branch']}\n")
                f.write(f"**File:** {sample['file_path']}\n\n")
                f.write(f"**Preview:**\n```\n{sample['content_preview'][:300]}...\n```\n\n")

            if len(results['task_samples']) > 10:
                f.write(f"*... and {len(results['task_samples']) - 10} more task samples*\n\n")

            f.write("## Recommendations\n\n")
            f.write("1. **Focus on high-priority branches** for comprehensive task extraction\n")
            f.write("2. **Review task samples** to understand content patterns\n")
            f.write("3. **Plan full extraction** from branches with significant task counts\n")
            f.write("4. **Consider branch consolidation** for tasks appearing in multiple branches\n")


def main():
    """Main execution."""
    repo_path = Path("/home/masum/github/EmailIntelligence")
    output_dir = Path("/home/masum/github/backlog/remote_branch_search")

    searcher = EfficientBranchSearcher(repo_path, output_dir)
    results = searcher.comprehensive_search()
    searcher.save_results(results)

    print("\n🎉 Efficient branch search complete!")
    print(f"📂 Results: {output_dir}")


if __name__ == "__main__":
    main()