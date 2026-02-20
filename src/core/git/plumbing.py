import subprocess
import re
from typing import List, Optional
from src.core.models.git import ConflictModel, ConflictType, HunkModel

class GitPlumbing:
    """Wrapper for low-level git commands."""
    
    def __init__(self, repo_root: str):
        self.repo_root = repo_root

    def _run(self, args: List[str]) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["git"] + args,
            cwd=self.repo_root,
            capture_output=True,
            text=True
        )

    def cat_file(self, ref: str, path: str) -> str:
        """Get file content from a specific ref."""
        result = self._run(["show", f"{ref}:{path}"])
        if result.returncode != 0:
            raise FileNotFoundError(f"File {path} not found in {ref}")
        return result.stdout

    def merge_tree(self, base: str, head: str) -> str:
        """Run git merge-tree --write-tree."""
        result = self._run(["merge-tree", "--write-tree", base, head])
        # merge-tree might return non-zero if there are conflicts.
        # Combine stdout and stderr just in case.
        return result.stdout + result.stderr

    def parse_merge_tree(self, output: str) -> List[ConflictModel]:
        """Regex-based parser for merge-tree output."""
        conflicts = []
        
        # In --write-tree mode, conflicts are listed after the tree OID
        # and usually start with CONFLICT
        for line in output.splitlines():
            if line.startswith("CONFLICT"):
                # Extract path: CONFLICT (content): Merge conflict in path
                match = re.search(r"in (.*)$", line)
                if match:
                    conflicts.append(ConflictModel(
                        path=match.group(1).strip(),
                        type=ConflictType.CONTENT,
                        oid_base=None,
                        oid_ours=None,
                        oid_theirs=None
                    ))
                
        return conflicts