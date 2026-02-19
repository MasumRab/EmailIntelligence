#!/usr/bin/env python3
"""
Documentation Inventory & Analysis Tool

Comprehensive analysis of .taskmaster documentation:
- File inventory with metadata
- Content categorization
- Link integrity checking
- TODO/FIXME detection
- Document relationship mapping
"""

import argparse
import json
import os
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Tuple
import subprocess


class DocumentationAnalyzer:
    """Analyze documentation files in .taskmaster directory"""

    def __init__(self, base_path: str = ".taskmaster"):
        self.base_path = Path(base_path).resolve()
        self.results = {
            "inventory": [],
            "categories": defaultdict(list),
            "links": {"valid": [], "broken": []},
            "todos": [],
            "relationships": [],
            "statistics": {}
        }

    def find_all_markdown_files(self) -> List[Path]:
        """Find all markdown files in the base path"""
        # Use absolute path for searching
        abs_path = self.base_path.resolve()
        md_files = list(abs_path.rglob("*.md"))
        txt_files = list(abs_path.rglob("*.txt"))
        # Filter out node_modules, .git, __pycache__
        exclude_dirs = {'node_modules', '.git', '__pycache__', '.pytest_cache'}
        filtered = []
        for f in md_files + txt_files:
            if not any(exclude in str(f) for exclude in exclude_dirs):
                filtered.append(f)
        return filtered

    def get_file_metadata(self, file_path: Path) -> Dict[str, Any]:
        """Extract metadata from a documentation file"""
        try:
            stat = file_path.stat()
            return {
                "path": str(file_path),
                "relative_path": str(file_path.relative_to(self.base_path)),
                "size_bytes": stat.st_size,
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "lines": self.count_lines(file_path),
                "words": self.count_words(file_path),
            }
        except Exception as e:
            return {"path": str(file_path), "error": str(e)}

    def count_lines(self, file_path: Path) -> int:
        """Count non-empty lines in file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return sum(1 for line in f if line.strip())
        except:
            return 0

    def count_words(self, file_path: Path) -> int:
        """Count words in file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return len(f.read().split())
        except:
            return 0

    def categorize_document(self, file_path: Path) -> str:
        """Categorize document based on path and content"""
        path_str = str(file_path).lower()
        name = file_path.name.lower()

        # Category rules
        if "task" in path_str and ("spec" in name or "task_" in name):
            return "task_specifications"
        elif "prd" in name:
            return "prd_documents"
        elif "guide" in name or "howto" in name:
            return "guides"
        elif "report" in name:
            return "reports"
        elif "summary" in name:
            return "summaries"
        elif "analysis" in name:
            return "analysis"
        elif "plan" in name or "strategy" in name:
            return "plans"
        elif "template" in name:
            return "templates"
        elif "test" in name:
            return "test_documentation"
        elif name in ["readme.md", "qwen.md", "claude.md", "agent.md", "agents.md"]:
            return "core_documentation"
        elif "archive" in path_str:
            return "archived"
        else:
            return "other"

    def extract_links(self, file_path: Path) -> List[str]:
        """Extract all markdown links from a file"""
        links = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                # Match markdown links: [text](url)
                link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
                matches = re.findall(link_pattern, content)
                links = [match[1] for match in matches if not match[1].startswith('http')]
        except:
            pass
        return links

    def find_todos(self, file_path: Path) -> List[Dict[str, Any]]:
        """Find TODO/FIXME/XXX markers in file"""
        todos = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    for marker in ['TODO', 'FIXME', 'XXX', 'HACK', 'TBD']:
                        if marker in line:
                            todos.append({
                                "file": str(file_path),
                                "line": line_num,
                                "marker": marker,
                                "content": line.strip()[:100]
                            })
        except:
            pass
        return todos

    def extract_references(self, file_path: Path) -> List[str]:
        """Extract document references (See also, Related to, etc.)"""
        references = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                patterns = [
                    r'See also[:\s]*([^\n]+)',
                    r'Related to[:\s]*([^\n]+)',
                    r'References?[:\s]*([^\n]+)',
                    r'Continued in[:\s]*([^\n]+)',
                    r'\[([^\]]+)\]\(([^\)]+\.(md|txt))\)',
                ]
                for pattern in patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    references.extend([m[0] if isinstance(m, tuple) else m for m in matches])
        except:
            pass
        return references

    def get_git_history(self, file_path: Path) -> Dict[str, Any]:
        """Get git history for a file"""
        try:
            # Get commit count
            result = subprocess.run(
                ["git", "log", "--oneline", "--", str(file_path)],
                capture_output=True,
                text=True,
                cwd=self.base_path
            )
            commits = result.stdout.strip().split('\n') if result.stdout.strip() else []

            # Get first commit (creation)
            created = commits[-1] if commits else None
            # Get last commit (modification)
            modified = commits[0] if commits else None

            return {
                "commit_count": len(commits),
                "first_commit": created,
                "last_commit": modified,
            }
        except:
            return {"commit_count": 0, "error": "Git history unavailable"}

    def analyze(self) -> Dict[str, Any]:
        """Run complete documentation analysis"""
        print("🔍 Starting documentation analysis...")

        # Find all files
        files = self.find_all_markdown_files()
        print(f"📁 Found {len(files)} documentation files")

        # Analyze each file
        for i, file_path in enumerate(files, 1):
            if i % 100 == 0:
                print(f"  [{i}/{len(files)}] ...")
            
            metadata = self.get_file_metadata(file_path)
            category = self.categorize_document(file_path)
            links = self.extract_links(file_path)
            todos = self.find_todos(file_path)
            references = self.extract_references(file_path)
            git_history = self.get_git_history(file_path) if Path(".git").exists() else {}

            # Combine all data
            file_data = {
                **metadata,
                "category": category,
                "links": links,
                "todos": todos,
                "references": references,
                "git_history": git_history
            }

            self.results["inventory"].append(file_data)
            self.results["categories"][category].append(str(file_path))

            if todos:
                self.results["todos"].extend(todos)

            if references:
                self.results["relationships"].append({
                    "file": str(file_path),
                    "references": references
                })

        # Calculate statistics
        self.results["statistics"] = {
            "total_files": len(files),
            "total_lines": sum(f.get("lines", 0) for f in self.results["inventory"]),
            "total_words": sum(f.get("words", 0) for f in self.results["inventory"]),
            "total_todos": len(self.results["todos"]),
            "categories": {k: len(v) for k, v in self.results["categories"].items()},
            "files_with_todos": len(set(t["file"] for t in self.results["todos"])),
        }

        print("✅ Analysis complete!")
        return self.results

    def save_report(self, output_file: str = "documentation_inventory.json"):
        """Save analysis results to JSON file"""
        output_path = Path(output_file)
        if not output_path.is_absolute():
            output_path = self.base_path / output_file
        
        # Create parent directories if needed
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, default=str)
        print(f"📄 Report saved to {output_path}")

    def print_summary(self):
        """Print analysis summary to console"""
        stats = self.results["statistics"]

        print("\n" + "="*60)
        print("📊 DOCUMENTATION INVENTORY SUMMARY")
        print("="*60)
        print(f"Total Files:        {stats['total_files']}")
        print(f"Total Lines:        {stats['total_lines']:,}")
        print(f"Total Words:        {stats['total_words']:,}")
        print(f"Files with TODOs:   {stats['files_with_todos']}")
        print(f"Total TODOs:        {stats['total_todos']}")
        print("\n📁 Files by Category:")
        for category, count in sorted(stats['categories'].items(), key=lambda x: -x[1]):
            print(f"  {category:30} {count:4} files")
        print("="*60)

        # Show top TODO files
        if self.results["todos"]:
            todo_by_file = defaultdict(int)
            for todo in self.results["todos"]:
                todo_by_file[todo["file"]] += 1

            print("\n⚠️  Files with Most TODOs:")
            for file, count in sorted(todo_by_file.items(), key=lambda x: -x[1])[:5]:
                rel_path = Path(file).relative_to(self.base_path)
                print(f"  {str(rel_path):50} {count} TODOs")


def main():
    parser = argparse.ArgumentParser(
        description="Analyze .taskmaster documentation inventory"
    )
    parser.add_argument(
        "--output", "-o",
        default="documentation_inventory.json",
        help="Output JSON file (default: documentation_inventory.json)"
    )
    parser.add_argument(
        "--path", "-p",
        default=".taskmaster",
        help="Base path to analyze (default: .taskmaster)"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress progress output"
    )

    args = parser.parse_args()

    analyzer = DocumentationAnalyzer(args.path)
    results = analyzer.analyze()
    analyzer.save_report(args.output)

    if not args.quiet:
        analyzer.print_summary()


if __name__ == "__main__":
    main()
