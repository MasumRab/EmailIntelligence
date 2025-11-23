#!/usr/bin/env python3
"""
Process High-Impact Branches with Batched Extraction

Targeted script to process branches with 400+ tasks using batched processing
to avoid timeouts.
"""

import json
import shutil
from pathlib import Path
from typing import Dict, List, Set, Optional
from collections import defaultdict
from prd_parser import PRDParser


class HighImpactBranchProcessor:
    """Processes high-impact branches (400+ tasks) with batched extraction."""

    def __init__(self, backlog_root: Path, search_results: Path):
        self.backlog_root = backlog_root
        self.search_results = search_results
        self.consolidated_dir = backlog_root / "consolidated"
        self.repo_path = Path("/home/masum/github/EmailIntelligence")

        # Load search results
        with open(search_results / "efficient_branch_search.json", 'r') as f:
            self.search_data = json.load(f)

        # High-impact branches (400+ tasks)
        self.high_impact_branches = [
            'feature-notmuch-tagging-1',      # 566 tasks
            'pr-179',                         # 402 tasks
            'pr-179-from-f11b20e',           # 566 tasks
            'pr-179-new',                     # 402 tasks
            'pr-179-patch-clean-1762881335', # 566 tasks
            'align-feature-notmuch-tagging-1',        # 405 tasks
            'align-feature-notmuch-tagging-1-v2'      # 405 tasks
        ]

    def process_high_impact_branches(self) -> Dict[str, Dict]:
        """Process all high-impact branches with batched extraction."""
        print("🎯 Processing high-impact branches with batched extraction...")

        all_tasks = {}

        for branch in self.high_impact_branches:
            if branch not in self.search_data['branch_summary']:
                print(f"⚠️  Branch {branch} not found in search data, skipping")
                continue

            branch_info = self.search_data['branch_summary'][branch]
            task_count = branch_info.get('task_count', 0)

            print(f"📊 Processing {branch} ({task_count} tasks)...")

            # Use batched extraction for all high-impact branches
            branch_tasks = self.extract_branch_tasks_batched(branch, batch_size=25)
            all_tasks.update(branch_tasks)

            print(f"✅ Completed {branch}: {len(branch_tasks)} tasks extracted\n")

        print(f"🎉 High-impact branch processing complete: {len(all_tasks)} total tasks")
        return all_tasks

    def extract_branch_tasks_batched(self, branch: str, batch_size: int = 25) -> Dict[str, Dict]:
        """Extract all tasks from a branch using batched processing."""
        import subprocess

        print(f"  🔄 Batched extraction for {branch} (batch size: {batch_size})...")

        # Get all task files from branch
        result = subprocess.run(
            ["git", "ls-tree", "-r", "--name-only", f"origin/{branch}"],
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"  ❌ Failed to list files in branch {branch}")
            return {}

        # Filter for task files
        all_task_files = [
            line.strip() for line in result.stdout.split('\n')
            if line.strip() and 'backlog/tasks' in line and line.endswith('.md')
        ]

        print(f"  📋 Found {len(all_task_files)} task files")

        branch_tasks = {}
        total_processed = 0

        # Process files in batches
        for i in range(0, len(all_task_files), batch_size):
            batch = all_task_files[i:i + batch_size]
            batch_num = (i // batch_size) + 1
            total_batches = (len(all_task_files) + batch_size - 1) // batch_size

            print(f"  📦 Batch {batch_num}/{total_batches} ({len(batch)} files)...")

            batch_tasks = {}
            for file_path in batch:
                # Get file content
                result = subprocess.run(
                    ["git", "show", f"origin/{branch}:{file_path}"],
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True,
                    timeout=30  # 30 second timeout per file
                )

                if result.returncode == 0:
                    content = result.stdout
                    task_data = self.parse_task_content(content, file_path, branch)
                    if task_data:
                        task_id = task_data['task_id']
                        batch_tasks[task_id] = task_data
                else:
                    print(f"    ⚠️  Failed to extract {file_path}")

            branch_tasks.update(batch_tasks)
            total_processed += len(batch)
            print(f"    ✅ {len(batch_tasks)} tasks extracted from batch")

        print(f"  🎯 {branch} complete: {len(branch_tasks)} tasks")
        return branch_tasks

    def parse_task_content(self, content: str, file_path: str, branch: str) -> Optional[Dict]:
        """Parse task content and metadata."""
        try:
            # Extract frontmatter
            frontmatter = {}
            body = content

            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    try:
                        import yaml
                        frontmatter = yaml.safe_load(parts[1]) or {}
                        body = parts[2].strip()
                    except:
                        body = content

            # Extract task ID
            task_id = frontmatter.get('id')
            if not task_id:
                import re
                match = re.search(r'(task-\d+(?:\.\d+)?)', file_path, re.IGNORECASE)
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
                'branch': branch,
                'file_path': file_path,
                'full_content': content
            }

        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return None

    def merge_with_existing_consolidation(self, new_tasks: Dict[str, Dict]):
        """Merge new tasks with existing consolidated tasks."""
        print("🔄 Merging with existing consolidation...")

        # Load existing consolidation data if available
        existing_tasks = {}
        master_backlog_path = self.consolidated_dir / "master_backlog.md"

        if master_backlog_path.exists():
            print("  📖 Found existing consolidation, loading...")
            # For now, just add the new tasks
            # In a full implementation, we'd deduplicate against existing tasks
            pass

        # Add new tasks
        existing_tasks.update(new_tasks)

        print(f"  📊 Total tasks after merge: {len(existing_tasks)}")
        return existing_tasks

    def save_high_impact_results(self, tasks: Dict[str, Dict]):
        """Save the high-impact branch processing results."""
        print("💾 Saving high-impact branch results...")

        # Create high-impact directory
        hi_dir = self.consolidated_dir / "high_impact_branches"
        hi_dir.mkdir(exist_ok=True)

        # Save raw task data
        hi_tasks_path = hi_dir / "high_impact_tasks.json"
        with open(hi_tasks_path, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, indent=2, ensure_ascii=False)

        # Generate summary
        summary_path = hi_dir / "high_impact_summary.md"
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write("# High-Impact Branch Processing Results\n\n")
            f.write("**Processed:** High-impact branches with 400+ tasks each\n\n")

            # Branch breakdown
            f.write("## Branch Breakdown\n\n")
            branch_counts = {}
            for task in tasks.values():
                branch = task['branch']
                branch_counts[branch] = branch_counts.get(branch, 0) + 1

            f.write("| Branch | Tasks Extracted |\n")
            f.write("|--------|----------------|\n")
            for branch, count in sorted(branch_counts.items()):
                f.write(f"| {branch} | {count} |\n")

            f.write(f"\n**Total:** {len(tasks)} tasks from {len(branch_counts)} branches\n")

        print(f"  📁 Results saved to: {hi_dir}")


def main():
    """Main processing execution."""
    backlog_root = Path("/home/masum/github/backlog")
    search_results = Path("/home/masum/github/backlog/remote_branch_search")

    processor = HighImpactBranchProcessor(backlog_root, search_results)

    print("🚀 Starting high-impact branch processing...")
    high_impact_tasks = processor.process_high_impact_branches()

    # Merge with existing consolidation
    merged_tasks = processor.merge_with_existing_consolidation(high_impact_tasks)

    # Save results
    processor.save_high_impact_results(merged_tasks)

    print("🎉 High-impact branch processing complete!")
    print(f"📊 Processed {len(high_impact_tasks)} tasks from {len(processor.high_impact_branches)} branches")


if __name__ == "__main__":
    main()