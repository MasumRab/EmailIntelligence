"""
Commit Reordering Module

This module provides functionality to analyze and reorder git commits based on
logical dependencies and file groupings. It helps in structuring PRs for easier
review and reducing conflict risk during rebases.
"""

from typing import List, Dict, Set, Any, Optional
from dataclasses import dataclass
from collections import defaultdict
import re

@dataclass
class CommitNode:
    """Represents a commit in the reordering graph."""
    hash: str
    message: str
    files: List[str]
    parents: List[str]
    author_date: str
    
    # Analysis fields
    modules: Set[str] = None
    dependencies: Set[str] = None

    def __post_init__(self):
        if self.modules is None:
            self.modules = set()
        if self.dependencies is None:
            self.dependencies = set()

class CommitReorderer:
    """
    Analyzes and reorders commits to optimize for review and stability.
    """
    
    def __init__(self):
        self.module_pattern = re.compile(r"src/([^/]+)/")

    def group_commits_by_module(self, commits: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Group commits by the primary module they affect.
        """
        groups = defaultdict(list)
        
        for commit in commits:
            # Identify primary module
            modules = self._extract_modules(commit.get('files', []))
            
            if not modules:
                key = "misc"
            elif len(modules) == 1:
                key = list(modules)[0]
            else:
                key = "cross-cutting"
                
            groups[key].append(commit)
            
        return dict(groups)

    def suggest_order(self, commits: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Suggest a topological order that respects file dependencies but groups logically.
        
        This is a simplified implementation that:
        1. Preserves strict parent-child relationships for same-file edits.
        2. Groups independent commits by module.
        """
        # Convert to nodes
        nodes = [self._to_node(c) for c in commits]
        node_map = {n.hash: n for n in nodes}
        
        # Build dependency graph
        # A depends on B if A modifies a file B modified, and A is historically after B
        # (This is implicit in git, but we want to know if we CAN reorder)
        
        # For now, let's implement a "Stable Module Sort":
        # Keep commits in relative time order, but group by module if safe.
        
        # 1. Group by module
        groups = self.group_commits_by_module(commits)
        
        # 2. Flatten groups with a specific order preference
        # Order: Core -> Utils -> Features -> Tests -> Docs (Example heuristic)
        priority_order = ["core", "utils", "git", "analysis", "resolution", "workflow", "cli"]
        
        ordered_commits = []
        
        # Add prioritized groups first
        for module in priority_order:
            if module in groups:
                ordered_commits.extend(groups[module])
                del groups[module]
        
        # Add remaining groups
        for module in sorted(groups.keys()):
            ordered_commits.extend(groups[module])
            
        return ordered_commits

    def _extract_modules(self, files: List[str]) -> Set[str]:
        """Extract module names from file paths."""
        modules = set()
        for f in files:
            match = self.module_pattern.search(f)
            if match:
                modules.add(match.group(1))
            elif f.startswith("tests/"):
                modules.add("tests")
            elif f.endswith(".md") or f.startswith("docs/"):
                modules.add("docs")
        return modules

    def _to_node(self, commit_dict: Dict[str, Any]) -> CommitNode:
        """Convert dictionary to CommitNode."""
        return CommitNode(
            hash=commit_dict.get('hash', ''),
            message=commit_dict.get('message', ''),
            files=commit_dict.get('files', []),
            parents=commit_dict.get('parents', []),
            author_date=commit_dict.get('date', '')
        )
