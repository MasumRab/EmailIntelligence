"""
Git Conflict Detection Module

Implements conflict detection for git repositories.
"""
from enum import Enum
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Optional


class ConflictType(Enum):
    """Types of git conflicts"""
    CONTENT = "content"
    MERGE = "merge"
    FILE_DELETE = "file_delete"
    PERMISSION = "permission"
    BINARY = "binary"


@dataclass
class ConflictBlock:
    """Represents a single conflict block in a file"""
    start_line: int
    end_line: int
    conflict_type: ConflictType
    content_before: List[str]
    content_after: List[str]
    content_common: List[str]


@dataclass
class Conflict:
    """Represents a git conflict"""
    file_path: str
    conflict_blocks: List[ConflictBlock]
    conflict_type: ConflictType
    severity: str  # 'low', 'medium', 'high', 'critical'


class GitConflictDetector:
    """Detects git conflicts in a repository"""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
    
    def detect_conflicts(self) -> List[Conflict]:
        """Detect all conflicts in the repository"""
        conflicts = []
        
        # Look for files with conflict markers
        for file_path in self._get_tracked_files():
            conflict_blocks = self._find_conflict_markers(file_path)
            if conflict_blocks:
                conflict = Conflict(
                    file_path=str(file_path),
                    conflict_blocks=conflict_blocks,
                    conflict_type=ConflictType.CONTENT,
                    severity=self._determine_severity(conflict_blocks)
                )
                conflicts.append(conflict)
        
        return conflicts
    
    def _get_tracked_files(self) -> List[Path]:
        """Get list of tracked files in the repository"""
        import subprocess
        try:
            result = subprocess.run(
                ["git", "ls-files"], 
                cwd=self.repo_path, 
                capture_output=True, 
                text=True, 
                check=True
            )
            return [self.repo_path / f for f in result.stdout.strip().split('\n') if f]
        except subprocess.CalledProcessError:
            return []
    
    def _find_conflict_markers(self, file_path: Path) -> List[ConflictBlock]:
        """Find conflict markers in a file"""
        if not file_path.exists():
            return []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            # Skip binary files
            return []
        
        conflict_blocks = []
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            if line.startswith("<<<<<<<"):
                # Found start of conflict block
                start_line = i
                content_before = []
                content_after = []
                content_common = []
                
                # Collect content before conflict
                j = i + 1
                while j < len(lines):
                    next_line = lines[j].strip()
                    if next_line.startswith("======="):
                        break
                    if next_line.startswith(">>>>>>>"):
                        # Malformed conflict, skip
                        break
                    content_before.append(lines[j])
                    j += 1
                else:
                    # Reached end without finding separator
                    i = j
                    continue
                
                # Collect content after conflict (from ======= to >>>>>>>)
                k = j + 1
                while k < len(lines):
                    next_line = lines[k].strip()
                    if next_line.startswith(">>>>>>>"):
                        break
                    content_after.append(lines[k])
                    k += 1
                else:
                    # Reached end without finding end marker
                    i = k
                    continue
                
                # Create conflict block
                conflict_block = ConflictBlock(
                    start_line=start_line,
                    end_line=k,
                    conflict_type=ConflictType.CONTENT,
                    content_before=content_before,
                    content_after=content_after,
                    content_common=content_common
                )
                conflict_blocks.append(conflict_block)
                
                i = k + 1  # Move past the conflict block
            else:
                i += 1
        
        return conflict_blocks
    
    def _determine_severity(self, conflict_blocks: List[ConflictBlock]) -> str:
        """Determine severity based on conflict characteristics"""
        if len(conflict_blocks) > 5:
            return "high"
        elif len(conflict_blocks) > 2:
            return "medium"
        else:
            return "low"