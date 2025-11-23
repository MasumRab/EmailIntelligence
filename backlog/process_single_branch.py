#!/usr/bin/env python3
"""
Process Single High-Impact Branch

Processes one high-impact branch at a time with very small batches
to avoid timeouts and provide better progress tracking.
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional


class SingleBranchProcessor:
    """Processes a single high-impact branch with small batches."""

    def __init__(self, repo_path: Path, branch_name: str):
        self.repo_path = repo_path
        self.branch_name = branch_name
        self.output_dir = Path("/home/masum/github/backlog/branch_processing")
        self.output_dir.mkdir(exist_ok=True)

    def get_task_files(self) -> List[str]:
        """Get all task files from the branch."""
        print(f"🔍 Getting task files from {self.branch_name}...")

        result = subprocess.run(
            ["git", "ls-tree", "-r", "--name-only", f"origin/{self.branch_name}"],
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            print(f"❌ Failed to list files: {result.stderr}")
            return []

        # Filter for task files
        task_files = [
            line.strip() for line in result.stdout.split('\n')
            if line.strip() and 'backlog/tasks' in line and line.endswith('.md')
        ]

        print(f"📋 Found {len(task_files)} task files")
        return task_files

    def process_batch(self, batch: List[str], batch_num: int) -> Dict[str, Dict]:
        """Process a single batch of files."""
        print(f"  📦 Processing batch {batch_num} ({len(batch)} files)...")

        batch_tasks = {}

        for i, file_path in enumerate(batch):
            if (i + 1) % 5 == 0:
                print(f"    📄 {i + 1}/{len(batch)} files...")

            try:
                # Get file content with timeout
                result = subprocess.run(
                    ["git", "show", f"origin/{self.branch_name}:{file_path}"],
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True,
                    timeout=10  # 10 second timeout per file
                )

                if result.returncode == 0:
                    content = result.stdout
                    task_data = self.parse_task_content(content, file_path)
                    if task_data:
                        task_id = task_data['task_id']
                        batch_tasks[task_id] = task_data
                else:
                    print(f"    ⚠️  Failed to extract {file_path}")

            except subprocess.TimeoutExpired:
                print(f"    ⏰ Timeout extracting {file_path}")
                continue
            except Exception as e:
                print(f"    ❌ Error extracting {file_path}: {e}")
                continue

        print(f"  ✅ Batch {batch_num} complete: {len(batch_tasks)} tasks")
        return batch_tasks

    def parse_task_content(self, content: str, file_path: str) -> Optional[Dict]:
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
                'branch': self.branch_name,
                'file_path': file_path,
                'full_content': content
            }

        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return None

    def process_branch(self, batch_size: int = 10) -> Dict[str, Dict]:
        """Process the entire branch in small batches."""
        print(f"🚀 Processing branch: {self.branch_name}")

        # Get all task files
        task_files = self.get_task_files()
        if not task_files:
            return {}

        all_tasks = {}
        total_batches = (len(task_files) + batch_size - 1) // batch_size

        print(f"📊 Processing {len(task_files)} files in {total_batches} batches of {batch_size}")

        # Process in batches
        for i in range(0, len(task_files), batch_size):
            batch = task_files[i:i + batch_size]
            batch_num = (i // batch_size) + 1

            try:
                batch_tasks = self.process_batch(batch, batch_num)
                all_tasks.update(batch_tasks)

                # Save progress after each batch
                self.save_progress(all_tasks, batch_num, total_batches)

                print(f"📈 Progress: {len(all_tasks)} tasks collected so far\n")

            except Exception as e:
                print(f"❌ Error processing batch {batch_num}: {e}")
                # Save partial results
                self.save_progress(all_tasks, batch_num, total_batches, error=True)
                break

        # Final save
        self.save_final_results(all_tasks)
        print(f"🎉 Branch processing complete: {len(all_tasks)} tasks from {self.branch_name}")
        return all_tasks

    def save_progress(self, tasks: Dict, batch_num: int, total_batches: int, error: bool = False):
        """Save current progress."""
        progress_file = self.output_dir / f"{self.branch_name}_progress_batch_{batch_num}.json"
        status = "error" if error else "in_progress"

        progress_data = {
            "branch": self.branch_name,
            "batch_num": batch_num,
            "total_batches": total_batches,
            "tasks_collected": len(tasks),
            "status": status,
            "timestamp": "2025-11-24"
        }

        with open(progress_file, 'w') as f:
            json.dump(progress_data, f, indent=2)

    def save_final_results(self, tasks: Dict):
        """Save final results for the branch."""
        output_file = self.output_dir / f"{self.branch_name}_complete.json"

        result_data = {
            "branch": self.branch_name,
            "total_tasks": len(tasks),
            "tasks": tasks,
            "processing_complete": True,
            "timestamp": "2025-11-24"
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, indent=2, ensure_ascii=False)

        print(f"💾 Final results saved to: {output_file}")


def main():
    """Main execution."""
    if len(sys.argv) < 2:
        print("Usage: python process_single_branch.py <branch_name>")
        sys.exit(1)

    branch_name = sys.argv[1]
    repo_path = Path("/home/masum/github/EmailIntelligence")

    processor = SingleBranchProcessor(repo_path, branch_name)
    tasks = processor.process_branch(batch_size=5)  # Very small batches

    print(f"✅ Completed processing {branch_name}: {len(tasks)} tasks extracted")


if __name__ == "__main__":
    main()