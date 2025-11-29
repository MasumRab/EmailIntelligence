
"""
Git history analysis module.
"""

import asyncio
import re
from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel, Field

from ..utils.logger import get_logger

logger = get_logger(__name__)

class Commit(BaseModel):
    """
    Represents a git commit.
    """
    hash: str
    author: str
    date: datetime
    message: str
    files_changed: List[str] = Field(default_factory=list)
    
    # Analysis fields
    category: Optional[str] = None
    risk_level: Optional[str] = None
    is_merge: bool = False

class GitHistory:
    """
    Handles git history operations.
    """
    
    async def get_commits(self, branch: str = "HEAD", limit: int = 100) -> List[Commit]:
        """
        Get commits from git log.
        """
        # Format: hash|author|iso_date|message
        cmd = f'git log {branch} -n {limit} --pretty=format:"%H|%an|%ad|%s" --date=iso'
        
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await proc.communicate()
        
        if proc.returncode != 0:
            logger.error("Git log failed", error=stderr.decode())
            return []
            
        commits = []
        for line in stdout.decode().splitlines():
            try:
                parts = line.split("|")
                if len(parts) >= 4:
                    commits.append(Commit(
                        hash=parts[0],
                        author=parts[1],
                        date=datetime.fromisoformat(parts[2]),
                        message=parts[3],
                        is_merge=parts[3].startswith("Merge")
                    ))
            except Exception as e:
                logger.warning("Failed to parse commit line", line=line, error=str(e))
                
        return commits
