#!/usr/bin/env python3
"""
Conflict Detection and Complexity Analysis

Find all files with merge conflicts and rank them by severity.
"""

import subprocess
import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from collections import defaultdict


class ConflictsCommand:
    """
    Command to detect and analyze Git merge conflicts.
    """

    def __init__(self, path: str):
        self.repo_path = Path(path).resolve()
        self.conflict_pattern = re.compile(
            r"^<<<<<<< [^\n]*\n"
            r"^=======\n?"
            r"^>>>>>>> [^\n]*$"
        )

    def _run_git(self, args: List[str], check: bool = False) -> str:
        """Run a git command."""
        result = subprocess.run(
            ["git"] + args,
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=check
        )
        return result.stdout.strip()

    def find_conflict_files(self) -> List[str]:
        """
        Find all files with merge conflict markers.
        
        Returns:
            List of file paths with conflicts
        """
        output = self._run_git(["grep", "-rl", "<<<<<<<", "."])
        if output:
            return output.split('\n')
        return []

    def get_conflict_details(self, file_path: str) -> List[Dict]:
        """
        Get detailed information about conflicts in a file.
        
        Args:
            file_path: Path to file
            
        Returns:
            List of conflict details
        """
        try:
            with open(self.repo_path / file_path, 'r') as f:
                content = f.read()
            
            conflicts = []
            matches = list(self.conflict_pattern.finditer(content))
            
            for i, match in enumerate(matches, 1):
                lines = content[:match.start()].count('\n') + 1
                context_before = content[max(0, match.start() - 200):match.start()]
                context_after = content[match.end():match.end() + 200]
                
                conflicts.append({
                    "id": i,
                    "file": file_path,
                    "line": lines,
                    "start_pos": match.start(),
                    "end_pos": match.end(),
                    "context_before": context_before.strip(),
                    "context_after": context_after.strip()[:100]
                })
            
            return conflicts
        except Exception as e:
            return [{"error": str(e), "file": file_path}]

    def rank_conflicts(self, conflicts: List[Dict]) -> List[Dict]:
        """
        Rank conflicts by complexity.
        
        Returns sorted list by priority (most complex first)
        """
        def complexity_score(conflict: Dict) -> int:
            """Calculate complexity score for a conflict."""
            score = 0
            
            # Check if this is in a critical file
            critical_files = ["setup/launch.py", "pyproject.toml", "requirements.txt"]
            if any(cf in conflict["file"] for cf in critical_files):
                score += 10
            
            # Check context size (larger context = more complex)
            context_len = len(conflict.get("context_before", ""))
            if context_len > 500:
                score += 5
            elif context_len > 200:
                score += 3
            
            # Penalize multiple conflicts in same file
            score += conflicts.count(lambda c: c["file"] == conflict["file"]) * 2
            
            return score
        
        # Add complexity scores and sort
        for conflict in conflicts:
            conflict["complexity_score"] = complexity_score(conflict)
        
        return sorted(conflicts, key=lambda c: c["complexity_score"], reverse=True)

    def analyze(self) -> Dict:
        """
        Full conflict analysis.
        
        Returns:
            Dict with conflict statistics and ranking
        """
        conflicted_files = self.find_conflict_files()
        
        if not conflicted_files:
            return {
                "status": "clean",
                "conflict_count": 0,
                "files_with_conflicts": 0,
                "conflicts": []
            }
        
        all_conflicts = []
        for file_path in conflicted_files:
            file_conflicts = self.get_conflict_details(file_path)
            all_conflicts.extend(file_conflicts)
        
        ranked_conflicts = self.rank_conflicts(all_conflicts)
        
        # Group by file
        by_file = defaultdict(list)
        for conflict in ranked_conflicts:
            by_file[conflict["file"]].append(conflict)
        
        return {
            "status": "conflicts_found",
            "conflict_count": len(ranked_conflicts),
            "files_with_conflicts": len(by_file),
            "files": dict(by_file),
            "ranked_conflicts": ranked_conflicts
        }

    def print_report(self, analysis: Optional[Dict] = None) -> None:
        """Print conflict report."""
        if analysis is None:
            analysis = self.analyze()
        
        if analysis["status"] == "clean":
            print("\n✅ No merge conflicts detected\n")
            return
        
        print(f"\n❌ {analysis['conflict_count']} conflict(s) found in {analysis['files_with_conflicts']} file(s)")
        print("-" * 60)
        
        for file_path, conflicts in analysis["files"].items():
            print(f"\n📁 {file_path}")
            print(f"   {len(conflicts)} conflict(s)")
            
            for i, conflict in enumerate(conflicts[:5], 1):  # Show top 5 per file
                print(f"\n   Conflict #{i} at line {conflict['line']}")
                print(f"   Complexity: {conflict['complexity_score']}/10")
                
        print("\n" + "-" * 60)
        print("🎯 Priority: Fix highest complexity conflicts first\n")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Detect and rank Git conflicts")
    parser.add_argument("--path", "-p", default=".", help="Path to repository")
    
    args = parser.parse_args()
    
    cmd = ConflictsCommand(args.path)
    cmd.print_report()
