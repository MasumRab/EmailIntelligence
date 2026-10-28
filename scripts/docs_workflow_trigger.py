#!/usr/bin/env python3
"""
Documentation Workflow Trigger

Orchestrates the documentation branch workflow by triggering analysis,
strategy determination, and review creation when documentation changes are detected.
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import List


class DocsWorkflowTrigger:
    def __init__(self):
        self.scripts_dir = Path("scripts")

    def get_recent_docs_commits(self) -> List[str]:
        """Get documentation-related commits from recent history."""
        try:
            # Get commits that modified docs/ in the last commit
            result = subprocess.run(
                ["git", "log", "--oneline", "-1", "--grep", "docs:"],
                capture_output=True, text=True, check=True
            )
            return result.stdout.strip().split('\n') if result.stdout.strip() else []
        except subprocess.CalledProcessError:
            return []

    def get_modified_docs_files(self) -> List[str]:
        """Get documentation files modified in the current HEAD commit."""
        try:
            result = subprocess.run(
                ["git", "show", "--name-only", "--pretty=format:", "HEAD"],
                capture_output=True, text=True, check=True
            )
            files = result.stdout.strip().split('\n')
            return [f for f in files if f.startswith('docs/') and f.endswith('.md') and not f.startswith('docs/reviews/')]
        except subprocess.CalledProcessError:
            return []

    def trigger_analysis(self, doc_files: List[str]):
        """Trigger content analysis for modified documentation files."""
        if not doc_files:
            print("No documentation files to analyze")
            return

        print(f"Analyzing {len(doc_files)} documentation files...")

        for doc_file in doc_files:
            print(f"Analyzing: {doc_file}")

            # Run content analyzer
            try:
                result = subprocess.run([
                    sys.executable, str(self.scripts_dir / "docs_content_analyzer.py"),
                    doc_file, "--save"
                ], capture_output=True, text=True, check=True)

                print(f"✓ Analysis completed for {doc_file}")

            except subprocess.CalledProcessError as e:
                print(f"✗ Analysis failed for {doc_file}: {e}")
                print(f"Error output: {e.stderr}")

    def trigger_strategy_determination(self, doc_files: List[str]):
        """Trigger merge strategy determination for analyzed files."""
        if not doc_files:
            print("No documentation files to process")
            return

        print(f"Determining strategies for {len(doc_files)} documentation files...")

        for doc_file in doc_files:
            print(f"Processing strategy for: {doc_file}")

            try:
                # Run merge strategist
                result = subprocess.run([
                    sys.executable, str(self.scripts_dir / "docs_merge_strategist.py"),
                    "--review", doc_file
                ], capture_output=True, text=True, check=True)

                print(f"✓ Strategy processed for {doc_file}")
                print(result.stdout.strip())

            except subprocess.CalledProcessError as e:
                print(f"✗ Strategy determination failed for {doc_file}: {e}")
                print(f"Error output: {e.stderr}")

    def run_workflow(self):
        """Run the complete documentation workflow."""
        print("🚀 Starting Documentation Branch Workflow")
        print("=" * 50)

        # Check if there are recent docs commits
        recent_commits = self.get_recent_docs_commits()
        if not recent_commits:
            print("No recent documentation commits found")
            return

        print(f"Found {len(recent_commits)} recent documentation commits")

        # Get modified files
        modified_files = self.get_modified_docs_files()
        if not modified_files:
            print("No documentation files modified in recent commits")
            return

        print(f"Modified documentation files: {len(modified_files)}")
        for file in modified_files:
            print(f"  - {file}")

        # Step 1: Analyze content
        print("\n📊 Step 1: Content Analysis")
        self.trigger_analysis(modified_files)

        # Step 2: Determine strategies
        print("\n🎯 Step 2: Strategy Determination")
        self.trigger_strategy_determination(modified_files)

        # Step 3: Show status
        print("\n📋 Step 3: Review Status")
        try:
            result = subprocess.run([
                sys.executable, str(self.scripts_dir / "docs_review_manager.py"),
                "--dashboard"
            ], capture_output=True, text=True, check=True)

            print(result.stdout.strip())

        except subprocess.CalledProcessError as e:
            print(f"Failed to show review status: {e}")

        print("\n✅ Documentation workflow completed")
        print("Review the generated review requests in docs/reviews/")


def main():
    trigger = DocsWorkflowTrigger()
    trigger.run_workflow()


if __name__ == "__main__":
    main()