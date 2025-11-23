#!/usr/bin/env python3
"""
Comprehensive Remote Branch Task Consolidation

Consolidates all tasks found across remote branches into the organized backlog system.
"""

import json
import shutil
from pathlib import Path
from typing import Dict, List, Set, Optional
from collections import defaultdict
from prd_parser import PRDParser


class ComprehensiveConsolidator:
    """Consolidates tasks from remote branches into organized backlog."""

    def __init__(self, backlog_root: Path, search_results: Path):
        self.backlog_root = backlog_root
        self.search_results = search_results
        self.organized_dir = backlog_root / "organized"
        self.consolidated_dir = backlog_root / "consolidated"
        self.repo_path = Path("/home/masum/github/EmailIntelligence")

        # Load search results
        with open(search_results / "efficient_branch_search.json", 'r') as f:
            self.search_data = json.load(f)

    def extract_all_remote_tasks(self) -> Dict[str, Dict]:
        """Extract all tasks from branches with significant task counts."""
        print("🔄 Extracting tasks from remote branches...")

        all_tasks = {}
        total_extracted = 0

        # First, extract from branches that have samples (found tasks)
        for branch, branch_info in self.search_data['branch_summary'].items():
            if not branch_info.get('has_samples', False):
                continue

            print(f"📥 Extracting from branch: {branch}")
            task_count = branch_info.get('task_count', 0)

            # Use batched processing for high-impact branches (>100 tasks)
            if task_count > 100:
                print(f"  📊 Large branch detected ({task_count} tasks) - using batched processing")
                branch_tasks = self.extract_branch_tasks_batched(branch, batch_size=50)
            else:
                branch_tasks = self.extract_branch_tasks_from_samples(branch, branch_info['samples'])

            all_tasks.update(branch_tasks)
            total_extracted += len(branch_tasks)
            print(f"  ✅ Extracted {len(branch_tasks)} tasks from {task_count} total")

        print(f"📊 Total tasks extracted: {total_extracted}")
        return all_tasks

    def extract_branch_tasks_from_samples(self, branch: str, samples: List[Dict]) -> Dict[str, Dict]:
        """Extract tasks from branch using the samples found in search results."""
        import subprocess

        branch_tasks = {}

        for sample in samples:
            file_path = sample['file_path']

            # Get full file content from git
            result = subprocess.run(
                ["git", "show", f"origin/{branch}:{file_path}"],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                content = result.stdout
                task_data = self.parse_task_content(content, file_path, branch)
                if task_data:
                    task_id = task_data['task_id']
                    branch_tasks[task_id] = task_data
            else:
                print(f"  ⚠️  Failed to extract {file_path} from {branch}")

        return branch_tasks

    def extract_branch_tasks_batched(self, branch: str, batch_size: int = 50) -> Dict[str, Dict]:
        """Extract all tasks from a branch using batched processing to avoid timeouts."""
        import subprocess

        print(f"  🔄 Starting batched extraction for {branch} (batch size: {batch_size})...")

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

        print(f"  📋 Found {len(all_task_files)} task files to process in batches")

        branch_tasks = {}
        total_processed = 0

        # Process files in batches
        for i in range(0, len(all_task_files), batch_size):
            batch = all_task_files[i:i + batch_size]
            batch_num = (i // batch_size) + 1
            total_batches = (len(all_task_files) + batch_size - 1) // batch_size

            print(f"  📦 Processing batch {batch_num}/{total_batches} ({len(batch)} files)...")

            batch_tasks = {}
            for file_path in batch:
                # Get file content
                result = subprocess.run(
                    ["git", "show", f"origin/{branch}:{file_path}"],
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True
                )

                if result.returncode == 0:
                    content = result.stdout
                    task_data = self.parse_task_content(content, file_path, branch)
                    if task_data:
                        task_id = task_data['task_id']
                        batch_tasks[task_id] = task_data

            branch_tasks.update(batch_tasks)
            total_processed += len(batch)
            print(f"    ✅ Batch {batch_num} complete: {len(batch_tasks)} tasks extracted")

            # Progress update
            if batch_num % 5 == 0 or batch_num == total_batches:
                print(f"  📊 Progress: {total_processed}/{len(all_task_files)} files processed")

        print(f"  🎯 Batched extraction complete: {len(branch_tasks)} tasks from {len(all_task_files)} files")
        return branch_tasks

    def extract_all_tasks_from_branch(self, branch: str) -> Dict[str, Dict]:
        """Extract all tasks from a specific branch by scanning all task files."""
        import subprocess

        print(f"  🔍 Scanning all task files in {branch}...")

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
        task_files = [
            line.strip() for line in result.stdout.split('\n')
            if line.strip() and 'backlog/tasks' in line and line.endswith('.md')
        ]

        print(f"  📋 Found {len(task_files)} task files")

        branch_tasks = {}
        processed = 0

        for file_path in task_files:
            # Get file content
            result = subprocess.run(
                ["git", "show", f"origin/{branch}:{file_path}"],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                content = result.stdout
                task_data = self.parse_task_content(content, file_path, branch)
                if task_data:
                    task_id = task_data['task_id']
                    branch_tasks[task_id] = task_data

            processed += 1
            if processed % 100 == 0:
                print(f"  📊 Processed {processed}/{len(task_files)} files...")

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

    def extract_prd_tasks(self) -> Dict[str, Dict]:
        """Extract tasks from PRD files in .taskmaster/docs."""
        print("📄 Extracting tasks from PRD files...")

        prd_parser = PRDParser()
        docs_dir = Path("/home/masum/github/EmailIntelligence/.taskmaster/docs")
        prd_tasks = prd_parser.parse_all_prd_files(docs_dir)

        # Convert list to dict with task_id as key
        prd_tasks_dict = {}
        for task in prd_tasks:
            task_id = task['task_id']
            prd_tasks_dict[task_id] = task

        print(f"✅ Extracted {len(prd_tasks_dict)} PRD tasks")
        return prd_tasks_dict

    def deduplicate_tasks(self, all_tasks: Dict[str, Dict]) -> Dict:
        """Identify and group duplicate tasks across branches."""
        print("🔍 Analyzing duplicates across branches...")

        # Group tasks by content hash
        content_hashes = defaultdict(list)

        for task_id, task_data in all_tasks.items():
            # Create content hash for deduplication
            content = task_data.get('content', '')
            content_hash = hash(content)
            content_hashes[content_hash].append(task_data)

        # Separate unique and duplicate tasks
        unique_tasks = {}
        duplicate_groups = {}

        for content_hash, tasks in content_hashes.items():
            if len(tasks) == 1:
                # Unique task
                task = tasks[0]
                unique_tasks[task['task_id']] = task
            else:
                # Duplicate group
                group_id = f"dup_group_{len(duplicate_groups) + 1}"
                duplicate_groups[group_id] = {
                    'tasks': tasks,
                    'branches': list(set(t['branch'] for t in tasks)),
                    'task_count': len(tasks),
                    'content_hash': content_hash
                }

        print(f"✅ Found {len(unique_tasks)} unique tasks")
        print(f"📋 Found {len(duplicate_groups)} duplicate groups")

        return {
            'unique_tasks': unique_tasks,
            'duplicate_groups': duplicate_groups,
            'stats': {
                'total_tasks': len(all_tasks),
                'unique_tasks': len(unique_tasks),
                'duplicate_groups': len(duplicate_groups),
                'duplication_rate': len(all_tasks) - len(unique_tasks)
            }
        }

    def consolidate_into_categories(self, deduped_data: Dict) -> Dict:
        """Consolidate tasks into organized categories."""
        print("📂 Consolidating into categories...")

        unique_tasks = deduped_data['unique_tasks']

        # Category definitions
        categories = {
            'consolidation_migration': {
                'name': 'Consolidation & Migration',
                'keywords': ['consolidat', 'migrat', 'centraliz', 'distribut', 'worktree', 'orchestrat', 'merge', 'integrat'],
                'tasks': {}
            },
            'branch_management': {
                'name': 'Branch Management & Alignment',
                'keywords': ['branch', 'align', 'pr ', 'merge', 'extract', 'split', 'rebase', 'pull', 'push'],
                'tasks': {}
            },
            'validation_testing': {
                'name': 'Validation & Testing',
                'keywords': ['validat', 'test', 'verif', 'check', 'assert', 'performance', 'monitor'],
                'tasks': {}
            },
            'documentation_research': {
                'name': 'Documentation & Research',
                'keywords': ['document', 'research', 'summary', 'analysis', 'review', 'spec', 'plan'],
                'tasks': {}
            },
            'development_implementation': {
                'name': 'Development & Implementation',
                'keywords': ['implement', 'develop', 'code', 'feature', 'function', 'api', 'database'],
                'tasks': {}
            },
            'security_hardening': {
                'name': 'Security & Hardening',
                'keywords': ['secur', 'auth', 'encrypt', 'audit', 'compliance', 'vulnerab'],
                'tasks': {}
            }
        }

        # Categorize tasks
        uncategorized = {}

        for task_id, task_data in unique_tasks.items():
            content = task_data.get('content', '').lower()
            title = task_data.get('title', '').lower()
            search_text = f"{content} {title}"

            categorized = False
            for category_key, category_info in categories.items():
                for keyword in category_info['keywords']:
                    if keyword.lower() in search_text:
                        categories[category_key]['tasks'][task_id] = task_data
                        categorized = True
                        break
                if categorized:
                    break

            if not categorized:
                uncategorized[task_id] = task_data

        # Add uncategorized as a separate category
        categories['uncategorized'] = {
            'name': 'Uncategorized',
            'keywords': [],
            'tasks': uncategorized
        }

        # Calculate stats
        category_stats = {}
        for category_key, category_info in categories.items():
            task_count = len(category_info['tasks'])
            category_stats[category_key] = {
                'name': category_info['name'],
                'task_count': task_count,
                'percentage': (task_count / len(unique_tasks)) * 100 if unique_tasks else 0
            }

        return {
            'categories': categories,
            'category_stats': category_stats,
            'total_categorized': sum(len(cat['tasks']) for cat in categories.values())
        }

    def save_consolidated_tasks(self, consolidation_data: Dict):
        """Save consolidated tasks to organized structure."""
        print("💾 Saving consolidated tasks...")

        self.consolidated_dir.mkdir(parents=True, exist_ok=True)

        # Save category files
        for category_key, category_info in consolidation_data['categories'].items():
            category_dir = self.consolidated_dir / category_key
            category_dir.mkdir(exist_ok=True)

            # Save individual task files
            for task_id, task_data in category_info['tasks'].items():
                filename = f"{task_id} - {task_data['title'].replace('/', '_')}.md"
                file_path = category_dir / filename

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(task_data['full_content'])

            # Save category README
            readme_path = category_dir / "README.md"
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(f"# {category_info['name']}\n\n")
                f.write(f"**Tasks:** {len(category_info['tasks'])}\n\n")
                f.write("## Task List\n\n")

                for task_id, task_data in category_info['tasks'].items():
                    status = task_data.get('status', 'Unknown')
                    title = task_data.get('title', '')
                    branch = task_data.get('branch', 'Unknown')
                    f.write(f"- **{task_id}**: {title} (*{status}* from {branch})\n")

                f.write("\n")

        # Save consolidation summary
        summary_path = self.consolidated_dir / "CONSOLIDATION_SUMMARY.md"
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write("# Comprehensive Task Consolidation Summary\n\n")
            f.write("**Generated:** Auto-generated from remote branch analysis\n\n")

            # Overall stats
            f.write("## Overall Statistics\n\n")
            f.write(f"- **Branches analyzed:** {len([b for b in self.search_data['branch_summary'].values() if b['task_count'] > 0])}\n")
            f.write(f"- **Total tasks extracted:** {consolidation_data.get('total_categorized', 0)}\n")
            f.write(f"- **Categories created:** {len(consolidation_data['categories'])}\n\n")

            # Category breakdown
            f.write("## Category Breakdown\n\n")
            f.write("| Category | Tasks | Percentage |\n")
            f.write("|----------|-------|------------|\n")

            for cat_key, stats in consolidation_data['category_stats'].items():
                f.write(f"| {stats['name']} | {stats['task_count']} | {stats['percentage']:.1f}% |\n")

            f.write("\n## Categories\n\n")

            for cat_key, cat_info in consolidation_data['categories'].items():
                stats = consolidation_data['category_stats'][cat_key]
                f.write(f"### {stats['name']}\n")
                f.write(f"- **Tasks:** {stats['task_count']}\n")
                f.write(f"- **Location:** `consolidated/{cat_key}/`\n")
                f.write(f"- **Keywords:** {', '.join(cat_info['keywords'])}\n\n")

    def generate_consolidation_report(self, deduped_data: Dict, consolidation_data: Dict):
        """Generate comprehensive consolidation report."""
        report_path = self.consolidated_dir / "consolidation_report.md"

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Remote Branch Task Consolidation Report\n\n")
            f.write("**Consolidation completed from comprehensive remote branch analysis**\n\n")

            # Executive summary
            f.write("## Executive Summary\n\n")
            stats = deduped_data.get('stats', {})
            f.write(f"- **Total tasks processed:** {stats.get('total_tasks', 0)}\n")
            f.write(f"- **Unique tasks retained:** {stats.get('unique_tasks', 0)}\n")
            f.write(f"- **Duplicate groups identified:** {stats.get('duplicate_groups', 0)}\n")
            f.write(f"- **Duplication elimination:** {stats.get('duplication_rate', 0)} tasks\n")
            f.write(f"- **Final categorized tasks:** {consolidation_data.get('total_categorized', 0)}\n\n")

            # Branch analysis
            f.write("## Branch Analysis\n\n")
            branches_with_tasks = [
                (branch, info) for branch, info in self.search_data['branch_summary'].items()
                if info['task_count'] > 0
            ]
            branches_with_tasks.sort(key=lambda x: x[1]['task_count'], reverse=True)

            f.write("| Branch | Tasks | Contribution |\n")
            f.write("|--------|-------|--------------|\n")

            total_tasks = sum(info['task_count'] for _, info in branches_with_tasks)
            for branch, info in branches_with_tasks[:15]:  # Top 15
                percentage = (info['task_count'] / total_tasks) * 100
                f.write(f"| {branch} | {info['task_count']} | {percentage:.1f}% |\n")

            f.write("\n")

            # Consolidation recommendations
            f.write("## Consolidation Recommendations\n\n")
            f.write("### Immediate Actions\n")
            f.write("1. **Review high-duplication branches** for consolidation opportunities\n")
            f.write("2. **Merge similar tasks** across branches where appropriate\n")
            f.write("3. **Update task references** to point to consolidated versions\n")
            f.write("4. **Archive redundant branches** after consolidation\n\n")

            f.write("### Long-term Strategy\n")
            f.write("1. **Implement centralized task management** to prevent future duplication\n")
            f.write("2. **Establish branch-specific task guidelines**\n")
            f.write("3. **Regular consolidation reviews** to maintain organization\n")
            f.write("4. **Cross-branch task visibility** for development teams\n\n")

            # Category utilization
            f.write("## Category Utilization\n\n")
            high_utilization = [
                (stats['name'], stats['task_count'], stats['percentage'])
                for stats in consolidation_data['category_stats'].values()
                if stats['percentage'] > 5  # Categories with >5% of tasks
            ]
            high_utilization.sort(key=lambda x: x[2], reverse=True)

            for name, count, percentage in high_utilization:
                f.write(f"- **{name}**: {count} tasks ({percentage:.1f}%)\n")

            f.write("\n## Next Steps\n\n")
            f.write("1. Review consolidated categories for completeness\n")
            f.write("2. Update development workflows to use consolidated tasks\n")
            f.write("3. Implement automated consolidation checks\n")
            f.write("4. Monitor for new duplication patterns\n")


def main():
    """Main consolidation execution."""
    backlog_root = Path("/home/masum/github/backlog")
    search_results = Path("/home/masum/github/backlog/remote_branch_search")

    consolidator = ComprehensiveConsolidator(backlog_root, search_results)

    # Extract all remote tasks
    print("🚀 Starting comprehensive task consolidation...")
    all_tasks = consolidator.extract_all_remote_tasks()

    # Extract PRD tasks
    prd_tasks = consolidator.extract_prd_tasks()
    all_tasks.update(prd_tasks)

    # Deduplicate
    deduped_data = consolidator.deduplicate_tasks(all_tasks)

    # Consolidate into categories
    consolidation_data = consolidator.consolidate_into_categories(deduped_data)

    # Save consolidated structure
    consolidator.save_consolidated_tasks(consolidation_data)

    # Generate reports
    consolidator.generate_consolidation_report(deduped_data, consolidation_data)

    print("🎉 Comprehensive consolidation complete!")
    print(f"📂 Consolidated tasks: {consolidation_data.get('total_categorized', 0)}")
    print(f"📋 Categories created: {len(consolidation_data['categories'])}")
    print(f"📊 Duplicates eliminated: {deduped_data['stats'].get('duplication_rate', 0)}")
    print(f"📁 Results in: {backlog_root / 'consolidated'}")


if __name__ == "__main__":
    main()